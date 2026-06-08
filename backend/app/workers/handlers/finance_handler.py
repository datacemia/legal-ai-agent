import json
from collections import Counter

from app.models.job import Job
from app.models.finance_analysis import FinanceAnalysis

from app.services.finance_agent.statement_parser import extract_statement_text_from_path
from app.services.cloud_storage_service import download_api_file_from_cloud
from app.services.finance_agent.finance_ai_agent import analyze_bank_statement
from app.services.finance_agent.transaction_extractor import (
    DEBUG_FINANCE_EXTRACTOR,
    debug_log,
    extract_transactions,
    extract_global_statement_summary,
    append_fx_fee_transactions,
    restore_semantically_valid_kpi_rows,
)
from app.services.finance_agent.subscription_detector import detect_recurring_subscriptions
from app.services.finance_agent.budget_engine import build_recommended_budget
from app.services.finance_agent.forecasting import predict_cashflow
from app.services.finance_agent.scoring import calculate_financial_scores
from app.services.finance_agent.charts_builder import (
    build_financial_charts,
    detect_category,
)
from app.services.finance_agent.savings_opportunities import (
    detect_savings_opportunities,
)
from app.services.finance_agent.insights_engine import (
    generate_financial_insights,
)
from app.services.finance_agent.alerts_engine import (
    generate_financial_alerts,
)

from app.workers.progress import update_job_progress


def apply_standard_own_account_transfer_guard(transactions: list[dict]) -> list[dict]:
    for tx in transactions or []:
        desc = str(tx.get("description") or "").lower()
        typ = str(tx.get("type") or "").lower()

        is_transfer_label = typ in {"transfer", "transfer in", "transfer out"} or "transfer in" in desc or "transfer out" in desc
        is_own_account = (
            "mercury checking" in desc
            or "own account" in desc
            or "between accounts" in desc
            or "internal transfer" in desc
            or "transfer from checking" in desc
            or "transfer to checking" in desc
        )

        if is_transfer_label and is_own_account:
            tx["type"] = "transfer"
            tx["is_internal_transfer"] = True
            tx["excluded_from_financial_kpis"] = True
            tx["exclude_from_income"] = True
            tx["exclude_from_expense"] = True
            tx["exclude_from_score"] = True
            tx["exclude_from_savings"] = True
            tx["exclude_from_cashflow"] = True
            tx["excluded_reason"] = "standard_own_account_transfer"

    return transactions


def get_job_input(job: Job) -> dict:
    """
    Safely read job input data.

    Some code creates jobs using input_data.
    Older code uses input. This supports both.
    """

    data = getattr(job, "input_data", None)

    if data is None:
        data = getattr(job, "input", None)

    if isinstance(data, str):
        try:
            data = json.loads(data)
        except Exception:
            data = {}

    return data if isinstance(data, dict) else {}






def build_observed_finance_summary(
    forecast: dict,
    currency: str,
    output_language: str = "en",
) -> str:
    income = round(
        forecast.get("observed_income", 0) or 0,
        2,
    )
    expenses = round(
        forecast.get("observed_expenses", 0) or 0,
        2,
    )
    net = round(
        forecast.get("observed_net_cashflow", 0) or 0,
        2,
    )

    if output_language == "fr":
        if net < 0:
            return (
                f"Les revenus observés s’élèvent à {income} {currency}, "
                f"tandis que les dépenses observées atteignent {expenses} {currency}. "
                f"La trésorerie nette observée est négative de {abs(net)} {currency}, "
                "ce qui indique que les dépenses dépassent les revenus."
            )

        return (
            f"Les revenus observés s’élèvent à {income} {currency}, "
            f"tandis que les dépenses observées atteignent {expenses} {currency}. "
            f"La trésorerie nette observée est positive de {net} {currency}."
        )

    if output_language == "ar":
        if net < 0:
            return (
                f"بلغ الدخل المرصود {income} {currency}، "
                f"بينما بلغت المصاريف المرصودة {expenses} {currency}. "
                f"صافي التدفق النقدي المرصود سلبي بقيمة {abs(net)} {currency}، "
                "مما يشير إلى أن المصاريف تتجاوز الدخل."
            )

        return (
            f"بلغ الدخل المرصود {income} {currency}، "
            f"بينما بلغت المصاريف المرصودة {expenses} {currency}. "
            f"صافي التدفق النقدي المرصود إيجابي بقيمة {net} {currency}."
        )

    if net < 0:
        return (
            f"Observed income is {income} {currency}, "
            f"while observed expenses are {expenses} {currency}. "
            f"Observed net cashflow is negative by {abs(net)} {currency}, "
            "which indicates that expenses exceed income."
        )

    return (
        f"Observed income is {income} {currency}, "
        f"while observed expenses are {expenses} {currency}. "
        f"Observed net cashflow is positive by {net} {currency}."
    )


def deduplicate_transactions(
    transactions: list[dict],
) -> list[dict]:
    seen = set()
    unique = []

    for tx in transactions:
        key = (
            tx.get("date"),
            tx.get("description"),
            round(
                float(tx.get("amount", 0)),
                2,
            ),
        )

        if key in seen:
            continue

        seen.add(key)
        unique.append(tx)

    return unique



def observed_income_from_transactions(
    transactions: list[dict],
) -> float:
    """Return positive income already visible in extracted transactions.

    This prevents downstream forecast/budget engines from adding an AI income
    fallback on top of real extracted income. The fallback remains available
    for statements where no income transaction was extracted.
    """
    total = 0.0

    for tx in transactions:
        try:
            amount = float(tx.get("amount") or 0)
        except Exception:
            continue

        if amount > 0:
            total += amount

    return round(total, 2)


def resolve_finance_currency(
    result_ai: dict,
    transactions: list[dict],
) -> str:
    """Resolve currency without hardcoding a country-specific fallback.

    Priority:
    1) AI-detected currency if explicit and not unknown.
    2) Most common non-unknown currency from extracted transactions.
    3) unknown.
    """
    currency = result_ai.get("currency_detected")

    if currency not in [None, "", "unknown"]:
        return str(currency).upper()

    detected = [
        str(tx.get("currency")).upper()
        for tx in transactions
        if tx.get("currency")
        and str(tx.get("currency")).lower() != "unknown"
    ]

    if detected:
        return Counter(detected).most_common(1)[0][0]

    return "unknown"


def get_finance_disclaimer(output_language: str = "en") -> str:
    disclaimers = {
        "en": (
            "This analysis is for informational purposes only "
            "and should not be considered financial advice."
        ),
        "fr": (
            "Cette analyse est fournie à titre informatif uniquement "
            "et ne constitue pas un conseil financier."
        ),
        "ar": (
            "هذا التحليل لأغراض معلوماتية فقط "
            "ولا يُعتبر نصيحة مالية."
        ),
    }

    return disclaimers.get(output_language, disclaimers["en"])


def safe_float(value: object) -> float:
    try:
        return float(value or 0)
    except (TypeError, ValueError):
        return 0.0


def contains_any_text(value: object, keywords: set[str]) -> bool:
    normalized = str(value or "").lower()

    return any(
        keyword in normalized
        for keyword in keywords
    )


def filter_metric_inconsistent_items(
    items: list,
    *,
    subscription_ratio: float,
    expense_ratio: float,
    savings_rate: float,
) -> list:
    subscription_terms = {
        "subscription",
        "subscriptions",
        "abonnement",
        "abonnements",
        "اشتراك",
        "اشتراكات",
    }

    increase_savings_terms = {
        "increase savings",
        "savings contribution",
        "savings contributions",
        "augmenter l’épargne",
        "augmenter l'epargne",
        "augmenter les contributions d’épargne",
        "augmenter les contributions d'epargne",
        "زيادة الادخار",
        "مساهمات الادخار",
    }

    reduce_spending_terms = {
        "reduce spending",
        "reduce discretionary spending",
        "reduce expenses",
        "réduire les dépenses",
        "reduire les depenses",
        "réduire les dépenses discrétionnaires",
        "reduire les depenses discretionnaires",
        "تقليل الإنفاق",
        "خفض الإنفاق",
        "تقليل المصاريف",
        "خفض المصاريف",
    }

    filtered = []

    for item in items or []:
        text = str(item or "").strip()

        if not text:
            continue

        if (
            subscription_ratio <= 0.05
            and contains_any_text(text, subscription_terms)
        ):
            continue

        if (
            savings_rate >= 0.15
            and contains_any_text(text, increase_savings_terms)
        ):
            continue

        if (
            expense_ratio <= 0.75
            and savings_rate >= 0.15
            and contains_any_text(text, reduce_spending_terms)
        ):
            continue

        filtered.append(item)

    return filtered




