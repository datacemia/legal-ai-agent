import re


SUPPORTED_LANGUAGES = {"en", "fr", "ar"}


def normalize_language(language: str) -> str:
    language = str(language or "en").lower()
    return language if language in SUPPORTED_LANGUAGES else "en"


def normalize_text(text: str) -> str:
    text = str(text or "").lower()
    text = text.replace("–", "-").replace("—", "-")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def first_matching_signal(text: str, signals: list[str]) -> str:
    for signal in signals:
        if signal.lower() in text:
            return signal
    return ""


def localized(en: str, fr: str, ar: str) -> dict:
    return {
        "en": en,
        "fr": fr,
        "ar": ar,
    }


def neutral_party() -> dict:
    return localized(
        "responsible party",
        "partie responsable",
        "الطرف المسؤول",
    )


def extract_deadline(text: str) -> str:
    patterns = [
        r"within\s+\d+\s+(days?|months?|years?)",
        r"\d+\s+(days?|months?|years?)",
        r"notice period",
        r"cure period",
        r"due date",
        r"effective date",
        r"expiration date",
        r"renewal date",
        r"dans\s+un\s+délai\s+de\s+\d+\s+jours?",
        r"\d+\s+jours?",
        r"préavis",
        r"délai de régularisation",
        r"date d['’]échéance",
        r"date d'effet",
        r"date d'expiration",
        r"خلال\s+\d+\s+يوم",
        r"\d+\s+يوماً",
        r"\d+\s+يوم",
        r"مهلة",
        r"إشعار",
        r"تاريخ السريان",
        r"تاريخ الانتهاء",
    ]

    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            return match.group(0)

    return ""


TRIGGER_SIGNALS = {
    "payment": [
        "invoice", "delivery", "milestone", "due date",
        "expense statement", "voucher", "acceptance",
        "facture", "livraison", "jalon", "échéance",
        "note de frais", "justificatif", "acceptation",
        "فاتورة", "تسليم", "مرحلة", "استحقاق", "إيصال", "قبول",
    ],
    "termination": [
        "breach", "default", "material breach", "non-payment",
        "failure to perform", "notice", "expiration",
        "manquement", "défaut", "violation substantielle",
        "non-paiement", "préavis", "expiration",
        "إخلال", "تقصير", "إخلال جوهري", "عدم الدفع", "إشعار", "انتهاء",
    ],
    "confidentiality": [
        "disclosure", "unauthorized use", "confidential information",
        "trade secret",
        "divulgation", "utilisation non autorisée",
        "information confidentielle", "secret commercial",
        "إفصاح", "استعمال غير مصرح", "معلومات سرية", "سر تجاري",
    ],
    "data_protection": [
        "personal data", "data breach", "security incident", "processing",
        "subprocessor", "unauthorized access",
        "données personnelles", "violation de données",
        "incident de sécurité", "traitement", "sous-traitant",
        "accès non autorisé",
        "البيانات الشخصية", "اختراق البيانات", "حادث أمني", "معالجة",
        "معالج فرعي", "وصول غير مصرح",
    ],
    "operational_support": [
        "repair", "maintenance request", "defect", "damage",
        "support request", "service failure", "downtime",
        "réparation", "demande de maintenance", "défaut", "dommage",
        "demande d'assistance", "défaillance du service", "interruption",
        "إصلاح", "طلب صيانة", "عيب", "ضرر", "طلب دعم", "فشل الخدمة", "انقطاع",
    ],
    "services_operations": [
        "statement of work", "scope of work", "service level", "support",
        "maintenance", "delivery", "performance", "change request",
        "énoncé des travaux", "périmètre des services", "niveau de service",
        "support", "maintenance", "livraison", "performance",
        "demande de changement",
        "بيان العمل", "نطاق العمل", "مستوى الخدمة", "الدعم", "الصيانة",
        "التسليم", "الأداء", "طلب تغيير",
    ],
    "delivery_acceptance": [
        "delivery", "acceptance", "acceptance criteria", "milestone",
        "handover", "testing",
        "livraison", "acceptation", "critères d'acceptation", "jalon",
        "remise", "test",
        "تسليم", "قبول", "معايير القبول", "مرحلة", "اختبار",
    ],
    "intellectual_property": [
        "invention", "patent", "work product", "assignment",
        "license", "deliverables", "ownership",
        "invention", "brevet", "création", "cession",
        "licence", "livrables", "propriété",
        "اختراع", "براءة اختراع", "تنازل", "ترخيص", "مخرجات العمل", "ملكية",
    ],
    "license": [
        "license", "permitted use", "usage rights", "subscription",
        "access rights",
        "licence", "utilisation autorisée", "droits d'utilisation",
        "abonnement", "droits d'accès",
        "ترخيص", "استخدام مسموح", "حقوق الاستخدام", "اشتراك", "حقوق الوصول",
    ],
    "restrictive_covenants": [
        "non-compete", "non-solicitation", "non-circumvention",
        "exclusivity", "exclusive dealing",
        "non-concurrence", "non-sollicitation", "non-contournement",
        "exclusivité",
        "عدم المنافسة", "عدم الاستقطاب", "عدم الالتفاف", "الحصرية",
    ],
    "governance_compliance": [
        "approval", "consent", "compliance", "sanctions", "anti-bribery",
        "change of control", "subcontracting",
        "approbation", "consentement", "conformité", "sanctions",
        "lutte contre la corruption", "changement de contrôle", "sous-traitance",
        "موافقة", "امتثال", "عقوبات", "مكافحة الرشوة",
        "تغيير السيطرة", "تعاقد من الباطن",
    ],
    "dispute_resolution": [
        "dispute", "claim", "arbitration", "mediation", "court",
        "governing law", "jurisdiction",
        "litige", "réclamation", "arbitrage", "médiation", "tribunal",
        "droit applicable", "juridiction",
        "نزاع", "مطالبة", "تحكيم", "وساطة", "محكمة",
        "القانون الواجب التطبيق", "اختصاص",
    ],
    "insurance": [
        "insurance", "policy", "coverage", "insured", "certificate of insurance",
        "assurance", "police", "couverture", "assuré", "attestation d'assurance",
        "تأمين", "وثيقة التأمين", "تغطية", "مؤمن عليه", "شهادة تأمين",
    ],
    "audit": [
        "audit", "inspection", "records", "books", "access to records",
        "audit", "inspection", "registres", "livres", "accès aux registres",
        "تدقيق", "تفتيش", "سجلات", "دفاتر", "الوصول إلى السجلات",
    ],
    "assignment": [
        "assignment", "assign", "transfer", "delegate",
        "cession", "céder", "transfert", "déléguer",
        "تنازل", "نقل", "تفويض",
    ],
    "indemnity": [
        "claim", "loss", "third party claim", "liability",
        "réclamation", "perte", "réclamation de tiers", "responsabilité",
        "مطالبة", "خسارة", "مطالبة طرف ثالث", "مسؤولية",
    ],
    "notice": [
        "notice", "notification", "address", "delivery",
        "avis", "notification", "adresse", "remise",
        "إشعار", "إخطار", "عنوان", "تسليم",
    ],
}


