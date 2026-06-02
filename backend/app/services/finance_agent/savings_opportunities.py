from __future__ import annotations

from collections import defaultdict
import re


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
    "TOO_MANY_SUBSCRIPTIONS_ISSUE": {
        "en": "Too many recurring subscriptions",
        "fr": "Trop d'abonnements récurrents",
        "ar": "عدد كبير من الاشتراكات المتكررة",
    },
    "TOO_MANY_SUBSCRIPTIONS_ACTION": {
        "en": "Reduce the number of active subscriptions.",
        "fr": "Réduisez le nombre d'abonnements actifs.",
        "ar": "قلّل عدد الاشتراكات النشطة.",
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
        "en": "Multiple charges detected for {merchant}",
        "fr": "Plusieurs prélèvements détectés pour {merchant}",
        "ar": "تم اكتشاف عدة عمليات خصم لـ {merchant}",
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


def detect_savings_opportunities(
    transactions: list[dict],
    subscriptions: list[dict],
    output_language: str = "en",
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
                "issue": t("HIGH_SUBSCRIPTION_SPENDING_ISSUE", output_language),
                "severity": "medium",
                "estimated_savings_opportunity": round(
                    subscription_total * 0.35,
                    2,
                ),
                "action": t("HIGH_SUBSCRIPTION_SPENDING_ACTION", output_language),
            }
        )

    # 🔥 Too many subscriptions
    if len(subscriptions) >= 5:
        opportunities.append(
            {
                "issue": t("TOO_MANY_SUBSCRIPTIONS_ISSUE", output_language),
                "severity": "high",
                "estimated_savings_opportunity": round(
                    subscription_total * 0.20,
                    2,
                ),
                "action": t("TOO_MANY_SUBSCRIPTIONS_ACTION", output_language),
            }
        )

    # 🔥 Overspending
    if total_expenses >= 5000:
        opportunities.append(
            {
                "issue": t("HIGH_SPENDING_ISSUE", output_language),
                "severity": "high",
                "estimated_savings_opportunity": round(
                    total_expenses * 0.10,
                    2,
                ),
                "action": t("HIGH_SPENDING_ACTION", output_language),
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
                        "issue": t(
                            "MULTIPLE_CHARGES_ISSUE",
                            output_language,
                            merchant=merchant,
                        ),
                        "severity": "medium",
                        "estimated_savings_opportunity": round(
                            matching_sub["monthly_cost"] * 0.50,
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
