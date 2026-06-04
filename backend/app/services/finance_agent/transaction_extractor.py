import re
import unicodedata
from collections import defaultdict
from datetime import datetime, date
from statistics import median


# ---------------------------------------------------------------------------
# International recurring subscription detector
# Standard FR / EN / AR approach:
# 1) Detect real recurrence patterns first.
# 2) Use known merchant names only as enrichment, not as the main condition.
# 3) Avoid bank-specific or country-specific rules.
# 4) Keep one-off legal / government / filing payments out of subscriptions.
# ---------------------------------------------------------------------------


KNOWN_SUBSCRIPTION_MERCHANTS = {
    "netflix": "Netflix",
    "spotify": "Spotify",
    "adobe": "Adobe",
    "aws": "AWS",
    "amazon web services": "AWS",
    "chatgpt": "ChatGPT",
    "openai": "OpenAI",
    "icloud": "iCloud",
    "apple": "Apple",
    "google": "Google",
    "youtube": "YouTube",
    "canva": "Canva",
    "gym": "Gym",
    "hostinger": "Hostinger",
    "www hostinger com": "Hostinger",
    "railway": "Railway",
    "namesilo": "Namesilo",
    "namecheap": "Namecheap",
    "godaddy": "GoDaddy",
    "notion": "Notion",
    "figma": "Figma",
    "slack": "Slack",
    "zoom": "Zoom",
    "microsoft": "Microsoft",
    "dropbox": "Dropbox",
}


RECURRING_HINTS = [
    # EN
    "subscription",
    "recurring",
    "monthly",
    "membership",
    "renewal",
    "plan",

    # FR
    "abonnement",
    "mensuel",
    "cotisation",
    "renouvellement",
    "forfait",
    "adhesion",
    "adhésion",

    # AR
    "اشتراك",
    "شهري",
    "تجديد",
    "عضوية",
]


FEE_KEYWORDS = [
    # EN
    "bank fee",
    "monthly fee",
    "service fee",
    "overdraft fee",
    "maintenance fee",

    # FR
    "frais bancaire",
    "frais bancaires",
    "commission bancaire",
    "frais de tenue",
    "frais de compte",

    # AR
    "رسوم بنكية",
    "رسوم الحساب",
    "عمولة بنكية",
]


ONE_OFF_SERVICE_HINTS = [
    # EN
    "attorney",
    "lawyer",
    "legal",
    "llc attorney",
    "company formation",
    "incorporation",
    "state filing",
    "government",
    "tax filing",
    "irs",

    # FR
    "avocat",
    "juridique",
    "création société",
    "creation societe",
    "constitution société",
    "constitution societe",
    "frais gouvernementaux",
    "impôt",
    "impot",
    "taxe",

    # AR
    "محامي",
    "قانوني",
    "تأسيس شركة",
    "رسوم حكومية",
    "ضريبة",
    "ضرائب",
]


GENERIC_WORDS = {
    "usd", "eur", "mad", "dhs", "aed", "sar", "qar", "gbp", "cad", "aud",
    "www", "com", "net", "org",
    "llc", "ltd", "inc", "sarl", "sa", "sas",
    "payment", "card", "purchase", "debit", "credit", "withdrawal",
    "subscription", "recurring", "monthly", "membership", "renewal",
    "paiement", "carte", "achat", "prelevement", "prélèvement",
    "abonnement", "mensuel", "cotisation", "renouvellement",
    "دفع", "بطاقة", "شراء", "خصم", "اقتطاع", "اشتراك", "شهري",
}