CONSEQUENCE_SIGNALS = {
    "payment": [
        "interest", "late fee", "suspension", "termination",
        "intérêt", "pénalité", "suspension", "résiliation",
        "فائدة", "غرامة", "تعليق", "فسخ",
    ],
    "termination": [
        "termination", "compensation", "damages", "suspension",
        "survival", "return", "destruction",
        "résiliation", "indemnité", "dommages", "suspension",
        "survie", "restitution", "destruction",
        "إنهاء", "تعويض", "أضرار", "تعليق", "استمرار", "إرجاع", "إتلاف",
    ],
    "confidentiality": [
        "damages", "injunction", "termination", "return", "destruction",
        "dommages", "injonction", "résiliation", "restitution", "destruction",
        "تعويض", "أمر قضائي", "فسخ", "إرجاع", "إتلاف",
    ],
    "data_protection": [
        "liability", "notification", "remediation", "penalty",
        "audit", "suspension",
        "responsabilité", "notification", "correction", "pénalité",
        "audit", "suspension",
        "مسؤولية", "إخطار", "معالجة", "غرامة", "تدقيق", "تعليق",
    ],
    "operational_support": [
        "repair", "replacement", "costs", "termination", "service credit",
        "réparation", "remplacement", "coûts", "résiliation", "crédit de service",
        "إصلاح", "استبدال", "تكاليف", "فسخ", "تعويض الخدمة",
    ],
    "services_operations": [
        "service credit", "termination", "suspension", "remediation",
        "acceptance", "re-performance",
        "crédit de service", "résiliation", "suspension", "correction",
        "acceptation", "réexécution",
        "تعويض الخدمة", "فسخ", "تعليق", "معالجة", "قبول", "إعادة التنفيذ",
    ],
    "delivery_acceptance": [
        "acceptance", "rejection", "payment", "remediation", "re-delivery",
        "acceptation", "rejet", "paiement", "correction", "nouvelle livraison",
        "قبول", "رفض", "دفع", "معالجة", "إعادة التسليم",
    ],
    "intellectual_property": [
        "assignment", "license", "ownership", "damages", "injunction",
        "cession", "licence", "propriété", "dommages", "injonction",
        "تنازل", "ترخيص", "ملكية", "تعويض", "أمر قضائي",
    ],
    "license": [
        "termination", "suspension", "revocation", "access restriction",
        "résiliation", "suspension", "révocation", "restriction d'accès",
        "فسخ", "تعليق", "إلغاء", "تقييد الوصول",
    ],
    "restrictive_covenants": [
        "injunction", "damages", "termination", "restriction",
        "injonction", "dommages", "résiliation", "restriction",
        "أمر قضائي", "تعويض", "فسخ", "قيد",
    ],
    "governance_compliance": [
        "termination", "suspension", "approval required", "audit",
        "résiliation", "suspension", "approbation requise", "audit",
        "فسخ", "تعليق", "موافقة مطلوبة", "تدقيق",
    ],
    "dispute_resolution": [
        "arbitration", "mediation", "court proceedings", "award",
        "arbitrage", "médiation", "procédure judiciaire", "sentence",
        "تحكيم", "وساطة", "إجراءات قضائية", "قرار تحكيمي",
    ],
    "insurance": [
        "coverage", "claim", "indemnification", "reimbursement",
        "couverture", "réclamation", "indemnisation", "remboursement",
        "تغطية", "مطالبة", "تعويض", "استرداد",
    ],
    "audit": [
        "access", "inspection", "remediation", "termination",
        "accès", "inspection", "correction", "résiliation",
        "وصول", "تفتيش", "معالجة", "فسخ",
    ],
    "assignment": [
        "void assignment", "consent required", "termination",
        "cession nulle", "consentement requis", "résiliation",
        "تنازل باطل", "موافقة مطلوبة", "فسخ",
    ],
    "indemnity": [
        "indemnification", "defense", "reimbursement", "hold harmless",
        "indemnisation", "défense", "remboursement", "tenir indemne",
        "تعويض", "دفاع", "استرداد", "إبقاء دون ضرر",
    ],
    "notice": [
        "deemed given", "effective notice", "delivery confirmed",
        "réputé reçu", "notification effective", "remise confirmée",
        "يعتبر مستلماً", "إشعار نافذ", "تأكيد التسليم",
    ],
}


def extract_generic_trigger(text: str, obligation_type: str) -> str:
    return first_matching_signal(
        text,
        TRIGGER_SIGNALS.get(obligation_type, []),
    )


def extract_generic_consequence(text: str, obligation_type: str) -> str:
    return first_matching_signal(
        text,
        CONSEQUENCE_SIGNALS.get(obligation_type, []),
    )


def build_obligation_pattern(
    obligation_type: str,
    signals: list[str],
    party: dict,
    obligation: dict,
) -> dict:
    return {
        "type": obligation_type,
        "signals": signals,
        "party": party,
        "obligation": obligation,
    }


