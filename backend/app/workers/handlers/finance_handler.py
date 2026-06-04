import json
import fitz
from collections import Counter

from app.models.job import Job
from app.models.finance_analysis import FinanceAnalysis

from app.services.finance_agent.statement_parser import extract_statement_text_from_path
from app.services.cloud_storage_service import download_api_file_from_cloud
from app.services.finance_agent.finance_ai_agent import analyze_bank_statement
from app.services.finance_agent.transaction_extractor import (
    debug_log,
    extract_transactions,
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

    if total_count < MIN_TRANSACTIONS or structure_ratio < PARTIAL_STRUCTURE_RATIO:
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

    # Do not deduplicate bank transactions by content.
    # Two real bank operations can have the same date, description and amount.
    # Example: two ATM withdrawals of 2 000 MAD on the same day.
    transactions = list(transactions)

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


    quality = assess_analysis_quality(transactions)

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


    print("QUALITY_CHECK")
    print(quality)

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


    for tx in transactions:
        if tx.get("_locked_amount") is not None:
            tx["amount"] = tx["_locked_amount"]

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


    for tx in transactions:
        if tx.get("_locked_amount") is not None:
            tx["amount"] = tx["_locked_amount"]

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

    for tx in kpi_transactions:
        print(
            "KPI_INPUT_DEBUG",
            {
                "amount": tx.get("amount"),
                "balance": tx.get("balance"),
                "type": tx.get("type")
            }
        )

    print(
        "KPI_AUDIT",
        {
            "raw_transactions": len(transactions),
            "kpi_transactions": len(kpi_transactions),
            "income": forecast.get("observed_income"),
            "expenses": forecast.get("observed_expenses"),
            "net": forecast.get("observed_net_cashflow"),
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
