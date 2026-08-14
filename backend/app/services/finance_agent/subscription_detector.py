import re
from collections import defaultdict
from datetime import datetime

# RUNEXA_SUBSCRIPTION_DETECTOR_VERSION
# v4-international-category-intersection
#
# Design goals:
# - no bank-specific logic
# - no country-specific logic
# - no currency-specific logic
# - no merchant whitelist
# - no payment-network whitelist
# - no language-specific merchant dictionary
# - recurring-charge detection is structural/accounting only
# - "confirmed subscription" requires BOTH:
#       1) recurring-charge evidence
#       2) independent canonical subscription categorization
#
# Important:
# Recurrence and business category are separate concepts.
# A recurring grocery, insurance, rent, loan or transport payment must not be
# presented as a subscription merely because it repeats.


def normalize_text(value: str) -> str:
    value = (value or "").lower()
    value = re.sub(r"[^\w\u0600-\u06FF]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def normalize_tokens(value: str) -> list[str]:
    return [
        token
        for token in re.split(
            r"[^\w\u0600-\u06FF]+",
            (value or "").lower(),
        )
        if token
    ]


def parse_tx_date(value: str | None):
    if not value:
        return None

    try:
        return datetime.fromisoformat(str(value)[:10]).date()
    except Exception:
        return None


def safe_float(value: object) -> float:
    try:
        return float(value or 0)
    except (TypeError, ValueError):
        return 0.0


def build_structural_counterparty_key(description: str) -> str:
    """
    Build a neutral recurring-charge grouping key from stable text structure.

    Purely numeric tokens and long alphanumeric instance/reference tokens are
    discarded. Remaining text tokens are kept in original order.

    No bank, merchant, country, currency, network or language dictionary is
    used here.
    """
    tokens = normalize_tokens(description)
    stable_tokens = []

    for token in tokens:
        # Ignore tokens made only of digits.
        if token.isdigit():
            continue

        # Ignore long alphanumeric instance/reference tokens containing digits.
        # This removes common card/reference/transaction-instance fragments
        # without depending on a specific bank/network/vendor.
        if any(ch.isdigit() for ch in token) and len(token) >= 6:
            continue

        stable_tokens.append(token)

    return " ".join(stable_tokens).strip()


def _amounts_are_consistent(items: list[dict]) -> bool:
    amounts = [
        safe_float(item.get("amount"))
        for item in items
        if safe_float(item.get("amount")) > 0
    ]

    if len(amounts) < 2:
        return False

    average = sum(amounts) / len(amounts)

    if average <= 0:
        return False

    maximum_deviation = max(
        abs(amount - average)
        for amount in amounts
    )

    # Conservative tolerance retained:
    # - absolute tolerance for small amounts
    # - proportional tolerance for larger amounts
    return maximum_deviation <= max(2.0, average * 0.20)


def _distinct_dates(items: list[dict]):
    return sorted(
        {
            date_value
            for date_value in (
                parse_tx_date(item.get("date"))
                for item in items
            )
            if date_value
        }
    )


# Structural cadence windows only.
# These intervals do not imply a business type.
CADENCE_WINDOWS = (
    ("weekly", 6, 9),
    ("biweekly", 12, 16),
    ("monthly", 25, 35),
    ("bimonthly", 55, 66),
    ("quarterly", 80, 100),
    ("semiannual", 170, 195),
    ("annual", 330, 400),
)


def _matching_cadence_name(gap_days: int) -> str | None:
    for name, low, high in CADENCE_WINDOWS:
        if low <= gap_days <= high:
            return name

    return None


def _recurrence_cadence_evidence(items: list[dict]) -> dict:
    """
    Return neutral cadence evidence.

    Rules:
    - 2 distinct observations:
        one supported gap is enough to say "recurring charge candidate";
    - 3+ distinct observations:
        recurrence must repeat consistently in the SAME cadence family.
        A single accidental weekly/monthly-looking gap among irregular charges
        is not enough.
    """
    dates = _distinct_dates(items)

    if len(dates) < 2:
        return {
            "supported": False,
            "cadence": None,
            "matching_gaps": 0,
            "total_gaps": 0,
            "gaps": [],
        }

    gaps = [
        (dates[index] - dates[index - 1]).days
        for index in range(1, len(dates))
    ]

    cadence_counts: dict[str, int] = defaultdict(int)

    for gap in gaps:
        cadence_name = _matching_cadence_name(gap)

        if cadence_name:
            cadence_counts[cadence_name] += 1

    if not cadence_counts:
        return {
            "supported": False,
            "cadence": None,
            "matching_gaps": 0,
            "total_gaps": len(gaps),
            "gaps": gaps,
        }

    cadence, matching_gaps = max(
        cadence_counts.items(),
        key=lambda item: item[1],
    )

    if len(dates) == 2:
        supported = matching_gaps >= 1
    else:
        # For 3+ observations, require at least two intervals in the same
        # cadence family and a majority of observed gaps supporting it.
        supported = (
            matching_gaps >= 2
            and (matching_gaps / len(gaps)) >= 0.60
        )

    return {
        "supported": supported,
        "cadence": cadence if supported else None,
        "matching_gaps": matching_gaps,
        "total_gaps": len(gaps),
        "gaps": gaps,
    }


def _has_supported_cadence(items: list[dict]) -> bool:
    return bool(
        _recurrence_cadence_evidence(items).get("supported")
    )


def has_recurring_pattern(items: list[dict]) -> bool:
    """
    Confirm recurring-charge evidence from accounting observations only.

    Required:
    - at least two expense observations;
    - at least two distinct dates;
    - materially similar amounts;
    - supported periodic cadence.

    This function does NOT classify the charge as a subscription.
    """
    if len(items) < 2:
        return False

    if len(_distinct_dates(items)) < 2:
        return False

    if not _amounts_are_consistent(items):
        return False

    return _has_supported_cadence(items)


def _canonical_category_value(tx: dict) -> str:
    """
    Read only structured category fields already produced by the independent
    categorization layer.

    No description/merchant text is inspected here.
    """
    for field_name in (
        "category",
        "spending_category",
        "normalized_category",
    ):
        value = tx.get(field_name)

        if value:
            return normalize_text(str(value))

    return ""


def is_subscription_categorized_transaction(tx: dict) -> bool:
    """
    True only when the independent categorization layer has explicitly marked
    the transaction with the canonical subscription category.

    This is a business-category observation, not recurrence evidence.

    The canonical English storage values below are internal category IDs/labels,
    not merchant or language heuristics.
    """
    category = _canonical_category_value(tx)

    return category in {
        "subscription",
        "subscriptions",
    }


def detect_recurring_charges(
    transactions: list[dict],
) -> list[dict]:
    """
    Detect confirmed recurring CHARGES using structural evidence only.

    Output is neutral. A result here may later be categorized as:
    - subscription
    - insurance
    - loan
    - utility
    - rent
    - transport
    - another recurring expense type

    No business-type conclusion is made in this function.
    """
    grouped = defaultdict(list)

    for tx in transactions:
        if tx.get("type") != "expense":
            continue

        amount = abs(safe_float(tx.get("amount")))

        if amount <= 0:
            continue

        description = str(tx.get("description") or "")
        counterparty_key = build_structural_counterparty_key(
            description
        )

        if not counterparty_key:
            continue

        grouped[counterparty_key].append(
            {
                "amount": amount,
                "date": tx.get("date"),
                "description": description,
                "source_transaction": tx,
            }
        )

    recurring = []

    for counterparty_key, items in grouped.items():
        if not has_recurring_pattern(items):
            continue

        cadence_evidence = _recurrence_cadence_evidence(items)

        amounts = [
            safe_float(item.get("amount"))
            for item in items
        ]
        total_observed = round(sum(amounts), 2)
        transactions_count = len(items)
        average_charge = round(
            total_observed / transactions_count,
            2,
        )

        first_description = (
            items[0].get("description")
            or counterparty_key
            or "Recurring charge"
        )

        recurring.append(
            {
                "name": first_description,
                "average_charge": average_charge,

                # Backward-compatible field retained.
                # It historically means average observed charge, despite name.
                "monthly_cost": average_charge,

                "total_observed_cost": total_observed,
                "yearly_cost_estimate": round(
                    average_charge * 12,
                    2,
                ),
                "transactions_count": transactions_count,
                "recurrence_evidence": (
                    "observed_structural_pattern"
                ),
                "recurring_key": counterparty_key,
                "cadence": cadence_evidence.get("cadence"),
                "matching_gaps": cadence_evidence.get(
                    "matching_gaps",
                    0,
                ),
                "total_gaps": cadence_evidence.get(
                    "total_gaps",
                    0,
                ),
            }
        )

    recurring.sort(
        key=lambda item: item["average_charge"],
        reverse=True,
    )

    return recurring


def _subscription_category_keys(
    transactions: list[dict],
) -> set[str]:
    """
    Build structural keys only from transactions independently categorized as
    subscription-like.

    Recurrence detection itself remains category-independent.
    """
    keys: set[str] = set()

    for tx in transactions:
        if tx.get("type") != "expense":
            continue

        if not is_subscription_categorized_transaction(tx):
            continue

        key = build_structural_counterparty_key(
            str(tx.get("description") or "")
        )

        if key:
            keys.add(key)

    return keys


def detect_recurring_subscriptions(
    transactions: list[dict],
) -> list[dict]:
    """
    Backward-compatible public API.

    A CONFIRMED SUBSCRIPTION requires the intersection of:

        recurring structural charge
        AND
        independent subscription categorization

    Therefore:
    - repeated grocery purchases are not subscriptions;
    - repeated insurance payments are not subscriptions;
    - repeated loan payments are not subscriptions;
    - repeated utility payments are not subscriptions;
    - a subscription-category charge without recurrence is not "confirmed";
    - only observations supported by BOTH layers are returned.

    If the upstream categorization layer does not provide a canonical category,
    this function conservatively returns no confirmed subscription rather than
    inventing one.
    """
    recurring_charges = detect_recurring_charges(
        transactions
    )
    subscription_keys = _subscription_category_keys(
        transactions
    )

    confirmed_subscriptions = [
        item
        for item in recurring_charges
        if item.get("recurring_key") in subscription_keys
    ]

    confirmed_subscriptions.sort(
        key=lambda item: item["monthly_cost"],
        reverse=True,
    )

    return confirmed_subscriptions
