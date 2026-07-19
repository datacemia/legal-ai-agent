from app.services.contract_agent.legal_ontology import (
    detect_legal_domains,
    detect_relation_triggers,
    detect_relation_consequences,
    get_trigger_consequences,
)


CONCEPT_TERMS = {
    "termination_event": [
        "termination", "terminate", "terminated", "expiration", "non-renewal",
        "résiliation", "résilier", "expiration", "non-renouvellement",
        "إنهاء", "فسخ", "انتهاء", "عدم التجديد",
    ],
    "notice_requirement": [
        "notice", "written notice", "notice period", "notification",
        "préavis", "avis écrit", "notification",
        "إشعار", "إخطار", "إشعار كتابي",
    ],
    "breach_default": [
        "breach", "default", "material breach", "failure to perform",
        "manquement", "défaut", "violation substantielle",
        "إخلال", "تقصير", "إخلال جوهري",
    ],
    "continuing_obligations": [
        "post-termination", "post termination", "after termination",
        "survive", "survival", "continuing obligations",
        "après résiliation", "après la résiliation", "survie",
        "obligations continues",
        "بعد الإنهاء", "بعد انتهاء", "استمرار الالتزامات",
    ],
    "payment_obligation": [
        "salary", "bonus", "compensation", "benefits", "payment",
        "reimbursement", "fees", "invoice", "purchase price", "rent",
        "royalty", "commission", "service fee", "subscription fee",
        "installment",
        "salaire", "prime", "rémunération", "avantages", "paiement",
        "remboursement", "honoraires", "frais", "facture", "prix",
        "loyer", "redevance", "commission",
        "راتب", "مكافأة", "تعويض", "مزايا", "دفع", "سداد",
        "رسوم", "فاتورة", "ثمن", "إيجار", "إتاوة", "عمولة", "اشتراك",
    ],
    "performance_condition": [
        "performance", "achievement",
        "service level", "milestone", "kpi", "deliverable",
        "acceptance criteria", "uptime", "quality level",
        "performance", "réalisation",
        "niveau de service", "jalon", "livrable", "critères d'acceptation",
        "disponibilité", "niveau de qualité",
        "أداء", "إنجاز", "مستوى الخدمة",
        "مرحلة", "مخرج", "معايير القبول", "التوافر", "مستوى الجودة",
    ],
    "confidentiality": [
        "confidential", "confidentiality", "trade secret",
        "proprietary information", "non-disclosure",
        "confidentialité", "secret commercial", "non-divulgation",
        "معلومات سرية", "سرية", "سر تجاري", "عدم الإفصاح",
    ],
    "data_protection": [
        "personal data", "data protection", "data processing", "processor",
        "controller", "subprocessor", "privacy", "security incident",
        "data breach", "cybersecurity",
        "données personnelles", "protection des données", "traitement des données",
        "sous-traitant", "responsable du traitement", "vie privée",
        "incident de sécurité", "violation de données", "cybersécurité",
        "بيانات شخصية", "حماية البيانات", "معالجة البيانات", "معالج البيانات",
        "المتحكم في البيانات", "الخصوصية", "حادث أمني", "اختراق البيانات",
        "الأمن السيبراني",
    ],
    "ip_ownership": [
        "intellectual property", "ownership", "license", "assignment",
        "deliverables", "work product", "copyright", "trademark",
        "patent", "moral rights",
        "propriété intellectuelle", "propriété", "licence", "cession",
        "livrables", "droit d'auteur", "marque", "brevet", "droits moraux",
        "ملكية فكرية", "ملكية", "ترخيص", "تنازل", "مخرجات العمل",
        "حقوق النشر", "علامة تجارية", "براءة", "حقوق معنوية",
    ],
    "liability_protection": [
        "liability", "indemnity", "indemnification", "insurance",
        "warranty", "damages", "liability cap", "limitation of liability",
        "responsabilité", "indemnisation", "assurance", "garantie",
        "dommages", "plafond de responsabilité", "limitation de responsabilité",
        "مسؤولية", "تعويض", "تأمين", "ضمان", "أضرار", "حد المسؤولية",
    ],
    "dispute_resolution": [
        "dispute", "claim", "arbitration", "mediation", "governing law",
        "jurisdiction", "venue", "court",
        "litige", "réclamation", "arbitrage", "médiation",
        "droit applicable", "juridiction", "tribunal",
        "نزاع", "مطالبة", "تحكيم", "وساطة", "القانون الواجب التطبيق",
        "اختصاص", "محكمة",
    ],
    "governance_control": [
        "audit", "compliance", "assignment",
        "change of control", "subcontracting", "sanctions", "anti-bribery",
        "audit", "conformité", "cession",
        "changement de contrôle", "sous-traitance", "sanctions",
        "تدقيق", "امتثال", "تنازل", "تغيير السيطرة",
        "تعاقد من الباطن", "عقوبات",
    ],
    "restrictive_covenant": [
        "non-compete", "non compete", "non-solicitation", "non solicitation",
        "non-circumvention", "non-dealing", "exclusivity", "exclusive dealing",
        "non-concurrence", "non-sollicitation", "non-contournement",
        "exclusivité",
        "عدم المنافسة", "عدم الاستقطاب", "عدم الالتفاف", "الحصرية",
    ],
}


LEGAL_ROLES = {
    "termination_event": "legal_consequence",
    "notice_requirement": "procedural_requirement",
    "breach_default": "breach_trigger",
    "continuing_obligations": "temporal_scope",
    "payment_obligation": "financial_consequence",
    "performance_condition": "condition",
    "confidentiality": "continuing_obligation",
    "data_protection": "regulated_obligation",
    "ip_ownership": "rights_allocation",
    "liability_protection": "risk_allocation",
    "dispute_resolution": "forum_resolution",
    "governance_control": "approval_control",
    "restrictive_covenant": "market_restriction",
}


