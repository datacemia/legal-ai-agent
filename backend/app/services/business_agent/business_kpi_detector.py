import re
from collections import defaultdict
from datetime import date, datetime
from typing import Any


BUSINESS_MODELS = {
    "saas": [
        "mrr",
        "arr",
        "subscription",
        "subscriptions",
        "subscriber",
        "subscribers",
        "churn",
        "trial",
        "plan",
        "monthly_recurring",
        "recurring_revenue",
        "abonnement",
        "abonnements",
        "revenu_recurrent",
        "desabonnement",
        "اشتراك",
        "اشتراكات",
        "مكرر",
    ],
    "ecommerce": [
        "order",
        "orders",
        "cart",
        "checkout",
        "sku",
        "product",
        "products",
        "aov",
        "shipping",
        "refund",
        "returns",
        "shopify",
        "woocommerce",
        "commande",
        "commandes",
        "panier",
        "produit",
        "produits",
        "livraison",
        "retour",
        "طلب",
        "طلبات",
        "سلة",
        "منتج",
        "منتجات",
        "شحن",
        "مرتجع",
    ],
    "agency": [
        "client",
        "clients",
        "project",
        "projects",
        "billable",
        "hours",
        "retainer",
        "invoice",
        "service",
        "campaign",
        "deliverable",
        "projet",
        "projets",
        "heures",
        "facture",
        "prestations",
        "عميل",
        "عملاء",
        "مشروع",
        "مشاريع",
        "فاتورة",
        "خدمة",
        "ساعات",
    ],
    "restaurant": [
        "restaurant",
        "menu",
        "table",
        "tables",
        "food",
        "beverage",
        "meal",
        "ticket",
        "reservation",
        "kitchen",
        "ingredient",
        "repas",
        "cuisine",
        "ingredient",
        "reservation",
        "مطعم",
        "قائمة",
        "طاولة",
        "وجبة",
        "مطبخ",
        "مكون",
        "حجز",
    ],
    "marketplace": [
        "gmv",
        "seller",
        "sellers",
        "buyer",
        "buyers",
        "vendor",
        "vendors",
        "commission",
        "take_rate",
        "transaction",
        "transactions",
        "marketplace",
        "vendeur",
        "vendeurs",
        "acheteur",
        "acheteurs",
        "عمولة",
        "معاملة",
        "سوق",
        "بائع",
        "مشتري",
    ],
}


KPI_ALIASES = {
    "date": [
        "date",
        "day",
        "month",
        "period",
        "created_at",
        "transaction_date",
        "order_date",
        "purchase_date",
        "invoice_date",
        "payment_date",
        "checkout_date",
        "booking_date",
        "time",
        "timestamp",
        "jour",
        "mois",
        "periode",
        "période",
        "تاريخ",
        "يوم",
        "شهر",
        "فترة",
    ],
    "revenue": [
        "revenue",
        "sales",
        "sale",
        "income",
        "turnover",
        "gross_sales",
        "net_sales",
        "total_sales",
        "amount",
        "total_amount",
        "order_total",
        "line_total",
        "item_total",
        "subtotal",
        "total",
        "price_total",
        "purchase_amount",
        "payment_amount",
        "gross_amount",
        "net_amount",
        "revenue_amount",
        "vente_totale",
        "montant_total",
        "total_commande",
        "montant_achat",
        "montant_paiement",
        "amount_in",
        "credit",
        "received",
        "payment_received",
        "revenu",
        "revenus",
        "chiffre_affaires",
        "ventes",
        "recettes",
        "encaissement",
        "إيراد",
        "إيرادات",
        "مبيعات",
        "دخل",
        "المداخيل",
        "مداخيل",
    ],
    "expenses": [
        "expense",
        "expenses",
        "cost",
        "costs",
        "spend",
        "spending",
        "amount_out",
        "debit",
        "paid",
        "payment",
        "fees",
        "charge",
        "charges",
        "depense",
        "dépense",
        "depenses",
        "dépenses",
        "cout",
        "coût",
        "couts",
        "coûts",
        "frais",
        "paiement",
        "مصروف",
        "مصروفات",
        "تكلفة",
        "تكاليف",
        "نفقات",
        "دفع",
        "رسوم",
    ],
    "profit": [
        "profit",
        "net_profit",
        "gross_profit",
        "margin",
        "benefit",
        "benefice",
        "bénéfice",
        "marge",
        "resultat",
        "résultat",
        "ربح",
        "أرباح",
        "هامش",
        "صافي_الربح",
    ],
    "category": [
        "category",
        "type",
        "label",
        "description",
        "merchant",
        "vendor",
        "product",
        "service",
        "channel",
        "source",
        "categorie",
        "catégorie",
        "libelle",
        "libellé",
        "fournisseur",
        "produit",
        "canal",
        "فئة",
        "نوع",
        "وصف",
        "تاجر",
        "مورد",
        "منتج",
        "خدمة",
        "قناة",
        "مصدر",
    ],
    "mrr": [
        "mrr",
        "monthly_recurring_revenue",
        "monthly recurring revenue",
        "revenu_recurrent_mensuel",
        "revenu récurrent mensuel",
    ],
    "arr": [
        "arr",
        "annual_recurring_revenue",
        "annual recurring revenue",
        "revenu_recurrent_annuel",
        "revenu récurrent annuel",
    ],
    "churn_rate": [
        "churn_rate",
        "churn percentage",
        "churn_percent",
        "desabonnement_rate",
        "désabonnement_rate",
        "taux_de_churn",
        "taux_churn",
        "taux_de_desabonnement",
        "taux_de_désabonnement",
        "إلغاء_الاشتراك_نسبة",
    ],
    "customers": [
        "customers",
        "customer_count",
        "active_customers",
        "clients",
        "client",
        "client_count",
        "customer",
        "customer_id",
        "user_id",
        "client_id",
        "buyer_id",
        "account_id",
        "member_id",
        "subscriber_id",
        "id_client",
        "utilisateur_id",
        "acheteur_id",
        "utilisateurs",
        "عملاء",
        "زبائن",
    ],
    "new_customers": [
        "new_customers",
        "new_clients",
        "nouveaux_clients",
        "nouveaux_utilisateurs",
        "عملاء_جدد",
    ],
    "churned_customers": [
        "churned_customers",
        "lost_customers",
        "cancelled_customers",
        "clients_perdus",
        "desabonnements",
        "désabonnements",
        "عملاء_مفقودون",
    ],
    "ad_spend": [
        "ad_spend",
        "ads_spend",
        "ad_cost",
        "ads_cost",
        "marketing_spend",
        "marketing_cost",
        "paid_ads",
        "cout_publicitaire",
        "coût_publicitaire",
        "depenses_publicitaires",
        "dépenses_publicitaires",
        "إنفاق_إعلاني",
    ],
    "orders": [
        "orders",
        "order_count",
        "order_id",
        "purchase_id",
        "transaction_id",
        "invoice_id",
        "receipt_id",
        "checkout_id",
        "booking_id",
        "transactions",
        "purchases",
        "commandes",
        "nombre_commandes",
        "طلبات",
    ],
    "conversion_rate": [
        "conversion_rate",
        "conversion",
        "taux_conversion",
        "taux_de_conversion",
    ],
    "gmv": [
        "gmv",
        "gross_merchandise_value",
        "volume_brut",
        "قيمة_البضائع",
    ],
    "take_rate": [
        "take_rate",
        "commission_rate",
        "taux_commission",
        "commission",
    ],
    "billable_hours": [
        "billable_hours",
        "hours",
        "heures_facturables",
        "heures",
        "ساعات",
    ],
}


