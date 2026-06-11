from statistics import mean, pstdev
from typing import Any


SEVERITY_LEVELS = {
    "info": {"min_score": 0, "max_score": 24},
    "low": {"min_score": 25, "max_score": 44},
    "medium": {"min_score": 45, "max_score": 64},
    "high": {"min_score": 65, "max_score": 84},
    "critical": {"min_score": 85, "max_score": 100},
}


def _to_float(value: Any) -> float:
    if value is None or isinstance(value, bool):
        return 0.0

    if isinstance(value, (int, float)):
        return float(value)

    try:
        return float(str(value).replace(",", ".").strip())
    except Exception:
        return 0.0


def _clamp(value: float, minimum: float = 0.0, maximum: float = 100.0) -> float:
    return max(minimum, min(maximum, value))


def _percent_change(previous: float, current: float) -> float:
    if previous == 0:
        return 0.0

    return ((current - previous) / previous) * 100


def _safe_mean(values: list[float]) -> float:
    clean_values = [value for value in values if isinstance(value, (int, float))]

    return mean(clean_values) if clean_values else 0.0


def _safe_std(values: list[float]) -> float:
    clean_values = [value for value in values if isinstance(value, (int, float))]

    return pstdev(clean_values) if len(clean_values) >= 2 else 0.0


def _severity_from_score(score: float) -> str:
    score = _clamp(score)

    for severity, config in SEVERITY_LEVELS.items():
        if config["min_score"] <= score <= config["max_score"]:
            return severity

    return "info"


def _confidence_from_context(
    periods_count: int,
    data_quality_score: float,
    supporting_signals: int = 1,
) -> float:
    confidence = 0.45

    if periods_count >= 6:
        confidence += 0.25
    elif periods_count >= 3:
        confidence += 0.15
    elif periods_count >= 2:
        confidence += 0.07

    if data_quality_score >= 90:
        confidence += 0.20
    elif data_quality_score >= 75:
        confidence += 0.12
    elif data_quality_score >= 50:
        confidence += 0.05

    confidence += min(max(supporting_signals, 0), 3) * 0.05

    return round(_clamp(confidence, 0.1, 0.98), 2)


def _impact_score_from_severity(severity: str) -> int:
    scores = {
        "critical": 95,
        "high": 78,
        "medium": 58,
        "low": 35,
        "info": 18,
    }

    return scores.get(severity, 18)


def _latest_period(monthly_series: list[dict[str, Any]]) -> str:
    if not monthly_series:
        return ""

    return str(monthly_series[-1].get("period", ""))


def _series_values(
    monthly_series: list[dict[str, Any]],
    key: str,
) -> list[float]:
    return [_to_float(item.get(key)) for item in monthly_series]


def _fingerprint(
    category: str,
    item_type: str,
    metric: str,
    period: str | None = None,
) -> str:
    parts = [category, item_type, metric, period or "current"]

    return "__".join(
        str(part).lower().strip().replace(" ", "_").replace("-", "_")
        for part in parts
        if part
    )


def _build_item(
    kind: str,
    category: str,
    item_type: str,
    title: str,
    severity_score: float,
    metric: str,
    value: Any,
    what_happened: str,
    why_it_matters: str,
    possible_causes: list[str],
    recommended_actions: list[str],
    business_impact: list[str],
    confidence: float,
    period: str | None = None,
) -> dict[str, Any]:
    severity_score = round(_clamp(severity_score), 2)
    severity = _severity_from_score(severity_score)

    return {
        "kind": kind,
        "category": category,
        "type": item_type,
        "title": title,
        "severity": severity,
        "severity_score": severity_score,
        "confidence": confidence,
        "impact_score": _impact_score_from_severity(severity),
        "metric": metric,
        "value": value,
        "period": period,
        "what_happened": what_happened,
        "why_it_matters": why_it_matters,
        "possible_causes": possible_causes,
        "recommended_actions": recommended_actions,
        "business_impact": business_impact,
        "fingerprint": _fingerprint(category, item_type, metric, period),
    }