def assess_analysis_quality(transactions: list[dict]) -> dict:
    """Assess extraction quality from transaction structure, not category success.

    International standard rule:
    - Parsing quality is based on valid transaction structure: date, amount,
      description and usable type.
    - Categorization quality is reported separately as `other_ratio`.
    - A bank statement must not be rejected only because many merchants or
      transfers are classified as `other`.

    This keeps Arabic / French / English statements valid even when merchant
    names, bank references, SWIFT/IBAN references or OCR fragments are unknown.
    """
    MIN_TRANSACTIONS = 5
    PARTIAL_STRUCTURE_RATIO = 0.50
    VERIFIED_STRUCTURE_RATIO = 0.75
    PARTIAL_TYPED_RATIO = 0.45
    VERIFIED_TYPED_RATIO = 0.65

    total_count = len(transactions or [])

    if total_count <= 0:
        return {
            "status": "insufficient_data",
            "confidence": 25,
            "other_ratio": 0,
            "transaction_count": 0,
            "valid_transaction_count": 0,
            "structure_ratio": 0,
            "typed_ratio": 0,
            "income_count": 0,
            "expense_count": 0,
        }

    valid_count = 0
    typed_count = 0
    income_count = 0
    expense_count = 0
    total_expenses = 0.0
    other_expenses = 0.0

    for tx in transactions:
        try:
            amount = float(tx.get("amount") or 0)
        except Exception:
            amount = 0.0

        description = str(tx.get("description") or "").strip()
        date = str(tx.get("date") or "").strip()
        tx_type = str(tx.get("type") or "").lower().strip()

        has_valid_amount = amount != 0
        has_description = bool(description)
        has_date = bool(date)

        if has_date and has_valid_amount and has_description:
            valid_count += 1

        if tx_type in ["income", "expense"]:
            typed_count += 1

        if tx_type == "income" and amount > 0:
            income_count += 1

        if tx_type == "expense" and amount < 0:
            expense_count += 1
            abs_amount = abs(amount)
            total_expenses += abs_amount

            category = str(
                tx.get("category")
                or detect_category(description)
            ).lower()

            if category in ["other", "autres", "أخرى"]:
                other_expenses += abs_amount

    structure_ratio = valid_count / total_count if total_count else 0
    typed_ratio = typed_count / total_count if total_count else 0
    other_ratio = other_expenses / total_expenses if total_expenses > 0 else 0

    short_but_clean_statement = (
        total_count >= 3
        and structure_ratio >= 0.95
        and typed_ratio >= 0.95
        and (income_count + expense_count) == total_count
    )

    if (
        (total_count < MIN_TRANSACTIONS and not short_but_clean_statement)
        or structure_ratio < PARTIAL_STRUCTURE_RATIO
    ):
        status = "insufficient_data"
        confidence = 25
    elif structure_ratio < VERIFIED_STRUCTURE_RATIO or typed_ratio < PARTIAL_TYPED_RATIO:
        status = "partial"
        confidence = 65
    elif typed_ratio < VERIFIED_TYPED_RATIO:
        status = "partial"
        confidence = 75
    else:
        status = "verified"
        confidence = 90

    # Category coverage is useful, but should not downgrade a structurally valid
    # statement to insufficient_data. Apply only a small confidence adjustment.
    if status == "verified" and other_ratio > 0.70:
        confidence = 80
    elif status == "verified" and other_ratio > 0.50:
        confidence = 85

    detected_count = sum(
        1
        for tx in transactions or []
        if tx.get("type") == "transfer"
        or tx.get("is_internal_transfer")
        or tx.get("excluded_from_financial_kpis")
    )

    debug_log(
        "INTERNAL_TRANSFER_STATS",
        {
            "detected": detected_count,
            "total": len(transactions or []),
        }
    )

    return {
        "status": status,
        "confidence": confidence,
        "other_ratio": round(other_ratio, 4),
        "transaction_count": total_count,
        "valid_transaction_count": valid_count,
        "structure_ratio": round(structure_ratio, 4),
        "typed_ratio": round(typed_ratio, 4),
        "income_count": income_count,
        "expense_count": expense_count,
    }




def ensure_signed_amount(tx: dict) -> None:
    """Canonical money invariant: signed_amount must mirror the KPI amount.

    Balance is never a movement amount. Exclusion flags may remove a row from
    KPI totals, but they must not destroy the original type/amount/signed value,
    because audits, quality checks and debugging rely on those fields.
    """
    if tx.get("signed_amount") is not None:
        return

    amount = safe_float(tx.get("amount"))
    if amount != 0:
        tx["signed_amount"] = amount


def exclude_from_financial_kpis(tx: dict, reason: str) -> dict:
    """Mark a transaction as excluded without deleting financial evidence."""
    tx["excluded_from_financial_kpis"] = True
    tx["exclude_from_income"] = True
    tx["exclude_from_expense"] = True
    tx["exclude_from_score"] = True
    tx["exclude_from_savings"] = True
    tx["exclude_from_cashflow"] = True
    tx["category_hint"] = tx.get("category_hint") or reason
    tx["exclusion_reason"] = reason
    return tx

def finance_progress_message(key: str, language: str) -> str:
    messages = {
        "loading": {
            "en": "Loading bank statement...",
            "fr": "Chargement du relevé bancaire...",
            "ar": "جارٍ تحميل كشف الحساب البنكي...",
        },
        "extracting": {
            "en": "Extracting bank statement text...",
            "fr": "Extraction du texte du relevé bancaire...",
            "ar": "جارٍ استخراج نص كشف الحساب البنكي...",
        },
        "transactions": {
            "en": "Reading visible transactions...",
            "fr": "Lecture des transactions visibles...",
            "ar": "جارٍ قراءة المعاملات الظاهرة...",
        },
        "spending": {
            "en": "Analyzing spending patterns...",
            "fr": "Analyse des habitudes de dépense...",
            "ar": "جارٍ تحليل أنماط الإنفاق...",
        },
        "subscriptions": {
            "en": "Detecting recurring subscriptions...",
            "fr": "Détection des abonnements récurrents...",
            "ar": "جارٍ كشف الاشتراكات المتكررة...",
        },
        "budget": {
            "en": "Building recommended budget...",
            "fr": "Construction du budget recommandé...",
            "ar": "جارٍ بناء الميزانية المقترحة...",
        },
        "forecast": {
            "en": "Generating cashflow forecast...",
            "fr": "Génération des prévisions de cashflow...",
            "ar": "جارٍ إنشاء توقعات التدفق النقدي...",
        },
        "insights": {
            "en": "Generating AI financial insights...",
            "fr": "Génération des insights financiers IA...",
            "ar": "جارٍ إنشاء الرؤى المالية الذكية...",
        },
        "charts": {
            "en": "Preparing financial charts...",
            "fr": "Préparation des graphiques financiers...",
            "ar": "جارٍ إعداد الرسوم المالية...",
        },
        "saving": {
            "en": "Saving financial analysis...",
            "fr": "Enregistrement de l’analyse financière...",
            "ar": "جارٍ حفظ التحليل المالي...",
        },
        "finalizing": {
            "en": "Finalizing AI financial report...",
            "fr": "Finalisation du rapport financier IA...",
            "ar": "جارٍ إنهاء التقرير المالي الذكي...",
        },
    }

    if language not in ["en", "fr", "ar"]:
        language = "en"

    return messages.get(key, {}).get(
        language,
        messages.get(key, {}).get("en", key),
    )



def normalize_signed_amounts_before_kpi(transactions):
    normalized = []
    for tx in transactions or []:
        if not isinstance(tx, dict):
            continue
        try:
            amount = float(tx.get("amount") or 0)
        except Exception:
            amount = 0.0
        if tx.get("signed_amount") is None:
            tx["signed_amount"] = amount
        if tx.get("_locked_amount") is None:
            tx["_locked_amount"] = tx["signed_amount"]
        if tx.get("locked_amount") is None:
            tx["locked_amount"] = tx["signed_amount"]
        normalized.append(tx)
    return normalized


print("RUNEXA_FINANCE_HANDLER_VERSION", "v2-global-absurd-guard")

