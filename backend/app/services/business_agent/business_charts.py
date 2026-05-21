from collections import defaultdict
from datetime import date, datetime
from typing import Any


NON_BUSINESS_CATEGORIES = {
    "",
    "unknown",
    "uncategorized",
    "none",
    "null",
}

REVENUE_CATEGORY_LABELS = {
    "revenue",
    "revenues",
    "sales",
    "sale",
    "income",
    "turnover",
    "gross sales",
    "net sales",
    "total sales",
    "revenu",
    "revenus",
    "ventes",
    "vente",
    "recettes",
    "chiffre affaires",
    "chiffre d affaires",
    "إيراد",
    "إيرادات",
    "مبيعات",
    "دخل",
}

EXPENSE_CATEGORY_LABELS = {
    "expense",
    "expenses",
    "cost",
    "costs",
    "spend",
    "spending",
    "paid",
    "payment",
    "depense",
    "depenses",
    "dépense",
    "dépenses",
    "cout",
    "couts",
    "coût",
    "coûts",
    "مصروف",
    "مصروفات",
    "تكلفة",
    "تكاليف",
    "نفقات",
}


def _normalize_label(value: Any) -> str:
    text = str(value or "").strip().lower()

    replacements = {
        "_": " ",
        "-": " ",
        "é": "e",
        "è": "e",
        "ê": "e",
        "ë": "e",
        "à": "a",
        "â": "a",
        "ù": "u",
        "û": "u",
        "ô": "o",
        "î": "i",
        "ï": "i",
        "ç": "c",
    }

    for source, target in replacements.items():
        text = text.replace(source, target)

    text = " ".join(text.split())

    return text


def _safe_float(value: Any) -> float:
    """
    Convert common spreadsheet values to float safely.

    Supports:
    - 1200
    - "1,200.50"
    - "$1,200.50"
    - "1 200,50"
    - "(1200.50)"
    """

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
    """
    Convert date-like values into a stable period label.
    """

    if value is None:
        return "Unknown"

    if isinstance(value, datetime):
        return value.strftime("%Y-%m")

    if isinstance(value, date):
        return value.strftime("%Y-%m")

    text = str(value).strip()

    if not text:
        return "Unknown"

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

    return text[:30]


def _clean_label(value: Any) -> str:
    if value is None:
        return "Uncategorized"

    text = str(value).strip()

    if not text:
        return "Uncategorized"

    return text[:60]


def _is_revenue_category(value: Any) -> bool:
    normalized = _normalize_label(value)

    return normalized in {
        _normalize_label(label)
        for label in REVENUE_CATEGORY_LABELS
    }


def _is_expense_category(value: Any) -> bool:
    normalized = _normalize_label(value)

    return normalized in {
        _normalize_label(label)
        for label in EXPENSE_CATEGORY_LABELS
    }


def _is_usable_category(value: Any) -> bool:
    normalized = _normalize_label(value)

    if normalized in NON_BUSINESS_CATEGORIES:
        return False

    return bool(normalized)


def _sort_periods(periods: list[str]) -> list[str]:
    """
    Sort YYYY-MM labels chronologically when possible.
    Fallback to normal string sort.
    """

    def sort_key(period: str):
        try:
            return datetime.strptime(period, "%Y-%m")
        except ValueError:
            return period

    return sorted(periods, key=sort_key)


def _build_time_series_chart(
    rows: list[dict[str, Any]],
    column_mapping: dict[str, str],
    title: str,
    y_key: str,
    source_column: str,
) -> dict[str, Any] | None:
    date_column = column_mapping.get("date")
    value_column = column_mapping.get(source_column)

    if not date_column or not value_column:
        return None

    grouped: dict[str, float] = defaultdict(float)

    for row in rows:
        period = _format_period(row.get(date_column))
        grouped[period] += _safe_float(row.get(value_column))

    if not grouped:
        return None

    periods = _sort_periods(list(grouped.keys()))

    data = [
        {
            "period": period,
            y_key: round(grouped[period], 2),
        }
        for period in periods
    ]

    return {
        "type": "line",
        "title": title,
        "x_key": "period",
        "y_key": y_key,
        "data": data,
    }


def _build_profit_chart(
    rows: list[dict[str, Any]],
    column_mapping: dict[str, str],
) -> dict[str, Any] | None:
    date_column = column_mapping.get("date")
    revenue_column = column_mapping.get("revenue")
    expense_column = column_mapping.get("expense")

    if not date_column or not revenue_column or not expense_column:
        return None

    grouped: dict[str, dict[str, float]] = defaultdict(
        lambda: {
            "revenue": 0.0,
            "expenses": 0.0,
        }
    )

    for row in rows:
        period = _format_period(row.get(date_column))

        grouped[period]["revenue"] += _safe_float(
            row.get(revenue_column)
        )

        grouped[period]["expenses"] += _safe_float(
            row.get(expense_column)
        )

    if not grouped:
        return None

    periods = _sort_periods(list(grouped.keys()))

    data = []

    for period in periods:
        revenue = grouped[period]["revenue"]
        expenses = grouped[period]["expenses"]

        data.append(
            {
                "period": period,
                "profit": round(revenue - expenses, 2),
                "revenue": round(revenue, 2),
                "expenses": round(expenses, 2),
            }
        )

    return {
        "type": "line",
        "title": "Profit Evolution",
        "x_key": "period",
        "y_key": "profit",
        "data": data,
    }