# Columns that may look financial by name but are profile, demographic,
# segmentation, or reference-table attributes. They must never be treated as
# verified business revenue.
NON_BUSINESS_REVENUE_COLUMNS = {
    "income_level",
    "user_income_level",
    "customer_income_level",
    "household_income",
    "personal_income",
    "annual_income",
    "monthly_income",
    "salary",
    "salary_range",
    "wage",
    "wage_range",
    "income_band",
    "income_bracket",
    "niveau_revenu",
    "niveau_de_revenu",
    "tranche_revenu",
    "salaire",
    "tranche_salaire",
}

# Standalone profile/reference identifiers or dimensions are not performance
# metrics. They can be useful context, but they do not prove revenue, growth,
# churn, customers, or orders by themselves.
NON_PERFORMANCE_IDENTIFIER_COLUMNS = {
    "user_id",
    "customer_id",
    "client_id",
    "member_id",
    "account_id",
    "profile_id",
    "person_id",
    "contact_id",
    "email",
    "phone",
    "name",
    "first_name",
    "last_name",
    "gender",
    "age",
    "country",
    "city",
    "state",
    "region",
    "signup_date",
    "registration_date",
    "created_at",
    "preferred_category",
    "preference",
    "loyalty_tier",
    "segment",
    "income_level",
}

# These columns are profile/customer-list fields. Counting them is not enough
# to calculate customer performance KPIs unless paired with true acquisition,
# churn, retention, order, subscription, or revenue data.
PROFILE_CUSTOMER_COLUMNS = {
    "user_id",
    "customer_id",
    "client_id",
    "member_id",
    "account_id",
    "profile_id",
    "person_id",
    "contact_id",
}

# Product/catalog attributes are not sales performance by themselves.
CATALOG_REFERENCE_COLUMNS = {
    "product_id",
    "sku",
    "product",
    "product_name",
    "name",
    "description",
    "category",
    "preferred_category",
    "subcategory",
    "brand",
    "stock",
    "stock_quantity",
    "inventory",
    "price",
    "list_price",
    "rating",
    "rating_avg",
    "review_count",
}


def normalize_text(value: Any) -> str:
    text = str(value or "").strip().lower()

    replacements = {
        "é": "e",
        "è": "e",
        "ê": "e",
        "ë": "e",
        "à": "a",
        "â": "a",
        "ä": "a",
        "ù": "u",
        "û": "u",
        "ü": "u",
        "ô": "o",
        "ö": "o",
        "î": "i",
        "ï": "i",
        "ç": "c",
    }

    for source, target in replacements.items():
        text = text.replace(source, target)

    text = re.sub(r"[^\w\u0600-\u06FF]+", "_", text, flags=re.UNICODE)
    text = re.sub(r"_+", "_", text).strip("_")

    return text