OBLIGATION_PATTERNS = [
    build_obligation_pattern(
        "payment",
        [
            "payment", "pay", "invoice", "rent", "reimbursement",
            "expense reimbursement", "expenses", "fees", "paid by",
            "purchase price", "royalty", "commission", "subscription fee",
            "paiement", "loyer", "remboursement", "frais", "facture",
            "prix", "redevance", "commission", "abonnement",
            "الدفع", "يدفع", "الكراء", "السداد", "المصاريف",
            "تعويض المصاريف", "فاتورة", "ثمن", "إتاوة", "عمولة", "اشتراك",
        ],
        localized("paying party", "partie payeuse", "الطرف الملزم بالدفع"),
        localized(
            "make payment or reimbursement when due",
            "effectuer le paiement ou le remboursement à l'échéance",
            "أداء المبلغ أو تعويض المصاريف عند الاستحقاق",
        ),
    ),
    build_obligation_pattern(
        "confidentiality",
        [
            "confidentiality", "confidential", "trade secret",
            "non-disclosure", "confidentialité", "information confidentielle",
            "secret commercial", "السرية", "سرية", "معلومات سرية", "سر تجاري",
        ],
        localized("receiving party", "partie destinataire", "الطرف المتلقي للمعلومات"),
        localized(
            "protect confidential information and avoid unauthorized disclosure",
            "protéger les informations confidentielles et éviter toute divulgation non autorisée",
            "حماية المعلومات السرية وتجنب الإفصاح غير المصرح به",
        ),
    ),
    build_obligation_pattern(
        "termination",
        [
            "termination", "terminate", "default", "breach",
            "material breach", "cure period", "notice period",
            "résiliation", "résilier", "manquement",
            "violation substantielle", "préavis",
            "فسخ", "إنهاء", "إخلال", "إخلال جوهري", "إشعار",
        ],
        localized("terminating party", "partie résiliante", "الطرف الذي ينهي العقد"),
        localized(
            "follow termination conditions, notice requirements, and cure periods",
            "respecter les conditions de résiliation, les exigences de préavis et les délais de régularisation",
            "احترام شروط الإنهاء ومتطلبات الإشعار ومهل المعالجة",
        ),
    ),
    build_obligation_pattern(
        "data_protection",
        [
            "data protection", "personal data", "gdpr",
            "data breach", "security incident", "processing", "subprocessor",
            "protection des données", "données personnelles",
            "violation de données", "incident de sécurité", "traitement",
            "sous-traitant", "حماية البيانات", "البيانات الشخصية",
            "اختراق البيانات", "حادث أمني", "معالجة", "معالج فرعي",
        ],
        neutral_party(),
        localized(
            "protect personal, client, confidential, or regulated data",
            "protéger les données personnelles, client, confidentielles ou réglementées",
            "حماية البيانات الشخصية أو بيانات العميل أو البيانات السرية أو المنظمة",
        ),
    ),
    build_obligation_pattern(
        "operational_support",
        [
            "maintenance", "repair", "defect", "support",
            "service failure", "downtime", "entretien", "réparation",
            "défaut", "assistance", "défaillance du service",
            "الصيانة", "الإصلاح", "عيب", "الدعم", "فشل الخدمة",
        ],
        neutral_party(),
        localized(
            "perform support, maintenance, remediation, or repairs when required",
            "assurer le support, l'entretien, la correction ou les réparations lorsque requis",
            "تنفيذ الدعم أو الصيانة أو المعالجة أو الإصلاحات عند الاقتضاء",
        ),
    ),
    build_obligation_pattern(
        "services_operations",
        [
            "services", "scope of work", "statement of work", "service level",
            "support", "maintenance", "delivery", "performance",
            "change request", "services", "périmètre des services",
            "énoncé des travaux", "niveau de service", "support",
            "maintenance", "livraison", "performance", "demande de changement",
            "الخدمات", "نطاق العمل", "بيان العمل", "مستوى الخدمة",
            "الدعم", "الصيانة", "التسليم", "الأداء", "طلب تغيير",
        ],
        neutral_party(),
        localized(
            "perform services according to the agreed scope, standards, and operational process",
            "exécuter les services conformément au périmètre, aux standards et au processus opérationnel convenus",
            "تنفيذ الخدمات وفق النطاق والمعايير والإجراءات التشغيلية المتفق عليها",
        ),
    ),
    build_obligation_pattern(
        "delivery_acceptance",
        [
            "delivery", "deliverable", "acceptance", "acceptance criteria",
            "milestone", "testing", "livraison", "livrable",
            "acceptation", "critères d'acceptation", "jalon", "test",
            "تسليم", "مخرج", "قبول", "معايير القبول", "مرحلة", "اختبار",
        ],
        neutral_party(),
        localized(
            "deliver, review, accept, reject, or remediate deliverables according to agreed criteria",
            "livrer, examiner, accepter, rejeter ou corriger les livrables selon les critères convenus",
            "تسليم أو مراجعة أو قبول أو رفض أو معالجة المخرجات وفق المعايير المتفق عليها",
        ),
    ),
    build_obligation_pattern(
        "intellectual_property",
        [
            "intellectual property", "invention", "patent", "work product",
            "assignment", "license", "ownership", "deliverables",
            "propriété intellectuelle", "invention", "brevet", "création",
            "cession", "licence", "propriété", "livrables",
            "الملكية الفكرية", "اختراع", "براءة اختراع", "تنازل",
            "ترخيص", "ملكية", "مخرجات العمل",
        ],
        localized(
            "creating, owning, assigning, or licensing party",
            "partie créatrice, propriétaire, cédante ou concédante",
            "الطرف المنشئ أو المالك أو المتنازل أو المرخِّص",
        ),
        localized(
            "respect ownership, assignment, or license conditions for intellectual property",
            "respecter les conditions de propriété, de cession ou de licence de la propriété intellectuelle",
            "احترام شروط الملكية أو التنازل أو الترخيص المتعلقة بالملكية الفكرية",
        ),
    ),
    build_obligation_pattern(
        "license",
        [
            "license", "permitted use", "usage rights", "access rights",
            "subscription", "licence", "utilisation autorisée",
            "droits d'utilisation", "droits d'accès", "abonnement",
            "ترخيص", "استخدام مسموح", "حقوق الاستخدام", "حقوق الوصول", "اشتراك",
        ],
        localized("licensed party", "partie licenciée", "الطرف المرخَّص له"),
        localized(
            "use licensed rights, access, or technology only within the permitted scope",
            "utiliser les droits, accès ou technologies concédés uniquement dans le périmètre autorisé",
            "استخدام الحقوق أو الوصول أو التقنية المرخصة فقط ضمن النطاق المسموح",
        ),
    ),
    build_obligation_pattern(
        "restrictive_covenants",
        [
            "non-compete", "non-solicitation", "non-circumvention",
            "exclusivity", "exclusive dealing", "non-concurrence",
            "non-sollicitation", "non-contournement", "exclusivité",
            "عدم المنافسة", "عدم الاستقطاب", "عدم الالتفاف", "الحصرية",
        ],
        localized("restricted party", "partie soumise à restriction", "الطرف الخاضع للقيد"),
        localized(
            "comply with competitive, solicitation, exclusivity, or market-access restrictions",
            "respecter les restrictions de concurrence, de sollicitation, d'exclusivité ou d'accès au marché",
            "الامتثال لقيود المنافسة أو الاستقطاب أو الحصرية أو الوصول إلى السوق",
        ),
    ),
    build_obligation_pattern(
        "governance_compliance",
        [
            "approval", "consent", "compliance", "sanctions",
            "anti-bribery", "subcontracting", "change of control",
            "approbation", "consentement", "conformité", "sanctions",
            "lutte contre la corruption", "sous-traitance",
            "changement de contrôle", "موافقة", "امتثال", "عقوبات",
            "مكافحة الرشوة", "تعاقد من الباطن", "تغيير السيطرة",
        ],
        neutral_party(),
        localized(
            "obtain required approvals and comply with governance, regulatory, and control requirements",
            "obtenir les approbations requises et respecter les exigences de gouvernance, de conformité et de contrôle",
            "الحصول على الموافقات المطلوبة والامتثال لمتطلبات الحوكمة والتنظيم والرقابة",
        ),
    ),
    build_obligation_pattern(
        "dispute_resolution",
        [
            "dispute", "arbitration", "mediation", "court",
            "governing law", "jurisdiction", "litige", "arbitrage",
            "médiation", "tribunal", "droit applicable", "juridiction",
            "نزاع", "تحكيم", "وساطة", "محكمة", "القانون الواجب التطبيق", "اختصاص",
        ],
        localized("disputing party", "partie au litige", "الطرف في النزاع"),
        localized(
            "follow the agreed dispute resolution process and forum requirements",
            "suivre le processus de règlement des litiges et les exigences de forum convenus",
            "اتباع إجراءات حل النزاعات ومتطلبات الجهة المختصة المتفق عليها",
        ),
    ),
    build_obligation_pattern(
        "insurance",
        [
            "insurance", "policy", "coverage", "insured",
            "certificate of insurance", "assurance", "police",
            "couverture", "assuré", "attestation d'assurance",
            "تأمين", "وثيقة التأمين", "تغطية", "مؤمن عليه", "شهادة تأمين",
        ],
        localized("insured or responsible party", "partie assurée ou responsable", "الطرف المؤمن عليه أو المسؤول"),
        localized(
            "maintain required insurance coverage and provide evidence when required",
            "maintenir la couverture d'assurance requise et fournir les justificatifs lorsque requis",
            "الحفاظ على التغطية التأمينية المطلوبة وتقديم الإثبات عند الاقتضاء",
        ),
    ),
    build_obligation_pattern(
        "audit",
        [
            "audit", "inspection", "records", "books",
            "access to records", "audit", "inspection", "registres",
            "livres", "accès aux registres", "تدقيق", "تفتيش",
            "سجلات", "دفاتر", "الوصول إلى السجلات",
        ],
        neutral_party(),
        localized(
            "provide or permit audit, inspection, or access to records within the agreed limits",
            "fournir ou permettre l'audit, l'inspection ou l'accès aux registres dans les limites convenues",
            "توفير أو السماح بالتدقيق أو التفتيش أو الوصول إلى السجلات ضمن الحدود المتفق عليها",
        ),
    ),
    build_obligation_pattern(
        "assignment",
        [
            "assignment", "assign", "transfer", "delegate",
            "cession", "céder", "transfert", "déléguer",
            "تنازل", "نقل", "تفويض",
        ],
        localized("assigning party", "partie cédante", "الطرف المتنازل"),
        localized(
            "comply with assignment, transfer, delegation, or consent restrictions",
            "respecter les restrictions de cession, transfert, délégation ou consentement",
            "الامتثال لقيود التنازل أو النقل أو التفويض أو الموافقة",
        ),
    ),
    build_obligation_pattern(
        "indemnity",
        [
            "indemnity", "indemnification", "indemnify",
            "hold harmless", "claims", "losses",
            "indemnisation", "indemniser", "tenir indemne",
            "réclamations", "pertes",
            "تعويض", "تعويضات", "مطالبات", "خسائر",
        ],
        localized("indemnifying party", "partie indemnisante", "الطرف الملتزم بالتعويض"),
        localized(
            "indemnify or protect the other party against covered claims or losses",
            "indemniser ou protéger l'autre partie contre les réclamations ou pertes couvertes",
            "تعويض أو حماية الطرف الآخر من المطالبات أو الخسائر المشمولة",
        ),
    ),
    build_obligation_pattern(
        "notice",
        [
            "notice", "written notice", "notification", "notify",
            "avis", "notification", "préavis", "notifier",
            "إشعار", "إخطار", "إبلاغ",
        ],
        localized("notifying party", "partie notificatrice", "الطرف المرسل للإشعار"),
        localized(
            "send notices using the required method and address",
            "envoyer les notifications selon la méthode et l'adresse requises",
            "إرسال الإشعارات بالطريقة والعنوان المطلوبين",
        ),
    ),
]


def extract_obligations_from_clause(
    clause: dict,
    language: str = "en",
) -> list[dict]:

    language = normalize_language(language)

    if not isinstance(clause, dict):
        return []

    text = normalize_text(" ".join([
        str(clause.get("clause_title", "")),
        str(clause.get("title", "")),
        str(clause.get("quoted_text", "")),
        str(clause.get("original_text", "")),
        str(clause.get("clause_text", "")),
        str(clause.get("text", "")),
        str(clause.get("explanation_simple", "")),
        str(clause.get("legal_insight", "")),
    ]))

    obligations = []

    for pattern in OBLIGATION_PATTERNS:
        if any(signal.lower() in text for signal in pattern["signals"]):
            obligation_type = pattern["type"]

            obligations.append({
                "type": obligation_type,
                "party": pattern["party"].get(
                    language,
                    pattern["party"]["en"],
                ),
                "obligation": pattern["obligation"].get(
                    language,
                    pattern["obligation"]["en"],
                ),
                "trigger": extract_generic_trigger(
                    text,
                    obligation_type,
                ),
                "deadline": extract_deadline(text),
                "consequence": extract_generic_consequence(
                    text,
                    obligation_type,
                ),
                "confidence": "high"
                if first_matching_signal(text, pattern["signals"])
                else "medium",
            })

    return obligations


