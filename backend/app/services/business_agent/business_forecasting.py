from collections import defaultdict
from datetime import date, datetime
from typing import Any
import re


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
        .replace("USD", "")
        .replace("EUR", "")
        .replace("CAD", "")
        .replace("AUD", "")
        .replace("AED", "")
        .replace("SAR", "")
        .replace(" ", "")
        .strip()
    )

    text = re.sub(r"[^0-9,\.\-]", "", text)

    if not text:
        return 0.0

    if "," in text and "." in text:
        last_comma = text.rfind(",")
        last_dot = text.rfind(".")

        if last_comma > last_dot:
            text = text.replace(".", "").replace(",", ".")
        else:
            text = text.replace(",", "")
    elif "," in text and "." not in text:
        parts = text.split(",")
        if len(parts[-1]) in {1, 2}:
            text = text.replace(",", ".")
        else:
            text = text.replace(",", "")

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

    # Accept ISO datetimes with time / fractional seconds, including nanoseconds
    # such as "2023-01-15 18:05:44.055402424".
    iso_date_match = re.match(r"^(\d{4})-(\d{2})-(\d{2})", text)

    if iso_date_match:
        return f"{iso_date_match.group(1)}-{iso_date_match.group(2)}"

    known_formats = [
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%d/%m/%Y",
        "%m/%d/%Y",
        "%Y-%m",
        "%m-%Y",
        "%d-%m-%Y",
        "%Y.%m.%d",
    ]

    for fmt in known_formats:
        try:
            parsed = datetime.strptime(text, fmt)
            return parsed.strftime("%Y-%m")
        except ValueError:
            continue

    if re.match(r"^\d{4}-\d{2}$", text):
        return text

    if len(text) <= 20 and re.search(r"\d{4}", text):
        return text

    return "Unknown"


def _sort_periods(periods: list[str]) -> list[str]:
    def sort_key(period: str):
        try:
            return datetime.strptime(period, "%Y-%m")
        except ValueError:
            return period

    return sorted(periods, key=sort_key)


def _get_mapped_column(
    column_mapping: dict[str, str],
    *keys: str,
) -> str | None:
    for key in keys:
        value = column_mapping.get(key)

        if value:
            return value

    return None


def build_monthly_financial_series(
    rows: list[dict[str, Any]] | None,
    column_mapping: dict[str, str] | None,
) -> list[dict[str, float | str]]:
    """
    Build monthly revenue / expenses / profit series from parsed rows.

    Supports both legacy mapping key "expense" and current canonical key
    "expenses" so global datasets do not lose cost data.
    """

    if not rows or not column_mapping:
        return []

    date_column = _get_mapped_column(column_mapping, "date", "period", "month")
    revenue_column = _get_mapped_column(column_mapping, "revenue", "sales", "amount")
    expense_column = _get_mapped_column(column_mapping, "expenses", "expense", "cost", "costs")
    profit_column = _get_mapped_column(column_mapping, "profit", "net_profit", "gross_profit")

    if not date_column or not revenue_column:
        return []

    grouped: dict[str, dict[str, float]] = defaultdict(
        lambda: {
            "revenue": 0.0,
            "expenses": 0.0,
            "profit": 0.0,
        }
    )

    has_expenses = bool(expense_column)
    has_profit = bool(profit_column)

    for row in rows:
        period = _format_period(row.get(date_column))

        if period == "Unknown":
            continue

        grouped[period]["revenue"] += _safe_float(row.get(revenue_column))

        if expense_column:
            grouped[period]["expenses"] += _safe_float(row.get(expense_column))

        if profit_column:
            grouped[period]["profit"] += _safe_float(row.get(profit_column))

    if not grouped:
        return []

    periods = _sort_periods(list(grouped.keys()))

    series = []

    for period in periods:
        revenue = grouped[period]["revenue"]
        expenses = grouped[period]["expenses"]

        if has_profit:
            profit = grouped[period]["profit"]
        elif has_expenses:
            profit = revenue - expenses
        else:
            # Revenue-only datasets cannot verify profitability.
            profit = 0.0

        item: dict[str, float | str] = {
            "period": period,
            "revenue": round(revenue, 2),
            "expenses": round(expenses, 2),
            "profit": round(profit, 2),
            "profit_available": has_profit or has_expenses,
            "expenses_available": has_expenses,
        }

        series.append(item)

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

    if not last.get("expenses_available"):
        return "unknown"

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