def _build_expenses_by_category_chart(
    rows: list[dict[str, Any]],
    column_mapping: dict[str, str],
) -> dict[str, Any] | None:
    category_column = column_mapping.get("category")
    expense_column = column_mapping.get("expense")

    if not category_column or not expense_column:
        return None

    grouped: dict[str, float] = defaultdict(float)

    for row in rows:
        raw_category = row.get(category_column)
        category = _clean_label(raw_category)

        if not _is_usable_category(category):
            continue

        # Critical strict rule:
        # Do not show "Revenue" as an expense category.
        # This happens in mixed financial transaction files where revenue rows
        # also carry a category label.
        if _is_revenue_category(category):
            continue

        expense_value = _safe_float(row.get(expense_column))

        if expense_value <= 0:
            continue

        grouped[category] += expense_value

    if not grouped:
        return None

    data = [
        {
            "category": category,
            "expenses": round(value, 2),
        }
        for category, value in sorted(
            grouped.items(),
            key=lambda item: item[1],
            reverse=True,
        )
        if value > 0
    ][:12]

    if not data:
        return None

    return {
        "type": "bar",
        "title": "Expenses by Category",
        "x_key": "category",
        "y_key": "expenses",
        "data": data,
    }


def _build_revenue_by_category_chart(
    rows: list[dict[str, Any]],
    column_mapping: dict[str, str],
) -> dict[str, Any] | None:
    category_column = column_mapping.get("category")
    revenue_column = column_mapping.get("revenue")

    if not category_column or not revenue_column:
        return None

    grouped: dict[str, float] = defaultdict(float)

    for row in rows:
        raw_category = row.get(category_column)
        category = _clean_label(raw_category)

        if not _is_usable_category(category):
            continue

        # Strict rule:
        # A row category called "Revenue", "Sales", etc. is not a useful
        # revenue breakdown. It only means "this row is revenue".
        # Revenue by category should only show real products/channels/sources.
        if _is_revenue_category(category) or _is_expense_category(category):
            continue

        revenue_value = _safe_float(row.get(revenue_column))

        if revenue_value <= 0:
            continue

        grouped[category] += revenue_value

    if not grouped:
        return None

    data = [
        {
            "category": category,
            "revenue": round(value, 2),
        }
        for category, value in sorted(
            grouped.items(),
            key=lambda item: item[1],
            reverse=True,
        )
        if value > 0
    ][:12]

    if not data:
        return None

    return {
        "type": "bar",
        "title": "Revenue by Category",
        "x_key": "category",
        "y_key": "revenue",
        "data": data,
    }


def _build_cashflow_chart(
    rows: list[dict[str, Any]],
    column_mapping: dict[str, str],
) -> dict[str, Any] | None:
    date_column = column_mapping.get("date")
    revenue_column = column_mapping.get("revenue")
    expense_column = column_mapping.get("expense")

    if not date_column or not revenue_column or not expense_column:
        return None

    grouped: dict[str, dict[str, float]] = defaultdict(
        lambda: {
            "revenue": 0.0,
            "expenses": 0.0,
        }
    )

    for row in rows:
        period = _format_period(row.get(date_column))

        grouped[period]["revenue"] += _safe_float(row.get(revenue_column))
        grouped[period]["expenses"] += _safe_float(row.get(expense_column))

    if not grouped:
        return None

    periods = _sort_periods(list(grouped.keys()))

    data = []

    for period in periods:
        revenue = grouped[period]["revenue"]
        expenses = grouped[period]["expenses"]
        net_cashflow = revenue - expenses

        data.append(
            {
                "period": period,
                "cashflow": round(net_cashflow, 2),
                "revenue": round(revenue, 2),
                "expenses": round(expenses, 2),
            }
        )

    return {
        "type": "line",
        "title": "Cashflow Trend",
        "x_key": "period",
        "y_key": "cashflow",
        "data": data,
    }


def build_business_charts(
    rows: list[dict[str, Any]] | None,
    column_mapping: dict[str, str] | None,
) -> list[dict[str, Any]]:
    """
    Build frontend-ready chart payloads for the Business Agent.

    Strict rules:
    - Do not show "Revenue" as an expense category.
    - Do not show fake Revenue by Category when category only means transaction type.
    - Keep charts deterministic and backend-calculated.
    - Return only charts that have meaningful data.
    """

    if not rows or not column_mapping:
        return []

    charts: list[dict[str, Any]] = []

    chart_builders = [
        lambda: _build_time_series_chart(
            rows=rows,
            column_mapping=column_mapping,
            title="Revenue Trend",
            y_key="revenue",
            source_column="revenue",
        ),
        lambda: _build_time_series_chart(
            rows=rows,
            column_mapping=column_mapping,
            title="Expense Trend",
            y_key="expenses",
            source_column="expense",
        ),
        lambda: _build_profit_chart(
            rows=rows,
            column_mapping=column_mapping,
        ),
        lambda: _build_cashflow_chart(
            rows=rows,
            column_mapping=column_mapping,
        ),
        lambda: _build_expenses_by_category_chart(
            rows=rows,
            column_mapping=column_mapping,
        ),
        lambda: _build_revenue_by_category_chart(
            rows=rows,
            column_mapping=column_mapping,
        ),
    ]

    seen_titles = set()

    for build_chart in chart_builders:
        chart = build_chart()

        if not chart or not chart.get("data"):
            continue

        title = chart.get("title")

        if title in seen_titles:
            continue

        seen_titles.add(title)
        charts.append(chart)

    return charts
