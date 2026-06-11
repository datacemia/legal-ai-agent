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
            "revenue": None,
            "expenses": None,
            "profit": None,
            "profit_margin_percent": None,
            "growth_rate_percent": None,
            "cashflow_status": "unknown",
            "revenue_available": False,
            "expenses_available": False,
            "profit_available": False,
            "growth_available": False,
            "cashflow_available": False,
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
            "next_month_revenue": None,
            "next_quarter_revenue": None,
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


def _has_verified_business_performance_data(
    detected_kpis: dict[str, Any] | None,
) -> bool:
    detected_kpis = detected_kpis or {}

    core_kpis = detected_kpis.get("core_kpis") or {}
    advanced_kpis = detected_kpis.get("advanced_kpis") or {}
    forecast = detected_kpis.get("forecast") or {}

    core_flags = (
        "revenue_available",
        "expenses_available",
        "profit_available",
        "growth_available",
        "cashflow_available",
        "orders_available",
        "customers_available",
    )

    advanced_flags = (
        "churn_available",
        "roas_available",
        "cac_available",
        "aov_available",
        "mrr_available",
        "arr_available",
        "ltv_available",
        "retention_available",
        "conversion_available",
    )

    if any(bool(core_kpis.get(flag)) for flag in core_flags):
        return True

    if any(bool(advanced_kpis.get(flag)) for flag in advanced_flags):
        return True

    if bool(forecast.get("available")):
        return True

    return False


def _unknown_currency() -> dict[str, Any]:
    return {
        "code": None,
        "symbol": None,
        "name": None,
        "locale": None,
        "position": None,
        "detected_from": "none",
        "multi_currency_detected": False,
        "detected_currencies": [],
        "confidence": 0.0,
    }