ALLOWED_RELATIONS = [
    ("procedural_requirement", "legal_consequence"),
    ("breach_trigger", "legal_consequence"),
    ("condition", "financial_consequence"),
    ("condition", "legal_consequence"),
    ("continuing_obligation", "temporal_scope"),
    ("rights_allocation", "continuing_obligation"),
    ("continuing_obligation", "risk_allocation"),
    ("regulated_obligation", "risk_allocation"),
    ("regulated_obligation", "legal_consequence"),
    ("market_restriction", "legal_consequence"),
    ("approval_control", "legal_consequence"),
    ("forum_resolution", "legal_consequence"),
]


DISPLAY_GROUPS = {
    "performance_condition": "Performance & Operations",
    "payment_obligation": "Payment & Commercial Terms",
    "termination_event": "Contract Lifecycle",
    "notice_requirement": "Contract Lifecycle",
    "continuing_obligations": "Survival & Post-Termination",
    "ip_ownership": "Intellectual Property",
    "confidentiality": "Data & Confidentiality",
    "data_protection": "Data & Confidentiality",
    "liability_protection": "Liability & Risk",
    "dispute_resolution": "Dispute Resolution",
    "governance_control": "Governance & Compliance",
    "restrictive_covenant": "Restrictive Covenants",
    "breach_default": "Default & Remedies",
    "other": "General",
}


