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


def _severity_rank(severity: str) -> int:
    ranks = {
        "critical": 5,
        "high": 4,
        "medium": 3,
        "low": 2,
        "info": 1,
    }

    return ranks.get(str(severity or "").lower(), 0)


def _priority_from_severity(severity: str) -> str:
    normalized = str(severity or "").lower()

    if normalized == "critical":
        return "critical"

    if normalized == "high":
        return "high"

    if normalized == "medium":
        return "medium"

    return "low"


def _impact_from_severity(severity: str) -> str:
    normalized = str(severity or "").lower()

    if normalized == "critical":
        return "critical"

    if normalized == "high":
        return "high"

    if normalized == "medium":
        return "medium"

    return "low"


def _business_model_label(business_model: str) -> str:
    labels = {
        "saas": "SaaS / subscription",
        "ecommerce": "e-commerce",
        "agency": "agency / services",
        "restaurant": "restaurant / hospitality",
        "marketplace": "marketplace",
        "general": "general business",
    }

    return labels.get(str(business_model or "general").lower(), "general business")


def _get_top_items(items: list[dict[str, Any]], limit: int = 3) -> list[dict[str, Any]]:
    return sorted(
        items,
        key=lambda item: (
            _to_float(item.get("severity_score")),
            _to_float(item.get("confidence")),
            _to_float(item.get("impact_score")),
        ),
        reverse=True,
    )[:limit]


def _build_default_decision() -> dict[str, Any]:
    return {
        "title": "Continue monitoring business performance",
        "decision": "Keep tracking revenue, expenses, cashflow, and customer metrics before making major changes.",
        "why": "No critical business risk was detected from the current analysis.",
        "impact": "medium",
        "timeframe": "30 days",
        "source": "backend_decision_engine",
    }


def _build_decision_from_top_risk(top_item: dict[str, Any]) -> dict[str, Any]:
    category = top_item.get("category", "business")
    severity = top_item.get("severity", "medium")
    title = str(top_item.get("title") or "Business risk detected")
    metric = top_item.get("metric")
    value = top_item.get("value")

    recommended_actions = top_item.get("recommended_actions") or []
    first_action = (
        recommended_actions[0]
        if recommended_actions
        else "Review the underlying metric and define a corrective action plan."
    )

    if category == "customers":
        decision_title = "Prioritize retention before scaling acquisition"
    elif category == "marketing":
        decision_title = "Improve acquisition efficiency before increasing spend"
    elif category == "cashflow":
        decision_title = "Protect cashflow and reduce near-term financial risk"
    elif category == "expenses":
        decision_title = "Control expense growth before scaling further"
    elif category == "profitability":
        decision_title = "Improve profitability before expanding costs"
    elif category == "revenue":
        decision_title = "Stabilize revenue performance"
    else:
        decision_title = title

    why = str(top_item.get("why_it_matters") or "")

    if metric:
        why = (
            f"{why} Analysis detected {metric} = {value}."
            if why
            else f"Analysis detected {metric} = {value}."
        )

    return {
        "title": decision_title,
        "decision": first_action,
        "why": why,
        "impact": _impact_from_severity(severity),
        "timeframe": "7 days" if severity == "critical" else "30 days",
        "source": "backend_decision_engine",
        "based_on": {
            "category": category,
            "type": top_item.get("type"),
            "metric": metric,
            "value": value,
            "severity": severity,
            "confidence": top_item.get("confidence"),
            "fingerprint": top_item.get("fingerprint"),
        },
    }


def _build_executive_summary(
    business_model: str,
    core_kpis: dict[str, Any],
    advanced_kpis: dict[str, Any],
    health: dict[str, Any],
    anomalies_v2: dict[str, Any],
) -> str:
    model_label = _business_model_label(business_model)
    revenue = _to_float(core_kpis.get("revenue"))
    profit = _to_float(core_kpis.get("profit"))
    margin = _to_float(core_kpis.get("profit_margin_percent"))
    growth = _to_float(core_kpis.get("growth_rate_percent"))
    cashflow_status = str(core_kpis.get("cashflow_status") or "unknown")
    health_score = _to_float(health.get("score"))
    health_rating = str(health.get("rating") or "unknown")
    anomaly_status = str(anomalies_v2.get("status") or "normal")
    churn = _to_float(advanced_kpis.get("churn_rate_percent"))

    summary = (
        f"This {model_label} analysis shows revenue of {round(revenue, 2)}, "
        f"profit of {round(profit, 2)}, and a profit margin of {round(margin, 2)}%. "
        f"Revenue growth is {round(growth, 2)}% and cashflow is {cashflow_status}. "
        f"The Business Health Score is {int(round(health_score))}/100 ({health_rating})."
    )

    if anomaly_status not in {"normal", "low_risk"}:
        summary += f" The current business risk assessment is {anomaly_status}."

    if churn > 12:
        summary += f" Customer churn is elevated at {round(churn, 2)}%, which should be treated as a priority."

    return summary