def is_non_business_revenue_column(column: Any) -> bool:
    normalized = normalize_text(column)

    if normalized in NON_BUSINESS_REVENUE_COLUMNS:
        return True

    # Avoid substring false positives such as "income_level" matching "income".
    profile_suffixes = (
        "_level",
        "_band",
        "_bracket",
        "_range",
        "_tier",
        "_segment",
        "_category",
    )

    if "income" in normalized and any(normalized.endswith(suffix) for suffix in profile_suffixes):
        return True

    if "salary" in normalized and any(normalized.endswith(suffix) for suffix in profile_suffixes):
        return True

    return False


def is_profile_customer_column(column: Any) -> bool:
    return normalize_text(column) in PROFILE_CUSTOMER_COLUMNS


def is_non_performance_identifier_column(column: Any) -> bool:
    return normalize_text(column) in NON_PERFORMANCE_IDENTIFIER_COLUMNS


def has_verified_amount_values(
    rows: list[dict[str, Any]],
    column: str | None,
) -> bool:
    if not column:
        return False

    numeric_values = [
        value
        for row in rows
        for value in [to_float(row.get(column))]
        if value is not None
    ]

    if not numeric_values:
        return False

    # A valid business amount column may legitimately sum to zero, but it must
    # contain numeric amount-like values. Profile labels such as "low"/"high"
    # produce no numeric values and are rejected.
    return True


def has_positive_amount_values(
    rows: list[dict[str, Any]],
    column: str | None,
) -> bool:
    if not column:
        return False

    return any((to_float(row.get(column)) or 0.0) > 0 for row in rows)


def to_float(value: Any) -> float | None:
    if value is None:
        return None

    if isinstance(value, bool):
        return None

    if isinstance(value, (int, float)):
        return float(value)

    text = str(value).strip()

    if not text:
        return None

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

    text = re.sub(r"[^0-9,\.\-]", "", text)

    if not text:
        return None

    if "," in text and "." in text:
        text = text.replace(",", "")
    elif "," in text and "." not in text:
        text = text.replace(",", ".")

    try:
        number = float(text)
        return -number if negative else number
    except ValueError:
        return None


def safe_divide(numerator: float, denominator: float) -> float:
    if denominator == 0:
        return 0.0

    return numerator / denominator


def round_money(value: float) -> float:
    return round(float(value or 0), 2)


def parse_period(value: Any) -> str:
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


def sort_periods(periods: list[str]) -> list[str]:
    def sort_key(period: str):
        try:
            return datetime.strptime(period, "%Y-%m")
        except ValueError:
            return period

    return sorted(periods, key=sort_key)


def resolve_column(
    canonical_name: str,
    columns: list[str],
    column_mapping: dict[str, str] | None = None,
) -> str | None:
    column_mapping = column_mapping or {}

    mapping_aliases = {
        "expenses": ["expenses", "expense"],
        "expense": ["expense", "expenses"],
    }

    for key in [canonical_name] + mapping_aliases.get(canonical_name, []):
        mapped = column_mapping.get(key)

        if mapped:
            if canonical_name == "revenue" and is_non_business_revenue_column(mapped):
                continue

            if canonical_name == "customers" and is_profile_customer_column(mapped):
                continue

            return mapped

    detected = detect_kpi_columns(columns)
    candidate = detected.get(canonical_name)

    if canonical_name == "revenue" and is_non_business_revenue_column(candidate):
        return None

    if canonical_name == "customers" and is_profile_customer_column(candidate):
        return None

    return candidate


def detect_kpi_columns(columns: list[str]) -> dict[str, str]:
    normalized_columns = {
        normalize_text(column): column
        for column in columns
        if column
    }

    detected: dict[str, str] = {}

    for kpi, aliases in KPI_ALIASES.items():
        normalized_aliases = [
            normalize_text(alias)
            for alias in aliases
        ]

        for alias in normalized_aliases:
            if alias in normalized_columns:
                detected[kpi] = normalized_columns[alias]
                break

        if kpi not in detected:
            for normalized_column, original_column in normalized_columns.items():
                if kpi == "revenue" and is_non_business_revenue_column(original_column):
                    continue

                if kpi == "customers" and is_profile_customer_column(original_column):
                    continue

                if kpi in {"revenue", "customers", "orders"}:
                    # For high-impact KPIs, avoid loose substring matches like
                    # income_level -> income or user_id -> user/customer.
                    continue

                if any(
                    alias and alias in normalized_column
                    for alias in normalized_aliases
                ):
                    detected[kpi] = original_column
                    break

    return detected


def looks_like_profile_or_reference_file(columns: list[str]) -> bool:
    normalized = {normalize_text(column) for column in columns if column}

    if not normalized:
        return False

    performance_markers = {
        "revenue",
        "sales",
        "sale",
        "turnover",
        "gross_sales",
        "net_sales",
        "amount",
        "total_amount",
        "order_total",
        "purchase_amount",
        "payment_amount",
        "expenses",
        "expense",
        "cost",
        "costs",
        "profit",
        "cashflow",
        "ad_spend",
        "marketing_spend",
        "mrr",
        "arr",
        "churned_customers",
        "new_customers",
    }

    if normalized.intersection(performance_markers):
        return False

    profile_hits = len(normalized.intersection(NON_PERFORMANCE_IDENTIFIER_COLUMNS))
    catalog_hits = len(normalized.intersection(CATALOG_REFERENCE_COLUMNS))

    return profile_hits >= 2 or catalog_hits >= 2


