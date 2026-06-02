from collections import defaultdict


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

    savings_rate = (
        net / income
        if income > 0
        else 0
    )

    expense_ratio = (
        expenses / income
        if income > 0
        else 1
    )

    subscription_ratio = (
        subscription_total / income
        if income > 0
        else 0
    )

    category_totals = defaultdict(float)

    for t in transactions:
        if t.get("type") == "expense":
            category = str(
                t.get("category") or "other"
            ).lower()

            category_totals[category] += abs(
                float(t.get("amount", 0) or 0)
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

    # 🔥 Universal financial position insight
    if savings_rate >= 0.30 and expense_ratio <= 0.70:
        financial_position_type = "positive"
        financial_position_title = {
            "en": "Strong financial position",
            "fr": "Situation financière solide",
            "ar": "وضع مالي قوي",
        }.get(
            output_language,
            "Strong financial position",
        )

        financial_position_message = {
            "en": "Your savings rate is strong and your expenses remain controlled compared with income.",
            "fr": "Votre taux d’épargne est élevé et vos dépenses restent maîtrisées par rapport à vos revenus.",
            "ar": "معدل ادخارك قوي ومصاريفك ما زالت تحت السيطرة مقارنة بدخلك.",
        }.get(
            output_language,
            "Your savings rate is strong and your expenses remain controlled compared with income.",
        )

    elif savings_rate >= 0.15 and expense_ratio <= 0.85:
        financial_position_type = "positive"
        financial_position_title = {
            "en": "Healthy financial position",
            "fr": "Situation financière saine",
            "ar": "وضع مالي صحي",
        }.get(
            output_language,
            "Healthy financial position",
        )

        financial_position_message = {
            "en": "Your financial position appears healthy, with a reasonable balance between income, expenses, and savings.",
            "fr": "Votre situation financière semble saine, avec un bon équilibre entre revenus, dépenses et épargne.",
            "ar": "يبدو وضعك المالي صحيًا، مع توازن مقبول بين الدخل والمصاريف والادخار.",
        }.get(
            output_language,
            "Your financial position appears healthy, with a reasonable balance between income, expenses, and savings.",
        )

    elif savings_rate >= 0.05:
        financial_position_type = "tip"
        financial_position_title = {
            "en": "Moderate financial position",
            "fr": "Situation financière modérée",
            "ar": "وضع مالي متوسط",
        }.get(
            output_language,
            "Moderate financial position",
        )

        financial_position_message = {
            "en": "You are saving some income, but your financial margin could be improved.",
            "fr": "Vous épargnez une partie de vos revenus, mais votre marge financière pourrait être améliorée.",
            "ar": "أنت تدخر جزءًا من دخلك، لكن يمكن تحسين هامشك المالي.",
        }.get(
            output_language,
            "You are saving some income, but your financial margin could be improved.",
        )

    else:
        financial_position_type = "warning"
        financial_position_title = {
            "en": "Financial pressure detected",
            "fr": "Pression financière détectée",
            "ar": "تم اكتشاف ضغط مالي",
        }.get(
            output_language,
            "Financial pressure detected",
        )

        financial_position_message = {
            "en": "Your current income, expenses, and savings suggest financial pressure.",
            "fr": "Vos revenus, dépenses et économies actuels indiquent une pression financière.",
            "ar": "يشير دخلك ومصاريفك وادخارك الحالي إلى وجود ضغط مالي.",
        }.get(
            output_language,
            "Your current income, expenses, and savings suggest financial pressure.",
        )

    insights.append(
        {
            "type": financial_position_type,
            "title": financial_position_title,
            "message": financial_position_message,
        }
    )

    # 🔥 General spending level insight
    if expense_ratio > 0.90:
        insights.append(
            {
                "type": "warning",
                "title": {
                    "en": "Very high expense ratio",
                    "fr": "Ratio de dépenses très élevé",
                    "ar": "نسبة مصاريف مرتفعة جدًا",
                }.get(
                    output_language,
                    "Very high expense ratio",
                ),
                "message": {
                    "en": "Your expenses consume most of your income.",
                    "fr": "Vos dépenses consomment la majeure partie de vos revenus.",
                    "ar": "مصاريفك تستهلك معظم دخلك.",
                }.get(
                    output_language,
                    "Your expenses consume most of your income.",
                ),
            }
        )

    elif expense_ratio > 0.75:
        insights.append(
            {
                "type": "warning",
                "title": {
                    "en": "Elevated spending level",
                    "fr": "Niveau de dépenses élevé",
                    "ar": "مستوى إنفاق مرتفع",
                }.get(
                    output_language,
                    "Elevated spending level",
                ),
                "message": {
                    "en": "Your spending level is elevated compared with income.",
                    "fr": "Votre niveau de dépenses est élevé par rapport à vos revenus.",
                    "ar": "مستوى إنفاقك مرتفع مقارنة بدخلك.",
                }.get(
                    output_language,
                    "Your spending level is elevated compared with income.",
                ),
            }
        )

    elif expense_ratio > 0.60:
        insights.append(
            {
                "type": "tip",
                "title": {
                    "en": "Moderate spending level",
                    "fr": "Niveau de dépenses modéré",
                    "ar": "مستوى إنفاق متوسط",
                }.get(
                    output_language,
                    "Moderate spending level",
                ),
                "message": {
                    "en": "Your spending is moderate but should be monitored.",
                    "fr": "Vos dépenses sont modérées mais doivent être surveillées.",
                    "ar": "إنفاقك متوسط لكنه يحتاج إلى متابعة.",
                }.get(
                    output_language,
                    "Your spending is moderate but should be monitored.",
                ),
            }
        )

    category_totals.pop("other", None)

    # 🔥 Category ratio insights
    for category, amount in category_totals.items():
        ratio = (
            amount / expenses
            if expenses > 0
            else 0
        )

        if ratio >= 0.40:
            insights.append(
                {
                    "type": "warning",
                    "title": {
                        "en": "Dominant spending category",
                        "fr": "Catégorie de dépenses dominante",
                        "ar": "فئة إنفاق مهيمنة",
                    }.get(
                        output_language,
                        "Dominant spending category",
                    ),
                    "message": {
                        "en": f"{category} is your dominant spending category.",
                        "fr": f"{category} représente votre catégorie de dépenses dominante.",
                        "ar": f"{category} هي فئة الإنفاق المهيمنة لديك.",
                    }.get(
                        output_language,
                        f"{category} is your dominant spending category.",
                    ),
                }
            )

        elif ratio >= 0.20:
            insights.append(
                {
                    "type": "tip",
                    "title": {
                        "en": "Significant spending category",
                        "fr": "Catégorie de dépenses significative",
                        "ar": "فئة إنفاق مهمة",
                    }.get(
                        output_language,
                        "Significant spending category",
                    ),
                    "message": {
                        "en": f"{category} represents a significant share of expenses.",
                        "fr": f"{category} représente une part importante des dépenses.",
                        "ar": f"{category} تمثل جزءًا مهمًا من المصاريف.",
                    }.get(
                        output_language,
                        f"{category} represents a significant share of expenses.",
                    ),
                }
            )

    # 🔥 Subscription pressure
    if income > 0:
        ratio = subscription_ratio * 100

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

    return insights