def extract_contract_obligations(
    clauses: list[dict],
    language: str = "en",
) -> list[dict]:

    language = normalize_language(language)
    obligations = []

    for clause in clauses:
        if not isinstance(clause, dict):
            continue

        clause_obligations = extract_obligations_from_clause(
            clause,
            language,
        )

        for obligation in clause_obligations:
            obligation["source_clause"] = clause.get(
                "clause_title",
                clause.get("title", ""),
            )
            obligation["source_clause_id"] = clause.get(
                "id",
                clause.get("clause_id", ""),
            )
            obligation["source_clause_type"] = clause.get(
                "clause_type",
                clause.get("type", ""),
            )
            obligation["risk_level"] = clause.get(
                "risk_level",
                "",
            )
            obligations.append(obligation)

    return obligations


import re


SUPPORTED_LANGUAGES = {"en", "fr", "ar"}


def normalize_language(language: str) -> str:
    language = str(language or "en").lower().strip()
    return language if language in SUPPORTED_LANGUAGES else "en"


def normalize_text(text: str) -> str:
    text = str(text or "").lower()
    text = text.replace("–", "-").replace("—", "-")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def first_matching_signal(text: str, signals: list[str]) -> str:
    for signal in signals:
        if signal.lower() in text:
            return signal
    return ""


def localized(en: str, fr: str, ar: str) -> dict:
    return {
        "en": en,
        "fr": fr,
        "ar": ar,
    }


def neutral_party() -> dict:
    return localized(
        "responsible party",
        "partie responsable",
        "الطرف المسؤول",
    )


def extract_deadline(text: str) -> str:
    patterns = [
        r"within\s+\d+\s+(days?|months?|years?)",
        r"\d+\s+(days?|months?|years?)",
        r"notice period",
        r"cure period",
        r"due date",
        r"effective date",
        r"expiration date",
        r"renewal date",
        r"suspension period",
        r"force majeure period",
        r"business continuity period",
        r"retention period",
        r"within\s+\d+\s+business\s+days?",
        r"dans\s+un\s+délai\s+de\s+\d+\s+jours?",
        r"\d+\s+jours?",
        r"préavis",
        r"délai de régularisation",
        r"date d['’]échéance",
        r"date d'effet",
        r"date d'expiration",
        r"période de suspension",
        r"période de force majeure",
        r"période de conservation",
        r"خلال\s+\d+\s+يوم",
        r"\d+\s+يوماً",
        r"\d+\s+يوم",
        r"مهلة",
        r"إشعار",
        r"تاريخ السريان",
        r"تاريخ الانتهاء",
        r"فترة التعليق",
        r"فترة القوة القاهرة",
        r"فترة الاحتفاظ",
    ]

    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            return match.group(0)

    return ""