def _build_risks_from_anomalies(
    anomalies_v2: dict[str, Any],
) -> list[dict[str, Any]]:
    risks = []

    items = anomalies_v2.get("items") or []

    for item in _get_top_items(items, limit=5):
        risks.append(
            {
                "risk": item.get("title", "Business risk detected"),
                "severity": item.get("severity", "medium"),
                "category": item.get("category", "business"),
                "metric": item.get("metric"),
                "value": item.get("value"),
                "confidence": item.get("confidence"),
                "description": item.get("why_it_matters") or item.get("what_happened"),
                "business_impact": item.get("business_impact", []),
                "source": "backend_anomaly_detection_v2",
            }
        )

    return risks


def _build_opportunities(
    core_kpis: dict[str, Any],
    advanced_kpis: dict[str, Any],
    health: dict[str, Any],
    anomalies_v2: dict[str, Any],
) -> list[dict[str, Any]]:
    opportunities = []

    margin = _to_float(core_kpis.get("profit_margin_percent"))
    growth = _to_float(core_kpis.get("growth_rate_percent"))
    roas = _to_float(advanced_kpis.get("roas"))
    churn = _to_float(advanced_kpis.get("churn_rate_percent"))
    cac_ratio = _to_float(
        (health.get("components") or {})
        .get("cac_efficiency", {})
        .get("value", {})
        .get("cac_to_revenue_per_customer_ratio")
    )

    if churn >= 7:
        opportunities.append(
            {
                "opportunity": "Improve customer retention",
                "impact": "high" if churn >= 12 else "medium",
                "why_it_matters": "Reducing churn can improve recurring revenue quality, LTV, and growth efficiency.",
                "recommended_action": "Launch retention analysis, improve onboarding, and segment churn by acquisition channel.",
                "source": "backend_decision_engine",
            }
        )

    if roas >= 3 and cac_ratio > 0 and cac_ratio <= 0.5:
        opportunities.append(
            {
                "opportunity": "Scale efficient acquisition carefully",
                "impact": "medium",
                "why_it_matters": "ROAS and CAC efficiency are healthy, which suggests acquisition can be scaled with monitoring.",
                "recommended_action": "Increase spend only on channels with proven ROAS and monitor churn quality.",
                "source": "backend_decision_engine",
            }
        )

    if margin >= 20 and growth >= 5:
        opportunities.append(
            {
                "opportunity": "Use healthy profitability to fund focused growth",
                "impact": "medium",
                "why_it_matters": "The business has both growth and profit margin strength.",
                "recommended_action": "Allocate budget to the highest-return growth or retention initiative.",
                "source": "backend_decision_engine",
            }
        )

    insights = anomalies_v2.get("insights") or []

    for insight in insights[:2]:
        opportunities.append(
            {
                "opportunity": insight.get("title", "Business improvement opportunity"),
                "impact": "medium",
                "why_it_matters": insight.get("summary", ""),
                "recommended_action": "Convert this positive signal into a repeatable operating process.",
                "business_impact": insight.get("business_impact", []),
                "source": "backend_anomaly_detection_v2",
            }
        )

    return opportunities[:5]


def _build_recommendations(
    anomalies_v2: dict[str, Any],
    core_kpis: dict[str, Any],
    advanced_kpis: dict[str, Any],
) -> list[dict[str, Any]]:
    recommendations = []
    seen_actions = set()

    for item in _get_top_items(anomalies_v2.get("items") or [], limit=5):
        actions = item.get("recommended_actions") or []

        for action in actions[:2]:
            normalized = str(action).strip().lower()

            if not normalized or normalized in seen_actions:
                continue

            seen_actions.add(normalized)

            recommendations.append(
                {
                    "recommendation": action,
                    "priority": _priority_from_severity(item.get("severity", "medium")),
                    "category": item.get("category", "business"),
                    "expected_impact": item.get("why_it_matters", ""),
                    "metric": item.get("metric"),
                    "source": "backend_anomaly_detection_v2",
                }
            )

    churn = _to_float(advanced_kpis.get("churn_rate_percent"))
    margin = _to_float(core_kpis.get("profit_margin_percent"))

    if churn >= 12:
        recommendations.append(
            {
                "recommendation": "Prioritize churn reduction before increasing acquisition spend.",
                "priority": "critical" if churn >= 20 else "high",
                "category": "customers",
                "expected_impact": "Improves retention, LTV, and recurring revenue stability.",
                "metric": "churn_rate_percent",
                "source": "backend_decision_engine",
            }
        )

    if margin < 15:
        recommendations.append(
            {
                "recommendation": "Review pricing, direct costs, and operating expenses to protect margin.",
                "priority": "high",
                "category": "profitability",
                "expected_impact": "Improves profit margin and cashflow resilience.",
                "metric": "profit_margin_percent",
                "source": "backend_decision_engine",
            }
        )

    return recommendations[:6]


