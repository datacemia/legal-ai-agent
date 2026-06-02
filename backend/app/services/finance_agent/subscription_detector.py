import re
from collections import defaultdict
from datetime import datetime


SUBSCRIPTION_SERVICE_KEYWORDS = {
    "netflix": "Netflix",
    "spotify": "Spotify",
    "adobe": "Adobe",
    "chatgpt": "ChatGPT",
    "openai": "OpenAI",
    "icloud": "iCloud",
    "apple music": "Apple Music",
    "apple tv": "Apple TV",
    "apple arcade": "Apple Arcade",
    "youtube premium": "YouTube Premium",
    "canva": "Canva",
    "hostinger": "Hostinger",
    "railway": "Railway",
    "namesilo": "Namesilo",
    "namecheap": "Namecheap",
    "godaddy": "GoDaddy",
    "notion": "Notion",
    "figma": "Figma",
    "slack": "Slack",
    "zoom": "Zoom",
    "microsoft 365": "Microsoft 365",
    "office 365": "Microsoft 365",
    "dropbox": "Dropbox",
    "aws": "AWS",
    "amazon web services": "AWS",
}


SERVICE_HINTS = [
    "subscription",
    "abonnement",
    "monthly",
    "recurring",
    "mensuel",
    "اشتراك",
    "شهري",
    "تجديد",
]


FEE_KEYWORDS = [
    "bank fee",
    "monthly fee",
    "service fee",
    "overdraft fee",
    "maintenance fee",
    "رسوم تحويل",
    "ضريبه القيمه المضافه",
    "ضريبة القيمة المضافة",
]


EXCLUDED_SUBSCRIPTION_KEYWORDS = [
    "attorney",
    "lawyer",
    "legal",
    "llc attorney",
    "wyoming llc",
    "wyoming",
    "company formation",
    "incorporation",
    "state filing",
    "government",
    "tax",
    "irs",
    "pos",
    "point of sale",
    "شراء عبر نقاط بيع",
    "نقاط بيع",
    "mada",
    "مدى",
    "مدي",
    "pay apple",
    "apple pay",
    "حواله",
    "حوالة",
    "تحويل",
    "سداد",
]


def normalize_text(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^\w\u0600-\u06FF]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def normalize_tokens(value: str) -> set[str]:
    return {
        token
        for token in re.split(r"[^\w\u0600-\u06FF]+", value.lower())
        if token
    }


def keyword_matches(text: str, tokens: set[str], keyword: str) -> bool:
    keyword = normalize_text(keyword)

    if not keyword:
        return False

    if " " in keyword:
        return keyword in text

    return keyword in tokens


def is_excluded_subscription(description: str) -> bool:
    normalized = normalize_text(description)
    tokens = normalize_tokens(description)

    return any(
        keyword_matches(normalized, tokens, keyword)
        for keyword in EXCLUDED_SUBSCRIPTION_KEYWORDS
    )


def extract_subscription_service(description: str) -> str | None:
    normalized = normalize_text(description)
    tokens = normalize_tokens(description)

    for keyword, merchant_name in SUBSCRIPTION_SERVICE_KEYWORDS.items():
        if keyword_matches(normalized, tokens, keyword):
            return merchant_name

    return None


def looks_like_subscription_service(description: str) -> bool:
    normalized = normalize_text(description)
    tokens = normalize_tokens(description)

    return any(
        keyword_matches(normalized, tokens, hint)
        for hint in SERVICE_HINTS
    )


def parse_tx_date(value: str | None):
    if not value:
        return None

    try:
        return datetime.fromisoformat(value[:10]).date()
    except Exception:
        return None


def has_recurring_pattern(items: list[dict]) -> bool:
    if len(items) < 2:
        return False

    amounts = [item["amount"] for item in items]
    avg = sum(amounts) / len(amounts)

    if avg <= 0:
        return False

    max_deviation = max(abs(amount - avg) for amount in amounts)

    if max_deviation > max(2.0, avg * 0.20):
        return False

    dates = sorted(
        d
        for d in (parse_tx_date(item.get("date")) for item in items)
        if d
    )

    if len(dates) < 2:
        return False

    gaps = [
        (dates[i] - dates[i - 1]).days
        for i in range(1, len(dates))
    ]

    return any(25 <= gap <= 35 for gap in gaps)


def detect_recurring_subscriptions(
    transactions: list[dict],
) -> list[dict]:
    grouped = defaultdict(list)

    for tx in transactions:
        if tx.get("type") != "expense":
            continue

        description = tx.get("description", "")

        if is_excluded_subscription(description):
            continue

        amount = abs(float(tx.get("amount", 0) or 0))

        if amount <= 0:
            continue

        merchant = extract_subscription_service(description)

        if not merchant and not looks_like_subscription_service(description):
            continue

        if not merchant:
            merchant = "Recurring service"

        grouped[merchant].append(
            {
                "amount": amount,
                "date": tx.get("date"),
                "description": description,
            }
        )

    subscriptions = []

    for merchant, items in grouped.items():
        service_is_explicit = merchant != "Recurring service"

        if not service_is_explicit and not has_recurring_pattern(items):
            continue

        amounts = [item["amount"] for item in items]
        total_observed = round(sum(amounts), 2)
        transactions_count = len(amounts)

        estimated_monthly_cost = round(
            total_observed / transactions_count,
            2,
        )

        subscriptions.append(
            {
                "name": merchant,
                "monthly_cost": estimated_monthly_cost,
                "total_observed_cost": total_observed,
                "yearly_cost_estimate": round(
                    estimated_monthly_cost * 12,
                    2,
                ),
                "transactions_count": transactions_count,
            }
        )

    subscriptions.sort(
        key=lambda item: item["monthly_cost"],
        reverse=True,
    )

    return subscriptions