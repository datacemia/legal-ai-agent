import json
from typing import Any

from app.models.job import Job
from app.models.business_analysis import BusinessAnalysis

from app.services.business_agent.business_ai_agent import analyze_business_data
from app.services.business_agent.business_kpi_detector import (
    detect_business_model,
    detect_business_kpis,
)
from app.services.business_agent.business_charts import build_business_charts
from app.services.business_agent.business_forecasting import forecast_business_performance
from app.services.business_agent.business_memory import attach_business_memory
from app.services.business_agent.business_health_score import apply_backend_health_score
from app.services.business_agent.business_anomaly_detector_v2 import attach_business_anomalies_v2
from app.services.business_agent.business_decision_engine import build_business_decision_layer
from app.services.business_agent.business_i18n_service import translate_business_analysis_payload
from app.services.business_agent.business_currency_service import (
    attach_currency_to_result,
    normalize_money_columns,
)

from app.workers.progress import update_job_progress


def business_progress_message(key: str, language: str) -> str:
    messages = {
        "loading": {
            "en": "Loading business data...",
            "fr": "Chargement des données business...",
            "ar": "جارٍ تحميل بيانات الأعمال...",
        },
        "parsing": {
            "en": "Preparing business data...",
            "fr": "Préparation des données business...",
            "ar": "جارٍ تجهيز بيانات الأعمال...",
        },
        "detecting": {
            "en": "Detecting business model and KPIs...",
            "fr": "Détection du modèle business et des KPI...",
            "ar": "جارٍ تحديد نموذج الأعمال ومؤشرات الأداء...",
        },
        "analyzing": {
            "en": "Running AI business analysis...",
            "fr": "Analyse business par IA en cours...",
            "ar": "جارٍ تشغيل تحليل الأعمال بالذكاء الاصطناعي...",
        },
        "charts": {
            "en": "Building charts and forecast...",
            "fr": "Création des graphiques et prévisions...",
            "ar": "جارٍ إنشاء الرسوم البيانية والتوقعات...",
        },
        "intelligence": {
            "en": "Building decision intelligence...",
            "fr": "Création de l’intelligence décisionnelle...",
            "ar": "جارٍ بناء ذكاء القرار...",
        },
        "localizing": {
            "en": "Localizing business report...",
            "fr": "Localisation du rapport business...",
            "ar": "جارٍ تكييف تقرير الأعمال لغويًا...",
        },
        "saving": {
            "en": "Saving business analysis...",
            "fr": "Enregistrement de l’analyse business...",
            "ar": "جارٍ حفظ تحليل الأعمال...",
        },
        "finalizing": {
            "en": "Finalizing business dashboard...",
            "fr": "Finalisation du tableau de bord business...",
            "ar": "جارٍ إنهاء لوحة تحكم الأعمال...",
        },
    }

    if language not in ["en", "fr", "ar"]:
        language = "en"

    return messages.get(key, {}).get(language, messages.get(key, {}).get("en", key))


def _build_safe_ai_fallback() -> dict[str, Any]:
    return {
        "business_model": "general",
        "confidence_level": "low",
        "executive_summary": "AI analysis returned an invalid response.",
        "business_health_score": None,
        "kpis": {
            "revenue": 0,
            "expenses": 0,
            "profit": 0,
            "profit_margin_percent": 0,
            "growth_rate_percent": 0,
            "cashflow_status": "unknown",
        },
        "advanced_kpis": {},
        "monthly_series": [],
        "smart_insights": {
            "most_important_decision": {
                "title": "Analysis error",
                "decision": "Retry the analysis with a cleaner file.",
                "why": "The AI response was not a valid object.",
                "impact": "low",
                "timeframe": "now",
            },
            "key_insights": [],
        },
        "risks": [],
        "opportunities": [],
        "recommendations": [],
        "charts": [],
        "forecast": {
            "available": False,
            "next_month_revenue": 0,
            "next_quarter_revenue": 0,
            "trend": "unknown",
            "explanation": "Forecast unavailable because the analysis failed.",
        },
        "data_quality": {
            "score": 0,
            "limitations": ["Invalid AI analysis response."],
            "missing_fields": [],
        },
        "disclaimer": (
            "This is for business decision support only. "
            "Verify important decisions with a qualified professional."
        ),
    }


def _force_backend_financial_truth(
    result: dict[str, Any],
    detected_kpis: dict[str, Any],
    business_model: str,
) -> dict[str, Any]:
    core_kpis = detected_kpis.get("core_kpis") or {}
    advanced_kpis = detected_kpis.get("advanced_kpis") or {}
    monthly_series = detected_kpis.get("monthly_series") or []
    data_quality = detected_kpis.get("data_quality") or {}
    model_detection = detected_kpis.get("model_detection") or {}

    result["business_model"] = detected_kpis.get("business_model") or business_model

    if model_detection:
        result["business_model_detection"] = model_detection

        confidence = model_detection.get("confidence")
        if confidence:
            result["confidence_level"] = confidence

    result["kpis"] = core_kpis or result.get("kpis", {})
    result["advanced_kpis"] = advanced_kpis or {}
    result["monthly_series"] = monthly_series or []

    if data_quality:
        result["data_quality"] = data_quality

    result["backend_truth"] = {
        "enabled": True,
        "source": detected_kpis.get("source", "backend_calculated_strict"),
        "rows_count": detected_kpis.get("rows_count", 0),
        "column_mapping": detected_kpis.get("column_mapping", {}),
        "detected_kpi_columns": detected_kpis.get("detected_kpi_columns", {}),
        "suggested_kpis": detected_kpis.get("suggested_kpis", []),
    }

    result["backend_detected_kpis"] = detected_kpis

    return result