TRIGGER_SIGNALS = {
    "payment": [
        "invoice", "delivery", "milestone", "due date",
        "expense statement", "voucher", "acceptance",
        "facture", "livraison", "jalon", "échéance",
        "note de frais", "justificatif", "acceptation",
        "فاتورة", "تسليم", "مرحلة", "استحقاق", "إيصال", "قبول",
    ],
    "termination": [
        "breach", "default", "material breach", "non-payment",
        "failure to perform", "notice", "expiration",
        "manquement", "défaut", "violation substantielle",
        "non-paiement", "préavis", "expiration",
        "إخلال", "تقصير", "إخلال جوهري", "عدم الدفع", "إشعار", "انتهاء",
    ],
    "confidentiality": [
        "disclosure", "unauthorized use", "confidential information",
        "trade secret",
        "divulgation", "utilisation non autorisée",
        "information confidentielle", "secret commercial",
        "إفصاح", "استعمال غير مصرح", "معلومات سرية", "سر تجاري",
    ],
    "data_protection": [
        "personal data", "data breach", "security incident", "processing",
        "subprocessor", "unauthorized access",
        "données personnelles", "violation de données",
        "incident de sécurité", "traitement", "sous-traitant",
        "accès non autorisé",
        "البيانات الشخصية", "اختراق البيانات", "حادث أمني", "معالجة",
        "معالج فرعي", "وصول غير مصرح",
    ],
    "operational_support": [
        "repair", "maintenance request", "defect", "damage",
        "support request", "service failure", "downtime",
        "réparation", "demande de maintenance", "défaut", "dommage",
        "demande d'assistance", "défaillance du service", "interruption",
        "إصلاح", "طلب صيانة", "عيب", "ضرر", "طلب دعم", "فشل الخدمة", "انقطاع",
    ],
    "services_operations": [
        "statement of work", "scope of work", "service level", "support",
        "maintenance", "delivery", "performance", "change request",
        "énoncé des travaux", "périmètre des services", "niveau de service",
        "support", "maintenance", "livraison", "performance",
        "demande de changement",
        "بيان العمل", "نطاق العمل", "مستوى الخدمة", "الدعم", "الصيانة",
        "التسليم", "الأداء", "طلب تغيير",
    ],
    "delivery_acceptance": [
        "delivery", "acceptance", "acceptance criteria", "milestone",
        "handover", "testing",
        "livraison", "acceptation", "critères d'acceptation", "jalon",
        "remise", "test",
        "تسليم", "قبول", "معايير القبول", "مرحلة", "اختبار",
    ],
    "intellectual_property": [
        "invention", "patent", "work product", "assignment",
        "license", "deliverables", "ownership",
        "invention", "brevet", "création", "cession",
        "licence", "livrables", "propriété",
        "اختراع", "براءة اختراع", "تنازل", "ترخيص", "مخرجات العمل", "ملكية",
    ],
    "license": [
        "license", "permitted use", "usage rights", "subscription",
        "access rights",
        "licence", "utilisation autorisée", "droits d'utilisation",
        "abonnement", "droits d'accès",
        "ترخيص", "استخدام مسموح", "حقوق الاستخدام", "اشتراك", "حقوق الوصول",
    ],
    "restrictive_covenants": [
        "non-compete", "non-solicitation", "non-circumvention",
        "exclusivity", "exclusive dealing",
        "non-concurrence", "non-sollicitation", "non-contournement",
        "exclusivité",
        "عدم المنافسة", "عدم الاستقطاب", "عدم الالتفاف", "الحصرية",
    ],
    "governance_compliance": [
        "approval", "consent", "compliance", "sanctions", "anti-bribery",
        "change of control", "subcontracting",
        "approbation", "consentement", "conformité", "sanctions",
        "lutte contre la corruption", "changement de contrôle", "sous-traitance",
        "موافقة", "امتثال", "عقوبات", "مكافحة الرشوة",
        "تغيير السيطرة", "تعاقد من الباطن",
    ],
    "dispute_resolution": [
        "dispute", "claim", "arbitration", "mediation", "court",
        "governing law", "jurisdiction",
        "litige", "réclamation", "arbitrage", "médiation", "tribunal",
        "droit applicable", "juridiction",
        "نزاع", "مطالبة", "تحكيم", "وساطة", "محكمة",
        "القانون الواجب التطبيق", "اختصاص",
    ],
    "insurance": [
        "insurance", "policy", "coverage", "insured", "certificate of insurance",
        "assurance", "police", "couverture", "assuré", "attestation d'assurance",
        "تأمين", "وثيقة التأمين", "تغطية", "مؤمن عليه", "شهادة تأمين",
    ],
    "audit": [
        "audit", "inspection", "records", "books", "access to records",
        "audit", "inspection", "registres", "livres", "accès aux registres",
        "تدقيق", "تفتيش", "سجلات", "دفاتر", "الوصول إلى السجلات",
    ],
    "assignment": [
        "assignment", "assign", "transfer", "delegate",
        "cession", "céder", "transfert", "déléguer",
        "تنازل", "نقل", "تفويض",
    ],
    "indemnity": [
        "claim", "loss", "third party claim", "liability",
        "réclamation", "perte", "réclamation de tiers", "responsabilité",
        "مطالبة", "خسارة", "مطالبة طرف ثالث", "مسؤولية",
    ],
    "notice": [
        "notice", "notification", "address", "delivery",
        "avis", "notification", "adresse", "remise",
        "إشعار", "إخطار", "عنوان", "تسليم",
    ],
    "force_majeure": [
        "force majeure", "act of god", "unforeseeable event",
        "beyond reasonable control", "natural disaster", "epidemic",
        "pandemic", "war", "strike", "government action",
        "cas de force majeure", "événement imprévisible",
        "hors du contrôle raisonnable", "catastrophe naturelle",
        "épidémie", "pandémie", "guerre", "grève", "action gouvernementale",
        "القوة القاهرة", "حدث غير متوقع", "خارج السيطرة المعقولة",
        "كارثة طبيعية", "وباء", "جائحة", "حرب", "إضراب", "إجراء حكومي",
    ],
    "tax": [
        "tax", "taxes", "vat", "gst", "withholding", "gross-up",
        "tax invoice", "sales tax", "duties", "levies",
        "impôt", "impôts", "taxe", "tva", "retenue à la source",
        "majoration fiscale", "facture fiscale", "droits", "prélèvements",
        "ضريبة", "ضرائب", "القيمة المضافة", "اقتطاع", "استقطاع",
        "تعويض ضريبي", "فاتورة ضريبية", "رسوم", "جبايات",
    ],
    "warranties": [
        "warranty", "warranties", "representation", "representations",
        "representations and warranties", "as is", "disclaimer of warranty",
        "fitness for purpose", "merchantability", "defect warranty",
        "garantie", "garanties", "déclaration", "déclarations",
        "déclarations et garanties", "en l'état", "exclusion de garantie",
        "aptitude à l'usage", "vice", "ضمان", "ضمانات", "إقرار",
        "إقرارات", "الإقرارات والضمانات", "كما هو", "استبعاد الضمان",
        "ملاءمة للغرض", "عيب",
    ],
    "renewal": [
        "renewal", "automatic renewal", "auto-renewal", "renewal term",
        "extension term", "successive terms", "non-renewal",
        "renouvellement", "reconduction automatique", "période de renouvellement",
        "durée de renouvellement", "non-renouvellement",
        "تجديد", "تجديد تلقائي", "مدة التجديد", "فترات متتالية", "عدم التجديد",
    ],
    "suspension": [
        "suspension", "suspend", "suspend services", "service suspension",
        "reinstatement", "restore service", "access suspension",
        "suspension", "suspendre", "suspendre les services",
        "rétablissement", "restaurer le service",
        "تعليق", "يعلق", "تعليق الخدمات", "استئناف الخدمة",
        "إعادة الخدمة", "تعليق الوصول",
    ],
    "business_continuity": [
        "business continuity", "disaster recovery", "bcp", "drp",
        "backup", "restore", "recovery time objective", "rto",
        "recovery point objective", "rpo", "contingency plan",
        "continuité d'activité", "reprise après sinistre", "sauvegarde",
        "restauration", "plan de continuité", "خطة استمرارية الأعمال",
        "استمرارية الأعمال", "التعافي من الكوارث", "نسخ احتياطي",
        "استعادة", "خطة طوارئ",
    ],
    "publicity": [
        "publicity", "press release", "public announcement", "use of name",
        "logo", "trademark in marketing", "case study", "reference customer",
        "publicité", "communiqué de presse", "annonce publique",
        "utilisation du nom", "logo", "étude de cas", "référence client",
        "دعاية", "بيان صحفي", "إعلان عام", "استخدام الاسم",
        "الشعار", "دراسة حالة", "عميل مرجعي",
    ],
    "severability": [
        "severability", "invalid provision", "unenforceable provision",
        "severed", "valid substitute", "remaining provisions",
        "divisibilité", "clause invalide", "clause inapplicable",
        "séparée", "disposition de remplacement", "قابلية الفصل",
        "حكم غير صحيح", "حكم غير قابل للتنفيذ", "فصل الحكم",
        "حكم بديل", "باقي الأحكام",
    ],
    "survival": [
        "survival", "survive termination", "survive expiry",
        "post-termination obligations", "continue after termination",
        "survie", "survivent à la résiliation",
        "obligations postérieures à la résiliation",
        "continuer après la résiliation", "استمرار", "تستمر بعد الإنهاء",
        "تستمر بعد الانقضاء", "التزامات ما بعد الإنهاء",
    ],
    "amendment": [
        "amendment", "amendments", "modified only in writing",
        "change order", "variation", "written modification",
        "modification", "avenant", "modifié uniquement par écrit",
        "ordre de modification", "changement", "تعديل", "تعديلات",
        "لا يعدل إلا كتابة", "أمر تغيير", "تغيير كتابي",
    ],
    "waiver": [
        "waiver", "no waiver", "failure to enforce", "delay in exercising",
        "waive", "single waiver", "renonciation", "absence de renonciation",
        "défaut d'exercice", "retard dans l'exercice", "renoncer",
        "تنازل", "عدم التنازل", "عدم ممارسة الحق", "التأخر في ممارسة الحق",
        "يتنازل",
    ],
}


