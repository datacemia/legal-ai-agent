from collections import defaultdict
from datetime import date, datetime
from typing import Any
import re


NON_BUSINESS_CATEGORIES = {
    "",
    "unknown",
    "uncategorized",
    "none",
    "null",
    "nan",
    "n/a",
    "na",
    "غير_معروف",
    "غير معروف",
    "sans categorie",
    "sans catégorie",
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
    "ca",
    "revenu",
    "revenus",
    "ventes",
    "vente",
    "recettes",
    "chiffre affaires",
    "chiffre d affaires",
    "chiffre_affaires",
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
    "fee",
    "fees",
    "charge",
    "charges",
    "depense",
    "depenses",
    "dépense",
    "dépenses",
    "cout",
    "couts",
    "coût",
    "coûts",
    "frais",
    "paiement",
    "مصروف",
    "مصروفات",
    "تكلفة",
    "تكاليف",
    "نفقات",
}

TECHNICAL_CATEGORY_KEYWORDS = {
    "id",
    "uuid",
    "guid",
    "hash",
    "token",
    "key",
    "session",
    "interaction",
    "purchase",
    "transaction",
    "order",
    "customer",
    "user",
    "client",
    "buyer",
    "account",
}

UUID_PATTERN = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
    re.IGNORECASE,
)

HEX_LIKE_PATTERN = re.compile(r"^[0-9a-f]{16,}$", re.IGNORECASE)


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


def _normalize_column_name(value: Any) -> str:
    return _normalize_label(value).replace(" ", "_")


def _get_column(column_mapping: dict[str, str], *keys: str) -> str | None:
    for key in keys:
        value = column_mapping.get(key)

        if value:
            return value

    return None


def _safe_float(value: Any) -> float:
    """
    Convert common spreadsheet values to float safely.

    Supports global formats:
    - 1200
    - "1,200.50"
    - "$1,200.50"
    - "1 200,50"
    - "1.200,50"
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

    if "-" in text:
        negative = True
        text = text.replace("-", "")

    text = (
        text.replace("$", "")
        .replace("€", "")
        .replace("£", "")
        .replace("MAD", "")
        .replace("DH", "")
        .replace("DHS", "")
        .replace("dhs", "")
        .replace("USD", "")
        .replace("EUR", "")
        .replace("GBP", "")
        .replace("CAD", "")
        .replace("AUD", "")
        .replace("د.م", "")
        .replace("درهم", "")
        .replace(" ", "")
        .replace("\u00a0", "")
        .strip()
    )

    text = re.sub(r"[^0-9,.]", "", text)

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
    elif "." in text and "," not in text:
        parts = text.split(".")

        if len(parts) > 2:
            text = text.replace(".", "")
        elif len(parts[-1]) == 3 and len(parts[0]) <= 3:
            text = text.replace(".", "")

    try:
        number = float(text)
        return -number if negative else number
    except ValueError:
        return 0.0


def _format_period(value: Any) -> str:
    """
    Convert date-like values into a stable YYYY-MM period label.
    Supports ISO datetimes with fractional seconds/nanoseconds.
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

    iso_match = re.match(r"^(\d{4})-(\d{2})-(\d{2})", text)

    if iso_match:
        return f"{iso_match.group(1)}-{iso_match.group(2)}"

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


def _looks_like_uuid_or_hash(value: Any) -> bool:
    text = str(value or "").strip()

    if not text:
        return False

    if UUID_PATTERN.match(text):
        return True

    compact = text.replace("-", "").replace("_", "")

    if HEX_LIKE_PATTERN.match(compact):
        return True

    return False


def _is_technical_category_column(column_name: Any) -> bool:
    normalized = _normalize_column_name(column_name)

    if not normalized:
        return False

    if normalized in {
        "id",
        "uuid",
        "guid",
        "product_id",
        "user_id",
        "customer_id",
        "client_id",
        "order_id",
        "purchase_id",
        "transaction_id",
        "session_id",
        "interaction_id",
        "invoice_id",
        "receipt_id",
        "account_id",
        "buyer_id",
    }:
        return True

    return normalized.endswith("_id") or any(
        token in normalized.split("_")
        for token in {"uuid", "guid", "hash"}
    )


def _is_usable_category(value: Any, column_name: Any | None = None) -> bool:
    normalized = _normalize_label(value)

    if normalized in NON_BUSINESS_CATEGORIES:
        return False

    if not normalized:
        return False

    if _looks_like_uuid_or_hash(value):
        return False

    if column_name and _is_technical_category_column(column_name):
        return False

    # Avoid labels that are mostly technical IDs or pure numbers.
    compact = normalized.replace(" ", "")

    if compact.isdigit():
        return False

    return True


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


def _has_positive_values(
    rows: list[dict[str, Any]],
    column: str | None,
) -> bool:
    if not column:
        return False

    return any(_safe_float(row.get(column)) > 0 for row in rows)