def _flag_enabled(payload: dict[str, Any], key: str, default: bool = True) -> bool:
    """
    Read KPI availability flags safely.

    Newer KPI detectors expose flags such as profit_available,
    expenses_available, churn_available, roas_available, and cashflow_available.
    If a flag is missing, default=True preserves backward compatibility.
    """

    if key not in payload:
        return default

    return bool(payload.get(key))


def _series_has_positive_values(
    monthly_series: list[dict[str, Any]],
    key: str,
) -> bool:
    return any(_to_float(item.get(key)) > 0 for item in monthly_series)


def _detect_revenue_items(
    monthly_series: list[dict[str, Any]],
    data_quality_score: float,
) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []

    if len(monthly_series) < 2:
        return items

    previous = _to_float(monthly_series[-2].get("revenue"))
    current = _to_float(monthly_series[-1].get("revenue"))
    change = round(_percent_change(previous, current), 2)
    period = _latest_period(monthly_series)

    if change <= -10:
        items.append(
            _build_item(
                kind="anomaly",
                category="revenue",
                item_type="revenue_drop",
                title="Revenue declined materially.",
                severity_score=min(95, abs(change) * 3.1),
                metric="revenue_change_percent",
                value=change,
                period=period,
                what_happened=f"Revenue changed by {change}% compared with the previous period.",
                why_it_matters="Revenue decline can affect profitability, cash planning, and forecasts.",
                possible_causes=[
                    "Lower demand",
                    "Customer churn",
                    "Lower conversion",
                    "Delayed payments",
                    "Seasonality",
                ],
                recommended_actions=[
                    "Review revenue by channel, product, and customer segment.",
                    "Check whether churn or acquisition slowed.",
                    "Validate whether the drop is one-time or recurring.",
                ],
                business_impact=[
                    "revenue_risk",
                    "forecast_risk",
                    "cashflow_pressure",
                ],
                confidence=_confidence_from_context(
                    len(monthly_series),
                    data_quality_score,
                    2,
                ),
            )
        )

    if len(monthly_series) >= 4:
        revenues = _series_values(monthly_series, "revenue")
        growth_rates = [
            _percent_change(revenues[index - 1], revenues[index])
            for index in range(1, len(revenues))
        ]

        latest_growth = growth_rates[-1]
        previous_average = _safe_mean(growth_rates[:-1])
        momentum_delta = round(latest_growth - previous_average, 2)

        if momentum_delta <= -8:
            items.append(
                _build_item(
                    kind="early_warning",
                    category="growth",
                    item_type="growth_momentum_weakening",
                    title="Revenue growth momentum is weakening.",
                    severity_score=min(75, abs(momentum_delta) * 3.2),
                    metric="growth_momentum_delta_percent",
                    value=momentum_delta,
                    period=period,
                    what_happened=(
                        f"Latest revenue growth is {round(latest_growth, 2)}%, "
                        f"below the recent average of {round(previous_average, 2)}%."
                    ),
                    why_it_matters="A weakening growth trend can appear before a visible revenue drop.",
                    possible_causes=[
                        "Lower conversion rate",
                        "Slower acquisition",
                        "Higher churn",
                        "Seasonality",
                        "Reduced marketing efficiency",
                    ],
                    recommended_actions=[
                        "Review acquisition and conversion for the latest period.",
                        "Compare new customers, churned customers, and ad spend movement.",
                    ],
                    business_impact=[
                        "growth_slowdown",
                        "forecast_risk",
                    ],
                    confidence=_confidence_from_context(
                        len(monthly_series),
                        data_quality_score,
                        2,
                    ),
                )
            )

    if len(monthly_series) >= 5:
        historical = _series_values(monthly_series[:-1], "revenue")
        baseline = _safe_mean(historical)
        volatility = _safe_std(historical)

        if volatility > 0 and current < baseline - 1.5 * volatility:
            items.append(
                _build_item(
                    kind="anomaly",
                    category="revenue",
                    item_type="revenue_below_trend",
                    title="Revenue is below recent trend.",
                    severity_score=70,
                    metric="revenue",
                    value=round(current, 2),
                    period=period,
                    what_happened="Latest revenue is materially below the recent historical baseline.",
                    why_it_matters="Revenue below trend may indicate a structural issue.",
                    possible_causes=[
                        "Demand weakness",
                        "Marketing efficiency decline",
                        "Pricing issue",
                        "Operational bottleneck",
                    ],
                    recommended_actions=[
                        "Compare latest revenue against historical baseline and pipeline.",
                        "Inspect channel-level revenue movement.",
                    ],
                    business_impact=[
                        "growth_slowdown",
                        "forecast_risk",
                    ],
                    confidence=_confidence_from_context(
                        len(monthly_series),
                        data_quality_score,
                        2,
                    ),
                )
            )

    return items


