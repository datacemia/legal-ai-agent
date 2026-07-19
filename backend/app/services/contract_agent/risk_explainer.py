"""
risk_explainer.py

Privacy-first, deterministic risk-reason helper for contract analysis.

Scope:
- International standard logic across contract families and domains.
- English / French / Arabic.
- No personal data processing and no external calls.
- API-compatible with the existing build_risk_explanation(analysis, clause_text, language).
"""

from typing import Dict, List


SUPPORTED_LANGUAGES = {"en", "fr", "ar"}
SUPPORTED_RISK_LEVELS = {"medium", "high", "elevated", "critical"}


MESSAGES = {
    "termination": {
        "en": "Termination provisions may affect operational continuity or legal remedies.",
        "fr": "Les dispositions de résiliation peuvent affecter la continuité opérationnelle ou les recours juridiques.",
        "ar": "قد تؤثر أحكام الإنهاء على استمرارية الأعمال أو وسائل الانتصاف القانونية.",
    },
    "renewal": {
        "en": "Renewal provisions may affect contract duration, exit rights, or future pricing leverage.",
        "fr": "Les dispositions de renouvellement peuvent affecter la durée du contrat, les droits de sortie ou le pouvoir de négociation futur.",
        "ar": "قد تؤثر أحكام التجديد على مدة العقد أو حقوق الخروج أو القدرة التفاوضية المستقبلية.",
    },
    "liability": {
        "en": "Liability allocation may affect financial exposure or available remedies.",
        "fr": "La répartition de la responsabilité peut affecter l'exposition financière ou les recours disponibles.",
        "ar": "قد يؤثر توزيع المسؤولية على التعرض المالي أو وسائل الانتصاف المتاحة.",
    },
    "confidentiality": {
        "en": "Confidentiality obligations may continue beyond contract termination.",
        "fr": "Les obligations de confidentialité peuvent survivre à la fin du contrat.",
        "ar": "قد تستمر التزامات السرية بعد انتهاء العقد.",
    },
    "restrictive": {
        "en": "Restrictive commitments may reduce commercial or operational flexibility.",
        "fr": "Les engagements restrictifs peuvent réduire la flexibilité commerciale ou opérationnelle.",
        "ar": "قد تقلل الالتزامات التقييدية من المرونة التجارية أو التشغيلية.",
    },
    "payment": {
        "en": "Payment provisions may affect cash flow or performance rights.",
        "fr": "Les dispositions de paiement peuvent affecter la trésorerie ou les droits d'exécution.",
        "ar": "قد تؤثر أحكام الدفع على التدفقات النقدية أو حقوق التنفيذ.",
    },
    "tax": {
        "en": "Tax provisions may affect net economics, withholding, reporting, or gross-up obligations.",
        "fr": "Les dispositions fiscales peuvent affecter l'économie nette, les retenues, les déclarations ou les obligations de majoration.",
        "ar": "قد تؤثر الأحكام الضريبية على الصافي الاقتصادي أو الاقتطاع أو الإقرارات أو التزامات التعويض الضريبي.",
    },
    "data": {
        "en": "Data protection obligations may require ongoing compliance measures.",
        "fr": "Les obligations de protection des données peuvent nécessiter des mesures de conformité continues.",
        "ar": "قد تتطلب التزامات حماية البيانات إجراءات امتثال مستمرة.",
    },
    "security": {
        "en": "Security obligations may require technical controls, incident response, monitoring, or audit readiness.",
        "fr": "Les obligations de sécurité peuvent exiger des contrôles techniques, une réponse aux incidents, une surveillance ou une préparation aux audits.",
        "ar": "قد تتطلب التزامات الأمن ضوابط تقنية أو استجابة للحوادث أو مراقبة أو جاهزية للتدقيق.",
    },
    "ip": {
        "en": "Intellectual property provisions may affect ownership or usage rights.",
        "fr": "Les dispositions de propriété intellectuelle peuvent affecter la propriété ou les droits d'utilisation.",
        "ar": "قد تؤثر أحكام الملكية الفكرية على الملكية أو حقوق الاستخدام.",
    },
    "licensing": {
        "en": "Licensing provisions may limit permitted use, sublicensing, duration, territory, or post-termination rights.",
        "fr": "Les dispositions de licence peuvent limiter les usages autorisés, la sous-licence, la durée, le territoire ou les droits après résiliation.",
        "ar": "قد تقيد أحكام الترخيص الاستخدام المسموح أو الترخيص من الباطن أو المدة أو النطاق الجغرافي أو الحقوق بعد الانتهاء.",
    },
    "services": {
        "en": "Service obligations should be assessed together with performance standards and remedies.",
        "fr": "Les obligations de service doivent être évaluées avec les niveaux de performance et les recours.",
        "ar": "يجب تقييم التزامات الخدمة مع معايير الأداء ووسائل الانتصاف.",
    },
    "subcontracting": {
        "en": "Subcontracting provisions may affect control over performance, data handling, and accountability.",
        "fr": "Les dispositions de sous-traitance peuvent affecter le contrôle de l'exécution, le traitement des données et la responsabilité.",
        "ar": "قد تؤثر أحكام التعاقد من الباطن على التحكم في الأداء ومعالجة البيانات والمساءلة.",
    },
    "dispute": {
        "en": "Dispute resolution provisions determine how disagreements are resolved.",
        "fr": "Les dispositions de règlement des litiges déterminent la manière de résoudre les différends.",
        "ar": "تحدد أحكام تسوية النزاعات كيفية حل الخلافات.",
    },
    "assignment": {
        "en": "Assignment provisions may affect transfer of contractual rights or obligations.",
        "fr": "Les dispositions de cession peuvent affecter le transfert des droits ou obligations contractuels.",
        "ar": "قد تؤثر أحكام التنازل على نقل الحقوق أو الالتزامات التعاقدية.",
    },
    "audit": {
        "en": "Audit provisions may require access to records or verification activities.",
        "fr": "Les dispositions d'audit peuvent exiger l'accès aux registres ou des vérifications.",
        "ar": "قد تتطلب أحكام التدقيق الوصول إلى السجلات أو أنشطة التحقق.",
    },
    "insurance": {
        "en": "Insurance requirements may allocate financial risk between the parties.",
        "fr": "Les exigences d'assurance peuvent répartir le risque financier entre les parties.",
        "ar": "قد توزع متطلبات التأمين المخاطر المالية بين الأطراف.",
    },
    "compliance": {
        "en": "Compliance provisions may create ongoing legal, regulatory, or policy obligations.",
        "fr": "Les dispositions de conformité peuvent créer des obligations juridiques, réglementaires ou internes continues.",
        "ar": "قد تنشئ أحكام الامتثال التزامات قانونية أو تنظيمية أو داخلية مستمرة.",
    },
    "governance": {
        "en": "Governance provisions may affect approval rights, decision-making, reporting, or oversight.",
        "fr": "Les dispositions de gouvernance peuvent affecter les droits d'approbation, la prise de décision, le reporting ou la supervision.",
        "ar": "قد تؤثر أحكام الحوكمة على حقوق الموافقة أو اتخاذ القرار أو التقارير أو الرقابة.",
    },
    "warranty": {
        "en": "Warranty provisions may affect quality commitments, remedies, exclusions, or reliance risk.",
        "fr": "Les garanties peuvent affecter les engagements de qualité, les recours, les exclusions ou le risque de dépendance.",
        "ar": "قد تؤثر أحكام الضمان على التزامات الجودة أو وسائل الانتصاف أو الاستثناءات أو مخاطر الاعتماد.",
    },
    "force_majeure": {
        "en": "Force majeure provisions may affect excuse from performance, notice duties, and termination rights during exceptional events.",
        "fr": "Les dispositions de force majeure peuvent affecter l'exonération d'exécution, les obligations de notification et les droits de résiliation en cas d'événements exceptionnels.",
        "ar": "قد تؤثر أحكام القوة القاهرة على الإعفاء من التنفيذ وواجبات الإشعار وحقوق الإنهاء أثناء الأحداث الاستثنائية.",
    },
    "real_estate": {
        "en": "Real estate provisions may affect possession, rent, maintenance, permitted use, deposits, or property-related liability.",
        "fr": "Les dispositions immobilières peuvent affecter la possession, le loyer, l'entretien, l'usage autorisé, les dépôts ou la responsabilité liée au bien.",
        "ar": "قد تؤثر الأحكام العقارية على الحيازة أو الإيجار أو الصيانة أو الاستخدام المسموح أو الودائع أو المسؤولية المتعلقة بالعقار.",
    },
    "loan": {
        "en": "Financing provisions may affect repayment, interest, collateral, default, acceleration, or guarantees.",
        "fr": "Les dispositions de financement peuvent affecter le remboursement, les intérêts, les sûretés, le défaut, l'exigibilité anticipée ou les garanties.",
        "ar": "قد تؤثر أحكام التمويل على السداد أو الفائدة أو الضمانات أو التعثر أو حلول الأجل أو الكفالات.",
    },
}