DEPENDENCY_TRIGGERS = {
    "termination": [
        # EN
        "payment", "fees", "invoice", "services", "support", "license",
        "intellectual property", "confidentiality", "return", "destruction",
        "data", "transition", "assets", "survival",
        # FR
        "paiement", "honoraires", "facture", "services", "support", "licence",
        "propriété intellectuelle", "confidentialité", "restitution", "destruction",
        "données", "transition", "actifs", "survie",
        # AR
        "الدفع", "الرسوم", "الفاتورة", "الخدمات", "الدعم", "الترخيص",
        "الملكية الفكرية", "السرية", "الإعادة", "الإتلاف",
        "البيانات", "الانتقال", "الأصول", "الاستمرارية",
    ],
    "payment": [
        # EN
        "termination", "performance", "delivery", "invoice", "acceptance",
        "milestone", "tax", "interest", "currency", "suspension",
        # FR
        "résiliation", "performance", "livraison", "facture", "acceptation",
        "jalon", "taxe", "intérêt", "devise", "suspension",
        # AR
        "الإنهاء", "الأداء", "التسليم", "الفاتورة", "القبول",
        "المرحلة", "الضريبة", "الفائدة", "العملة", "التعليق",
    ],
    "liability": [
        # EN
        "damages", "claims", "breach", "indemnity", "insurance",
        "intellectual property", "data protection", "security incident",
        "force majeure", "confidentiality",
        # FR
        "dommages", "réclamation", "manquement", "indemnisation", "assurance",
        "propriété intellectuelle", "protection des données", "incident de sécurité",
        "force majeure", "confidentialité",
        # AR
        "الأضرار", "المطالبات", "الإخلال", "التعويض", "التأمين",
        "الملكية الفكرية", "حماية البيانات", "الحادث الأمني",
        "القوة القاهرة", "السرية",
    ],
    "confidentiality": [
        # EN
        "breach", "injunctive relief", "data", "security", "return",
        "destruction", "liability",
        # FR
        "manquement", "mesure injonctive", "données", "sécurité", "restitution",
        "destruction", "responsabilité",
        # AR
        "الإخلال", "الأمر القضائي", "البيانات", "الأمن", "الإعادة",
        "الإتلاف", "المسؤولية",
    ],
     "data_protection": [
        "confidentiality", "liability", "indemnity", "audit",
        "subprocessor", "security incident", "notification", "deletion",
        "confidentialité", "responsabilité", "indemnisation", "audit",
        "sous-traitant ultérieur", "incident de sécurité", "notification", "suppression",
        "السرية", "المسؤولية", "التعويض", "التدقيق",
        "المعالج الفرعي", "الحادث الأمني", "الإخطار", "الحذف",
    ],
    "privacy": [
        "confidentiality", "liability", "indemnity", "audit",
        "subprocessor", "security incident", "notification", "deletion",
        "confidentialité", "responsabilité", "indemnisation", "audit",
        "sous-traitant ultérieur", "incident de sécurité", "notification", "suppression",
        "السرية", "المسؤولية", "التعويض", "التدقيق",
        "المعالج الفرعي", "الحادث الأمني", "الإخطار", "الحذف",
    ],
    "data_processing": [
        "confidentiality", "liability", "indemnity", "audit",
        "subprocessor", "security incident", "notification", "deletion",
        "confidentialité", "responsabilité", "indemnisation", "audit",
        "sous-traitant ultérieur", "incident de sécurité", "notification", "suppression",
        "السرية", "المسؤولية", "التعويض", "التدقيق",
        "المعالج الفرعي", "الحادث الأمني", "الإخطار", "الحذف",
    ],
    "security": [
        "confidentiality", "liability", "indemnity", "audit",
        "subprocessor", "security incident", "notification", "deletion",
        "confidentialité", "responsabilité", "indemnisation", "audit",
        "sous-traitant ultérieur", "incident de sécurité", "notification", "suppression",
        "السرية", "المسؤولية", "التعويض", "التدقيق",
        "المعالج الفرعي", "الحادث الأمني", "الإخطار", "الحذف",
    ],
    "cybersecurity": [
        "confidentiality", "liability", "indemnity", "audit",
        "subprocessor", "security incident", "notification", "deletion",
        "confidentialité", "responsabilité", "indemnisation", "audit",
        "sous-traitant ultérieur", "incident de sécurité", "notification", "suppression",
        "السرية", "المسؤولية", "التعويض", "التدقيق",
        "المعالج الفرعي", "الحادث الأمني", "الإخطار", "الحذف",
    ],
    "intellectual_property": [
        "confidentiality", "license", "assignment", "termination",
        "deliverables", "payment",
        "confidentialité", "licence", "cession", "résiliation",
        "livrables", "paiement",
        "السرية", "الترخيص", "التنازل", "الإنهاء",
        "المخرجات", "الدفع",
    ],
    "services": [
        "payment", "acceptance", "liability", "service level",
        "termination", "support", "maintenance",
        "paiement", "acceptation", "responsabilité", "niveau de service",
        "résiliation", "support", "maintenance",
        "الدفع", "القبول", "المسؤولية", "مستوى الخدمة",
        "الإنهاء", "الدعم", "الصيانة",
    ],
    "service_level": [
        "payment", "acceptance", "liability", "service level",
        "termination", "support", "maintenance",
        "paiement", "acceptation", "responsabilité", "niveau de service",
        "résiliation", "support", "maintenance",
        "الدفع", "القبول", "المسؤولية", "مستوى الخدمة",
        "الإنهاء", "الدعم", "الصيانة",
    ],
    "support": [
        "payment", "acceptance", "liability", "service level",
        "termination", "support", "maintenance",
        "paiement", "acceptation", "responsabilité", "niveau de service",
        "résiliation", "support", "maintenance",
        "الدفع", "القبول", "المسؤولية", "مستوى الخدمة",
        "الإنهاء", "الدعم", "الصيانة",
    ],
    "maintenance": [
        "payment", "acceptance", "liability", "service level",
        "termination", "support", "maintenance",
        "paiement", "acceptation", "responsabilité", "niveau de service",
        "résiliation", "support", "maintenance",
        "الدفع", "القبول", "المسؤولية", "مستوى الخدمة",
        "الإنهاء", "الدعم", "الصيانة",
    ],
    "non_compete": [
        "termination", "confidentiality", "liability", "injunction",
        "duration", "territory",
        "résiliation", "confidentialité", "responsabilité", "injonction",
        "durée", "territoire",
        "الإنهاء", "السرية", "المسؤولية", "الأمر الزجري",
        "المدة", "النطاق الجغرافي",
    ],
    "non_solicitation": [
        "termination", "confidentiality", "liability", "injunction",
        "duration", "territory",
        "résiliation", "confidentialité", "responsabilité", "injonction",
        "durée", "territoire",
        "الإنهاء", "السرية", "المسؤولية", "الأمر الزجري",
        "المدة", "النطاق الجغرافي",
    ],
    "exclusivity": [
        "termination", "confidentiality", "liability", "injunction",
        "duration", "territory",
        "résiliation", "confidentialité", "responsabilité", "injonction",
        "durée", "territoire",
        "الإنهاء", "السرية", "المسؤولية", "الأمر الزجري",
        "المدة", "النطاق الجغرافي",
    ],
    "conflict_of_interest": [
        "termination", "confidentiality", "liability", "injunction",
        "duration", "territory",
        "résiliation", "confidentialité", "responsabilité", "injonction",
        "durée", "territoire",
        "الإنهاء", "السرية", "المسؤولية", "الأمر الزجري",
        "المدة", "النطاق الجغرافي",
    ],
    "governance": [
        "assignment", "change of control", "termination", "audit",
        "sanctions", "subcontracting", "consent",
        "cession", "changement de contrôle", "résiliation", "audit",
        "sanctions", "sous-traitance", "consentement",
        "التنازل", "تغيير السيطرة", "الإنهاء", "التدقيق",
        "العقوبات", "التعاقد من الباطن", "الموافقة",
    ],
    "compliance": [
        "assignment", "change of control", "termination", "audit",
        "sanctions", "subcontracting", "consent",
        "cession", "changement de contrôle", "résiliation", "audit",
        "sanctions", "sous-traitance", "consentement",
        "التنازل", "تغيير السيطرة", "الإنهاء", "التدقيق",
        "العقوبات", "التعاقد من الباطن", "الموافقة",
    ],
    "assignment": [
        "assignment", "change of control", "termination", "audit",
        "sanctions", "subcontracting", "consent",
        "cession", "changement de contrôle", "résiliation", "audit",
        "sanctions", "sous-traitance", "consentement",
        "التنازل", "تغيير السيطرة", "الإنهاء", "التدقيق",
        "العقوبات", "التعاقد من الباطن", "الموافقة",
    ],
    "change_of_control": [
        "assignment", "change of control", "termination", "audit",
        "sanctions", "subcontracting", "consent",
        "cession", "changement de contrôle", "résiliation", "audit",
        "sanctions", "sous-traitance", "consentement",
        "التنازل", "تغيير السيطرة", "الإنهاء", "التدقيق",
        "العقوبات", "التعاقد من الباطن", "الموافقة",
    ],
    "subcontracting": [
        "assignment", "change of control", "termination", "audit",
        "sanctions", "subcontracting", "consent",
        "cession", "changement de contrôle", "résiliation", "audit",
        "sanctions", "sous-traitance", "consentement",
        "التنازل", "تغيير السيطرة", "الإنهاء", "التدقيق",
        "العقوبات", "التعاقد من الباطن", "الموافقة",
    ],
    "sanctions": [
        "assignment", "change of control", "termination", "audit",
        "sanctions", "subcontracting", "consent",
        "cession", "changement de contrôle", "résiliation", "audit",
        "sanctions", "sous-traitance", "consentement",
        "التنازل", "تغيير السيطرة", "الإنهاء", "التدقيق",
        "العقوبات", "التعاقد من الباطن", "الموافقة",
    ],
    "anti_bribery": [
        "assignment", "change of control", "termination", "audit",
        "sanctions", "subcontracting", "consent",
        "cession", "changement de contrôle", "résiliation", "audit",
        "sanctions", "sous-traitance", "consentement",
        "التنازل", "تغيير السيطرة", "الإنهاء", "التدقيق",
        "العقوبات", "التعاقد من الباطن", "الموافقة",
    ],
}


# ---------------------------------------------------------------------
# Translation layer. Every reason string previously hard-coded in English
# is now looked up here so the graph is generated in the requested output
# language (en / fr / ar), matching the rest of the pipeline.
# ---------------------------------------------------------------------

SUPPORTED_LANGUAGES = {"en", "fr", "ar"}


def _lang(language: str) -> str:
    return language if language in SUPPORTED_LANGUAGES else "en"


