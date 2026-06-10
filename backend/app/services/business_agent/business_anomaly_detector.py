from statistics import mean, pstdev
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


def _percent_change(previous: float, current: float) -> float:
    if previous == 0:
        return 0.0

    return ((current - previous) / previous) * 100


def _severity_from_percent_drop(value: float) -> str:
    if value <= -35:
        return "critical"

    if value <= -20:
        return "high"

    if value <= -10:
        return "medium"

    return "low"


def _severity_from_percent_increase(value: float) -> str:
    if value >= 60:
        return "critical"

    if value >= 35:
        return "high"

    if value >= 20:
        return "medium"

    return "low"


def _impact_score(severity: str) -> int:
    scores = {
        "critical": 95,
        "high": 80,
        "medium": 60,
        "low": 35,
    }

    return scores.get(severity, 35)


def _build_anomaly(
    anomaly_type: str,
    title: str,
    severity: str,
    metric: str,
    value: Any,
    reason: str,
    recommended_action: str,
    period: str | None = None,
) -> dict[str, Any]:
    return {
        "type": anomaly_type,
        "title": title,
        "severity": severity,
        "impact_score": _impact_score(severity),
        "metric": metric,
        "value": value,
        "period": period,
        "reason": reason,
        "recommended_action": recommended_action,
    }




