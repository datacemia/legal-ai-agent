import json
import os
from typing import Any

from openai import OpenAI

from app.services.business_agent.prompts.analysis_prompt import build_analysis_prompt
from app.services.business_agent.prompts.system_prompt import SYSTEM_PROMPT


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


DEFAULT_DISCLAIMER = (
    "This is for business decision support only. "
    "Verify important decisions with a qualified professional."
)


def build_default_business_result(
    executive_summary: str = "Analysis unavailable.",
    limitation: str = "The analysis could not be completed.",
) -> dict[str, Any]:
    return {
        "business_model": "general",
        "confidence_level": "low",
        "executive_summary": executive_summary,
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
                "title": "Analysis unavailable",
                "decision": "Retry the analysis with a cleaner business file.",
                "why": limitation,
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
            "explanation": "Forecast unavailable because the analysis could not be completed.",
        },
        "data_quality": {
            "score": 0,
            "limitations": [limitation],
            "missing_fields": [],
        },
        "disclaimer": DEFAULT_DISCLAIMER,
    }


def ensure_business_result_shape(result: dict[str, Any]) -> dict[str, Any]:
    """
    Keeps the API response stable even if the AI omits a field.
    This avoids breaking the frontend while still returning the richer AI CFO shape.
    """

    default_result = build_default_business_result()

    for key, value in default_result.items():
        if key not in result or result[key] is None:
            result[key] = value

    result.setdefault("kpis", {})

    if not isinstance(result["kpis"], dict):
        result["kpis"] = default_result["kpis"]

    for key, value in default_result["kpis"].items():
        if key not in result["kpis"] or result["kpis"][key] is None:
            result["kpis"][key] = value

    result.setdefault("advanced_kpis", {})

    if not isinstance(result["advanced_kpis"], dict):
        result["advanced_kpis"] = {}

    result.setdefault("monthly_series", [])

    if not isinstance(result["monthly_series"], list):
        result["monthly_series"] = []

    result.setdefault("smart_insights", {})

    if not isinstance(result["smart_insights"], dict):
        result["smart_insights"] = default_result["smart_insights"]

    result["smart_insights"].setdefault(
        "most_important_decision",
        default_result["smart_insights"]["most_important_decision"],
    )

    if not isinstance(result["smart_insights"]["most_important_decision"], dict):
        result["smart_insights"]["most_important_decision"] = (
            default_result["smart_insights"]["most_important_decision"]
        )

    result["smart_insights"].setdefault("key_insights", [])

    if not isinstance(result["smart_insights"]["key_insights"], list):
        result["smart_insights"]["key_insights"] = []

    result.setdefault("forecast", default_result["forecast"])

    if not isinstance(result["forecast"], dict):
        result["forecast"] = default_result["forecast"]

    for key, value in default_result["forecast"].items():
        if key not in result["forecast"] or result["forecast"][key] is None:
            result["forecast"][key] = value

    result.setdefault("data_quality", default_result["data_quality"])

    if not isinstance(result["data_quality"], dict):
        result["data_quality"] = default_result["data_quality"]

    for key, value in default_result["data_quality"].items():
        if key not in result["data_quality"] or result["data_quality"][key] is None:
            result["data_quality"][key] = value

    result.setdefault("risks", [])
    result.setdefault("opportunities", [])
    result.setdefault("recommendations", [])
    result.setdefault("charts", [])
    result.setdefault("disclaimer", DEFAULT_DISCLAIMER)

    if not isinstance(result["risks"], list):
        result["risks"] = []

    if not isinstance(result["opportunities"], list):
        result["opportunities"] = []

    if not isinstance(result["recommendations"], list):
        result["recommendations"] = []

    if not isinstance(result["charts"], list):
        result["charts"] = []

    return result


def apply_backend_source_of_truth(
    result: dict[str, Any],
    backend_kpis: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Strict 10/10 rule:
    - Backend is the source of truth for all numeric KPI values.
    - AI is only the reasoning/explanation layer.
    - This prevents hallucinated revenue, profit, growth, and data quality.
    """

    backend_kpis = backend_kpis or {}

    core_kpis = backend_kpis.get("core_kpis") or {}
    advanced_kpis = backend_kpis.get("advanced_kpis") or {}
    monthly_series = backend_kpis.get("monthly_series") or []
    data_quality = backend_kpis.get("data_quality") or {}
    business_model = backend_kpis.get("business_model")
    model_detection = backend_kpis.get("model_detection") or {}

    if core_kpis:
        result["kpis"] = core_kpis

    if advanced_kpis:
        result["advanced_kpis"] = advanced_kpis

    if monthly_series:
        result["monthly_series"] = monthly_series

    if data_quality:
        result["data_quality"] = data_quality

    if business_model:
        result["business_model"] = business_model

    if model_detection:
        result["business_model_detection"] = model_detection

        confidence = model_detection.get("confidence")

        if confidence:
            result["confidence_level"] = confidence

    # Store strict backend metadata for debugging / auditability.
    result["backend_truth"] = {
        "enabled": True,
        "source": backend_kpis.get("source", "backend_calculated_strict"),
        "rows_count": backend_kpis.get("rows_count", 0),
        "column_mapping": backend_kpis.get("column_mapping", {}),
        "detected_kpi_columns": backend_kpis.get("detected_kpi_columns", {}),
        "suggested_kpis": backend_kpis.get("suggested_kpis", []),
    }

    return result


def analyze_business_data(
    business_data: str,
    backend_kpis: dict[str, Any] | None = None,
    output_language: str = "en",
) -> dict[str, Any]:
    """
    AI CFO analysis.

    Important:
    backend_kpis is optional for backward compatibility, but when provided,
    it overrides AI numeric KPIs and data quality.
    """

    if not business_data or not business_data.strip():
        result = build_default_business_result(
            executive_summary="No business data was provided.",
            limitation="The extracted business data is empty.",
        )

        return apply_backend_source_of_truth(
            result=result,
            backend_kpis=backend_kpis,
        )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": build_analysis_prompt(
                    business_data=business_data,
                    output_language=output_language,
                ),
            },
        ],
        temperature=0.2,
    )

    content = response.choices[0].message.content or "{}"

    try:
        parsed_result = json.loads(content)

    except json.JSONDecodeError:
        result = build_default_business_result(
            executive_summary="AI returned invalid JSON.",
            limitation="The AI response could not be parsed as JSON.",
        )

        return apply_backend_source_of_truth(
            result=result,
            backend_kpis=backend_kpis,
        )

    if not isinstance(parsed_result, dict):
        result = build_default_business_result(
            executive_summary="AI returned an invalid response format.",
            limitation="The AI response was not a JSON object.",
        )

        return apply_backend_source_of_truth(
            result=result,
            backend_kpis=backend_kpis,
        )

    parsed_result = ensure_business_result_shape(parsed_result)

    parsed_result = apply_backend_source_of_truth(
        result=parsed_result,
        backend_kpis=backend_kpis,
    )

    return ensure_business_result_shape(parsed_result)
