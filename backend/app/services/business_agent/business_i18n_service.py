from copy import deepcopy
from typing import Any


SUPPORTED_LANGUAGES = {"en", "fr", "ar"}


def normalize_language(language: str | None) -> str:
    normalized = str(language or "en").lower().strip()

    if normalized in {"english", "anglais", "eng"}:
        return "en"

    if normalized in {"french", "français", "francais", "fra"}:
        return "fr"

    if normalized in {"arabic", "العربية", "arabe", "ara"}:
        return "ar"

    if normalized not in SUPPORTED_LANGUAGES:
        return "en"

    return normalized


TERM_TRANSLATIONS: dict[str, dict[str, str]] = {
    # Severity / status
    "critical": {
        "en": "Critical",
        "fr": "Critique",
        "ar": "حرج",
    },
    "high": {
        "en": "High",
        "fr": "Élevé",
        "ar": "مرتفع",
    },
    "medium": {
        "en": "Medium",
        "fr": "Moyen",
        "ar": "متوسط",
    },
    "low": {
        "en": "Low",
        "fr": "Faible",
        "ar": "منخفض",
    },
    "info": {
        "en": "Info",
        "fr": "Info",
        "ar": "معلومة",
    },
    "healthy": {
        "en": "Healthy",
        "fr": "Sain",
        "ar": "صحي",
    },
    "watch": {
        "en": "Watch",
        "fr": "À surveiller",
        "ar": "قيد المراقبة",
    },
    "normal": {
        "en": "Normal",
        "fr": "Normal",
        "ar": "طبيعي",
    },
    "critical_status": {
        "en": "Critical",
        "fr": "Critique",
        "ar": "حرج",
    },
    "high_risk": {
        "en": "High risk",
        "fr": "Risque élevé",
        "ar": "مخاطر مرتفعة",
    },
    "low_risk": {
        "en": "Low risk",
        "fr": "Risque faible",
        "ar": "مخاطر منخفضة",
    },
    "positive": {
        "en": "Positive",
        "fr": "Positif",
        "ar": "إيجابي",
    },
    "negative": {
        "en": "Negative",
        "fr": "Négatif",
        "ar": "سلبي",
    },
    "unknown": {
        "en": "Unknown",
        "fr": "Inconnu",
        "ar": "غير معروف",
    },

    # Business model labels
    "saas": {
        "en": "SaaS / subscription",
        "fr": "SaaS / abonnement",
        "ar": "SaaS / اشتراك",
    },
    "ecommerce": {
        "en": "E-commerce",
        "fr": "E-commerce",
        "ar": "تجارة إلكترونية",
    },
    "agency": {
        "en": "Agency / services",
        "fr": "Agence / services",
        "ar": "وكالة / خدمات",
    },
    "restaurant": {
        "en": "Restaurant / hospitality",
        "fr": "Restaurant / hôtellerie",
        "ar": "مطعم / ضيافة",
    },
    "marketplace": {
        "en": "Marketplace",
        "fr": "Marketplace",
        "ar": "سوق رقمي",
    },
    "general": {
        "en": "General business",
        "fr": "Entreprise générale",
        "ar": "نشاط عام",
    },

    # KPI labels
    "revenue": {
        "en": "Revenue",
        "fr": "Revenus",
        "ar": "الإيرادات",
    },
    "expenses": {
        "en": "Expenses",
        "fr": "Dépenses",
        "ar": "المصاريف",
    },
    "profit": {
        "en": "Profit",
        "fr": "Profit",
        "ar": "الأرباح",
    },
    "profit_margin_percent": {
        "en": "Profit margin",
        "fr": "Marge bénéficiaire",
        "ar": "هامش الربح",
    },
    "growth_rate_percent": {
        "en": "Revenue growth",
        "fr": "Croissance des revenus",
        "ar": "نمو الإيرادات",
    },
    "cashflow_status": {
        "en": "Cashflow status",
        "fr": "Statut cashflow",
        "ar": "حالة التدفق النقدي",
    },
    "churn_rate_percent": {
        "en": "Customer churn",
        "fr": "Churn client",
        "ar": "معدل فقدان العملاء",
    },
    "roas": {
        "en": "ROAS",
        "fr": "ROAS",
        "ar": "عائد الإنفاق الإعلاني",
    },
    "cac": {
        "en": "CAC",
        "fr": "CAC",
        "ar": "تكلفة اكتساب العميل",
    },
    "aov": {
        "en": "Average order value",
        "fr": "Panier moyen",
        "ar": "متوسط قيمة الطلب",
    },
    "mrr": {
        "en": "MRR",
        "fr": "MRR",
        "ar": "الإيراد الشهري المتكرر",
    },
    "arr": {
        "en": "ARR",
        "fr": "ARR",
        "ar": "الإيراد السنوي المتكرر",
    },

    # Business impacts
    "retention_risk": {
        "en": "Retention risk",
        "fr": "Risque de rétention",
        "ar": "مخاطر الاحتفاظ بالعملاء",
    },
    "growth_quality_risk": {
        "en": "Growth quality risk",
        "fr": "Risque sur la qualité de croissance",
        "ar": "مخاطر جودة النمو",
    },
    "ltv_pressure": {
        "en": "LTV pressure",
        "fr": "Pression sur la LTV",
        "ar": "ضغط على قيمة العميل",
    },
    "marketing_efficiency": {
        "en": "Marketing efficiency",
        "fr": "Efficacité marketing",
        "ar": "كفاءة التسويق",
    },
    "positive_growth_quality": {
        "en": "Positive growth quality",
        "fr": "Qualité de croissance positive",
        "ar": "جودة نمو إيجابية",
    },
    "profitability_strength": {
        "en": "Profitability strength",
        "fr": "Solidité de la rentabilité",
        "ar": "قوة الربحية",
    },
    "cashflow_pressure": {
        "en": "Cashflow pressure",
        "fr": "Pression sur le cashflow",
        "ar": "ضغط على التدفق النقدي",
    },
    "forecast_risk": {
        "en": "Forecast risk",
        "fr": "Risque de prévision",
        "ar": "مخاطر التوقعات",
    },
    "margin_pressure": {
        "en": "Margin pressure",
        "fr": "Pression sur la marge",
        "ar": "ضغط على الهامش",
    },
    "profitability_risk": {
        "en": "Profitability risk",
        "fr": "Risque de rentabilité",
        "ar": "مخاطر الربحية",
    },
    "unit_economics_pressure": {
        "en": "Unit economics pressure",
        "fr": "Pression sur les unit economics",
        "ar": "ضغط على اقتصاديات الوحدة",
    },
    "cac_payback_risk": {
        "en": "CAC payback risk",
        "fr": "Risque de remboursement CAC",
        "ar": "مخاطر استرداد تكلفة اكتساب العميل",
    },

    # Health labels / signals
    "healthy_margin": {
        "en": "Healthy profit margin.",
        "fr": "Marge bénéficiaire saine.",
        "ar": "هامش ربح صحي.",
    },
    "healthy_growth": {
        "en": "Healthy growth.",
        "fr": "Croissance saine.",
        "ar": "نمو صحي.",
    },
    "positive_cashflow": {
        "en": "Positive cashflow.",
        "fr": "Cashflow positif.",
        "ar": "تدفق نقدي إيجابي.",
    },
    "critical_churn": {
        "en": "Critical churn level.",
        "fr": "Niveau de churn critique.",
        "ar": "مستوى فقدان عملاء حرج.",
    },
    "healthy_roas": {
        "en": "Healthy ROAS.",
        "fr": "ROAS sain.",
        "ar": "عائد إنفاق إعلاني صحي.",
    },
    "healthy_cac_efficiency": {
        "en": "Healthy CAC efficiency.",
        "fr": "Efficacité CAC saine.",
        "ar": "كفاءة تكلفة اكتساب العميل صحية.",
    },
    "excellent_data_quality": {
        "en": "Excellent data quality.",
        "fr": "Excellente qualité des données.",
        "ar": "جودة بيانات ممتازة.",
    },
}


