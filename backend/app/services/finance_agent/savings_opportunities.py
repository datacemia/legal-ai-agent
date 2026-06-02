from __future__ import annotations


TEXT = {
    "HIGH_SUBSCRIPTION_SPENDING_ISSUE": {
        "en": "High subscription spending",
        "fr": "Dépenses d'abonnements élevées",
        "ar": "إنفاق مرتفع على الاشتراكات",
    },
    "HIGH_SUBSCRIPTION_SPENDING_ACTION": {
        "en": "Review unused subscriptions and cancel unnecessary services.",
        "fr": "Passez en revue les abonnements inutilisés et annulez les services non nécessaires.",
        "ar": "راجع الاشتراكات غير المستخدمة وألغِ الخدمات غير الضرورية.",
    },
    "HIGH_SPENDING_ISSUE": {
        "en": "High spending detected",
        "fr": "Dépenses élevées détectées",
        "ar": "تم اكتشاف إنفاق مرتفع",
    },
    "HIGH_SPENDING_ACTION": {
        "en": "Reduce discretionary spending and monitor card payments.",
        "fr": "Réduire les dépenses discrétionnaires et surveiller les paiements par carte.",
        "ar": "قلّل الإنفاق غير الضروري وراقب مدفوعات البطاقة.",
    },
    "MULTIPLE_CHARGES_ISSUE": {
        "en": "Multiple meaningful charges detected for {merchant}",
        "fr": "Plusieurs prélèvements significatifs détectés pour {merchant}",
        "ar": "تم اكتشاف عدة عمليات خصم مهمة لـ {merchant}",
    },
    "MULTIPLE_CHARGES_ACTION": {
        "en": "Check whether all {merchant} charges are necessary.",
        "fr": "Vérifiez si tous les prélèvements {merchant} sont nécessaires.",
        "ar": "تحقق مما إذا كانت جميع عمليات خصم {merchant} ضرورية.",
    },
}


def t(key: str, output_language: str = "en", **kwargs) -> str:
    """Return translated text for a key, falling back to English then the key itself."""
    template = TEXT.get(key, {}).get(
        output_language,
        TEXT.get(key, {}).get("en", key),
    )
    return template.format(**kwargs) if kwargs else template


def safe_float(value: object) -> float:
    try:
        return float(value or 0)
    except (TypeError, ValueError):
        return 0.0


def detect_savings_opportunities(
    transactions: list[dict],
    subscriptions: list[dict],
    output_language: str = "en",
) -> list[dict]:
    opportunities = []

    expenses = [
        tx
        for tx in transactions
        if tx.get("type") == "expense"
    ]

    total_expenses = sum(
        abs(safe_float(tx.get("amount", 0)))
        for tx in expenses
    )

    income = sum(
        safe_float(tx.get("amount", 0))
        for tx in transactions
        if tx.get("type") == "income"
        and safe_float(tx.get("amount", 0)) > 0
    )

    net_cashflow = income - total_expenses

    expense_ratio = (
        total_expenses / income
        if income > 0
        else 1
    )

    savings_rate = (
        net_cashflow / income
        if income > 0
        else 0
    )

    subscription_total = sum(
        safe_float(subscription.get("monthly_cost", 0))
        for subscription in subscriptions
    )

    subscription_ratio = (
        subscription_total / income
        if income > 0
        else 0
    )

    # 🔥 Subscription waste
    # General rule:
    # only flag subscription waste when subscriptions consume more than 5%
    # of observed income. Do not use fixed currency thresholds or counts.
    if subscription_ratio > 0.05:
        opportunities.append(
            {
                "issue": t(
                    "HIGH_SUBSCRIPTION_SPENDING_ISSUE",
                    output_language,
                ),
                "severity": "medium",
                "estimated_savings_opportunity": round(
                    subscription_total * 0.35,
                    2,
                ),
                "action": t(
                    "HIGH_SUBSCRIPTION_SPENDING_ACTION",
                    output_language,
                ),
            }
        )

    # 🔥 Overspending
    # General rule:
    # only recommend spending reduction when expenses consume more than 75%
    # of income or when the observed savings rate is below 15%.
    if expense_ratio > 0.75 or savings_rate < 0.15:
        opportunities.append(
            {
                "issue": t(
                    "HIGH_SPENDING_ISSUE",
                    output_language,
                ),
                "severity": "high",
                "estimated_savings_opportunity": round(
                    total_expenses * 0.10,
                    2,
                ),
                "action": t(
                    "HIGH_SPENDING_ACTION",
                    output_language,
                ),
            }
        )

    # 🔥 Duplicate subscription detection
    # General rule:
    # multiple charges are only meaningful if subscriptions are already
    # financially significant relative to income.
    if subscription_ratio > 0.05:
        for subscription in subscriptions:
            merchant = subscription.get("name")
            transactions_count = int(
                subscription.get("transactions_count", 0) or 0
            )
            monthly_cost = safe_float(
                subscription.get("monthly_cost", 0)
            )

            merchant_ratio = (
                monthly_cost / income
                if income > 0
                else 0
            )

            if (
                not merchant
                or transactions_count < 3
                or merchant_ratio <= 0.02
            ):
                continue

            opportunities.append(
                {
                    "issue": t(
                        "MULTIPLE_CHARGES_ISSUE",
                        output_language,
                        merchant=merchant,
                    ),
                    "severity": "medium",
                    "estimated_savings_opportunity": round(
                        monthly_cost * 0.50,
                        2,
                    ),
                    "action": t(
                        "MULTIPLE_CHARGES_ACTION",
                        output_language,
                        merchant=merchant,
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