# Translations for the words used inside DEPENDENCY_TRIGGERS (both the
# source_type keys and the trigger terms), used to build the dynamic
# "semantic_dependency" reason sentence in the requested language.
TERM_TRANSLATIONS = {
    "termination": {"en": "Termination", "fr": "La résiliation", "ar": "الإنهاء"},
    "payment": {"en": "payment", "fr": "de paiement", "ar": "الدفع"},
    "liability": {"en": "Liability", "fr": "La responsabilité", "ar": "المسؤولية"},
    "confidentiality": {"en": "Confidentiality", "fr": "La confidentialité", "ar": "السرية"},
    "data_privacy_security": {"en": "Data privacy and security", "fr": "La confidentialité et la sécurité des données", "ar": "خصوصية البيانات وأمنها"},
    "intellectual_property": {"en": "Intellectual property", "fr": "La propriété intellectuelle", "ar": "الملكية الفكرية"},
    "services_operations": {"en": "Services and operations", "fr": "Les services et opérations", "ar": "الخدمات والعمليات"},
    "restrictive_covenants": {"en": "Restrictive covenants", "fr": "Les engagements restrictifs", "ar": "التعهدات التقييدية"},
    "governance_compliance": {"en": "Governance and compliance", "fr": "La gouvernance et la conformité", "ar": "الحوكمة والامتثال"},
    "fees": {"en": "fees", "fr": "d'honoraires", "ar": "الرسوم"},
    "invoice": {"en": "invoicing", "fr": "de facturation", "ar": "الفوترة"},
    # NOTE: a duplicate "services" key used to exist here (silently shadowed
    # by the later "services" entry below, since Python dict literals keep
    # only the last duplicate key -- see _TARGET_STYLE_OVERRIDES for how
    # this is now handled explicitly). Removed to avoid two contradictory
    # definitions of the same key sitting in the file.
    "support": {"en": "support", "fr": "de support", "ar": "الدعم"},
    "license": {"en": "licensing", "fr": "de licence", "ar": "الترخيص"},
    "intellectual property": {"en": "intellectual property", "fr": "de propriété intellectuelle", "ar": "الملكية الفكرية"},
    "return": {"en": "return", "fr": "de restitution", "ar": "الإعادة"},
    "destruction": {"en": "destruction", "fr": "de destruction", "ar": "الإتلاف"},
    "data": {"en": "data", "fr": "de données", "ar": "البيانات"},
    "transition": {"en": "transition", "fr": "de transition", "ar": "الانتقال"},
    "assets": {"en": "asset", "fr": "d'actifs", "ar": "الأصول"},
    "survival": {"en": "survival", "fr": "de survie", "ar": "الاستمرارية"},
    "performance": {"en": "performance", "fr": "de performance", "ar": "الأداء"},
    "delivery": {"en": "delivery", "fr": "de livraison", "ar": "التسليم"},
    "acceptance": {"en": "acceptance", "fr": "d'acceptation", "ar": "القبول"},
    "milestone": {"en": "milestone", "fr": "de jalon", "ar": "المراحل"},
    "tax": {"en": "tax", "fr": "fiscales", "ar": "الضريبة"},
    "interest": {"en": "interest", "fr": "d'intérêts", "ar": "الفائدة"},
    "currency": {"en": "currency", "fr": "de devise", "ar": "العملة"},
    "suspension": {"en": "suspension", "fr": "de suspension", "ar": "التعليق"},
    "damages": {"en": "damages", "fr": "de dommages", "ar": "الأضرار"},
    "claims": {"en": "claims", "fr": "de réclamation", "ar": "المطالبات"},
    "breach": {"en": "breach", "fr": "de manquement", "ar": "الإخلال"},
    "indemnity": {"en": "indemnity", "fr": "d'indemnisation", "ar": "التعويض"},
    "insurance": {"en": "insurance", "fr": "d'assurance", "ar": "التأمين"},
    "security incident": {"en": "security incident", "fr": "d'incident de sécurité", "ar": "الحادث الأمني"},
    "force majeure": {"en": "force majeure", "fr": "de force majeure", "ar": "القوة القاهرة"},
    "injunctive relief": {"en": "injunctive relief", "fr": "de mesure injonctive", "ar": "الأمر القضائي"},
    "security": {"en": "security", "fr": "de sécurité", "ar": "الأمن"},
    "audit": {"en": "audit", "fr": "d'audit", "ar": "التدقيق"},
    "subprocessor": {"en": "subprocessor", "fr": "de sous-traitant ultérieur", "ar": "المعالج الفرعي"},
    "notification": {"en": "notification", "fr": "de notification", "ar": "الإخطار"},
    "deletion": {"en": "deletion", "fr": "de suppression", "ar": "الحذف"},
    "deliverables": {"en": "deliverables", "fr": "de livrables", "ar": "المخرجات"},
    "maintenance": {"en": "maintenance", "fr": "de maintenance", "ar": "الصيانة"},
    "service level": {"en": "service level", "fr": "de niveau de service", "ar": "مستوى الخدمة"},
    "injunction": {"en": "injunction", "fr": "d'injonction", "ar": "الأمر الزجري"},
    "duration": {"en": "duration", "fr": "de durée", "ar": "المدة"},
    "territory": {"en": "territory", "fr": "de territoire", "ar": "النطاق الجغرافي"},
    "change of control": {"en": "change of control", "fr": "de changement de contrôle", "ar": "تغيير السيطرة"},
    "sanctions": {"en": "sanctions", "fr": "de sanctions", "ar": "العقوبات"},
    "subcontracting": {"en": "subcontracting", "fr": "de sous-traitance", "ar": "التعاقد من الباطن"},
    "consent": {"en": "consent", "fr": "de consentement", "ar": "الموافقة"},
    "non_compete": {"en": "Non-compete", "fr": "La clause de non-concurrence", "ar": "عدم المنافسة"},
    "non_solicitation": {"en": "Non-solicitation", "fr": "La clause de non-sollicitation", "ar": "عدم الاستقطاب"},
    "exclusivity": {"en": "Exclusivity", "fr": "L'exclusivité", "ar": "الحصرية"},
    "conflict_of_interest": {"en": "Conflict of interest", "fr": "Le conflit d'intérêts", "ar": "تضارب المصالح"},
    "governance": {"en": "Governance", "fr": "La gouvernance", "ar": "الحوكمة"},
    "compliance": {"en": "Compliance", "fr": "La conformité", "ar": "الامتثال"},
    "change_of_control": {"en": "Change of control", "fr": "Le changement de contrôle", "ar": "تغيير السيطرة"},
    "anti_bribery": {"en": "Anti-bribery", "fr": "La lutte anticorruption", "ar": "مكافحة الرشوة"},
    "data_protection": {"en": "Data protection", "fr": "La protection des données", "ar": "حماية البيانات"},
    "privacy": {"en": "Privacy", "fr": "La confidentialité des données", "ar": "الخصوصية"},
    "data_processing": {"en": "Data processing", "fr": "Le traitement des données", "ar": "معالجة البيانات"},
    "cybersecurity": {"en": "Cybersecurity", "fr": "La cybersécurité", "ar": "الأمن السيبراني"},
    "services": {"en": "Services", "fr": "Les services", "ar": "الخدمات"},
    "service_level": {"en": "Service level", "fr": "Le niveau de service", "ar": "مستوى الخدمة"},
}