def _mark_non_performance_dataset(
    result: dict[str, Any],
    output_language: str = "en",
) -> dict[str, Any]:
    messages = {
        "en": {
            "summary": (
                "The uploaded file does not contain enough verified business "
                "performance data to calculate Revenue, growth, Profitability, "
                "cashflow, risks, forecasts, or priority decisions."
            ),
            "decision_title": "Upload performance data before making business decisions",
            "decision": (
                "Upload a file with dated Revenue, orders, Expenses, customers, "
                "cashflow, or advertising spend before using this agent for "
                "executive decisions."
            ),
            "why": (
                "The uploaded file does not contain verified business performance "
                "metrics."
            ),
            "recommendation": (
                "Upload a file with dated Revenue, orders, Expenses, customers, "
                "cashflow, or advertising spend before using this agent for "
                "executive decisions."
            ),
            "recommendation_impact": (
                "Enables verified KPI, risk, forecast, and decision analysis."
            ),
            "insight": (
                "The uploaded file does not contain verified business performance "
                "metrics."
            ),
            "health_reason": (
                "Business health score is unavailable because insufficient "
                "business performance data was provided."
            ),
            "forecast_explanation": (
                "Forecast requires enough dated revenue or business performance data."
            ),
        },
        "fr": {
            "summary": (
                "Le fichier importé ne contient pas suffisamment de données de "
                "performance business vérifiées pour calculer le chiffre d’affaires, "
                "la croissance, la rentabilité, le cashflow, les risques, les "
                "prévisions ou les décisions prioritaires."
            ),
            "decision_title": (
                "Importer des données de performance avant de prendre des décisions business"
            ),
            "decision": (
                "Importez un fichier avec des revenus datés, commandes, dépenses, "
                "clients, cashflow ou dépenses publicitaires avant d’utiliser cet "
                "agent pour des décisions exécutives."
            ),
            "why": (
                "Le fichier importé ne contient pas de métriques de performance "
                "business vérifiées."
            ),
            "recommendation": (
                "Importez un fichier avec des revenus datés, commandes, dépenses, "
                "clients, cashflow ou dépenses publicitaires avant d’utiliser cet "
                "agent pour des décisions exécutives."
            ),
            "recommendation_impact": (
                "Permet une analyse vérifiée des KPI, des risques, des prévisions "
                "et des décisions."
            ),
            "insight": (
                "Le fichier importé ne contient pas de métriques de performance "
                "business vérifiées."
            ),
            "health_reason": (
                "Le score de santé business est indisponible faute de données de "
                "performance suffisantes."
            ),
            "forecast_explanation": (
                "Les prévisions nécessitent suffisamment de données datées sur les "
                "revenus ou la performance business."
            ),
        },
        "ar": {
            "summary": (
                "لا يحتوي الملف المرفوع على بيانات أداء أعمال موثقة وكافية لحساب "
                "الإيرادات أو النمو أو الربحية أو التدفق النقدي أو المخاطر أو "
                "التوقعات أو القرارات ذات الأولوية."
            ),
            "decision_title": "ارفع بيانات أداء قبل اتخاذ قرارات أعمال",
            "decision": (
                "ارفع ملفاً يحتوي على إيرادات مؤرخة أو طلبات أو مصروفات أو عملاء "
                "أو تدفق نقدي أو إنفاق إعلاني قبل استخدام هذا الوكيل لاتخاذ "
                "قرارات تنفيذية."
            ),
            "why": "لا يحتوي الملف المرفوع على مؤشرات أداء أعمال موثقة.",
            "recommendation": (
                "ارفع ملفاً يحتوي على إيرادات مؤرخة أو طلبات أو مصروفات أو عملاء "
                "أو تدفق نقدي أو إنفاق إعلاني قبل استخدام هذا الوكيل لاتخاذ "
                "قرارات تنفيذية."
            ),
            "recommendation_impact": (
                "يتيح تحليلاً موثقاً للمؤشرات والمخاطر والتوقعات والقرارات."
            ),
            "insight": "لا يحتوي الملف المرفوع على مؤشرات أداء أعمال موثقة.",
            "health_reason": (
                "درجة صحة الأعمال غير متاحة بسبب عدم توفر بيانات أداء كافية."
            ),
            "forecast_explanation": (
                "تتطلب التوقعات بيانات كافية ومؤرخة عن الإيرادات أو أداء الأعمال."
            ),
        },
    }

    text = messages.get(output_language, messages["en"])

    result["analysis_available"] = False
    result["confidence_level"] = "low"
    result["executive_summary"] = text["summary"]

    result["kpis"] = {
        "revenue": None,
        "expenses": None,
        "profit": None,
        "profit_margin_percent": None,
        "growth_rate_percent": None,
        "cashflow_status": "unknown",
        "revenue_available": False,
        "expenses_available": False,
        "profit_available": False,
        "growth_available": False,
        "cashflow_available": False,
    }

    result["advanced_kpis"] = {}
    result["monthly_series"] = []
    result["charts"] = []

    result["forecast"] = {
        "available": False,
        "next_month_revenue": None,
        "next_quarter_revenue": None,
        "trend": "unknown",
        "explanation": text["forecast_explanation"],
    }

    result["business_health_score"] = None
    result["business_health"] = {
        "available": False,
        "score": None,
        "rating": "not_available",
        "reason": text["health_reason"],
        "components": {},
        "weights": {},
        "strengths": [],
        "warnings": [text["insight"]],
        "availability": {
            "profit": False,
            "roas": False,
            "churn": False,
            "cac": False,
        },
        "source": "business_health_scoring",
    }

    result["currency"] = _unknown_currency()

    result["risks"] = []
    result["opportunities"] = []
    result["recommendations"] = [
        {
            "recommendation": text["recommendation"],
            "priority": "medium",
            "expected_impact": text["recommendation_impact"],
            "action_steps": [
                text["recommendation"],
            ],
        }
    ]

    result["smart_insights"] = {
        "most_important_decision": {
            "title": text["decision_title"],
            "decision": text["decision"],
            "why": text["why"],
            "impact": "medium",
            "timeframe": "before executive decisions",
        },
        "key_insights": [
            text["insight"],
            text["health_reason"],
        ],
    }

    result.setdefault("data_quality", {})
    result["data_quality"]["score"] = int(result["data_quality"].get("score") or 0)
    limitations = result["data_quality"].get("limitations")
    if not isinstance(limitations, list):
        limitations = []
    if text["insight"] not in limitations:
        limitations.append(text["insight"])
    result["data_quality"]["limitations"] = limitations

    missing_fields = result["data_quality"].get("missing_fields")
    if not isinstance(missing_fields, list):
        missing_fields = []
    for field in (
        "revenue",
        "expenses",
        "profit",
        "cashflow",
        "customers",
        "orders",
        "marketing_spend",
    ):
        if field not in missing_fields:
            missing_fields.append(field)
    result["data_quality"]["missing_fields"] = missing_fields

    return result


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

    has_verified_business_performance_data = _has_verified_business_performance_data(
        detected_kpis
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

    if not has_verified_business_performance_data:
        result = _mark_non_performance_dataset(
            result=result,
            output_language=output_language,
        )

    update_job_progress(job, db, 58, business_progress_message("charts", output_language))

    if has_verified_business_performance_data:
        charts = build_business_charts(rows=normalized_rows, column_mapping=column_mapping)
        forecast = forecast_business_performance(rows=normalized_rows, column_mapping=column_mapping)
    else:
        charts = []
        forecast = result.get("forecast", {})

    result["charts"] = charts
    result["forecast"] = forecast

    update_job_progress(job, db, 72, business_progress_message("intelligence", output_language))

    result = apply_backend_health_score(result=result, detected_kpis=detected_kpis)
    result = attach_business_anomalies_v2(
        result=result,
        detected_kpis=detected_kpis,
        forecast=forecast,
        strictness="professional",
        language=output_language,
    )
    result = build_business_decision_layer(
        result=result,
        detected_kpis=detected_kpis,
        language=output_language,
    )

    result["file_metadata"] = {
        "file_name": file_name,
        "rows_count": row_count,
        "columns": columns,
        "column_mapping": column_mapping,
        "output_language": output_language,
    }

    result = attach_business_memory(db=db, user_id=job.user_id, current_result=result)
    result = _force_backend_financial_truth(result, detected_kpis, business_model)

    if not has_verified_business_performance_data:
        result = _mark_non_performance_dataset(
            result=result,
            output_language=output_language,
        )

    result = apply_backend_health_score(result=result, detected_kpis=detected_kpis)
    result = attach_business_anomalies_v2(
        result=result,
        detected_kpis=detected_kpis,
        forecast=forecast,
        strictness="professional",
        language=output_language,
    )
    result = build_business_decision_layer(
        result=result,
        detected_kpis=detected_kpis,
        language=output_language,
    )
    result = attach_currency_to_result(result=result, rows=normalized_rows, default_currency=None)

    if not has_verified_business_performance_data:
        result["currency"] = _unknown_currency()

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