RULES = [
    ("termination", ["terminate", "termination", "termination for cause", "termination for convenience", "résiliation", "mettre fin", "فسخ", "إنهاء"]),
    ("renewal", ["renewal", "automatic renewal", "auto-renewal", "renouvellement", "reconduction", "تجديد", "تجديد تلقائي"]),
    ("liability", ["liability", "limitation of liability", "liability cap", "responsibility", "indemnity", "indemnification", "responsabilité", "indemnisation", "المسؤولية", "تعويض"]),
    ("confidentiality", ["confidentiality", "confidential information", "non-disclosure", "trade secret", "confidentialité", "information confidentielle", "secret", "سرية", "معلومات سرية", "عدم الإفصاح"]),
    ("payment", ["payment", "invoice", "fees", "price", "late payment", "paiement", "facture", "frais", "prix", "retard de paiement", "الدفع", "فاتورة", "الرسوم", "السعر", "تأخير الدفع"]),
    ("tax", ["tax", "withholding", "gross-up", "vat", "sales tax", "impôt", "taxe", "retenue à la source", "tva", "ضريبة", "اقتطاع", "القيمة المضافة"]),
    ("data", ["personal data", "data protection", "data processing", "privacy", "gdpr", "données personnelles", "protection des données", "traitement des données", "vie privée", "rgpd", "البيانات الشخصية", "حماية البيانات", "معالجة البيانات", "الخصوصية"]),
    ("security", ["security incident", "security measures", "cybersecurity", "breach notification", "encryption", "access control", "incident de sécurité", "mesures de sécurité", "cybersécurité", "notification de violation", "حادث أمني", "تدابير أمنية", "الأمن السيبراني", "إشعار بالاختراق"]),
    ("ip", ["intellectual property", "ownership of ip", "work product", "copyright", "patent", "trademark", "propriété intellectuelle", "droit d'auteur", "brevet", "marque", "الملكية الفكرية", "حقوق النشر", "براءة", "علامة تجارية"]),
    ("licensing", ["license grant", "license fee", "licensed software", "permitted use", "sublicense", "octroi de licence", "redevance", "logiciel sous licence", "usage autorisé", "منح الترخيص", "رسوم الترخيص", "برنامج مرخص", "استخدام مسموح"]),
    ("services", ["service level", "uptime", "availability", "support", "maintenance", "service credits", "performance standard", "niveau de service", "disponibilité", "support", "maintenance", "crédits de service", "مستوى الخدمة", "التوافر", "الدعم", "الصيانة", "ائتمانات الخدمة"]),
    ("subcontracting", ["subcontract", "subcontractor", "subprocessor", "delegate performance", "sous-traitance", "sous-traitant", "sous-traitant ultérieur", "التعاقد من الباطن", "مقاول من الباطن", "معالج فرعي"]),
    ("dispute", ["arbitration", "mediation", "governing law", "jurisdiction", "venue", "court", "arbitrage", "médiation", "droit applicable", "juridiction", "tribunal", "تحكيم", "وساطة", "القانون الواجب التطبيق", "الاختصاص", "محكمة"]),
    ("assignment", ["assignment", "assign", "transfer this agreement", "change of control", "cession", "céder", "transfert du contrat", "changement de contrôle", "تنازل", "نقل العقد", "تغيير السيطرة"]),
    ("audit", ["audit", "inspection", "records inspection", "verify compliance", "droit d'audit", "inspection", "vérification", "تدقيق", "تفتيش", "فحص السجلات"]),
    ("insurance", ["insurance", "insured", "coverage", "policy", "assurance", "assuré", "couverture", "police d'assurance", "تأمين", "مؤمن", "تغطية", "وثيقة التأمين"]),
    ("compliance", ["compliance", "anti-bribery", "anti-corruption", "sanctions", "export control", "applicable law", "conformité", "anti-corruption", "sanctions", "contrôle des exportations", "loi applicable", "امتثال", "مكافحة الرشوة", "مكافحة الفساد", "عقوبات", "ضوابط التصدير"]),
    ("governance", ["governance", "committee", "approval rights", "reporting", "oversight", "board approval", "gouvernance", "comité", "droits d'approbation", "reporting", "supervision", "حوكمة", "لجنة", "حقوق الموافقة", "تقارير", "رقابة"]),
    ("warranty", ["warranty", "representation", "disclaimer of warranty", "as is", "garantie", "déclaration", "exclusion de garantie", "en l'état", "ضمان", "إقرار", "استبعاد الضمان", "كما هو"]),
    ("force_majeure", ["force majeure", "act of god", "unforeseeable event", "cas de force majeure", "événement imprévisible", "القوة القاهرة", "حدث غير متوقع"]),
    ("real_estate", ["lease", "rent", "tenant", "landlord", "lessor", "lessee", "premises", "security deposit", "bail", "loyer", "locataire", "bailleur", "locaux", "dépôt de garantie", "إيجار", "كراء", "المستأجر", "المؤجر", "العقار", "وديعة الضمان"]),
    ("loan", ["loan", "borrower", "lender", "interest rate", "collateral", "security interest", "repayment", "acceleration", "guarantor", "prêt", "emprunteur", "prêteur", "taux d'intérêt", "sûreté", "remboursement", "exigibilité anticipée", "قرض", "مقترض", "مقرض", "معدل الفائدة", "ضمان", "سداد", "حلول الأجل"]),
]