def _translate_term(term: str, language: str) -> str:
    entry = TERM_TRANSLATIONS.get(term)
    if entry:
        return entry.get(language, entry.get("en", term))
    return term.replace("_", " ")


# ---------------------------------------------------------------------
# Source/target grammar fix for _semantic_dependency_reason().
#
# TERM_TRANSLATIONS mixes two incompatible French phrasing styles under
# a single key: some entries are capitalized standalone subjects meant
# for the start of a sentence ("La résiliation", "La responsabilité"),
# while others are lowercase "de/d'"-prefixed fragments meant to slot
# into "les obligations {X}" ("de paiement", "d'audit"). Using a
# source-style entry as a target (or vice versa) produces broken
# grammar such as "de sécurité peut affecter..." or "les obligations La
# résiliation.". Four issues compounded this in practice:
#   1. A handful of concepts used as DEPENDENCY_TRIGGERS source_type
#      keys (payment, security, support, maintenance, sanctions,
#      subcontracting) only ever had the target-style form defined, so
#      using them as a SOURCE produced a lowercase "de X peut..." sentence.
#   2. "assignment" had no French/Arabic translation entry at all and
#      fell straight through to the raw English word.
#   3. DEPENDENCY_TRIGGERS interleaves literal EN/FR/AR matching words as
#      three equal-length blocks. When a clause's own text matched the
#      FR or AR literal directly (e.g. "résiliation" appearing in a
#      French clause), that raw matched string -- not the canonical EN
#      concept key -- was passed straight into _translate_term(), which
#      only recognizes EN keys, so it fell back to returning the raw,
#      unprefixed, uncapitalized word untranslated ("les obligations
#      résiliation." instead of "les obligations de résiliation.").
#   4. A few source concepts are grammatically plural in French ("Les
#      services", "Les sanctions"), which needs "peuvent" rather than
#      the default singular "peut" -- otherwise "Les services peut
#      affecter..." disagrees in number.
# ---------------------------------------------------------------------

_SOURCE_STYLE_OVERRIDES = {
    "assignment": {"en": "Assignment", "fr": "La cession", "ar": "التنازل"},
    "payment": {"en": "Payment", "fr": "Le paiement", "ar": "الدفع"},
    "security": {"en": "Security", "fr": "La sécurité", "ar": "الأمن"},
    "support": {"en": "Support", "fr": "Le support", "ar": "الدعم"},
    "maintenance": {"en": "Maintenance", "fr": "La maintenance", "ar": "الصيانة"},
    "sanctions": {"en": "Sanctions", "fr": "Les sanctions", "ar": "العقوبات"},
    "subcontracting": {"en": "Subcontracting", "fr": "La sous-traitance", "ar": "التعاقد من الباطن"},
}

_TARGET_STYLE_OVERRIDES = {
    "termination": {"en": "termination", "fr": "de résiliation", "ar": "الإنهاء"},
    "liability": {"en": "liability", "fr": "de responsabilité", "ar": "المسؤولية"},
    "confidentiality": {"en": "confidentiality", "fr": "de confidentialité", "ar": "السرية"},
    # "services" is defined TWICE in TERM_TRANSLATIONS (once lowercase/
    # target-style at its first definition, once capitalized/source-style
    # at a later definition). Python dict literals silently keep only the
    # LAST duplicate key, so TERM_TRANSLATIONS["services"] actually
    # resolves to the capitalized source-style form -- which leaked into
    # target position as "Termination may affect Services obligations."
    # (capital S). This override guarantees the correct lowercase form
    # for target usage regardless of which duplicate definition wins.
    "services": {"en": "services", "fr": "de services", "ar": "الخدمات"},
}

_PLURAL_SOURCE_CONCEPTS = {
    "services",
    "services_operations",
    "restrictive_covenants",
    "sanctions",
}


def _translate_source_term(term: str, language: str) -> str:
    override = _SOURCE_STYLE_OVERRIDES.get(term)
    if override:
        return override.get(language, override.get("en", term))
    return _translate_term(term, language)


def _translate_target_term(term: str, language: str) -> str:
    override = _TARGET_STYLE_OVERRIDES.get(term)
    if override:
        return override.get(language, override.get("en", term))
    return _translate_term(term, language)


def _build_trigger_concept_map() -> dict:
    """
    DEPENDENCY_TRIGGERS lists interleave EN/FR/AR literal matching words
    as three equal-length blocks, in the same concept order, per
    source_type. This builds a lookup from ANY literal trigger word --
    in any of the three languages -- back to its canonical English
    concept key, so a French or Arabic literal match can still be
    translated correctly instead of falling through untranslated.
    """
    concept_map = {}

    for triggers in DEPENDENCY_TRIGGERS.values():
        if len(triggers) % 3 != 0:
            continue

        block_size = len(triggers) // 3

        if block_size == 0:
            continue

        en_block = triggers[:block_size]
        fr_block = triggers[block_size:2 * block_size]
        ar_block = triggers[2 * block_size:3 * block_size]

        for en_word, fr_word, ar_word in zip(en_block, fr_block, ar_block):
            canonical = en_word.strip().lower()
            concept_map.setdefault(en_word.strip().lower(), canonical)
            concept_map.setdefault(fr_word.strip().lower(), canonical)
            concept_map.setdefault(ar_word.strip(), canonical)

    return concept_map