PHRASE_TRANSLATIONS: dict[str, dict[str, str]] = {
    # Decision engine
    "Prioritize retention before scaling acquisition": {
        "en": "Prioritize retention before scaling acquisition",
        "fr": "Prioriser la rétention avant d’augmenter l’acquisition",
        "ar": "إعطاء الأولوية للاحتفاظ بالعملاء قبل توسيع الاكتساب",
    },
    "Analyze churn reasons and cancellation timing.": {
        "en": "Analyze churn reasons and cancellation timing.",
        "fr": "Analyser les raisons du churn et le moment des annulations.",
        "ar": "تحليل أسباب فقدان العملاء وتوقيت الإلغاءات.",
    },
    "Improve onboarding and customer success follow-up.": {
        "en": "Improve onboarding and customer success follow-up.",
        "fr": "Améliorer l’onboarding et le suivi customer success.",
        "ar": "تحسين تهيئة العملاء ومتابعة نجاح العملاء.",
    },
    "Prioritize churn reduction before increasing acquisition spend.": {
        "en": "Prioritize churn reduction before increasing acquisition spend.",
        "fr": "Prioriser la réduction du churn avant d’augmenter les dépenses d’acquisition.",
        "ar": "إعطاء الأولوية لتقليل فقدان العملاء قبل زيادة الإنفاق على الاكتساب.",
    },
    "High churn reduces growth quality and can make acquisition spend less efficient.": {
        "en": "High churn reduces growth quality and can make acquisition spend less efficient.",
        "fr": "Un churn élevé réduit la qualité de la croissance et peut rendre les dépenses d’acquisition moins efficaces.",
        "ar": "ارتفاع فقدان العملاء يقلل جودة النمو وقد يجعل إنفاق الاكتساب أقل كفاءة.",
    },
    "Customer churn is elevated.": {
        "en": "Customer churn is elevated.",
        "fr": "Le churn client est élevé.",
        "ar": "معدل فقدان العملاء مرتفع.",
    },
    "Estimated churn rate is 28.65%.": {
        "en": "Estimated churn rate is 28.65%.",
        "fr": "Le taux de churn estimé est de 28,65%.",
        "ar": "معدل فقدان العملاء المقدر هو 28.65٪.",
    },

    # Key insights templates
    "Revenue is {revenue} with profit of {profit}.": {
        "en": "Revenue is {revenue} with profit of {profit}.",
        "fr": "Les revenus sont de {revenue}, avec un profit de {profit}.",
        "ar": "بلغت الإيرادات {revenue} مع ربح قدره {profit}.",
    },
    "Profit margin is {margin}% and revenue growth is {growth}%.": {
        "en": "Profit margin is {margin}% and revenue growth is {growth}%.",
        "fr": "La marge bénéficiaire est de {margin}% et la croissance des revenus est de {growth}%.",
        "ar": "هامش الربح هو {margin}% ونمو الإيرادات هو {growth}%.",
    },
    "Customer churn is estimated at {churn}%, which affects retention quality.": {
        "en": "Customer churn is estimated at {churn}%, which affects retention quality.",
        "fr": "Le churn client est estimé à {churn}%, ce qui affecte la qualité de rétention.",
        "ar": "يُقدر معدل فقدان العملاء بـ {churn}%، مما يؤثر على جودة الاحتفاظ.",
    },
    "ROAS is {roas}, based on revenue and advertising spend.": {
        "en": "ROAS is {roas}, based on revenue and advertising spend.",
        "fr": "Le ROAS est de {roas}, basé sur les revenus et les dépenses publicitaires.",
        "ar": "عائد الإنفاق الإعلاني هو {roas}، بناءً على الإيرادات والإنفاق الإعلاني.",
    },
    "Business Health Score is {score}/100.": {
        "en": "Business Health Score is {score}/100.",
        "fr": "Le score de santé business est de {score}/100.",
        "ar": "درجة صحة النشاط هي {score}/100.",
    },
    "{total} business risk indicator(s) and {insights} positive business signal(s) were identified.": {
        "en": "{total} business risk indicator(s) and {insights} positive business signal(s) were identified.",
        "fr": "{total} indicateur(s) de risque business et {insights} signal(aux) positif(s) ont été identifiés.",
        "ar": "تم تحديد {total} مؤشر مخاطر للأعمال و{insights} إشارة إيجابية للأعمال.",
    },

    # Opportunities
    "Improve customer retention": {
        "en": "Improve customer retention",
        "fr": "Améliorer la rétention client",
        "ar": "تحسين الاحتفاظ بالعملاء",
    },
    "Scale efficient acquisition carefully": {
        "en": "Scale efficient acquisition carefully",
        "fr": "Développer l’acquisition efficace avec prudence",
        "ar": "توسيع الاكتساب الفعال بحذر",
    },
    "Use healthy profitability to fund focused growth": {
        "en": "Use healthy profitability to fund focused growth",
        "fr": "Utiliser la rentabilité saine pour financer une croissance ciblée",
        "ar": "استخدام الربحية الصحية لتمويل نمو مركز",
    },
    "Growth and profitability are both positive.": {
        "en": "Growth and profitability are both positive.",
        "fr": "La croissance et la rentabilité sont toutes deux positives.",
        "ar": "النمو والربحية كلاهما إيجابيان.",
    },
    "Marketing efficiency appears healthy.": {
        "en": "Marketing efficiency appears healthy.",
        "fr": "L’efficacité marketing semble saine.",
        "ar": "تبدو كفاءة التسويق صحية.",
    },
    "Latest profit is above recent average.": {
        "en": "Latest profit is above recent average.",
        "fr": "Le dernier profit est supérieur à la moyenne récente.",
        "ar": "آخر ربح أعلى من المتوسط الأخير.",
    },
    "Reducing churn can improve recurring revenue quality, LTV, and growth efficiency.": {
        "en": "Reducing churn can improve recurring revenue quality, LTV, and growth efficiency.",
        "fr": "Réduire le churn peut améliorer la qualité des revenus récurrents, la LTV et l’efficacité de croissance.",
        "ar": "تقليل فقدان العملاء يمكن أن يحسن جودة الإيرادات المتكررة وقيمة العميل وكفاءة النمو.",
    },
    "ROAS and CAC efficiency are healthy, which suggests acquisition can be scaled with monitoring.": {
        "en": "ROAS and CAC efficiency are healthy, which suggests acquisition can be scaled with monitoring.",
        "fr": "Le ROAS et l’efficacité CAC sont sains, ce qui suggère que l’acquisition peut être augmentée avec suivi.",
        "ar": "عائد الإنفاق الإعلاني وكفاءة تكلفة اكتساب العميل في وضع صحي، مما يشير إلى إمكانية توسيع الاكتساب مع المراقبة.",
    },
    "The business has both growth and profit margin strength.": {
        "en": "The business has both growth and profit margin strength.",
        "fr": "L’entreprise combine croissance et solidité de marge.",
        "ar": "النشاط يجمع بين النمو وقوة هامش الربح.",
    },
    "The business is growing while maintaining a healthy profit margin.": {
        "en": "The business is growing while maintaining a healthy profit margin.",
        "fr": "L’entreprise progresse tout en conservant une marge bénéficiaire saine.",
        "ar": "النشاط ينمو مع الحفاظ على هامش ربح صحي.",
    },
    "ROAS is in a healthy range, suggesting acquisition spend is producing return.": {
        "en": "ROAS is in a healthy range, suggesting acquisition spend is producing return.",
        "fr": "Le ROAS est dans une zone saine, ce qui suggère que les dépenses d’acquisition génèrent un retour.",
        "ar": "عائد الإنفاق الإعلاني ضمن نطاق صحي، مما يشير إلى أن إنفاق الاكتساب يحقق عائدًا.",
    },
    "Convert this positive signal into a repeatable operating process.": {
        "en": "Convert this positive signal into a repeatable operating process.",
        "fr": "Transformer ce signal positif en processus opérationnel répétable.",
        "ar": "تحويل هذه الإشارة الإيجابية إلى عملية تشغيلية قابلة للتكرار.",
    },
    "Launch retention analysis, improve onboarding, and segment churn by acquisition channel.": {
        "en": "Launch retention analysis, improve onboarding, and segment churn by acquisition channel.",
        "fr": "Lancer une analyse de rétention, améliorer l’onboarding et segmenter le churn par canal d’acquisition.",
        "ar": "إطلاق تحليل للاحتفاظ، وتحسين تهيئة العملاء، وتقسيم فقدان العملاء حسب قناة الاكتساب.",
    },
    "Increase spend only on channels with proven ROAS and monitor churn quality.": {
        "en": "Increase spend only on channels with proven ROAS and monitor churn quality.",
        "fr": "Augmenter les dépenses uniquement sur les canaux avec ROAS prouvé et surveiller la qualité du churn.",
        "ar": "زيادة الإنفاق فقط على القنوات ذات عائد إنفاق إعلاني مثبت ومراقبة جودة فقدان العملاء.",
    },
    "Allocate budget to the highest-return growth or retention initiative.": {
        "en": "Allocate budget to the highest-return growth or retention initiative.",
        "fr": "Allouer le budget à l’initiative de croissance ou de rétention au meilleur retour.",
        "ar": "تخصيص الميزانية لمبادرة النمو أو الاحتفاظ ذات أعلى عائد.",
    },

    # Recommendations
    "Improves retention, LTV, and recurring revenue stability.": {
        "en": "Improves retention, LTV, and recurring revenue stability.",
        "fr": "Améliore la rétention, la LTV et la stabilité des revenus récurrents.",
        "ar": "يحسن الاحتفاظ وقيمة العميل واستقرار الإيرادات المتكررة.",
    },

    # Memory / forecast / disclaimers
    "No major business change detected compared with the previous analysis.": {
        "en": "No major business change detected compared with the previous analysis.",
        "fr": "Aucun changement business majeur détecté par rapport à l’analyse précédente.",
        "ar": "لم يتم اكتشاف تغيير تجاري كبير مقارنة بالتحليل السابق.",
    },
    "Forecast is based on recent monthly revenue, capped growth, and a conservative weighted average. It should be treated as directional, not guaranteed.": {
        "en": "Forecast is based on recent monthly revenue, capped growth, and a conservative weighted average. It should be treated as directional, not guaranteed.",
        "fr": "La prévision est basée sur les revenus mensuels récents, une croissance plafonnée et une moyenne pondérée prudente. Elle doit être considérée comme indicative, non garantie.",
        "ar": "تعتمد التوقعات على الإيرادات الشهرية الأخيرة، ونمو محدود، ومتوسط مرجح محافظ. يجب اعتبارها اتجاهية وليست مضمونة.",
    },
}


