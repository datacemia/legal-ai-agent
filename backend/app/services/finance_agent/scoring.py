def clamp_score(value: float) -> int:
    return int(max(0, min(100, round(value))))


def calculate_financial_scores(
    transactions: list[dict],
    subscriptions: list[dict],
    fallback_income: float | None = None,
) -> dict:
    income = sum(
        float(t.get("amount", 0) or 0)
        for t in transactions
        if t.get("type") == "income" and float(t.get("amount", 0) or 0) > 0
    )

    income_source = "transactions"

    if income <= 0 and fallback_income:
        income = float(fallback_income)
        income_source = "ai_fallback"

    expenses = sum(
        abs(float(t.get("amount", 0) or 0))
        for t in transactions
        if t.get("type") == "expense"
    )

    if expenses <= 0 and transactions:
        expenses = sum(
            abs(float(t.get("amount", 0) or 0))
            for t in transactions
            if float(t.get("amount", 0) or 0) < 0
        )

    if not transactions:
        extraction_quality = "failed"
    elif expenses <= 0:
        extraction_quality = "partial"
    else:
        extraction_quality = "success"

    subscription_total = sum(
        float(s.get("monthly_cost", 0) or 0)
        for s in subscriptions
    )

    subscription_count = len(subscriptions)

    category_totals = {}

    for t in transactions:
        if t.get("type") != "expense":
            continue

        category = str(t.get("category") or "Other").lower()

        category_totals[category] = (
            category_totals.get(category, 0)
            + abs(float(t.get("amount", 0) or 0))
        )

    other_expenses = category_totals.get("other", 0)

    discretionary_keywords = {
        "food",
        "shopping",
        "subscriptions",
        "entertainment",
        "transport",
        "travel",
    }

    discretionary_expenses = sum(
        amount
        for category, amount in category_totals.items()
        if category in discretionary_keywords
    )

    if income > 0:
        savings_rate = (
            (income - expenses) / income
        ) * 100

        expense_ratio = (
            expenses / income
        ) * 100

        subscription_ratio = (
            subscription_total / income
        ) * 100

    else:
        savings_rate = 0

        expense_ratio = (
            100
            if expenses > 0
            else 0
        )

        subscription_ratio = (
            (subscription_total / expenses) * 100
            if expenses > 0
            else 0
        )

    saving_behavior = clamp_score(
        min(
            100,
            savings_rate * 2.0,
        )
    )

    if expenses <= 0:
        subscription_control = 100

    else:
        subscription_expense_ratio = (
            subscription_total / expenses
        ) * 100

        subscription_control = clamp_score(
            100
            - (subscription_expense_ratio * 1.5)
            - (subscription_count * 5)
        )

    debt_risk = clamp_score(
        100 - max(
            0,
            expense_ratio - 70,
        )
    )

    impulse_spending = clamp_score(
        100 - min(
            80,
            expense_ratio * 0.6,
        )
    )

    income_stability = (
        80
        if income > 0
        else 35
    )

    overall_score = clamp_score(
        (
            saving_behavior * 0.30
            + subscription_control * 0.20
            + debt_risk * 0.20
            + impulse_spending * 0.15
            + income_stability * 0.15
        )
    )

    penalty = 0

    if income > 0:
        raw_expense_ratio = (
            expenses / income
        )

        raw_subscription_ratio = (
            subscription_total / income
        )

    else:
        raw_expense_ratio = (
            1
            if expenses > 0
            else 0
        )

        raw_subscription_ratio = 0

    raw_other_ratio = (
        other_expenses / expenses
        if expenses > 0
        else 0
    )

    raw_discretionary_ratio = (
        discretionary_expenses / expenses
        if expenses > 0
        else 0
    )

    if raw_expense_ratio > 0.90:
        penalty += 30

    elif raw_expense_ratio > 0.75:
        penalty += 20

    elif raw_expense_ratio > 0.60:
        penalty += 10

    if raw_other_ratio > 0.70:
        penalty += 5

    if raw_discretionary_ratio > 0.30:
        penalty += 10

    if raw_subscription_ratio > 0.05:
        penalty += 6

    if income - expenses < 0:
        penalty += 25

    overall_score = clamp_score(
        overall_score - penalty
    )

    if extraction_quality == "success" and transactions:
        overall_score = max(10, overall_score)

    return {
        "saving_behavior": saving_behavior,
        "subscription_control": subscription_control,
        "debt_risk": debt_risk,
        "impulse_spending": impulse_spending,
        "income_stability": income_stability,
        "overall_financial_habits_score": overall_score,
        "extraction_quality": extraction_quality,
        "metrics": {
            "income_detected": round(
                income,
                2,
            ),
            "income_source": income_source,
            "expenses_detected": round(
                expenses,
                2,
            ),
            "subscription_total": round(
                subscription_total,
                2,
            ),
            "subscription_count": subscription_count,
            "savings_rate_percent": round(
                savings_rate,
                2,
            ),
            "expense_ratio_percent": round(
                expense_ratio,
                2,
            ),
            "subscription_ratio_percent": round(
                subscription_ratio,
                2,
            ),
            "other_ratio_percent": round(
                raw_other_ratio * 100,
                2,
            ),
            "discretionary_ratio_percent": round(
                raw_discretionary_ratio * 100,
                2,
            ),
            "score_penalty": penalty,
            "extraction_quality": extraction_quality,
        },
    }