CONSEQUENCE_SIGNALS = {
    "payment": [
        "interest", "late fee", "suspension", "termination",
        "intérêt", "pénalité", "suspension", "résiliation",
        "فائدة", "غرامة", "تعليق", "فسخ",
    ],
    "termination": [
        "termination", "compensation", "damages", "suspension",
        "survival", "return", "destruction",
        "résiliation", "indemnité", "dommages", "suspension",
        "survie", "restitution", "destruction",
        "إنهاء", "تعويض", "أضرار", "تعليق", "استمرار", "إرجاع", "إتلاف",
    ],
    "confidentiality": [
        "damages", "injunction", "termination", "return", "destruction",
        "dommages", "injonction", "résiliation", "restitution", "destruction",
        "تعويض", "أمر قضائي", "فسخ", "إرجاع", "إتلاف",
    ],
    "data_protection": [
        "liability", "notification", "remediation", "penalty",
        "audit", "suspension",
        "responsabilité", "notification", "correction", "pénalité",
        "audit", "suspension",
        "مسؤولية", "إخطار", "معالجة", "غرامة", "تدقيق", "تعليق",
    ],
    "operational_support": [
        "repair", "replacement", "costs", "termination", "service credit",
        "réparation", "remplacement", "coûts", "résiliation", "crédit de service",
        "إصلاح", "استبدال", "تكاليف", "فسخ", "تعويض الخدمة",
    ],
    "services_operations": [
        "service credit", "termination", "suspension", "remediation",
        "acceptance", "re-performance",
        "crédit de service", "résiliation", "suspension", "correction",
        "acceptation", "réexécution",
        "تعويض الخدمة", "فسخ", "تعليق", "معالجة", "قبول", "إعادة التنفيذ",
    ],
    "delivery_acceptance": [
        "acceptance", "rejection", "payment", "remediation", "re-delivery",
        "acceptation", "rejet", "paiement", "correction", "nouvelle livraison",
        "قبول", "رفض", "دفع", "معالجة", "إعادة التسليم",
    ],
    "intellectual_property": [
        "assignment", "license", "ownership", "damages", "injunction",
        "cession", "licence", "propriété", "dommages", "injonction",
        "تنازل", "ترخيص", "ملكية", "تعويض", "أمر قضائي",
    ],
    "license": [
        "termination", "suspension", "revocation", "access restriction",
        "résiliation", "suspension", "révocation", "restriction d'accès",
        "فسخ", "تعليق", "إلغاء", "تقييد الوصول",
    ],
    "restrictive_covenants": [
        "injunction", "damages", "termination", "restriction",
        "injonction", "dommages", "résiliation", "restriction",
        "أمر قضائي", "تعويض", "فسخ", "قيد",
    ],
    "governance_compliance": [
        "termination", "suspension", "approval required", "audit",
        "résiliation", "suspension", "approbation requise", "audit",
        "فسخ", "تعليق", "موافقة مطلوبة", "تدقيق",
    ],
    "dispute_resolution": [
        "arbitration", "mediation", "court proceedings", "award",
        "arbitrage", "médiation", "procédure judiciaire", "sentence",
        "تحكيم", "وساطة", "إجراءات قضائية", "قرار تحكيمي",
    ],
    "insurance": [
        "coverage", "claim", "indemnification", "reimbursement",
        "couverture", "réclamation", "indemnisation", "remboursement",
        "تغطية", "مطالبة", "تعويض", "استرداد",
    ],
    "audit": [
        "access", "inspection", "remediation", "termination",
        "accès", "inspection", "correction", "résiliation",
        "وصول", "تفتيش", "معالجة", "فسخ",
    ],
    "assignment": [
        "void assignment", "consent required", "termination",
        "cession nulle", "consentement requis", "résiliation",
        "تنازل باطل", "موافقة مطلوبة", "فسخ",
    ],
    "indemnity": [
        "indemnification", "defense", "reimbursement", "hold harmless",
        "indemnisation", "défense", "remboursement", "tenir indemne",
        "تعويض", "دفاع", "استرداد", "إبقاء دون ضرر",
    ],
    "notice": [
        "deemed given", "effective notice", "delivery confirmed",
        "réputé reçu", "notification effective", "remise confirmée",
        "يعتبر مستلماً", "إشعار نافذ", "تأكيد التسليم",
    ],
    "force_majeure": [
        "suspension", "excuse from performance", "termination",
        "extension", "mitigation", "notice", "cost allocation",
        "suspension", "exonération d'exécution", "résiliation",
        "prolongation", "atténuation", "notification", "répartition des coûts",
        "تعليق", "إعفاء من التنفيذ", "فسخ", "تمديد", "تخفيف", "إشعار", "توزيع التكاليف",
    ],
    "tax": [
        "withholding", "gross-up", "reimbursement", "tax liability",
        "invoice adjustment", "penalty", "retenue à la source",
        "majoration fiscale", "remboursement", "responsabilité fiscale",
        "ajustement de facture", "pénalité", "اقتطاع", "تعويض ضريبي",
        "استرداد", "مسؤولية ضريبية", "تعديل الفاتورة", "غرامة",
    ],
    "warranties": [
        "repair", "replacement", "refund", "re-performance", "disclaimer",
        "exclusive remedy", "réparation", "remplacement", "remboursement",
        "réexécution", "exclusion", "recours exclusif",
        "إصلاح", "استبدال", "رد المبلغ", "إعادة التنفيذ", "استبعاد", "وسيلة انتصاف حصرية",
    ],
    "renewal": [
        "extension", "automatic renewal", "price change", "termination",
        "non-renewal notice", "prolongation", "reconduction automatique",
        "changement de prix", "résiliation", "préavis de non-renouvellement",
        "تمديد", "تجديد تلقائي", "تغيير السعر", "فسخ", "إشعار عدم التجديد",
    ],
    "suspension": [
        "service interruption", "reinstatement", "termination", "fees due",
        "data access restriction", "interruption de service", "rétablissement",
        "résiliation", "sommes dues", "restriction d'accès aux données",
        "انقطاع الخدمة", "استئناف الخدمة", "فسخ", "مبالغ مستحقة", "تقييد الوصول إلى البيانات",
    ],
    "business_continuity": [
        "restore service", "backup recovery", "continuity plan", "incident response",
        "service credit", "restaurer le service", "récupération des sauvegardes",
        "plan de continuité", "réponse aux incidents", "crédit de service",
        "استعادة الخدمة", "استعادة النسخ الاحتياطية", "خطة الاستمرارية",
        "استجابة للحوادث", "تعويض الخدمة",
    ],
    "publicity": [
        "approval required", "removal", "damages", "injunction",
        "approbation requise", "retrait", "dommages", "injonction",
        "موافقة مطلوبة", "إزالة", "تعويض", "أمر قضائي",
    ],
    "severability": [
        "severed provision", "replacement clause", "remaining agreement continues",
        "renegotiation", "clause séparée", "clause de remplacement",
        "maintien du contrat", "renégociation", "فصل الحكم", "حكم بديل",
        "استمرار العقد", "إعادة التفاوض",
    ],
    "survival": [
        "continued obligation", "post-termination duty", "enforcement",
        "return", "destruction", "obligation continue", "obligation postérieure",
        "exécution", "restitution", "destruction", "التزام مستمر",
        "التزام بعد الإنهاء", "تنفيذ", "إرجاع", "إتلاف",
    ],
    "amendment": [
        "invalid change", "written approval required", "change order",
        "version control", "modification invalide", "approbation écrite requise",
        "ordre de modification", "contrôle des versions", "تعديل غير صحيح",
        "موافقة كتابية مطلوبة", "أمر تغيير", "ضبط الإصدارات",
    ],
    "waiver": [
        "rights preserved", "specific waiver", "written waiver",
        "future enforcement", "droits préservés", "renonciation spécifique",
        "renonciation écrite", "exécution future", "الحقوق محفوظة",
        "تنازل محدد", "تنازل كتابي", "تنفيذ مستقبلي",
    ],
}


def extract_generic_trigger(text: str, obligation_type: str) -> str:
    return first_matching_signal(
        text,
        TRIGGER_SIGNALS.get(obligation_type, []),
    )


def extract_generic_consequence(text: str, obligation_type: str) -> str:
    return first_matching_signal(
        text,
        CONSEQUENCE_SIGNALS.get(obligation_type, []),
    )


def build_obligation_pattern(
    obligation_type: str,
    signals: list[str],
    party: dict,
    obligation: dict,
) -> dict:
    return {
        "type": obligation_type,
        "signals": signals,
        "party": party,
        "obligation": obligation,
    }


