from typing import Any


def _to_float(value: Any) -> float:
    if value is None:
        return 0.0

    if isinstance(value, bool):
        return 0.0

    if isinstance(value, (int, float)):
        return float(value)

    try:
        return float(str(value).replace(",", ".").strip())
    except Exception:
        return 0.0


def _clamp(value: float, minimum: float = 0.0, maximum: float = 100.0) -> float:
    return max(minimum, min(maximum, value))


def _score_profit_margin(profit_margin_percent: float) -> dict[str, Any]:
    """
    Profit margin score.
    Strong margins improve business health.
    Negative margins heavily penalize the score.
    """

    if profit_margin_percent >= 35:
        score = 100
        signal = "excellent_margin"
        label = "Excellent profit margin."
    elif profit_margin_percent >= 20:
        score = 85
        signal = "healthy_margin"
        label = "Healthy profit margin."
    elif profit_margin_percent >= 10:
        score = 65
        signal = "moderate_margin"
        label = "Moderate profit margin."
    elif profit_margin_percent >= 0:
        score = 45
        signal = "thin_margin"
        label = "Thin profit margin."
    else:
        score = 10
        signal = "negative_margin"
        label = "Negative profit margin."

    return {
        "score": score,
        "signal": signal,
        "label": label,
        "value": round(profit_margin_percent, 2),
    }



def _score_profitability_unavailable() -> dict[str, Any]:
    return {
        "score": 60,
        "signal": "profitability_unavailable",
        "label": "Profitability unavailable because expenses or costs were not provided.",
        "value": "unavailable",
    }

def _score_growth(growth_rate_percent: float) -> dict[str, Any]:
    """
    Growth score.
    Rewards sustainable growth, not extreme or negative movement.
    """

    if growth_rate_percent >= 30:
        score = 90
        signal = "very_high_growth"
        label = "Very strong growth."
    elif growth_rate_percent >= 10:
        score = 85
        signal = "healthy_growth"
        label = "Healthy growth."
    elif growth_rate_percent >= 3:
        score = 70
        signal = "moderate_growth"
        label = "Moderate growth."
    elif growth_rate_percent >= -3:
        score = 55
        signal = "flat_growth"
        label = "Flat growth."
    elif growth_rate_percent >= -15:
        score = 35
        signal = "declining_growth"
        label = "Revenue is declining."
    else:
        score = 15
        signal = "severe_decline"
        label = "Severe revenue decline."

    return {
        "score": score,
        "signal": signal,
        "label": label,
        "value": round(growth_rate_percent, 2),
    }


def _score_cashflow(cashflow_status: str) -> dict[str, Any]:
    normalized = str(cashflow_status or "").lower().strip()

    if normalized == "positive":
        score = 90
        signal = "positive_cashflow"
        label = "Positive cashflow."
    elif normalized == "negative":
        score = 15
        signal = "negative_cashflow"
        label = "Negative cashflow."
    else:
        score = 60
        signal = "unknown_cashflow"
        label = "Cashflow status is unavailable or unclear."

    return {
        "score": score,
        "signal": signal,
        "label": label,
        "value": normalized or "unknown",
    }


def _score_churn(churn_rate_percent: float) -> dict[str, Any]:
    """
    Churn scoring for SaaS/subscription-like businesses.
    Lower churn is better.
    """

    if churn_rate_percent <= 0:
        score = 70
        signal = "churn_unknown_or_zero"
        label = "Churn is zero or unavailable."
    elif churn_rate_percent <= 3:
        score = 95
        signal = "excellent_churn"
        label = "Excellent churn level."
    elif churn_rate_percent <= 7:
        score = 80
        signal = "healthy_churn"
        label = "Healthy churn level."
    elif churn_rate_percent <= 12:
        score = 55
        signal = "elevated_churn"
        label = "Elevated churn."
    elif churn_rate_percent <= 20:
        score = 35
        signal = "high_churn"
        label = "High churn."
    else:
        score = 15
        signal = "critical_churn"
        label = "Critical churn level."

    return {
        "score": score,
        "signal": signal,
        "label": label,
        "value": round(churn_rate_percent, 2),
    }


