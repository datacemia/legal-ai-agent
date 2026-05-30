def generate_financial_insights(
    transactions: list[dict],
    subscriptions: list[dict],
    scores: dict,
    forecast: dict,
    opportunities: list[dict],
    currency: str = "MAD",
) -> list[dict]:
    insights = []

    expenses = forecast.get(
        "monthly_expenses",
        0,
    )

    income = forecast.get(
        "monthly_income",
        0,
    )

    net = forecast.get(
        "net_cashflow",
        0,
    )

    score = scores.get(
        "overall_financial_habits_score",
        0,
    )

    subscription_total = sum(
        s.get("monthly_cost", 0)
        for s in subscriptions
    )

    # 🔥 Cashflow
    if net > 0:
        insights.append(
            {
                "type": "positive",
                "title": "Positive cashflow detected",
                "message": (
                    f"You currently retain approximately "
                    f"{round(net, 2)} {currency} after expenses."
                ),
            }
        )

    else:
        insights.append(
            {
                "type": "warning",
                "title": "Negative cashflow risk",
                "message": (
                    "Your current expenses exceed your income."
                ),
            }
        )

    # 🔥 Score insight
    if score >= 80:
        insights.append(
            {
                "type": "positive",
                "title": "Excellent financial habits",
                "message": (
                    "Your financial behavior appears healthy and stable."
                ),
            }
        )

    elif score < 50:
        insights.append(
            {
                "type": "warning",
                "title": "Financial habits need improvement",
                "message": (
                    "Your spending patterns may require closer monitoring."
                ),
            }
        )

    # 🔥 Subscription pressure
    if income > 0:
        ratio = (
            subscription_total / income
        ) * 100

        if ratio >= 10:
            insights.append(
                {
                    "type": "warning",
                    "title": "High subscription pressure",
                    "message": (
                        f"Subscriptions consume approximately "
                        f"{round(ratio, 1)}% of your income."
                    ),
                }
            )

    # 🔥 Opportunities
    if opportunities:
        estimated = sum(
            o.get(
                "estimated_savings_opportunity",
                0,
            )
            for o in opportunities
        )

        insights.append(
            {
                "type": "tip",
                "title": "Savings opportunities detected",
                "message": (
                    f"Potential savings opportunities identified: "
                    f"{round(estimated, 2)} {currency}."
                ),
            }
        )

    # 🔥 Expense intensity
    if expenses >= 5000:
        insights.append(
            {
                "type": "warning",
                "title": "High spending intensity",
                "message": (
                    "Your observed expenses are relatively high."
                ),
            }
        )

    return insights