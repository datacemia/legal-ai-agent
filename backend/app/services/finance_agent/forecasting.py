def predict_cashflow(
    transactions: list[dict],
    fallback_income: float | None = None,
    output_language: str = "en",
) -> dict:
    detected_income = sum(
        t["amount"]
        for t in transactions
        if t.get("type") == "income"
        and t.get("amount", 0) > 0
    )

    expenses = sum(
        abs(t["amount"])
        for t in transactions
        if t.get("type") == "expense"
        and t.get("amount", 0) < 0
    )

    income = detected_income

    if income <= 0 and fallback_income:
        income = float(fallback_income)

    income_source = (
        "transactions"
        if detected_income > 0
        else "ai_fallback"
        if fallback_income
        else "not_detected"
    )

    net_cashflow = income - expenses

    daily_burn = (
        expenses / 30
        if expenses > 0
        else 0
    )

    days_until_cash_risk = (
        0
        if net_cashflow <= 0
        else round(net_cashflow / daily_burn)
        if daily_burn > 0
        else None
    )

    if net_cashflow < 0:
        trend = "negative"
        message = {
            "en": "Your expenses exceed your income.",
            "fr": "Vos dépenses dépassent vos revenus.",
            "ar": "مصاريفك تتجاوز دخلك.",
        }.get(output_language, "Your expenses exceed your income.")

    elif income > 0 and net_cashflow > income * 0.2:
        trend = "improving"
        message = {
            "en": "Your balance trend is improving.",
            "fr": "La tendance de votre solde s’améliore.",
            "ar": "اتجاه الرصيد في تحسن.",
        }.get(output_language, "Your balance trend is improving.")

    elif income == 0 and expenses > 0:
        trend = "risky"
        message = {
            "en": "No income was detected while expenses exist.",
            "fr": "Aucun revenu n’a été détecté alors que des dépenses existent.",
            "ar": "لم يتم اكتشاف دخل بينما توجد مصاريف.",
        }.get(output_language, "No income was detected while expenses exist.")

    else:
        trend = "stable"
        message = {
            "en": "Your cashflow is relatively stable.",
            "fr": "Votre trésorerie est relativement stable.",
            "ar": "تدفقك النقدي مستقر نسبياً.",
        }.get(output_language, "Your cashflow is relatively stable.")

    return {
        "income_source": income_source,

        # legacy fields (keep for compatibility)
        "monthly_income": round(income, 2),
        "monthly_expenses": round(expenses, 2),

        # new explicit fields
        "observed_income": round(income, 2),
        "observed_expenses": round(expenses, 2),
        "observed_net_cashflow": round(
            net_cashflow,
            2,
        ),

        "net_cashflow": round(
            net_cashflow,
            2,
        ),
        "estimated_daily_burn": round(
            daily_burn,
            2,
        ),
        "days_until_cash_risk": days_until_cash_risk,
        "trend": trend,
        "message": message,
    }
