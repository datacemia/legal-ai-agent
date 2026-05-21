import json
from typing import Any

from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.utils.security import get_current_user
from app.utils.billing import check_and_consume_agent_access

from app.models.user import User
from app.models.business_analysis import BusinessAnalysis

from app.schemas.business_schema import (
    BusinessHistoryItem,
)

from app.services.business_agent.business_parser import extract_business_data
from app.services.business_agent.business_ai_agent import analyze_business_data
from app.services.business_agent.business_kpi_detector import (
    detect_business_model,
    detect_business_kpis,
)
from app.services.business_agent.business_charts import (
    build_business_charts,
)
from app.services.business_agent.business_forecasting import (
    forecast_business_performance,
)
from app.services.business_agent.business_memory import (
    attach_business_memory,
)
from app.services.business_agent.business_health_score import (
    apply_backend_health_score,
)
from app.services.business_agent.business_anomaly_detector_v2 import (
    attach_business_anomalies_v2,
)
from app.services.business_agent.business_decision_engine import (
    build_business_decision_layer,
)
from app.services.business_agent.business_i18n_service import (
    translate_business_analysis_payload,
)
from app.services.business_agent.business_currency_service import (
    attach_currency_to_result,
    normalize_money_columns,
)

from app.services.enterprise_service import (
    check_enterprise_agent_access,
    consume_enterprise_agent_quota,
    consume_enterprise_credits,
)


router = APIRouter(
    prefix="/business",
    tags=["Business"],
)

BUSINESS_AGENT_CREDITS = 30