CHART_TITLE_TRANSLATIONS: dict[str, dict[str, str]] = {
    "Revenue Trend": {
        "en": "Revenue Trend",
        "fr": "Évolution des revenus",
        "ar": "تطور الإيرادات",
    },
    "Expense Trend": {
        "en": "Expense Trend",
        "fr": "Évolution des dépenses",
        "ar": "تطور المصاريف",
    },
    "Profit Evolution": {
        "en": "Profit Evolution",
        "fr": "Évolution du profit",
        "ar": "تطور الأرباح",
    },
    "Cashflow Trend": {
        "en": "Cashflow Trend",
        "fr": "Évolution du cashflow",
        "ar": "تطور التدفق النقدي",
    },
    "Expenses by Category": {
        "en": "Expenses by Category",
        "fr": "Dépenses par catégorie",
        "ar": "المصاريف حسب الفئة",
    },
}


# These JSON branches are consumed by frontend charts / analytics engines.
# Do NOT recursively translate their internal strings or keys.
# Example:
# - chart.y_key must stay "revenue", not "الإيرادات"
# - chart.x_key must stay "period"
# - chart.data rows must keep "revenue", "expenses", "profit", "cashflow"
PROTECTED_STRUCTURE_KEYS = {
    "charts",
}


def translate_term(key: Any, language: str = "en") -> Any:
    lang = normalize_language(language)

    if not isinstance(key, str):
        return key

    normalized_key = key.strip()

    if normalized_key in TERM_TRANSLATIONS:
        return TERM_TRANSLATIONS[normalized_key].get(lang, normalized_key)

    lowered = normalized_key.lower()

    if lowered in TERM_TRANSLATIONS:
        return TERM_TRANSLATIONS[lowered].get(lang, normalized_key)

    return key


