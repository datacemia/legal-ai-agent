import re
from collections import defaultdict


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


SERVICE_HINTS = [
    "subscription",
    "abonnement",
    "monthly",
    "recurring",
    "paiement carte",
    "card payment",
    "3ds",
    "usd",
    "eur",
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
]


def normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", value.lower()).strip()


def is_excluded_subscription(description: str) -> bool:
    normalized = normalize_text(description)

    return any(
        keyword in normalized
        for keyword in EXCLUDED_SUBSCRIPTION_KEYWORDS
    )


def extract_known_merchant(description: str) -> str | None:
    normalized = normalize_text(description)

    for keyword, merchant_name in KNOWN_SUBSCRIPTION_MERCHANTS.items():
        if keyword in normalized:
            return merchant_name

    return None


def looks_like_digital_service(description: str) -> bool:
    normalized = normalize_text(description)

    return any(hint in normalized for hint in SERVICE_HINTS)


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

        merchant = extract_known_merchant(description)

        if not merchant and looks_like_digital_service(description):
            words = re.findall(r"[A-Z][A-Z0-9]{2,}", description.upper())

            ignored_words = {
                "USD",
                "EUR",
                "MAD",
                "DHS",
                "WWW",
                "COM",
                "LLC",
                "SARL",
                "PAYMENT",
                "PAIEMENT",
                "CARTE",
                "CARD",
                "THE",
            }

            merchant_words = [
                word
                for word in words
                if word not in ignored_words and not word.isdigit()
            ]

            if merchant_words:
                merchant = merchant_words[0].title()

        if not merchant:
            continue

        grouped[merchant].append(amount)

    subscriptions = []

    for merchant, amounts in grouped.items():
        monthly_cost = round(sum(amounts), 2)

        subscriptions.append(
            {
                "name": merchant,
                "monthly_cost": monthly_cost,
                "yearly_cost_estimate": round(monthly_cost * 12, 2),
                "transactions_count": len(amounts),
            }
        )

    subscriptions.sort(
        key=lambda item: item["monthly_cost"],
        reverse=True,
    )

    return subscriptions