def _normalize_parsed_business_data(parsed_data: Any):
    if isinstance(parsed_data, str):
        return {
            "raw_preview": parsed_data,
            "normalized_rows": [],
            "column_mapping": {},
            "columns": [],
            "row_count": 0,
        }

    if not isinstance(parsed_data, dict):
        raise ValueError("Invalid parsed business data.")

    return parsed_data


def handle_business_ai(job: Job, db):
    parsed_data = job.input.get("parsed_data")
    file_name = job.input.get("file_name", "business_file")
    output_language = job.input.get("output_language", "en")
    access_type = job.input.get("access_type")
    credits_used = job.input.get("credits_used", 0)

    if output_language not in ["en", "fr", "ar"]:
        output_language = "en"

    update_job_progress(job, db, 8, business_progress_message("loading", output_language))

    if not parsed_data:
        raise ValueError("Business parsed data is missing from job input")

    update_job_progress(job, db, 15, business_progress_message("parsing", output_language))

    parsed_data = _normalize_parsed_business_data(parsed_data)

    raw_preview = parsed_data.get("raw_preview", "")
    normalized_rows = parsed_data.get("normalized_rows", [])
    normalized_rows = normalize_money_columns(normalized_rows)
    column_mapping = parsed_data.get("column_mapping", {})
    columns = parsed_data.get("columns", [])
    row_count = parsed_data.get("row_count", len(normalized_rows))

    if not raw_preview.strip():
        raise ValueError("Business data preview is empty.")

    update_job_progress(job, db, 28, business_progress_message("detecting", output_language))

    business_model = detect_business_model(columns=columns, rows=normalized_rows)
    detected_kpis = detect_business_kpis(
        business_model=business_model,
        rows=normalized_rows,
        column_mapping=column_mapping,
    )

    update_job_progress(job, db, 42, business_progress_message("analyzing", output_language))

    try:
        result = analyze_business_data(
            business_data=raw_preview,
            backend_kpis=detected_kpis,
            output_language=output_language,
        )
    except TypeError:
        result = analyze_business_data(
            business_data=raw_preview,
            output_language=output_language,
        )
    except Exception as error:
        result = _build_safe_ai_fallback()
        result["data_quality"]["limitations"].append(
            f"AI analysis failed: {str(error)}"
        )

    if not isinstance(result, dict):
        result = _build_safe_ai_fallback()

    result = _force_backend_financial_truth(result, detected_kpis, business_model)

    update_job_progress(job, db, 58, business_progress_message("charts", output_language))

    charts = build_business_charts(rows=normalized_rows, column_mapping=column_mapping)
    forecast = forecast_business_performance(rows=normalized_rows, column_mapping=column_mapping)

    result["charts"] = charts
    result["forecast"] = forecast

    update_job_progress(job, db, 72, business_progress_message("intelligence", output_language))

    result = apply_backend_health_score(result=result, detected_kpis=detected_kpis)
    result = attach_business_anomalies_v2(
        result=result,
        detected_kpis=detected_kpis,
        forecast=forecast,
        strictness="professional",
    )
    result = build_business_decision_layer(result=result, detected_kpis=detected_kpis)

    result["file_metadata"] = {
        "file_name": file_name,
        "rows_count": row_count,
        "columns": columns,
        "column_mapping": column_mapping,
        "output_language": output_language,
    }

    result = attach_business_memory(db=db, user_id=job.user_id, current_result=result)
    result = _force_backend_financial_truth(result, detected_kpis, business_model)
    result = apply_backend_health_score(result=result, detected_kpis=detected_kpis)
    result = attach_business_anomalies_v2(
        result=result,
        detected_kpis=detected_kpis,
        forecast=forecast,
        strictness="professional",
    )
    result = build_business_decision_layer(result=result, detected_kpis=detected_kpis)
    result = attach_currency_to_result(result=result, rows=normalized_rows, default_currency="USD")

    update_job_progress(job, db, 85, business_progress_message("localizing", output_language))

    result = translate_business_analysis_payload(payload=result, language=output_language)

    update_job_progress(job, db, 92, business_progress_message("saving", output_language))

    raw_health_score = result.get("business_health_score")

    health_score_for_db = (
        int(round(raw_health_score))
        if isinstance(raw_health_score, (int, float))
        and not isinstance(raw_health_score, bool)
        else None
    )

    analysis = BusinessAnalysis(
        user_id=job.user_id,
        file_name=file_name,
        result=json.dumps(result, ensure_ascii=False),
        business_model=str(result.get("business_model", "general")),
        business_health_score=health_score_for_db,
        access_type=access_type,
        credits_used=credits_used,
        output_language=output_language,
        rows_count=row_count,
    )

    db.add(analysis)
    db.commit()
    db.refresh(analysis)

    result["analysis_id"] = analysis.id

    update_job_progress(job, db, 96, business_progress_message("finalizing", output_language))

    return result
