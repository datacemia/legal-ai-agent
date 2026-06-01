import json
import fitz
from collections import Counter

from app.models.job import Job
from app.models.finance_analysis import FinanceAnalysis

from app.services.finance_agent.statement_parser import extract_statement_text_from_path
from app.services.cloud_storage_service import download_api_file_from_cloud
from app.services.finance_agent.finance_ai_agent import analyze_bank_statement
from app.services.finance_agent.transaction_extractor import extract_transactions
from app.services.finance_agent.subscription_detector import detect_recurring_subscriptions
from app.services.finance_agent.budget_engine import build_recommended_budget
from app.services.finance_agent.forecasting import predict_cashflow
from app.services.finance_agent.scoring import calculate_financial_scores
from app.services.finance_agent.charts_builder import build_financial_charts
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
        text = ""

        with fitz.open(stream=content, filetype="pdf") as doc:
            for page in doc:
                text += page.get_text()
    else:
        if storage_path:
            file_path = download_api_file_from_cloud(
                storage_path=str(storage_path),
                suffix=".pdf",
            )

        text = extract_statement_text_from_path(str(file_path))

    if not text or not text.strip():
        raise ValueError("Could not extract text from PDF.")

    update_job_progress(
        job,
        db,
        32,
        finance_progress_message("transactions", output_language),
    )

    transactions = extract_transactions(text)

    transactions = deduplicate_transactions(
        transactions
    )

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
        transactions=transactions,
        subscriptions=subscriptions,
    )

    update_job_progress(
        job,
        db,
        64,
        finance_progress_message("budget", output_language),
    )

    budget = build_recommended_budget(
        transactions=transactions,
        fallback_income=effective_fallback_income,
    )

    scores = calculate_financial_scores(
        transactions=transactions,
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
        transactions=transactions,
        fallback_income=effective_fallback_income,
    )
    

    observed_income = forecast.get(
        "observed_income",
        0,
    )

    observed_expenses = forecast.get(
        "observed_expenses",
        0,
    )

    if (
        result_ai.get(
            "total_spending_estimate",
            0,
        ) == 0
        and observed_expenses > 0
    ):
        result_ai["total_spending_estimate"] = round(
            observed_expenses,
            2,
        )

    if (
        result_ai.get(
            "total_income_estimate",
            0,
        ) == 0
        and observed_income > 0
    ):
        result_ai["total_income_estimate"] = round(
            observed_income,
            2,
        )

    if (
        result_ai.get(
            "financial_score",
            0,
        ) == 0
    ):
        result_ai["financial_score"] = scores.get(
            "overall_financial_habits_score",
            0,
        )

    alerts = generate_financial_alerts(
        transactions=transactions,
        subscriptions=subscriptions,
        forecast=forecast,
        scores=scores,
    )

    update_job_progress(
        job,
        db,
        86,
        finance_progress_message("insights", output_language),
    )

    insights = generate_financial_insights(
        transactions=transactions,
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

    charts = build_financial_charts(transactions)

    result_ai["summary"] = build_observed_finance_summary(
        forecast=forecast,
        currency=currency,
        output_language=output_language,
    )

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