def _detect_expense_items(
    monthly_series: list[dict[str, Any]],
    data_quality_score: float,
    language: str = "en",
) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []

    if len(monthly_series) < 2:
        return items

    previous_expenses = _to_float(monthly_series[-2].get("expenses"))
    current_expenses = _to_float(monthly_series[-1].get("expenses"))
    previous_revenue = _to_float(monthly_series[-2].get("revenue"))
    current_revenue = _to_float(monthly_series[-1].get("revenue"))
    period = _latest_period(monthly_series)

    expense_growth = round(_percent_change(previous_expenses, current_expenses), 2)
    revenue_growth = round(_percent_change(previous_revenue, current_revenue), 2)

    if expense_growth >= 20:
        items.append(
            _build_item(
                kind="anomaly",
                category="expenses",
                item_type="expense_spike",
                title="Expenses increased materially.",
                severity_score=min(90, 35 + expense_growth),
                metric="expense_growth_percent",
                value=expense_growth,
                period=period,
                what_happened=f"Expenses increased by {expense_growth}% compared with the previous period.",
                why_it_matters="Expense spikes can reduce profit margin even when revenue is growing.",
                possible_causes=[
                    "Payroll increase",
                    "Marketing spend increase",
                    "Software or vendor costs",
                    "One-time operational expense",
                ],
                recommended_actions=[
                    "Separate recurring expenses from one-time expenses.",
                    "Review the biggest expense categories.",
                    "Pause non-essential spending until the driver is understood.",
                ],
                business_impact=[
                    "margin_pressure",
                    "cashflow_pressure",
                ],
                confidence=_confidence_from_context(
                    len(monthly_series),
                    data_quality_score,
                    2,
                ),
            )
        )

    gap = round(expense_growth - revenue_growth, 2)

    if gap >= 12:
        items.append(
            _build_item(
                kind="risk",
                category="expenses",
                item_type="expenses_growing_faster_than_revenue",
                title={
                    "en": "Expenses are growing faster than revenue.",
                    "fr": "Les dépenses augmentent plus vite que les revenus.",
                    "ar": "المصاريف تنمو أسرع من الإيرادات.",
                }.get(language, "Expenses are growing faster than revenue."),
                severity_score=min(85, 35 + gap * 2.2),
                metric="expense_vs_revenue_growth_gap",
                value=gap,
                period=period,
                what_happened=f"Expense growth exceeded revenue growth by {gap} percentage points.",
                why_it_matters={
                    "en": "This can compress margins even if revenue continues to grow.",
                    "fr": "Cela peut réduire les marges même si les revenus continuent de progresser.",
                    "ar": "قد يؤدي ذلك إلى ضغط الهوامش حتى إذا استمرت الإيرادات في النمو.",
                }.get(language, "This can compress margins even if revenue continues to grow."),
                possible_causes=[
                    "Scaling costs too quickly",
                    "Inefficient acquisition spend",
                    "Payroll expansion ahead of revenue",
                    "Vendor cost creep",
                ],
                recommended_actions=[
                    {
                    "en": "Compare each major cost category against revenue contribution.",
                    "fr": "Comparez chaque grande catégorie de coûts à sa contribution aux revenus.",
                    "ar": "قارن كل فئة تكلفة رئيسية بمساهمتها في الإيرادات.",
                }.get(language, "Compare each major cost category against revenue contribution."),
                    {
                    "en": "Review whether the spending increase produces measurable return.",
                    "fr": "Vérifiez si l’augmentation des dépenses génère un retour mesurable.",
                    "ar": "راجع ما إذا كانت زيادة الإنفاق تحقق عائداً قابلاً للقياس.",
                }.get(language, "Review whether the spending increase produces measurable return."),
                ],
                business_impact=[
                    "margin_pressure",
                    "profitability_risk",
                ],
                confidence=_confidence_from_context(
                    len(monthly_series),
                    data_quality_score,
                    3,
                ),
            )
        )

    return items


