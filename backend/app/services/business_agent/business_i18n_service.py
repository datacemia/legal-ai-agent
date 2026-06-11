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
    "excellent": {
        "en": "Excellent",
        "fr": "Excellent",
        "ar": "ممتاز",
    },
    "moderate": {
        "en": "Moderate",
        "fr": "Modéré",
        "ar": "متوسط",
    },
    "weak": {
        "en": "Weak",
        "fr": "Faible",
        "ar": "ضعيف",
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
        "fr": "Indisponible",
        "ar": "غير متاح",
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
    "retail": {
        "en": "Retail",
        "fr": "Commerce de détail",
        "ar": "تجارة التجزئة",
    },
    "wholesale": {
        "en": "Wholesale",
        "fr": "Commerce de gros",
        "ar": "تجارة الجملة",
    },
    "manufacturing": {
        "en": "Manufacturing",
        "fr": "Industrie / fabrication",
        "ar": "التصنيع",
    },
    "services": {
        "en": "Services",
        "fr": "Services",
        "ar": "الخدمات",
    },
    "healthcare": {
        "en": "Healthcare",
        "fr": "Santé",
        "ar": "الرعاية الصحية",
    },
    "education": {
        "en": "Education",
        "fr": "Éducation",
        "ar": "التعليم",
    },
    "real_estate": {
        "en": "Real estate",
        "fr": "Immobilier",
        "ar": "العقارات",
    },
    "logistics": {
        "en": "Logistics",
        "fr": "Logistique",
        "ar": "الخدمات اللوجستية",
    },
    "hospitality": {
        "en": "Hospitality",
        "fr": "Hôtellerie / hospitalité",
        "ar": "الضيافة",
    },
    "finance": {
        "en": "Finance",
        "fr": "Finance",
        "ar": "المالية",
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
        "fr": "Statut du flux de trésorerie",
        "ar": "حالة التدفق النقدي",
    },
    "cashflow": {
        "en": "Cashflow",
        "fr": "Flux de trésorerie",
        "ar": "التدفق النقدي",
    },
    "churn_rate_percent": {
        "en": "Customer churn",
        "fr": "Taux d’attrition client",
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
        "fr": "Pression sur le flux de trésorerie",
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
        "fr": "Flux de trésorerie positif.",
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
    "Insufficient verified business performance data was provided. Executive KPI, risk, forecast, and priority decision analysis is unavailable.": {
        "en": "Insufficient verified business performance data was provided. Executive KPI, risk, forecast, and priority decision analysis is unavailable.",
        "fr": "Les données de performance de l'entreprise vérifiées sont insuffisantes. L’analyse des KPI, des risques, des prévisions et des décisions prioritaires n’est pas disponible.",
        "ar": "بيانات أداء الأعمال الموثقة غير كافية. تحليل مؤشرات الأداء والمخاطر والتوقعات والقرارات ذات الأولوية غير متاح."
    },


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
    "High customer churn reduces growth quality and can make acquisition spend less efficient.": {
        "en": "High customer churn reduces growth quality and can make acquisition spend less efficient.",
        "fr": "Un taux d’attrition client élevé réduit la qualité de la croissance et peut rendre les dépenses d’acquisition moins efficaces.",
        "ar": "ارتفاع معدل فقدان العملاء يقلل جودة النمو وقد يجعل الإنفاق على الاكتساب أقل كفاءة.",
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

    "Continue monitoring business performance": {
        "en": "Continue monitoring business performance",
        "fr": "Continuer à surveiller la performance de l'entreprise",
        "ar": "مواصلة مراقبة أداء الأعمال",
    },
    "Keep tracking revenue, expenses, cashflow, and customer metrics before making major changes.": {
        "en": "Keep tracking revenue, expenses, cashflow, and customer metrics before making major changes.",
        "fr": "Continuez à suivre les revenus, les dépenses, le flux de trésorerie et les indicateurs clients avant tout changement majeur.",
        "ar": "استمر في تتبع الإيرادات والمصاريف والتدفق النقدي ومؤشرات العملاء قبل إجراء تغييرات كبيرة.",
    },
    "No Critical business risk was detected from the current analysis.": {
        "en": "No Critical business risk was detected from the current analysis.",
        "fr": "Aucun risque de l'entreprise critique n’a été détecté dans l’analyse actuelle.",
        "ar": "لم يتم اكتشاف أي خطر أعمال حرج في التحليل الحالي.",
    },
    "No critical business risk was detected from the current analysis.": {
        "en": "No critical business risk was detected from the current analysis.",
        "fr": "Aucun risque de l'entreprise critique n’a été détecté dans l’analyse actuelle.",
        "ar": "لم يتم اكتشاف أي خطر أعمال حرج في التحليل الحالي.",
    },
    "No major business risk was detected from the current analysis.": {
        "en": "No major business risk was detected from the current analysis.",
        "fr": "Aucun risque de l'entreprise majeur n’a été détecté dans l’analyse actuelle.",
        "ar": "لم يتم اكتشاف أي خطر أعمال كبير في التحليل الحالي.",
    },
    "Add expense, cost, or profit columns to verify profitability before making margin decisions.": {
        "en": "Add expense, cost, or profit columns to verify profitability before making margin decisions.",
        "fr": "Ajoutez des colonnes de dépenses, de coûts ou de profit pour vérifier la rentabilité avant de prendre des décisions sur les marges.",
        "ar": "أضف أعمدة للمصاريف أو التكاليف أو الربح للتحقق من الربحية قبل اتخاذ قرارات بشأن الهوامش.",
    },
    "Improves decision quality by enabling verified margin, profit, and cashflow analysis.": {
        "en": "Improves decision quality by enabling verified margin, profit, and cashflow analysis.",
        "fr": "Améliore la qualité des décisions en permettant une analyse vérifiée des marges, du profit et du flux de trésorerie.",
        "ar": "يحسن جودة القرار من خلال تمكين تحليل موثق للهامش والربح والتدفق النقدي.",
    },
    "Upload performance data before making business decisions": {
        "en": "Upload performance data before making business decisions",
        "fr": "Importer des données de performance avant de prendre des décisions d'entreprise",
        "ar": "ارفع بيانات أداء قبل اتخاذ قرارات أعمال",
    },
    "Upload a file with dated revenue, orders, expenses, customers, cashflow, or advertising spend before using this agent for executive decisions.": {
        "en": "Upload a file with dated revenue, orders, expenses, customers, cashflow, or advertising spend before using this agent for executive decisions.",
        "fr": "Importez un fichier avec des revenus datés, des commandes, des dépenses, des clients, du flux de trésorerie ou des dépenses publicitaires avant d’utiliser cet agent pour des décisions exécutives.",
        "ar": "ارفع ملفاً يحتوي على إيرادات مؤرخة أو طلبات أو مصروفات أو عملاء أو تدفق نقدي أو إنفاق إعلاني قبل استخدام هذا الوكيل لاتخاذ قرارات تنفيذية.",
    },
    "Enables verified KPI, risk, forecast, and decision analysis.": {
        "en": "Enables verified KPI, risk, forecast, and decision analysis.",
        "fr": "Permet une analyse vérifiée des KPI, des risques, des prévisions et des décisions.",
        "ar": "يتيح تحليلاً موثقاً للمؤشرات والمخاطر والتوقعات والقرارات.",
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
        "fr": "Le taux d’attrition client est estimé à {churn}%, ce qui affecte la qualité de rétention.",
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
        "ar": "درجة صحة الأعمال هي {score}/100.",
    },
    "Business Health Score could not be calculated because insufficient business performance data was provided.": {
        "en": "Business Health Score could not be calculated because insufficient business performance data was provided.",
        "fr": "Le score de santé business n’a pas pu être calculé faute de données de performance suffisantes.",
        "ar": "تعذر حساب درجة صحة الأعمال بسبب عدم توفر بيانات أداء كافية.",
    },
    "Revenue could not be calculated from the uploaded data.": {
        "en": "Revenue could not be calculated from the uploaded data.",
        "fr": "Les revenus n’ont pas pu être calculés à partir des données importées.",
        "ar": "تعذر حساب الإيرادات من البيانات المرفوعة.",
    },
    "Revenue growth could not be calculated from the uploaded data.": {
        "en": "Revenue growth could not be calculated from the uploaded data.",
        "fr": "La croissance des revenus n’a pas pu être calculée à partir des données importées.",
        "ar": "تعذر حساب نمو الإيرادات من البيانات المرفوعة.",
    },
    "Business performance metrics are unavailable because the uploaded file does not contain verified business performance data.": {
        "en": "Business performance metrics are unavailable because the uploaded file does not contain verified business performance data.",
        "fr": "Les indicateurs de performance de l'entreprise sont indisponibles car le fichier importé ne contient pas de données de performance vérifiées.",
        "ar": "مؤشرات أداء الأعمال غير متاحة لأن الملف المرفوع لا يحتوي على بيانات أداء موثقة.",
    },
    "Revenue is {revenue}. Profit could not be calculated because no expense, cost, or profit column was provided.": {
        "en": "Revenue is {revenue}. Profit could not be calculated because no expense, cost, or profit column was provided.",
        "fr": "Les revenus sont de {revenue}. Le profit n’a pas pu être calculé car aucune colonne de dépenses, de coûts ou de profit n’a été fournie.",
        "ar": "بلغت الإيرادات {revenue}. تعذر حساب الربح لأنه لم يتم توفير أي عمود للمصاريف أو التكاليف أو الربح.",
    },
    "Profit could not be calculated because no expense, cost, or profit column was provided.": {
        "en": "Profit could not be calculated because no expense, cost, or profit column was provided.",
        "fr": "Le profit n’a pas pu être calculé car aucune colonne de dépenses, de coûts ou de profit n’a été fournie.",
        "ar": "تعذر حساب الربح لأنه لم يتم توفير أي عمود للمصاريف أو التكاليف أو الربح.",
    },
    "{total} business risk indicator(s) and {insights} positive business signal(s) were identified.": {
        "en": "{total} business risk indicator(s) and {insights} positive business signal(s) were identified.",
        "fr": "{total} indicateur(s) de risque de l'entreprise et {insights} signal(aux) positif(s) ont été identifiés.",
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

    # KPI availability / limitations
    "Profitability metrics cannot be verified because no expense, cost, or profit column was provided.": {
        "en": "Profitability metrics cannot be verified because no expense, cost, or profit column was provided.",
        "fr": "Les indicateurs de rentabilité ne peuvent pas être vérifiés car aucune colonne de dépenses, de coûts ou de profit n’a été fournie.",
        "ar": "لا يمكن التحقق من مؤشرات الربحية لأنه لم يتم توفير أي عمود للمصاريف أو التكاليف أو الربح.",
    },
    "Customer churn could not be calculated from the uploaded data.": {
        "en": "Customer churn could not be calculated from the uploaded data.",
        "fr": "Le taux d’attrition client n’a pas pu être calculé à partir des données importées.",
        "ar": "تعذر حساب معدل فقدان العملاء من البيانات المرفوعة.",
    },
    "ROAS could not be calculated because advertising spend was not provided.": {
        "en": "ROAS could not be calculated because advertising spend was not provided.",
        "fr": "Le ROAS n’a pas pu être calculé car les dépenses publicitaires n’ont pas été fournies.",
        "ar": "تعذر حساب عائد الإنفاق الإعلاني لأن الإنفاق الإعلاني غير متوفر.",
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
        "fr": "Évolution du flux de trésorerie",
        "ar": "تطور التدفق النقدي",
    },
    "Expenses by Category": {
        "en": "Expenses by Category",
        "fr": "Dépenses par catégorie",
        "ar": "المصاريف حسب الفئة",
    },
    "Revenue by Category": {
        "en": "Revenue by Category",
        "fr": "Revenus par catégorie",
        "ar": "الإيرادات حسب الفئة",
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

    text = _normalize_generated_phrase(text)

    if not isinstance(text, str):
        return text

    stripped = text.strip()

    if stripped in PHRASE_TRANSLATIONS:
        return PHRASE_TRANSLATIONS[stripped].get(lang, stripped)

    revenue_prefix = "Revenue is "
    revenue_suffix = ". Profit could not be calculated because no expense, cost, or profit column was provided."
    if stripped.startswith(revenue_prefix) and stripped.endswith(revenue_suffix):
        revenue_value = stripped[len(revenue_prefix):-len(revenue_suffix)].strip()
        return PHRASE_TRANSLATIONS[
            "Revenue is {revenue}. Profit could not be calculated because no expense, cost, or profit column was provided."
        ][lang].format(revenue=revenue_value)

    translated = stripped

    for source, translations in PHRASE_TRANSLATIONS.items():
        translated = translated.replace(source, translations.get(lang, source))

    # If the phrase was not fully translated, avoid partial term replacement.
    # Partial replacements created mixed-language strings such as:
    # "Add expense, cost, or Bénéfice net columns..."
    if translated == stripped:
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


def _is_available(value: Any) -> bool:
    return value not in (None, "", "None", "null", "NULL", "N/A", "n/a")


def _metric_available(
    source: dict[str, Any],
    flag_name: str,
    value: Any,
    default: bool = False,
) -> bool:
    if isinstance(source.get(flag_name), bool):
        return bool(source.get(flag_name))

    return default and _is_available(value)


def _display_metric(value: Any, language: str = "en") -> str:
    if value is None:
        return "N/A"

    try:
        number = float(value)
    except (TypeError, ValueError):
        return str(value)

    if language == "fr":
        formatted = f"{number:,.2f}".replace(",", " ").replace(".", ",")
        return formatted.rstrip("0").rstrip(",")

    if language == "ar":
        formatted = f"{number:,.2f}"
        return formatted.rstrip("0").rstrip(".")

    formatted = f"{number:,.2f}"
    return formatted.rstrip("0").rstrip(".")

def _display_percent(value: Any, language: str = "en") -> str:
    if not _is_available(value):
        return "N/A"

    number = _display_metric(value, language)

    if language == "fr":
        return f"{number} %"

    if language == "ar":
        return f"{number}٪"

    return f"{number}%"

def _has_business_performance(payload: dict[str, Any]) -> bool:
    if payload.get("analysis_available") is False:
        return False

    kpis = payload.get("kpis") or {}
    advanced = payload.get("advanced_kpis") or {}
    forecast = payload.get("forecast") or {}

    core_flags = (
        "revenue_available",
        "expenses_available",
        "profit_available",
        "growth_available",
        "cashflow_available",
        "orders_available",
        "customers_available",
    )

    advanced_flags = (
        "churn_available",
        "roas_available",
        "cac_available",
        "aov_available",
        "mrr_available",
        "arr_available",
        "ltv_available",
        "retention_available",
        "conversion_available",
    )

    if any(bool(kpis.get(flag)) for flag in core_flags):
        return True

    if any(bool(advanced.get(flag)) for flag in advanced_flags):
        return True

    return bool(forecast.get("available"))


def _business_performance_unavailable_sentence(language: str) -> str:
    lang = normalize_language(language)

    return PHRASE_TRANSLATIONS[
        "Business performance metrics are unavailable because the uploaded file does not contain verified business performance data."
    ][lang]


def _build_executive_summary(payload: dict[str, Any], language: str) -> str:
    lang = normalize_language(language)

    kpis = payload.get("kpis") or {}
    advanced = payload.get("advanced_kpis") or {}
    health = payload.get("business_health") or {}
    anomalies = payload.get("anomalies_v2") or payload.get("anomalies") or {}

    model = translate_term(payload.get("business_model", "general"), lang)
    revenue = kpis.get("revenue")
    profit = kpis.get("profit")
    margin = kpis.get("profit_margin_percent")
    growth = kpis.get("growth_rate_percent")
    cashflow = translate_term(kpis.get("cashflow_status", "unknown"), lang)
    score = payload.get("business_health_score", health.get("score"))
    rating = translate_term(health.get("rating", "unknown"), lang)
    anomaly_status = translate_term(anomalies.get("status", "normal"), lang)
    churn = advanced.get("churn_rate_percent")

    has_performance_data = _has_business_performance(payload)

    revenue_available = _metric_available(
        kpis,
        "revenue_available",
        revenue,
        default=has_performance_data,
    )
    profit_available = _metric_available(
        kpis,
        "profit_available",
        profit,
        default=False,
    )
    growth_available = _metric_available(
        kpis,
        "growth_available",
        growth,
        default=has_performance_data,
    )
    churn_available = _metric_available(
        advanced,
        "churn_available",
        churn,
        default=False,
    )

    revenue_display = _display_metric(revenue, lang) if revenue_available else "N/A"
    growth_display = _display_percent(growth, lang) if growth_available else "N/A"

    if not has_performance_data:
        if lang == "fr":
            return (
                f"Cette analyse {model} ne contient pas suffisamment de données "
                "de performance de l'entreprise vérifiées. Les revenus, la croissance, "
                "la rentabilité, le flux de trésorerie, les risques avancés et les prévisions "
                "ne peuvent pas être calculés de manière fiable. "
                f"{PHRASE_TRANSLATIONS['Business Health Score could not be calculated because insufficient business performance data was provided.'][lang]} "
                f"Le niveau de risque de l'entreprise actuel est {anomaly_status}. "
                f"{PHRASE_TRANSLATIONS['Customer churn could not be calculated from the uploaded data.'][lang]}"
            )

        if lang == "ar":
            return (
                f"لا يحتوي تحليل {model} على بيانات أداء أعمال موثقة وكافية. "
                "لا يمكن حساب الإيرادات أو النمو أو الربحية أو التدفق النقدي أو "
                "المخاطر المتقدمة أو التوقعات بشكل موثوق. "
                f"{PHRASE_TRANSLATIONS['Business Health Score could not be calculated because insufficient business performance data was provided.'][lang]} "
                f"مستوى مخاطر الأعمال الحالي هو {anomaly_status}. "
                f"{PHRASE_TRANSLATIONS['Customer churn could not be calculated from the uploaded data.'][lang]}"
            )

        return (
            f"This {model} analysis does not contain enough verified business "
            "performance data. Revenue, growth, profitability, cashflow, advanced "
            "risks, and forecasts cannot be calculated reliably. "
            f"{PHRASE_TRANSLATIONS['Business Health Score could not be calculated because insufficient business performance data was provided.'][lang]} "
            f"The current business risk assessment is {anomaly_status}. "
            f"{PHRASE_TRANSLATIONS['Customer churn could not be calculated from the uploaded data.'][lang]}"
        )

    if profit_available:
        profit_display = _display_metric(profit, lang)
        margin_display = _display_percent(margin, lang)

        if lang == "fr":
            profitability_sentence = (
                f"un profit de {profit_display} et une marge bénéficiaire de {margin_display}. "
            )
        elif lang == "ar":
            profitability_sentence = (
                f"وربحًا قدره {profit_display}، وهامش ربح قدره {margin_display}. "
            )
        else:
            profitability_sentence = (
                f"profit of {profit_display}, and a profit margin of {margin_display}. "
            )
    else:
        if lang == "fr":
            profitability_sentence = (
                "les indicateurs de rentabilité ne peuvent pas être vérifiés "
                "car les dépenses ou les coûts ne sont pas fournis. "
            )
        elif lang == "ar":
            profitability_sentence = (
                "ولا يمكن التحقق من مؤشرات الربحية لأن المصاريف أو التكاليف غير متوفرة. "
            )
        else:
            profitability_sentence = (
                "profitability metrics cannot be verified because expenses or costs were not provided. "
            )

    if churn_available:
        churn_display = _display_percent(churn, lang)

        if lang == "fr":
            churn_sentence = (
                f"Le churn client est estimé à {churn_display}, ce qui doit être surveillé."
            )
        elif lang == "ar":
            churn_sentence = (
                f"يُقدر معدل فقدان العملاء بـ {churn_display} ويجب مراقبته."
            )
        else:
            churn_sentence = (
                f"Customer churn is estimated at {churn_display} and should be monitored."
            )
    else:
        churn_sentence = PHRASE_TRANSLATIONS[
            "Customer churn could not be calculated from the uploaded data."
        ][lang]

    if score is None:
        health_sentence = PHRASE_TRANSLATIONS[
            "Business Health Score could not be calculated because insufficient business performance data was provided."
        ][lang] + " "
    else:
        if lang == "fr":
            health_sentence = f"Le score de santé business est de {score}/100 ({rating}). "
        elif lang == "ar":
            health_sentence = f"درجة صحة الأعمال هي {score}/100 ({rating}). "
        else:
            health_sentence = f"The Business Health Score is {score}/100 ({rating}). "

    if lang == "fr":
        return (
            f"Cette analyse montre des revenus de {revenue_display}, "
            f"{profitability_sentence}"
            f"La croissance des revenus est {growth_display} et le flux de trésorerie est {cashflow}. "
            f"{health_sentence}"
            f"Le niveau de risque de l'entreprise actuel est {anomaly_status}. "
            f"{churn_sentence}"
        )

    if lang == "ar":
        return (
            f"يوضح هذا التحليل إيرادات قدرها {revenue_display}، "
            f"{profitability_sentence}"
            f"نمو الإيرادات هو {growth_display} والتدفق النقدي هو {cashflow}. "
            f"{health_sentence}"
            f"مستوى مخاطر الأعمال الحالي هو {anomaly_status}. "
            f"{churn_sentence}"
        )

    return (
        f"This analysis shows revenue of {revenue_display}, "
        f"{profitability_sentence}"
        f"Revenue growth is {growth_display} and cashflow is {cashflow}. "
        f"{health_sentence}"
        f"The current business risk assessment is {anomaly_status}. "
        f"{churn_sentence}"
    )

def _build_key_insights(payload: dict[str, Any], language: str) -> list[str]:
    lang = normalize_language(language)

    kpis = payload.get("kpis") or {}
    advanced = payload.get("advanced_kpis") or {}
    health = payload.get("business_health") or {}
    anomalies = payload.get("anomalies_v2") or payload.get("anomalies") or {}
    summary = anomalies.get("summary") or {}

    revenue = kpis.get("revenue")
    profit = kpis.get("profit")
    margin = kpis.get("profit_margin_percent")
    growth = kpis.get("growth_rate_percent")
    churn = advanced.get("churn_rate_percent")
    roas = advanced.get("roas")
    score = payload.get("business_health_score", health.get("score"))
    total = summary.get("total_items", 0)
    positive_insights = summary.get("insights", 0)

    has_performance_data = _has_business_performance(payload)

    revenue_available = _metric_available(
        kpis,
        "revenue_available",
        revenue,
        default=has_performance_data,
    )
    profit_available = _metric_available(
        kpis,
        "profit_available",
        profit,
        default=False,
    )
    growth_available = _metric_available(
        kpis,
        "growth_available",
        growth,
        default=has_performance_data,
    )
    churn_available = _metric_available(
        advanced,
        "churn_available",
        churn,
        default=False,
    )
    roas_available = _metric_available(
        advanced,
        "roas_available",
        roas,
        default=False,
    )

    insights: list[str] = []

    if not has_performance_data:
        insights.append(_business_performance_unavailable_sentence(lang))
    elif revenue_available and profit_available:
        insights.append(
            PHRASE_TRANSLATIONS["Revenue is {revenue} with profit of {profit}."][lang].format(
                revenue=_display_metric(revenue, lang),
                profit=_display_metric(profit, lang),
            )
        )
    elif revenue_available:
        insights.append(
            PHRASE_TRANSLATIONS[
                "Revenue is {revenue}. Profit could not be calculated because no expense, cost, or profit column was provided."
            ][lang].format(
                revenue=_display_metric(revenue, lang),
            )
        )
    else:
        insights.append(
            PHRASE_TRANSLATIONS[
                "Revenue could not be calculated from the uploaded data."
            ][lang]
        )

    if profit_available:
        insights.append(
            PHRASE_TRANSLATIONS[
                "Profit margin is {margin}% and revenue growth is {growth}%."
            ][lang].format(
                margin=_display_metric(margin),
                growth=_display_metric(growth) if growth_available else "N/A",
            )
        )
    else:
        insights.append(
            PHRASE_TRANSLATIONS[
                "Profitability metrics cannot be verified because no expense, cost, or profit column was provided."
            ][lang]
        )

    if has_performance_data and not growth_available:
        insights.append(
            PHRASE_TRANSLATIONS[
                "Revenue growth could not be calculated from the uploaded data."
            ][lang]
        )

    if churn_available:
        insights.append(
            PHRASE_TRANSLATIONS[
                "Customer churn is estimated at {churn}%, which affects retention quality."
            ][lang].format(churn=_display_metric(churn))
        )
    else:
        insights.append(
            PHRASE_TRANSLATIONS[
                "Customer churn could not be calculated from the uploaded data."
            ][lang]
        )

    if roas_available:
        insights.append(
            PHRASE_TRANSLATIONS[
                "ROAS is {roas}, based on revenue and advertising spend."
            ][lang].format(roas=_display_metric(roas))
        )
    else:
        insights.append(
            PHRASE_TRANSLATIONS[
                "ROAS could not be calculated because advertising spend was not provided."
            ][lang]
        )

    if score is None:
        insights.append(
            PHRASE_TRANSLATIONS[
                "Business Health Score could not be calculated because insufficient business performance data was provided."
            ][lang]
        )
    else:
        insights.append(
            PHRASE_TRANSLATIONS["Business Health Score is {score}/100."][lang].format(
                score=score
            )
        )

    insights.append(
        PHRASE_TRANSLATIONS[
            "{total} business risk indicator(s) and {insights} positive business signal(s) were identified."
        ][lang].format(total=total, insights=positive_insights)
    )

    deduped: list[str] = []
    for insight in insights:
        if insight not in deduped:
            deduped.append(insight)

    return deduped[:6]

def _normalize_generated_phrase(text: Any) -> Any:
    if not isinstance(text, str):
        return text

    stripped = text.strip()

    normalized_variants = {
        "Add expense, cost, or Bénéfice net columns to verify Profitability before making margin decisions.": (
            "Add expense, cost, or profit columns to verify profitability before making margin decisions."
        ),
        "Add expense, cost, or profit columns to verify Profitability before making margin decisions.": (
            "Add expense, cost, or profit columns to verify profitability before making margin decisions."
        ),
        "Add expense, cost, or Bénéfice net columns to verify profitability before making margin decisions.": (
            "Add expense, cost, or profit columns to verify profitability before making margin decisions."
        ),
        "Improves decision quality by enabling verified margin, Bénéfice net, and Flux de trésorerie analysis.": (
            "Improves decision quality by enabling verified margin, profit, and cashflow analysis."
        ),
        "Improves decision quality by enabling verified margin, profit, and Flux de trésorerie analysis.": (
            "Improves decision quality by enabling verified margin, profit, and cashflow analysis."
        ),
        "Keep tracking Revenus, Dépenses, Flux de trésorerie, and customer metrics before making major changes.": (
            "Keep tracking revenue, expenses, cashflow, and customer metrics before making major changes."
        ),
        "No Critique business risk was detected from the current analysis.": (
            "No Critical business risk was detected from the current analysis."
        ),
        "Ajoutez des colonnes de dépenses, de coûts ou de Bénéfice net pour vérifier la rentabilité avant de prendre des décisions sur les marges.": (
            "Add expense, cost, or profit columns to verify profitability before making margin decisions."
        ),
        "Améliore la qualité des décisions en permettant une analyse vérifiée des marges, du Bénéfice net et du Flux de trésorerie.": (
            "Improves decision quality by enabling verified margin, profit, and cashflow analysis."
        ),
        "Améliore la qualité des décisions en permettant une analyse vérifiée des marges, du profit et du Flux de trésorerie.": (
            "Improves decision quality by enabling verified margin, profit, and cashflow analysis."
        ),
        "Continuez à suivre les revenus, les dépenses, le Flux de trésorerie et les indicateurs clients avant tout changement majeur.": (
            "Keep tracking revenue, expenses, cashflow, and customer metrics before making major changes."
        ),
        "Les revenus sont de {revenue}, avec un Bénéfice net de N/A.": (
            "Revenue is {revenue}. Profit could not be calculated because no expense, cost, or profit column was provided."
        ),
        "Les revenus sont de {revenue}, avec un profit de N/A.": (
            "Revenue is {revenue}. Profit could not be calculated because no expense, cost, or profit column was provided."
        ),
        "Les revenus sont de 129510.85, avec un Bénéfice net de N/A.": (
            "Revenue is 129510.85. Profit could not be calculated because no expense, cost, or profit column was provided."
        ),
        "Les revenus sont de 129510.85, avec un profit de N/A.": (
            "Revenue is 129510.85. Profit could not be calculated because no expense, cost, or profit column was provided."
        ),
    }

    if stripped in normalized_variants:
        return normalized_variants[stripped]

    french_revenue_profit_na = "Les revenus sont de "
    if stripped.startswith(french_revenue_profit_na) and (
        "avec un Bénéfice net de N/A" in stripped
        or "avec un profit de N/A" in stripped
    ):
        revenue_value = stripped[len(french_revenue_profit_na):].split(",", 1)[0].strip()
        return (
            "Revenue is "
            f"{revenue_value}. "
            "Profit could not be calculated because no expense, cost, or profit column was provided."
        )

    if stripped.startswith(french_revenue_profit_na) and (
        "Le Bénéfice net n’a pas pu être calculé" in stripped
        or "Le profit n’a pas pu être calculé" in stripped
    ):
        revenue_value = stripped[len(french_revenue_profit_na):].split(".", 1)[0].strip()
        return (
            "Revenue is "
            f"{revenue_value}. "
            "Profit could not be calculated because no expense, cost, or profit column was provided."
        )

    if (
        stripped.startswith("Ajoutez des colonnes de dépenses, de coûts ou de ")
        and "pour vérifier la rentabilité avant de prendre des décisions sur les marges." in stripped
    ):
        return "Add expense, cost, or profit columns to verify profitability before making margin decisions."

    if (
        stripped.startswith("Améliore la qualité des décisions en permettant une analyse vérifiée des marges")
        and ("Bénéfice net" in stripped or "Flux de trésorerie" in stripped)
    ):
        return "Improves decision quality by enabling verified margin, profit, and cashflow analysis."

    if (
        stripped.startswith("Continuez à suivre les revenus, les dépenses")
        and "indicateurs clients avant tout changement majeur." in stripped
    ):
        return "Keep tracking revenue, expenses, cashflow, and customer metrics before making major changes."

    english_revenue_profit_na = "Revenue is "
    if stripped.startswith(english_revenue_profit_na) and "with profit of N/A" in stripped:
        revenue_value = stripped[len(english_revenue_profit_na):].split(" with profit of N/A", 1)[0].strip()
        return (
            "Revenue is "
            f"{revenue_value}. "
            "Profit could not be calculated because no expense, cost, or profit column was provided."
        )

    return text


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
        return translate_phrase(_normalize_generated_phrase(value), lang)

    return value


def _cleanup_mixed_business_terms(value: Any, language: str) -> Any:
    lang = normalize_language(language)

    if isinstance(value, list):
        return [_cleanup_mixed_business_terms(item, lang) for item in value]

    if isinstance(value, dict):
        return {
            key: _cleanup_mixed_business_terms(nested_value, lang)
            for key, nested_value in value.items()
        }

    if not isinstance(value, str):
        return value

    if lang == "fr":
        replacements = {
            "Bénéfice net": "profit",
            "bénéfice net": "profit",
            "Flux de trésorerie": "cashflow",
            "flux de trésorerie": "flux de trésorerie",
            "Le profit n’a pas pu être calculé car aucune colonne de dépenses, de coûts ou de profit n’a été fournie.": "Le profit n’a pas pu être calculé car aucune colonne de dépenses, de coûts ou de profit n’a été fournie.",
        }

        cleaned = value
        for source, target in replacements.items():
            cleaned = cleaned.replace(source, target)

        # Keep the executive-summary style natural.
        cleaned = cleaned.replace(
            "et le flux de trésorerie est",
            "et le flux de trésorerie est",
        )

        return cleaned

    if lang == "ar":
        return value

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
                metric_key = str(metric or "").strip().lower()
                metric_label = translate_term(metric_key, lang)

                numeric_value = None

                try:
                    numeric_value = abs(float(value))
                except (TypeError, ValueError):
                    numeric_value = None

                if metric_key == "profit_change_percent" and numeric_value is not None:
                    value_display = _display_percent(numeric_value, lang)

                    if lang == "fr":
                        decision["why"] = (
                            f"{translate_phrase(decision.get('why', ''), lang)} "
                            f"L’analyse a détecté une baisse du profit de {value_display}."
                        )
                    elif lang == "ar":
                        decision["why"] = (
                            f"{translate_phrase(decision.get('why', ''), lang)} "
                            f"كشف التحليل انخفاضاً في الربح بنسبة {value_display}."
                        )
                    else:
                        decision["why"] = (
                            f"{translate_phrase(decision.get('why', ''), lang)} "
                            f"Analysis detected a profit decrease of {value_display}."
                        )
                else:
                    if lang == "fr":
                        decision["why"] = (
                            f"{translate_phrase(decision.get('why', ''), lang)} "
                            f"L’analyse a détecté {metric_label} = {value}."
                        )
                    elif lang == "ar":
                        decision["why"] = (
                            f"{translate_phrase(decision.get('why', ''), lang)} "
                            f"كشف التحليل {metric_label} = {value}."
                        )
                    else:
                        decision["why"] = (
                            f"{translate_phrase(decision.get('why', ''), lang)} "
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

    result = _cleanup_mixed_business_terms(result, lang)

    return result