_TRIGGER_CONCEPT_MAP = _build_trigger_concept_map()


def _resolve_trigger_concept(trigger: str) -> str:
    normalized = str(trigger or "").strip().lower()
    return _TRIGGER_CONCEPT_MAP.get(normalized, trigger)


def _semantic_dependency_reason(source_type: str, trigger: str, language: str) -> str:
    language = _lang(language)
    source_label = _translate_source_term(source_type, language)

    resolved_trigger = _resolve_trigger_concept(trigger)
    target_label = _translate_target_term(resolved_trigger, language)

    if language == "fr":
        connector = "peuvent" if source_type in _PLURAL_SOURCE_CONCEPTS else "peut"
        return f"{source_label} {connector} affecter les obligations {target_label}."
    if language == "ar":
        return f"قد يؤثر {source_label} على الالتزامات المتعلقة بـ {target_label}."
    return f"{source_label} may affect {target_label} obligations."


# Explicit relation reasons (add_relation_edges / detect_relation).
RELATION_REASONS = {
    "notice_dependency": {
        "en": "Termination or contractual consequences may depend on notice requirements.",
        "fr": "La résiliation ou d'autres conséquences contractuelles peuvent dépendre des exigences de préavis.",
        "ar": "قد تعتمد نتائج الإنهاء أو الالتزامات التعاقدية الأخرى على متطلبات الإشعار.",
    },
    "breach_termination_dependency": {
        "en": "Breach or default may trigger termination rights or consequences.",
        "fr": "Un manquement ou un défaut peut déclencher des droits ou des conséquences de résiliation.",
        "ar": "قد يؤدي الإخلال أو التقصير إلى نشوء حق الإنهاء أو ترتيب نتائج عليه.",
    },
    "performance_payment_dependency": {
        "en": "Payment may depend on performance, delivery, milestones, or acceptance conditions.",
        "fr": "Le paiement peut dépendre de la performance, de la livraison, de jalons ou de conditions d'acceptation.",
        "ar": "قد يعتمد الدفع على الأداء أو التسليم أو مراحل الإنجاز أو شروط القبول.",
    },
    "survival_obligation": {
        "en": "Confidentiality or related obligations may continue after the contract ends.",
        "fr": "Les obligations de confidentialité ou obligations connexes peuvent se poursuivre après la fin du contrat.",
        "ar": "قد تستمر التزامات السرية أو الالتزامات ذات الصلة بعد انتهاء العقد.",
    },
    "information_rights_dependency": {
        "en": "IP or ownership rights may depend on confidential information handling.",
        "fr": "Les droits de propriété intellectuelle ou de propriété peuvent dépendre du traitement des informations confidentielles.",
        "ar": "قد تعتمد حقوق الملكية الفكرية أو حقوق الملكية على كيفية التعامل مع المعلومات السرية.",
    },
    "liability_exception": {
        "en": "Confidentiality breaches may affect liability or indemnity exposure.",
        "fr": "Les violations de confidentialité peuvent affecter l'exposition à la responsabilité ou à l'indemnisation.",
        "ar": "قد تؤثر خروقات السرية على مدى التعرض للمسؤولية أو التعويض.",
    },
    "data_liability_dependency": {
        "en": "Data protection failures may affect liability or indemnity exposure.",
        "fr": "Les manquements en matière de protection des données peuvent affecter l'exposition à la responsabilité ou à l'indemnisation.",
        "ar": "قد تؤثر إخفاقات حماية البيانات على مدى التعرض للمسؤولية أو التعويض.",
    },
    "post_contract_restriction_dependency": {
        "en": "Restrictive covenants may apply during or after the contract term.",
        "fr": "Les engagements restrictifs peuvent s'appliquer pendant ou après la durée du contrat.",
        "ar": "قد تُطبَّق التعهدات التقييدية أثناء مدة العقد أو بعدها.",
    },
    "trigger_consequence": {
        "en": "A trigger in one clause may produce consequences addressed in another clause.",
        "fr": "Un événement déclencheur dans une clause peut produire des conséquences traitées dans une autre clause.",
        "ar": "قد ينتج عن عامل مُحفِّز في أحد البنود آثار تُعالَج في بند آخر.",
    },
}


def _relation_reason(key: str, language: str) -> str:
    entry = RELATION_REASONS.get(key, {})
    return entry.get(_lang(language), entry.get("en", ""))