def _detect_profit_items(
    monthly_series: list[dict[str, Any]],
    core_kpis: dict[str, Any],
    data_quality_score: float,
    language: str = "en",
) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    profit_available = _flag_enabled(core_kpis, "profit_available", True)
    margin_available = _flag_enabled(
        core_kpis,
        "profit_margin_available",
        profit_available,
    )
    margin = _to_float(core_kpis.get("profit_margin_percent"))
    period = _latest_period(monthly_series)

    if margin_available and margin < 10:
        items.append(
            _build_item(
                kind="risk",
                category="profitability",
                item_type="thin_profit_margin",
                title="Profit margin is below a healthy range.",
                severity_score=85 if margin < 5 else 70,
                metric="profit_margin_percent",
                value=round(margin, 2),
                period=period or None,
                what_happened=f"Profit margin is {round(margin, 2)}%.",
                why_it_matters="A thin margin leaves less room for growth investment and unexpected costs.",
                possible_causes=[
                    "Pricing too low",
                    "High operating costs",
                    "Low gross margin",
                    "Inefficient marketing spend",
                ],
                recommended_actions=[
                    "Review pricing, direct costs, and operating expenses.",
                    "Identify costs that can be reduced without harming revenue.",
                ],
                business_impact=[
                    "margin_pressure",
                    "cashflow_pressure",
                ],
                confidence=_confidence_from_context(
                    len(monthly_series),
                    data_quality_score,
                    2,
                ),
            )
        )

    if profit_available and len(monthly_series) >= 2:
        previous = _to_float(monthly_series[-2].get("profit"))
        current = _to_float(monthly_series[-1].get("profit"))
        change = round(_percent_change(previous, current), 2)

        if change <= -15:
            items.append(
                _build_item(
                    kind="anomaly",
                    category="profitability",
                    item_type="profit_drop",
                    title={
                    "en": "Profit declined materially.",
                    "fr": "Le profit a fortement diminué.",
                    "ar": "انخفض الربح بشكل ملحوظ.",
                }.get(language, "Profit declined materially."),
                    severity_score=min(90, abs(change) * 2.6),
                    metric="profit_change_percent",
                    value=change,
                    period=period,
                    what_happened=f"Profit changed by {change}% compared with the previous period.",
                    why_it_matters={
                    "en": "Profit deterioration can happen even while revenue is stable or growing.",
                    "fr": "La dégradation du profit peut se produire même lorsque les revenus sont stables ou en croissance.",
                    "ar": "قد يتراجع الربح حتى عندما تكون الإيرادات مستقرة أو في نمو.",
                }.get(language, "Profit deterioration can happen even while revenue is stable or growing."),
                    possible_causes=[
                        "Expense growth",
                        "Revenue mix change",
                        "Discounting",
                        "Churn or lower repeat purchases",
                    ],
                    recommended_actions=[
                        {
                            "en": "Compare revenue growth and expense growth side by side.",
                            "fr": "Comparez la croissance des revenus et celle des dépenses côte à côte.",
                            "ar": "قارن نمو الإيرادات ونمو المصاريف جنباً إلى جنب.",
                        }.get(language, "Compare revenue growth and expense growth side by side."),
                        {
                            "en": "Identify the cost categories that changed most.",
                            "fr": "Identifiez les catégories de coûts qui ont le plus changé.",
                            "ar": "حدد فئات التكاليف التي تغيرت أكثر.",
                        }.get(language, "Identify the cost categories that changed most."),
                    ],
                    business_impact=[
                        "profitability_risk",
                        "margin_pressure",
                    ],
                    confidence=_confidence_from_context(
                        len(monthly_series),
                        data_quality_score,
                        2,
                    ),
                )
            )

    return items


