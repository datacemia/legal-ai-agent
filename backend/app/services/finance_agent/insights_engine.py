def generate_financial_insights(
    transactions: list[dict],
    subscriptions: list[dict],
    scores: dict,
    forecast: dict,
    opportunities: list[dict],
    currency: str = "MAD",
    output_language: str = "en",
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
                "title": {
                    "en": "Positive cashflow detected",
                    "fr": "Trésorerie positive détectée",
                    "ar": "تم اكتشاف تدفق نقدي إيجابي",
                }.get(
                    output_language,
                    "Positive cashflow detected",
                ),
                "message": {
                    "en": (
                        f"You currently retain approximately "
                        f"{round(net, 2)} {currency} after expenses."
                    ),
                    "fr": (
                        f"Vous conservez actuellement environ "
                        f"{round(net, 2)} {currency} après vos dépenses."
                    ),
                    "ar": (
                        f"تحتفظ حاليًا بحوالي "
                        f"{round(net, 2)} {currency} بعد المصاريف."
                    ),
                }.get(
                    output_language,
                    (
                        f"You currently retain approximately "
                        f"{round(net, 2)} {currency} after expenses."
                    ),
                ),
            }
        )

    else:
        insights.append(
            {
                "type": "warning",
                "title": {
                    "en": "Negative cashflow risk",
                    "fr": "Risque de trésorerie négative",
                    "ar": "خطر تدفق نقدي سلبي",
                }.get(
                    output_language,
                    "Negative cashflow risk",
                ),
                "message": {
                    "en": "Your current expenses exceed your income.",
                    "fr": "Vos dépenses actuelles dépassent vos revenus.",
                    "ar": "مصاريفك الحالية تتجاوز دخلك.",
                }.get(
                    output_language,
                    "Your current expenses exceed your income.",
                ),
            }
        )

    # 🔥 Score insight
    if score >= 80:
        insights.append(
            {
                "type": "positive",
                "title": {
                    "en": "Excellent financial habits",
                    "fr": "Excellentes habitudes financières",
                    "ar": "عادات مالية ممتازة",
                }.get(
                    output_language,
                    "Excellent financial habits",
                ),
                "message": {
                    "en": "Your financial behavior appears healthy and stable.",
                    "fr": "Votre comportement financier semble sain et stable.",
                    "ar": "يبدو أن سلوكك المالي صحي ومستقر.",
                }.get(
                    output_language,
                    "Your financial behavior appears healthy and stable.",
                ),
            }
        )

    elif score < 50:
        insights.append(
            {
                "type": "warning",
                "title": {
                    "en": "Financial habits need improvement",
                    "fr": "Les habitudes financières doivent être améliorées",
                    "ar": "العادات المالية تحتاج إلى تحسين",
                }.get(
                    output_language,
                    "Financial habits need improvement",
                ),
                "message": {
                    "en": "Your spending patterns may require closer monitoring.",
                    "fr": "Vos habitudes de dépense peuvent nécessiter un suivi plus attentif.",
                    "ar": "قد تتطلب أنماط إنفاقك مراقبة أدق.",
                }.get(
                    output_language,
                    "Your spending patterns may require closer monitoring.",
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
                    "title": {
                        "en": "High subscription pressure",
                        "fr": "Pression élevée des abonnements",
                        "ar": "ضغط مرتفع من الاشتراكات",
                    }.get(
                        output_language,
                        "High subscription pressure",
                    ),
                    "message": {
                        "en": (
                            f"Subscriptions consume approximately "
                            f"{round(ratio, 1)}% of your income."
                        ),
                        "fr": (
                            f"Les abonnements consomment environ "
                            f"{round(ratio, 1)}% de vos revenus."
                        ),
                        "ar": (
                            f"تستهلك الاشتراكات حوالي "
                            f"{round(ratio, 1)}% من دخلك."
                        ),
                    }.get(
                        output_language,
                        (
                            f"Subscriptions consume approximately "
                            f"{round(ratio, 1)}% of your income."
                        ),
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
                "title": {
                    "en": "Savings opportunities detected",
                    "fr": "Opportunités d’économies détectées",
                    "ar": "تم اكتشاف فرص للتوفير",
                }.get(
                    output_language,
                    "Savings opportunities detected",
                ),
                "message": {
                    "en": (
                        f"Potential savings opportunities identified: "
                        f"{round(estimated, 2)} {currency}."
                    ),
                    "fr": (
                        f"Opportunités d’économies potentielles identifiées : "
                        f"{round(estimated, 2)} {currency}."
                    ),
                    "ar": (
                        f"تم تحديد فرص توفير محتملة: "
                        f"{round(estimated, 2)} {currency}."
                    ),
                }.get(
                    output_language,
                    (
                        f"Potential savings opportunities identified: "
                        f"{round(estimated, 2)} {currency}."
                    ),
                ),
            }
        )

    # 🔥 Expense intensity
    if expenses >= 5000:
        insights.append(
            {
                "type": "warning",
                "title": {
                    "en": "High spending intensity",
                    "fr": "Intensité de dépenses élevée",
                    "ar": "مستوى إنفاق مرتفع",
                }.get(
                    output_language,
                    "High spending intensity",
                ),
                "message": {
                    "en": "Your observed expenses are relatively high.",
                    "fr": "Vos dépenses observées sont relativement élevées.",
                    "ar": "مصاريفك المسجلة مرتفعة نسبيًا.",
                }.get(
                    output_language,
                    "Your observed expenses are relatively high.",
                ),
            }
        )

    return insights
