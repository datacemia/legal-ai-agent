def build_recommended_budget(
    transactions: list[dict],
    fallback_income: float | None = None,
    output_language: str = "en",
) -> dict:
    income = sum(
        t["amount"]
        for t in transactions
        if t.get("type") == "income" and t.get("amount", 0) > 0
    )

    expenses = sum(
        abs(t["amount"])
        for t in transactions
        if t.get("type") == "expense" and t.get("amount", 0) < 0
    )

    if income <= 0 and expenses <= 0 and not fallback_income:
        return {}

    if income > 0:
        estimated_income = income
        income_source = "transactions"
    elif fallback_income:
        estimated_income = float(fallback_income)
        income_source = "ai_fallback"
    else:
        estimated_income = expenses
        income_source = "estimated_from_expenses"

    needs_budget = round(estimated_income * 0.50, 2)
    wants_budget = round(estimated_income * 0.30, 2)
    savings_target = round(estimated_income * 0.20, 2)

    emergency_fund_target = round(estimated_income * 0.10, 2)
    max_safe_spending = round(estimated_income - savings_target, 2)

    current_savings_gap = round(
        max(0, expenses - max_safe_spending),
        2,
    )

    if expenses > estimated_income:
        status = "over_budget"

        message = {
            "en": (
                "Your current spending is higher than your estimated income."
            ),
            "fr": (
                "Vos dépenses actuelles sont supérieures à votre revenu estimé."
            ),
            "ar": (
                "مصاريفك الحالية أعلى من دخلك التقديري."
            ),
        }.get(output_language)

    elif expenses > max_safe_spending:
        status = "needs_attention"

        message = {
            "en": (
                "Your spending is within income but above the recommended safe level."
            ),
            "fr": (
                "Vos dépenses restent inférieures à vos revenus mais dépassent le niveau recommandé."
            ),
            "ar": (
                "مصاريفك أقل من دخلك ولكنها تتجاوز المستوى الآمن الموصى به."
            ),
        }.get(output_language)

    else:
        status = "healthy"

        message = {
            "en": (
                "Your spending is within the recommended safe level."
            ),
            "fr": (
                "Vos dépenses restent dans le niveau recommandé."
            ),
            "ar": (
                "مصاريفك ضمن المستوى الآمن الموصى به."
            ),
        }.get(output_language)

    return {
        "income_source": income_source,
        "estimated_monthly_income": round(estimated_income, 2),
        "current_monthly_expenses": round(expenses, 2),
        "needs": needs_budget,
        "wants": wants_budget,
        "savings_target": savings_target,
        "emergency_fund_target": emergency_fund_target,
        "max_safe_spending": max_safe_spending,
        "current_savings_gap": current_savings_gap,
        "status": status,
        "message": message,
        "recommended_budget": {
            "needs": needs_budget,
            "wants": wants_budget,
            "savings": savings_target,
            "emergency_fund": emergency_fund_target,
        },
    }