def _detect_customer_items(
    advanced_kpis: dict[str, Any],
    data_quality_score: float,
) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []

    churn_available = _flag_enabled(advanced_kpis, "churn_available", True)
    customer_series_available = _flag_enabled(
        advanced_kpis,
        "customer_series_available",
        True,
    )
    customers = _to_float(advanced_kpis.get("customers"))
    new_customers = _to_float(advanced_kpis.get("new_customers"))
    churned_customers = _to_float(advanced_kpis.get("churned_customers"))
    churn_rate = (
        _to_float(advanced_kpis.get("churn_rate_percent"))
        if churn_available
        else 0.0
    )
    customer_series = advanced_kpis.get("customer_series")

    periods_count = len(customer_series) if isinstance(customer_series, list) else 1

    if churn_available and churn_rate >= 7:
        if churn_rate >= 20:
            severity_score = 88
        elif churn_rate >= 12:
            severity_score = 72
        else:
            severity_score = 55

        items.append(
            _build_item(
                kind="risk",
                category="customers",
                item_type="elevated_churn",
                title="Customer churn is elevated.",
                severity_score=severity_score,
                metric="churn_rate_percent",
                value=round(churn_rate, 2),
                what_happened=f"Estimated churn rate is {round(churn_rate, 2)}%.",
                why_it_matters="High churn reduces growth quality and can make acquisition spend less efficient.",
                possible_causes=[
                    "Weak onboarding",
                    "Poor retention",
                    "Product-market mismatch",
                    "Support or quality issues",
                    "Pricing friction",
                ],
                recommended_actions=[
                    "Analyze churn reasons and cancellation timing.",
                    "Improve onboarding and customer success follow-up.",
                    "Segment churn by acquisition channel or plan.",
                ],
                business_impact=[
                    "retention_risk",
                    "growth_quality_risk",
                    "ltv_pressure",
                ],
                confidence=_confidence_from_context(
                    periods_count,
                    data_quality_score,
                    2,
                ),
            )
        )

    if churn_available and new_customers > 0 and churned_customers > new_customers * 0.5:
        ratio = round(churned_customers / new_customers, 2)

        items.append(
            _build_item(
                kind="early_warning",
                category="customers",
                item_type="churn_high_vs_acquisition",
                title="Customer losses are high relative to new customers.",
                severity_score=min(82, 45 + ratio * 35),
                metric="churned_to_new_customers_ratio",
                value={
                    "new_customers": round(new_customers, 2),
                    "churned_customers": round(churned_customers, 2),
                    "ratio": ratio,
                    "customers": round(customers, 2),
                },
                what_happened="Churned customers represent a high share of newly acquired customers.",
                why_it_matters="Acquiring customers while losing many existing customers can hide weak net growth.",
                possible_causes=[
                    "Retention problems",
                    "Low-quality acquisition channels",
                    "Mismatch between marketing promise and product experience",
                ],
                recommended_actions=[
                    "Prioritize retention before increasing acquisition spend.",
                    "Compare churn by campaign, plan, or customer segment.",
                ],
                business_impact=[
                    "retention_risk",
                    "cac_payback_risk",
                    "growth_quality_risk",
                ],
                confidence=_confidence_from_context(
                    periods_count,
                    data_quality_score,
                    3,
                ),
            )
        )

    if customer_series_available and isinstance(customer_series, list) and len(customer_series) >= 2:
        previous = _to_float(customer_series[-2].get("customers"))
        current = _to_float(customer_series[-1].get("customers"))
        change = round(_percent_change(previous, current), 2)

        if change <= -5:
            items.append(
                _build_item(
                    kind="anomaly",
                    category="customers",
                    item_type="customer_base_decline",
                    title="Customer base declined.",
                    severity_score=min(80, abs(change) * 5),
                    metric="customer_growth_percent",
                    value=change,
                    period=str(customer_series[-1].get("period", "")),
                    what_happened=f"Customer base changed by {change}% compared with the previous period.",
                    why_it_matters="Customer base decline can weaken recurring revenue and future growth.",
                    possible_causes=[
                        "High churn",
                        "Lower acquisition",
                        "Customer dissatisfaction",
                        "Pricing or product changes",
                    ],
                    recommended_actions=[
                        "Review churn and acquisition for the latest period.",
                        "Contact recently churned customers to identify root causes.",
                    ],
                    business_impact=[
                        "retention_risk",
                        "revenue_risk",
                    ],
                    confidence=_confidence_from_context(
                        len(customer_series),
                        data_quality_score,
                        2,
                    ),
                )
            )

    return items