EXCLUSIVE_NEGATIVE_TERMS = [
    "non-exclusive",
    "non exclusive",
    "non exclusif",
    "non-exclusif",
    "غير حصري",
]


EXCLUSIVE_POSITIVE_TERMS = [
    "exclusive",
    "exclusivity",
    "sole provider",
    "exclusive rights",
    "exclusif",
    "exclusivité",
    "حصري",
    "حصرية",
]


def normalize_language(language: str = "en") -> str:
    language = str(language or "en").lower().strip()
    return language if language in SUPPORTED_LANGUAGES else "en"


def normalize_risk_level(value) -> str:
    return str(value or "").lower().strip()


def contains_any(text: str, terms: List[str]) -> bool:
    return any(str(term or "").lower() in text for term in terms)


def unique_preserve_order(items: List[str]) -> List[str]:
    return list(dict.fromkeys(item for item in items if item))


def has_restrictive_exclusivity(lowered: str) -> bool:
    if contains_any(lowered, EXCLUSIVE_NEGATIVE_TERMS):
        return False
    return contains_any(lowered, EXCLUSIVE_POSITIVE_TERMS)


def build_risk_explanation(
    analysis: Dict,
    clause_text: str,
    language: str = "en",
) -> Dict:
    language = normalize_language(language)
    reasons: List[str] = []
    lowered = str(clause_text or "").lower()

    if normalize_risk_level(analysis.get("risk_level")) in SUPPORTED_RISK_LEVELS:
        for key, terms in RULES:
            if contains_any(lowered, terms):
                reasons.append(MESSAGES[key][language])

        if has_restrictive_exclusivity(lowered):
            reasons.append(MESSAGES["restrictive"][language])

    analysis["risk_reasons"] = unique_preserve_order(reasons)[:5]

    return analysis
