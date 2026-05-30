import re
from collections import defaultdict


def detect_savings_opportunities(
    transactions: list[dict],
    subscriptions: list[dict],
) -> list[dict]:
    opportunities = []

    expenses = [
        t
        for t in transactions
        if t.get("type") == "expense"
    ]

    total_expenses = sum(
        abs(t.get("amount", 0))
        for t in expenses
    )

    subscription_total = sum(
        s.get("monthly_cost", 0)
        for s in subscriptions
    )

    # 🔥 High subscription spending
    if subscription_total >= 300:
        opportunities.append(
            {
                "issue": "High subscription spending",
                "severity": "medium",
                "estimated_savings_opportunity": round(
                    subscription_total * 0.35,
                    2,
                ),
                "recommendation": (
                    "Review unused subscriptions and cancel unnecessary services."
                ),
            }
        )

    # 🔥 Too many subscriptions
    if len(subscriptions) >= 5:
        opportunities.append(
            {
                "issue": "Too many recurring subscriptions",
                "severity": "high",
                "estimated_savings_opportunity": round(
                    subscription_total * 0.20,
                    2,
                ),
                "recommendation": (
                    "Reduce the number of active subscriptions."
                ),
            }
        )

    # 🔥 Overspending
    if total_expenses >= 5000:
        opportunities.append(
            {
                "issue": "High spending detected",
                "severity": "high",
                "estimated_savings_opportunity": round(
                    total_expenses * 0.10,
                    2,
                ),
                "recommendation": (
                    "Reduce discretionary spending and monitor card payments."
                ),
            }
        )

    # 🔥 Duplicate subscription detection
    merchant_counts = {}

    for sub in subscriptions:
        merchant_counts[sub["name"]] = sub.get(
            "transactions_count",
            0,
        )

    for merchant, count in merchant_counts.items():
        if count >= 3:
            matching_sub = next(
                (
                    s
                    for s in subscriptions
                    if s["name"] == merchant
                ),
                None,
            )

            if matching_sub:
                opportunities.append(
                    {
                        "issue": f"Multiple charges detected for {merchant}",
                        "severity": "medium",
                        "estimated_savings_opportunity": round(
                            matching_sub["monthly_cost"] * 0.50,
                            2,
                        ),
                        "recommendation": (
                            f"Check whether all {merchant} charges are necessary."
                        ),
                    }
                )

    opportunities.sort(
        key=lambda item: item[
            "estimated_savings_opportunity"
        ],
        reverse=True,
    )

    return opportunities