def translate_phrase(text: Any, language: str = "en") -> Any:
    lang = normalize_language(language)

    if not isinstance(text, str):
        return text

    stripped = text.strip()

    if stripped in PHRASE_TRANSLATIONS:
        return PHRASE_TRANSLATIONS[stripped].get(lang, stripped)

    translated = stripped

    for source, translations in PHRASE_TRANSLATIONS.items():
        translated = translated.replace(source, translations.get(lang, source))

    for source, translations in TERM_TRANSLATIONS.items():
        # Avoid replacing tiny/generic words inside larger words too aggressively.
        if len(source) >= 4:
            translated = translated.replace(source, translations.get(lang, source))

    return translated


def _translate_list(values: Any, language: str) -> Any:
    if not isinstance(values, list):
        return values

    return [
        translate_term(value, language)
        if isinstance(value, str)
        else translate_payload(value, language)
        for value in values
    ]


def _build_executive_summary(payload: dict[str, Any], language: str) -> str:
    lang = normalize_language(language)

    kpis = payload.get("kpis") or {}
    advanced = payload.get("advanced_kpis") or {}
    health = payload.get("business_health") or {}
    anomalies = payload.get("anomalies_v2") or payload.get("anomalies") or {}

    model = translate_term(payload.get("business_model", "general"), lang)
    revenue = kpis.get("revenue", 0)
    profit = kpis.get("profit", 0)
    margin = kpis.get("profit_margin_percent", 0)
    growth = kpis.get("growth_rate_percent", 0)
    cashflow = translate_term(kpis.get("cashflow_status", "unknown"), lang)
    score = payload.get("business_health_score", health.get("score", 0))
    rating = translate_term(health.get("rating", "unknown"), lang)
    anomaly_status = translate_term(anomalies.get("status", "normal"), lang)
    churn = advanced.get("churn_rate_percent", 0)

    if lang == "fr":
        return (
            f"Cette analyse {model} montre des revenus de {revenue}, "
            f"un profit de {profit} et une marge bénéficiaire de {margin}%. "
            f"La croissance des revenus est de {growth}% et le cashflow est {cashflow}. "
            f"Le score de santé business est de {score}/100 ({rating}). "
            f"L’évaluation actuelle du risque business est {anomaly_status}. "
            f"Le churn client est élevé à {churn}%, ce qui doit être traité en priorité."
        )

    if lang == "ar":
        return (
            f"يوضح تحليل {model} إيرادات قدرها {revenue}، "
            f"وربحًا قدره {profit}، وهامش ربح قدره {margin}%. "
            f"نمو الإيرادات هو {growth}% والتدفق النقدي {cashflow}. "
            f"درجة صحة النشاط هي {score}/100 ({rating}). "
            f"تقييم مخاطر الأعمال الحالي هو {anomaly_status}. "
            f"معدل فقدان العملاء مرتفع عند {churn}% ويجب التعامل معه كأولوية."
        )

    return (
        f"This {model} analysis shows revenue of {revenue}, "
        f"profit of {profit}, and a profit margin of {margin}%. "
        f"Revenue growth is {growth}% and cashflow is {cashflow}. "
        f"The Business Health Score is {score}/100 ({rating}). "
        f"The current business risk assessment is {anomaly_status}. "
        f"Customer churn is elevated at {churn}%, which should be treated as a priority."
    )