def _detect_marketing_items(
    advanced_kpis: dict[str, Any],
    data_quality_score: float,
    periods_count: int,
) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []

    roas_available = _flag_enabled(advanced_kpis, "roas_available", True)
    cac_available = _flag_enabled(advanced_kpis, "cac_available", True)
    revenue_per_customer_available = _flag_enabled(
        advanced_kpis,
        "revenue_per_customer_available",
        True,
    )
    roas = _to_float(advanced_kpis.get("roas")) if roas_available else 0.0
    cac = _to_float(advanced_kpis.get("cac")) if cac_available else 0.0
    revenue_per_customer = (
        _to_float(advanced_kpis.get("revenue_per_customer"))
        if revenue_per_customer_available
        else 0.0
    )
    ad_spend = _to_float(advanced_kpis.get("ad_spend"))

    if roas_available and ad_spend > 0 and roas > 0 and roas < 2:
        items.append(
            _build_item(
                kind="risk",
                category="marketing",
                item_type="weak_roas",
                title="Marketing return appears weak.",
                severity_score=76 if roas < 1.5 else 58,
                metric="roas",
                value=round(roas, 2),
                what_happened=f"ROAS is {round(roas, 2)}, below a strong efficiency range.",
                why_it_matters="Weak ROAS can reduce profitability and make growth expensive.",
                possible_causes=[
                    "Poor campaign targeting",
                    "Low conversion rate",
                    "High acquisition cost",
                    "Weak offer or funnel",
                ],
                recommended_actions=[
                    "Review campaign-level ROAS.",
                    "Pause low-return campaigns.",
                    "Improve landing page and offer conversion.",
                ],
                business_impact=[
                    "marketing_efficiency_risk",
                    "margin_pressure",
                ],
                confidence=_confidence_from_context(
                    periods_count,
                    data_quality_score,
                    2,
                ),
            )
        )

    if cac_available and revenue_per_customer_available and cac > 0 and revenue_per_customer > 0:
        ratio = cac / revenue_per_customer

        if ratio >= 0.75:
            items.append(
                _build_item(
                    kind="early_warning",
                    category="marketing",
                    item_type="cac_efficiency_pressure",
                    title="CAC efficiency needs attention.",
                    severity_score=82 if ratio >= 1 else 62,
                    metric="cac_to_revenue_per_customer_ratio",
                    value=round(ratio, 2),
                    what_happened="Customer acquisition cost is high compared with revenue per customer.",
                    why_it_matters="If CAC approaches or exceeds revenue per customer, growth may become unprofitable.",
                    possible_causes=[
                        "Expensive paid acquisition",
                        "Low customer monetization",
                        "Weak retention",
                        "Low conversion rate",
                    ],
                    recommended_actions=[
                        "Improve conversion before scaling spend.",
                        "Increase revenue per customer through pricing or upsell.",
                        "Reduce spend on low-quality acquisition channels.",
                    ],
                    business_impact=[
                        "cac_payback_risk",
                        "unit_economics_pressure",
                    ],
                    confidence=_confidence_from_context(
                        periods_count,
                        data_quality_score,
                        2,
                    ),
                )
            )

    return items