OBLIGATION_PATTERNS = [
    build_obligation_pattern(
        "payment",
        [
            "payment", "pay", "invoice", "rent", "reimbursement",
            "expense reimbursement", "expenses", "fees", "paid by",
            "purchase price", "royalty", "commission", "subscription fee",
            "paiement", "loyer", "remboursement", "frais", "facture",
            "prix", "redevance", "commission", "abonnement",
            "الدفع", "يدفع", "الكراء", "السداد", "المصاريف",
            "تعويض المصاريف", "فاتورة", "ثمن", "إتاوة", "عمولة", "اشتراك",
        ],
        localized("paying party", "partie payeuse", "الطرف الملزم بالدفع"),
        localized(
            "make payment or reimbursement when due",
            "effectuer le paiement ou le remboursement à l'échéance",
            "أداء المبلغ أو تعويض المصاريف عند الاستحقاق",
        ),
    ),
    build_obligation_pattern(
        "confidentiality",
        [
            "confidentiality", "confidential", "trade secret",
            "non-disclosure", "confidentialité", "information confidentielle",
            "secret commercial", "السرية", "سرية", "معلومات سرية", "سر تجاري",
        ],
        localized("receiving party", "partie destinataire", "الطرف المتلقي للمعلومات"),
        localized(
            "protect confidential information and avoid unauthorized disclosure",
            "protéger les informations confidentielles et éviter toute divulgation non autorisée",
            "حماية المعلومات السرية وتجنب الإفصاح غير المصرح به",
        ),
    ),
    build_obligation_pattern(
        "termination",
        [
            "termination", "terminate", "default", "breach",
            "material breach", "cure period", "notice period",
            "résiliation", "résilier", "manquement",
            "violation substantielle", "préavis",
            "فسخ", "إنهاء", "إخلال", "إخلال جوهري", "إشعار",
        ],
        localized("terminating party", "partie résiliante", "الطرف الذي ينهي العقد"),
        localized(
            "follow termination conditions, notice requirements, and cure periods",
            "respecter les conditions de résiliation, les exigences de préavis et les délais de régularisation",
            "احترام شروط الإنهاء ومتطلبات الإشعار ومهل المعالجة",
        ),
    ),
    build_obligation_pattern(
        "data_protection",
        [
            "data protection", "personal data", "gdpr",
            "data breach", "security incident", "processing", "subprocessor",
            "protection des données", "données personnelles",
            "violation de données", "incident de sécurité", "traitement",
            "sous-traitant", "حماية البيانات", "البيانات الشخصية",
            "اختراق البيانات", "حادث أمني", "معالجة", "معالج فرعي",
        ],
        neutral_party(),
        localized(
            "protect personal, client, confidential, or regulated data",
            "protéger les données personnelles, client, confidentielles ou réglementées",
            "حماية البيانات الشخصية أو بيانات العميل أو البيانات السرية أو المنظمة",
        ),
    ),
    build_obligation_pattern(
        "operational_support",
        [
            "maintenance", "repair", "defect", "support",
            "service failure", "downtime", "entretien", "réparation",
            "défaut", "assistance", "défaillance du service",
            "الصيانة", "الإصلاح", "عيب", "الدعم", "فشل الخدمة",
        ],
        neutral_party(),
        localized(
            "perform support, maintenance, remediation, or repairs when required",
            "assurer le support, l'entretien, la correction ou les réparations lorsque requis",
            "تنفيذ الدعم أو الصيانة أو المعالجة أو الإصلاحات عند الاقتضاء",
        ),
    ),
    build_obligation_pattern(
        "services_operations",
        [
            "services", "scope of work", "statement of work", "service level",
            "support", "maintenance", "delivery", "performance",
            "change request", "services", "périmètre des services",
            "énoncé des travaux", "niveau de service", "support",
            "maintenance", "livraison", "performance", "demande de changement",
            "الخدمات", "نطاق العمل", "بيان العمل", "مستوى الخدمة",
            "الدعم", "الصيانة", "التسليم", "الأداء", "طلب تغيير",
        ],
        neutral_party(),
        localized(
            "perform services according to the agreed scope, standards, and operational process",
            "exécuter les services conformément au périmètre, aux standards et au processus opérationnel convenus",
            "تنفيذ الخدمات وفق النطاق والمعايير والإجراءات التشغيلية المتفق عليها",
        ),
    ),
    build_obligation_pattern(
        "delivery_acceptance",
        [
            "delivery", "deliverable", "acceptance", "acceptance criteria",
            "milestone", "testing", "livraison", "livrable",
            "acceptation", "critères d'acceptation", "jalon", "test",
            "تسليم", "مخرج", "قبول", "معايير القبول", "مرحلة", "اختبار",
        ],
        neutral_party(),
        localized(
            "deliver, review, accept, reject, or remediate deliverables according to agreed criteria",
            "livrer, examiner, accepter, rejeter ou corriger les livrables selon les critères convenus",
            "تسليم أو مراجعة أو قبول أو رفض أو معالجة المخرجات وفق المعايير المتفق عليها",
        ),
    ),
    build_obligation_pattern(
        "intellectual_property",
        [
            "intellectual property", "invention", "patent", "work product",
            "assignment", "license", "ownership", "deliverables",
            "propriété intellectuelle", "invention", "brevet", "création",
            "cession", "licence", "propriété", "livrables",
            "الملكية الفكرية", "اختراع", "براءة اختراع", "تنازل",
            "ترخيص", "ملكية", "مخرجات العمل",
        ],
        localized(
            "creating, owning, assigning, or licensing party",
            "partie créatrice, propriétaire, cédante ou concédante",
            "الطرف المنشئ أو المالك أو المتنازل أو المرخِّص",
        ),
        localized(
            "respect ownership, assignment, or license conditions for intellectual property",
            "respecter les conditions de propriété, de cession ou de licence de la propriété intellectuelle",
            "احترام شروط الملكية أو التنازل أو الترخيص المتعلقة بالملكية الفكرية",
        ),
    ),
    build_obligation_pattern(
        "license",
        [
            "license", "permitted use", "usage rights", "access rights",
            "subscription", "licence", "utilisation autorisée",
            "droits d'utilisation", "droits d'accès", "abonnement",
            "ترخيص", "استخدام مسموح", "حقوق الاستخدام", "حقوق الوصول", "اشتراك",
        ],
        localized("licensed party", "partie licenciée", "الطرف المرخَّص له"),
        localized(
            "use licensed rights, access, or technology only within the permitted scope",
            "utiliser les droits, accès ou technologies concédés uniquement dans le périmètre autorisé",
            "استخدام الحقوق أو الوصول أو التقنية المرخصة فقط ضمن النطاق المسموح",
        ),
    ),
    build_obligation_pattern(
        "restrictive_covenants",
        [
            "non-compete", "non-solicitation", "non-circumvention",
            "exclusivity", "exclusive dealing", "non-concurrence",
            "non-sollicitation", "non-contournement", "exclusivité",
            "عدم المنافسة", "عدم الاستقطاب", "عدم الالتفاف", "الحصرية",
        ],
        localized("restricted party", "partie soumise à restriction", "الطرف الخاضع للقيد"),
        localized(
            "comply with competitive, solicitation, exclusivity, or market-access restrictions",
            "respecter les restrictions de concurrence, de sollicitation, d'exclusivité ou d'accès au marché",
            "الامتثال لقيود المنافسة أو الاستقطاب أو الحصرية أو الوصول إلى السوق",
        ),
    ),
    build_obligation_pattern(
        "governance_compliance",
        [
            "approval", "consent", "compliance", "sanctions",
            "anti-bribery", "subcontracting", "change of control",
            "approbation", "consentement", "conformité", "sanctions",
            "lutte contre la corruption", "sous-traitance",
            "changement de contrôle", "موافقة", "امتثال", "عقوبات",
            "مكافحة الرشوة", "تعاقد من الباطن", "تغيير السيطرة",
        ],
        neutral_party(),
        localized(
            "obtain required approvals and comply with governance, regulatory, and control requirements",
            "obtenir les approbations requises et respecter les exigences de gouvernance, de conformité et de contrôle",
            "الحصول على الموافقات المطلوبة والامتثال لمتطلبات الحوكمة والتنظيم والرقابة",
        ),
    ),
    build_obligation_pattern(
        "dispute_resolution",
        [
            "dispute", "arbitration", "mediation", "court",
            "governing law", "jurisdiction", "litige", "arbitrage",
            "médiation", "tribunal", "droit applicable", "juridiction",
            "نزاع", "تحكيم", "وساطة", "محكمة", "القانون الواجب التطبيق", "اختصاص",
        ],
        localized("disputing party", "partie au litige", "الطرف في النزاع"),
        localized(
            "follow the agreed dispute resolution process and forum requirements",
            "suivre le processus de règlement des litiges et les exigences de forum convenus",
            "اتباع إجراءات حل النزاعات ومتطلبات الجهة المختصة المتفق عليها",
        ),
    ),
    build_obligation_pattern(
        "insurance",
        [
            "insurance", "policy", "coverage", "insured",
            "certificate of insurance", "assurance", "police",
            "couverture", "assuré", "attestation d'assurance",
            "تأمين", "وثيقة التأمين", "تغطية", "مؤمن عليه", "شهادة تأمين",
        ],
        localized("insured or responsible party", "partie assurée ou responsable", "الطرف المؤمن عليه أو المسؤول"),
        localized(
            "maintain required insurance coverage and provide evidence when required",
            "maintenir la couverture d'assurance requise et fournir les justificatifs lorsque requis",
            "الحفاظ على التغطية التأمينية المطلوبة وتقديم الإثبات عند الاقتضاء",
        ),
    ),
    build_obligation_pattern(
        "audit",
        [
            "audit", "inspection", "records", "books",
            "access to records", "audit", "inspection", "registres",
            "livres", "accès aux registres", "تدقيق", "تفتيش",
            "سجلات", "دفاتر", "الوصول إلى السجلات",
        ],
        neutral_party(),
        localized(
            "provide or permit audit, inspection, or access to records within the agreed limits",
            "fournir ou permettre l'audit, l'inspection ou l'accès aux registres dans les limites convenues",
            "توفير أو السماح بالتدقيق أو التفتيش أو الوصول إلى السجلات ضمن الحدود المتفق عليها",
        ),
    ),
    build_obligation_pattern(
        "assignment",
        [
            "assignment", "assign", "transfer", "delegate",
            "cession", "céder", "transfert", "déléguer",
            "تنازل", "نقل", "تفويض",
        ],
        localized("assigning party", "partie cédante", "الطرف المتنازل"),
        localized(
            "comply with assignment, transfer, delegation, or consent restrictions",
            "respecter les restrictions de cession, transfert, délégation ou consentement",
            "الامتثال لقيود التنازل أو النقل أو التفويض أو الموافقة",
        ),
    ),
    build_obligation_pattern(
        "indemnity",
        [
            "indemnity", "indemnification", "indemnify",
            "hold harmless", "claims", "losses",
            "indemnisation", "indemniser", "tenir indemne",
            "réclamations", "pertes",
            "تعويض", "تعويضات", "مطالبات", "خسائر",
        ],
        localized("indemnifying party", "partie indemnisante", "الطرف الملتزم بالتعويض"),
        localized(
            "indemnify or protect the other party against covered claims or losses",
            "indemniser ou protéger l'autre partie contre les réclamations ou pertes couvertes",
            "تعويض أو حماية الطرف الآخر من المطالبات أو الخسائر المشمولة",
        ),
    ),
    build_obligation_pattern(
        "notice",
        [
            "notice", "written notice", "notification", "notify",
            "avis", "notification", "préavis", "notifier",
            "إشعار", "إخطار", "إبلاغ",
        ],
        localized("notifying party", "partie notificatrice", "الطرف المرسل للإشعار"),
        localized(
            "send notices using the required method and address",
            "envoyer les notifications selon la méthode et l'adresse requises",
            "إرسال الإشعارات بالطريقة والعنوان المطلوبين",
        ),
    ),
    build_obligation_pattern(
        "force_majeure",
        TRIGGER_SIGNALS["force_majeure"],
        neutral_party(),
        localized(
            "notify, mitigate, document, and manage performance impacts caused by force majeure events",
            "notifier, atténuer, documenter et gérer les impacts d'exécution causés par les événements de force majeure",
            "الإشعار والتخفيف والتوثيق وإدارة آثار التنفيذ الناتجة عن أحداث القوة القاهرة",
        ),
    ),
    build_obligation_pattern(
        "tax",
        TRIGGER_SIGNALS["tax"],
        localized("tax-responsible party", "partie responsable fiscalement", "الطرف المسؤول ضريبياً"),
        localized(
            "handle taxes, withholding, invoices, and tax documentation according to the contract",
            "traiter les impôts, retenues, factures et documents fiscaux conformément au contrat",
            "معالجة الضرائب والاستقطاعات والفواتير والمستندات الضريبية وفقاً للعقد",
        ),
    ),
    build_obligation_pattern(
        "warranties",
        TRIGGER_SIGNALS["warranties"],
        localized("warranting party", "partie garante", "الطرف المقدم للضمان"),
        localized(
            "comply with representations, warranties, disclaimers, and warranty remedies",
            "respecter les déclarations, garanties, exclusions et recours de garantie",
            "الامتثال للإقرارات والضمانات والاستثناءات ووسائل الانتصاف الخاصة بالضمان",
        ),
    ),
    build_obligation_pattern(
        "renewal",
        TRIGGER_SIGNALS["renewal"],
        neutral_party(),
        localized(
            "manage renewal, non-renewal, extension, and related notice requirements",
            "gérer le renouvellement, le non-renouvellement, la prolongation et les préavis associés",
            "إدارة التجديد وعدم التجديد والتمديد ومتطلبات الإشعار المرتبطة بها",
        ),
    ),
    build_obligation_pattern(
        "suspension",
        TRIGGER_SIGNALS["suspension"],
        localized("suspending or affected party", "partie suspendant ou affectée", "الطرف المعلق أو المتأثر"),
        localized(
            "follow suspension conditions, cure rights, service continuity protections, and reinstatement steps",
            "respecter les conditions de suspension, les droits de régularisation, les protections de continuité et les étapes de rétablissement",
            "اتباع شروط التعليق وحقوق المعالجة وضمانات الاستمرارية وخطوات الاستئناف",
        ),
    ),
    build_obligation_pattern(
        "business_continuity",
        TRIGGER_SIGNALS["business_continuity"],
        neutral_party(),
        localized(
            "maintain business continuity, disaster recovery, backup, and restoration measures",
            "maintenir les mesures de continuité d'activité, reprise après sinistre, sauvegarde et restauration",
            "الحفاظ على تدابير استمرارية الأعمال والتعافي من الكوارث والنسخ الاحتياطي والاستعادة",
        ),
    ),
    build_obligation_pattern(
        "publicity",
        TRIGGER_SIGNALS["publicity"],
        localized("publicity-using party", "partie utilisant la publicité", "الطرف المستخدم للدعاية"),
        localized(
            "obtain required approval before using names, logos, public announcements, or marketing references",
            "obtenir l'approbation requise avant d'utiliser les noms, logos, annonces publiques ou références marketing",
            "الحصول على الموافقة المطلوبة قبل استخدام الأسماء أو الشعارات أو الإعلانات العامة أو المراجع التسويقية",
        ),
    ),
    build_obligation_pattern(
        "severability",
        TRIGGER_SIGNALS["severability"],
        neutral_party(),
        localized(
            "preserve the remaining agreement and address invalid or unenforceable provisions as agreed",
            "préserver le reste du contrat et traiter les clauses invalides ou inapplicables comme convenu",
            "الحفاظ على باقي العقد ومعالجة الأحكام غير الصحيحة أو غير القابلة للتنفيذ كما هو متفق عليه",
        ),
    ),
    build_obligation_pattern(
        "survival",
        TRIGGER_SIGNALS["survival"],
        neutral_party(),
        localized(
            "continue performing obligations that survive termination or expiry",
            "continuer à exécuter les obligations qui survivent à la résiliation ou à l'expiration",
            "الاستمرار في تنفيذ الالتزامات التي تبقى بعد الإنهاء أو الانقضاء",
        ),
    ),
    build_obligation_pattern(
        "amendment",
        TRIGGER_SIGNALS["amendment"],
        neutral_party(),
        localized(
            "follow required written amendment, authorization, and change-control procedures",
            "respecter les procédures écrites de modification, d'autorisation et de contrôle des changements",
            "اتباع إجراءات التعديل الخطي والتفويض وضبط التغييرات المطلوبة",
        ),
    ),
    build_obligation_pattern(
        "waiver",
        TRIGGER_SIGNALS["waiver"],
        neutral_party(),
        localized(
            "preserve rights unless a waiver is written, specific, and authorized",
            "préserver les droits sauf renonciation écrite, spécifique et autorisée",
            "الحفاظ على الحقوق ما لم يكن التنازل خطياً ومحدداً ومفوضاً",
        ),
    ),
]