def _build_key_insights(payload: dict[str, Any], language: str) -> list[str]:
    lang = normalize_language(language)

    kpis = payload.get("kpis") or {}
    advanced = payload.get("advanced_kpis") or {}
    health = payload.get("business_health") or {}
    anomalies = payload.get("anomalies_v2") or payload.get("anomalies") or {}
    summary = anomalies.get("summary") or {}

    values = {
        "revenue": kpis.get("revenue", 0),
        "profit": kpis.get("profit", 0),
        "margin": kpis.get("profit_margin_percent", 0),
        "growth": kpis.get("growth_rate_percent", 0),
        "churn": advanced.get("churn_rate_percent", 0),
        "roas": advanced.get("roas", 0),
        "score": payload.get("business_health_score", health.get("score", 0)),
        "total": summary.get("total_items", 0),
        "insights": summary.get("insights", 0),
    }

    templates = [
        "Revenue is {revenue} with profit of {profit}.",
        "Profit margin is {margin}% and revenue growth is {growth}%.",
        "Customer churn is estimated at {churn}%, which affects retention quality.",
        "ROAS is {roas}, based on revenue and advertising spend.",
        "Business Health Score is {score}/100.",
        "{total} business risk indicator(s) and {insights} positive business signal(s) were identified.",
    ]

    return [
        PHRASE_TRANSLATIONS[template][lang].format(**values)
        for template in templates
    ]