CROSS_DOMAIN_RELATIONS = [
    {
        "source_domain": "confidentiality",
        "target_domain": "data_privacy_security",
        "type": "confidentiality_data_dependency",
        "reason": {
            "en": "Confidentiality obligations may interact with data protection duties.",
            "fr": "Les obligations de confidentialité peuvent interagir avec les obligations de protection des données.",
            "ar": "قد تتفاعل التزامات السرية مع واجبات حماية البيانات.",
        },
        "confidence": 0.75,
    },
    {
        "source_domain": "data_privacy_security",
        "target_domain": "liability",
        "type": "data_liability_dependency",
        "reason": {
            "en": "Data protection failures may affect liability or indemnity exposure.",
            "fr": "Les manquements en matière de protection des données peuvent affecter l'exposition à la responsabilité ou à l'indemnisation.",
            "ar": "قد تؤثر إخفاقات حماية البيانات على مدى التعرض للمسؤولية أو التعويض.",
        },
        "confidence": 0.8,
    },
    {
        "source_domain": "termination",
        "target_domain": "payment",
        "type": "termination_payment_dependency",
        "reason": {
            "en": "Termination may affect outstanding fees, refunds, or payment obligations.",
            "fr": "La résiliation peut affecter les honoraires impayés, les remboursements ou les obligations de paiement.",
            "ar": "قد يؤثر الإنهاء على الرسوم المستحقة أو المبالغ المستردة أو التزامات الدفع.",
        },
        "confidence": 0.75,
    },
    {
        "source_domain": "termination",
        "target_domain": "intellectual_property",
        "type": "termination_ip_dependency",
        "reason": {
            "en": "Termination may affect license rights, deliverables, or IP use after contract end.",
            "fr": "La résiliation peut affecter les droits de licence, les livrables ou l'usage de la propriété intellectuelle après la fin du contrat.",
            "ar": "قد يؤثر الإنهاء على حقوق الترخيص أو المخرجات أو استخدام الملكية الفكرية بعد انتهاء العقد.",
        },
        "confidence": 0.75,
    },
    {
        "source_domain": "intellectual_property",
        "target_domain": "confidentiality",
        "type": "ip_confidentiality_dependency",
        "reason": {
            "en": "IP rights may depend on confidential information handling.",
            "fr": "Les droits de propriété intellectuelle peuvent dépendre du traitement des informations confidentielles.",
            "ar": "قد تعتمد حقوق الملكية الفكرية على كيفية التعامل مع المعلومات السرية.",
        },
        "confidence": 0.75,
    },
    {
        "source_domain": "services_operations",
        "target_domain": "payment",
        "type": "services_payment_dependency",
        "reason": {
            "en": "Service delivery, milestones, or acceptance may affect payment obligations.",
            "fr": "La livraison des services, les jalons ou l'acceptation peuvent affecter les obligations de paiement.",
            "ar": "قد يؤثر تقديم الخدمة أو مراحل الإنجاز أو القبول على التزامات الدفع.",
        },
        "confidence": 0.75,
    },
    {
        "source_domain": "services_operations",
        "target_domain": "liability",
        "type": "services_liability_dependency",
        "reason": {
            "en": "Service failures may interact with liability caps, remedies, or indemnities.",
            "fr": "Les défaillances de service peuvent interagir avec les plafonds de responsabilité, les recours ou les indemnisations.",
            "ar": "قد تتفاعل إخفاقات الخدمة مع حدود المسؤولية أو سبل الانتصاف أو التعويضات.",
        },
        "confidence": 0.75,
    },
    {
        "source_domain": "governance_compliance",
        "target_domain": "termination",
        "type": "approval_termination_dependency",
        "reason": {
            "en": "Approval, assignment, or compliance controls may affect termination rights.",
            "fr": "Les contrôles d'approbation, de cession ou de conformité peuvent affecter les droits de résiliation.",
            "ar": "قد تؤثر ضوابط الموافقة أو التنازل أو الامتثال على حقوق الإنهاء.",
        },
        "confidence": 0.7,
    },
]


def build_legal_relation_graph(
    clauses: list[dict],
    language: str = "en",
) -> dict:
    language = _lang(language)

    nodes = []
    edges = []
    groups = {}

    indexed = []

    for index, clause in enumerate(clauses):
        title = str(
            clause.get("title")
            or clause.get("clause_title")
            or f"Clause {index + 1}"
        )

        text = " ".join([
            title,
            str(clause.get("quoted_text") or ""),
            str(clause.get("original_text") or ""),
            str(clause.get("clause_text") or ""),
            str(clause.get("text") or ""),
            str(clause.get("legal_insight") or ""),
        ]).lower()

        concepts = detect_concepts(
            title,
            text,
        )

        roles = detect_roles(concepts)

        domains = detect_legal_domains(text)

        all_triggers = []
        all_consequences = []

        for domain in domains:
            all_triggers.extend(
                detect_relation_triggers(
                    text,
                    domain,
                )
            )

            all_consequences.extend(
                detect_relation_consequences(
                    text,
                    domain,
                )
            )

        node_id = f"clause_{index}"

        nodes.append({
            "id": node_id,
            "title": title,
            "risk_level": clause.get("risk_level", "low"),
            "clause_type": clause.get("clause_type", "other"),
            "concepts": concepts,
            "roles": roles,
            "domains": domains,
            "relation_triggers": list(dict.fromkeys(all_triggers)),
            "relation_consequences": list(dict.fromkeys(all_consequences)),
        })

        indexed.append({
            "index": index,
            "title": title,
            "text": text,
            "concepts": concepts,
            "roles": roles,
            "domains": domains,
            "source_type": clause.get("clause_type", "other"),
        })

        for concept in concepts:
            group_name = DISPLAY_GROUPS.get(
                concept,
                concept,
            )

            groups.setdefault(
                group_name,
                [],
            ).append(node_id)

        for domain in domains:
            group_name = DISPLAY_GROUPS.get(domain, domain)
            groups.setdefault(group_name, []).append(node_id)

    add_relation_edges(
        indexed,
        edges,
        language,
    )

    directional_edges = build_directional_edges(nodes, language)
    cross_domain_edges = build_cross_domain_edges(nodes, language)

    return {
        "nodes": nodes,
        "edges": (
            edges
            + directional_edges
            + cross_domain_edges
        ),
        "groups": {
            group: list(dict.fromkeys(ids))
            for group, ids in groups.items()
        },
    }


def detect_concepts(
    title: str,
    text: str,
) -> list[str]:
    title_text = str(title or "").lower()
    body_text = str(text or "").lower()

    concepts = []

    for concept, terms in CONCEPT_TERMS.items():
        title_hit = contains_any(title_text, terms)
        body_hit = contains_any(body_text, terms)

        if title_hit:
            concepts.append(concept)
            continue

        if body_hit and concept in {
            "continuing_obligations",
            "performance_condition",
            "liability_protection",
            "data_protection",
            "ip_ownership",
            "restrictive_covenant",
            "dispute_resolution",
            "governance_control",
            "breach_default",
        }:
            concepts.append(concept)

    return list(dict.fromkeys(concepts))


def detect_roles(
    concepts: list[str],
) -> list[str]:
    roles = []

    for concept in concepts:
        role = LEGAL_ROLES.get(concept)

        if role and role not in roles:
            roles.append(role)

    return roles


def relation_allowed(
    source_roles: set[str],
    target_roles: set[str],
) -> bool:
    return any(
        source_role in source_roles
        and target_role in target_roles
        for source_role, target_role in ALLOWED_RELATIONS
    )


