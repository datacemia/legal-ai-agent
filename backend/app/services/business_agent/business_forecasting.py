from collections import defaultdict
from datetime import date, datetime
from typing import Any


def _safe_float(value: Any) -> float:
    if value is None:
        return 0.0

    if isinstance(value, bool):
        return 0.0

    if isinstance(value, (int, float)):
        return float(value)

    text = str(value).strip()

    if not text:
        return 0.0

    negative = False

    if text.startswith("(") and text.endswith(")"):
        negative = True
        text = text[1:-1]

    text = (
        text.replace("$", "")
        .replace("€", "")
        .replace("£", "")
        .replace("MAD", "")
        .replace("DH", "")
        .replace("dhs", "")
        .replace(" ", "")
        .strip()
    )

    if "," in text and "." in text:
        text = text.replace(",", "")
    elif "," in text and "." not in text:
        text = text.replace(",", ".")

    try:
        number = float(text)
        return -number if negative else number
    except ValueError:
        return 0.0


def _format_period(value: Any) -> str:
    if value is None:
        return "Unknown"

    if isinstance(value, datetime):
        return value.strftime("%Y-%m")

    if isinstance(value, date):
        return value.strftime("%Y-%m")

    text = str(value).strip()

    if not text:
        return "Unknown"

    # Try common date formats.
    known_formats = [
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%d/%m/%Y",
        "%m/%d/%Y",
        "%Y-%m",
        "%m-%Y",
        "%d-%m-%Y",
    ]

    for fmt in known_formats:
        try:
            parsed = datetime.strptime(text, fmt)
            return parsed.strftime("%Y-%m")
        except ValueError:
            continue

    return text[:30]


def _sort_periods(periods: list[str]) -> list[str]:
    def sort_key(period: str):
        try:
            return datetime.strptime(period, "%Y-%m")
        except ValueError:
            return period

    return sorted(periods, key=sort_key)


def build_monthly_financial_series(
    rows: list[dict[str, Any]] | None,
    column_mapping: dict[str, str] | None,
) -> list[dict[str, float | str]]:
    """
    Build monthly revenue / expenses / profit series from parsed rows.
    """

    if not rows or not column_mapping:
        return []

    date_column = column_mapping.get("date")
    revenue_column = column_mapping.get("revenue")
    expense_column = column_mapping.get("expense")

    if not date_column or not revenue_column:
        return []

    grouped: dict[str, dict[str, float]] = defaultdict(
        lambda: {
            "revenue": 0.0,
            "expenses": 0.0,
        }
    )

    for row in rows:
        period = _format_period(row.get(date_column))

        if period == "Unknown":
            continue

        grouped[period]["revenue"] += _safe_float(
            row.get(revenue_column)
        )

        if expense_column:
            grouped[period]["expenses"] += _safe_float(
                row.get(expense_column)
            )

    if not grouped:
        return []

    periods = _sort_periods(list(grouped.keys()))

    series = []

    for period in periods:
        revenue = grouped[period]["revenue"]
        expenses = grouped[period]["expenses"]
        profit = revenue - expenses

        series.append(
            {
                "period": period,
                "revenue": round(revenue, 2),
                "expenses": round(expenses, 2),
                "profit": round(profit, 2),
            }
        )

    return series


def _growth_rate(previous: float, current: float) -> float:
    if previous == 0:
        return 0.0

    return ((current - previous) / previous) * 100


def _average(values: list[float]) -> float:
    if not values:
        return 0.0

    return sum(values) / len(values)


def _detect_trend(values: list[float]) -> str:
    if len(values) < 2:
        return "unknown"

    first = values[0]
    last = values[-1]

    if first == 0 and last == 0:
        return "flat"

    change = _growth_rate(first, last)

    if change > 10:
        return "up"

    if change < -10:
        return "down"

    return "flat"


def _detect_cashflow_risk(
    monthly_series: list[dict[str, Any]],
) -> str:
    if not monthly_series:
        return "unknown"

    last = monthly_series[-1]

    revenue = float(last.get("revenue", 0) or 0)
    expenses = float(last.get("expenses", 0) or 0)
    profit = float(last.get("profit", 0) or 0)

    if revenue <= 0 and expenses > 0:
        return "high"

    if profit < 0 and expenses >= revenue:
        return "high"

    if revenue > 0:
        expense_ratio = expenses / revenue

        if expense_ratio >= 0.9:
            return "medium"

    return "low"


def _detect_volatility(values: list[float]) -> str:
    if len(values) < 3:
        return "unknown"

    avg = _average(values)

    if avg == 0:
        return "unknown"

    max_value = max(values)
    min_value = min(values)

    spread = (max_value - min_value) / avg

    if spread >= 0.75:
        return "high"

    if spread >= 0.35:
        return "medium"

    return "low"


def forecast_business_performance(
    rows: list[dict[str, Any]] | None,
    column_mapping: dict[str, str] | None,
) -> dict[str, Any]:
    """
    Simple deterministic forecasting engine.

    This is intentionally conservative.
    It avoids fake precision and returns unavailable when data is insufficient.
    """

    monthly_series = build_monthly_financial_series(
        rows=rows,
        column_mapping=column_mapping,
    )

    if len(monthly_series) < 3:
        return {
            "available": False,
            "next_month_revenue": 0,
            "next_quarter_revenue": 0,
            "trend": "unknown",
            "growth_rate_percent": 0,
            "cashflow_risk": "unknown",
            "volatility": "unknown",
            "monthly_series": monthly_series,
            "explanation": "Forecast requires at least 3 dated revenue periods.",
        }

    revenues = [
        float(item.get("revenue", 0) or 0)
        for item in monthly_series
    ]

    last_revenue = revenues[-1]
    previous_revenue = revenues[-2]

    recent_values = revenues[-3:]

    recent_average = _average(recent_values)

    latest_growth = _growth_rate(
        previous=previous_revenue,
        current=last_revenue,
    )

    # Conservative forecast:
    # 70% last month + 30% recent average, then apply capped recent growth.
    capped_growth = max(min(latest_growth, 25), -25) / 100

    baseline = (last_revenue * 0.7) + (recent_average * 0.3)

    next_month_revenue = baseline * (1 + capped_growth)

    next_month_revenue = max(next_month_revenue, 0)

    next_quarter_revenue = next_month_revenue * 3

    trend = _detect_trend(recent_values)

    cashflow_risk = _detect_cashflow_risk(monthly_series)

    volatility = _detect_volatility(revenues)

    explanation = (
        "Forecast is based on recent monthly revenue, capped growth, "
        "and a conservative weighted average. It should be treated as "
        "directional, not guaranteed."
    )

    return {
        "available": True,
        "next_month_revenue": round(next_month_revenue, 2),
        "next_quarter_revenue": round(next_quarter_revenue, 2),
        "trend": trend,
        "growth_rate_percent": round(latest_growth, 2),
        "cashflow_risk": cashflow_risk,
        "volatility": volatility,
        "monthly_series": monthly_series,
        "explanation": explanation,
    }