def _detect_cashflow_items(
    core_kpis: dict[str, Any],
    forecast: dict[str, Any],
    data_quality_score: float,
    periods_count: int,
) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []

    cashflow_available = _flag_enabled(core_kpis, "cashflow_available", True)
    cashflow_status = str(core_kpis.get("cashflow_status") or "unknown").lower()
    cashflow_risk = str(forecast.get("cashflow_risk") or "").lower()

    if cashflow_available and cashflow_status == "negative":
        items.append(
            _build_item(
                kind="anomaly",
                category="cashflow",
                item_type="negative_cashflow",
                title="Cashflow is negative.",
                severity_score=92,
                metric="cashflow_status",
                value=cashflow_status,
                what_happened="The business generated negative cashflow.",
                why_it_matters="Negative cashflow can create short-term liquidity pressure.",
                possible_causes=[
                    "Expenses exceed revenue",
                    "Delayed collections",
                    "One-time costs",
                    "Margin compression",
                ],
                recommended_actions=[
                    "Reduce non-essential expenses.",
                    "Review collections and payment timing.",
                    "Prepare a short-term cash preservation plan.",
                ],
                business_impact=[
                    "cashflow_pressure",
                    "liquidity_risk",
                ],
                confidence=_confidence_from_context(
                    periods_count,
                    data_quality_score,
                    2,
                ),
            )
        )

    if cashflow_risk in {"high", "critical"}:
        items.append(
            _build_item(
                kind="risk",
                category="cashflow",
                item_type="forecast_cashflow_risk",
                title="Forecast indicates cashflow risk.",
                severity_score=88 if cashflow_risk == "critical" else 72,
                metric="forecast_cashflow_risk",
                value=cashflow_risk,
                what_happened=f"Forecasting engine classified cashflow risk as {cashflow_risk}.",
                why_it_matters="Forward-looking cashflow risk should be addressed before it becomes urgent.",
                possible_causes=[
                    "Expense growth",
                    "Revenue volatility",
                    "Weak margin",
                    "Seasonality",
                ],
                recommended_actions=[
                    "Monitor weekly revenue and expense movement.",
                    "Create a cashflow contingency plan.",
                ],
                business_impact=[
                    "forecast_risk",
                    "cashflow_pressure",
                ],
                confidence=_confidence_from_context(
                    periods_count,
                    data_quality_score,
                    2,
                ),
            )
        )

    return items