def translate_payload(value: Any, language: str = "en") -> Any:
    lang = normalize_language(language)

    if isinstance(value, list):
        return [translate_payload(item, lang) for item in value]

    if isinstance(value, dict):
        translated: dict[str, Any] = {}

        for key, nested_value in value.items():
            if key in PROTECTED_STRUCTURE_KEYS:
                translated[key] = deepcopy(nested_value)

            elif key in {
                "severity",
                "impact",
                "priority",
                "status",
                "rating",
                "cashflow_status",
            }:
                translated[key] = translate_term(nested_value, lang)

            elif key in {
                "title",
                "risk",
                "opportunity",
                "recommendation",
                "decision",
                "why",
                "description",
                "explanation",
                "why_it_matters",
                "recommended_action",
                "expected_impact",
                "summary",
                "what_happened",
            }:
                translated[key] = translate_phrase(nested_value, lang)

            elif key in {"business_impact", "strengths", "warnings", "possible_causes", "recommended_actions"}:
                translated[key] = _translate_list(nested_value, lang)

            elif key == "label":
                # Health labels often map from signal; fallback to phrase translation.
                translated[key] = translate_phrase(nested_value, lang)

            else:
                translated[key] = translate_payload(nested_value, lang)

        return translated

    if isinstance(value, str):
        return translate_phrase(value, lang)

    return value