def _flag_enabled(payload: dict[str, Any], key: str, default: bool = True) -> bool:
    """
    Read KPI availability flags safely.

    Newer KPI detectors expose flags such as profit_available,
    expenses_available, churn_available, and roas_available.
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


def _series_values(
    monthly_series: list[dict[str, Any]],
    key: str,
) -> list[float]:
    values = []

    for item in monthly_series:
        values.append(_to_float(item.get(key)))

    return values


def _latest_period(monthly_series: list[dict[str, Any]]) -> str:
    if not monthly_series:
        return ""

    return str(monthly_series[-1].get("period", ""))


def detect_revenue_anomalies(
    monthly_series: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    anomalies = []

    if len(monthly_series) < 2:
        return anomalies

    previous = _to_float(monthly_series[-2].get("revenue"))
    current = _to_float(monthly_series[-1].get("revenue"))
    change = round(_percent_change(previous, current), 2)
    period = _latest_period(monthly_series)

    if change <= -10:
        severity = _severity_from_percent_drop(change)

        anomalies.append(
            _build_anomaly(
                anomaly_type="revenue_drop",
                title="Revenue dropped compared with the previous period.",
                severity=severity,
                metric="revenue_growth_percent",
                value=change,
                period=period,
                reason=f"Revenue changed by {change}% compared with the previous period.",
                recommended_action=(
                    "Review sales channels, pricing, churn, traffic, and conversion drivers immediately."
                ),
            )
        )

    if len(monthly_series) >= 4:
        revenue_values = _series_values(monthly_series[:-1], "revenue")
        baseline = mean(revenue_values)
        volatility = pstdev(revenue_values) if len(revenue_values) > 1 else 0

        if volatility > 0 and current < baseline - (1.5 * volatility):
            anomalies.append(
                _build_anomaly(
                    anomaly_type="revenue_below_trend",
                    title="Revenue is below historical trend.",
                    severity="high",
                    metric="revenue",
                    value=round(current, 2),
                    period=period,
                    reason=(
                        "Latest revenue is materially below the recent historical baseline."
                    ),
                    recommended_action=(
                        "Compare the latest period against marketing, sales, churn, and seasonality."
                    ),
                )
            )

    return anomalies


def detect_expense_anomalies(
    monthly_series: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    anomalies = []

    if len(monthly_series) < 2:
        return anomalies

    previous = _to_float(monthly_series[-2].get("expenses"))
    current = _to_float(monthly_series[-1].get("expenses"))
    change = round(_percent_change(previous, current), 2)
    period = _latest_period(monthly_series)

    if change >= 20:
        severity = _severity_from_percent_increase(change)

        anomalies.append(
            _build_anomaly(
                anomaly_type="expense_spike",
                title="Expenses increased sharply.",
                severity=severity,
                metric="expense_growth_percent",
                value=change,
                period=period,
                reason=f"Expenses increased by {change}% compared with the previous period.",
                recommended_action=(
                    "Audit payroll, software, marketing, fees, and one-time costs before the next billing cycle."
                ),
            )
        )

    if len(monthly_series) >= 4:
        expense_values = _series_values(monthly_series[:-1], "expenses")
        baseline = mean(expense_values)
        volatility = pstdev(expense_values) if len(expense_values) > 1 else 0

        if volatility > 0 and current > baseline + (1.5 * volatility):
            anomalies.append(
                _build_anomaly(
                    anomaly_type="expenses_above_trend",
                    title="Expenses are above historical trend.",
                    severity="high",
                    metric="expenses",
                    value=round(current, 2),
                    period=period,
                    reason=(
                        "Latest expenses are materially above the recent historical baseline."
                    ),
                    recommended_action=(
                        "Separate recurring expenses from one-time expenses and cut low-ROI spending."
                    ),
                )
            )

    return anomalies


def detect_profit_anomalies(
    monthly_series: list[dict[str, Any]],
    core_kpis: dict[str, Any],
) -> list[dict[str, Any]]:
    anomalies = []

    profit_available = _flag_enabled(core_kpis, "profit_available", True)
    margin_available = _flag_enabled(core_kpis, "profit_margin_available", profit_available)

    if profit_available and len(monthly_series) >= 2:
        previous = _to_float(monthly_series[-2].get("profit"))
        current = _to_float(monthly_series[-1].get("profit"))
        change = round(_percent_change(previous, current), 2)
        period = _latest_period(monthly_series)

        if change <= -15:
            severity = _severity_from_percent_drop(change)

            anomalies.append(
                _build_anomaly(
                    anomaly_type="profit_drop",
                    title="Profit dropped significantly.",
                    severity=severity,
                    metric="profit_growth_percent",
                    value=change,
                    period=period,
                    reason=f"Profit changed by {change}% compared with the previous period.",
                    recommended_action=(
                        "Identify whether the drop came from revenue weakness, expense growth, discounting, or churn."
                    ),
                )
            )

        if current < 0:
            anomalies.append(
                _build_anomaly(
                    anomaly_type="negative_profit",
                    title="Profit is negative.",
                    severity="critical",
                    metric="profit",
                    value=round(current, 2),
                    period=period,
                    reason="The latest period generated a negative profit.",
                    recommended_action=(
                        "Freeze non-essential spend and create a near-term profitability recovery plan."
                    ),
                )
            )

    profit_margin = _to_float(core_kpis.get("profit_margin_percent"))

    if margin_available and profit_margin < 10:
        anomalies.append(
            _build_anomaly(
                anomaly_type="thin_margin",
                title="Profit margin is weak.",
                severity="high" if profit_margin < 5 else "medium",
                metric="profit_margin_percent",
                value=round(profit_margin, 2),
                reason="Profit margin is below a healthy operating range.",
                recommended_action=(
                    "Review pricing, direct costs, marketing efficiency, and operational expenses."
                ),
            )
        )

    return anomalies


def detect_customer_anomalies(
    advanced_kpis: dict[str, Any],
) -> list[dict[str, Any]]:
    anomalies = []

    churn_available = _flag_enabled(advanced_kpis, "churn_available", True)
    customers = _to_float(advanced_kpis.get("customers"))
    new_customers = _to_float(advanced_kpis.get("new_customers"))
    churned_customers = _to_float(advanced_kpis.get("churned_customers"))
    churn_rate = _to_float(advanced_kpis.get("churn_rate_percent")) if churn_available else 0.0

    if churn_available and churn_rate >= 20:
        severity = "critical"
    elif churn_available and churn_rate >= 12:
        severity = "high"
    elif churn_available and churn_rate >= 7:
        severity = "medium"
    else:
        severity = ""

    if severity:
        anomalies.append(
            _build_anomaly(
                anomaly_type="high_churn",
                title="Churn is elevated.",
                severity=severity,
                metric="churn_rate_percent",
                value=round(churn_rate, 2),
                reason=(
                    "Customer loss is high enough to threaten growth quality and acquisition efficiency."
                ),
                recommended_action=(
                    "Analyze cancellation reasons, onboarding quality, support tickets, and product usage."
                ),
            )
        )

    if churn_available and new_customers > 0 and churned_customers > new_customers * 0.5:
        anomalies.append(
            _build_anomaly(
                anomaly_type="churn_vs_acquisition_risk",
                title="Customer losses are high relative to new customers.",
                severity="high",
                metric="churned_customers_vs_new_customers",
                value={
                    "new_customers": round(new_customers, 2),
                    "churned_customers": round(churned_customers, 2),
                    "customers": round(customers, 2),
                },
                reason=(
                    "Churned customers are more than 50% of newly acquired customers."
                ),
                recommended_action=(
                    "Prioritize retention before scaling acquisition spend further."
                ),
            )
        )

    customer_series = advanced_kpis.get("customer_series")

    if isinstance(customer_series, list) and len(customer_series) >= 2:
        previous = _to_float(customer_series[-2].get("customers"))
        current = _to_float(customer_series[-1].get("customers"))
        change = round(_percent_change(previous, current), 2)

        if change <= -10:
            anomalies.append(
                _build_anomaly(
                    anomaly_type="customer_base_drop",
                    title="Customer base dropped.",
                    severity=_severity_from_percent_drop(change),
                    metric="customer_growth_percent",
                    value=change,
                    period=str(customer_series[-1].get("period", "")),
                    reason="Customer base declined compared with the previous period.",
                    recommended_action=(
                        "Review churn, acquisition quality, pricing changes, and recent product issues."
                    ),
                )
            )

    return anomalies


def detect_marketing_anomalies(
    advanced_kpis: dict[str, Any],
) -> list[dict[str, Any]]:
    anomalies = []

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

    if roas_available and ad_spend > 0 and roas > 0 and roas < 1.5:
        severity = "critical" if roas < 1 else "high"

        anomalies.append(
            _build_anomaly(
                anomaly_type="low_roas",
                title="Marketing ROAS is weak.",
                severity=severity,
                metric="roas",
                value=round(roas, 2),
                reason="Advertising return is below a healthy threshold.",
                recommended_action=(
                    "Pause low-performing campaigns and reallocate budget to profitable channels."
                ),
            )
        )

    if cac_available and revenue_per_customer_available and cac > 0 and revenue_per_customer > 0:
        cac_ratio = cac / revenue_per_customer

        if cac_ratio >= 1:
            anomalies.append(
                _build_anomaly(
                    anomaly_type="high_cac",
                    title="CAC may be too high.",
                    severity="critical" if cac_ratio >= 1.5 else "high",
                    metric="cac_to_revenue_per_customer_ratio",
                    value=round(cac_ratio, 2),
                    reason=(
                        "Customer acquisition cost is too high compared with revenue per customer."
                    ),
                    recommended_action=(
                        "Improve targeting, conversion rates, onboarding, pricing, or retention before scaling spend."
                    ),
                )
            )

    return anomalies


def detect_cashflow_anomalies(
    core_kpis: dict[str, Any],
    forecast: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    anomalies = []

    forecast = forecast or {}
    cashflow_available = _flag_enabled(core_kpis, "cashflow_available", True)
    cashflow_status = str(core_kpis.get("cashflow_status") or "").lower()
    forecast_cashflow_risk = str(forecast.get("cashflow_risk") or "").lower()

    if cashflow_available and cashflow_status == "negative":
        anomalies.append(
            _build_anomaly(
                anomaly_type="negative_cashflow",
                title="Cashflow is negative.",
                severity="critical",
                metric="cashflow_status",
                value=cashflow_status,
                reason="The business is not generating positive net cashflow.",
                recommended_action=(
                    "Reduce non-essential expenses and review pricing, collections, and margins."
                ),
            )
        )

    if forecast_cashflow_risk in {"high", "critical"}:
        anomalies.append(
            _build_anomaly(
                anomaly_type="forecast_cashflow_risk",
                title="Forecast indicates cashflow risk.",
                severity="critical" if forecast_cashflow_risk == "critical" else "high",
                metric="forecast_cashflow_risk",
                value=forecast_cashflow_risk,
                reason="Forecasting engine indicates elevated future cashflow risk.",
                recommended_action=(
                    "Prepare a cash preservation plan and monitor weekly revenue/expense movements."
                ),
            )
        )

    return anomalies


def detect_business_anomalies(
    result: dict[str, Any] | None = None,
    detected_kpis: dict[str, Any] | None = None,
    forecast: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Deterministic anomaly detection for the Business Agent.

    Designed for:
    - deterministic business rules
    - dashboards
    - CEO weekly reports
    - future alerting system
    """

    result = result or {}
    detected_kpis = detected_kpis or {}

    core_kpis = detected_kpis.get("core_kpis") or result.get("kpis") or {}
    advanced_kpis = detected_kpis.get("advanced_kpis") or result.get("advanced_kpis") or {}
    monthly_series = detected_kpis.get("monthly_series") or result.get("monthly_series") or []
    forecast = forecast or result.get("forecast") or {}

    anomalies = []

    if isinstance(monthly_series, list):
        anomalies.extend(detect_revenue_anomalies(monthly_series))

        if _flag_enabled(core_kpis, "expenses_available", True) and _series_has_positive_values(monthly_series, "expenses"):
            anomalies.extend(detect_expense_anomalies(monthly_series))

        if _flag_enabled(core_kpis, "profit_available", True):
            anomalies.extend(detect_profit_anomalies(monthly_series, core_kpis))
        else:
            anomalies.extend(detect_profit_anomalies([], core_kpis))

    anomalies.extend(detect_customer_anomalies(advanced_kpis))
    anomalies.extend(detect_marketing_anomalies(advanced_kpis))
    anomalies.extend(detect_cashflow_anomalies(core_kpis, forecast))

    anomalies = sorted(
        anomalies,
        key=lambda item: item.get("impact_score", 0),
        reverse=True,
    )

    critical_count = sum(1 for item in anomalies if item.get("severity") == "critical")
    high_count = sum(1 for item in anomalies if item.get("severity") == "high")
    medium_count = sum(1 for item in anomalies if item.get("severity") == "medium")

    if critical_count:
        status = "critical"
    elif high_count:
        status = "high_risk"
    elif medium_count:
        status = "watch"
    elif anomalies:
        status = "low_risk"
    else:
        status = "normal"

    return {
        "available": True,
        "status": status,
        "total": len(anomalies),
        "critical_count": critical_count,
        "high_count": high_count,
        "medium_count": medium_count,
        "items": anomalies,
        "source": "business_risk_engine",
    }


def attach_business_anomalies(
    result: dict[str, Any],
    detected_kpis: dict[str, Any],
    forecast: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Mutates and returns result with business risk detection.
    """

    result["anomalies"] = detect_business_anomalies(
        result=result,
        detected_kpis=detected_kpis,
        forecast=forecast,
    )

    return result
