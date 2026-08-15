import json
from collections import Counter
import re
from datetime import datetime

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
    get_finance_extraction_status,
    get_finance_audit_candidate,
    get_finance_observed_analysis_candidate,
    get_finance_scope_rejection_evidence,
    detect_currency,
)
from app.services.finance_agent.transaction_extractor import extract_transactions_from_pdf_path
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
            # Option B / standard reconciliation rule:
            # If the row is locked by a trusted statement parser, keep it in KPI.
            # This preserves official statement deposits/withdrawals such as
            # Mercury Transfer In/Out while still excluding weak internal transfers.
            if (
                tx.get("_balance_locked")
                or tx.get("locked_amount") is not None
                or tx.get("_locked_amount") is not None
            ):
                continue

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


def build_analysis_ledger(accounting_transactions: list[dict]) -> tuple[list[dict], list[dict]]:
    """Build a behavioral ledger without mutating the reconciled accounting ledger.

    Historical explicit exclusions remain authoritative.  Additive v24 keeps
    behavioral neutrality strictly structural: a category label is diagnostic
    only and can never, by itself, remove a transaction from observed income or
    spending.  A row is excluded only when an existing explicit exclusion or a
    structural accounting-neutrality proof is present.

    No bank, country, currency, language, merchant, network, counterparty, or
    commercial-label rule exists here.  Equal amount/date coincidence and a
    categorization result alone remain insufficient.
    """
    analysis_rows = []
    excluded_rows = []
    neutral_roles = {
        "transfer",
        "internal_transfer",
        "neutral_transfer",
        "account_transfer",
    }

    for tx in accounting_transactions or []:
        if not isinstance(tx, dict):
            continue

        pair_id = (
            tx.get("analysis_neutral_pair_id")
            or tx.get("_analysis_neutral_pair_id")
            or tx.get("accounting_pair_id")
            or tx.get("_accounting_pair_id")
        )
        accounting_role = str(
            tx.get("accounting_role")
            or tx.get("row_role")
            or ""
        ).strip().lower()

        already_excluded = bool(
            tx.get("excluded_from_financial_kpis")
            or tx.get("is_internal_transfer")
            or str(tx.get("type") or "").strip().lower() == "transfer"
        )

        structurally_neutral = bool(
            pair_id is not None
            and accounting_role in neutral_roles
        )

        description = str(tx.get("description") or "")
        category = str(
            tx.get("category")
            or detect_category(description)
            or "other"
        ).strip().lower()

        # v24 — category labels are not accounting evidence.
        # A transfer/savings categorization may describe the economic purpose of
        # a row, but it does not prove that the cashflow is internal or neutral.
        # Neutrality must already be explicit or structurally demonstrated by a
        # paired accounting role.
        if already_excluded or structurally_neutral:
            excluded_rows.append({
                **tx,
                "_analysis_exclusion_reason": "existing_structural_neutrality",
                "_analysis_category": category,
            })
        else:
            analysis_rows.append(tx)

    return analysis_rows, excluded_rows


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

        if net == 0:
            return (
                f"Les revenus observés s’élèvent à {income} {currency}, "
                f"tandis que les dépenses observées atteignent {expenses} {currency}. "
                f"La trésorerie nette observée est de {net} {currency}."
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

        if net == 0:
            return (
                f"بلغ الدخل المرصود {income} {currency}، "
                f"بينما بلغت المصاريف المرصودة {expenses} {currency}. "
                f"صافي التدفق النقدي المرصود هو {net} {currency}."
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

    if net == 0:
        return (
            f"Observed income is {income} {currency}, "
            f"while observed expenses are {expenses} {currency}. "
            f"Observed net cashflow is {net} {currency}."
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


def _currency_from_primary_transaction_header(
    statement_text: str | None,
) -> str | None:
    """Return a concrete currency explicitly printed in a transaction header.

    Additive source-scoped authority only.  Legal/disclosure currency lists are
    ignored because the marker must occur on the same physical line as a
    transaction-table header containing movement roles and a balance role.
    """
    raw = str(statement_text or "")

    explicit_marker_map = {
        "S$": "SGD",
        "SGD": "SGD",
        "US$": "USD",
        "USD": "USD",
        "A$": "AUD",
        "AUD": "AUD",
        "C$": "CAD",
        "CAD": "CAD",
        "NZ$": "NZD",
        "NZD": "NZD",
        "HK$": "HKD",
        "HKD": "HKD",
        "EUR": "EUR",
        "GBP": "GBP",
        "CHF": "CHF",
        "JPY": "JPY",
        "CNY": "CNY",
        "CNH": "CNH",
    }

    for raw_line in raw.splitlines():
        line = " ".join(str(raw_line or "").split())
        lowered = line.lower()

        has_date_role = bool(re.search(r"\bdate\b", lowered))
        has_balance_role = bool(
            re.search(
                r"\b(?:balance|solde|الرصيد)\b",
                lowered,
                flags=re.IGNORECASE,
            )
        )
        has_flow_roles = bool(
            re.search(
                r"\b(?:withdrawals?|debits?|débits?|"
                r"deposits?|credits?|crédits?|"
                r"money\s+out|money\s+in)\b",
                lowered,
                flags=re.IGNORECASE,
            )
        )

        if not (has_date_role and has_balance_role and has_flow_roles):
            continue

        # Prefer a marker explicitly attached to the balance/header role.
        parenthetical = re.findall(r"\(([^()]{1,24})\)", line)
        candidates = parenthetical + [line]

        for candidate in candidates:
            compact = str(candidate or "").upper().strip()

            for marker, code in explicit_marker_map.items():
                if marker in {"S$", "US$", "A$", "C$", "NZ$", "HK$"}:
                    if marker in compact:
                        return code
                elif re.search(
                    rf"(?<![A-Z]){re.escape(marker)}(?![A-Z])",
                    compact,
                ):
                    return code

    return None


def resolve_finance_currency(
    result_ai: dict,
    transactions: list[dict],
    statement_text: str | None = None,
) -> str:
    """Resolve currency from observed statement evidence before AI fallback.

    Priority:
    1) Concrete transaction-level currency consensus.
    2) Concrete currency printed in the primary transaction-table header.
    3) AI-detected concrete currency.
    4) MULTI only when no stronger scoped evidence exists.
    5) unknown.

    `MULTI` is intentionally not treated as a concrete transaction consensus:
    it can be produced when legal/footer currency-code lists coexist with a
    single-currency account table.
    """
    detected = [
        str(tx.get("currency")).upper().strip()
        for tx in transactions
        if tx.get("currency")
        and str(tx.get("currency")).strip().lower()
        not in {"", "unknown", "none", "multi"}
    ]

    if detected:
        counts = Counter(detected)
        most_common_currency, most_common_count = counts.most_common(1)[0]

        if (
            len(counts) == 1
            or most_common_count > (len(detected) / 2)
        ):
            return most_common_currency

    scoped_header_currency = _currency_from_primary_transaction_header(
        statement_text
    )
    if scoped_header_currency:
        return scoped_header_currency

    currency = result_ai.get("currency_detected")
    if (
        currency not in [None, "", "unknown", "UNKNOWN"]
        and str(currency).strip().lower() not in {"none", "multi"}
    ):
        return str(currency).upper().strip()

    # Preserve historical MULTI only as a final non-concrete fallback.
    if str(result_ai.get("currency_detected") or "").upper().strip() == "MULTI":
        return "MULTI"

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


def _verification_money_to_float(value: object) -> float | None:
    """Parse a statement-level monetary observation without mutating extraction data."""
    if value is None:
        return None

    import re

    s = str(value).strip()
    if not s:
        return None

    negative_parentheses = s.startswith("(") and s.endswith(")")
    s = (
        s.replace("$", "")
         .replace("€", "")
         .replace("£", "")
         .replace("SAR", "")
         .replace("AED", "")
         .replace("MAD", "")
         .replace("USD", "")
         .replace("EUR", "")
         .replace("GBP", "")
         .replace("\u00a0", "")
         .replace(" ", "")
         .strip()
    )
    s = re.sub(r"[^0-9,.\-+]", "", s)

    if not s or s in {"+", "-", ".", ","}:
        return None

    if "." in s:
        s = s.replace(",", "")
    elif s.count(",") == 1:
        left, right = s.split(",", 1)
        if len(right) in {1, 2}:
            s = left + "." + right
        else:
            s = left + right
    else:
        s = s.replace(",", "")

    try:
        value_float = float(s)
    except (TypeError, ValueError):
        return None

    if negative_parentheses:
        value_float = -abs(value_float)

    return value_float


def enrich_source_summary_from_transaction_table_totals(
    statement_text: str | None,
    statement_summary: dict | None,
) -> dict:
    """Fill missing debit/credit totals from a strict transaction TOTAL row.

    This is source-document auditing only.  It does not mutate transactions,
    parser routing, candidate selection, signs, or financial authority.

    Structural requirements:
    - a physical header line contains Date + debit/withdrawal + credit/deposit
      + balance roles;
    - a later physical line in that same table begins with TOTAL;
    - that TOTAL line contains exactly two money values;
    - column order is inherited only from the detected header.
    """
    summary = dict(statement_summary or {})
    if (
        summary.get("deposits") is not None
        and summary.get("withdrawals") is not None
    ):
        return summary

    lines = [
        " ".join(str(line or "").split())
        for line in str(statement_text or "").splitlines()
    ]

    money_token_re = re.compile(
        r"(?<!\d)"
        r"(?:\d{1,3}(?:[ ,.']\d{3})+|\d+)"
        r"(?:[.,]\d{2})"
        r"(?!\d)"
    )

    for header_index, line in enumerate(lines):
        lowered = line.lower()

        if not re.search(r"\bdate\b", lowered):
            continue
        if not re.search(r"\b(?:balance|solde|الرصيد)\b", lowered, re.I):
            continue

        debit_match = re.search(
            r"\b(?:withdrawals?|debits?|débits?|money\s+out)\b",
            lowered,
            re.I,
        )
        credit_match = re.search(
            r"\b(?:deposits?|credits?|crédits?|money\s+in)\b",
            lowered,
            re.I,
        )
        if debit_match is None or credit_match is None:
            continue

        first_role = (
            "withdrawals"
            if debit_match.start() < credit_match.start()
            else "deposits"
        )
        second_role = (
            "deposits"
            if first_role == "withdrawals"
            else "withdrawals"
        )

        for candidate in lines[header_index + 1: header_index + 120]:
            candidate_lower = candidate.lower()

            if re.search(
                r"\b(?:page\s+\d+\s+of\s+\d+|"
                r"message\s+for\s+you|terms\s+and\s+codes)\b",
                candidate_lower,
                re.I,
            ):
                break

            if not re.match(r"^total\b", candidate_lower, re.I):
                continue

            money_tokens = money_token_re.findall(candidate)
            if len(money_tokens) != 2:
                continue

            parsed_values = [
                _verification_money_to_float(token)
                for token in money_tokens
            ]
            if any(value is None for value in parsed_values):
                continue

            role_values = {
                first_role: round(abs(float(parsed_values[0])), 2),
                second_role: round(abs(float(parsed_values[1])), 2),
            }

            if summary.get("withdrawals") is None:
                summary["withdrawals"] = role_values["withdrawals"]
            if summary.get("deposits") is None:
                summary["deposits"] = role_values["deposits"]

            summary["source"] = (
                "source_transaction_table_four_role_summary"
            )
            summary.setdefault("evidence", {})
            if isinstance(summary["evidence"], dict):
                summary["evidence"]["movement_totals"] = {
                    "source": "strict_transaction_total_row",
                    "header": line[:240],
                    "total_line": candidate[:240],
                    "column_order": [first_role, second_role],
                }

            return summary

    return summary


def assess_source_statement_consistency(statement_summary: dict | None) -> dict:
    """Audit the source statement's own four-role accounting identity only."""
    summary = dict(statement_summary or {})

    opening = _verification_money_to_float(summary.get("opening_balance"))
    deposits = _verification_money_to_float(summary.get("deposits"))
    withdrawals = _verification_money_to_float(summary.get("withdrawals"))
    ending = _verification_money_to_float(
        summary.get("ending_balance")
        if summary.get("ending_balance") is not None
        else summary.get("closing_balance")
    )

    # ADDITIVE v13 — preserve explicit DR/CR balance signs from source evidence.
    # This belongs to the common accounting consistency layer, not parser
    # selection.  DR means a negative account balance and CR a positive one.
    # The rule is structural and independent of bank, country, currency, or
    # transaction wording.  Historical summaries without these explicit markers
    # keep their existing behavior unchanged.
    evidence = summary.get("evidence") if isinstance(summary.get("evidence"), dict) else {}

    def _signed_balance_from_evidence(value, role):
        if value is None:
            return None
        item = evidence.get(role) if isinstance(evidence, dict) else None
        label = str(item.get("label") or "") if isinstance(item, dict) else ""
        marker_match = re.search(r"\b(DR|CR)\b", label, flags=re.I)
        if marker_match is None:
            return value
        marker = marker_match.group(1).upper()
        return -abs(float(value)) if marker == "DR" else abs(float(value))

    opening = _signed_balance_from_evidence(opening, "opening_balance")
    ending_role = (
        "ending_balance"
        if isinstance(evidence, dict) and "ending_balance" in evidence
        else "closing_balance"
    )
    ending = _signed_balance_from_evidence(ending, ending_role)

    components_complete = all(
        value is not None
        for value in (opening, deposits, withdrawals, ending)
    )

    if not components_complete:
        return {
            "available": False,
            "source_consistent": None,
            "source_inconsistency_detected": False,
            "accounting_gap": None,
            "opening_balance": opening,
            "deposits": deposits,
            "withdrawals": withdrawals,
            "ending_balance": ending,
            "source": summary.get("source"),
        }

    calculated_ending = round(
        float(opening) + abs(float(deposits)) - abs(float(withdrawals)),
        2,
    )
    accounting_gap = round(float(ending) - calculated_ending, 2)
    source_consistent = abs(accounting_gap) <= 0.02

    return {
        "available": True,
        "source_consistent": source_consistent,
        "source_inconsistency_detected": not source_consistent,
        "accounting_gap": accounting_gap,
        "calculated_ending_balance": calculated_ending,
        "opening_balance": round(float(opening), 2),
        "deposits": round(abs(float(deposits)), 2),
        "withdrawals": round(abs(float(withdrawals)), 2),
        "ending_balance": round(float(ending), 2),
        "source": summary.get("source"),
    }



def collect_explicit_statement_period_diagnostic(
    text: str | None,
    transactions: list[dict] | None,
) -> dict:
    """
    Audit-only document consistency check.

    Detect an explicitly printed financial statement-period range and compare it
    with dated ledger observations.

    Additive structural rule:
    a date range printed inside an auxiliary rewards/points/miles block is not a
    financial statement period. Candidate ranges are therefore classified by
    section role before one is allowed to become period authority.

    No bank, country, currency, merchant, card network, or product identity is
    used. No parser output, routing, candidate selection, transaction amount, or
    financial authority is mutated here.
    """
    raw = str(text or "")
    txs = [
        tx
        for tx in (transactions or [])
        if isinstance(tx, dict) and tx.get("date")
    ]

    def _parse_date_token(token: str, default_year: int | None = None):
        value = " ".join(str(token or "").strip().split())
        value = value.replace("\\", "/")

        for fmt in (
            "%d/%m/%Y",
            "%d/%m/%y",
            "%d-%m-%Y",
            "%d-%m-%y",
            "%d.%m.%Y",
            "%d.%m.%y",
            "%Y/%m/%d",
            "%Y-%m-%d",
            "%Y.%m.%d",
        ):
            try:
                return datetime.strptime(value, fmt).date()
            except ValueError:
                pass

        month_map = {
            "janvier": 1, "janv": 1,
            "février": 2, "fevrier": 2, "févr": 2, "fevr": 2,
            "mars": 3,
            "avril": 4, "avr": 4,
            "mai": 5,
            "juin": 6,
            "juillet": 7, "juil": 7,
            "août": 8, "aout": 8,
            "septembre": 9, "sept": 9,
            "octobre": 10, "oct": 10,
            "novembre": 11, "nov": 11,
            "décembre": 12, "decembre": 12, "déc": 12, "dec": 12,
            "january": 1, "jan": 1,
            "february": 2, "feb": 2,
            "march": 3, "mar": 3,
            "april": 4, "apr": 4,
            "may": 5,
            "june": 6, "jun": 6,
            "july": 7, "jul": 7,
            "august": 8, "aug": 8,
            "september": 9, "sep": 9,
            "october": 10,
            "november": 11,
            "december": 12,
        }

        textual = re.fullmatch(
            r"(?i)\s*(\d{1,2})\s+"
            r"([A-Za-zÀ-ÿ]+)"
            r"(?:\s+(\d{2,4}))?\s*",
            value,
        )
        if textual:
            day = int(textual.group(1))
            month_key = textual.group(2).casefold()
            year_raw = textual.group(3)
            month = month_map.get(month_key)

            if month is None:
                return None

            if year_raw:
                year = int(year_raw)
                if year < 100:
                    year += 2000
            elif default_year is not None:
                year = int(default_year)
            else:
                return None

            try:
                return datetime(year, month, day).date()
            except ValueError:
                return None

        return None

    numeric_date_token = (
        r"(?:"
        r"\d{1,2}[./-]\d{1,2}[./-]\d{2,4}"
        r"|"
        r"\d{4}[./-]\d{1,2}[./-]\d{1,2}"
        r")"
    )

    textual_month = (
        r"(?:"
        r"janvier|janv|février|fevrier|févr|fevr|mars|avril|avr|mai|"
        r"juin|juillet|juil|août|aout|septembre|sept|octobre|oct|"
        r"novembre|nov|décembre|decembre|déc|dec|"
        r"january|jan|february|feb|march|mar|april|apr|may|june|jun|"
        r"july|jul|august|aug|september|sep|october|november|december"
        r")"
    )
    textual_date_token = (
        rf"(?:\d{{1,2}}\s+{textual_month}(?:\s+\d{{2,4}})?)"
    )
    date_token = rf"(?:{numeric_date_token}|{textual_date_token})"

    period_patterns = (
        re.compile(
            rf"(?i)\b(?:account\s+statement|statement)"
            rf"[^\n]{{0,80}}?"
            rf"(?:from(?:\s+date)?|period(?:\s+from)?)"
            rf"\s*(?P<start>{date_token})"
            rf"\s*(?:to|through|thru|[-–—])\s*"
            rf"(?P<end>{date_token})"
        ),
        re.compile(
            rf"(?i)\bstatement\s+period"
            rf"[^\n]{{0,30}}"
            rf"(?P<start>{date_token})"
            rf"\s*(?:to|through|thru|[-–—])\s*"
            rf"(?P<end>{date_token})"
        ),
        re.compile(
            rf"(?i)\b(?:p[ée]riode(?:\s+du\s+relev[ée])?|relev[ée])"
            rf"[^\n]{{0,80}}?"
            rf"(?:du|de)\s*(?P<start>{date_token})"
            rf"\s*(?:au|à|a|[-–—])\s*"
            rf"(?P<end>{date_token})"
        ),
        re.compile(
            rf"(?:كشف\s+الحساب|فترة\s+الكشف|الفترة)"
            rf"[^\n]{{0,80}}?"
            rf"(?:من)\s*(?P<start>{numeric_date_token})"
            rf"\s*(?:إلى|الى|[-–—])\s*"
            rf"(?P<end>{numeric_date_token})"
        ),
        # ADDITIVE v28 — explicit statement-adjacent numeric range.
        #
        # Some real statements expose the period as a date range next to a
        # generic "Statement" label without the literal word "period".  The
        # date range itself is structural evidence.  This branch is deliberately
        # narrow: two complete numeric dates must appear on the same physical
        # line next to a statement/relevé/account-statement role.
        re.compile(
            rf"(?i)\b(?:account\s+statement|statement|relev[ée])"
            rf"[^\n]{{0,60}}?"
            rf"(?P<start>{numeric_date_token})"
            rf"\s*(?:to|through|thru|au|à|a|[-–—])\s*"
            rf"(?P<end>{numeric_date_token})"
        ),
        # ADDITIVE v30 — statement title on one line, explicit period on the
        # immediately following physical line.  This is source-document
        # consistency evidence only.  It never changes parser output.
        re.compile(
            rf"(?i)\b(?:relev[ée](?:\s+de)?\s+[^\n]{{0,50}}|"
            rf"account\s+statement|statement)"
            rf"\s*\n\s*"
            rf"(?:du|de|from)\s*"
            rf"(?P<start>{numeric_date_token})"
            rf"\s*(?:au|à|a|to|through|thru|[-–—])\s*"
            rf"(?P<end>{numeric_date_token})"
        ),
    )

    auxiliary_period_markers = (
        "miles",
        "points",
        "loyalty",
        "rewards",
        "reward",
        "fidélité",
        "fidelite",
        "récompenses",
        "recompenses",
        "أميال",
        "نقاط",
        "مكافآت",
    )

    candidates = []

    for pattern_index, pattern in enumerate(period_patterns):
        for match in pattern.finditer(raw):
            match_start = match.start()
            match_end = match.end()

            context_start = max(0, match_start - 180)
            context_end = min(len(raw), match_end + 180)
            context = " ".join(
                raw[context_start:context_end].split()
            ).casefold()

            auxiliary = any(
                marker.casefold() in context
                for marker in auxiliary_period_markers
            )

            start_raw = match.group("start")
            end_raw = match.group("end")

            end = _parse_date_token(end_raw)
            start = _parse_date_token(
                start_raw,
                default_year=(end.year if end is not None else None),
            )

            if end is None:
                start_with_year = _parse_date_token(start_raw)
                end = _parse_date_token(
                    end_raw,
                    default_year=(
                        start_with_year.year
                        if start_with_year is not None
                        else None
                    ),
                )
                if start is None:
                    start = start_with_year

            if start is None or end is None or start > end:
                continue

            if (end - start).days > 550:
                continue

            candidates.append(
                {
                    "start": start,
                    "end": end,
                    "matched_text": " ".join(
                        match.group(0).split()
                    )[:240],
                    "auxiliary": auxiliary,
                    "pattern_index": pattern_index,
                    "position": match_start,
                }
            )

    financial_candidates = [
        item for item in candidates
        if not item["auxiliary"]
    ]

    if not financial_candidates:
        return {
            "available": False,
            "source_period_inconsistency_detected": False,
            "period_start": None,
            "period_end": None,
            "dated_transaction_count": len(txs),
            "out_of_period_transaction_count": 0,
            "out_of_period_samples": [],
            "evidence_source": None,
            "rejected_auxiliary_period_count": len(
                [item for item in candidates if item["auxiliary"]]
            ),
        }

    # Prefer an explicit accounting/posting/value date when the responsible
    # structural parser emitted one. Historical single-date rows remain
    # unchanged. This avoids evaluating a dual-date statement period only
    # against the commercial/operation date.
    def _period_observation_date(tx: dict):
        for key in (
            "value_date",
            "posting_date",
            "booking_date",
            "date",
        ):
            raw_date = tx.get(key)
            if not raw_date:
                continue
            try:
                return (
                    datetime.fromisoformat(
                        str(raw_date)[:10]
                    ).date(),
                    key,
                )
            except Exception:
                continue
        return None, None

    dated_dates = []
    for tx in txs:
        observed, _date_role = _period_observation_date(tx)
        if observed is not None:
            dated_dates.append(observed)

    # A one-day physical boundary tolerance is allowed only for rows from a
    # structural dual-date family. This covers statement-cycle cutoffs where a
    # transaction printed immediately adjacent to the cycle boundary is still
    # visibly part of the statement. Single-date historical families keep the
    # exact historical comparison.
    def _period_contains(item, observed, tx=None):
        tolerance_days = 0
        if isinstance(tx, dict):
            parser_family = str(
                tx.get("parser_family") or ""
            ).strip().lower()
            if "dual" in parser_family and "date" in parser_family:
                tolerance_days = 1

        from datetime import timedelta
        return (
            item["start"] - timedelta(days=tolerance_days)
            <= observed
            <= item["end"] + timedelta(days=tolerance_days)
        )

    def _coverage(item):
        covered = sum(
            1
            for tx in txs
            for observed, _role in [_period_observation_date(tx)]
            if observed is not None
            and _period_contains(item, observed, tx)
        )
        return (
            covered,
            -item["position"],
        )

    selected = max(financial_candidates, key=_coverage)
    period_start = selected["start"]
    period_end = selected["end"]
    matched_text = selected["matched_text"]

    dated = []
    for tx in txs:
        parsed, date_role = _period_observation_date(tx)
        if parsed is None:
            continue
        dated.append((parsed, date_role, tx))

    out_of_period = [
        (parsed, date_role, tx)
        for parsed, date_role, tx in dated
        if not _period_contains(selected, parsed, tx)
    ]

    samples = [
        {
            "date": parsed.isoformat(),
            "date_role": date_role,
            "description": str(
                tx.get("description") or ""
            )[:160],
            "amount": tx.get("amount"),
            "type": tx.get("type"),
        }
        for parsed, date_role, tx in out_of_period[:12]
    ]

    # ADDITIVE v28 — compare explicitly dated opening/closing balance roles
    # with the selected financial statement period.
    #
    # A source statement can reconcile arithmetically while still printing a
    # structurally contradictory period marker, e.g. an "Opening balance on"
    # date many months away from the statement start.  This is source-document
    # consistency evidence only; it never mutates parser output, routing,
    # transactions, candidate selection, or financial authority.
    role_date_token = (
        rf"(?:{numeric_date_token}|"
        rf"\d{{1,2}}\s+{textual_month}(?:\s+\d{{2,4}})?)"
    )

    role_patterns = (
        (
            "opening",
            re.compile(
                rf"(?i)\b(?:opening\s+balance|beginning\s+balance|"
                rf"solde\s+(?:initial|d[ée]but)|"
                rf"الرصيد\s+الافتتاحي|رصيد\s+افتتاحي)"
                rf"[^\n]{{0,40}}?"
                rf"(?:on|au|le|في)?\s*"
                rf"(?P<date>{role_date_token})"
            ),
        ),
        (
            "closing",
            re.compile(
                rf"(?i)\b(?:closing\s+balance|ending\s+balance|"
                rf"solde\s+(?:final|de\s+cl[ôo]ture)|"
                rf"الرصيد\s+الختامي|رصيد\s+ختامي)"
                rf"[^\n]{{0,40}}?"
                rf"(?:on|au|le|في)?\s*"
                rf"(?P<date>{role_date_token})"
            ),
        ),
    )

    def _resolve_role_date(token: str, role: str):
        anchor = period_start if role == "opening" else period_end

        direct = _parse_date_token(token)
        if direct is not None:
            return direct

        candidates_for_year = []
        for candidate_year in (
            anchor.year - 1,
            anchor.year,
            anchor.year + 1,
        ):
            parsed = _parse_date_token(
                token,
                default_year=candidate_year,
            )
            if parsed is not None:
                candidates_for_year.append(parsed)

        if not candidates_for_year:
            return None

        return min(
            candidates_for_year,
            key=lambda value: abs((value - anchor).days),
        )

    role_date_inconsistencies = []
    ROLE_DATE_TOLERANCE_DAYS = 7

    for role, role_pattern in role_patterns:
        anchor = period_start if role == "opening" else period_end

        for role_match in role_pattern.finditer(raw):
            raw_role_date = role_match.group("date")
            parsed_role_date = _resolve_role_date(
                raw_role_date,
                role,
            )
            if parsed_role_date is None:
                continue

            delta_days = (parsed_role_date - anchor).days
            if abs(delta_days) <= ROLE_DATE_TOLERANCE_DAYS:
                continue

            role_date_inconsistencies.append(
                {
                    "role": role,
                    "printed_date": parsed_role_date.isoformat(),
                    "expected_anchor": anchor.isoformat(),
                    "delta_days": delta_days,
                    "matched_text": " ".join(
                        role_match.group(0).split()
                    )[:200],
                }
            )

    detected = bool(
        out_of_period
        or role_date_inconsistencies
    )

    return {
        "available": True,
        "source_period_inconsistency_detected": detected,
        "period_start": period_start.isoformat(),
        "period_end": period_end.isoformat(),
        "dated_transaction_count": len(dated),
        "out_of_period_transaction_count": len(out_of_period),
        "out_of_period_samples": samples,
        "source_role_date_inconsistency_count": len(
            role_date_inconsistencies
        ),
        "source_role_date_inconsistencies": (
            role_date_inconsistencies[:12]
        ),
        "matched_period_text": matched_text,
        "evidence_source": (
            "explicit_financial_statement_period_vs_"
            "transaction_and_balance_role_dates"
        ),
        "rejected_auxiliary_period_count": len(
            [item for item in candidates if item["auxiliary"]]
        ),
    }


def collect_explicit_source_balance_diagnostic(
    extraction_status: dict | None,
    transactions: list[dict] | None,
) -> dict:
    """Collect only parser-produced source-balance inconsistency evidence.

    Audit-only: no parser/router/candidate/KPI mutation and no recomputation
    of accounting contradictions from generic flags.
    """
    extraction_status = dict(extraction_status or {})
    details = dict(extraction_status.get("details") or {})
    txs = [tx for tx in (transactions or []) if isinstance(tx, dict)]

    try:
        explicit_rows = int(details.get("source_inconsistent_balance_rows") or 0)
    except (TypeError, ValueError):
        explicit_rows = 0

    explicit_samples = details.get("source_inconsistent_balance_samples")
    if not isinstance(explicit_samples, list):
        explicit_samples = []

    flagged_transactions = [
        tx for tx in txs
        if tx.get("source_accounting_inconsistency") is True
    ]

    transaction_aggregate_rows = 0
    transaction_aggregate_detected = False

    for tx in txs:
        try:
            transaction_aggregate_rows = max(
                transaction_aggregate_rows,
                int(tx.get("source_inconsistent_balance_rows") or 0),
            )
        except (TypeError, ValueError):
            pass

        if tx.get("source_balance_inconsistency_detected") is True:
            transaction_aggregate_detected = True

    mismatch_count = max(
        explicit_rows,
        len(flagged_transactions),
        transaction_aggregate_rows,
    )
    samples = list(explicit_samples[:12])

    if not samples and flagged_transactions:
        for tx in flagged_transactions[:12]:
            samples.append(
                {
                    "date": tx.get("date"),
                    "description": str(tx.get("description") or "")[:160],
                    "balance": tx.get("balance"),
                    "amount": tx.get("amount"),
                    "type": tx.get("type"),
                }
            )

    available = bool(
        mismatch_count > 0
        or samples
        or transaction_aggregate_detected
    )

    return {
        "available": available,
        "source_balance_inconsistency_detected": bool(
            mismatch_count > 0 or transaction_aggregate_detected
        ),
        "source_inconsistent_balance_rows": mismatch_count,
        "source_inconsistent_balance_samples": samples,
        "evidence_source": "explicit_parser_diagnostic" if available else None,
    }


def finance_verification_copy(
    *,
    status: str,
    language: str = "en",
) -> dict:
    """Return verification UI copy in the finance language selected by the user."""
    if language not in {"en", "fr", "ar"}:
        language = "en"

    copy = {
        "verified": {
            "en": {
                "title": "Analysis verified",
                "message": "The extracted transactions are reconciled with the accounting evidence available in the statement.",
            },
            "fr": {
                "title": "Analyse vérifiée",
                "message": "Les transactions extraites sont réconciliées avec les éléments comptables disponibles dans le relevé.",
            },
            "ar": {
                "title": "تم التحقق من التحليل",
                "message": "تمت مطابقة المعاملات المستخرجة مع الأدلة المحاسبية المتاحة في كشف الحساب.",
            },
        },
        "verified_with_source_inconsistency": {
            "en": {
                "title": "Transactions reconciled — statement inconsistency detected",
                "message": "The extracted transaction ledger reconciles, but the statement's own printed summary contains an internal accounting inconsistency. The statement is not presented as fully verified.",
            },
            "fr": {
                "title": "Transactions réconciliées — incohérence détectée dans le relevé",
                "message": "Le ledger des transactions extraites est réconcilié, mais le résumé imprimé du relevé contient une incohérence comptable interne. Le relevé n’est pas présenté comme entièrement vérifié.",
            },
            "ar": {
                "title": "تمت مطابقة المعاملات — تم اكتشاف تناقض في كشف الحساب",
                "message": "تمت مطابقة سجل المعاملات المستخرجة، لكن الملخص المطبوع في كشف الحساب يحتوي على تناقض محاسبي داخلي. لذلك لا يتم عرض كشف الحساب على أنه متحقق منه بالكامل.",
            },
        },
        "unverified": {
            "en": {
                "title": "Analysis not verified",
                "message": "The extracted transactions could not be fully reconciled with the available accounting evidence in the statement.",
            },
            "fr": {
                "title": "Analyse non vérifiée",
                "message": "Les transactions extraites n’ont pas pu être entièrement réconciliées avec les éléments comptables disponibles dans le relevé.",
            },
            "ar": {
                "title": "لم يتم التحقق من التحليل",
                "message": "تعذر مطابقة المعاملات المستخرجة بالكامل مع الأدلة المحاسبية المتاحة في كشف الحساب.",
            },
        },
    }

    selected = copy.get(status, copy["unverified"])
    return selected.get(language, selected["en"])


def collect_source_section_total_contradiction(
    statement_text: str | None,
) -> dict:
    """Detect a contradiction between complete section subtotals and a global TOTAL.

    Audit/display only:
    - no parser/router/candidate modification;
    - no transaction mutation;
    - no bank/country/currency/merchant identity;
    - analyses may remain visible even when inconsistency is detected.

    Structural proof requires:
    1) a Debit/Credit accounting table header;
    2) at least two section SUBTOTAL rows, each with exactly two money values;
    3) one later global TOTAL row with exactly two money values;
    4) the sum of section subtotals materially differs from the global TOTAL.
    """
    raw_lines = [
        " ".join(str(line or "").split())
        for line in str(statement_text or "").splitlines()
    ]

    money_token_re = re.compile(
        r"(?<!\d)"
        r"(?:\d{1,3}(?:[ .,'’]\d{3})+|\d+)"
        r"(?:[.,]\d{2})"
        r"(?!\d)"
    )

    def _money(token: str):
        return _verification_money_to_float(token)

    header_indexes = []
    for i, line in enumerate(raw_lines):
        lowered = line.casefold()
        if (
            re.search(r"\b(?:d[ée]bit|debit|مدين)\b", lowered, re.I)
            and re.search(r"\b(?:cr[ée]dit|credit|دائن)\b", lowered, re.I)
            and re.search(r"\b(?:date|التاريخ)\b", lowered, re.I)
        ):
            header_indexes.append(i)

    if not header_indexes:
        return {
            "available": False,
            "source_section_total_inconsistency_detected": False,
            "section_subtotal_count": 0,
            "section_debit_total": None,
            "section_credit_total": None,
            "global_debit_total": None,
            "global_credit_total": None,
            "debit_gap": None,
            "credit_gap": None,
            "evidence_source": None,
        }

    subtotal_rows = []
    global_rows = []

    for i, line in enumerate(raw_lines):
        lowered = line.casefold()
        values = [_money(token) for token in money_token_re.findall(line)]
        values = [value for value in values if value is not None]

        # Section-role classification only.
        if re.match(
            r"^(?:sous\s*total|soustotal|subtotal|sub\s*total|"
            r"المجموع\s+الفرعي)",
            lowered,
            re.I,
        ):
            if len(values) == 2:
                subtotal_rows.append(
                    {
                        "line_index": i,
                        "line": line[:240],
                        "debit": round(abs(float(values[0])), 2),
                        "credit": round(abs(float(values[1])), 2),
                    }
                )
            continue

        if re.match(
            r"^(?:total|totaux|المجموع)\b",
            lowered,
            re.I,
        ):
            if len(values) == 2:
                global_rows.append(
                    {
                        "line_index": i,
                        "line": line[:240],
                        "debit": round(abs(float(values[0])), 2),
                        "credit": round(abs(float(values[1])), 2),
                    }
                )

    if len(subtotal_rows) < 2 or not global_rows:
        return {
            "available": False,
            "source_section_total_inconsistency_detected": False,
            "section_subtotal_count": len(subtotal_rows),
            "section_debit_total": None,
            "section_credit_total": None,
            "global_debit_total": None,
            "global_credit_total": None,
            "debit_gap": None,
            "credit_gap": None,
            "evidence_source": None,
        }

    # Use the last global TOTAL after the first detected accounting header,
    # and only section subtotals physically preceding it.
    first_header = min(header_indexes)
    eligible_globals = [
        row for row in global_rows
        if row["line_index"] > first_header
    ]
    if not eligible_globals:
        return {
            "available": False,
            "source_section_total_inconsistency_detected": False,
            "section_subtotal_count": len(subtotal_rows),
            "section_debit_total": None,
            "section_credit_total": None,
            "global_debit_total": None,
            "global_credit_total": None,
            "debit_gap": None,
            "credit_gap": None,
            "evidence_source": None,
        }

    global_row = eligible_globals[-1]
    scoped_subtotals = [
        row for row in subtotal_rows
        if first_header < row["line_index"] < global_row["line_index"]
    ]

    if len(scoped_subtotals) < 2:
        return {
            "available": False,
            "source_section_total_inconsistency_detected": False,
            "section_subtotal_count": len(scoped_subtotals),
            "section_debit_total": None,
            "section_credit_total": None,
            "global_debit_total": global_row["debit"],
            "global_credit_total": global_row["credit"],
            "debit_gap": None,
            "credit_gap": None,
            "evidence_source": None,
        }

    section_debit = round(sum(row["debit"] for row in scoped_subtotals), 2)
    section_credit = round(sum(row["credit"] for row in scoped_subtotals), 2)
    debit_gap = round(section_debit - global_row["debit"], 2)
    credit_gap = round(section_credit - global_row["credit"], 2)

    detected = bool(
        abs(debit_gap) > 0.02
        or abs(credit_gap) > 0.02
    )

    return {
        "available": True,
        "source_section_total_inconsistency_detected": detected,
        "section_subtotal_count": len(scoped_subtotals),
        "section_debit_total": section_debit,
        "section_credit_total": section_credit,
        "global_debit_total": global_row["debit"],
        "global_credit_total": global_row["credit"],
        "debit_gap": debit_gap,
        "credit_gap": credit_gap,
        "section_samples": scoped_subtotals[:12],
        "global_total_sample": global_row,
        "evidence_source": "section_subtotals_vs_global_total",
    }


def build_frontend_verification(
    *,
    extraction_status: dict | None,
    quality: dict | None,
    transactions: list[dict] | None,
    kpi_transactions: list[dict] | None,
    currency: str | None = None,
    output_language: str = "en",
    source_statement_consistency: dict | None = None,
    source_balance_diagnostic: dict | None = None,
    source_period_diagnostic: dict | None = None,
    source_section_total_diagnostic: dict | None = None,
) -> dict:
    """Build the frontend contract without changing parser or candidate decisions."""
    extraction_status = dict(extraction_status or {})
    quality = dict(quality or {})
    details = dict(extraction_status.get("details") or {})
    source_consistency = dict(source_statement_consistency or {})
    source_balance = dict(source_balance_diagnostic or {})
    source_period = dict(source_period_diagnostic or {})
    source_section_total = dict(source_section_total_diagnostic or {})

    reconciliation_status = str(
        details.get("reconciliation_status")
        or extraction_status.get("status")
        or "unavailable"
    ).strip().lower()

    authority_basis = str(
        details.get("authority_basis") or ""
    ).strip().lower()

    internally_reconciled_authority = bool(
        reconciliation_status == "internally_supported"
        and authority_basis
        == "internal_accounting_and_balance_reconciliation"
    )

    accounting_reconciled = bool(
        extraction_status.get("recognized") is True
        and extraction_status.get("financial_authority") is True
        and str(
            extraction_status.get("status") or ""
        ).strip().lower() == "reconciled"
        and (
            reconciliation_status == "reconciled"
            or internally_reconciled_authority
        )
    )

    # Display-level diagnostic only. An "internally_supported" candidate is
    # shown as reconciled only when the extractor has already promoted it to
    # financial authority through the strict internal accounting+balance proof.
    ledger_status = (
        "reconciled"
        if accounting_reconciled
        else (
            "internally_supported"
            if (
                extraction_status.get("recognized") is True
                and reconciliation_status == "internally_supported"
            )
            else "not_available"
        )
    )

    source_balance_inconsistency_detected = bool(
        source_balance.get("source_balance_inconsistency_detected") is True
    )
    source_period_inconsistency_detected = bool(
        source_period.get("source_period_inconsistency_detected") is True
    )
    source_section_total_inconsistency_detected = bool(
        source_section_total.get(
            "source_section_total_inconsistency_detected"
        ) is True
    )
    source_inconsistency_detected = bool(
        source_consistency.get("source_inconsistency_detected") is True
        or source_balance_inconsistency_detected
        or source_period_inconsistency_detected
        or source_section_total_inconsistency_detected
        or extraction_status.get("reason") == "source_statement_section_inconsistency"
    )

    # ADDITIVE v14 — display policy for recognized but unreconciled statements.
    #
    # Product contract:
    # - Reconciliation/financial authority remains unchanged.
    # - A recognized statement with usable extracted transactions may still
    #   produce a non-verified financial analysis.
    # - Source inconsistency diagnostics remain visible as warnings and are
    #   never converted into financial authority.
    # - Analysis is withheld only when no usable transaction basis exists or
    #   when an upstream component explicitly marks the analysis unsafe.
    #
    # This is display/analysis availability policy only. It does not modify
    # parser routing, parser selection, candidate ranking, ledger authority,
    # transaction direction, or accounting reconciliation.
    usable_analysis_transactions = list(
        kpi_transactions
        if kpi_transactions is not None
        else (transactions or [])
    )

    has_usable_transactions = bool(
        extraction_status.get("recognized") is True
        and len(usable_analysis_transactions) > 0
    )

    explicit_analysis_block = bool(
        details.get("analysis_blocked") is True
        or details.get("unsafe_for_analysis") is True
    )

    analysis_available_unverified = bool(
        not accounting_reconciled
        and has_usable_transactions
        and not explicit_analysis_block
    )

    analysis_withheld = bool(
        not accounting_reconciled
        and not analysis_available_unverified
    )

    source_consistent = source_consistency.get("source_consistent")
    if (
        source_balance_inconsistency_detected
        or source_period_inconsistency_detected
        or source_section_total_inconsistency_detected
    ):
        source_consistent = False

    source_consistency_available = bool(
        source_consistency.get("available")
        or source_balance.get("available")
        or source_period.get("available")
        or source_section_total.get("available")
    )

    if accounting_reconciled and source_inconsistency_detected:
        verification_status = "verified_with_source_inconsistency"
        reason = "statement_summary_conflict"
    elif accounting_reconciled:
        verification_status = "verified"
        reason = "accounting_reconciled"
    else:
        verification_status = "unverified"
        reason = "accounting_not_reconciled"

    localized = finance_verification_copy(
        status=verification_status,
        language=output_language,
    )

    txs = list(transactions or [])
    kpi_txs = list(kpi_transactions or [])
    currency_value = str(currency or "unknown").strip().upper() or "UNKNOWN"
    language_value = output_language if output_language in {"en", "fr", "ar"} else "en"

    return {
        "status": verification_status,
        "reason": reason,
        "title": localized.get("title"),
        "message": localized.get("message"),
        "language": language_value,
        "recognized": extraction_status.get("recognized") is True,
        "financial_authority": extraction_status.get("financial_authority") is True,
        "accounting_reconciled": accounting_reconciled,
        "ledger_reconciled": accounting_reconciled,
        "ledger_status": ledger_status,
        "reconciliation_status": reconciliation_status,
        "source_consistency_available": source_consistency_available,
        "source_consistent": source_consistent,
        "source_inconsistency_detected": source_inconsistency_detected,
        "analysis_available": bool(accounting_reconciled or analysis_available_unverified),
        "analysis_available_unverified": analysis_available_unverified,
        "analysis_withheld": analysis_withheld,
        "analysis_basis": details.get("analysis_basis"),
        "source_inconsistent_observed_analysis": bool(
            details.get("source_inconsistent_observed_analysis") is True
        ),
        "strong_warning_required": bool(
            details.get("strong_warning_required") is True
        ),
        "materiality_policy": details.get("materiality_policy"),
        "materiality_threshold": details.get("materiality_threshold"),
        "max_direction_gap_ratio": details.get("max_direction_gap_ratio"),
        "income_gap": details.get("income_gap"),
        "expense_gap": details.get("expense_gap"),
        "source_balance_inconsistency_detected": source_balance_inconsistency_detected,
        "source_period_inconsistency_detected": source_period_inconsistency_detected,
        "source_period_start": source_period.get("period_start"),
        "source_period_end": source_period.get("period_end"),
        "source_out_of_period_transaction_count": int(
            source_period.get("out_of_period_transaction_count") or 0
        ),
        "source_out_of_period_samples": list(
            source_period.get("out_of_period_samples") or []
        ),
        "source_inconsistent_balance_rows": int(
            source_balance.get("source_inconsistent_balance_rows") or 0
        ),
        "transaction_count": len(kpi_txs),
        "extracted_transaction_count": len(txs),
        "excluded_transaction_count": max(0, len(txs) - len(kpi_txs)),
        "currency": currency_value,
        "confidence": quality.get("confidence"),
        "analysis_scope": quality.get("analysis_scope", "full"),
        "analysis_scope_reason": quality.get("analysis_scope_reason"),
        "checks": {
            "statement_recognized": extraction_status.get("recognized") is True,
            "financial_authority": extraction_status.get("financial_authority") is True,
            "transactions_extracted": len(kpi_txs) > 0,
            "currency_detected": currency_value not in {"", "UNKNOWN", "NONE"},
            "accounting_reconciled": accounting_reconciled,
            "ledger_reconciled": accounting_reconciled,
            "source_consistent": source_consistent,
        },
        "evidence": {
            "income_gap": details.get("income_gap"),
            "expense_gap": details.get("expense_gap"),
            "total_gap": details.get("total_gap"),
            "official_components_compared": details.get("official_components_compared"),
            "selection_reason": details.get("selection_reason"),
            "parser": details.get("parser") or details.get("parser_name"),
            "source_accounting_gap": source_consistency.get("accounting_gap"),
            "source_calculated_ending_balance": source_consistency.get(
                "calculated_ending_balance"
            ),
            "source_opening_balance": source_consistency.get("opening_balance"),
            "source_deposits": source_consistency.get("deposits"),
            "source_withdrawals": source_consistency.get("withdrawals"),
            "source_ending_balance": source_consistency.get("ending_balance"),
            "source_summary_type": source_consistency.get("source"),
            "ledger_status": ledger_status,
            "source_balance_diagnostic_source": source_balance.get("evidence_source"),
            "source_inconsistent_balance_rows": int(
                source_balance.get("source_inconsistent_balance_rows") or 0
            ),
            "source_inconsistent_balance_samples": list(
                source_balance.get("source_inconsistent_balance_samples") or []
            )[:12],
        },
    }

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


print(
    "RUNEXA_FINANCE_HANDLER_VERSION",
    "v30-source-contradiction-display-only-gate",
)

print(
    "SOURCE_PERIOD_DIAGNOSTIC_VERSION",
    "v5-financial-period-and-section-total-source-contradiction",
)

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
        ocr_messages = {
            "en": "This PDF appears to be scanned or has no usable text layer. OCR is required before financial analysis.",
            "fr": "Ce PDF semble être scanné ou ne contient pas de couche texte exploitable. Un traitement OCR est requis avant l’analyse financière.",
            "ar": "يبدو أن ملف PDF ممسوح ضوئياً أو لا يحتوي على طبقة نص قابلة للاستخدام. يلزم التعرف الضوئي على الحروف قبل التحليل المالي.",
        }
        return {
            "status": "ocr_required",
            "analysis_status": "ocr_required",
            "reason": "scanned_pdf_requires_ocr",
            "transactions": [],
            "summary": {},
            "totals": {"income": 0, "expenses": 0},
            "message": ocr_messages.get(output_language, ocr_messages["en"]),
            "disclaimer": get_finance_disclaimer(output_language),
            "verification": {
                "status": "unverified",
                "recognized": False,
                "financial_authority": False,
                "accounting_reconciled": False,
                "reconciliation_status": "unavailable",
                "transaction_count": 0,
                "extracted_transaction_count": 0,
                "excluded_transaction_count": 0,
                "currency": "UNKNOWN",
                "confidence": 0,
                "checks": {
                    "statement_recognized": False,
                    "financial_authority": False,
                    "transactions_extracted": False,
                    "currency_detected": False,
                    "accounting_reconciled": False,
                },
            },
        }

    update_job_progress(
        job,
        db,
        32,
        finance_progress_message("transactions", output_language),
    )

    # ADDITIVE v6 — preserve PDF geometry for file_bytes inputs.
    #
    # Historical file_path/storage_path behavior remains unchanged.  The only
    # new branch is for jobs carrying the PDF as hexadecimal bytes: previously
    # those jobs were reduced to flattened text before transaction extraction,
    # so structural parsers could not observe physical Debit/Credit columns.
    #
    # Materialization is transport-only: it does not select a parser, alter the
    # candidate engine, or infer transaction direction from bank/language/text.
    if "file_path" in locals() and file_path:
        transactions = extract_transactions_from_pdf_path(str(file_path), text)
    elif file_bytes_hex:
        import os
        import tempfile

        temporary_pdf_path = None

        try:
            with tempfile.NamedTemporaryFile(
                mode="wb",
                suffix=".pdf",
                delete=False,
            ) as temporary_pdf:
                temporary_pdf.write(content)
                temporary_pdf_path = temporary_pdf.name

            print(
                "FINANCE_FILE_BYTES_PDF_GEOMETRY_PATH",
                {
                    "enabled": True,
                    "bytes": len(content),
                },
            )

            transactions = extract_transactions_from_pdf_path(
                str(temporary_pdf_path),
                text,
            )
        except OSError as exc:
            # Backward-compatible fallback: if the runtime cannot materialize a
            # temporary PDF, preserve the historical flattened-text behavior.
            print(
                "FINANCE_FILE_BYTES_PDF_GEOMETRY_FALLBACK",
                {
                    "reason": "temporary_pdf_materialization_failed",
                    "error": type(exc).__name__,
                },
            )
            transactions = extract_transactions(text)
        finally:
            if temporary_pdf_path:
                try:
                    os.unlink(temporary_pdf_path)
                except OSError:
                    pass
    else:
        transactions = extract_transactions(text)

    # ADDITIVE v11 — allow analysis from a strong audit candidate when the
    # official-flow discrepancy is immaterial. This does NOT grant financial
    # authority and does NOT change parser/candidate selection. The selected
    # ledger remains unreconciled; the worker only uses the preserved audit
    # candidate as an explicitly non-verified analytical basis.
    extraction_status = get_finance_extraction_status()
    unverified_analysis_context = None

    # ADDITIVE v25 — do not analyze across multiple accounting scopes.
    #
    # The responsible structural parser may reject a PDF because the physical
    # document contains several account/statement-period scopes. Candidate
    # routing is intentionally left untouched; this is output-policy only.
    # A generic fallback ledger must not be combined with summary totals from
    # another scope.
    scope_rejection_evidence = (
        get_finance_scope_rejection_evidence() or {}
    )

    if (
        scope_rejection_evidence.get("reason")
        == "multiple_account_period_scopes"
        and scope_rejection_evidence.get("analysis_safe_to_merge") is False
    ):
        withheld_currency = detect_currency(text) or "UNKNOWN"

        message_by_language = {
            "en": (
                "Multiple accounting scopes were detected in this PDF. "
                "No combined financial analysis was generated because the "
                "statement periods and/or account scopes cannot be merged safely."
            ),
            "fr": (
                "Plusieurs périmètres comptables ont été détectés dans ce PDF. "
                "Aucune analyse financière combinée n’a été générée, car les "
                "périodes et/ou comptes ne peuvent pas être fusionnés de manière fiable."
            ),
            "ar": (
                "تم اكتشاف عدة نطاقات محاسبية داخل ملف PDF. "
                "لم يتم إنشاء تحليل مالي موحّد لأن فترات الكشوف و/أو نطاقات "
                "الحسابات لا يمكن دمجها بشكل موثوق."
            ),
        }

        withheld_result = {
            "status": "recognized_but_unreconciled",
            "analysis_status": "analysis_withheld",
            "reason": "multiple_account_period_scopes",
            "recognized": True,
            "financial_authority": False,
            "currency": withheld_currency,
            "currency_detected": withheld_currency,
            "transactions": [],
            "summary": {},
            "totals": {
                "income": 0,
                "expenses": 0,
            },
            "message": message_by_language.get(
                output_language,
                message_by_language["en"],
            ),
            "verification": {
                "status": "unverified",
                "recognized": True,
                "financial_authority": False,
                "accounting_reconciled": False,
                "ledger_reconciled": False,
                "ledger_status": "not_reconciled",
                "reconciliation_status": "multiple_account_period_scopes",
                "source_consistency_available": False,
                "source_consistent": None,
                "source_inconsistency_detected": False,
                "analysis_available": False,
                "analysis_available_unverified": False,
                "analysis_withheld": True,
                "transaction_count": 0,
                "extracted_transaction_count": int(
                    scope_rejection_evidence.get("transaction_count") or 0
                ),
                "excluded_transaction_count": 0,
                "currency": withheld_currency,
                "confidence": 0,
                "checks": {
                    "statement_recognized": True,
                    "financial_authority": False,
                    "transactions_extracted": bool(
                        scope_rejection_evidence.get("transaction_count")
                    ),
                    "currency_detected": bool(
                        withheld_currency
                        and withheld_currency != "UNKNOWN"
                    ),
                    "accounting_reconciled": False,
                    "ledger_reconciled": False,
                    "single_accounting_scope": False,
                },
                "details": {
                    **scope_rejection_evidence,
                    "analysis_withheld_reason": (
                        "multiple_account_period_scopes"
                    ),
                },
            },
        }

        print(
            "COMPOSITE_SCOPE_ANALYSIS_WITHHELD",
            {
                "reason": "multiple_account_period_scopes",
                "scope_count": scope_rejection_evidence.get("scope_count"),
                "transaction_count": scope_rejection_evidence.get(
                    "transaction_count"
                ),
                "period_count": scope_rejection_evidence.get("period_count"),
                "account_count": scope_rejection_evidence.get("account_count"),
                "analysis_withheld": True,
                "financial_authority": False,
            },
        )

        return withheld_result

    if (
        not transactions
        and extraction_status.get("recognized") is True
        and extraction_status.get("financial_authority") is not True
    ):
        observed_analysis_candidate = (
            get_finance_observed_analysis_candidate() or {}
        )
        generic_audit_candidate = get_finance_audit_candidate() or {}

        extraction_details = dict(
            extraction_status.get("details") or {}
        )
        responsible_parser = str(
            extraction_details.get("parser") or ""
        ).strip()

        observed_parser = str(
            observed_analysis_candidate.get("parser") or ""
        ).strip()

        use_observed_parser_candidate = bool(
            observed_analysis_candidate.get("observed_transactions_only") is True
            and observed_analysis_candidate.get("financial_authority") is not True
            and responsible_parser
            and observed_parser == responsible_parser
        )

        audit_candidate = (
            observed_analysis_candidate
            if use_observed_parser_candidate
            else generic_audit_candidate
        )

        audit_transactions = [
            dict(tx)
            for tx in (audit_candidate.get("transactions") or [])
            if isinstance(tx, dict) and tx.get("date")
        ]

        try:
            max_gap_ratio = float(
                audit_candidate.get("max_direction_gap_ratio")
            )
        except (TypeError, ValueError, OverflowError):
            max_gap_ratio = float("inf")

        # International materiality rule requested by product policy:
        # ratio-based, never bank/country/currency specific. Up to 10% of the
        # affected official flow direction may be shown as an UNVERIFIED
        # analysis when a structurally usable audit ledger exists. This never
        # grants financial authority and never upgrades the result to Verified.
        # Source/candidate gaps above 10% remain withheld.
        IMMATERIAL_UNRECONCILED_RATIO = 0.10

        structurally_usable_audit = bool(
            len(audit_transactions) >= 3
            and all(
                tx.get("date")
                and str(tx.get("description") or "").strip()
                and float(tx.get("amount") or 0) != 0
                and str(tx.get("type") or "").lower() in {"income", "expense"}
                for tx in audit_transactions
            )
        )

        observed_parser_analysis_basis = bool(
            use_observed_parser_candidate
            and audit_candidate.get("source_detail_unreconciled") is True
        )

        if (
            structurally_usable_audit
            and (
                max_gap_ratio <= IMMATERIAL_UNRECONCILED_RATIO
                or observed_parser_analysis_basis
            )
        ):
            transactions = audit_transactions
            source_inconsistent_observed_basis = bool(
                audit_candidate.get("observed_transactions_only") is True
                and audit_candidate.get("source_accounting_inconsistency") is True
                and audit_candidate.get("financial_authority") is not True
            )

            unverified_analysis_context = {
                "analysis_allowed_unverified": True,
                "analysis_withheld": False,
                # Override only the DISPLAY/analysis kill switch when the
                # accepted basis is explicitly the parser's own observed rows.
                # The source inconsistency flags and financial_authority=False
                # remain intact.
                "analysis_blocked": False,
                "source_inconsistent_observed_analysis": (
                    source_inconsistent_observed_basis
                ),
                "analysis_basis": (
                    "extracted_transactions_only"
                    if (
                        source_inconsistent_observed_basis
                        or observed_parser_analysis_basis
                    )
                    else "audit_candidate"
                ),
                "strong_warning_required": bool(
                    source_inconsistent_observed_basis
                    or observed_parser_analysis_basis
                ),
                "materiality_policy": "max_direction_gap_ratio",
                "materiality_threshold": IMMATERIAL_UNRECONCILED_RATIO,
                "max_direction_gap_ratio": max_gap_ratio,
                "income_gap": audit_candidate.get("income_gap"),
                "expense_gap": audit_candidate.get("expense_gap"),
                "official_income": audit_candidate.get("official_income"),
                "official_expense": audit_candidate.get("official_expense"),
                "audit_parser": audit_candidate.get("parser"),
                "audit_transaction_count": len(audit_transactions),
            }
            print("UNVERIFIED_ANALYSIS_AUDIT_CANDIDATE_ACCEPTED", unverified_analysis_context)
        else:
            unverified_analysis_context = {
                "analysis_allowed_unverified": False,
                "analysis_withheld": True,
                "materiality_policy": "max_direction_gap_ratio",
                "materiality_threshold": IMMATERIAL_UNRECONCILED_RATIO,
                "max_direction_gap_ratio": max_gap_ratio,
                "income_gap": audit_candidate.get("income_gap"),
                "expense_gap": audit_candidate.get("expense_gap"),
                "official_income": audit_candidate.get("official_income"),
                "official_expense": audit_candidate.get("official_expense"),
                "audit_parser": audit_candidate.get("parser"),
                "audit_transaction_count": len(audit_transactions),
            }
            print("UNVERIFIED_ANALYSIS_AUDIT_CANDIDATE_WITHHELD", unverified_analysis_context)

    if not transactions:
        extraction_details = dict(extraction_status.get("details") or {})

        # ADDITIVE v16 — preserve common currency detection in recognized but
        # unreconciled/withheld responses. This does not change parser routing,
        # candidate selection, reconciliation, or financial authority.
        withheld_currency = detect_currency(text)
        if not withheld_currency:
            withheld_currency = "UNKNOWN"

        # ADDITIVE status projection only. Parser selection and transaction
        # extraction remain untouched. A structurally recognized statement that
        # fails accounting reconciliation must not be mislabeled as unsupported.
        if extraction_status.get("recognized") is True:
            return {
                "status": "recognized_but_unreconciled",
                "analysis_status": "recognized_but_unreconciled",
                "reason": extraction_status.get("reason") or "accounting_not_reconciled",
                "recognized": True,
                "financial_authority": False,
                "currency": withheld_currency,
                "currency_detected": withheld_currency,
                "transactions": [],
                "summary": {},
                "totals": {
                    "income": 0,
                    "expenses": 0,
                },
                "verification": {
                    "status": "unverified",
                    "recognized": True,
                    "financial_authority": False,
                    "accounting_reconciled": False,
                    "ledger_reconciled": False,
                    "ledger_status": "not_reconciled",
                    "reconciliation_status": extraction_details.get("reconciliation_status") or extraction_status.get("status"),
                    "source_consistency_available": bool(
                        extraction_details.get("source_accounting_inconsistency") is True
                        or extraction_details.get("source_inconsistency_detected") is True
                    ),
                    "source_consistent": (
                        False
                        if (
                            extraction_details.get("source_accounting_inconsistency") is True
                            or extraction_details.get("source_inconsistency_detected") is True
                        )
                        else None
                    ),
                    "source_inconsistency_detected": bool(
                        extraction_details.get("source_accounting_inconsistency") is True
                        or extraction_details.get("source_inconsistency_detected") is True
                    ),
                    "analysis_available": False,
                    "analysis_available_unverified": False,
                    "analysis_withheld": bool(
                        extraction_details.get("analysis_withheld") is True
                        or extraction_details.get("analysis_blocked") is True
                    ),
                    "transaction_count": 0,
                    "extracted_transaction_count": int(
                        extraction_details.get("visible_transaction_count") or 0
                    ),
                    "excluded_transaction_count": 0,
                    "currency": withheld_currency,
                    "confidence": 0,
                    "checks": {
                        "statement_recognized": True,
                        "financial_authority": False,
                        "transactions_extracted": int(
                            extraction_details.get("visible_transaction_count") or 0
                        ) > 0,
                        "currency_detected": bool(
                            withheld_currency and withheld_currency != "UNKNOWN"
                        ),
                        "accounting_reconciled": False,
                        "ledger_reconciled": False,
                        "source_consistent": (
                            False
                            if (
                                extraction_details.get("source_accounting_inconsistency") is True
                                or extraction_details.get("source_inconsistency_detected") is True
                            )
                            else None
                        ),
                    },
                    "evidence": {
                        "income_gap": extraction_details.get("income_gap"),
                        "expense_gap": extraction_details.get("expense_gap"),
                        "debit_gap": extraction_details.get("debit_gap"),
                        "credit_gap": extraction_details.get("credit_gap"),
                        "balance_gap": extraction_details.get("balance_gap"),
                        "parser": extraction_details.get("parser"),
                        "parser_family": extraction_details.get("parser_family"),
                        "opening_balance": extraction_details.get("opening_balance"),
                        "closing_balance": extraction_details.get("closing_balance"),
                        "official_debit_total": extraction_details.get("official_debit_total"),
                        "official_movement_credit_total": extraction_details.get("official_movement_credit_total"),
                        "visible_debit_total": extraction_details.get("visible_debit_total"),
                        "visible_credit_total": extraction_details.get("visible_credit_total"),
                        "source_accounting_inconsistency": extraction_details.get("source_accounting_inconsistency") is True,
                    },
                },
            }

        return {
            "status": "unsupported_document",
            "reason": "unsupported_statement_format",
            "transactions": [],
            "summary": {},
            "totals": {
                "income": 0,
                "expenses": 0,
            },
            "verification": {
                "status": "unverified",
                "recognized": False,
                "financial_authority": False,
                "accounting_reconciled": False,
                "reconciliation_status": "unavailable",
                "transaction_count": 0,
                "extracted_transaction_count": 0,
                "excluded_transaction_count": 0,
                "currency": "UNKNOWN",
                "confidence": 0,
                "checks": {
                    "statement_recognized": False,
                    "financial_authority": False,
                    "transactions_extracted": False,
                    "currency_detected": False,
                    "accounting_reconciled": False,
                },
            },
        }
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

    def is_global_non_transaction_amount(tx: dict):
        """
        Detect rows that are not genuine financial movements.

        Important:
        Transactions validated by a trusted parser or by the running-balance
        chain must never be rejected by the generic absurd-amount heuristic.
        """
        import re

        desc = str(tx.get("description") or tx.get("desc") or "")
        upper = desc.upper()

        try:
            amount = abs(float(tx.get("amount") or 0))
        except (TypeError, ValueError):
            amount = 0.0

        # Debug focused on large transactions.
        if amount >= 100_000:
            print(
                "GLOBAL_GUARD_ENTRY_V3",
                {
                    "amount": tx.get("amount"),
                    "type": tx.get("type"),
                    "_balance_locked": tx.get("_balance_locked"),
                    "locked_amount": tx.get("locked_amount"),
                    "_locked_amount": tx.get("_locked_amount"),
                    "balance_authority": tx.get("balance_authority"),
                    "classification_source": tx.get("classification_source"),
                    "parser_family": tx.get("parser_family"),
                    "description": desc[:180],
                    "file": __file__,
                },
            )

        # Transactions structurally validated by an authoritative parser.
        # Balance-delta validation is one authority; an explicit debit/credit
        # column is another.  The generic absurd-amount heuristic must not
        # override either proof.
        is_trusted_locked_transaction = bool(
            (
                tx.get("_balance_locked") is True
                and tx.get("balance_authority") is True
                and tx.get("classification_source") == "balance_delta"
            )
            or (
                tx.get("classification_source") == "explicit_debit_credit_column"
                and tx.get("parser_family") == "reference_description_debit_credit_table"
                and tx.get("type") in {"income", "expense"}
                and tx.get("amount") is not None
                and (
                    tx.get("locked_amount") is not None
                    or tx.get("_locked_amount") is not None
                )
            )
        )

        if is_trusted_locked_transaction:
            if amount >= 100_000:
                print(
                    "GLOBAL_GUARD_BYPASSED_V3",
                    {
                        "amount": tx.get("amount"),
                        "reason": "trusted_locked_or_balance_validated_transaction",
                    },
                )
            return None

        # ADDITIVE v5 — narrow structural proof used ONLY by the final
        # absurd-amount fallback below.
        #
        # Historical trusted authorities above keep their exact priority.
        # Explicit non-transaction guards below (cheque fusion, totals,
        # opening balances, value-date metadata) also keep exact priority.
        is_structurally_reconciled_transaction = bool(
            tx.get("accounting_reconciled") is True
            and tx.get("balance_reconciled") is True
        )

        # Cheque/check number fused with an amount:
        # Example: CHEQUE 458 + 150.00 incorrectly extracted as 458150.00.
        cheque_like = re.search(
            r"\b(CH[EÈ]QUE|CHEQUE|CHECK|CHQ|CHK|شيك|صك)\b",
            upper,
            re.IGNORECASE,
        )

        word_count = len(
            re.findall(
                r"[A-Za-zÀ-ÿ\u0600-\u06FF]+",
                desc,
            )
        )

        desc_has_only_cheque_word = bool(
            cheque_like and word_count <= 2
        )

        if (
            cheque_like
            and amount >= 100_000
            and desc_has_only_cheque_word
        ):
            return "cheque_number_amount_fusion"

        # Statement totals and movement summaries are not transactions.
        if re.search(
            r"(TOTAUX?\s+DES\s+MOUVEMENTS|"
            r"TOTAL\s+MOVEMENTS?|"
            r"TOTAL\s+DEBITS?|"
            r"TOTAL\s+CREDITS?|"
            r"TOTAL\s+DES\s+OP[ÉE]RATIONS|"
            r"TOTAL\s+TRANSACTIONS?|"
            r"MOUVEMENTS\s+DU\s+MOIS|"
            r"مجموع\s+الحركات|"
            r"إجمالي\s+الحركات|"
            r"اجمالي\s+الحركات)",
            upper,
            re.IGNORECASE,
        ):
            return "statement_total_or_summary_row"

        # Opening and brought-forward balances are not movements.
        if re.search(
            r"(\bB/F\b|"
            r"\bBF\b|"
            r"BROUGHT\s+FORWARD|"
            r"BALANCE\s+BROUGHT\s+FORWARD|"
            r"OPENING\s+BALANCE|"
            r"BEGINNING\s+BALANCE|"
            r"SOLDE\s+INITIAL|"
            r"SOLDE\s+D[ÉE]BUT|"
            r"REPORT\s+[ÀA]\s+NOUVEAU|"
            r"رصيد\s+افتتاحي|"
            r"الرصيد\s+الافتتاحي|"
            r"رصيد\s+سابق)",
            upper,
            re.IGNORECASE,
        ):
            return "opening_or_brought_forward_balance"

        # Value-date-only rows are metadata.
        if (
            re.search(
                r"(VALUE\s+DATE|DATE\s+VALEUR|تاريخ\s+القيمة)",
                upper,
                re.IGNORECASE,
            )
            and word_count <= 4
        ):
            return "value_date_metadata_row"

        # A large amount remains valid when the description contains a strong
        # banking transaction signal.
        trusted_transaction_signal = re.search(
            r"(DEPOT|"
            r"D[ÉE]P[ÔO]T|"
            r"DEPOSIT|"
            r"CASH\s+DEPOSIT|"
            r"VERSEMENT|"
            r"VERST|"
            r"EPARGNE|"
            r"[ÉE]PARGNE|"
            r"SAVINGS|"
            r"RETRAIT|"
            r"WITHDRAWAL|"
            r"VIREMENT|"
            r"TRANSFER|"
            r"CHEQUE|"
            r"CH[EÈ]QUE|"
            r"CHECK|"
            r"CHQ|"
            r"PAYMENT|"
            r"PAIEMENT|"
            r"ISLAMIC\s+TAWARUQ|"
            r"TAWARUQ|"
            r"تمويل|"
            r"تورق|"
            r"إيداع|"
            r"ايداع|"
            r"سحب|"
            r"تحويل|"
            r"دفع|"
            r"شيك|"
            r"صك)",
            upper,
            re.IGNORECASE,
        )

        if trusted_transaction_signal:
            return None

        # Broader transaction vocabulary used by the last-resort absurd guard.
        strong_tx_words = re.search(
            r"(CARTE|"
            r"CARD|"
            r"MADA|"
            r"PAYMENT|"
            r"PAIEMENT|"
            r"VIREMENT|"
            r"VIR\s+RECU|"
            r"VIR\s+EMIS|"
            r"TRANSFER|"
            r"PRELEVEMENT|"
            r"PR[ÉE]L[ÈE]VEMENT|"
            r"ATM|"
            r"RETRAIT|"
            r"DAB|"
            r"DEPOSIT|"
            r"DEPOT|"
            r"D[ÉE]P[ÔO]T|"
            r"VERSEMENT|"
            r"VERST|"
            r"EPARGNE|"
            r"[ÉE]PARGNE|"
            r"SAVINGS|"
            r"CASH\s+DEPOSIT|"
            r"SALAIRE|"
            r"SALARY|"
            r"INVOICE|"
            r"FACTURE|"
            r"ISLAMIC\s+TAWARUQ|"
            r"TAWARUQ|"
            r"تمويل|"
            r"تورق|"
            r"رسوم|"
            r"تحويل|"
            r"دفع|"
            r"سحب|"
            r"إيداع|"
            r"ادخار|"
            r"توفير)",
            upper,
            re.IGNORECASE,
        )

        # Last-resort heuristic only for untrusted rows.
        #
        # Additive v5: a transaction already proven by BOTH accounting and
        # balance reconciliation is no longer "untrusted" for this final
        # heuristic. All explicit guards above remain authoritative.
        if (
            amount >= 100_000
            and not strong_tx_words
            and not is_structurally_reconciled_transaction
        ):
            return "absurd_amount_weak_description"

        if (
            amount >= 100_000
            and not strong_tx_words
            and is_structurally_reconciled_transaction
        ):
            print(
                "GLOBAL_GUARD_STRUCTURAL_RECONCILIATION_BYPASS",
                {
                    "amount": tx.get("amount"),
                    "classification_source": tx.get(
                        "classification_source"
                    ),
                    "parser_family": tx.get("parser_family"),
                    "accounting_reconciled": tx.get(
                        "accounting_reconciled"
                    ),
                    "balance_reconciled": tx.get(
                        "balance_reconciled"
                    ),
                    "reason": "final_absurd_amount_fallback_bypassed",
                },
            )

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

        if (
            is_global_non_transaction_statement_row(tx)
            and not (
                tx.get("locked_amount") is not None
                or tx.get("_locked_amount") is not None
                or tx.get("_balance_locked")
            )
        ):
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
            tx.get("type") in {"income", "expense", "transfer"}
            and tx.get("amount") is not None
            and (
                tx.get("locked_amount") is not None
                or tx.get("_locked_amount") is not None
                or tx.get("_balance_locked")
            )
        ):
            kept_transactions.append(tx)
            continue

        # Standard worldwide rule:
        # A structurally locked transaction from a trusted table/section parser
        # must not be removed only because OCR made its description weak.
        if (
            tx.get("_balance_locked")
            or tx.get("locked_amount") is not None
            or tx.get("_locked_amount") is not None
        ):
            kept_transactions.append(tx)
            continue

        # Standard worldwide rule:
        # Structurally locked transactions from trusted parsers must not be
        # removed only because OCR made their description weak.
        if (
            tx.get("type") in {"income", "expense", "transfer"}
            and tx.get("amount") is not None
            and (
                tx.get("locked_amount") is not None
                or tx.get("_locked_amount") is not None
                or tx.get("_balance_locked")
            )
        ):
            kept_transactions.append(tx)
            continue

        if abs(float(tx.get("amount") or 0)) == 303.0:
            print("MIN_DESC_303_AUDIT", {
                "amount": tx.get("amount"),
                "type": tx.get("type"),
                "locked_amount": tx.get("locked_amount"),
                "_locked_amount": tx.get("_locked_amount"),
                "_balance_locked": tx.get("_balance_locked"),
                "parser_family": tx.get("parser_family"),
                "desc": str(tx.get("description") or tx.get("desc") or "")[:160],
            })

        if abs(float(tx.get("amount") or 0)) == 303.0:
            print("TX_303_FULL_OBJECT", tx)

        if amount > 0 and not description_has_min_signal(tx):
            # Standard worldwide rule:
            # A structurally locked transaction from a trusted table parser
            # must not be removed only because OCR made its description weak.
            if (
                tx.get("_balance_locked")
                or tx.get("locked_amount") is not None
                or tx.get("_locked_amount") is not None
            ):
                kept_transactions.append(tx)
                continue

            if (
                tx.get("locked_amount") is not None
                or tx.get("_locked_amount") is not None
                or tx.get("_balance_locked")
            ):
                kept_transactions.append(tx)
                continue

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

    # ------------------------------------------------------------------
    # ADDITIVE QUALITY CONTRACT v5 — reliability != analysis depth
    # ------------------------------------------------------------------
    #
    # Historical assess_analysis_quality() intentionally treats fewer than five
    # transactions as insufficient_data. That is useful for trend/statistical
    # depth, but it must not imply that extraction is unreliable when the
    # extraction layer has already proved the ledger against statement-level
    # accounting observations.
    #
    # This branch is parser/bank/country/language/currency neutral. It activates
    # only when ALL of the following are true:
    #   - at least one transaction exists;
    #   - every transaction is structurally valid and typed;
    #   - the extraction status says recognized + financial_authority;
    #   - the selected candidate is explicitly reconciled.
    #
    # We therefore keep the extraction as verified while separately marking the
    # analytical scope as limited because the sample is small.
    extraction_status = get_finance_extraction_status()
    extraction_details = dict(
        extraction_status.get("details") or {}
    )
    if unverified_analysis_context:
        extraction_details.update(unverified_analysis_context)
        extraction_status = {
            **extraction_status,
            "details": extraction_details,
        }

    # ADDITIVE v18 — small-statement quality must consume the SAME financial
    # authority contract already accepted by build_frontend_verification().
    #
    # A selected ledger may keep reconciliation_status="internally_supported"
    # while the extractor promotes it to financial_authority only after strict
    # accounting + running-balance reconciliation.  Treat that proof as
    # reconciled for analysis-quality availability, without changing parser
    # routing, candidate ranking, transaction direction, or accounting state.
    reconciliation_status_for_quality = str(
        extraction_details.get("reconciliation_status") or ""
    ).strip().lower()

    authority_basis_for_quality = str(
        extraction_details.get("authority_basis") or ""
    ).strip().lower()

    internally_reconciled_for_quality = bool(
        reconciliation_status_for_quality == "internally_supported"
        and authority_basis_for_quality
        == "internal_accounting_and_balance_reconciliation"
    )

    extraction_reconciled = bool(
        extraction_status.get("recognized") is True
        and extraction_status.get("financial_authority") is True
        and str(
            extraction_status.get("status") or ""
        ).strip().lower() == "reconciled"
        and (
            reconciliation_status_for_quality == "reconciled"
            or internally_reconciled_for_quality
        )
    )

    structurally_complete_sample = bool(
        quality.get("transaction_count", 0) > 0
        and quality.get("valid_transaction_count")
            == quality.get("transaction_count")
        and float(quality.get("structure_ratio") or 0) >= 0.95
        and float(quality.get("typed_ratio") or 0) >= 0.95
    )

    analysis_scope_limited = bool(
        extraction_reconciled
        and structurally_complete_sample
        and int(quality.get("transaction_count") or 0) < 5
    )

    if (
        quality.get("status") == "insufficient_data"
        and analysis_scope_limited
    ):
        quality = {
            **quality,
            "status": "verified",
            "confidence": 90,
            "extraction_reliable": True,
            "accounting_reconciled": True,
            "analysis_scope": "limited",
            "analysis_scope_reason": "low_transaction_count",
        }

        print(
            "QUALITY_RECONCILED_SHORT_STATEMENT_OVERRIDE",
            {
                "transactions": quality.get("transaction_count"),
                "structure_ratio": quality.get("structure_ratio"),
                "typed_ratio": quality.get("typed_ratio"),
                "extraction_status": extraction_status.get("status"),
                "reconciliation_status": extraction_details.get(
                    "reconciliation_status"
                ),
                "quality_status": quality.get("status"),
                "confidence": quality.get("confidence"),
                "analysis_scope": quality.get("analysis_scope"),
                "reason": quality.get("analysis_scope_reason"),
            },
        )

    # Conservative international FR/EN/AR restoration guard.
    # Never reactivate opening balances, statement totals, metadata, OCR-fused
    # identifiers or internal transfers. Only trusted parser rows excluded by the
    # specific unlocked-balance heuristic may be restored.
    restorable_reasons = {"unlocked_amount_balance_row"}
    for tx in transactions:
        exclusion_reason = tx.get("excluded_reason") or tx.get("exclusion_reason")
        is_trusted_locked_row = bool(
            tx.get("_balance_locked")
            or tx.get("locked_amount") is not None
            or tx.get("_locked_amount") is not None
        )
        if (
            tx.get("excluded_from_financial_kpis")
            and exclusion_reason in restorable_reasons
            and is_trusted_locked_row
            and tx.get("type") in {"income", "expense"}
            and abs(float(tx.get("amount") or 0)) > 0
            and not tx.get("is_internal_transfer")
        ):
            tx["excluded_from_financial_kpis"] = False
            tx["exclude_from_income"] = tx.get("type") != "income"
            tx["exclude_from_expense"] = tx.get("type") != "expense"
            tx["exclude_from_score"] = False
            tx["exclude_from_savings"] = False
            tx["exclude_from_cashflow"] = False
            tx.pop("excluded_reason", None)
            tx.pop("exclusion_reason", None)
            tx["category_hint"] = "restored_trusted_locked_balance_row"

    # International KPI filter:
    # Internal transfers must never affect income, expenses,
    # savings, scores, forecasts or charts.
    def is_locked_real_kpi_row(tx):
        return (
            tx.get("type") in {"income", "expense"}
            and not tx.get("is_internal_transfer")
            and abs(float(tx.get("amount") or 0)) > 0
            and (
                tx.get("locked_amount") is not None
                or tx.get("_locked_amount") is not None
                or tx.get("_balance_locked")
            )
        )

    kpi_transactions = [
        tx
        for tx in transactions
        if (
            is_locked_real_kpi_row(tx)
            or not (
                tx.get("type") == "transfer"
                or tx.get("is_internal_transfer")
                or tx.get("excluded_from_financial_kpis")
            )
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

        has_explicit_debit_credit_authority = bool(
            tx.get("classification_source") == "explicit_debit_credit_column"
            and tx.get("parser_family") == "reference_description_debit_credit_table"
            and tx.get("type") in {"income", "expense"}
            and tx.get("amount") is not None
            and (
                tx.get("locked_amount") is not None
                or tx.get("_locked_amount") is not None
            )
        )

        is_absurd = (
            not has_explicit_debit_credit_authority
            and (
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

    # v20: explicit accounting-ledger / analysis-ledger boundary.
    accounting_transactions = list(kpi_transactions)
    analysis_transactions, analysis_excluded_transactions = build_analysis_ledger(accounting_transactions)
    print("ANALYSIS_LEDGER_SEPARATION_AUDIT", {
        "accounting_transactions": len(accounting_transactions),
        "analysis_transactions": len(analysis_transactions),
        "analysis_excluded_transactions": len(analysis_excluded_transactions),
        "rule": "explicit_structural_neutrality_only",
    })

    audit_tx_stage("TX_STAGE_3_KPI_TRANSACTIONS_CREATED", kpi_transactions)

    print("QUALITY_CHECK")
    print(quality)

    # ------------------------------------------------------------------
    # ADDITIVE POST-SELECTION ACCOUNTING AUTHORITY GUARD v7
    # ------------------------------------------------------------------
    # A parser may already have proven one coherent pair of structural
    # debit/credit totals for every dated transaction.  Downstream audit/KPI
    # reconciliation must not replace that stronger proof with a weaker
    # document-level regex summary.  This helper is deliberately self-disabling:
    # historical behavior is unchanged unless all dated KPI rows carry the same
    # finite local totals, are accounting-reconciled, and the ledger matches them
    # exactly within 0.02.  No transaction, parser choice, or router state is
    # modified here.
    def _validated_candidate_local_kpi_totals(rows):
        dated = [
            tx for tx in (rows or [])
            if isinstance(tx, dict) and tx.get("date")
        ]

        if not dated:
            return None

        debit_values = set()
        credit_values = set()

        for tx in dated:
            if tx.get("accounting_reconciled") is not True:
                return None

            try:
                debit = float(tx.get("_official_debit_total"))
                credit = float(tx.get("_official_credit_total"))
            except (TypeError, ValueError, OverflowError):
                return None

            if debit != debit or credit != credit:
                return None
            if abs(debit) == float("inf") or abs(credit) == float("inf"):
                return None

            debit_values.add(round(abs(debit), 2))
            credit_values.add(round(abs(credit), 2))

        if len(debit_values) != 1 or len(credit_values) != 1:
            return None

        official_debit = next(iter(debit_values))
        official_credit = next(iter(credit_values))

        ledger_debit = round(
            sum(
                abs(float(tx.get("amount") or 0))
                for tx in dated
                if tx.get("type") == "expense"
                and not tx.get("excluded_from_financial_kpis")
            ),
            2,
        )
        ledger_credit = round(
            sum(
                abs(float(tx.get("amount") or 0))
                for tx in dated
                if tx.get("type") == "income"
                and not tx.get("excluded_from_financial_kpis")
            ),
            2,
        )

        if (
            abs(ledger_debit - official_debit) > 0.02
            or abs(ledger_credit - official_credit) > 0.02
        ):
            return None

        summary = {
            "deposits": official_credit,
            "withdrawals": official_debit,
            "source": "candidate_local_structural_totals",
        }

        # ADDITIVE v19 — propagate the parser's already-observed four-role
        # statement evidence when it is complete and identical across every
        # dated transaction. This is structural/accounting evidence only.
        # No bank, country, currency, merchant, label, router, candidate rank,
        # or transaction direction is involved.
        opening_values = set()
        closing_values = set()

        for tx in dated:
            try:
                opening_value = float(
                    tx.get("_statement_opening_balance")
                )
                closing_value = float(
                    tx.get("_statement_closing_balance")
                )
            except (TypeError, ValueError, OverflowError):
                opening_values.clear()
                closing_values.clear()
                break

            if (
                opening_value != opening_value
                or closing_value != closing_value
                or abs(opening_value) == float("inf")
                or abs(closing_value) == float("inf")
            ):
                opening_values.clear()
                closing_values.clear()
                break

            opening_values.add(round(opening_value, 2))
            closing_values.add(round(closing_value, 2))

        if len(opening_values) == 1 and len(closing_values) == 1:
            summary["opening_balance"] = next(iter(opening_values))
            summary["ending_balance"] = next(iter(closing_values))
            summary["source"] = (
                "candidate_local_structural_four_role_summary"
            )

        return summary

    # Global FR/EN/AR statement-vs-ledger reconciliation audit.
    # Audit only: never mutates KPI transactions, never creates synthetic rows.
    try:
        statement_summary = extract_global_statement_summary(text)
    except Exception:
        statement_summary = {}

    # ADDITIVE v29 — when the generic summary contains opening/closing balances
    # but omits movement totals, recover only a strict two-value TOTAL row from
    # the same Date | Debit/Withdrawal | Credit/Deposit | Balance table.
    statement_summary = enrich_source_summary_from_transaction_table_totals(
        text,
        statement_summary,
    )

    # Phase 1B: preserve the source statement's own four-role accounting identity
    # before candidate-local totals become the ledger reconciliation authority.
    # Audit only: no parser, router, candidate or transaction mutation.
    source_statement_consistency = assess_source_statement_consistency(
        statement_summary
    )
    print(
        "SOURCE_STATEMENT_CONSISTENCY_AUDIT",
        source_statement_consistency,
    )

    source_balance_diagnostic = collect_explicit_source_balance_diagnostic(
        extraction_status,
        transactions,
    )
    print(
        "SOURCE_BALANCE_DIAGNOSTIC_AUDIT",
        source_balance_diagnostic,
    )

    source_period_diagnostic = collect_explicit_statement_period_diagnostic(
        text,
        transactions,
    )
    print(
        "SOURCE_PERIOD_DIAGNOSTIC_AUDIT",
        source_period_diagnostic,
    )

    source_section_total_diagnostic = (
        collect_source_section_total_contradiction(text)
    )
    print(
        "SOURCE_SECTION_TOTAL_CONTRADICTION_AUDIT",
        source_section_total_diagnostic,
    )

    candidate_local_summary = _validated_candidate_local_kpi_totals(
        kpi_transactions
    )
    if candidate_local_summary is not None:
        # ADDITIVE v19 — source consistency may be established from the
        # parser-produced structural four-role summary only if the generic
        # source audit had no complete four-role evidence. Existing source
        # consistency/inconsistency always stays authoritative.
        if source_statement_consistency.get("available") is not True:
            candidate_source_consistency = (
                assess_source_statement_consistency(
                    candidate_local_summary
                )
            )

            if candidate_source_consistency.get("available") is True:
                source_statement_consistency = (
                    candidate_source_consistency
                )
                print(
                    "SOURCE_STATEMENT_CONSISTENCY_FROM_STRUCTURAL_SUMMARY",
                    source_statement_consistency,
                )

        statement_summary = candidate_local_summary
        print(
            "STATEMENT_RECONCILIATION_AUTHORITY",
            {
                "source": candidate_local_summary.get("source"),
                "deposits": candidate_local_summary.get("deposits"),
                "withdrawals": candidate_local_summary.get("withdrawals"),
                "opening_balance": candidate_local_summary.get(
                    "opening_balance"
                ),
                "ending_balance": candidate_local_summary.get(
                    "ending_balance"
                ),
                "reason": "exact_reconciled_selected_ledger",
            },
        )

    if statement_summary:
        statement_deposits = statement_summary.get("deposits")
        statement_withdrawals = statement_summary.get("withdrawals")

        # Additive guard for an internally-supported, non-authoritative ledger:
        # a single movement component with no opening/ending balance is not
        # enough to become statement-level reconciliation authority.
        incomplete_one_sided_source_summary = bool(
            candidate_local_summary is None
            and extraction_status.get("recognized") is True
            and extraction_status.get("financial_authority") is not True
            and str(
                extraction_details.get("reconciliation_status") or ""
            ).strip().lower() == "internally_supported"
            and source_statement_consistency.get("available") is not True
            and (
                (statement_deposits is not None)
                ^ (statement_withdrawals is not None)
            )
            and source_statement_consistency.get("opening_balance") is None
            and source_statement_consistency.get("ending_balance") is None
        )

        if incomplete_one_sided_source_summary:
            print(
                "INCOMPLETE_SOURCE_MOVEMENT_SUMMARY_NOT_AUTHORITATIVE",
                {
                    "source": statement_summary.get("source"),
                    "deposits": statement_deposits,
                    "withdrawals": statement_withdrawals,
                    "reconciliation_status": extraction_details.get(
                        "reconciliation_status"
                    ),
                    "financial_authority": extraction_status.get(
                        "financial_authority"
                    ),
                },
            )
            statement_deposits = None
            statement_withdrawals = None

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

        def _money_to_float(value):
            import re

            if value is None:
                return None

            s = str(value).strip()

            # Production-safe guard:
            # finance summaries may return "", "$", "+", "-", or OCR-empty values.
            # These must never crash the worker.
            if s in {"", "$", "+", "-", "+$", "-$"}:
                return 0.0

            s = re.sub(r"^([+-])\\s+", r"\\1", s)
            s = (
                s.replace("$", "")
                 .replace("€", "")
                 .replace("£", "")
                 .replace(",", "")
                 .replace(" ", "")
                 .strip()
            )

            if s in {"", "+", "-"}:
                return 0.0

            try:
                return float(s)
            except (TypeError, ValueError):
                return 0.0

        statement_deposits_float = _money_to_float(statement_deposits)
        statement_withdrawals_float = _money_to_float(statement_withdrawals)

        if statement_deposits_float is not None:
            print("STATEMENT_INCOME_RECONCILIATION", {
                "statement": round(abs(statement_deposits_float), 2),
                "ledger": ledger_income,
                "gap": round(abs(statement_deposits_float) - ledger_income, 2),
            })

        if statement_withdrawals_float is not None:
            print("STATEMENT_EXPENSE_RECONCILIATION", {
                "statement": round(abs(statement_withdrawals_float), 2),
                "ledger": ledger_expense,
                "gap": round(abs(statement_withdrawals_float) - ledger_expense, 2),
            })

        income_gap = None
        expense_gap = None

        if statement_deposits_float is not None:
            income_gap = abs(round(abs(statement_deposits_float) - ledger_income, 2))

        if statement_withdrawals_float is not None:
            expense_gap = abs(round(abs(statement_withdrawals_float) - ledger_expense, 2))

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
    elif analysis_scope_limited:
        reconciliation_warnings.append(
            "LIMITED_ANALYSIS_SCOPE_LOW_TRANSACTION_COUNT"
        )

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
            "verification": build_frontend_verification(
                extraction_status=extraction_status,
                quality=quality,
                transactions=transactions,
                kpi_transactions=kpi_transactions,
                currency=None,
                output_language=output_language,
                source_statement_consistency=source_statement_consistency,
                source_balance_diagnostic=source_balance_diagnostic,
            ),
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
        kpi_transactions
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
        statement_text=text,
    )

    # Keep downstream UI/report fields consistent with the resolved value.
    result_ai["currency_detected"] = currency

    update_job_progress(
        job,
        db,
        52,
        finance_progress_message("subscriptions", output_language),
    )

    subscriptions = detect_recurring_subscriptions(kpi_transactions)

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

        if (
            is_metadata
            and not (
                tx.get("locked_amount") is not None
                or tx.get("_locked_amount") is not None
                or tx.get("_balance_locked")
            )
        ):
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

    # ADDITIVE v19 — preserve the pre-guard ledger so a KPI-only filter can
    # never silently destroy an exact statement-level reconciliation.
    #
    # This is not a parser/routing change.  It is a downstream invariant:
    # if the selected ledger already exactly matches independently observed
    # statement totals, a heuristic KPI exclusion is allowed only when the
    # filtered ledger still preserves those same totals.
    balance_noop_guard_input = list(kpi_transactions)

    def _kpi_totals_for_guard(rows):
        income = round(
            sum(
                float(tx.get("amount", 0) or 0)
                for tx in rows
                if tx.get("type") == "income"
            ),
            2,
        )
        expense = round(
            sum(
                abs(float(tx.get("amount", 0) or 0))
                for tx in rows
                if tx.get("type") == "expense"
            ),
            2,
        )
        return income, expense

    guard_official_income = None
    guard_official_expense = None

    if isinstance(statement_summary, dict):
        try:
            if statement_summary.get("deposits") is not None:
                guard_official_income = round(
                    float(statement_summary.get("deposits")),
                    2,
                )
        except (TypeError, ValueError, OverflowError):
            guard_official_income = None

        try:
            if statement_summary.get("withdrawals") is not None:
                guard_official_expense = round(
                    float(statement_summary.get("withdrawals")),
                    2,
                )
        except (TypeError, ValueError, OverflowError):
            guard_official_expense = None

    guard_input_income, guard_input_expense = _kpi_totals_for_guard(
        balance_noop_guard_input
    )

    # Global balance-chain no-op guard.
    #
    # Historical behavior:
    # exclude a repeated-balance expense row because it may be an informational
    # fee/detail row that does not affect the account balance.
    #
    # Additive structural branch:
    # some statements print one running/closing balance for a consecutive group
    # of real movements. Before excluding repeated-balance rows, reconcile the
    # complete group against the previous distinct balance:
    #
    #     previous_balance + sum(group signed movements) == group_balance
    #
    # When exact, every row in that group is a genuine accounting movement and
    # must remain in KPI. When the proof is absent, preserve the historical
    # row-by-row exclusion behavior unchanged.
    no_op_excluded = []
    no_op_kept = []
    reconciled_repeated_balance_groups = []

    def _kpi_balance_value(tx: dict):
        raw_value = tx.get("balance")
        if raw_value is None:
            raw_value = tx.get("_balance")

        try:
            return (
                round(float(raw_value), 2)
                if raw_value is not None
                else None
            )
        except (TypeError, ValueError, OverflowError):
            return None

    def _kpi_signed_value(tx: dict) -> float:
        raw_value = tx.get("signed_amount")
        if raw_value is None:
            raw_value = tx.get("amount")

        try:
            return round(float(raw_value or 0), 2)
        except (TypeError, ValueError, OverflowError):
            return 0.0

    # Build consecutive balance groups without reordering transactions.
    balance_groups = []
    current_group = []
    current_balance = None

    for tx in kpi_transactions:
        balance = _kpi_balance_value(tx)

        # Rows without a balance cannot prove or disprove a balance transition.
        # Keep each such row outside repeated-balance grouping.
        if balance is None:
            if current_group:
                balance_groups.append(
                    {
                        "balance": current_balance,
                        "transactions": current_group,
                    }
                )
                current_group = []
                current_balance = None

            balance_groups.append(
                {
                    "balance": None,
                    "transactions": [tx],
                }
            )
            continue

        if current_group and balance != current_balance:
            balance_groups.append(
                {
                    "balance": current_balance,
                    "transactions": current_group,
                }
            )
            current_group = []

        current_balance = balance
        current_group.append(tx)

    if current_group:
        balance_groups.append(
            {
                "balance": current_balance,
                "transactions": current_group,
            }
        )

    previous_distinct_balance = None

    for group in balance_groups:
        group_balance = group["balance"]
        group_transactions = group["transactions"]

        if group_balance is None:
            no_op_kept.extend(group_transactions)
            continue

        group_signed_total = round(
            sum(
                _kpi_signed_value(tx)
                for tx in group_transactions
            ),
            2,
        )

        group_reconciled = bool(
            len(group_transactions) > 1
            and previous_distinct_balance is not None
            and round(
                previous_distinct_balance
                + group_signed_total
                - group_balance,
                2,
            ) == 0
        )

        if group_reconciled:
            no_op_kept.extend(group_transactions)
            reconciled_repeated_balance_groups.append({
                "previous_balance": previous_distinct_balance,
                "group_balance": group_balance,
                "movement_total": group_signed_total,
                "count": len(group_transactions),
                "dates": [
                    tx.get("date")
                    for tx in group_transactions
                ][:20],
                "amounts": [
                    _kpi_signed_value(tx)
                    for tx in group_transactions
                ][:20],
            })
            previous_distinct_balance = group_balance
            continue

        # Historical fallback, unchanged:
        # keep the first row at a new balance and exclude only later expense
        # rows that repeat that exact balance without group reconciliation.
        local_previous_balance = previous_distinct_balance

        for tx in group_transactions:
            amount = abs(_kpi_signed_value(tx))

            is_no_op_balance_row = (
                tx.get("type") == "expense"
                and amount > 0
                and local_previous_balance is not None
                and round(
                    abs(local_previous_balance - group_balance),
                    2,
                ) == 0
            )

            if is_no_op_balance_row:
                tx["excluded_from_financial_kpis"] = True
                tx["excluded_reason"] = "balance_chain_noop_row"
                no_op_excluded.append({
                    "date": tx.get("date"),
                    "amount": tx.get("amount"),
                    "balance": group_balance,
                    "prev_balance": local_previous_balance,
                    "type": tx.get("type"),
                    "desc": (
                        tx.get("description")
                        or tx.get("desc")
                        or ""
                    )[:160],
                })
                local_previous_balance = group_balance
                continue

            no_op_kept.append(tx)
            local_previous_balance = group_balance

        previous_distinct_balance = group_balance

    if reconciled_repeated_balance_groups:
        print(
            "BALANCE_CHAIN_REPEATED_GROUP_RECONCILED",
            {
                "count": len(reconciled_repeated_balance_groups),
                "samples": reconciled_repeated_balance_groups[:20],
            },
        )

    if no_op_excluded:
        print("BALANCE_CHAIN_NOOP_GUARD", {
            "count": len(no_op_excluded),
            "samples": no_op_excluded[:20],
        })

    kpi_transactions = no_op_kept

    # ADDITIVE v19 — exact-reconciliation preservation.
    #
    # Roll back ONLY this KPI heuristic when:
    #   1) the statement exposes complete official credit/debit totals;
    #   2) the pre-guard selected ledger matches both totals exactly;
    #   3) the no-op heuristic would make either side stop matching.
    #
    # This is international/accounting-only evidence.  It does not inspect
    # bank name, country, currency, merchant, or language.
    guard_output_income, guard_output_expense = _kpi_totals_for_guard(
        kpi_transactions
    )

    guard_has_complete_official_totals = bool(
        guard_official_income is not None
        and guard_official_expense is not None
    )

    guard_input_exact = bool(
        guard_has_complete_official_totals
        and abs(
            guard_input_income - guard_official_income
        ) <= 0.02
        and abs(
            guard_input_expense - guard_official_expense
        ) <= 0.02
    )

    guard_output_exact = bool(
        guard_has_complete_official_totals
        and abs(
            guard_output_income - guard_official_income
        ) <= 0.02
        and abs(
            guard_output_expense - guard_official_expense
        ) <= 0.02
    )

    if (
        no_op_excluded
        and guard_input_exact
        and not guard_output_exact
    ):
        for tx in no_op_excluded:
            pass

        # Clear only exclusions created by this guard in this pass.
        for tx in balance_noop_guard_input:
            if tx.get("excluded_reason") == "balance_chain_noop_row":
                tx.pop("excluded_from_financial_kpis", None)
                tx.pop("excluded_reason", None)

        kpi_transactions = balance_noop_guard_input

        print(
            "BALANCE_CHAIN_NOOP_GUARD_ROLLBACK",
            {
                "reason": "would_break_exact_statement_reconciliation",
                "official_income": guard_official_income,
                "official_expense": guard_official_expense,
                "input_income": guard_input_income,
                "input_expense": guard_input_expense,
                "filtered_income": guard_output_income,
                "filtered_expense": guard_output_expense,
                "restored_transactions": len(
                    balance_noop_guard_input
                ),
                "heuristic_exclusions_reverted": len(
                    no_op_excluded
                ),
            },
        )

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
            if v is None:
                return None

            try:
                cleaned = (
                    str(v)
                    .replace(",", "")
                    .replace("£", "")
                    .replace("$", "")
                    .replace("€", "")
                    .strip()
                )
            except Exception:
                return None

            if cleaned in {"", "+", "-"}:
                return None

            try:
                return round(float(cleaned), 2)
            except (TypeError, ValueError, OverflowError):
                return None

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

            # ------------------------------------------------------------
            # ADDITIVE STANDARD KPI AUTHORITY GUARD
            #
            # The final selected ledger is the primary KPI source. A secondary
            # regex summary may validate it, but must not replace it when the
            # ledger already reconciles exactly with the structural statement
            # summary produced by the extractor.
            #
            # Historical fallback behavior remains available only when the
            # selected ledger is not already reconciled.
            # ------------------------------------------------------------
            authoritative_summary = {}
            try:
                authoritative_summary = (
                    extract_global_statement_summary(raw_text_for_summary)
                    or {}
                )
            except Exception:
                authoritative_summary = {}

            candidate_local_summary = _validated_candidate_local_kpi_totals(
                kpi_transactions
            )

            if candidate_local_summary is not None:
                authoritative_income = candidate_local_summary.get("deposits")
                authoritative_expense = candidate_local_summary.get("withdrawals")
                print(
                    "SUMMARY_RECONCILIATION_AUTHORITY",
                    {
                        "source": "candidate_local_structural_totals",
                        "income": authoritative_income,
                        "expense": authoritative_expense,
                        "reason": "exact_reconciled_selected_ledger",
                    },
                )
            else:
                authoritative_income = _money_to_float(
                    authoritative_summary.get("deposits")
                )
                authoritative_expense = _money_to_float(
                    authoritative_summary.get("withdrawals")
                )

            authoritative_income_gap = (
                None
                if authoritative_income is None
                else round(
                    abs(authoritative_income) - parsed_income,
                    2,
                )
            )
            authoritative_expense_gap = (
                None
                if authoritative_expense is None
                else round(
                    abs(authoritative_expense) - parsed_expense,
                    2,
                )
            )

            ledger_already_reconciled = bool(
                authoritative_income is not None
                and authoritative_expense is not None
                and abs(authoritative_income_gap or 0.0) <= 0.01
                and abs(authoritative_expense_gap or 0.0) <= 0.01
            )

            if ledger_already_reconciled:
                print(
                    "SUMMARY_RECONCILIATION_SKIPPED",
                    {
                        "reason": "final_ledger_already_reconciled",
                        "authoritative_income": authoritative_income,
                        "authoritative_expense": authoritative_expense,
                        "parsed_income": parsed_income,
                        "parsed_expense": parsed_expense,
                        "secondary_income": official_income,
                        "secondary_expense": official_expense,
                    },
                )

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
                not ledger_already_reconciled
                and len(kpi_transactions) > 0
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

    # KPI audit must reflect the final ledger unless a validated official-summary
    # reconciliation was intentionally selected. Do not silently overwrite that
    # aggregate-only reconciliation here.
    if not result_ai.get("summary_reconciliation_used"):
        income_total = round(
            sum(abs(float(tx.get("amount") or 0)) for tx in kpi_transactions if tx.get("type") == "income"),
            2,
        )
        expense_total = round(
            sum(abs(float(tx.get("amount") or 0)) for tx in kpi_transactions if tx.get("type") == "expense"),
            2,
        )

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


    # ------------------------------------------------------------------
    # v21 — AUTHORITATIVE ANALYSIS LEDGER BOUNDARY
    # ------------------------------------------------------------------
    # Rebuild from the FINAL reconciled accounting/KPI ledger, after all
    # structural metadata/no-op guards have completed.  From this point on,
    # behavioral engines MUST consume analysis_transactions only.  The
    # reconciled accounting ledger remains untouched and continues to back
    # reconciliation / statement-source verification.
    accounting_transactions = list(kpi_transactions)
    analysis_transactions, analysis_excluded_transactions = build_analysis_ledger(
        accounting_transactions
    )

    analysis_observed_income = observed_income_from_transactions(analysis_transactions)
    analysis_fallback_income = (
        None if analysis_observed_income > 0 else fallback_income
    )

    subscriptions = detect_recurring_subscriptions(analysis_transactions)
    savings_opportunities = detect_savings_opportunities(
        transactions=analysis_transactions,
        subscriptions=subscriptions,
    )
    budget = build_recommended_budget(
        transactions=analysis_transactions,
        fallback_income=analysis_fallback_income,
        output_language=output_language,
    )
    scores = calculate_financial_scores(
        transactions=analysis_transactions,
        subscriptions=subscriptions,
        fallback_income=analysis_fallback_income,
    )
    forecast = predict_cashflow(
        transactions=analysis_transactions,
        fallback_income=analysis_fallback_income,
        output_language=output_language,
    )

    print(
        "ANALYSIS_LEDGER_AUTHORITATIVE",
        {
            "accounting_transactions": len(accounting_transactions),
            "analysis_transactions": len(analysis_transactions),
            "analysis_excluded_transactions": len(analysis_excluded_transactions),
            "observed_income": forecast.get("observed_income"),
            "observed_expenses": forecast.get("observed_expenses"),
            "observed_net_cashflow": forecast.get("observed_net_cashflow"),
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
        transactions=analysis_transactions,
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
        transactions=analysis_transactions,
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

    charts = build_financial_charts(analysis_transactions)

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

    # A perfectly reconciled one/few-transaction statement is reliable evidence,
    # but not enough evidence for behavioral scoring, recurring-pattern claims,
    # budget prescriptions, savings opportunities or trend forecasts.
    #
    # Keep observed transactions/totals/charts. Suppress only conclusions that
    # require a broader sample.
    if analysis_scope_limited:
        limited_scope_messages = {
            "en": (
                "The extracted transactions reconcile with the statement, "
                "but this statement contains too few transactions for reliable "
                "behavioral trends, subscription detection, scoring, budgeting "
                "or savings recommendations."
            ),
            "fr": (
                "Les transactions extraites se réconcilient avec le relevé, "
                "mais celui-ci contient trop peu d’opérations pour établir de "
                "façon fiable des tendances de comportement, détecter des "
                "abonnements, calculer un score, recommander un budget ou "
                "proposer des économies."
            ),
            "ar": (
                "تتطابق المعاملات المستخرجة محاسبياً مع كشف الحساب، "
                "لكن عدد العمليات قليل جداً لاستخلاص اتجاهات سلوكية موثوقة "
                "أو كشف الاشتراكات أو احتساب درجة مالية أو اقتراح ميزانية "
                "أو فرص ادخار."
            ),
        }

        result_ai["analysis_scope"] = "limited"
        result_ai["analysis_scope_reason"] = "low_transaction_count"
        result_ai["analysis_scope_message"] = limited_scope_messages.get(
            output_language,
            limited_scope_messages["en"],
        )

        # Preserve the observed accounting facts.
        limited_forecast = {
            "status": "limited_scope",
            "observed_income": round(income_total, 2),
            "observed_expenses": round(expense_total, 2),
            "observed_net_cashflow": round(
                income_total - expense_total,
                2,
            ),
            "trend": None,
            "days_before_risk": None,
        }

        result_ai["financial_score"] = None
        result_ai["saving_strategies"] = []
        result_ai["waste_detected"] = []
        result_ai["risk_notes"] = []

        subscriptions = []
        savings_opportunities = []
        budget = {
            "status": "limited_scope",
            "available": False,
        }
        forecast = limited_forecast
        scores = {
            "status": "limited_scope",
            "overall_financial_habits_score": None,
        }
        alerts = []
        insights = []

        # Rebuild only the factual observed summary from the reconciled ledger.
        result_ai["summary"] = build_observed_finance_summary(
            forecast=forecast,
            currency=currency,
            output_language=output_language,
        )

        print(
            "LIMITED_ANALYSIS_SCOPE_APPLIED",
            {
                "transactions": len(kpi_transactions),
                "income_total": income_total,
                "expense_total": expense_total,
                "net": round(income_total - expense_total, 2),
                "suppressed": [
                    "financial_score",
                    "subscriptions",
                    "savings_opportunities",
                    "recommended_budget",
                    "behavioral_forecast",
                    "alerts",
                    "financial_insights",
                ],
            },
        )

    result_ai["analysis_status"] = quality["status"]
    result_ai["confidence"] = quality["confidence"]
    result_ai["analysis_quality"] = quality

    verification = build_frontend_verification(
        extraction_status=extraction_status,
        quality=quality,
        transactions=transactions,
        kpi_transactions=kpi_transactions,
        currency=currency,
        output_language=output_language,
        source_statement_consistency=source_statement_consistency,
        source_balance_diagnostic=source_balance_diagnostic,
        source_period_diagnostic=source_period_diagnostic,
        source_section_total_diagnostic=source_section_total_diagnostic,
    )

    print(
        "FRONTEND_VERIFICATION_CONTRACT",
        {
            "status": verification.get("status"),
            "recognized": verification.get("recognized"),
            "financial_authority": verification.get("financial_authority"),
            "accounting_reconciled": verification.get("accounting_reconciled"),
            "source_consistent": verification.get("source_consistent"),
            "source_inconsistency_detected": verification.get("source_inconsistency_detected"),
            "reason": verification.get("reason"),
            "language": verification.get("language"),
            "reconciliation_status": verification.get("reconciliation_status"),
            "transaction_count": verification.get("transaction_count"),
            "excluded_transaction_count": verification.get("excluded_transaction_count"),
            "currency": verification.get("currency"),
            "confidence": verification.get("confidence"),
        },
    )

    # ADDITIVE v23 — frontend ledger contract.
    #
    # The reconciled accounting ledger remains the source of truth for
    # verification and statement reconciliation.  Behavioral amounts, charts,
    # categories, recommendations and transaction drill-downs must all expose
    # the same analysis ledger used by the behavioral engines.
    #
    # This is a projection-only change:
    # - no parser/router/candidate logic changes;
    # - no transaction amount/direction mutation;
    # - no bank/country/currency/merchant rule;
    # - the full accounting evidence remains available separately.
    result = {
        **result_ai,
        "analysis_status": (
            "unverified_analysis_available"
            if verification.get("analysis_available_unverified") is True
            else result_ai.get("analysis_status")
        ),
        "verification": verification,

        # Frontend/behavioral transaction views.
        "transactions": analysis_transactions,

        # Explicit preserved ledgers for audit/debug/export consumers.
        "accounting_transactions": accounting_transactions,
        "analysis_transactions": analysis_transactions,
        "analysis_excluded_transactions": analysis_excluded_transactions,

        "charts": charts,
        "subscriptions_detected": subscriptions,
        "savings_opportunities": savings_opportunities,
        "recommended_budget": budget,
        "cashflow_forecast": forecast,
        "financial_habit_scores": scores,
        "financial_alerts": alerts,
        "financial_insights": insights,
        "ledger_scope": {
            "accounting_transactions": len(accounting_transactions),
            "analysis_transactions": len(analysis_transactions),
            "analysis_excluded_transactions": len(analysis_excluded_transactions),
            "analysis_rule": "explicit_structural_neutrality_only",
            "accounting_ledger_preserved": True,
            "behavioral_engines_use_analysis_ledger": True,
            "frontend_transactions_use_analysis_ledger": True,
        },
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