def extract_obligations_from_clause(
    clause: dict,
    language: str = "en",
) -> list[dict]:

    language = normalize_language(language)

    if not isinstance(clause, dict):
        return []

    text = normalize_text(" ".join([
        str(clause.get("clause_title", "")),
        str(clause.get("title", "")),
        str(clause.get("quoted_text", "")),
        str(clause.get("original_text", "")),
        str(clause.get("clause_text", "")),
        str(clause.get("text", "")),
        str(clause.get("explanation_simple", "")),
        str(clause.get("legal_insight", "")),
    ]))

    obligations = []

    for pattern in OBLIGATION_PATTERNS:
        if any(signal.lower() in text for signal in pattern["signals"]):
            obligation_type = pattern["type"]

            obligations.append({
                "type": obligation_type,
                "party": pattern["party"].get(
                    language,
                    pattern["party"]["en"],
                ),
                "obligation": pattern["obligation"].get(
                    language,
                    pattern["obligation"]["en"],
                ),
                "trigger": extract_generic_trigger(
                    text,
                    obligation_type,
                ),
                "deadline": extract_deadline(text),
                "consequence": extract_generic_consequence(
                    text,
                    obligation_type,
                ),
                "confidence": "high"
                if first_matching_signal(text, pattern["signals"])
                else "medium",
            })

    return obligations


def extract_contract_obligations(
    clauses: list[dict],
    language: str = "en",
) -> list[dict]:

    language = normalize_language(language)
    obligations = []

    for clause in clauses:
        if not isinstance(clause, dict):
            continue

        clause_obligations = extract_obligations_from_clause(
            clause,
            language,
        )

        for obligation in clause_obligations:
            obligation["source_clause"] = clause.get(
                "clause_title",
                clause.get("title", ""),
            )
            obligation["source_clause_id"] = clause.get(
                "id",
                clause.get("clause_id", ""),
            )
            obligation["source_clause_type"] = clause.get(
                "clause_type",
                clause.get("type", ""),
            )
            obligation["risk_level"] = clause.get(
                "risk_level",
                "",
            )
            obligations.append(obligation)

    return obligations


UNIVERSAL_OBLIGATION_TYPES = [
    pattern["type"]
    for pattern in OBLIGATION_PATTERNS
]