def add_relation_edges(
    indexed_clauses: list[dict],
    edges: list[dict],
    language: str = "en",
) -> None:

    seen = set()

    for source in indexed_clauses:
        for target in indexed_clauses:
            if source["index"] == target["index"]:
                continue

            relation = detect_relation(
                source,
                target,
                language,
            )

            if not relation:
                continue

            edge_key = (
                source["index"],
                target["index"],
                relation["type"],
            )

            if edge_key in seen:
                continue

            seen.add(edge_key)

            edges.append({
                "from": f"clause_{source['index']}",
                "to": f"clause_{target['index']}",
                "type": relation["type"],
                "reason": relation["reason"],
                "confidence": relation["confidence"],
            })


def detect_relation(
    source: dict,
    target: dict,
    language: str = "en",
) -> dict | None:

    language = _lang(language)

    source_concepts = set(source.get("concepts", []))
    target_concepts = set(target.get("concepts", []))

    source_roles = set(source.get("roles", []))
    target_roles = set(target.get("roles", []))

    if not relation_allowed(
        source_roles,
        target_roles,
    ):
        source_type = str(
            source.get("source_type", "")
        ).lower()

        target_text = " ".join([
            str(target.get("title", "")),
            str(target.get("text", "")),
        ]).lower()

        if source_type in DEPENDENCY_TRIGGERS:
            for trigger in DEPENDENCY_TRIGGERS[source_type]:
                if trigger in target_text:
                    return {
                        "type": "semantic_dependency",
                        "reason": _semantic_dependency_reason(source_type, trigger, language),
                        "confidence": 0.75,
                    }

        return None

    if (
        "notice_requirement" in source_concepts
        and "termination_event" in target_concepts
    ):
        return {
            "type": "notice_dependency",
            "reason": _relation_reason("notice_dependency", language),
            "confidence": 0.9,
        }

    if (
        "breach_default" in source_concepts
        and "termination_event" in target_concepts
    ):
        return {
            "type": "breach_termination_dependency",
            "reason": _relation_reason("breach_termination_dependency", language),
            "confidence": 0.85,
        }

    if (
        "performance_condition" in source_concepts
        and "payment_obligation" in target_concepts
    ):
        return {
            "type": "performance_payment_dependency",
            "reason": _relation_reason("performance_payment_dependency", language),
            "confidence": 0.85,
        }

    if (
        "confidentiality" in source_concepts
        and "continuing_obligations" in target_concepts
    ):
        return {
            "type": "survival_obligation",
            "reason": _relation_reason("survival_obligation", language),
            "confidence": 0.85,
        }

    if (
        "ip_ownership" in source_concepts
        and "confidentiality" in target_concepts
    ):
        return {
            "type": "information_rights_dependency",
            "reason": _relation_reason("information_rights_dependency", language),
            "confidence": 0.8,
        }

    if (
        "confidentiality" in source_concepts
        and "liability_protection" in target_concepts
    ):
        return {
            "type": "liability_exception",
            "reason": _relation_reason("liability_exception", language),
            "confidence": 0.8,
        }

    if (
        "data_protection" in source_concepts
        and "liability_protection" in target_concepts
    ):
        return {
            "type": "data_liability_dependency",
            "reason": _relation_reason("data_liability_dependency", language),
            "confidence": 0.85,
        }

    if (
        "restrictive_covenant" in source_concepts
        and "termination_event" in target_concepts
    ):
        return {
            "type": "post_contract_restriction_dependency",
            "reason": _relation_reason("post_contract_restriction_dependency", language),
            "confidence": 0.75,
        }

    return None


def contains_any(
    text: str,
    terms: list[str],
) -> bool:
    return any(
        term.lower() in text
        for term in terms
    )


def build_directional_edges(
    nodes: list,
    language: str = "en",
) -> list:

    edges = []

    for source in nodes:

        source_domains = set(
            source.get("domains", [])
        )

        source_triggers = set(
            source.get(
                "relation_triggers",
                [],
            )
        )

        if not source_triggers:
            continue

        for target in nodes:

            if source["id"] == target["id"]:
                continue

            target_domains = set(
                target.get("domains", [])
            )

            shared_domains = (
                source_domains
                & target_domains
            )

            if not shared_domains:
                continue

            target_consequences = set(
                target.get(
                    "relation_consequences",
                    [],
                )
            )

            if not target_consequences:
                continue

            shared_terms = set()

            for trigger in source_triggers:

                mapped_consequences = set(
                    get_trigger_consequences(trigger)
                )

                overlap = (
                    mapped_consequences
                    & target_consequences
                )

                shared_terms.update(overlap)

            shared_trigger_count = len(shared_terms)

            if (
                len(shared_domains) < 1
                or shared_trigger_count < 1
            ):
                continue

            score = (
                shared_trigger_count * 4
                + len(shared_domains)
            )

            if score < 5:
                continue

            edges.append({
                "from": source["id"],
                "to": target["id"],
                "domains": list(shared_domains),
                "shared_terms": list(shared_terms),
                "relation_type": "trigger_consequence",
                "type": "trigger_consequence",
                "reason": _relation_reason("trigger_consequence", language),
                "confidence": min(0.95, 0.65 + (score / 20)),
                "score": score,
            })

    return edges


def build_cross_domain_edges(
    nodes: list,
    language: str = "en",
) -> list:
    language = _lang(language)
    edges = []
    seen = set()

    for source in nodes:
        source_domains = set(source.get("domains", []))

        if not source_domains:
            continue

        for target in nodes:
            if source["id"] == target["id"]:
                continue

            target_domains = set(target.get("domains", []))

            if not target_domains:
                continue

            for rule in CROSS_DOMAIN_RELATIONS:
                if (
                    rule["source_domain"] in source_domains
                    and rule["target_domain"] in target_domains
                ):
                    key = (
                        source["id"],
                        target["id"],
                        rule["type"],
                    )

                    if key in seen:
                        continue

                    seen.add(key)

                    reason_value = rule["reason"]
                    if isinstance(reason_value, dict):
                        reason_value = reason_value.get(language, reason_value.get("en", ""))

                    edges.append({
                        "from": source["id"],
                        "to": target["id"],
                        "type": rule["type"],
                        "relation_type": "cross_domain_dependency",
                        "domains": [
                            rule["source_domain"],
                            rule["target_domain"],
                        ],
                        "reason": reason_value,
                        "confidence": rule["confidence"],
                    })

    return edges