def _build_safe_ai_fallback() -> dict[str, Any]:
    return {
        "business_model": "general",
        "confidence_level": "low",
        "executive_summary": "AI analysis returned an invalid response.",
        "business_health_score": 0,
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
    """
    10/10 strict rule:
    Backend-calculated financial data is the source of truth.

    AI can generate:
    - executive_summary
    - risks
    - opportunities
    - recommendations
    - decisions

    Backend must own:
    - business_model
    - kpis
    - advanced_kpis
    - monthly_series
    - data_quality
    """

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

    if core_kpis:
        result["kpis"] = core_kpis

    if advanced_kpis:
        result["advanced_kpis"] = advanced_kpis
    else:
        result["advanced_kpis"] = {}

    if monthly_series:
        result["monthly_series"] = monthly_series
    else:
        result["monthly_series"] = []

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


def _localize_business_result_text(
    result: dict[str, Any],
    output_language: str,
) -> dict[str, Any]:
    """
    Final deterministic localization layer.

    Important:
    - This runs after the backend decision engine.
    - It does not change KPI values.
    - It only localizes known backend-generated business text.
    - It prevents the frontend from showing English text inside a French/Arabic UI.
    """

    language = (output_language or "en").lower()

    if language not in {"fr", "ar"}:
        result["disclaimer"] = (
            "This is for business decision support only. "
            "Verify important decisions with a qualified professional."
        )
        return result

    if language == "fr":
        translations = {
            "SaaS / subscription": "SaaS / abonnement",
            "general business": "entreprise générale",
            "critical": "critique",
            "high": "élevé",
            "medium": "moyen",
            "low": "faible",
            "positive": "positif",
            "negative": "négatif",
            "healthy": "sain",
            "warning": "à surveiller",
            "critical_churn": "désabonnement critique",
            "Customer churn is elevated.": "Le désabonnement client est élevé.",
            "Customer churn is elevated": "Le désabonnement client est élevé",
            "Prioritize retention before scaling acquisition": (
                "Prioriser la rétention avant d’augmenter l’acquisition"
            ),
            "Analyze churn reasons and cancellation timing.": (
                "Analyser les raisons du désabonnement et le moment des annulations."
            ),
            "Improve onboarding and customer success follow-up.": (
                "Améliorer l’onboarding et le suivi customer success."
            ),
            "Prioritize churn reduction before increasing acquisition spend.": (
                "Prioriser la réduction du churn avant d’augmenter les dépenses d’acquisition."
            ),
            "Improve customer retention": "Améliorer la rétention client",
            "Scale efficient acquisition carefully": (
                "Développer l’acquisition efficace avec prudence"
            ),
            "Use healthy profitability to fund focused growth": (
                "Utiliser la rentabilité saine pour financer une croissance ciblée"
            ),
            "Growth and profitability are both positive.": (
                "La croissance et la rentabilité sont toutes deux positives."
            ),
            "Marketing efficiency appears healthy.": (
                "L’efficacité marketing semble saine."
            ),
            "Latest profit is above recent average.": (
                "Le dernier profit est supérieur à la moyenne récente."
            ),
            "High churn reduces growth quality and can make acquisition spend less efficient.": (
                "Un churn élevé réduit la qualité de la croissance et peut rendre les dépenses d’acquisition moins efficaces."
            ),
            "Reducing churn can improve recurring revenue quality, LTV, and growth efficiency.": (
                "Réduire le churn peut améliorer la qualité des revenus récurrents, la LTV et l’efficacité de croissance."
            ),
            "ROAS and CAC efficiency are healthy, which suggests acquisition can be scaled with monitoring.": (
                "Le ROAS et l’efficacité CAC sont sains, ce qui suggère que l’acquisition peut être augmentée avec un suivi strict."
            ),
            "The business has both growth and profit margin strength.": (
                "L’entreprise combine croissance et bonne marge bénéficiaire."
            ),
            "The business is growing while maintaining a healthy profit margin.": (
                "L’entreprise progresse tout en conservant une marge bénéficiaire saine."
            ),
            "ROAS is in a healthy range, suggesting acquisition spend is producing return.": (
                "Le ROAS est dans une zone saine, ce qui suggère que les dépenses d’acquisition génèrent un retour."
            ),
            "The latest period outperformed the recent profit baseline.": (
                "La dernière période dépasse la base de profit récente."
            ),
            "Launch retention analysis, improve onboarding, and segment churn by acquisition channel.": (
                "Lancer une analyse de rétention, améliorer l’onboarding et segmenter le churn par canal d’acquisition."
            ),
            "Increase spend only on channels with proven ROAS and monitor churn quality.": (
                "Augmenter les dépenses uniquement sur les canaux avec un ROAS prouvé et surveiller la qualité du churn."
            ),
            "Allocate budget to the highest-return growth or retention initiative.": (
                "Allouer le budget à l’initiative de croissance ou de rétention au meilleur retour."
            ),
            "Convert this positive signal into a repeatable operating process.": (
                "Transformer ce signal positif en processus opérationnel répétable."
            ),
            "Improves retention, LTV, and recurring revenue stability.": (
                "Améliore la rétention, la LTV et la stabilité des revenus récurrents."
            ),
        }

        def tr(text: Any) -> Any:
            if not isinstance(text, str):
                return text

            translated = translations.get(text)

            if translated:
                return translated

            translated = text
            for source, target in translations.items():
                translated = translated.replace(source, target)

            return translated

        kpis = result.get("kpis") or {}
        health = result.get("business_health") or {}
        anomalies = result.get("anomalies_v2") or {}
        advanced = result.get("advanced_kpis") or {}

        revenue = kpis.get("revenue", 0)
        profit = kpis.get("profit", 0)
        margin = kpis.get("profit_margin_percent", 0)
        growth = kpis.get("growth_rate_percent", 0)
        cashflow = tr(kpis.get("cashflow_status", "unknown"))
        score = result.get("business_health_score", health.get("score", 0))
        rating = tr(health.get("rating", "unknown"))
        anomaly_status = tr(anomalies.get("status", "normal"))
        churn = advanced.get("churn_rate_percent", 0)
        model = tr(result.get("business_model", "general"))

        result["executive_summary"] = (
            f"Cette analyse {model} montre des revenus de {revenue}, "
            f"un profit de {profit} et une marge bénéficiaire de {margin}%. "
            f"La croissance des revenus est de {growth}% et le cashflow est {cashflow}. "
            f"Le score de santé backend est de {score}/100 ({rating}). "
            f"Le moteur d’anomalies classe la situation actuelle comme {anomaly_status}. "
            f"Le churn client est élevé à {churn}%, ce qui doit être traité en priorité."
        )

        result["disclaimer"] = (
            "Ceci est uniquement destiné au soutien à la décision business. "
            "Vérifiez les décisions importantes avec un professionnel qualifié."
        )

    else:
        translations = {
            "SaaS / subscription": "SaaS / اشتراك",
            "general business": "نشاط عام",
            "critical": "حرج",
            "high": "مرتفع",
            "medium": "متوسط",
            "low": "منخفض",
            "positive": "إيجابي",
            "negative": "سلبي",
            "healthy": "صحي",
            "Customer churn is elevated.": "معدل فقدان العملاء مرتفع.",
            "Customer churn is elevated": "معدل فقدان العملاء مرتفع",
            "Prioritize retention before scaling acquisition": (
                "إعطاء الأولوية للاحتفاظ بالعملاء قبل توسيع الاكتساب"
            ),
            "Analyze churn reasons and cancellation timing.": (
                "تحليل أسباب فقدان العملاء وتوقيت الإلغاءات."
            ),
            "Improve onboarding and customer success follow-up.": (
                "تحسين تهيئة العملاء ومتابعة نجاح العملاء."
            ),
            "Prioritize churn reduction before increasing acquisition spend.": (
                "إعطاء الأولوية لتقليل فقدان العملاء قبل زيادة الإنفاق على الاكتساب."
            ),
            "Improve customer retention": "تحسين الاحتفاظ بالعملاء",
            "Scale efficient acquisition carefully": "توسيع الاكتساب الفعال بحذر",
            "Use healthy profitability to fund focused growth": (
                "استخدام الربحية الصحية لتمويل نمو مركز"
            ),
            "High churn reduces growth quality and can make acquisition spend less efficient.": (
                "ارتفاع فقدان العملاء يقلل جودة النمو وقد يجعل إنفاق الاكتساب أقل كفاءة."
            ),
            "Reducing churn can improve recurring revenue quality, LTV, and growth efficiency.": (
                "تقليل فقدان العملاء يمكن أن يحسن جودة الإيرادات المتكررة وقيمة العميل وكفاءة النمو."
            ),
            "Improves retention, LTV, and recurring revenue stability.": (
                "يحسن الاحتفاظ وقيمة العميل واستقرار الإيرادات المتكررة."
            ),
        }

        def tr(text: Any) -> Any:
            if not isinstance(text, str):
                return text

            translated = translations.get(text)

            if translated:
                return translated

            translated = text
            for source, target in translations.items():
                translated = translated.replace(source, target)

            return translated

        kpis = result.get("kpis") or {}
        health = result.get("business_health") or {}
        anomalies = result.get("anomalies_v2") or {}
        advanced = result.get("advanced_kpis") or {}

        revenue = kpis.get("revenue", 0)
        profit = kpis.get("profit", 0)
        margin = kpis.get("profit_margin_percent", 0)
        growth = kpis.get("growth_rate_percent", 0)
        cashflow = tr(kpis.get("cashflow_status", "unknown"))
        score = result.get("business_health_score", health.get("score", 0))
        rating = tr(health.get("rating", "unknown"))
        anomaly_status = tr(anomalies.get("status", "normal"))
        churn = advanced.get("churn_rate_percent", 0)
        model = tr(result.get("business_model", "general"))

        result["executive_summary"] = (
            f"يوضح تحليل {model} إيرادات قدرها {revenue}، "
            f"وربحًا قدره {profit}، وهامش ربح قدره {margin}%. "
            f"نمو الإيرادات هو {growth}% والتدفق النقدي {cashflow}. "
            f"درجة صحة النشاط من النظام الخلفي هي {score}/100 ({rating}). "
            f"يصنف محرك الشذوذ الوضع الحالي على أنه {anomaly_status}. "
            f"معدل فقدان العملاء مرتفع عند {churn}% ويجب التعامل معه كأولوية."
        )

        result["disclaimer"] = (
            "هذا التقرير مخصص فقط لدعم قرارات الأعمال. "
            "تحقق من القرارات المهمة مع متخصص مؤهل."
        )

    def localize_value(value: Any) -> Any:
        if isinstance(value, str):
            return tr(value)

        if isinstance(value, list):
            return [localize_value(item) for item in value]

        if isinstance(value, dict):
            return {
                key: localize_value(nested_value)
                for key, nested_value in value.items()
            }

        return value

    fields_to_localize = [
        "smart_insights",
        "risks",
        "opportunities",
        "recommendations",
        "anomalies_v2",
        "anomalies",
        "business_health",
    ]

    for field in fields_to_localize:
        if field in result:
            result[field] = localize_value(result[field])

    return result


@router.post("/analyze")
async def analyze_business(
    file: UploadFile = File(...),
    output_language: str = Form("en"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Main AI CFO analysis endpoint.

    Flow:
    1. Validate file.
    2. Check billing / enterprise access.
    3. Parse CSV/XLSX business data.
    4. Detect business model and backend KPIs.
    5. Run AI CFO analysis.
    6. Force backend financial truth.
    7. Build charts.
    8. Build deterministic forecast.
    9. Apply backend health scoring.
    10. Attach anomaly detection V2.
    11. Apply backend decision engine.
    12. Attach business memory comparison.
    13. Re-apply backend truth, health, anomalies, and decisions.
    14. Apply final output localization.
    15. Save analysis.
    16. Return full dashboard-ready result.
    """

    # =========================
    # File validation
    # =========================

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="File is required.",
        )

    allowed_extensions = (".csv", ".xlsx")

    if not file.filename.lower().endswith(allowed_extensions):
        raise HTTPException(
            status_code=400,
            detail="Only CSV or Excel (.xlsx) files are supported.",
        )

    # =========================
    # Billing / Enterprise access
    # =========================

    enterprise_context = check_enterprise_agent_access(
        db=db,
        user=current_user,
        agent_slug="business",
    )

    if enterprise_context:
        consume_enterprise_agent_quota(
            db=db,
            access=enterprise_context["access"],
        )

        billing = consume_enterprise_credits(
            db=db,
            user=current_user,
            agent_slug="business",
            credits_used=BUSINESS_AGENT_CREDITS,
            request_type="analysis",
        )

    else:
        billing = check_and_consume_agent_access(
            db=db,
            user=current_user,
            agent_slug="business",
        )

    # =========================
    # Parse business file
    # =========================

    try:
        parsed_data = await extract_business_data(file)

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to parse business file: {str(error)}",
        )

    if not parsed_data:
        raise HTTPException(
            status_code=400,
            detail="Could not extract business data from file.",
        )

    if isinstance(parsed_data, str):
        # Backward compatibility if an old parser is accidentally loaded.
        raw_preview = parsed_data
        normalized_rows = []
        column_mapping = {}
        columns = []
        row_count = 0
    else:
        raw_preview = parsed_data.get("raw_preview", "")
        normalized_rows = parsed_data.get("normalized_rows", [])
        normalized_rows = normalize_money_columns(normalized_rows)
        column_mapping = parsed_data.get("column_mapping", {})
        columns = parsed_data.get("columns", [])
        row_count = parsed_data.get("row_count", len(normalized_rows))

    if not raw_preview.strip():
        raise HTTPException(
            status_code=400,
            detail="Business data preview is empty.",
        )

    # =========================
    # Backend KPI detection
    # =========================

    business_model = detect_business_model(
        columns=columns,
        rows=normalized_rows,
    )

    detected_kpis = detect_business_kpis(
        business_model=business_model,
        rows=normalized_rows,
        column_mapping=column_mapping,
    )

    # =========================
    # AI analysis
    # =========================

    try:
        result = analyze_business_data(
            business_data=raw_preview,
            backend_kpis=detected_kpis,
            output_language=output_language,
        )

    except TypeError:
        # Backward compatibility if business_ai_agent.py has not been upgraded yet.
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

    # =========================
    # Strict backend financial truth
    # =========================

    result = _force_backend_financial_truth(
        result=result,
        detected_kpis=detected_kpis,
        business_model=business_model,
    )

    # =========================
    # Charts
    # =========================

    charts = build_business_charts(
        rows=normalized_rows,
        column_mapping=column_mapping,
    )

    # =========================
    # Forecasting
    # =========================

    forecast = forecast_business_performance(
        rows=normalized_rows,
        column_mapping=column_mapping,
    )

    # =========================
    # Inject dashboard intelligence
    # =========================

    result["charts"] = charts
    result["forecast"] = forecast

    # =========================
    # Backend health score
    # =========================

    result = apply_backend_health_score(
        result=result,
        detected_kpis=detected_kpis,
    )

    # =========================
    # Enterprise anomaly detection V2
    # =========================

    result = attach_business_anomalies_v2(
        result=result,
        detected_kpis=detected_kpis,
        forecast=forecast,
        strictness="professional",
    )

    # =========================
    # Backend decision engine
    # =========================

    result = build_business_decision_layer(
        result=result,
        detected_kpis=detected_kpis,
    )

    result["file_metadata"] = {
        "file_name": file.filename,
        "rows_count": row_count,
        "columns": columns,
        "column_mapping": column_mapping,
        "output_language": output_language,
    }

    # =========================
    # Business memory
    # =========================

    result = attach_business_memory(
        db=db,
        user_id=current_user.id,
        current_result=result,
    )

    # Re-force after memory because memory reads current_result.kpis.
    result = _force_backend_financial_truth(
        result=result,
        detected_kpis=detected_kpis,
        business_model=business_model,
    )

    # Re-apply backend health and anomalies after final backend truth enforcement.
    result = apply_backend_health_score(
        result=result,
        detected_kpis=detected_kpis,
    )

    result = attach_business_anomalies_v2(
        result=result,
        detected_kpis=detected_kpis,
        forecast=forecast,
        strictness="professional",
    )

    # Re-apply deterministic backend decision layer last.
    # This prevents LLM-generated narrative from overriding backend truth.
    result = build_business_decision_layer(
        result=result,
        detected_kpis=detected_kpis,
    )

    # =========================
    # Currency detection / money context
    # =========================

    result = attach_currency_to_result(
        result=result,
        rows=normalized_rows,
        default_currency="USD",
    )

    # =========================
    # Final output localization
    # =========================

    result = translate_business_analysis_payload(
        payload=result,
        language=output_language,
    )

    # =========================
    # Save analysis
    # =========================

    analysis = BusinessAnalysis(
        user_id=current_user.id,
        file_name=file.filename,
        result=json.dumps(result, ensure_ascii=False),
        business_model=str(result.get("business_model", "general")),
        business_health_score=int(result.get("business_health_score", 0) or 0),
        access_type=billing["access_type"],
        credits_used=billing["credits_used"],
        output_language=output_language,
        rows_count=row_count,
    )

    db.add(analysis)
    db.commit()
    db.refresh(analysis)

    return result


@router.get(
    "/history",
    response_model=list[BusinessHistoryItem],
)
def get_business_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Return previous business analyses.
    """

    analyses = (
        db.query(BusinessAnalysis)
        .filter(
            BusinessAnalysis.user_id == current_user.id
        )
        .order_by(BusinessAnalysis.id.desc())
        .all()
    )

    history = []

    for analysis in analyses:
        try:
            parsed_result = json.loads(analysis.result)

        except Exception:
            parsed_result = {
                "error": "Invalid stored analysis result."
            }

        history.append(
            {
                "id": analysis.id,
                "file_name": analysis.file_name,
                "result": parsed_result,
                "created_at": analysis.created_at,
            }
        )

    return history
