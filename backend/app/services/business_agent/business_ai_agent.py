import json
import os
import re
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

    Important:
    - business_health_score is allowed to be None when health cannot be calculated.
    - Do not replace None business_health_score with 0, because 0/100 is a real
      critical score and would be misleading for product catalogs or incomplete files.
    """

    default_result = build_default_business_result()

    for key, value in default_result.items():
        if key == "business_health_score":
            if key not in result:
                result[key] = value
            continue

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

    # Preserve explicit backend unavailable health score.
    # Some downstream layers intentionally set business_health_score=None for
    # non-performance files. Do not coerce that to 0 here.
    if result.get("business_health_score") is None:
        business_health = result.get("business_health")

        if isinstance(business_health, dict):
            business_health.setdefault("available", False)
            business_health.setdefault("score", None)
            business_health.setdefault("rating", "not_available")

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



def _safe_output_language(language: str | None) -> str:
    return language if language in {"en", "fr", "ar"} else "en"


def _to_number(value: Any) -> float | None:
    if isinstance(value, bool):
        return None

    if isinstance(value, (int, float)):
        return float(value)

    try:
        return float(value)
    except Exception:
        return None


def _format_business_percent(value: Any, language: str) -> str:
    numeric = _to_number(value)

    if numeric is None:
        return "N/A" if language == "en" else "N/D" if language == "fr" else "غير متاح"

    if language == "fr":
        return f"{numeric:.2f}".rstrip("0").rstrip(".").replace(".", ",") + " %"

    return f"{numeric:.2f}".rstrip("0").rstrip(".") + "%"


def _get_churn_label_key(advanced_kpis: dict[str, Any]) -> str:
    label_key = str(advanced_kpis.get("churn_label_key") or "").strip().lower()
    scope = str(advanced_kpis.get("churn_scope") or "").strip().lower()

    if label_key:
        return label_key

    if scope == "latest_period":
        return "latest_customer_churn"

    if scope == "average_period":
        return "average_customer_churn"

    return "customer_churn"


def _churn_label(advanced_kpis: dict[str, Any], language: str) -> str:
    key = _get_churn_label_key(advanced_kpis)
    labels = {
        "en": {
            "latest_customer_churn": "Latest customer churn",
            "average_customer_churn": "Average customer churn",
            "customer_churn": "Customer churn",
        },
        "fr": {
            "latest_customer_churn": "Churn client dernière période",
            "average_customer_churn": "Churn client moyen",
            "customer_churn": "Churn client",
        },
        "ar": {
            "latest_customer_churn": "معدل فقدان العملاء لآخر فترة",
            "average_customer_churn": "متوسط معدل فقدان العملاء",
            "customer_churn": "معدل فقدان العملاء",
        },
    }

    return labels.get(language, labels["en"]).get(key, labels[language if language in labels else "en"]["customer_churn"])


def _churn_sentence(advanced_kpis: dict[str, Any], language: str) -> str | None:
    churn = _to_number(advanced_kpis.get("churn_rate_percent"))

    if churn is None or churn <= 0:
        return None

    label = _churn_label(advanced_kpis, language)
    value = _format_business_percent(churn, language)

    if language == "fr":
        return f"{label} : {value}. La rétention doit rester suivie."

    if language == "ar":
        return f"{label}: {value}. يجب الاستمرار في متابعة الاحتفاظ بالعملاء."

    return f"{label} is {value}; retention should continue to be monitored."


def _harmonize_churn_text(text: str, advanced_kpis: dict[str, Any], language: str) -> str:
    sentence = _churn_sentence(advanced_kpis, language)

    if not sentence:
        return text

    # Replace legacy generic churn wording with scope-aware wording.
    replacements = [
        (r"Customer churn is estimated at\s+[0-9]+(?:\.[0-9]+)?%[^.]*\.", sentence),
        (r"Estimated churn is not currently in a high-risk range\.", sentence),
        (r"Churn appears controlled\.", sentence),
        (r"Excellent churn level\.", "Excellent customer retention level."),
        (r"The current business risk assessment is Watch\.", "The current business risk assessment is Watch: no critical risks were detected, but monitoring is recommended."),
    ]

    updated = text

    for pattern, replacement in replacements:
        updated = re.sub(pattern, replacement, updated, flags=re.IGNORECASE)

    return updated


def _walk_and_harmonize(value: Any, advanced_kpis: dict[str, Any], language: str) -> Any:
    if isinstance(value, str):
        return _harmonize_churn_text(value, advanced_kpis, language)

    if isinstance(value, list):
        return [_walk_and_harmonize(item, advanced_kpis, language) for item in value]

    if isinstance(value, dict):
        return {
            key: _walk_and_harmonize(item, advanced_kpis, language)
            for key, item in value.items()
        }

    return value


def harmonize_business_narrative(
    result: dict[str, Any],
    output_language: str = "en",
) -> dict[str, Any]:
    """
    Keep generated narrative aligned with deterministic KPI scope.

    The KPI engine can distinguish latest-period, average-period, overall,
    or provided churn. This helper updates only display text; it never changes
    the numeric KPI source of truth.
    """

    language = _safe_output_language(output_language)
    advanced_kpis = result.get("advanced_kpis") or {}

    if not isinstance(advanced_kpis, dict):
        return result

    # Store a stable human label for exports/frontends that do not compute labels.
    advanced_kpis.setdefault("churn_display_label", _churn_label(advanced_kpis, language))
    result["advanced_kpis"] = advanced_kpis

    return _walk_and_harmonize(result, advanced_kpis, language)


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

    parsed_result = ensure_business_result_shape(parsed_result)
    parsed_result = harmonize_business_narrative(
        result=parsed_result,
        output_language=output_language,
    )

    return ensure_business_result_shape(parsed_result)