def _build_time_series_chart(
    rows: list[dict[str, Any]],
    column_mapping: dict[str, str],
    title: str,
    y_key: str,
    source_column: str,
) -> dict[str, Any] | None:
    date_column = _get_column(column_mapping, "date")
    value_column = _get_column(column_mapping, source_column)

    if not date_column or not value_column:
        return None

    grouped: dict[str, float] = defaultdict(float)

    for row in rows:
        period = _format_period(row.get(date_column))

        if period == "Unknown":
            continue

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

    if not any(item.get(y_key, 0) for item in data):
        return None

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
    date_column = _get_column(column_mapping, "date")
    revenue_column = _get_column(column_mapping, "revenue")
    expense_column = _get_column(column_mapping, "expenses", "expense")
    profit_column = _get_column(column_mapping, "profit")

    if not date_column or not revenue_column:
        return None

    if not profit_column and not expense_column:
        # Do not invent profit when neither profit nor expenses/costs exist.
        return None

    grouped: dict[str, dict[str, float]] = defaultdict(
        lambda: {
            "revenue": 0.0,
            "expenses": 0.0,
            "profit": 0.0,
        }
    )

    for row in rows:
        period = _format_period(row.get(date_column))

        if period == "Unknown":
            continue

        revenue = _safe_float(row.get(revenue_column))
        expenses = _safe_float(row.get(expense_column)) if expense_column else 0.0
        explicit_profit = _safe_float(row.get(profit_column)) if profit_column else None

        grouped[period]["revenue"] += revenue
        grouped[period]["expenses"] += expenses

        if explicit_profit is not None:
            grouped[period]["profit"] += explicit_profit
        else:
            grouped[period]["profit"] += revenue - expenses

    if not grouped:
        return None

    periods = _sort_periods(list(grouped.keys()))

    data = []

    for period in periods:
        item = grouped[period]

        data.append(
            {
                "period": period,
                "profit": round(item["profit"], 2),
                "revenue": round(item["revenue"], 2),
                "expenses": round(item["expenses"], 2),
            }
        )

    if not any(item.get("profit", 0) for item in data):
        return None

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
    category_column = _get_column(column_mapping, "category")
    expense_column = _get_column(column_mapping, "expenses", "expense")

    if not category_column or not expense_column:
        return None

    if _is_technical_category_column(category_column):
        return None

    grouped: dict[str, float] = defaultdict(float)

    for row in rows:
        raw_category = row.get(category_column)
        category = _clean_label(raw_category)

        if not _is_usable_category(category, category_column):
            continue

        # Strict rule:
        # Do not show "Revenue" as an expense category.
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
    category_column = _get_column(column_mapping, "category")
    revenue_column = _get_column(column_mapping, "revenue")

    if not category_column or not revenue_column:
        return None

    if _is_technical_category_column(category_column):
        return None

    grouped: dict[str, float] = defaultdict(float)

    for row in rows:
        raw_category = row.get(category_column)
        category = _clean_label(raw_category)

        if not _is_usable_category(category, category_column):
            continue

        # Strict rule:
        # A row category called "Revenue", "Sales", etc. is not a useful
        # revenue breakdown. Revenue by category should only show real
        # products/channels/sources/categories.
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
    date_column = _get_column(column_mapping, "date")
    revenue_column = _get_column(column_mapping, "revenue")
    expense_column = _get_column(column_mapping, "expenses", "expense")
    cashflow_column = _get_column(column_mapping, "cashflow", "cash_flow")

    if not date_column:
        return None

    if cashflow_column:
        return _build_time_series_chart(
            rows=rows,
            column_mapping={**column_mapping, "cashflow": cashflow_column},
            title="Cashflow Trend",
            y_key="cashflow",
            source_column="cashflow",
        )

    if not revenue_column or not expense_column:
        # Do not invent cashflow when costs/expenses are absent.
        return None

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

    if not any(item.get("cashflow", 0) for item in data):
        return None

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

    Global rules:
    - Support both "expense" and "expenses" mappings.
    - Do not show technical IDs / UUIDs as business categories.
    - Do not invent profit or cashflow charts when costs are unavailable.
    - Keep chart keys deterministic for frontend and translation layers.
    - Return only charts that have meaningful data.
    """

    if not rows or not column_mapping:
        return []

    revenue_column = _get_column(column_mapping, "revenue")
    expense_column = _get_column(column_mapping, "expenses", "expense")

    charts: list[dict[str, Any]] = []

    chart_builders = [
        lambda: _build_time_series_chart(
            rows=rows,
            column_mapping=column_mapping,
            title="Revenue Trend",
            y_key="revenue",
            source_column="revenue",
        ) if revenue_column else None,
        lambda: _build_time_series_chart(
            rows=rows,
            column_mapping={**column_mapping, "expenses": expense_column} if expense_column else column_mapping,
            title="Expense Trend",
            y_key="expenses",
            source_column="expenses",
        ) if expense_column and _has_positive_values(rows, expense_column) else None,
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
