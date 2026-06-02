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

    subscription_count = len(subscriptions)

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

    category_totals.pop(
        "other",
        None,
    )

    dominant_category = None
    dominant_category_amount = 0

    if category_totals:
        dominant_category, dominant_category_amount = max(
            category_totals.items(),
            key=lambda item: item[1],
        )

    dominant_ratio = (
        dominant_category_amount / expenses
        if expenses > 0
        else 0
    )

    # 🔥 Cashflow risk
    if net < 0:
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

    # 🔥 Savings capacity levels
    if savings_rate >= 0.30:
        insights.append(
            {
                "type": "positive",
                "title": {
                    "en": "Excellent savings capacity",
                    "fr": "Excellente capacité d’épargne",
                    "ar": "قدرة ممتازة على الادخار",
                }.get(
                    output_language,
                    "Excellent savings capacity",
                ),
                "message": {
                    "en": (
                        f"You retain approximately "
                        f"{round(savings_rate * 100, 1)}% of your income after expenses."
                    ),
                    "fr": (
                        f"Vous conservez environ "
                        f"{round(savings_rate * 100, 1)}% de vos revenus après dépenses."
                    ),
                    "ar": (
                        f"تحتفظ بحوالي "
                        f"{round(savings_rate * 100, 1)}% من دخلك بعد المصاريف."
                    ),
                }.get(
                    output_language,
                    (
                        f"You retain approximately "
                        f"{round(savings_rate * 100, 1)}% of your income after expenses."
                    ),
                ),
            }
        )

    elif savings_rate >= 0.15:
        insights.append(
            {
                "type": "positive",
                "title": {
                    "en": "Healthy savings capacity",
                    "fr": "Capacité d’épargne saine",
                    "ar": "قدرة صحية على الادخار",
                }.get(
                    output_language,
                    "Healthy savings capacity",
                ),
                "message": {
                    "en": (
                        f"You retain approximately "
                        f"{round(savings_rate * 100, 1)}% of your income after expenses."
                    ),
                    "fr": (
                        f"Vous conservez environ "
                        f"{round(savings_rate * 100, 1)}% de vos revenus après dépenses."
                    ),
                    "ar": (
                        f"تحتفظ بحوالي "
                        f"{round(savings_rate * 100, 1)}% من دخلك بعد المصاريف."
                    ),
                }.get(
                    output_language,
                    (
                        f"You retain approximately "
                        f"{round(savings_rate * 100, 1)}% of your income after expenses."
                    ),
                ),
            }
        )

    else:
        insights.append(
            {
                "type": "warning",
                "title": {
                    "en": "Limited savings capacity",
                    "fr": "Capacité d’épargne limitée",
                    "ar": "قدرة محدودة على الادخار",
                }.get(
                    output_language,
                    "Limited savings capacity",
                ),
                "message": {
                    "en": "Your current income and expenses leave limited room for savings.",
                    "fr": "Vos revenus et dépenses actuels laissent une marge limitée pour l’épargne.",
                    "ar": "دخلك ومصاريفك الحالية تترك مجالًا محدودًا للادخار.",
                }.get(
                    output_language,
                    "Your current income and expenses leave limited room for savings.",
                ),
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

    # 🔥 Dominant category insight
    if dominant_category and dominant_ratio > 0.40:
        insights.append(
            {
                "type": "warning",
                "title": {
                    "en": "Primary expense category",
                    "fr": "Catégorie principale de dépenses",
                    "ar": "فئة المصاريف الرئيسية",
                }.get(
                    output_language,
                    "Primary expense category",
                ),
                "message": {
                    "en": f"{dominant_category} is the primary expense category.",
                    "fr": f"{dominant_category} est la principale catégorie de dépenses.",
                    "ar": f"{dominant_category} هي فئة المصاريف الرئيسية.",
                }.get(
                    output_language,
                    f"{dominant_category} is the primary expense category.",
                ),
            }
        )

    # 🔥 Subscription pressure
    if subscription_count > 0 and income > 0:
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
    filtered_opportunities = []

    for opportunity in opportunities:
        recommendation = str(
            opportunity.get("recommendation") or ""
        ).lower()

        action = str(
            opportunity.get("action") or ""
        ).lower()

        issue = str(
            opportunity.get("issue") or ""
        ).lower()

        text = f"{issue} {recommendation} {action}"

        if subscription_count == 0 and "subscription" in text:
            continue

        if savings_rate >= 0.15 and (
            "increase savings" in text
            or "savings contribution" in text
            or "savings contributions" in text
            or "increase savings contributions" in text
        ):
            continue

        if expense_ratio < 0.60 and (
            "reduce spending" in text
            or "reduce discretionary spending" in text
            or "spending reduction" in text
            or "reduce expenses" in text
        ):
            continue

        filtered_opportunities.append(opportunity)

    if filtered_opportunities:
        estimated = sum(
            o.get(
                "estimated_savings_opportunity",
                0,
            )
            for o in filtered_opportunities
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