def _score_roas(roas: float) -> dict[str, Any]:
    """
    ROAS score.
    If no ad spend exists, neutral score.
    """

    if roas <= 0:
        score = 60
        signal = "roas_unavailable"
        label = "ROAS unavailable."
    elif roas >= 5:
        score = 95
        signal = "excellent_roas"
        label = "Excellent ROAS."
    elif roas >= 3:
        score = 80
        signal = "healthy_roas"
        label = "Healthy ROAS."
    elif roas >= 1.5:
        score = 55
        signal = "weak_roas"
        label = "Weak ROAS."
    elif roas >= 1:
        score = 35
        signal = "low_roas"
        label = "Low ROAS."
    else:
        score = 15
        signal = "unprofitable_ads"
        label = "Advertising appears unprofitable."

    return {
        "score": score,
        "signal": signal,
        "label": label,
        "value": round(roas, 2),
    }


def _score_cac_efficiency(cac: float, revenue_per_customer: float) -> dict[str, Any]:
    """
    CAC efficiency.
    If CAC is unavailable, neutral score.
    """

    if cac <= 0 or revenue_per_customer <= 0:
        return {
            "score": 60,
            "signal": "cac_efficiency_unavailable",
            "label": "CAC efficiency unavailable.",
            "value": {
                "cac": round(cac, 2),
                "revenue_per_customer": round(revenue_per_customer, 2),
            },
        }

    ratio = cac / revenue_per_customer

    if ratio <= 0.25:
        score = 95
        signal = "excellent_cac_efficiency"
        label = "Excellent CAC efficiency."
    elif ratio <= 0.5:
        score = 80
        signal = "healthy_cac_efficiency"
        label = "Healthy CAC efficiency."
    elif ratio <= 0.85:
        score = 60
        signal = "moderate_cac_efficiency"
        label = "Moderate CAC efficiency."
    elif ratio <= 1.2:
        score = 35
        signal = "weak_cac_efficiency"
        label = "Weak CAC efficiency."
    else:
        score = 15
        signal = "critical_cac_efficiency"
        label = "CAC may be too high."

    return {
        "score": score,
        "signal": signal,
        "label": label,
        "value": {
            "cac": round(cac, 2),
            "revenue_per_customer": round(revenue_per_customer, 2),
            "cac_to_revenue_per_customer_ratio": round(ratio, 2),
        },
    }


def _score_data_quality(data_quality_score: float) -> dict[str, Any]:
    if data_quality_score >= 90:
        score = 100
        signal = "excellent_data_quality"
        label = "Excellent data quality."
    elif data_quality_score >= 75:
        score = 80
        signal = "good_data_quality"
        label = "Good data quality."
    elif data_quality_score >= 50:
        score = 55
        signal = "limited_data_quality"
        label = "Limited data quality."
    else:
        score = 25
        signal = "poor_data_quality"
        label = "Poor data quality."

    return {
        "score": score,
        "signal": signal,
        "label": label,
        "value": round(data_quality_score, 2),
    }


