def clamp_score(value: float) -> int:
    return int(max(0, min(100, round(value))))


def _safe_float(value: object) -> float:
    try:
        return float(value or 0)
    except (TypeError, ValueError):
        return 0.0


def _normalize_category(category: object) -> str:
    value = str(category or "other").strip().lower()

    aliases = {
        "food": "food_dining",
        "debt": "debt_loans",
        "government": "government_taxes",
        "savings": "savings_investments",
        "autres": "other",
        "أخرى": "other",
    }

    return aliases.get(value, value)


def calculate_financial_scores(
    transactions: list[dict],
    subscriptions: list[dict],
    fallback_income: float | None = None,
) -> dict:
    """Calculate deterministic financial habit scores from observed data.

    International standard rule:
    - Score ratios, not raw spending amounts.
    - A high expense amount is not automatically bad if income is also high.
    - Unknown categories should not heavily punish the user; category coverage is
      a parsing/categorization signal, not a direct financial habit.
    """
    income = sum(
        _safe_float(t.get("amount"))
        for t in transactions
        if t.get("type") == "income" and _safe_float(t.get("amount")) > 0
    )

    income_source = "transactions"

    if income <= 0 and fallback_income:
        income = float(fallback_income)
        income_source = "ai_fallback"

    expenses = sum(
        abs(_safe_float(t.get("amount")))
        for t in transactions
        if t.get("type") == "expense"
    )

    if expenses <= 0 and transactions:
        expenses = sum(
            abs(_safe_float(t.get("amount")))
            for t in transactions
            if _safe_float(t.get("amount")) < 0
        )

    if not transactions:
        extraction_quality = "failed"
    elif expenses <= 0 and income <= 0:
        extraction_quality = "partial"
    else:
        extraction_quality = "success"

    subscription_total = sum(
        _safe_float(s.get("monthly_cost"))
        for s in subscriptions
    )

    subscription_count = len(subscriptions or [])

    category_totals: dict[str, float] = {}

    for t in transactions:
        if t.get("type") != "expense":
            continue

        category = _normalize_category(t.get("category"))
        category_totals[category] = (
            category_totals.get(category, 0.0)
            + abs(_safe_float(t.get("amount")))
        )

    other_expenses = category_totals.get("other", 0.0)

    discretionary_categories = {
        "food_dining",
        "shopping",
        "subscriptions",
        "entertainment",
        "travel",
    }

    discretionary_expenses = sum(
        amount
        for category, amount in category_totals.items()
        if category in discretionary_categories
    )

    if income > 0:
        net_cashflow = income - expenses
        savings_rate = net_cashflow / income
        expense_ratio = expenses / income
        subscription_ratio = subscription_total / income
    else:
        net_cashflow = -expenses
        savings_rate = 0.0
        expense_ratio = 1.0 if expenses > 0 else 0.0
        subscription_ratio = (
            subscription_total / expenses
            if expenses > 0
            else 0.0
        )

    raw_other_ratio = (
        other_expenses / expenses
        if expenses > 0
        else 0.0
    )

    raw_discretionary_ratio = (
        discretionary_expenses / expenses
        if expenses > 0
        else 0.0
    )

    # Savings behavior: 20%+ savings is excellent, 10% is acceptable.
    if income <= 0:
        saving_behavior = 35 if expenses > 0 else 70
    elif savings_rate >= 0.20:
        saving_behavior = 100
    elif savings_rate >= 0.10:
        saving_behavior = 60 + (savings_rate - 0.10) / 0.10 * 40
    elif savings_rate >= 0:
        saving_behavior = savings_rate / 0.10 * 60
    else:
        saving_behavior = max(0, 30 + savings_rate * 100)

    saving_behavior = clamp_score(saving_behavior)

    if expenses <= 0:
        subscription_control = 100
    else:
        subscription_expense_ratio = subscription_total / expenses
        subscription_control = clamp_score(
            100
            - (subscription_expense_ratio * 100 * 1.2)
            - (subscription_count * 4)
        )

    if income <= 0 and expenses > 0:
        debt_risk = 35
    elif expense_ratio <= 0.60:
        debt_risk = 95
    elif expense_ratio <= 0.80:
        debt_risk = 80 - ((expense_ratio - 0.60) / 0.20 * 20)
    elif expense_ratio <= 1.00:
        debt_risk = 60 - ((expense_ratio - 0.80) / 0.20 * 30)
    else:
        debt_risk = max(0, 30 - min(30, (expense_ratio - 1.00) * 60))

    debt_risk = clamp_score(debt_risk)

    impulse_spending = clamp_score(
        100 - min(70, raw_discretionary_ratio * 100 * 0.8)
    )

    income_stability = 80 if income > 0 else 35

    overall_score = clamp_score(
        saving_behavior * 0.35
        + subscription_control * 0.15
        + debt_risk * 0.25
        + impulse_spending * 0.10
        + income_stability * 0.15
    )

    penalty = 0

    if income > 0 and net_cashflow < 0:
        negative_gap_ratio = abs(net_cashflow) / income
        if negative_gap_ratio > 0.50:
            penalty += 25
        elif negative_gap_ratio > 0.25:
            penalty += 18
        elif negative_gap_ratio > 0.10:
            penalty += 10
        else:
            penalty += 5

    if subscription_ratio > 0.10:
        penalty += 8
    elif subscription_ratio > 0.05:
        penalty += 4

    # Unknown category penalty is intentionally small. It is not proof of bad
    # financial behavior; it mostly indicates merchant/categorization coverage.
    if raw_other_ratio > 0.80:
        penalty += 3

    overall_score = clamp_score(overall_score - penalty)

    if extraction_quality == "success" and transactions:
        overall_score = max(35, overall_score)

    return {
        "saving_behavior": saving_behavior,
        "subscription_control": subscription_control,
        "debt_risk": debt_risk,
        "impulse_spending": impulse_spending,
        "income_stability": income_stability,
        "overall_financial_habits_score": overall_score,
        "extraction_quality": extraction_quality,
        "metrics": {
            "income_detected": round(income, 2),
            "income_source": income_source,
            "expenses_detected": round(expenses, 2),
            "net_cashflow_detected": round(net_cashflow, 2),
            "subscription_total": round(subscription_total, 2),
            "subscription_count": subscription_count,
            "savings_rate_percent": round(savings_rate * 100, 2),
            "expense_ratio_percent": round(expense_ratio * 100, 2),
            "subscription_ratio_percent": round(subscription_ratio * 100, 2),
            "other_ratio_percent": round(raw_other_ratio * 100, 2),
            "discretionary_ratio_percent": round(raw_discretionary_ratio * 100, 2),
            "score_penalty": penalty,
            "extraction_quality": extraction_quality,
        },
    }