def _build_key_insights(
    core_kpis: dict[str, Any],
    advanced_kpis: dict[str, Any],
    health: dict[str, Any],
    anomalies_v2: dict[str, Any],
) -> list[str]:
    insights = []

    revenue = _to_float(core_kpis.get("revenue"))
    profit = _to_float(core_kpis.get("profit"))
    margin = _to_float(core_kpis.get("profit_margin_percent"))
    growth = _to_float(core_kpis.get("growth_rate_percent"))
    churn = _to_float(advanced_kpis.get("churn_rate_percent"))
    roas = _to_float(advanced_kpis.get("roas"))
    health_score = _to_float(health.get("score"))

    insights.append(
        f"Revenue is {round(revenue, 2)} with profit of {round(profit, 2)}."
    )

    insights.append(
        f"Profit margin is {round(margin, 2)}% and revenue growth is {round(growth, 2)}%."
    )

    if churn > 0:
        insights.append(
            f"Customer churn is estimated at {round(churn, 2)}%, which affects retention quality."
        )

    if roas > 0:
        insights.append(
            f"ROAS is {round(roas, 2)}, based on revenue and advertising spend."
        )

    insights.append(
        f"Business Health Score is {int(round(health_score))}/100."
    )

    anomaly_summary = anomalies_v2.get("summary") or {}

    if anomaly_summary:
        insights.append(
            f"{anomaly_summary.get('total_items', 0)} business risk indicator(s) and {anomaly_summary.get('insights', 0)} positive business signal(s) were identified."
        )

    return insights[:6]


def build_business_decision_layer(
    result: dict[str, Any],
    detected_kpis: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Business decision engine.

    This module prevents LLM hallucination from controlling:
    - executive summary
    - most important decision
    - risks
    - opportunities
    - recommendations
    - key insights

    It uses verified deterministic analysis outputs:
    - kpis
    - advanced_kpis
    - business_health
    - anomalies_v2
    - forecast
    - backend_detected_kpis
    """

    detected_kpis = detected_kpis or result.get("backend_detected_kpis") or {}

    business_model = (
        detected_kpis.get("business_model")
        or result.get("business_model")
        or "general"
    )

    core_kpis = detected_kpis.get("core_kpis") or result.get("kpis") or {}
    advanced_kpis = detected_kpis.get("advanced_kpis") or result.get("advanced_kpis") or {}
    health = result.get("business_health") or {}
    anomalies_v2 = result.get("anomalies_v2") or result.get("anomalies") or {}

    items = anomalies_v2.get("items") or []
    top_items = _get_top_items(items, limit=1)

    if top_items:
        most_important_decision = _build_decision_from_top_risk(top_items[0])
    else:
        most_important_decision = _build_default_decision()

    result["executive_summary"] = _build_executive_summary(
        business_model=business_model,
        core_kpis=core_kpis,
        advanced_kpis=advanced_kpis,
        health=health,
        anomalies_v2=anomalies_v2,
    )

    result["smart_insights"] = {
        "most_important_decision": most_important_decision,
        "key_insights": _build_key_insights(
            core_kpis=core_kpis,
            advanced_kpis=advanced_kpis,
            health=health,
            anomalies_v2=anomalies_v2,
        ),
        "source": "backend_decision_engine",
    }

    result["risks"] = _build_risks_from_anomalies(
        anomalies_v2=anomalies_v2,
    )

    result["opportunities"] = _build_opportunities(
        core_kpis=core_kpis,
        advanced_kpis=advanced_kpis,
        health=health,
        anomalies_v2=anomalies_v2,
    )

    result["recommendations"] = _build_recommendations(
        anomalies_v2=anomalies_v2,
        core_kpis=core_kpis,
        advanced_kpis=advanced_kpis,
    )

    result["decision_engine"] = {
        "enabled": True,
        "source": "backend_decision_engine",
        "business_model": business_model,
        "based_on": {
            "core_kpis": bool(core_kpis),
            "advanced_kpis": bool(advanced_kpis),
            "business_health": bool(health),
            "anomalies_v2": bool(anomalies_v2),
        },
    }

    return result