def calculate_backend_health_score(
    core_kpis: dict[str, Any] | None = None,
    advanced_kpis: dict[str, Any] | None = None,
    data_quality: dict[str, Any] | None = None,
    business_model: str = "general",
) -> dict[str, Any]:
    """
    Deterministic business health scoring.

    Score dimensions:
    - Profit margin when profitability is available
    - Revenue growth
    - Cashflow
    - Churn when available
    - ROAS when available
    - CAC efficiency when available
    - Data quality

    Missing KPIs are treated as neutral/unavailable rather than as strong
    positives or negatives. Revenue-only ecommerce files should not be
    punished as if margin, ROAS, churn, CAC, or cashflow were bad.
    """

    core_kpis = core_kpis or {}
    advanced_kpis = advanced_kpis or {}
    data_quality = data_quality or {}

    profit_margin = _to_float(core_kpis.get("profit_margin_percent"))
    growth_rate = _to_float(core_kpis.get("growth_rate_percent"))
    cashflow_status = str(core_kpis.get("cashflow_status") or "unknown")

    churn_rate = _to_float(advanced_kpis.get("churn_rate_percent"))
    roas = _to_float(advanced_kpis.get("roas"))
    cac = _to_float(advanced_kpis.get("cac"))
    revenue_per_customer = _to_float(advanced_kpis.get("revenue_per_customer"))
    data_quality_score = _to_float(data_quality.get("score", 50))

    profit_available = bool(core_kpis.get("profit_available", True))
    roas_available = bool(advanced_kpis.get("roas_available", roas > 0))
    churn_available = bool(advanced_kpis.get("churn_available", churn_rate > 0))
    cac_available = bool(advanced_kpis.get("cac_available", cac > 0 and revenue_per_customer > 0))

    components = {
        "profit_margin": (
            _score_profit_margin(profit_margin)
            if profit_available
            else _score_profitability_unavailable()
        ),
        "growth": _score_growth(growth_rate),
        "cashflow": _score_cashflow(cashflow_status if profit_available else "unknown"),
        "churn": _score_churn(churn_rate) if churn_available else {
            "score": 60,
            "signal": "churn_unavailable",
            "label": "Churn unavailable.",
            "value": "unavailable",
        },
        "roas": _score_roas(roas) if roas_available else {
            "score": 60,
            "signal": "roas_unavailable",
            "label": "ROAS unavailable.",
            "value": "unavailable",
        },
        "cac_efficiency": (
            _score_cac_efficiency(cac, revenue_per_customer)
            if cac_available
            else {
                "score": 60,
                "signal": "cac_efficiency_unavailable",
                "label": "CAC efficiency unavailable.",
                "value": {
                    "cac": round(cac, 2),
                    "revenue_per_customer": round(revenue_per_customer, 2),
                },
            }
        ),
        "data_quality": _score_data_quality(data_quality_score),
    }

    normalized_model = str(business_model or "general").lower().strip()

    if normalized_model == "saas":
        weights = {
            "profit_margin": 0.20,
            "growth": 0.20,
            "cashflow": 0.15,
            "churn": 0.18,
            "roas": 0.10,
            "cac_efficiency": 0.10,
            "data_quality": 0.07,
        }

    elif normalized_model == "ecommerce":
        weights = {
            "profit_margin": 0.24,
            "growth": 0.18,
            "cashflow": 0.18,
            "churn": 0.06,
            "roas": 0.18,
            "cac_efficiency": 0.09,
            "data_quality": 0.07,
        }

    else:
        weights = {
            "profit_margin": 0.25,
            "growth": 0.20,
            "cashflow": 0.20,
            "churn": 0.08,
            "roas": 0.10,
            "cac_efficiency": 0.10,
            "data_quality": 0.07,
        }

    weighted_score = 0.0

    for key, weight in weights.items():
        weighted_score += components[key]["score"] * weight

    score = int(round(_clamp(weighted_score)))

    if score >= 85:
        rating = "excellent"
    elif score >= 70:
        rating = "healthy"
    elif score >= 55:
        rating = "moderate"
    elif score >= 40:
        rating = "weak"
    else:
        rating = "critical"

    strengths = []
    warnings = []

    for component in components.values():
        component_score = component["score"]

        if component_score >= 80:
            strengths.append(component["label"])
        elif component_score <= 40:
            warnings.append(component["label"])

    return {
        "score": score,
        "rating": rating,
        "components": components,
        "weights": weights,
        "strengths": strengths[:5],
        "warnings": warnings[:5],
        "availability": {
            "profit": profit_available,
            "roas": roas_available,
            "churn": churn_available,
            "cac": cac_available,
        },
        "source": "business_health_scoring",
    }

