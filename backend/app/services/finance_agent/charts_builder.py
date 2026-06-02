from collections import defaultdict


CATEGORY_KEYWORDS = {
    "subscriptions": [
        "netflix", "spotify", "adobe", "openai", "chatgpt",
        "hostinger", "railway", "namesilo", "aws", "google",
        "youtube", "canva", "apple.com bill", "subscription",
        "premium", "recurring",
    ],
    "housing": [
        "rent", "rental", "landlord", "mortgage", "flat",
        "apartment", "housing", "loyer", "credit logement",
        "crédit logement",
    ],
    "utilities": [
        "water", "electricity", "internet", "telecom", "orange",
        "inwi", "maroc telecom", "gas", "british gas",
        "thames water", "edf", "sfr", "fiber", "fibre",
        "utility", "utilities",
    ],
    "government": [
        "council tax", "tax", "hmrc", "municipal", "government",
        "impot", "impôt", "taxe",
    ],
    "food": [
        "restaurant", "cafe", "coffee", "glovo", "uber eats",
        "deliveroo", "just eat", "pret", "pret a manger",
        "costa", "mcdonald", "kfc", "burger", "pizza",
        "pub", "bar", "food", "order",
    ],
    "groceries": [
        "tesco", "sainsburys", "sainsbury", "carrefour",
        "lidl", "aldi", "monoprix", "intermarche",
        "intermarché", "supermarket", "grocery", "groceries",
    ],
    "transport": [
        "uber trip", "taxi", "careem", "fuel", "train",
        "rail", "national rail", "trainline", "tfl",
        "contactless london", "transport", "sncf",
    ],
    "shopping": [
        "amazon", "shein", "zara", "mall", "shop", "store",
        "marketplace", "paypal payment", "card purchase",
        "retail", "electronics",
    ],
    "healthcare": [
        "nhs", "prescription", "pharmacy", "pharmacie",
        "doctor", "hospital", "clinic", "medical",
    ],
    "charity": [
        "charity", "donation", "donate",
    ],
    "transfers": [
        "to savings", "savings", "own account",
        "internal transfer", "transfer between accounts",
        "virement interne", "livret", "transfer",
        "osko transfer", "bank transfer", "wise transfer",
        "faster payment",
    ],
    "business_services": [
        "wyoming", "attorney", "llc", "legal", "company",
        "formation",
    ],
    "fees": [
        "fee", "fees", "frais", "commission",
    ],
}


def detect_category(description: str) -> str:
    normalized = description.lower()

    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(keyword in normalized for keyword in keywords):
            return category

    return "other"


def build_financial_charts(
    transactions: list[dict],
) -> dict:
    spending_over_time = defaultdict(float)
    income_over_time = defaultdict(float)
    net_cashflow_over_time = defaultdict(float)
    category_breakdown = defaultdict(float)
    subscription_growth = defaultdict(float)

    savings_evolution = []
    running_net = 0.0

    sorted_transactions = sorted(
        transactions,
        key=lambda tx: tx.get("date") or "9999-12-31",
    )

    for tx in sorted_transactions:
        date = tx.get("date") or "unknown"
        amount = float(tx.get("amount", 0) or 0)
        description = tx.get("description", "")

        running_net += amount

        savings_evolution.append(
            {
                "date": date,
                "amount": round(running_net, 2),
            }
        )

        net_cashflow_over_time[date] += amount

        if tx.get("type") == "expense":
            expense_amount = abs(amount)
            category = detect_category(description)

            spending_over_time[date] += expense_amount
            category_breakdown[category] += expense_amount

            if category == "subscriptions":
                subscription_growth[date] += expense_amount

        elif tx.get("type") == "income":
            income_over_time[date] += amount

    total_income = round(sum(income_over_time.values()), 2)
    total_expenses = round(sum(spending_over_time.values()), 2)

    return {
        "spending_over_time": [
            {
                "date": date,
                "amount": round(amount, 2),
            }
            for date, amount in spending_over_time.items()
        ],
        "income_over_time": [
            {
                "date": date,
                "amount": round(amount, 2),
            }
            for date, amount in income_over_time.items()
        ],
        "income_vs_expenses": {
            "income": total_income,
            "expenses": total_expenses,
            "net": round(total_income - total_expenses, 2),
        },
        "category_breakdown": [
            {
                "category": category,
                "amount": round(amount, 2),
            }
            for category, amount in sorted(
                category_breakdown.items(),
                key=lambda item: item[1],
                reverse=True,
            )
        ],
        "net_cashflow_over_time": [
            {
                "date": date,
                "amount": round(amount, 2),
            }
            for date, amount in net_cashflow_over_time.items()
        ],
        "subscription_growth": [
            {
                "date": date,
                "amount": round(amount, 2),
            }
            for date, amount in subscription_growth.items()
        ],
        "savings_evolution": savings_evolution,
    }