def handle_finance_ai(job: Job, db):
    input_data = get_job_input(job)

    file_path = input_data.get("file_path")
    file_bytes_hex = input_data.get("file_bytes")
    storage_path = input_data.get("storage_path")

    file_name = input_data.get("file_name")
    user_id = input_data.get("user_id")
    output_language = input_data.get("output_language", "en")
    access_type = input_data.get("access_type")
    credits_used = input_data.get("credits_used", 0)

    if output_language not in ["en", "fr", "ar"]:
        output_language = "en"

    if not file_path and not file_bytes_hex and not storage_path:
        raise ValueError(
            "file_path, file_bytes, or storage_path is required for finance analysis job"
        )

    if not file_name:
        file_name = "bank_statement.pdf"

    if not user_id:
        raise ValueError("user_id is required for finance analysis job")

    update_job_progress(
        job,
        db,
        10,
        finance_progress_message("loading", output_language),
    )

    if not str(file_name).lower().endswith(".pdf"):
        raise ValueError("Only PDF bank statements are allowed.")

    update_job_progress(
        job,
        db,
        20,
        finance_progress_message("extracting", output_language),
    )

    if file_bytes_hex:
        content = bytes.fromhex(file_bytes_hex)

        from app.services.finance_agent.statement_parser import (
            extract_statement_text,
        )

        class BytesUpload:
            async def read(self):
                return content

        import asyncio

        text = asyncio.run(
            extract_statement_text(BytesUpload())
        )

    else:
        if storage_path:
            file_path = download_api_file_from_cloud(
                storage_path=str(storage_path),
                suffix=".pdf",
            )

        text = extract_statement_text_from_path(str(file_path))

    if not text or len(text.strip()) < 100:
        raise ValueError(
            "Could not extract text from PDF. "
            "This PDF appears to be scanned and requires OCR."
        )

    update_job_progress(
        job,
        db,
        32,
        finance_progress_message("transactions", output_language),
    )

    transactions = extract_transactions(text)
    transactions = append_fx_fee_transactions(transactions)
    transactions = apply_standard_own_account_transfer_guard(transactions)
    transactions = restore_semantically_valid_kpi_rows(transactions)

    # International FR/EN/AR rule:
    # Exclude daily-balance-summary rows from KPI while keeping real transactions.
    balance_summary_only_rows = []
    filtered_transactions = []
    for tx in transactions:
        desc = str(tx.get("description") or tx.get("desc") or "")
        compact = desc.strip()

        is_balance_summary_row = False

        # TD/US pattern: "06105 164,852.27 06/25 116,152.40"
        # means DATE BALANCE DATE BALANCE, not a transaction.
        import re
        if re.match(
            r"^(?:\d{5}|\d{2}/\d{2})\s+[-+]?\d{1,3}(?:,\d{3})*\.\d{2}"
            r"(?:\s+(?:\d{5}|\d{2}/\d{2})\s+[-+]?\d{1,3}(?:,\d{3})*\.\d{2})?$",
            compact,
        ):
            is_balance_summary_row = True

        if is_balance_summary_row:
            tx["excluded_from_financial_kpis"] = True
            tx["excluded_reason"] = "daily_balance_summary_row"
            balance_summary_only_rows.append({
                "date": tx.get("date"),
                "amount": tx.get("amount"),
                "balance": tx.get("balance") or tx.get("_balance"),
                "desc": compact[:120],
            })
            continue

        filtered_transactions.append(tx)

    if balance_summary_only_rows:
        print(
            "DAILY_BALANCE_SUMMARY_ROWS_EXCLUDED",
            {
                "count": len(balance_summary_only_rows),
                "samples": balance_summary_only_rows[:10],
            },
        )

    transactions = filtered_transactions

    # International FR/EN/AR rule:
    # Opening / brought-forward balance rows are not transactions.
    opening_balance_rows = []
    filtered_transactions = []

    import re
    opening_balance_re = re.compile(
        r"(\bB/F\b|\bBF\b|BROUGHT\s+FORWARD|BALANCE\s+BROUGHT\s+FORWARD|"
        r"OPENING\s+BALANCE|BEGINNING\s+BALANCE|SOLDE\s+INITIAL|SOLDE\s+D[ÉE]BUT|"
        r"REPORT\s+[ÀA]\s+NOUVEAU|رصيد\s+افتتاحي|الرصيد\s+الافتتاحي|رصيد\s+سابق)",
        re.IGNORECASE,
    )

    for tx in transactions:
        desc = str(tx.get("description") or tx.get("desc") or "")
        if opening_balance_re.search(desc):
            tx["excluded_from_financial_kpis"] = True
            tx["excluded_reason"] = "opening_or_brought_forward_balance"
            opening_balance_rows.append({
                "date": tx.get("date"),
                "amount": tx.get("amount"),
                "balance": tx.get("balance") or tx.get("_balance"),
                "desc": desc[:140],
            })
            continue

        filtered_transactions.append(tx)

    if opening_balance_rows:
        print(
            "OPENING_BALANCE_ROWS_EXCLUDED",
            {
                "count": len(opening_balance_rows),
                "samples": opening_balance_rows[:10],
            },
        )

    transactions = filtered_transactions

    # Do not deduplicate bank transactions by content.
    # Two real bank operations can have the same date, description and amount.
    # Example: two ATM withdrawals of 2 000 MAD on the same day.
    transactions = list(transactions)

    def audit_tx_stage(stage: str, txs: list[dict]):
        print(
            stage,
            [
                {
                    "i": i,
                    "date": tx.get("date"),
                    "amount": tx.get("amount"),
                    "locked": tx.get("_locked_amount"),
                    "signed": tx.get("signed_amount"),
                    "balance": tx.get("balance") or tx.get("_balance"),
                    "type": tx.get("type"),
                    "desc": str(tx.get("description") or "")[:80],
                }
                for i, tx in enumerate(txs[:50])
            ],
        )

    audit_tx_stage("TX_STAGE_1_AFTER_EXTRACT", transactions)

    print(
        "INCOME_AUDIT",
        [
            {
                "date": tx.get("date"),
                "amount": tx.get("amount"),
                "type": tx.get("type"),
                "description": tx.get("description"),
            }
            for tx in transactions
            if tx.get("amount", 0) > 0
        ][:50]
    )


    # Canonicalize transactions BEFORE any quality/KPI/budget/forecast/chart usage.
    # International FR / EN / AR rule:
    # amount/signed_amount = real transaction movement
    # balance/_balance = account balance only, never used as KPI amount.
    for tx in transactions:
        locked_amount = tx.get("_locked_amount")

        if locked_amount is not None:
            tx["amount"] = locked_amount
            tx["signed_amount"] = locked_amount

        # Standard international FR / EN / AR rule:
        # amount/balance ledger rows must never become income only because
        # their visible movement amount is positive. Only balance-delta locked
        # rows may participate in KPI totals.
        if (
            tx.get("_balance") is not None
            and not tx.get("_balance_locked")
            and tx.get("parser_family") != "running_balance_column_statement"
        ):
            # Do not destroy amount/type/signed_amount. This row may be excluded
            # from KPI totals, but audit must preserve the extracted evidence.
            ensure_signed_amount(tx)
            exclude_from_financial_kpis(tx, "unlocked_amount_balance_row")
            tx["untrusted_balance_row"] = True
            continue

        ensure_signed_amount(tx)

        if tx.get("type") is None:
            amount = safe_float(tx.get("signed_amount", tx.get("amount")))

            if amount > 0:
                tx["type"] = "income"
            elif amount < 0:
                tx["type"] = "expense"

    transactions = normalize_signed_amounts_before_kpi(transactions)


    # Global international safety guard before KPI/canonical audit.
    # FR/EN/AR: protect against references, cheque numbers, totals, balances,
    # and OCR-fused identifiers becoming financial movements.
    import re

    def is_global_non_transaction_amount(tx):
        desc = str(tx.get("description") or tx.get("desc") or "")
        upper = desc.upper()
        amount = abs(float(tx.get("amount") or 0))

        # 1) Cheque/check/chq number fused with amount:
        # CHEQUE 458 + 150,00 -> 458150.00
        cheque_like = re.search(
            r"\b(CH[EÈ]QUE|CHEQUE|CHECK|CHQ|CHK|شيك|صك)\b",
            upper,
            re.IGNORECASE,
        )
        desc_has_only_cheque_word = cheque_like and len(re.findall(r"[A-Za-zÀ-ÿ\u0600-\u06FF]+", desc)) <= 2

        if cheque_like and amount >= 100000 and desc_has_only_cheque_word:
            return "cheque_number_amount_fusion"

        # 2) Totals / movement summaries are not transactions.
        # Strict total-summary detection only.
        # Do not exclude normal transactions containing REF / MOTIF / ID.
        if re.search(
            r"(TOTAUX?\s+DES\s+MOUVEMENTS|TOTAL\s+MOVEMENTS?|TOTAL\s+DEBITS?|TOTAL\s+CREDITS?|"
            r"TOTAL\s+DES\s+OP[ÉE]RATIONS|TOTAL\s+TRANSACTIONS?|MOUVEMENTS\s+DU\s+MOIS|"
            r"مجموع\s+الحركات|إجمالي\s+الحركات|اجمالي\s+الحركات)",
            upper,
            re.IGNORECASE,
        ):
            return "statement_total_or_summary_row"

        # 3) Opening / brought-forward balances are not transactions.
        if re.search(
            r"(\bB/F\b|\bBF\b|BROUGHT\s+FORWARD|BALANCE\s+BROUGHT\s+FORWARD|"
            r"OPENING\s+BALANCE|BEGINNING\s+BALANCE|SOLDE\s+INITIAL|SOLDE\s+D[ÉE]BUT|"
            r"REPORT\s+[ÀA]\s+NOUVEAU|رصيد\s+افتتاحي|الرصيد\s+الافتتاحي|رصيد\s+سابق)",
            upper,
            re.IGNORECASE,
        ):
            return "opening_or_brought_forward_balance"

        # 4) Value-date-only rows are metadata, not transactions.
        if re.search(
            r"(VALUE\s+DATE|DATE\s+VALEUR|تاريخ\s+القيمة)",
            upper,
            re.IGNORECASE,
        ) and len(re.findall(r"[A-Za-zÀ-ÿ\u0600-\u06FF]+", desc)) <= 4:
            return "value_date_metadata_row"

        # 5) Generic absurd amount guard:
        # Global FR/EN/AR rule:
        # A high amount is NOT absurd if the row has trusted transaction verbs.
        trusted_transaction_signal = re.search(
            r"(DEPOT|D[ÉE]P[ÔO]T|DEPOSIT|CASH\s+DEPOSIT|VERSEMENT|VERST|EPARGNE|[ÉE]PARGNE|"
            r"RETRAIT|WITHDRAWAL|VIREMENT|TRANSFER|CHEQUE|CH[EÈ]QUE|CHECK|CHQ|"
            r"إيداع|ايداع|سحب|تحويل|شيك|صك)",
            upper,
            re.IGNORECASE,
        )

        if trusted_transaction_signal:
            return None

        # 5) Generic absurd amount guard:
        # huge amount + weak description = likely ID/reference/balance/OCR fusion.
        strong_tx_words = re.search(
            r"(CARTE|CARD|PAYMENT|PAIEMENT|VIREMENT|VIR\s+RECU|VIR\s+EMIS|TRANSFER|"
            r"PRELEVEMENT|PR[ÉE]L[ÈE]VEMENT|ATM|RETRAIT|DAB|DEPOSIT|DEPOT|D[ÉE]P[ÔO]T|"
            r"VERSEMENT|VERST|EPARGNE|[ÉE]PARGNE|SAVINGS|CASH\s+DEPOSIT|"
            r"SALAIRE|SALARY|INVOICE|FACTURE|رسوم|تحويل|دفع|سحب|إيداع|ادخار|توفير)",
            upper,
            re.IGNORECASE,
        )
        if amount >= 100000 and not strong_tx_words:
            return "absurd_amount_weak_description"

        return None

    global_guard_excluded = []
    kept_transactions = []

    for tx in transactions:
        reason = is_global_non_transaction_amount(tx)
        if reason:
            tx["excluded_from_financial_kpis"] = True
            tx["excluded_reason"] = reason
            tx["exclude_from_income"] = True
            tx["exclude_from_expense"] = True
            tx["exclude_from_score"] = True
            tx["exclude_from_savings"] = True
            tx["exclude_from_cashflow"] = True
            global_guard_excluded.append({
                "date": tx.get("date"),
                "amount": tx.get("amount"),
                "type": tx.get("type"),
                "reason": reason,
                "desc": (tx.get("description") or tx.get("desc") or "")[:160],
            })
            continue
        kept_transactions.append(tx)

    if global_guard_excluded:
        print(
            "GLOBAL_NON_TRANSACTION_AMOUNT_GUARD",
            {
                "count": len(global_guard_excluded),
                "samples": global_guard_excluded[:20],
            },
        )

    transactions = kept_transactions


    # Enterprise international quality batch: FR / EN / AR.
    import re
    from datetime import datetime

    def description_has_min_signal(tx):
        desc = str(tx.get("description") or tx.get("desc") or "")
        cleaned = re.sub(r"[/\\|:_*.,;()\\-]+", " ", desc)
        cleaned = re.sub(r"\b(20\d{2}|\d{1,2}/\d{1,2}/?\d{0,4}|SAR|EUR|USD|MAD|GBP|AED)\b", " ", cleaned, flags=re.I)
        cleaned = re.sub(r"\s+", " ", cleaned).strip()

        strong_markers = re.search(
            r"(CARD|CARTE|MADA|مدى|PAYMENT|PAIEMENT|VIREMENT|TRANSFER|تحويل|"
            r"DEPOSIT|DEPOT|D[ÉE]P[ÔO]T|إيداع|WITHDRAWAL|RETRAIT|سحب|ATM|DAB|"
            r"SADAD|VAT|FEE|FEES|CHARGE|رسوم|ضريبة|MERCHANT|CITY|BANK|IBAN|CARD:|"
            r"CREDIT CARD|PRELEVEMENT|PR[ÉE]L[ÈE]VEMENT)",
            desc,
            re.I,
        )

        words = re.findall(r"[A-Za-zÀ-ÿ\u0600-\u06FF]{3,}", cleaned)
        digits = re.findall(r"\d{4,}", cleaned)

        # Real-world safe signals:
        # - sender/beneficiary-only rows: "De BADLYZ", "From X", Arabic sender markers
        # - cheque/check rows with normal amounts: "CHEQUE 459" + amount 70.00
        sender_marker = re.search(r"\b(DE|FROM|PAR|BY|من|إلى|الى)\b\s+\S+", desc, re.I)
        cheque_marker = re.search(r"\b(CH[EÈ]QUE|CHEQUE|CHECK|CHQ|CHK|شيك|صك)\b\s*\d{1,8}\b", desc, re.I)

        return bool(strong_markers or sender_marker or cheque_marker or len(words) >= 2 or digits)

    def is_global_non_transaction_statement_row(tx: dict) -> bool:
        desc = str(tx.get("description") or tx.get("desc") or "").lower()

        patterns = [
            "interest rate",
            "interest rates",
            "credit interest",
            "debit interest",
            "automatic limit",
            "excess @",
            "p.a.",
            "p.a",
            "tier 1",
            "tier 2",
            "opening balance",
            "closing balance",
            "brought forward",
            "carried forward",
            "total debits",
            "total credits",
            "statement number",
            "account number",
            "page 1 of",
            "page 2 of",
            "page 3 of",
        ]

        return any(p in desc for p in patterns)

    weak_desc_excluded = []
    kept_transactions = []

    for tx in transactions:
        amount = abs(float(tx.get("amount") or 0))

        if is_global_non_transaction_statement_row(tx):
            tx["excluded_from_financial_kpis"] = True
            tx["excluded_reason"] = "global_non_transaction_statement_row"
            weak_desc_excluded.append({
                "date": tx.get("date"),
                "amount": tx.get("amount"),
                "type": tx.get("type"),
                "desc": (tx.get("description") or tx.get("desc") or "")[:160],
            })
            continue

        # Typed table rows are already structurally validated by parser family:
        # DATE + TYPE + AMOUNT + NET AMOUNT.
        # Do not drop them only because OCR lost/shortened description text.
        if (
            tx.get("parser_family") == "typed_transaction_table_statement"
            and tx.get("type") in {"income", "expense", "transfer"}
            and tx.get("amount") is not None
            and tx.get("locked_amount") is not None
        ):
            kept_transactions.append(tx)
            continue

        if amount > 0 and not description_has_min_signal(tx):
            tx["excluded_from_financial_kpis"] = True
            tx["excluded_reason"] = "min_description_signal_guard"
            weak_desc_excluded.append({
                "date": tx.get("date"),
                "amount": tx.get("amount"),
                "type": tx.get("type"),
                "desc": (tx.get("description") or tx.get("desc") or "")[:160],
            })
            continue
        kept_transactions.append(tx)

    if weak_desc_excluded:
        print("MIN_DESCRIPTION_SIGNAL_GUARD", {
            "count": len(weak_desc_excluded),
            "samples": weak_desc_excluded[:20],
        })

    transactions = kept_transactions

    def parse_tx_date_safe(value):
        s = str(value or "")
        for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%d-%m-%Y", "%m-%d-%Y"):
            try:
                return datetime.strptime(s, fmt)
            except Exception:
                pass
        return None

    parsed_dates = [parse_tx_date_safe(tx.get("date")) for tx in transactions]
    parsed_dates = [d for d in parsed_dates if d is not None]

    if len(parsed_dates) >= 3:
        asc = sum(1 for a, b in zip(parsed_dates, parsed_dates[1:]) if b >= a)
        desc = sum(1 for a, b in zip(parsed_dates, parsed_dates[1:]) if b < a)
        order = "ascending" if asc > desc else "descending" if desc > asc else "mixed"

        print("STATEMENT_ORDER_DETECTION", {
            "order": order,
            "ascending_pairs": asc,
            "descending_pairs": desc,
            "dated_transactions": len(parsed_dates),
        })

        # Smart international date-order audit.
        # FR/EN/AR: detect if ambiguous DD/MM vs MM/DD dates are likely mixed.
        # Audit-only: does not mutate transactions yet.
        ambiguous = []
        for tx in transactions:
            raw_date = str(tx.get("date") or "")
            m = re.match(r"^2024-(\d{2})-(\d{2})$", raw_date)
            if not m:
                continue
            mm = int(m.group(1))
            dd = int(m.group(2))
            if 1 <= mm <= 12 and 1 <= dd <= 12:
                ambiguous.append(raw_date)

        if ambiguous:
            print("SMART_DATE_ORDER_SELECTION", {
                "mode": "audit_only",
                "ambiguous_dates": len(ambiguous),
                "samples": ambiguous[:20],
                "current_order": order,
                "note": "candidate for DD/MM vs MM/DD normalization",
            })

    cc_rows = []
    cc_seen = {}

    for tx in transactions:
        desc = str(tx.get("description") or tx.get("desc") or "")
        if re.search(r"(DEPOSIT\s+FROM\s+CREDIT\s+CARD|CREDIT\s+CARD\s+PAYMENT|CARD:|carte\s+cr[ée]dit|بطاقة\s+ائتمان)", desc, re.I):
            key = (
                tx.get("date"),
                round(float(tx.get("amount") or 0), 2),
                re.sub(r"\d", "0", desc[:80]).lower(),
            )
            cc_seen[key] = cc_seen.get(key, 0) + 1
            cc_rows.append({
                "date": tx.get("date"),
                "amount": tx.get("amount"),
                "type": tx.get("type"),
                "desc": desc[:120],
            })

    repeated_cc = [
        {"key": str(k), "count": v}
        for k, v in cc_seen.items()
        if v >= 2
    ]

    if cc_rows:
        print("REPEATED_CREDIT_CARD_DEPOSIT_AUDIT", {
            "rows": len(cc_rows),
            "repeated_patterns": repeated_cc[:20],
            "samples": cc_rows[:20],
            "action": "audit_only_no_automatic_exclusion",
        })

    audit_tx_stage("TX_STAGE_2_AFTER_CANONICALIZE", transactions)


    print(
        "TX_BEFORE_QUALITY_CHECK",
        {
            "count": len(transactions),
            "income": sum(1 for tx in transactions if tx.get("type") == "income"),
            "expense": sum(1 for tx in transactions if tx.get("type") == "expense"),
        },
    )

    for tx in transactions:
        desc = str(tx.get("description") or "")
        if any(x in desc for x in ["اعاده", "اعادة", "ﺍﻋﺎﺩﻩ", "refund", "reversal"]):
            print(
                "REFUND_ROW_BEFORE_QUALITY_CHECK",
                {
                    "amount": tx.get("amount"),
                    "type": tx.get("type"),
                    "locked": tx.get("locked_type"),
                    "signed": tx.get("signed_amount"),
                    "desc": desc[:300],
                },
            )

    quality = assess_analysis_quality(transactions)

    # Hotfix international FR/EN/AR:
    # Restore valid income/expense rows wrongly excluded by balance heuristics
    # immediately before KPI filtering.
    for tx in transactions:
        if (
            tx.get("excluded_from_financial_kpis")
            and tx.get("type") in {"income", "expense"}
            and tx.get("signed_amount") is not None
            and abs(float(tx.get("amount") or 0)) > 0
            and not tx.get("is_internal_transfer")
        ):
            tx["excluded_from_financial_kpis"] = False
            tx["exclude_from_income"] = False if tx.get("type") == "income" else True
            tx["exclude_from_expense"] = False if tx.get("type") == "expense" else True
            tx["exclude_from_score"] = False
            tx["exclude_from_savings"] = False
            tx["exclude_from_cashflow"] = False
            tx.pop("excluded_reason", None)
            tx["category_hint"] = "restored_valid_kpi_row_before_filter"

    # International KPI filter:
    # Internal transfers must never affect income, expenses,
    # savings, scores, forecasts or charts.
    kpi_transactions = [
        tx
        for tx in transactions
        if not (
            tx.get("type") == "transfer"
            or tx.get("is_internal_transfer")
            or tx.get("excluded_from_financial_kpis")
        )
    ]


    kpi_transactions = normalize_signed_amounts_before_kpi(kpi_transactions)

    # International sanity guard:
    # Bank statement transaction amounts should not be absurdly larger than
    # the local running balance or common retail/business transaction scale.
    sane_kpi_transactions = []
    absurd_amounts = []

    for tx in kpi_transactions:
        try:
            amount_abs = abs(float(tx.get("amount") or 0))
            balance_abs = abs(float(tx.get("balance") or tx.get("_balance") or 0))
        except Exception:
            sane_kpi_transactions.append(tx)
            continue

        desc = str(tx.get("description") or tx.get("desc") or "")
        upper = desc.upper()

        trusted_transaction_signal = re.search(
            r"(DEPOT|D[ÉE]P[ÔO]T|DEPOSIT|CASH\\s+DEPOSIT|VERSEMENT|VERST|EPARGNE|[ÉE]PARGNE|"
            r"RETRAIT|WITHDRAWAL|VIREMENT|TRANSFER|CHEQUE|CH[EÈ]QUE|CHECK|CHQ|"
            r"PAIEMENT|PAYMENT|CARTE|CARD|ATM|DAB|FRAIS|FEE|FEES|COMMISSION|TAXE|TAX|"
            r"إيداع|ايداع|سحب|تحويل|شيك|صك|دفع|بطاقة|رسوم|عمولة|ضريبة)",
            upper,
            re.IGNORECASE,
        )

        weak_description = len(re.findall(r"[A-Za-zÀ-ÿ\\u0600-\\u06FF]+", desc)) <= 2

        is_absurd = (
            (
                amount_abs >= 1_000_000
                and not trusted_transaction_signal
                and weak_description
            )
            or (
                balance_abs > 0
                and amount_abs > balance_abs * 20
                and amount_abs > 10_000
                and not trusted_transaction_signal
            )
        )

        if is_absurd:
            tx["excluded_from_financial_kpis"] = True
            tx["excluded_reason"] = "absurd_amount_guard"
            absurd_amounts.append({
                "date": tx.get("date"),
                "amount": tx.get("amount"),
                "balance": tx.get("balance") or tx.get("_balance"),
                "type": tx.get("type"),
                "desc": (tx.get("description") or tx.get("desc") or "")[:120],
            })
            continue

        sane_kpi_transactions.append(tx)

    if absurd_amounts:
        print(
            "ABSURD_AMOUNT_GUARD",
            {
                "count": len(absurd_amounts),
                "samples": absurd_amounts[:10],
            },
        )

    kpi_transactions = sane_kpi_transactions

    audit_tx_stage("TX_STAGE_3_KPI_TRANSACTIONS_CREATED", kpi_transactions)

    print("QUALITY_CHECK")
    print(quality)

    # Global FR/EN/AR statement-vs-ledger reconciliation audit.
    # Audit only: never mutates KPI transactions, never creates synthetic rows.
    try:
        statement_summary = extract_global_statement_summary(text)
    except Exception:
        statement_summary = {}

    if statement_summary:
        statement_deposits = statement_summary.get("deposits")
        statement_withdrawals = statement_summary.get("withdrawals")

        ledger_income = round(
            sum(
                abs(float(tx.get("amount") or 0))
                for tx in kpi_transactions
                if tx.get("type") == "income"
            ),
            2,
        )

        ledger_expense = round(
            sum(
                abs(float(tx.get("amount") or 0))
                for tx in kpi_transactions
                if tx.get("type") == "expense"
            ),
            2,
        )

        if statement_deposits is not None:
            print("STATEMENT_INCOME_RECONCILIATION", {
                "statement": round(abs(float(statement_deposits)), 2),
                "ledger": ledger_income,
                "gap": round(abs(float(statement_deposits)) - ledger_income, 2),
            })

        if statement_withdrawals is not None:
            print("STATEMENT_EXPENSE_RECONCILIATION", {
                "statement": round(abs(float(statement_withdrawals)), 2),
                "ledger": ledger_expense,
                "gap": round(abs(float(statement_withdrawals)) - ledger_expense, 2),
            })

        income_gap = None
        expense_gap = None

        if statement_deposits is not None:
            income_gap = abs(round(abs(float(statement_deposits)) - ledger_income, 2))

        if statement_withdrawals is not None:
            expense_gap = abs(round(abs(float(statement_withdrawals)) - ledger_expense, 2))

        status = "PERFECT_RECONCILIATION"

        if (income_gap is not None and income_gap > 10) or (expense_gap is not None and expense_gap > 10):
            status = "NEEDS_REVIEW"
        elif (income_gap is not None and income_gap > 1) or (expense_gap is not None and expense_gap > 1):
            status = "ACCEPTABLE_RECONCILIATION"
        elif (income_gap is not None and income_gap > 0.01) or (expense_gap is not None and expense_gap > 0.01):
            status = "EXCELLENT_RECONCILIATION"

        print("RECONCILIATION_STATUS", status, {
            "income_gap": income_gap,
            "expense_gap": expense_gap,
        })

    reconciliation_income_total = round(
        sum(float(tx.get("amount") or 0) for tx in kpi_transactions if tx.get("type") == "income"),
        2,
    )
    reconciliation_expense_total = round(
        sum(abs(float(tx.get("amount") or 0)) for tx in kpi_transactions if tx.get("type") == "expense"),
        2,
    )

    reconciliation_warnings = []

    if transactions and not kpi_transactions:
        reconciliation_warnings.append("NO_KPI_TRANSACTIONS_AFTER_FILTER")

    if any(tx.get("signed_amount") is None for tx in kpi_transactions):
        reconciliation_warnings.append("MISSING_SIGNED_AMOUNT")

    if kpi_transactions and all(
        tx.get("balance") is None and tx.get("_balance") is None
        for tx in kpi_transactions
    ):
        reconciliation_warnings.append("NO_BALANCE_DATA")

    if quality.get("status") == "insufficient_data":
        reconciliation_warnings.append("INSUFFICIENT_DATA")

    print(
        "RECONCILIATION_CHECK",
        {
            "transactions": len(kpi_transactions),
            "income_count": sum(1 for tx in kpi_transactions if tx.get("type") == "income"),
            "expense_count": sum(1 for tx in kpi_transactions if tx.get("type") == "expense"),
            "income_total": reconciliation_income_total,
            "expense_total": reconciliation_expense_total,
            "excluded_transactions": len(transactions) - len(kpi_transactions),
            "warning": ";".join(reconciliation_warnings) if reconciliation_warnings else None,
        },
    )

    if quality["status"] == "insufficient_data":
        result = {
            "status": "insufficient_data",
            "analysis_status": "insufficient_data",
            "confidence": quality["confidence"],
            "analysis_quality": quality,
            "financial_score": None,
            "transactions": transactions,
            "message": {
                "en": "We detected this statement, but there is not enough reliable data to generate a full financial analysis. Please upload a clearer exported PDF or a higher-quality scan.",
                "fr": "Nous avons détecté ce relevé, mais les données fiables sont insuffisantes pour générer une analyse financière complète. Veuillez importer un PDF exporté plus clair ou un scan de meilleure qualité.",
                "ar": "تم اكتشاف كشف الحساب، لكن البيانات الموثوقة غير كافية لإنشاء تحليل مالي كامل. يرجى رفع ملف PDF أوضح أو نسخة ممسوحة بجودة أعلى.",
            }.get(output_language),
            "disclaimer": get_finance_disclaimer(output_language),
        }

        analysis = FinanceAnalysis(
            user_id=user_id,
            file_name=file_name,
            result=json.dumps(result, ensure_ascii=False),
            access_type=access_type,
            credits_used=credits_used,
        )

        db.add(analysis)
        db.commit()
        db.refresh(analysis)

        result["id"] = analysis.id
        return result

    update_job_progress(
        job,
        db,
        42,
        finance_progress_message("spending", output_language),
    )

    result_ai = analyze_bank_statement(text, output_language)
    fallback_income = result_ai.get("total_income_estimate")

    observed_transaction_income = observed_income_from_transactions(
        transactions
    )

    # General protection:
    # If income is already visible in extracted transactions, do not pass the
    # AI estimate as fallback income to forecast/budget/scoring engines.
    # Otherwise some statements can double-count income:
    # extracted income + AI estimated income.
    effective_fallback_income = (
        None
        if observed_transaction_income > 0
        else fallback_income
    )

    currency = resolve_finance_currency(
        result_ai=result_ai,
        transactions=transactions,
    )

    # Keep downstream UI/report fields consistent with the resolved value.
    result_ai["currency_detected"] = currency

    update_job_progress(
        job,
        db,
        52,
        finance_progress_message("subscriptions", output_language),
    )

    subscriptions = detect_recurring_subscriptions(transactions)

    # Global post-KPI metadata guard.
    # Removes statement/rate/disclosure rows that can look like dated transactions.

    savings_opportunities = detect_savings_opportunities(
        transactions=kpi_transactions,
        subscriptions=subscriptions,
    )

    update_job_progress(
        job,
        db,
        64,
        finance_progress_message("budget", output_language),
    )



    audit_tx_stage("TX_STAGE_4_BEFORE_EXPENSE_FULL_AUDIT", kpi_transactions)

    print(
        "EXPENSE_FULL_AUDIT",
        [
            {
                "date": tx.get("date"),
                "amount": tx.get("amount"),
                "type": tx.get("type"),
                "description": tx.get("description"),
            }
            for tx in kpi_transactions
            if tx.get("type") == "expense"
        ],
    )


    print(
        "KPI_SOURCE_AUDIT",
        [
            {
                "date": tx.get("date"),
                "amount": tx.get("amount"),
                "type": tx.get("type"),
            }
            for tx in transactions[:20]
        ],
    )

    budget = build_recommended_budget(
        transactions=kpi_transactions,
        fallback_income=effective_fallback_income,
        output_language=output_language,
    )

    scores = calculate_financial_scores(
        transactions=kpi_transactions,
        subscriptions=subscriptions,
        fallback_income=effective_fallback_income,
    )

    update_job_progress(
        job,
        db,
        76,
        finance_progress_message("forecast", output_language),
    )

    forecast = predict_cashflow(
        transactions=kpi_transactions,
        fallback_income=effective_fallback_income,
        output_language=output_language,
    )

    print("METADATA_GUARD_INPUT_DEBUG", [
        {
            "date": tx.get("date"),
            "amount": tx.get("amount"),
            "type": tx.get("type"),
            "desc": (tx.get("description") or tx.get("desc") or "")[:200],
        }
        for tx in kpi_transactions
        if any(x in str(tx.get("description") or tx.get("desc") or "").lower() for x in [
            "interest", "rate", "automatic", "limit", "excess", "tier", "p.a"
        ])
    ])

    metadata_excluded = []
    metadata_kept = []

    for tx in kpi_transactions:
        desc = str(tx.get("description") or tx.get("desc") or "").lower()
        is_metadata = any(p in desc for p in [
            "interest rate",
            "interest rates",
            "credit interest",
            "debit interest",
            "automatic limit",
            "excess @",
            "p.a.",
            "tier 1",
            "tier 2",
            "page 1 of",
            "page 2 of",
            "page 3 of",
        ])

        if is_metadata:
            tx["excluded_from_financial_kpis"] = True
            tx["excluded_reason"] = "global_statement_metadata_guard"
            metadata_excluded.append({
                "date": tx.get("date"),
                "amount": tx.get("amount"),
                "type": tx.get("type"),
                "desc": (tx.get("description") or tx.get("desc") or "")[:160],
            })
            continue

        metadata_kept.append(tx)

    if metadata_excluded:
        print("GLOBAL_STATEMENT_METADATA_GUARD", {
            "count": len(metadata_excluded),
            "samples": metadata_excluded[:20],
        })

    kpi_transactions = metadata_kept

    # Global balance-chain no-op guard:
    # Exclude rows that look like debit/fee transactions but do not change the running balance.
    # This avoids counting informational fee rows displayed inside card/FX settlement details.
    no_op_excluded = []
    no_op_kept = []
    prev_balance = None

    for tx in kpi_transactions:
        balance_raw = tx.get("balance") or tx.get("_balance")
        amount = abs(float(tx.get("amount") or 0))

        try:
            balance = float(balance_raw) if balance_raw is not None else None
        except Exception:
            balance = None

        is_no_op_balance_row = (
            tx.get("type") == "expense"
            and amount > 0
            and balance is not None
            and prev_balance is not None
            and round(abs(prev_balance - balance), 2) == 0
        )

        if is_no_op_balance_row:
            tx["excluded_from_financial_kpis"] = True
            tx["excluded_reason"] = "balance_chain_noop_row"
            no_op_excluded.append({
                "date": tx.get("date"),
                "amount": tx.get("amount"),
                "balance": balance,
                "prev_balance": prev_balance,
                "type": tx.get("type"),
                "desc": (tx.get("description") or tx.get("desc") or "")[:160],
            })
            prev_balance = balance
            continue

        no_op_kept.append(tx)
        if balance is not None:
            prev_balance = balance

    if no_op_excluded:
        print("BALANCE_CHAIN_NOOP_GUARD", {
            "count": len(no_op_excluded),
            "samples": no_op_excluded[:20],
        })

    kpi_transactions = no_op_kept

    print(
        "EXPENSE_TOTAL_RECALC",
        round(
            sum(
                abs(float(tx.get("amount", 0)))
                for tx in kpi_transactions
                if tx.get("type") == "expense"
            ),
            2,
        ),
    )

    print(
        "INCOME_TOTAL_RECALC",
        round(
            sum(
                float(tx.get("amount", 0))
                for tx in kpi_transactions
                if tx.get("type") == "income"
            ),
            2,
        ),
    )

    income_total = round(
        sum(
            float(tx.get("amount", 0))
            for tx in kpi_transactions
            if tx.get("type") == "income"
        ),
        2,
    )

    expense_total = round(
        sum(
            abs(float(tx.get("amount", 0)))
            for tx in kpi_transactions
            if tx.get("type") == "expense"
        ),
        2,
    )

    # Global EN/FR/AR validated official-summary fallback.
    # Uses 4-number accounting summary only:
    # beginning_balance, withdrawals/debits, deposits/credits, ending_balance.
    summary_reconciliation_used = False
    try:
        import re

        raw_text_for_summary = str(
            result_ai.get("raw_text")
            or result_ai.get("text")
            or result_ai.get("extracted_text")
            or locals().get("text")
            or locals().get("raw_text")
            or ""
        )

        money_re = r"\d{1,3}(?:,\d{3})*(?:\.\d{2})|\d+\.\d{2}"

        summary_block_match = re.search(
            r"(?:ACCOUNT SUMMARY|R[ÉE]SUM[ÉE] DU COMPTE|RESUME DU COMPTE|ملخص الحساب)"
            r".{0,600}?"
            r"(?:BALANCE|SOLDE|الرصيد).{0,120}?"
            r"(?:CHECKS/WITHDRAWALS|WITHDRAWALS|DEBITS|RETRAITS|D[ÉE]BITS|السحوبات|مدين).{0,120}?"
            r"(?:DEPOSITS/ADDITIONS|DEPOSITS|ADDITIONS|CREDITS|D[ÉE]P[ÔO]TS|DEPOTS|CR[ÉE]DITS|VERSEMENTS|الإيداعات|دائن).{0,120}?"
            r"(?:BALANCE|SOLDE|الرصيد)"
            r"(?P<body>.{0,300})",
            raw_text_for_summary,
            re.I | re.S,
        )

        if summary_block_match:
            nums = re.findall(money_re, summary_block_match.group("body"))
            nums = [round(float(x.replace(",", "")), 2) for x in nums]

            if len(nums) >= 4:
                beginning_balance, official_expense, official_income, ending_balance = nums[:4]
                accounting_ok = abs((beginning_balance - official_expense + official_income) - ending_balance) <= 1.00

                parsed_income = income_total
                parsed_expense = expense_total
                income_count = sum(1 for tx in kpi_transactions if tx.get("type") == "income")
                expense_count = sum(1 for tx in kpi_transactions if tx.get("type") == "expense")

                should_use_summary_fallback = (
                    accounting_ok
                    and len(kpi_transactions) > 0
                    and expense_count > 0
                    and income_count == 0
                    and official_income > 0
                    and official_expense > 0
                )

                print("SUMMARY_RECONCILIATION_4NUM_AUDIT", {
                    "beginning_balance": beginning_balance,
                    "official_expense": official_expense,
                    "official_income": official_income,
                    "ending_balance": ending_balance,
                    "parsed_income": parsed_income,
                    "parsed_expense": parsed_expense,
                    "accounting_ok": accounting_ok,
                    "will_apply": should_use_summary_fallback,
                })

                if should_use_summary_fallback:
                    income_total = official_income
                    expense_total = official_expense
                    summary_reconciliation_used = True
                    result_ai["summary_reconciliation_used"] = True
                    result_ai["analysis_confidence"] = "limited"
                    print("SUMMARY_RECONCILIATION_FALLBACK", {
                        "official_income": official_income,
                        "official_expense": official_expense,
                        "parsed_income": parsed_income,
                        "parsed_expense": parsed_expense,
                        "income_gap": round(official_income - parsed_income, 2),
                        "expense_gap": round(official_expense - parsed_expense, 2),
                        "action": "aggregate_kpi_only_no_transaction_mutation",
                    })

    except Exception as e:
        print("SUMMARY_RECONCILIATION_FALLBACK_ERROR", str(e)[:200])

    # Global EN/FR/AR official summary reconciliation.
    # KPI override only: never mutates extracted transactions.
    try:
        import re

        raw_text_for_summary = str(
            result_ai.get("raw_text")
            or result_ai.get("text")
            or result_ai.get("extracted_text")
            or locals().get("text")
            or locals().get("raw_text")
            or ""
        )
        low_summary = raw_text_for_summary.lower()

        def _money_to_float(v):
            return round(float(str(v).replace(",", "").replace("£", "").replace("$", "").replace("€", "").strip()), 2)

        official_income = None
        official_expense = None
        official_start = None
        official_end = None

        # EN/UK/Commonwealth: Money in / Money out
        m_in = re.search(r"(?:money\s+in|total\s+credits?|credits?)\s*[£$€]?\s*([\d,]+\.\d{2})", raw_text_for_summary, re.I)
        m_out = re.search(r"(?:money\s+out|total\s+debits?|debits?)\s*[£$€]?\s*([\d,]+\.\d{2})", raw_text_for_summary, re.I)
        m_start = re.search(r"(?:start|beginning)\s+balance\s*[£$€]?\s*([\d,]+\.\d{2})", raw_text_for_summary, re.I)
        m_end = re.search(r"(?:end|ending)\s+balance\s*[£$€]?\s*([\d,]+\.\d{2})", raw_text_for_summary, re.I)

        if m_in and m_out:
            official_income = _money_to_float(m_in.group(1))
            official_expense = _money_to_float(m_out.group(1))
            official_start = _money_to_float(m_start.group(1)) if m_start else None
            official_end = _money_to_float(m_end.group(1)) if m_end else None

        # Credit-card/account-summary/checking style EN
        if official_income is None or official_expense is None:
            m_income = re.search(
                r"(?:payments\s+and\s+other\s+credits|deposits?\s+and\s+additions|"
                r"deposits?/additions?|deposits?|additions?|total\s+credits?)"
                r"\s*-?[£$€]?\s*([\d,]+\.\d{2})",
                raw_text_for_summary,
                re.I,
            )
            m_expense = re.search(
                r"(?:purchases\s+and\s+adjustments|atm\s*&\s*debit\s+card\s+withdrawals|"
                r"atm\s+and\s+debit\s+card\s+withdrawals|checks/withdrawals|"
                r"withdrawals|total\s+debits?)"
                r"\s*-?[£$€]?\s*([\d,]+\.\d{2})",
                raw_text_for_summary,
                re.I,
            )
            if m_income and m_expense:
                official_income = _money_to_float(m_income.group(1))
                official_expense = _money_to_float(m_expense.group(1))

        # FR
        if official_income is None or official_expense is None:
            m_income = re.search(r"(?:entr[ée]e|cr[ée]dits?|d[ée]p[ôo]ts?|versements?)\s*[£$€]?\s*([\d,]+\.\d{2})", raw_text_for_summary, re.I)
            m_expense = re.search(r"(?:sortie|d[ée]bits?|retraits?|paiements?|frais)\s*[£$€]?\s*([\d,]+\.\d{2})", raw_text_for_summary, re.I)
            if m_income and m_expense:
                official_income = _money_to_float(m_income.group(1))
                official_expense = _money_to_float(m_expense.group(1))

        # AR
        if official_income is None or official_expense is None:
            m_income = re.search(r"(?:دائن|الإيداعات|الايداعات|إيداع|ايداع)\s*[£$€]?\s*([\d,]+\.\d{2})", raw_text_for_summary)
            m_expense = re.search(r"(?:مدين|السحوبات|سحب|المدفوعات|رسوم)\s*[£$€]?\s*([\d,]+\.\d{2})", raw_text_for_summary)
            if m_income and m_expense:
                official_income = _money_to_float(m_income.group(1))
                official_expense = _money_to_float(m_expense.group(1))

        if official_income is not None and official_expense is not None:
            parsed_income = income_total
            parsed_expense = expense_total

            income_gap_ratio = (
                abs(parsed_income - official_income) / official_income
                if official_income > 0 else 0
            )
            expense_gap_ratio = (
                abs(parsed_expense - official_expense) / official_expense
                if official_expense > 0 else 0
            )

            accounting_ok = True
            if official_start is not None and official_end is not None:
                accounting_ok = abs((official_start + official_income - official_expense) - official_end) <= 2.00

            has_strong_official_totals = (
                official_income is not None
                and official_expense is not None
                and (official_income > 0 or official_expense > 0)
            )

            should_apply_summary_reconciliation = (
                len(kpi_transactions) > 0
                and has_strong_official_totals
                and income_gap_ratio <= 0.25
                and expense_gap_ratio <= 0.35
                and (
                    accounting_ok
                    or ("money in" in low_summary and "money out" in low_summary)
                    or ("payments and other credits" in low_summary and "purchases and adjustments" in low_summary)
                    or ("deposits and additions" in low_summary and "withdrawals" in low_summary)
                )
                and (
                    income_gap_ratio > 0.005
                    or expense_gap_ratio > 0.005
                )
            )

            print("SUMMARY_RECONCILIATION_AUDIT", {
                "official_income": official_income,
                "official_expense": official_expense,
                "parsed_income": parsed_income,
                "parsed_expense": parsed_expense,
                "income_gap_ratio": round(income_gap_ratio, 4),
                "expense_gap_ratio": round(expense_gap_ratio, 4),
                "accounting_ok": accounting_ok,
                "will_apply": should_apply_summary_reconciliation,
            })

            if should_apply_summary_reconciliation:
                income_total = official_income
                expense_total = official_expense
                result_ai["summary_reconciliation_used"] = True
                result_ai["summary_reconciliation_mode"] = "kpi_override_only_no_transaction_mutation"

                print("SUMMARY_RECONCILIATION_APPLIED", {
                    "official_income": official_income,
                    "official_expense": official_expense,
                    "parsed_income": parsed_income,
                    "parsed_expense": parsed_expense,
                    "action": "kpi_override_only_no_transaction_mutation",
                })

    except Exception as e:
        print("SUMMARY_RECONCILIATION_ERROR", str(e)[:200])

    uncategorized_count = sum(
        1
        for tx in kpi_transactions
        if tx.get("type") not in ["income", "expense"]
    )

    print(
        "KPI_TOTALS",
        {
            "income": income_total,
            "expense": expense_total,
            "uncategorized": uncategorized_count
        }
    )

    suspicious_balance_like = []
    for tx in kpi_transactions:
        try:
            amount_abs = abs(float(tx.get("amount") or 0))
            balance_abs = abs(float(tx.get("balance") or tx.get("_balance") or 0))
        except Exception:
            continue

        if balance_abs > 0 and amount_abs > 0:
            ratio = amount_abs / balance_abs
            if ratio > 0.80:
                suspicious_balance_like.append({
                    "date": tx.get("date"),
                    "amount": tx.get("amount"),
                    "balance": tx.get("balance") or tx.get("_balance"),
                    "type": tx.get("type"),
                    "desc": (tx.get("description") or tx.get("desc") or "")[:120],
                    "ratio": round(ratio, 4),
                })

    if suspicious_balance_like:
        print(
            "BALANCE_LIKE_AMOUNT_WARNING",
            {
                "count": len(suspicious_balance_like),
                "samples": suspicious_balance_like[:10],
            },
        )

    # International banking audit:
    # For chronological statement rows, current_balance should equal
    # previous_balance + signed_amount within a small tolerance.
    balance_chain_mismatches = []
    tx_with_balance = [
        tx for tx in kpi_transactions
        if tx.get("balance") is not None or tx.get("_balance") is not None
    ]

    for prev_tx, curr_tx in zip(tx_with_balance, tx_with_balance[1:]):
        try:
            prev_balance = float(prev_tx.get("balance") or prev_tx.get("_balance"))
            curr_balance = float(curr_tx.get("balance") or curr_tx.get("_balance"))
            signed_amount = float(curr_tx.get("signed_amount") or curr_tx.get("amount") or 0)
        except Exception:
            continue

        expected = round(prev_balance + signed_amount, 2)
        delta = round(curr_balance - expected, 2)

        if abs(delta) > 0.05:
            balance_chain_mismatches.append({
                "prev_date": prev_tx.get("date"),
                "date": curr_tx.get("date"),
                "prev_balance": prev_balance,
                "signed_amount": signed_amount,
                "expected_balance": expected,
                "actual_balance": curr_balance,
                "delta": delta,
                "type": curr_tx.get("type"),
                "desc": (curr_tx.get("description") or curr_tx.get("desc") or "")[:120],
            })

    if balance_chain_mismatches:
        mismatch_ratio = (
            len(balance_chain_mismatches) / max(len(tx_with_balance) - 1, 1)
        )

        if mismatch_ratio > 0.30:
            print(
                "BALANCE_CHAIN_UNRELIABLE",
                {
                    "count": len(balance_chain_mismatches),
                    "checked_pairs": max(len(tx_with_balance) - 1, 1),
                    "mismatch_ratio": round(mismatch_ratio, 4),
                    "samples": balance_chain_mismatches[:5],
                },
            )
        else:
            print(
                "BALANCE_CHAIN_MISMATCH",
                {
                    "count": len(balance_chain_mismatches),
                    "samples": balance_chain_mismatches[:10],
                },
            )

    for idx, tx in enumerate(kpi_transactions):
        if idx < 50 or DEBUG_FINANCE_EXTRACTOR:
            print(
                "KPI_INPUT",
                {
                    "amount": tx.get("amount"),
                    "signed_amount": tx.get("signed_amount"),
                    "type": tx.get("type")
                }
            )
    if len(kpi_transactions) > 50 and not DEBUG_FINANCE_EXTRACTOR:
        print("KPI_INPUT_TRUNCATED", {"printed": 50, "total": len(kpi_transactions)})

    # Hotfix: KPI_AUDIT must reflect parsed kpi_transactions,
    # not stale forecast values.
    forecast["observed_income"] = income_total
    forecast["observed_expenses"] = expense_total
    forecast["observed_net_cashflow"] = round(income_total - expense_total, 2)

    excluded_transactions = max(len(transactions) - len(kpi_transactions), 0)
    exclusion_ratio = (
        excluded_transactions / len(transactions)
        if len(transactions) > 0
        else 0
    )

    if excluded_transactions > max(3, int(len(transactions) * 0.10)):
        excluded_samples = [
            {
                "date": tx.get("date"),
                "amount": tx.get("amount"),
                "signed_amount": tx.get("signed_amount"),
                "type": tx.get("type"),
                "excluded_flag": tx.get("excluded_from_financial_kpis"),
                "excluded_reason": tx.get("excluded_reason") or tx.get("category_hint"),
                "is_internal_transfer": tx.get("is_internal_transfer"),
                "desc": (tx.get("description") or tx.get("desc") or "")[:120],
            }
            for tx in transactions
            if tx not in kpi_transactions
        ][:10]

        print(
            "KPI_EXCLUSION_WARNING",
            {
                "raw_transactions": len(transactions),
                "kpi_transactions": len(kpi_transactions),
                "excluded_transactions": excluded_transactions,
                "exclusion_ratio": round(exclusion_ratio, 4),
                "warning": (
                    "EXPECTED_INTERNAL_TRANSFER_EXCLUSIONS"
                    if all(
                        (tx.get("is_internal_transfer") or tx.get("excluded_reason") == "internal_transfer")
                        for tx in excluded_samples
                    )
                    else "TOO_MANY_EXCLUDED_TRANSACTIONS"
                ),
                "samples": excluded_samples,
            },
        )

    print(
        "KPI_AUDIT",
        {
            "raw_transactions": len(transactions),
            "kpi_transactions": len(kpi_transactions),
            "income": income_total,
            "expenses": expense_total,
            "net": round(income_total - expense_total, 2),
            "excluded_transactions": excluded_transactions,
        },
    )


    savings_rate = (
        forecast.get("observed_net_cashflow", 0)
        / forecast.get("observed_income", 1)
        if forecast.get("observed_income", 0) > 0
        else 0
    )

    observed_income = forecast.get(
        "observed_income",
        0,
    )

    observed_expenses = forecast.get(
        "observed_expenses",
        0,
    )

    subscription_total = sum(
        safe_float(subscription.get("monthly_cost", 0))
        for subscription in subscriptions
    )

    subscription_ratio = (
        subscription_total / observed_income
        if observed_income > 0
        else 0
    )

    expense_ratio = (
        observed_expenses / observed_income
        if observed_income > 0
        else 1
    )

    result_ai["waste_detected"] = filter_metric_inconsistent_items(
        result_ai.get("waste_detected", []),
        subscription_ratio=subscription_ratio,
        expense_ratio=expense_ratio,
        savings_rate=savings_rate,
    )

    result_ai["saving_strategies"] = filter_metric_inconsistent_items(
        result_ai.get("saving_strategies", []),
        subscription_ratio=subscription_ratio,
        expense_ratio=expense_ratio,
        savings_rate=savings_rate,
    )

    if observed_expenses > 0:
        result_ai["total_spending_estimate"] = round(
            observed_expenses,
            2,
        )

    if observed_income > 0:
        result_ai["total_income_estimate"] = round(
            observed_income,
            2,
        )

    result_ai["financial_score"] = scores.get(
        "overall_financial_habits_score",
        0,
    )

    alerts = generate_financial_alerts(
        transactions=kpi_transactions,
        subscriptions=subscriptions,
        forecast=forecast,
        scores=scores,
    )

    RISK_TRANSLATIONS = {
        "NEGATIVE_CASHFLOW": {
            "en": "Negative cashflow detected.",
            "fr": "Trésorerie négative détectée.",
            "ar": "تم اكتشاف خطر على التدفق النقدي.",
        },
        "LOW_FINANCIAL_SCORE": {
            "en": "Financial habits need improvement.",
            "fr": "Les habitudes financières doivent être améliorées.",
            "ar": "العادات المالية تحتاج إلى تحسين.",
        },
        "HIGH_EXPENSES": {
            "en": "Monthly expenses are relatively high.",
            "fr": "Les dépenses mensuelles sont relativement élevées.",
            "ar": "المصاريف الشهرية مرتفعة نسبياً.",
        },
        "TOO_MANY_SUBSCRIPTIONS": {
            "en": "Multiple recurring subscriptions detected.",
            "fr": "Plusieurs abonnements récurrents détectés.",
            "ar": "تم اكتشاف عدة اشتراكات متكررة.",
        },
    }

    risk_notes = []

    for alert in alerts:
        code = alert.get("code")

        text = (
            RISK_TRANSLATIONS
            .get(code, {})
            .get(output_language)
        )

        if text:
            risk_notes.append(text)

    result_ai["risk_notes"] = risk_notes

    update_job_progress(
        job,
        db,
        86,
        finance_progress_message("insights", output_language),
    )

    insights = generate_financial_insights(
        transactions=kpi_transactions,
        subscriptions=subscriptions,
        scores=scores,
        forecast=forecast,
        opportunities=savings_opportunities,
        currency=currency,
        output_language=output_language,
    )

    update_job_progress(
        job,
        db,
        92,
        finance_progress_message("charts", output_language),
    )

    charts = build_financial_charts(kpi_transactions)

    result_ai["summary"] = build_observed_finance_summary(
        forecast=forecast,
        currency=currency,
        output_language=output_language,
    )

    for field in [
        "saving_strategies",
        "waste_detected",
        "risk_notes",
    ]:
        result_ai[field] = [
            item
            for item in result_ai.get(field, [])
            if str(item).strip()
        ]

    result_ai["disclaimer"] = get_finance_disclaimer(
        output_language
    )

    result_ai["analysis_status"] = quality["status"]
    result_ai["confidence"] = quality["confidence"]
    result_ai["analysis_quality"] = quality

    result = {
        **result_ai,
        "transactions": transactions,
        "charts": charts,
        "subscriptions_detected": subscriptions,
        "savings_opportunities": savings_opportunities,
        "recommended_budget": budget,
        "cashflow_forecast": forecast,
        "financial_habit_scores": scores,
        "financial_alerts": alerts,
        "financial_insights": insights,
    }

    update_job_progress(
        job,
        db,
        96,
        finance_progress_message("saving", output_language),
    )

    analysis = FinanceAnalysis(
        user_id=user_id,
        file_name=file_name,
        result=json.dumps(result, ensure_ascii=False),
        access_type=access_type,
        credits_used=credits_used,
    )

    db.add(analysis)
    db.commit()
    db.refresh(analysis)

    result["id"] = analysis.id

    update_job_progress(
        job,
        db,
        98,
        finance_progress_message("finalizing", output_language),
    )

    return result