def apply_backend_health_score(
    result: dict[str, Any],
    detected_kpis: dict[str, Any],
) -> dict[str, Any]:
    """
    Mutates and returns result with deterministic business health score.

    Use after backend KPIs have been calculated and injected.

    If an earlier validation / decision layer marks the upload as not
    suitable for business performance analysis, do not force a synthetic
    health score. This prevents product catalogs, SKU lists, inventory
    reference files, and other non-performance datasets from becoming
    misleading 0/100 or 59/100 business-health results.
    """

    if result.get("analysis_available") is False:
        existing_health = result.get("business_health")
        existing_reason = ""

        if isinstance(existing_health, dict):
            existing_reason = str(existing_health.get("reason") or "").strip()

        reason = (
            existing_reason
            or "Business health score is unavailable because insufficient business performance data was provided."
        )

        result["business_health_score"] = None
        result["business_health"] = {
            "available": False,
            "score": None,
            "rating": "not_available",
            "reason": reason,
            "components": {},
            "weights": {},
            "strengths": [],
            "warnings": [],
            "availability": {
                "profit": False,
                "roas": False,
                "churn": False,
                "cac": False,
            },
            "source": "business_health_scoring",
        }

        return result

    detected_kpis = detected_kpis or {}
    core_kpis = detected_kpis.get("core_kpis", {}) or {}
    advanced_kpis = detected_kpis.get("advanced_kpis", {}) or {}

    revenue_available = bool(core_kpis.get("revenue_available"))
    growth_available = bool(core_kpis.get("growth_available"))
    expenses_available = bool(core_kpis.get("expenses_available"))
    profit_available = bool(core_kpis.get("profit_available"))
    margin_available = bool(core_kpis.get("profit_margin_available"))
    cashflow_available = bool(core_kpis.get("cashflow_available"))

    customer_or_marketing_available = any(
        bool(advanced_kpis.get(flag))
        for flag in (
            "customers_available",
            "orders_available",
            "churn_available",
            "roas_available",
            "cac_available",
            "aov_available",
            "mrr_available",
            "arr_available",
        )
    )

    verified_dimensions = sum(
        [
            revenue_available,
            growth_available,
            expenses_available,
            profit_available,
            margin_available,
            cashflow_available,
            customer_or_marketing_available,
        ]
    )

    completeness_score = int(round((verified_dimensions / 7) * 100))
    confidence_level = (
        "high" if completeness_score >= 75
        else "medium" if completeness_score >= 45
        else "low"
    )

    result["data_completeness_score"] = completeness_score
    result["confidence_score"] = completeness_score
    result["confidence_level"] = confidence_level

    data_quality = detected_kpis.get("data_quality", {}) or {}
    if isinstance(data_quality, dict):
        data_quality["data_completeness_score"] = completeness_score
        data_quality["confidence_score"] = completeness_score
        data_quality["confidence_level"] = confidence_level
        result["data_quality"] = data_quality

    has_verified_performance_data = any(
        [
            revenue_available,
            growth_available,
            expenses_available,
            profit_available,
            margin_available,
            cashflow_available,
            customer_or_marketing_available,
        ]
    )

    has_minimum_health_basis = (
        revenue_available
        and (
            expenses_available
            or profit_available
            or margin_available
            or cashflow_available
            or customer_or_marketing_available
        )
    )

    if not has_verified_performance_data or not has_minimum_health_basis:
        result["business_health_score"] = None
        result["business_health"] = {
            "available": False,
            "score": None,
            "rating": "insufficient_data",
            "reason": (
                "Business health score is unavailable because revenue alone is not enough. "
                "Add expenses, profit, margin, cashflow, customers, marketing, or retention data."
            ),
            "data_completeness_score": completeness_score,
            "confidence_score": completeness_score,
            "confidence_level": confidence_level,
            "components": {},
            "weights": {},
            "strengths": [],
            "warnings": [
                "Insufficient data to assess business health reliably."
            ],
            "availability": {
                "revenue": revenue_available,
                "growth": growth_available,
                "expenses": expenses_available,
                "profit": profit_available,
                "margin": margin_available,
                "cashflow": cashflow_available,
                "customer_or_marketing": customer_or_marketing_available,
            },
            "source": "business_health_scoring",
        }
        return result

    health = calculate_backend_health_score(
        core_kpis=core_kpis,
        advanced_kpis=advanced_kpis,
        data_quality=detected_kpis.get("data_quality", {}),
        business_model=detected_kpis.get(
            "business_model",
            result.get("business_model", "general"),
        ),
    )

    result["business_health_score"] = health["score"]
    result["business_health"] = health

    return result