def detect_business_model_details(
    columns: list[str],
    rows: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    rows = rows or []

    if looks_like_profile_or_reference_file(columns):
        return {
            "business_model": "general",
            "confidence": "low",
            "scores": {
                model: 0
                for model in BUSINESS_MODELS
            },
        }

    text_parts = list(columns)

    for row in rows[:100]:
        text_parts.extend(
            str(value)
            for value in row.values()
            if value is not None
        )

    combined = normalize_text(" ".join(text_parts))

    scores = {
        model: 0
        for model in BUSINESS_MODELS
    }

    for model, keywords in BUSINESS_MODELS.items():
        for keyword in keywords:
            normalized_keyword = normalize_text(keyword)

            if normalized_keyword and normalized_keyword in combined:
                scores[model] += 1

    best_model = max(scores, key=scores.get) if scores else "general"
    best_score = scores.get(best_model, 0)

    if best_score <= 0:
        return {
            "business_model": "general",
            "confidence": "low",
            "scores": scores,
        }

    confidence = "high" if best_score >= 3 else "medium"

    return {
        "business_model": best_model,
        "confidence": confidence,
        "scores": scores,
    }


def detect_business_model(
    columns: list[str],
    rows: list[dict[str, Any]] | None = None,
) -> str:
    """
    Router-compatible helper.

    Returns a string because API responses and frontend expect:
    business_model: "saas" | "ecommerce" | "agency" | "restaurant" | "marketplace" | "general"
    """

    return detect_business_model_details(
        columns=columns,
        rows=rows,
    )["business_model"]


def build_monthly_series(
    rows: list[dict[str, Any]],
    columns: list[str],
    column_mapping: dict[str, str] | None = None,
) -> list[dict[str, Any]]:
    date_col = resolve_column("date", columns, column_mapping)
    revenue_col = resolve_column("revenue", columns, column_mapping)
    expenses_col = resolve_column("expenses", columns, column_mapping)
    profit_col = resolve_column("profit", columns, column_mapping)

    if not date_col or not revenue_col:
        return []

    has_expenses = bool(expenses_col)
    has_explicit_profit = bool(profit_col)

    grouped: dict[str, dict[str, float]] = defaultdict(
        lambda: {
            "revenue": 0.0,
            "expenses": 0.0,
            "profit": 0.0,
        }
    )

    for row in rows:
        period = parse_period(row.get(date_col))

        if period == "Unknown":
            continue

        grouped[period]["revenue"] += to_float(row.get(revenue_col)) or 0.0

        if expenses_col:
            grouped[period]["expenses"] += to_float(row.get(expenses_col)) or 0.0

        if profit_col:
            grouped[period]["profit"] += to_float(row.get(profit_col)) or 0.0

    periods = sort_periods(list(grouped.keys()))

    series = []

    for period in periods:
        revenue = grouped[period]["revenue"]
        expenses = grouped[period]["expenses"]

        if has_explicit_profit:
            profit = grouped[period]["profit"]
            profit_margin_percent = safe_divide(profit, revenue) * 100
        elif has_expenses:
            profit = revenue - expenses
            profit_margin_percent = safe_divide(profit, revenue) * 100
        else:
            profit = 0.0
            profit_margin_percent = 0.0

        series.append(
            {
                "period": period,
                "revenue": round_money(revenue),
                "expenses": round_money(expenses),
                "profit": round_money(profit),
                "profit_margin_percent": round_money(profit_margin_percent),
                "profit_available": bool(has_explicit_profit or has_expenses),
                "expenses_available": bool(has_expenses),
            }
        )

    return series

def calculate_core_kpis(
    rows: list[dict[str, Any]],
    columns: list[str],
    column_mapping: dict[str, str] | None = None,
) -> dict[str, Any]:
    revenue_col = resolve_column("revenue", columns, column_mapping)
    expenses_col = resolve_column("expenses", columns, column_mapping)
    profit_col = resolve_column("profit", columns, column_mapping)

    revenue = 0.0
    expenses = 0.0
    explicit_profit = 0.0

    has_revenue = bool(revenue_col and has_verified_amount_values(rows, revenue_col))
    has_expenses = bool(expenses_col and has_verified_amount_values(rows, expenses_col))
    has_explicit_profit = bool(profit_col and has_verified_amount_values(rows, profit_col))

    for row in rows:
        if has_revenue and revenue_col:
            revenue += to_float(row.get(revenue_col)) or 0.0

        if has_expenses and expenses_col:
            expenses += to_float(row.get(expenses_col)) or 0.0

        if has_explicit_profit and profit_col:
            explicit_profit += to_float(row.get(profit_col)) or 0.0

    if has_explicit_profit:
        profit = explicit_profit
        profit_margin_percent = safe_divide(profit, revenue) * 100
        profit_available = True
    elif has_expenses:
        profit = revenue - expenses
        profit_margin_percent = safe_divide(profit, revenue) * 100
        profit_available = True
    else:
        # Revenue-only datasets, such as many e-commerce order exports, do not
        # contain costs/expenses. Do not present revenue as profit.
        profit = 0.0
        profit_margin_percent = 0.0
        profit_available = False

    monthly_series = build_monthly_series(
        rows=rows,
        columns=columns,
        column_mapping=column_mapping,
    )

    growth_rate_percent = 0.0

    if len(monthly_series) >= 2:
        previous = float(monthly_series[-2].get("revenue", 0) or 0)
        current = float(monthly_series[-1].get("revenue", 0) or 0)

        growth_rate_percent = safe_divide(
            current - previous,
            previous,
        ) * 100 if previous else 0.0

    if profit_available:
        if profit > 0:
            cashflow_status = "positive"
        elif profit < 0:
            cashflow_status = "negative"
        else:
            cashflow_status = "unknown"
    else:
        cashflow_status = "unknown"

    return {
        "revenue": round_money(revenue),
        "expenses": round_money(expenses),
        "profit": round_money(profit),
        "profit_margin_percent": round_money(profit_margin_percent),
        "growth_rate_percent": round_money(growth_rate_percent),
        "cashflow_status": cashflow_status,
        "periods_count": len(monthly_series),
        "latest_period": monthly_series[-1]["period"] if monthly_series else "",
        "revenue_available": bool(has_revenue),
        "expenses_available": bool(has_expenses),
        "profit_available": bool(profit_available),
        "profit_margin_available": bool(profit_available),
        "growth_available": bool(has_revenue and len(monthly_series) >= 2),
        "cashflow_available": bool(profit_available),
        "profit_source": (
            "explicit_profit_column"
            if has_explicit_profit
            else "revenue_minus_expenses"
            if has_expenses
            else "unavailable_missing_expenses"
        ),
        "source": "verified_calculation",
    }

def sum_column(
    rows: list[dict[str, Any]],
    column: str | None,
) -> float:
    if not column:
        return 0.0

    total = 0.0

    for row in rows:
        total += to_float(row.get(column)) or 0.0

    return total


def count_distinct_values(
    rows: list[dict[str, Any]],
    column: str | None,
) -> float:
    if not column:
        return 0.0

    values = {
        str(row.get(column)).strip()
        for row in rows
        if row.get(column) not in (None, "")
    }

    return float(len(values))


def count_or_sum_identifier_column(
    rows: list[dict[str, Any]],
    column: str | None,
) -> float:
    if not column:
        return 0.0

    summed = sum_column(rows, column)
    distinct = count_distinct_values(rows, column)

    # Identifier columns such as order_id, purchase_id, user_id, client_id
    # are often UUID/text values. They should be counted, not summed.
    normalized = normalize_text(column)
    identifier_tokens = [
        "id",
        "uuid",
        "order",
        "purchase",
        "transaction",
        "invoice",
        "customer",
        "client",
        "user",
        "buyer",
    ]

    if distinct > 0 and (summed <= 0 or any(token in normalized for token in identifier_tokens)):
        return distinct

    return summed


def latest_column_value(
    rows: list[dict[str, Any]],
    column: str | None,
) -> float:
    if not column:
        return 0.0

    for row in reversed(rows):
        value = to_float(row.get(column))

        if value is not None:
            return value

    return 0.0


def max_column_value(
    rows: list[dict[str, Any]],
    column: str | None,
) -> float:
    if not column:
        return 0.0

    max_value = 0.0

    for row in rows:
        value = to_float(row.get(column))

        if value is not None:
            max_value = max(max_value, value)

    return max_value


def build_monthly_customer_series(
    rows: list[dict[str, Any]],
    columns: list[str],
    column_mapping: dict[str, str] | None = None,
) -> list[dict[str, Any]]:
    date_col = resolve_column("date", columns, column_mapping)
    customers_col = resolve_column("customers", columns, column_mapping)
    new_customers_col = resolve_column("new_customers", columns, column_mapping)
    churned_customers_col = resolve_column("churned_customers", columns, column_mapping)

    if not date_col:
        return []

    grouped: dict[str, dict[str, float]] = defaultdict(
        lambda: {
            "customers_sum": 0.0,
            "customers_max": 0.0,
            "new_customers": 0.0,
            "churned_customers": 0.0,
        }
    )

    for row in rows:
        period = parse_period(row.get(date_col))

        if period == "Unknown":
            continue

        if customers_col:
            value = to_float(row.get(customers_col))

            if value is not None:
                grouped[period]["customers_sum"] += value
                grouped[period]["customers_max"] = max(
                    grouped[period]["customers_max"],
                    value,
                )

        if new_customers_col:
            grouped[period]["new_customers"] += to_float(row.get(new_customers_col)) or 0.0

        if churned_customers_col:
            grouped[period]["churned_customers"] += to_float(row.get(churned_customers_col)) or 0.0

    periods = sort_periods(list(grouped.keys()))
    series = []

    for period in periods:
        item = grouped[period]
        customers = max(item["customers_max"], item["customers_sum"])

        if customers <= 0 and item["new_customers"] > 0:
            customers = item["new_customers"]

        series.append(
            {
                "period": period,
                "customers": round_money(customers),
                "new_customers": round_money(item["new_customers"]),
                "churned_customers": round_money(item["churned_customers"]),
            }
        )

    return series


def calculate_customer_metrics(
    rows: list[dict[str, Any]],
    columns: list[str],
    column_mapping: dict[str, str] | None = None,
) -> dict[str, Any]:
    customers_col = resolve_column("customers", columns, column_mapping)
    new_customers_col = resolve_column("new_customers", columns, column_mapping)
    churned_customers_col = resolve_column("churned_customers", columns, column_mapping)
    churn_rate_col = resolve_column("churn_rate", columns, column_mapping)

    total_new_customers = sum_column(rows, new_customers_col)
    total_churned_customers = sum_column(rows, churned_customers_col)

    latest_customers = latest_column_value(rows, customers_col)
    max_customers = max_column_value(rows, customers_col)
    distinct_customers = count_distinct_values(rows, customers_col)

    # Strongest observed customer denominator.
    # For e-commerce exports, customers_col may be user_id/customer_id,
    # so distinct IDs are safer than numeric summation.
    effective_customers = max(latest_customers, max_customers, distinct_customers)

    # Conservative fallback when only acquisition/churn movement exists.
    if effective_customers <= 0 and (total_new_customers > 0 or total_churned_customers > 0):
        effective_customers = max(
            total_new_customers - total_churned_customers,
            total_new_customers,
            0.0,
        )

    calculated_churn_rate = (
        safe_divide(total_churned_customers, effective_customers) * 100
        if effective_customers
        else 0.0
    )

    explicit_churn_rate = latest_column_value(rows, churn_rate_col)

    # Use explicit churn rate only if there is a real churn_rate column.
    churn_rate_percent = explicit_churn_rate if explicit_churn_rate > 0 else calculated_churn_rate

    return {
        "customers": round_money(effective_customers),
        "latest_customers": round_money(latest_customers),
        "max_customers": round_money(max_customers),
        "distinct_customers": round_money(distinct_customers),
        "new_customers": round_money(total_new_customers),
        "churned_customers": round_money(total_churned_customers),
        "churn_rate_percent": round_money(churn_rate_percent),
        "customer_series": build_monthly_customer_series(
            rows=rows,
            columns=columns,
            column_mapping=column_mapping,
        ),
    }


def calculate_advanced_kpis(
    business_model: str,
    rows: list[dict[str, Any]],
    columns: list[str],
    column_mapping: dict[str, str] | None = None,
) -> dict[str, Any]:
    revenue_col = resolve_column("revenue", columns, column_mapping)
    expenses_col = resolve_column("expenses", columns, column_mapping)
    orders_col = resolve_column("orders", columns, column_mapping)
    ad_spend_col = resolve_column("ad_spend", columns, column_mapping)
    mrr_col = resolve_column("mrr", columns, column_mapping)
    arr_col = resolve_column("arr", columns, column_mapping)
    gmv_col = resolve_column("gmv", columns, column_mapping)
    take_rate_col = resolve_column("take_rate", columns, column_mapping)
    billable_hours_col = resolve_column("billable_hours", columns, column_mapping)
    conversion_rate_col = resolve_column("conversion_rate", columns, column_mapping)
    churn_rate_col = resolve_column("churn_rate", columns, column_mapping)
    new_customers_col = resolve_column("new_customers", columns, column_mapping)
    churned_customers_col = resolve_column("churned_customers", columns, column_mapping)

    total_revenue = sum_column(rows, revenue_col)
    total_expenses = sum_column(rows, expenses_col)
    total_orders = count_or_sum_identifier_column(rows, orders_col)
    total_ad_spend = sum_column(rows, ad_spend_col)
    total_gmv = sum_column(rows, gmv_col)
    total_billable_hours = sum_column(rows, billable_hours_col)

    customer_metrics = calculate_customer_metrics(
        rows=rows,
        columns=columns,
        column_mapping=column_mapping,
    )

    total_customers = float(customer_metrics["customers"])
    total_new_customers = float(customer_metrics["new_customers"])
    total_churned_customers = float(customer_metrics["churned_customers"])
    churn_rate_percent = float(customer_metrics["churn_rate_percent"])

    has_verified_revenue = bool(revenue_col and has_verified_amount_values(rows, revenue_col))
    has_verified_ad_spend = bool(ad_spend_col and has_positive_amount_values(rows, ad_spend_col))
    has_real_customer_movement = bool(new_customers_col or churned_customers_col or churn_rate_col)

    churn_available = bool(churn_rate_col or churned_customers_col)
    roas_available = bool(has_verified_ad_spend and total_ad_spend > 0 and total_revenue > 0)
    cac_available = bool(has_verified_ad_spend and total_ad_spend > 0 and total_new_customers > 0)
    aov_available = bool(has_verified_revenue and total_revenue > 0 and total_orders > 0)
    revenue_per_customer_available = bool(
        has_verified_revenue and total_revenue > 0 and total_customers > 0
    )
    customers_available = bool(has_real_customer_movement or revenue_per_customer_available)
    orders_available = bool(orders_col and has_verified_revenue and total_orders > 0)

    advanced: dict[str, Any] = {
        "aov": round_money(safe_divide(total_revenue, total_orders)) if aov_available else 0.0,
        "cac": round_money(safe_divide(total_ad_spend, total_new_customers)) if cac_available else 0.0,
        "roas": round_money(safe_divide(total_revenue, total_ad_spend)) if roas_available else 0.0,
        "churn_rate_percent": round_money(churn_rate_percent) if churn_available else 0.0,
        "revenue_per_customer": round_money(
            safe_divide(total_revenue, total_customers)
        ) if revenue_per_customer_available else 0.0,
        "orders": round_money(total_orders) if orders_available else 0.0,
        "customers": round_money(total_customers) if customers_available else 0.0,
        "latest_customers": customer_metrics["latest_customers"],
        "max_customers": customer_metrics["max_customers"],
        "distinct_customers": customer_metrics.get("distinct_customers", 0),
        "new_customers": round_money(total_new_customers),
        "churned_customers": round_money(total_churned_customers),
        "ad_spend": round_money(total_ad_spend),
        "aov_available": aov_available,
        "cac_available": cac_available,
        "roas_available": roas_available,
        "churn_available": churn_available,
        "revenue_per_customer_available": revenue_per_customer_available,
        "orders_available": orders_available,
        "customers_available": customers_available,
        "ad_spend_available": has_verified_ad_spend,
        "customer_series": customer_metrics["customer_series"] if customers_available else [],
    }

    if mrr_col:
        mrr = latest_column_value(rows, mrr_col)
    else:
        monthly_series = build_monthly_series(
            rows=rows,
            columns=columns,
            column_mapping=column_mapping,
        )
        mrr = float(monthly_series[-1]["revenue"]) if monthly_series else 0.0

    if arr_col:
        arr = latest_column_value(rows, arr_col)
    else:
        arr = mrr * 12 if business_model == "saas" else 0.0

    advanced["mrr"] = round_money(mrr) if business_model == "saas" else 0
    advanced["arr"] = round_money(arr) if business_model == "saas" else 0

    if total_gmv:
        advanced["gmv"] = round_money(total_gmv)

        if take_rate_col:
            advanced["take_rate_percent"] = round_money(
                latest_column_value(rows, take_rate_col)
            )
        else:
            advanced["take_rate_percent"] = round_money(
                safe_divide(total_revenue, total_gmv) * 100
            )

    if total_billable_hours:
        advanced["revenue_per_billable_hour"] = round_money(
            safe_divide(total_revenue, total_billable_hours)
        )
        advanced["billable_hours"] = round_money(total_billable_hours)

    if conversion_rate_col:
        advanced["conversion_rate_percent"] = round_money(
            latest_column_value(rows, conversion_rate_col)
        )

    return advanced

def build_data_quality(
    rows: list[dict[str, Any]],
    columns: list[str],
    column_mapping: dict[str, str] | None,
    detected_columns: dict[str, str],
) -> dict[str, Any]:
    missing_fields = []

    if not resolve_column("revenue", columns, column_mapping):
        missing_fields.append("revenue")

    if not resolve_column("expenses", columns, column_mapping):
        missing_fields.append("expenses")

    if not resolve_column("date", columns, column_mapping):
        missing_fields.append("date")

    limitations = []

    if len(rows) < 3:
        limitations.append("Very few rows; trend analysis may be weak.")

    if (
        not detected_columns.get("customers")
        and (
            detected_columns.get("new_customers")
            or detected_columns.get("churned_customers")
        )
    ):
        limitations.append(
            "Customer base column is missing; customer count was estimated from acquisition/churn data."
        )

    if "date" in missing_fields:
        limitations.append("No clear date/period column; growth and forecasting are limited.")

    if "revenue" in missing_fields:
        limitations.append("No clear revenue column; financial analysis is limited.")

    if "expenses" in missing_fields:
        limitations.append(
            "No clear expenses, cost, or profit column was detected; profitability metrics cannot be verified."
        )

    score = 100
    score -= len(missing_fields) * 20

    if len(rows) < 3:
        score -= 20

    if (
        not detected_columns.get("customers")
        and (
            detected_columns.get("new_customers")
            or detected_columns.get("churned_customers")
        )
    ):
        score -= 5

    score = max(0, min(score, 100))

    return {
        "score": score,
        "missing_fields": missing_fields,
        "limitations": limitations,
        "detected_columns": detected_columns,
    }


def suggested_kpis_for_model(business_model: str) -> list[str]:
    suggestions = {
        "saas": [
            "mrr",
            "arr",
            "churn_rate_percent",
            "cac",
            "ltv",
            "runway",
            "revenue_per_customer",
        ],
        "ecommerce": [
            "aov",
            "orders",
            "cac",
            "roas",
            "conversion_rate_percent",
            "refund_rate",
        ],
        "agency": [
            "revenue",
            "profit_margin_percent",
            "revenue_per_billable_hour",
            "client_concentration",
        ],
        "restaurant": [
            "revenue",
            "average_ticket",
            "food_cost_ratio",
            "peak_periods",
        ],
        "marketplace": [
            "gmv",
            "take_rate_percent",
            "buyers",
            "sellers",
            "transactions",
        ],
        "general": [
            "revenue",
            "expenses",
            "profit",
            "profit_margin_percent",
            "growth_rate_percent",
        ],
    }

    return suggestions.get(business_model, suggestions["general"])


def detect_smart_kpis(
    columns: list[str],
    rows: list[dict[str, Any]] | None = None,
    column_mapping: dict[str, str] | None = None,
) -> dict[str, Any]:
    rows = rows or []
    column_mapping = column_mapping or {}

    model_details = detect_business_model_details(
        columns=columns,
        rows=rows,
    )

    business_model = model_details["business_model"]

    detected_columns = detect_kpi_columns(columns)

    core_kpis = calculate_core_kpis(
        rows=rows,
        columns=columns,
        column_mapping=column_mapping,
    ) if rows else {
        "revenue": None,
        "expenses": None,
        "profit": None,
        "profit_margin_percent": None,
        "growth_rate_percent": None,
        "cashflow_status": "unknown",
        "periods_count": 0,
        "latest_period": "",
        "revenue_available": False,
        "expenses_available": False,
        "profit_available": False,
        "profit_margin_available": False,
        "growth_available": False,
        "cashflow_available": False,
        "source": "verified_calculation",
    }

    advanced_kpis = calculate_advanced_kpis(
        business_model=business_model,
        rows=rows,
        columns=columns,
        column_mapping=column_mapping,
    ) if rows else {}

    monthly_series = build_monthly_series(
        rows=rows,
        columns=columns,
        column_mapping=column_mapping,
    ) if rows else []

    data_quality = build_data_quality(
        rows=rows,
        columns=columns,
        column_mapping=column_mapping,
        detected_columns=detected_columns,
    )

    has_financial_performance = bool(
        core_kpis.get("revenue_available")
        or core_kpis.get("expenses_available")
        or core_kpis.get("profit_available")
        or core_kpis.get("cashflow_available")
        or advanced_kpis.get("orders_available")
        or advanced_kpis.get("customers_available")
        or advanced_kpis.get("churn_available")
        or advanced_kpis.get("roas_available")
        or advanced_kpis.get("cac_available")
        or advanced_kpis.get("mrr_available")
        or advanced_kpis.get("arr_available")
    )

    if not has_financial_performance:
        business_model = "general"
        model_details = {
            **model_details,
            "business_model": "general",
            "confidence": "low",
        }

    return {
        "business_model": business_model,
        "analysis_available": has_financial_performance,
        "dataset_type": "business_performance" if has_financial_performance else "non_performance_dataset",
        "model_detection": model_details,
        "confidence_level": model_details["confidence"],
        "detected_kpi_columns": detected_columns,
        "core_kpis": core_kpis,
        "advanced_kpis": advanced_kpis,
        "monthly_series": monthly_series,
        "suggested_kpis": suggested_kpis_for_model(business_model),
        "data_quality": data_quality,
        "source": "verified_calculation_strict",
    }


def detect_business_kpis(
    business_model: str,
    rows: list[dict[str, Any]],
    column_mapping: dict[str, str],
) -> dict[str, Any]:
    """
    Strict production wrapper used by business_routes.py.

    The backend is the source of truth for numeric KPIs.
    The AI may explain the numbers, but should not be trusted to calculate them.
    """

    rows = rows or []
    column_mapping = column_mapping or {}

    columns: list[str] = []

    if rows:
        seen = set()

        for row in rows:
            for column in row.keys():
                if column not in seen:
                    columns.append(column)
                    seen.add(column)

    if not business_model or isinstance(business_model, dict):
        business_model = detect_business_model(columns, rows)

    smart = detect_smart_kpis(
        columns=columns,
        rows=rows,
        column_mapping=column_mapping,
    )

    # Keep router-provided model only when verified business performance data exists.
    # For profile/reference/catalog/review files, force general to avoid false
    # e-commerce/restaurant/etc. classification from words like product/category/user.
    if smart.get("analysis_available") and (
        business_model in BUSINESS_MODELS or business_model == "general"
    ):
        smart["business_model"] = business_model
    elif not smart.get("analysis_available"):
        smart["business_model"] = "general"
        smart["model_detection"] = {
            **(smart.get("model_detection") or {}),
            "business_model": "general",
            "confidence": "low",
        }

    return {
        "business_model": smart["business_model"],
        "available": bool(smart.get("analysis_available")),
        "analysis_available": bool(smart.get("analysis_available")),
        "dataset_type": smart.get("dataset_type", "business_performance"),
        "rows_count": len(rows),
        "column_mapping": column_mapping,
        "detected_kpi_columns": smart["detected_kpi_columns"],
        "core_kpis": smart["core_kpis"],
        "advanced_kpis": smart["advanced_kpis"],
        "monthly_series": smart["monthly_series"],
        "suggested_kpis": smart["suggested_kpis"],
        "data_quality": smart["data_quality"],
        "model_detection": smart["model_detection"],
        "source": "verified_calculation_strict",
    }