def translate_chart_titles(payload: dict[str, Any], language: str) -> dict[str, Any]:
    lang = normalize_language(language)

    charts = payload.get("charts")

    if not isinstance(charts, list):
        return payload

    for chart in charts:
        if not isinstance(chart, dict):
            continue

        title = chart.get("title")

        if title in CHART_TITLE_TRANSLATIONS:
            chart["title"] = CHART_TITLE_TRANSLATIONS[title].get(lang, title)

    return payload


def translate_business_analysis_payload(
    payload: dict[str, Any],
    language: str = "en",
) -> dict[str, Any]:
    """
    Universal business i18n layer.

    Goals:
    - Support any input language -> en/fr/ar output.
    - Never change numeric KPI truth.
    - Translate public-facing business narratives.
    - Keep internal codes available while translating display text.
    """

    lang = normalize_language(language)
    result = deepcopy(payload or {})

    result = translate_payload(result, lang)

    # Rebuild deterministic public-facing summary and key insights
    # from verified KPI truth to avoid mixed-language fragments.
    result["executive_summary"] = _build_executive_summary(result, lang)

    if isinstance(result.get("smart_insights"), dict):
        result["smart_insights"]["key_insights"] = _build_key_insights(result, lang)

        decision = result["smart_insights"].get("most_important_decision")

        if isinstance(decision, dict):
            metric = (
                decision.get("based_on", {}).get("metric")
                if isinstance(decision.get("based_on"), dict)
                else None
            )
            value = (
                decision.get("based_on", {}).get("value")
                if isinstance(decision.get("based_on"), dict)
                else None
            )

            if metric and value is not None:
                metric_label = translate_term(metric, lang)

                if lang == "fr":
                    decision["why"] = (
                        f"{translate_phrase('High churn reduces growth quality and can make acquisition spend less efficient.', lang)} "
                        f"L’analyse a détecté {metric_label} = {value}."
                    )
                elif lang == "ar":
                    decision["why"] = (
                        f"{translate_phrase('High churn reduces growth quality and can make acquisition spend less efficient.', lang)} "
                        f"كشف التحليل {metric_label} = {value}."
                    )
                else:
                    decision["why"] = (
                        f"{translate_phrase('High churn reduces growth quality and can make acquisition spend less efficient.', lang)} "
                        f"Analysis detected {metric_label} = {value}."
                    )

    result = translate_chart_titles(result, lang)

    if lang == "fr":
        result["disclaimer"] = (
            "Ceci est uniquement destiné au soutien à la décision business. "
            "Vérifiez les décisions importantes avec un professionnel qualifié."
        )
    elif lang == "ar":
        result["disclaimer"] = (
            "هذا التقرير مخصص فقط لدعم قرارات الأعمال. "
            "تحقق من القرارات المهمة مع متخصص مؤهل."
        )
    else:
        result["disclaimer"] = (
            "This is for business decision support only. "
            "Verify important decisions with a qualified professional."
        )

    return result