def _generate_insights(
    core_kpis: dict[str, Any],
    advanced_kpis: dict[str, Any],
    monthly_series: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    insights: list[dict[str, Any]] = []

    profit_available = _flag_enabled(core_kpis, "profit_available", True)
    margin_available = _flag_enabled(
        core_kpis,
        "profit_margin_available",
        profit_available,
    )
    roas_available = _flag_enabled(advanced_kpis, "roas_available", True)
    churn_available = _flag_enabled(advanced_kpis, "churn_available", True)

    profit_margin = _to_float(core_kpis.get("profit_margin_percent"))
    growth_rate = _to_float(core_kpis.get("growth_rate_percent"))
    roas = _to_float(advanced_kpis.get("roas")) if roas_available else 0.0
    churn_rate = (
        _to_float(advanced_kpis.get("churn_rate_percent"))
        if churn_available
        else 0.0
    )

    if margin_available and profit_margin >= 20 and growth_rate >= 5:
        insights.append(
            {
                "kind": "insight",
                "category": "performance",
                "title": "Growth and profitability are both positive.",
                "summary": "The business is growing while maintaining a healthy profit margin.",
                "business_impact": [
                    "positive_growth_quality",
                    "profitability_strength",
                ],
            }
        )

    if roas_available and roas >= 3:
        insights.append(
            {
                "kind": "insight",
                "category": "marketing",
                "title": "Marketing efficiency appears healthy.",
                "summary": "ROAS is in a healthy range, suggesting acquisition spend is producing return.",
                "business_impact": [
                    "marketing_efficiency",
                ],
            }
        )

    if churn_available and churn_rate > 0 and churn_rate < 7:
        insights.append(
            {
                "kind": "insight",
                "category": "customers",
                "title": "Churn appears controlled.",
                "summary": "Estimated churn is not currently in a high-risk range.",
                "business_impact": [
                    "retention_strength",
                ],
            }
        )

    if profit_available and len(monthly_series) >= 3:
        latest_profit = _to_float(monthly_series[-1].get("profit"))
        average_profit = _safe_mean(_series_values(monthly_series[:-1], "profit"))

        if average_profit > 0 and latest_profit > average_profit:
            insights.append(
                {
                    "kind": "insight",
                    "category": "profitability",
                    "title": "Latest profit is above recent average.",
                    "summary": "The latest period outperformed the recent profit baseline.",
                    "business_impact": [
                        "profitability_strength",
                    ],
                }
            )

    return insights


def detect_business_anomalies_v2(
    result: dict[str, Any] | None = None,
    detected_kpis: dict[str, Any] | None = None,
    forecast: dict[str, Any] | None = None,
    strictness: str = "professional",
) -> dict[str, Any]:
    result = result or {}
    detected_kpis = detected_kpis or {}
    forecast = forecast or result.get("forecast") or {}

    core_kpis = detected_kpis.get("core_kpis") or result.get("kpis") or {}
    advanced_kpis = detected_kpis.get("advanced_kpis") or result.get("advanced_kpis") or {}
    monthly_series = detected_kpis.get("monthly_series") or result.get("monthly_series") or []
    data_quality = detected_kpis.get("data_quality") or result.get("data_quality") or {}
    language = (
        result.get("output_language")
        or result.get("language")
        or detected_kpis.get("output_language")
        or detected_kpis.get("language")
        or "en"
    )

    data_quality_score = _to_float(data_quality.get("score", 75))
    periods_count = len(monthly_series) if isinstance(monthly_series, list) else 0

    if strictness == "casual":
        minimum_score = 55
    elif strictness == "enterprise":
        minimum_score = 35
    else:
        minimum_score = 45

    items: list[dict[str, Any]] = []

    if isinstance(monthly_series, list):
        items.extend(_detect_revenue_items(monthly_series, data_quality_score))

        if (
            _flag_enabled(core_kpis, "expenses_available", True)
            and _series_has_positive_values(monthly_series, "expenses")
        ):
            items.extend(_detect_expense_items(monthly_series, data_quality_score, language))

        items.extend(_detect_profit_items(monthly_series, core_kpis, data_quality_score, language))

    items.extend(_detect_customer_items(advanced_kpis, data_quality_score))
    items.extend(_detect_marketing_items(advanced_kpis, data_quality_score, periods_count))
    items.extend(_detect_cashflow_items(core_kpis, forecast, data_quality_score, periods_count))

    filtered_items = [
        item
        for item in items
        if _to_float(item.get("severity_score")) >= minimum_score
    ]

    filtered_items = sorted(
        filtered_items,
        key=lambda item: (
            _to_float(item.get("severity_score")),
            _to_float(item.get("confidence")),
        ),
        reverse=True,
    )

    anomalies = [item for item in filtered_items if item.get("kind") == "anomaly"]
    risks = [item for item in filtered_items if item.get("kind") == "risk"]
    early_warnings = [item for item in filtered_items if item.get("kind") == "early_warning"]
    insights = _generate_insights(
        core_kpis=core_kpis,
        advanced_kpis=advanced_kpis,
        monthly_series=monthly_series if isinstance(monthly_series, list) else [],
    )

    critical_count = sum(1 for item in filtered_items if item.get("severity") == "critical")
    high_count = sum(1 for item in filtered_items if item.get("severity") == "high")
    medium_count = sum(1 for item in filtered_items if item.get("severity") == "medium")

    if critical_count:
        status = "critical"
    elif high_count:
        status = "high_risk"
    elif medium_count:
        status = "watch"
    elif filtered_items:
        status = "low_risk"
    else:
        status = "normal"

    return {
        "available": True,
        "version": "v2",
        "strictness": strictness,
        "status": status,
        "summary": {
            "total_items": len(filtered_items),
            "anomalies": len(anomalies),
            "risks": len(risks),
            "early_warnings": len(early_warnings),
            "insights": len(insights),
            "critical_count": critical_count,
            "high_count": high_count,
            "medium_count": medium_count,
        },
        "items": filtered_items,
        "anomalies": anomalies,
        "risks": risks,
        "early_warnings": early_warnings,
        "insights": insights,
        "source": "business_risk_engine_v2",
    }


def attach_business_anomalies_v2(
    result: dict[str, Any],
    detected_kpis: dict[str, Any],
    forecast: dict[str, Any] | None = None,
    strictness: str = "professional",
) -> dict[str, Any]:
    result["anomalies_v2"] = detect_business_anomalies_v2(
        result=result,
        detected_kpis=detected_kpis,
        forecast=forecast,
        strictness=strictness,
    )

    result["anomalies"] = result["anomalies_v2"]

    return result