def strip_accents(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", str(value or ""))
    return "".join(
        char for char in normalized
        if not unicodedata.combining(char)
    )


def normalize_text(value: str) -> str:
    value = strip_accents(str(value or "")).lower()
    value = re.sub(r"[^a-z0-9\u0600-\u06ff]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def parse_tx_date(value) -> date | None:
    if isinstance(value, date):
        return value

    raw = str(value or "").strip()

    if not raw:
        return None

    formats = [
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%d-%m-%Y",
        "%d.%m.%Y",
        "%m/%d/%Y",
        "%m-%d-%Y",
        "%m.%d.%Y",
        "%d/%m/%y",
        "%m/%d/%y",
    ]

    for fmt in formats:
        try:
            return datetime.strptime(raw, fmt).date()
        except ValueError:
            continue

    return None


def amount_close(a: float, b: float, tolerance_ratio: float = 0.08) -> bool:
    if a <= 0 or b <= 0:
        return False

    tolerance = max(1.0, min(a, b) * tolerance_ratio)
    return abs(a - b) <= tolerance


def is_monthly_spacing(days: int) -> bool:
    return 25 <= abs(days) <= 35


def is_excluded_subscription(description: str) -> bool:
    normalized = normalize_text(description)
    return any(keyword in normalized for keyword in ONE_OFF_SERVICE_HINTS)


def is_bank_fee(description: str) -> bool:
    normalized = normalize_text(description)
    return any(keyword in normalized for keyword in FEE_KEYWORDS)


def extract_known_merchant(description: str) -> str | None:
    normalized = normalize_text(description)

    for keyword, merchant_name in KNOWN_SUBSCRIPTION_MERCHANTS.items():
        if normalize_text(keyword) in normalized:
            return merchant_name

    return None


def looks_like_recurring_service(description: str) -> bool:
    normalized = normalize_text(description)
    return any(hint in normalized for hint in RECURRING_HINTS)


def canonicalize_merchant(description: str) -> str:
    known = extract_known_merchant(description)

    if known:
        return known

    normalized = normalize_text(description)

    tokens = [
        token
        for token in normalized.split()
        if token not in GENERIC_WORDS
        and not token.isdigit()
        and not re.fullmatch(r"\d{2,}", token)
        and len(token) >= 3
    ]

    if not tokens:
        return normalized[:40] or "Unknown"

    return " ".join(tokens[:3]).title()


def has_recurring_pattern(items: list[dict]) -> bool:
    if len(items) < 2:
        return False

    sorted_items = sorted(
        items,
        key=lambda item: item["date"] or date.min,
    )

    similar_amount_pairs = 0

    for index, current in enumerate(sorted_items):
        for other in sorted_items[index + 1:]:
            if amount_close(current["amount"], other["amount"]):
                similar_amount_pairs += 1

    if similar_amount_pairs == 0:
        return False

    dated_items = [
        item for item in sorted_items
        if item["date"] is not None
    ]

    if len(dated_items) >= 2:
        monthly_pairs = 0

        for index, current in enumerate(dated_items):
            for other in dated_items[index + 1:]:
                days = (other["date"] - current["date"]).days

                if is_monthly_spacing(days) and amount_close(
                    current["amount"],
                    other["amount"],
                ):
                    monthly_pairs += 1

        if monthly_pairs > 0:
            return True

    return similar_amount_pairs > 0


def detect_recurring_subscriptions(
    transactions: list[dict],
) -> list[dict]:
    grouped: dict[str, list[dict]] = defaultdict(list)

    for tx in transactions:
        if tx.get("type") != "expense":
            continue

        description = tx.get("description", "")

        if is_excluded_subscription(description):
            continue

        if is_bank_fee(description):
            continue

        try:
            amount = abs(float(tx.get("amount", 0) or 0))
        except (TypeError, ValueError):
            continue

        if amount <= 0:
            continue

        merchant = canonicalize_merchant(description)

        grouped[merchant].append(
            {
                "amount": amount,
                "date": parse_tx_date(tx.get("date")),
                "description": description,
                "has_hint": looks_like_recurring_service(description),
                "known_merchant": extract_known_merchant(description),
            }
        )

    subscriptions = []

    for merchant, items in grouped.items():
        if not items:
            continue

        known_or_hint = any(
            item["known_merchant"] or item["has_hint"]
            for item in items
        )

        recurring = has_recurring_pattern(items)

        # One known merchant transaction alone is not enough.
        if not recurring and len(items) < 2:
            continue

        amounts = [item["amount"] for item in items]
        monthly_cost = round(float(median(amounts)), 2)

        confidence = 85 if recurring else 60

        if known_or_hint:
            confidence = min(confidence + 10, 95)

        subscriptions.append(
            {
                "name": merchant,
                "monthly_cost": monthly_cost,
                "yearly_cost_estimate": round(monthly_cost * 12, 2),
                "transactions_count": len(items),
                "confidence": confidence,
                "evidence": [
                    {
                        "date": item["date"].isoformat() if item["date"] else None,
                        "amount": item["amount"],
                        "description": item["description"],
                    }
                    for item in items[:5]
                ],
            }
        )

    subscriptions.sort(
        key=lambda item: (
            item["confidence"],
            item["monthly_cost"],
        ),
        reverse=True,
    )

    return subscriptions
