LEGAL_ONTOLOGY = {
    "termination": {
        "concepts": [
            "termination",
            "dismissal",
            "resignation",
            "good reason",
            "for cause",
            "without cause",
            "constructive termination",
            "non-renewal",
            "expiration",

            "résiliation",
            "licenciement",
            "démission",
            "non-renouvellement",
            "expiration",

            "إنهاء",
            "فسخ",
            "استقالة",
            "عدم التجديد",
            "انتهاء",
        ],
        "roles": [
            "trigger",
            "notice",
            "compensation",
            "severance",
            "breach_consequence",
        ],
    },

    "payment": {
        "concepts": [
            "payment",
            "salary",
            "bonus",
            "compensation",
            "fees",
            "invoice",
            "pricing",
            "refund",
            "reimbursement",
            "commission",
            "royalties",

            "paiement",
            "salaire",
            "prime",
            "rémunération",
            "frais",
            "facture",
            "prix",
            "remboursement",
            "commission",
            "redevances",

            "دفع",
            "سداد",
            "راتب",
            "مكافأة",
            "تعويض",
            "رسوم",
            "فاتورة",
            "تسعير",
            "استرداد",
            "عمولة",
            "إتاوات",
        ],
        "roles": [
            "payment_obligation",
            "late_payment",
            "financial_trigger",
        ],
    },

    "confidentiality": {
        "concepts": [
            "confidentiality",
            "confidential information",
            "nda",
            "non-disclosure",
            "trade secret",

            "confidentialité",
            "information confidentielle",
            "accord de confidentialité",
            "non-divulgation",
            "secret commercial",

            "السرية",
            "معلومات سرية",
            "اتفاقية عدم الإفصاح",
            "عدم الإفصاح",
            "سر تجاري",
        ],
        "roles": [
            "non_disclosure",
            "post_contract_obligation",
            "data_protection",
        ],
    },

    "liability": {
        "concepts": [
            "liability",
            "damages",
            "indemnification",
            "indemnity",
            "limitation of liability",
            "liability cap",
            "unlimited liability",
            "insurance",
            "warranty",
            "remedies",

            "responsabilité",
            "dommages",
            "indemnisation",
            "limitation de responsabilité",
            "plafond de responsabilité",
            "responsabilité illimitée",
            "assurance",
            "garantie",
            "recours",

            "المسؤولية",
            "الأضرار",
            "التعويض",
            "حد المسؤولية",
            "مسؤولية غير محدودة",
            "تأمين",
            "ضمان",
            "وسائل الانتصاف",
        ],
        "roles": [
            "financial_exposure",
            "risk_allocation",
            "indemnity",
        ],
    },

    "data_privacy_security": {
        "concepts": [
            "personal data",
            "data protection",
            "data processing",
            "processor",
            "controller",
            "subprocessor",
            "privacy",
            "security incident",
            "security measures",
            "cybersecurity",
            "data breach",

            "données personnelles",
            "protection des données",
            "traitement des données",
            "sous-traitant",
            "responsable du traitement",
            "vie privée",
            "incident de sécurité",
            "mesures de sécurité",
            "cybersécurité",
            "violation de données",

            "بيانات شخصية",
            "حماية البيانات",
            "معالجة البيانات",
            "معالج البيانات",
            "المتحكم في البيانات",
            "الخصوصية",
            "حادث أمني",
            "تدابير أمنية",
            "الأمن السيبراني",
            "اختراق البيانات",
        ],
        "roles": [
            "data_processing_obligation",
            "security_obligation",
            "privacy_obligation",
            "incident_response",
        ],
    },

    "services_operations": {
        "concepts": [
            "services",
            "service level",
            "sla",
            "support",
            "maintenance",
            "delivery",
            "acceptance",
            "performance",
            "change request",
            "availability",
            "uptime",
            "service credit",

            "services",
            "niveau de service",
            "support",
            "maintenance",
            "livraison",
            "acceptation",
            "performance",
            "demande de changement",
            "disponibilité",
            "crédit de service",

            "الخدمات",
            "مستوى الخدمة",
            "الدعم",
            "الصيانة",
            "التسليم",
            "القبول",
            "الأداء",
            "طلب تغيير",
            "التوافر",
            "تعويض الخدمة",
        ],
        "roles": [
            "service_obligation",
            "operational_requirement",
            "performance_standard",
        ],
    },

    "intellectual_property": {
        "concepts": [
            "intellectual property",
            "ip",
            "ownership",
            "assignment",
            "license",
            "work product",
            "deliverables",
            "copyright",
            "trademark",
            "patent",
            "invention",
            "moral rights",

            "propriété intellectuelle",
            "cession",
            "licence",
            "livrables",
            "droit d'auteur",
            "marque",
            "brevet",
            "invention",
            "droits moraux",

            "الملكية الفكرية",
            "تنازل",
            "ترخيص",
            "مخرجات العمل",
            "حقوق النشر",
            "علامة تجارية",
            "براءة",
            "اختراع",
            "حقوق معنوية",
        ],
        "roles": [
            "ownership_allocation",
            "license_right",
            "assignment_obligation",
            "use_restriction",
        ],
    },

    "restrictive_covenants": {
        "concepts": [
            "non-compete",
            "non compete",
            "non-solicitation",
            "non solicitation",
            "non-dealing",
            "non dealing",
            "non-circumvention",
            "non circumvention",
            "exclusivity",
            "exclusive dealing",
            "restraint of trade",
            "customer solicitation",
            "employee solicitation",

            "non-concurrence",
            "non-sollicitation",
            "non sollicitation",
            "non-contournement",
            "exclusivité",
            "restriction de concurrence",
            "sollicitation de clients",
            "sollicitation d'employés",

            "عدم المنافسة",
            "عدم الاستقطاب",
            "عدم الالتفاف",
            "الحصرية",
            "قيد المنافسة",
            "استقطاب العملاء",
            "استقطاب الموظفين",
        ],
        "roles": [
            "competitive_restriction",
            "post_contract_restriction",
            "market_access_restriction",
        ],
    },

    "conflict_of_interest": {
        "concepts": [
            "conflict of interest",
            "conflicting interest",
            "fiduciary duty",
            "self dealing",
            "self-dealing",
            "related party",
            "disinterested directors",
            "interested transaction",

            "conflit d'intérêt",
            "conflit d’intérêts",
            "devoir fiduciaire",
            "partie liée",
            "transaction intéressée",

            "تعارض المصالح",
            "تضارب المصالح",
            "واجب ائتماني",
            "طرف ذو صلة",
            "معاملة ذات مصلحة",
        ],
        "roles": [
            "governance_constraint",
            "approval_condition",
            "conflict_control",
        ],
    },

    "arbitration": {
        "concepts": [
            "arbitration",
            "arbitrator",
            "binding arbitration",
            "commercial arbitration rules",
            "arbitral tribunal",
            "american arbitration association",
            "icc arbitration",
            "lcia arbitration",

            "arbitrage",
            "arbitre",
            "tribunal arbitral",
            "sentence arbitrale",

            "تحكيم",
            "محكم",
            "هيئة التحكيم",
            "قرار تحكيمي",
        ],
        "roles": [
            "dispute_resolution",
            "forum",
        ],
    },

    "notice": {
        "concepts": [
            "notice",
            "written notice",
            "notices",
            "notify",
            "notification",

            "avis",
            "préavis",
            "notification",
            "avis écrit",
            "notifier",

            "إشعار",
            "إخطار",
            "إبلاغ",
            "إشعار خطي",
        ],
        "roles": [
            "procedural_requirement",
            "notice_requirement",
        ],
    },

    "change_of_control": {
        "concepts": [
            "change of control",
            "merger",
            "acquisition",
            "takeover",
            "sale of substantially all assets",
            "sale of all or substantially all assets",

            "changement de contrôle",
            "fusion",
            "acquisition",
            "cession de la quasi-totalité des actifs",

            "تغيير السيطرة",
            "تغيير التحكم",
            "اندماج",
            "استحواذ",
            "بيع معظم الأصول",
        ],
        "roles": [
            "trigger",
            "corporate_transaction",
            "control_event",
        ],
    },

    "governing_law": {
        "concepts": [
            "governing law",
            "jurisdiction",
            "venue",
            "court",
            "courts",
            "applicable law",

            "droit applicable",
            "juridiction",
            "tribunal",
            "tribunaux",
            "loi applicable",

            "القانون الواجب التطبيق",
            "الاختصاص",
            "محكمة",
            "المحاكم",
            "القانون المطبق",
        ],
        "roles": [
            "forum",
            "dispute_resolution",
            "jurisdiction_selection",
        ],
    },

    "employment_hr": {
        "concepts": [
            "employee",
            "employment",
            "employment agreement",
            "salary",
            "termination of employment",
            "vacation",
            "benefits",
            "employer",
            "compensation",
            "working time",
            "leave",
            "disciplinary",

            "employé",
            "emploi",
            "contrat de travail",
            "salaire",
            "congés",
            "avantages",
            "employeur",
            "rémunération",
            "temps de travail",
            "licenciement",

            "موظف",
            "عمل",
            "عقد عمل",
            "راتب",
            "إجازة",
            "مزايا",
            "صاحب العمل",
            "تعويض",
            "ساعات العمل",
        ],
        "roles": [
            "employment_relationship",
            "compensation_obligation",
            "employee_benefit",
        ],
    },

    "finance_lending": {
        "concepts": [
            "loan",
            "financing",
            "interest",
            "collateral",
            "guarantee",
            "repayment",
            "acceleration",
            "borrower",
            "lender",
            "security interest",

            "prêt",
            "financement",
            "intérêt",
            "garantie",
            "sûreté",
            "remboursement",
            "exigibilité",
            "emprunteur",
            "prêteur",

            "قرض",
            "تمويل",
            "فائدة",
            "ضمان",
            "حق ضمان",
            "سداد",
            "مقترض",
            "مقرض",
        ],
        "roles": [
            "loan_obligation",
            "repayment_obligation",
            "security_interest",
            "default_consequence",
        ],
    },

    "real_estate": {
        "concepts": [
            "lease",
            "rent",
            "deposit",
            "premises",
            "property",
            "repairs",
            "utilities",
            "tenant",
            "landlord",

            "bail",
            "loyer",
            "dépôt",
            "locaux",
            "bien immobilier",
            "réparations",
            "charges",
            "locataire",
            "bailleur",

            "إيجار",
            "أجرة",
            "وديعة",
            "عقار",
            "إصلاحات",
            "مرافق",
            "مستأجر",
            "مؤجر",
        ],
        "roles": [
            "lease_obligation",
            "rent_obligation",
            "property_use",
            "maintenance_obligation",
        ],
    },

    "governance_compliance": {
        "concepts": [
            "assignment",
            "change of control",
            "compliance",
            "anti-bribery",
            "sanctions",
            "governance",
            "subcontracting",
            "audit",
            "board",
            "director",
            "shareholder",
            "approval",
            "consent",

            "cession",
            "changement de contrôle",
            "conformité",
            "lutte contre la corruption",
            "sanctions",
            "gouvernance",
            "sous-traitance",
            "audit",
            "conseil",
            "administrateur",
            "actionnaire",
            "approbation",
            "consentement",

            "التنازل",
            "تغيير السيطرة",
            "الامتثال",
            "مكافحة الرشوة",
            "العقوبات",
            "الحوكمة",
            "التعاقد من الباطن",
            "التدقيق",
            "مجلس الإدارة",
            "مدير",
            "مساهم",
            "موافقة",
        ],
        "roles": [
            "governance_constraint",
            "approval_condition",
            "compliance_obligation",
            "third_party_control",
        ],
    },
}


LEGAL_RELATIONS = {
    "termination": {
        "trigger_terms": [
            "breach", "default", "misconduct", "cause",
            "disability", "death", "good reason",
            "change of control",
            "manquement", "faute", "incapacité", "décès",
            "إخلال", "خطأ", "عجز", "وفاة",
        ],
        "consequence_terms": [
            "terminate", "termination", "severance",
            "compensation", "notice",
            "résiliation", "indemnité", "préavis",
            "إنهاء", "فسخ", "تعويض", "إشعار",
        ],
    },

    "payment": {
        "trigger_terms": [
            "invoice", "milestone", "delivery",
            "performance", "approval",
            "facture", "livraison", "performance",
            "فاتورة", "تسليم", "أداء",
        ],
        "consequence_terms": [
            "payment", "late fee", "interest",
            "suspension", "reimbursement",
            "paiement", "intérêt", "suspension",
            "دفع", "فائدة", "تعليق", "سداد",
        ],
    },

    "confidentiality": {
        "trigger_terms": [
            "disclosure", "unauthorized use", "breach",
            "divulgation", "utilisation non autorisée",
            "إفصاح", "استعمال غير مصرح",
        ],
        "consequence_terms": [
            "injunction", "damages", "termination",
            "injonction", "dommages", "résiliation",
            "أمر قضائي", "تعويض", "فسخ",
        ],
    },

    "liability": {
        "trigger_terms": [
            "breach",
            "claim",
            "third party claim",
            "loss",
            "damage",
            "liability",
            "réclamation",
            "perte",
            "dommage",
            "responsabilité",
            "مطالبة",
            "خسارة",
            "ضرر",
            "مسؤولية",
        ],
        "consequence_terms": [
            "indemnification",
            "damages",
            "liability cap",
            "limitation of liability",
            "insurance",
            "indemnisation",
            "dommages",
            "plafond de responsabilité",
            "assurance",
            "تعويض",
            "أضرار",
            "حد المسؤولية",
            "تأمين",
        ],
    },

    "data_privacy_security": {
        "trigger_terms": [
            "security incident",
            "data breach",
            "unauthorized access",
            "personal data",
            "incident de sécurité",
            "violation de données",
            "accès non autorisé",
            "données personnelles",
            "حادث أمني",
            "اختراق البيانات",
            "وصول غير مصرح",
            "بيانات شخصية",
        ],
        "consequence_terms": [
            "notify",
            "report",
            "remediate",
            "cooperate",
            "notification",
            "signaler",
            "corriger",
            "coopérer",
            "إخطار",
            "إبلاغ",
            "معالجة",
            "تعاون",
        ],
    },

    "restrictive_covenants": {
        "trigger_terms": [
            "termination",
            "post-termination",
            "after termination",
            "during the term",
            "résiliation",
            "après la résiliation",
            "pendant la durée",
            "إنهاء",
            "بعد الإنهاء",
            "خلال المدة",
        ],
        "consequence_terms": [
            "non-compete",
            "non-solicitation",
            "exclusivity",
            "restriction",
            "non-concurrence",
            "non-sollicitation",
            "exclusivité",
            "restriction",
            "عدم المنافسة",
            "عدم الاستقطاب",
            "الحصرية",
            "قيد",
        ],
    },

    "change_of_control": {
        "trigger_terms": [
            "change of control",
            "merger",
            "acquisition",
            "takeover",
            "sale of substantially all assets",
            "changement de contrôle",
            "fusion",
            "acquisition",
            "تغيير السيطرة",
            "اندماج",
            "استحواذ",
        ],
        "consequence_terms": [
            "termination",
            "compensation",
            "vesting",
            "lump sum",
            "résiliation",
            "indemnité",
            "acquisition des droits",
            "إنهاء",
            "تعويض",
            "استحقاق",
        ],
    },

    "arbitration": {
        "trigger_terms": [
            "dispute",
            "claim",
            "breach",
            "litige",
            "réclamation",
            "manquement",
            "نزاع",
            "مطالبة",
            "إخلال",
        ],
        "consequence_terms": [
            "arbitration",
            "arbitrator",
            "award",
            "arbitrage",
            "arbitre",
            "sentence arbitrale",
            "تحكيم",
            "محكم",
            "قرار تحكيمي",
        ],
    },
}


def detect_legal_domains(text: str) -> list[str]:
    normalized = str(text or "").lower()
    domains = []

    for domain, data in LEGAL_ONTOLOGY.items():
        if any(
            term.lower() in normalized
            for term in data.get("concepts", [])
        ):
            domains.append(domain)

    return domains


def detect_legal_roles(text: str) -> list[str]:
    normalized = str(text or "").lower()
    roles = []

    for data in LEGAL_ONTOLOGY.values():
        for role in data.get("roles", []):
            role_terms = role.replace("_", " ").lower()

            if role_terms in normalized:
                roles.append(role)

    return list(dict.fromkeys(roles))


def get_domain_concepts(domain: str) -> list[str]:
    return LEGAL_ONTOLOGY.get(
        domain,
        {},
    ).get(
        "concepts",
        [],
    )


def get_domain_roles(domain: str) -> list[str]:
    return LEGAL_ONTOLOGY.get(
        domain,
        {},
    ).get(
        "roles",
        [],
    )


def get_relation_terms(domain: str) -> dict:
    return LEGAL_RELATIONS.get(
        domain,
        {},
    )


def detect_relation_triggers(
    text: str,
    domain: str,
) -> list[str]:

    normalized = str(text or "").lower()

    relation_data = LEGAL_RELATIONS.get(
        domain,
        {},
    )

    triggers = []

    for term in relation_data.get(
        "trigger_terms",
        [],
    ):
        if term.lower() in normalized:
            triggers.append(term)

    return list(dict.fromkeys(triggers))


def detect_relation_consequences(
    text: str,
    domain: str,
) -> list[str]:

    normalized = str(text or "").lower()

    relation_data = LEGAL_RELATIONS.get(
        domain,
        {},
    )

    consequences = []

    for term in relation_data.get(
        "consequence_terms",
        [],
    ):
        if term.lower() in normalized:
            consequences.append(term)

    return list(dict.fromkeys(consequences))


LEGAL_TRIGGER_TO_CONSEQUENCE = {
    "breach": [
        "termination",
        "damages",
        "injunction",
    ],
    "default": [
        "termination",
        "late fee",
        "interest",
    ],
    "misconduct": [
        "termination",
    ],
    "disability": [
        "termination",
        "compensation",
    ],
    "death": [
        "termination",
        "compensation",
    ],
    "good reason": [
        "termination",
        "compensation",
    ],
    "change of control": [
        "termination",
        "compensation",
        "vesting",
    ],
    "merger": [
        "termination",
        "compensation",
    ],
    "acquisition": [
        "termination",
        "compensation",
    ],
    "invoice": [
        "payment",
        "late fee",
    ],
    "delivery": [
        "payment",
    ],
    "disclosure": [
        "injunction",
        "damages",
        "termination",
    ],
    "security incident": [
        "notification",
        "remediation",
        "cooperation",
    ],
    "data breach": [
        "notification",
        "remediation",
        "cooperation",
    ],
    "dispute": [
        "arbitration",
    ],
    "claim": [
        "arbitration",
        "indemnification",
    ],
    "post-termination": [
        "non-compete",
        "non-solicitation",
        "confidentiality",
    ],
}


def get_trigger_consequences(
    trigger: str,
) -> list[str]:

    return LEGAL_TRIGGER_TO_CONSEQUENCE.get(
        str(trigger or "").lower(),
        [],
    )

# ---------------------------------------------------------------------------
# International universal ontology extensions
# ---------------------------------------------------------------------------
# Privacy-first: these dictionaries only classify legal concepts in anonymized
# or generic contract text. They do not infer, reconstruct, restore, request,
# or output real party identities or personal data.

INTERNATIONAL_LEGAL_ONTOLOGY_EXTENSIONS = {
    "force_majeure": {
        "concepts": [
            "force majeure", "act of god", "natural disaster",
            "unforeseeable event", "beyond reasonable control",
            "epidemic", "pandemic", "war", "strike", "government action",
            "cas de force majeure", "cas fortuit", "catastrophe naturelle",
            "événement imprévisible", "hors du contrôle raisonnable",
            "épidémie", "pandémie", "guerre", "grève", "action gouvernementale",
            "القوة القاهرة", "حدث غير متوقع", "خارج السيطرة المعقولة",
            "كارثة طبيعية", "وباء", "جائحة", "حرب", "إضراب", "إجراء حكومي",
        ],
        "roles": [
            "performance_excuse",
            "mitigation_obligation",
            "notice_requirement",
            "suspension_right",
            "termination_trigger",
        ],
    },
    "tax": {
        "concepts": [
            "tax", "taxes", "vat", "gst", "withholding", "gross-up",
            "tax invoice", "sales tax", "duties", "levies",
            "impôt", "impôts", "taxe", "tva", "retenue à la source",
            "majoration fiscale", "facture fiscale", "droits", "prélèvements",
            "ضريبة", "ضرائب", "القيمة المضافة", "اقتطاع", "استقطاع",
            "تعويض ضريبي", "فاتورة ضريبية", "رسوم", "جبايات",
        ],
        "roles": [
            "tax_obligation",
            "withholding_obligation",
            "gross_up_obligation",
            "invoice_requirement",
        ],
    },
    "warranties": {
        "concepts": [
            "warranty", "warranties", "representation", "representations",
            "representations and warranties", "as is", "disclaimer of warranty",
            "fitness for purpose", "merchantability", "defect warranty",
            "garantie", "garanties", "déclaration", "déclarations",
            "déclarations et garanties", "en l'état", "exclusion de garantie",
            "aptitude à l'usage", "vice",
            "ضمان", "ضمانات", "إقرار", "إقرارات",
            "الإقرارات والضمانات", "كما هو", "استبعاد الضمان",
            "ملاءمة للغرض", "عيب",
        ],
        "roles": [
            "quality_commitment",
            "representation_statement",
            "disclaimer",
            "remedy_allocation",
        ],
    },
    "renewal": {
        "concepts": [
            "renewal", "automatic renewal", "auto-renewal", "renewal term",
            "extension term", "successive terms", "non-renewal",
            "renouvellement", "reconduction automatique",
            "période de renouvellement", "durée de renouvellement",
            "non-renouvellement",
            "تجديد", "تجديد تلقائي", "مدة التجديد",
            "فترات متتالية", "عدم التجديد",
        ],
        "roles": [
            "renewal_trigger",
            "non_renewal_notice",
            "term_extension",
            "pricing_adjustment",
        ],
    },
    "suspension": {
        "concepts": [
            "suspension", "suspend", "suspend services",
            "service suspension", "reinstatement", "restore service",
            "access suspension",
            "suspension", "suspendre", "suspendre les services",
            "rétablissement", "restaurer le service",
            "تعليق", "يعلق", "تعليق الخدمات",
            "استئناف الخدمة", "إعادة الخدمة", "تعليق الوصول",
        ],
        "roles": [
            "suspension_right",
            "cure_right",
            "service_continuity",
            "reinstatement_condition",
        ],
    },
    "business_continuity": {
        "concepts": [
            "business continuity", "disaster recovery", "bcp", "drp",
            "backup", "restore", "recovery time objective", "rto",
            "recovery point objective", "rpo", "contingency plan",
            "continuité d'activité", "reprise après sinistre",
            "sauvegarde", "restauration", "plan de continuité",
            "خطة استمرارية الأعمال", "استمرارية الأعمال",
            "التعافي من الكوارث", "نسخ احتياطي", "استعادة", "خطة طوارئ",
        ],
        "roles": [
            "continuity_obligation",
            "recovery_obligation",
            "backup_obligation",
            "incident_response",
        ],
    },
    "publicity": {
        "concepts": [
            "publicity", "press release", "public announcement",
            "use of name", "logo", "trademark in marketing",
            "case study", "reference customer",
            "publicité", "communiqué de presse", "annonce publique",
            "utilisation du nom", "logo", "étude de cas", "référence client",
            "دعاية", "بيان صحفي", "إعلان عام", "استخدام الاسم",
            "الشعار", "دراسة حالة", "عميل مرجعي",
        ],
        "roles": [
            "approval_condition",
            "brand_use_restriction",
            "confidentiality_control",
            "marketing_reference",
        ],
    },
    "severability": {
        "concepts": [
            "severability", "invalid provision", "unenforceable provision",
            "severed", "valid substitute", "remaining provisions",
            "divisibilité", "clause invalide", "clause inapplicable",
            "séparée", "disposition de remplacement",
            "قابلية الفصل", "حكم غير صحيح", "حكم غير قابل للتنفيذ",
            "فصل الحكم", "حكم بديل", "باقي الأحكام",
        ],
        "roles": [
            "invalidity_consequence",
            "replacement_mechanism",
            "contract_preservation",
        ],
    },
    "survival": {
        "concepts": [
            "survival", "survive termination", "survive expiry",
            "post-termination obligations", "continue after termination",
            "survie", "survivent à la résiliation",
            "obligations postérieures à la résiliation",
            "continuer après la résiliation",
            "استمرار", "تستمر بعد الإنهاء", "تستمر بعد الانقضاء",
            "التزامات ما بعد الإنهاء",
        ],
        "roles": [
            "post_contract_obligation",
            "surviving_obligation",
            "duration_control",
        ],
    },
    "amendment": {
        "concepts": [
            "amendment", "amendments", "modified only in writing",
            "change order", "variation", "written modification",
            "modification", "avenant", "modifié uniquement par écrit",
            "ordre de modification", "changement",
            "تعديل", "تعديلات", "لا يعدل إلا كتابة",
            "أمر تغيير", "تغيير كتابي",
        ],
        "roles": [
            "written_approval",
            "change_control",
            "authorization_requirement",
        ],
    },
    "waiver": {
        "concepts": [
            "waiver", "no waiver", "failure to enforce",
            "delay in exercising", "waive", "single waiver",
            "renonciation", "absence de renonciation",
            "défaut d'exercice", "retard dans l'exercice", "renoncer",
            "تنازل", "عدم التنازل", "عدم ممارسة الحق",
            "التأخر في ممارسة الحق", "يتنازل",
        ],
        "roles": [
            "rights_preservation",
            "written_waiver",
            "specific_waiver",
        ],
    },
    "assignment": {
        "concepts": [
            "assignment", "assign", "transfer this agreement",
            "delegate", "novation", "permitted transfer",
            "cession", "céder", "transfert du contrat",
            "déléguer", "novation",
            "تنازل", "نقل العقد", "تفويض", "حوالة",
        ],
        "roles": [
            "assignment_restriction",
            "consent_requirement",
            "transfer_right",
            "delegation_control",
        ],
    },
    "insurance": {
        "concepts": [
            "insurance", "policy", "coverage", "insured",
            "certificate of insurance", "deductible", "additional insured",
            "assurance", "police", "couverture", "assuré",
            "attestation d'assurance", "franchise", "assuré additionnel",
            "تأمين", "وثيقة التأمين", "تغطية", "مؤمن عليه",
            "شهادة تأمين", "تحمل", "مؤمن له إضافي",
        ],
        "roles": [
            "coverage_requirement",
            "insurance_evidence",
            "risk_allocation",
            "claim_process",
        ],
    },
    "export_control": {
        "concepts": [
            "export control", "sanctions", "trade sanctions",
            "restricted party", "embargo", "anti-boycott", "dual use",
            "contrôle des exportations", "sanctions", "embargo",
            "partie restreinte", "double usage",
            "ضوابط التصدير", "عقوبات", "حظر",
            "طرف مقيد", "استخدام مزدوج",
        ],
        "roles": [
            "trade_compliance",
            "restricted_party_screening",
            "export_restriction",
            "sanctions_termination",
        ],
    },
    "open_source": {
        "concepts": [
            "open source", "copyleft", "oss", "third-party software",
            "source code", "software component",
            "logiciel libre", "open source", "copyleft",
            "logiciel tiers", "code source",
            "برنامج مفتوح المصدر", "كود مفتوح", "كود المصدر",
            "برنامج طرف ثالث",
        ],
        "roles": [
            "license_compliance",
            "source_code_obligation",
            "third_party_component",
            "disclosure_obligation",
        ],
    },
    "escrow": {
        "concepts": [
            "escrow", "source code escrow", "deposit materials",
            "release condition",
            "séquestre", "séquestre de code source",
            "dépôt", "condition de libération",
            "ضمان الكود", "إيداع", "مواد مودعة", "شرط الإفراج",
        ],
        "roles": [
            "deposit_obligation",
            "release_condition",
            "verification_right",
            "access_right",
        ],
    },
    "transition_assistance": {
        "concepts": [
            "transition assistance", "exit assistance", "handover",
            "migration", "knowledge transfer", "wind-down",
            "assistance de transition", "assistance à la sortie",
            "transfert de connaissances", "migration", "remise",
            "مساعدة انتقالية", "مساعدة الخروج",
            "نقل المعرفة", "ترحيل", "تسليم انتقالي",
        ],
        "roles": [
            "exit_obligation",
            "migration_support",
            "data_portability",
            "knowledge_transfer",
        ],
    },
}


INTERNATIONAL_LEGAL_RELATIONS = {
    "force_majeure": {
        "trigger_terms": [
            "force majeure", "natural disaster", "pandemic",
            "government action", "cas de force majeure", "catastrophe naturelle",
            "pandémie", "القوة القاهرة", "كارثة طبيعية", "جائحة",
        ],
        "consequence_terms": [
            "suspension", "excuse from performance", "extension",
            "termination", "mitigation", "suspension", "exonération",
            "prolongation", "résiliation", "تعليق", "إعفاء من التنفيذ",
            "تمديد", "فسخ",
        ],
    },
    "tax": {
        "trigger_terms": [
            "invoice", "payment", "withholding", "vat",
            "facture", "paiement", "retenue à la source", "tva",
            "فاتورة", "دفع", "اقتطاع", "القيمة المضافة",
        ],
        "consequence_terms": [
            "gross-up", "tax liability", "reimbursement", "penalty",
            "majoration fiscale", "responsabilité fiscale", "remboursement",
            "pénalité", "تعويض ضريبي", "مسؤولية ضريبية", "استرداد", "غرامة",
        ],
    },
    "warranties": {
        "trigger_terms": [
            "defect", "breach of warranty", "misrepresentation",
            "vice", "violation de garantie", "fausse déclaration",
            "عيب", "خرق الضمان", "تصريح مضلل",
        ],
        "consequence_terms": [
            "repair", "replacement", "refund", "re-performance",
            "réparation", "remplacement", "remboursement", "réexécution",
            "إصلاح", "استبدال", "رد المبلغ", "إعادة التنفيذ",
        ],
    },
    "renewal": {
        "trigger_terms": [
            "expiration", "renewal date", "non-renewal notice",
            "expiration", "date de renouvellement", "préavis de non-renouvellement",
            "انتهاء", "تاريخ التجديد", "إشعار عدم التجديد",
        ],
        "consequence_terms": [
            "automatic renewal", "extension", "termination",
            "reconduction automatique", "prolongation", "résiliation",
            "تجديد تلقائي", "تمديد", "فسخ",
        ],
    },
    "suspension": {
        "trigger_terms": [
            "non-payment", "breach", "security risk", "unauthorized use",
            "non-paiement", "manquement", "risque de sécurité",
            "utilisation non autorisée",
            "عدم الدفع", "إخلال", "خطر أمني", "استخدام غير مصرح",
        ],
        "consequence_terms": [
            "suspension", "reinstatement", "access restriction",
            "termination", "suspension", "rétablissement", "restriction d'accès",
            "résiliation", "تعليق", "استئناف", "تقييد الوصول", "فسخ",
        ],
    },
    "business_continuity": {
        "trigger_terms": [
            "incident", "disruption", "disaster", "security incident",
            "incident", "perturbation", "sinistre",
            "حادث", "تعطيل", "كارثة",
        ],
        "consequence_terms": [
            "restore", "backup", "recovery", "continuity plan",
            "restaurer", "sauvegarde", "reprise", "plan de continuité",
            "استعادة", "نسخ احتياطي", "تعافي", "خطة الاستمرارية",
        ],
    },
    "publicity": {
        "trigger_terms": [
            "press release", "public announcement", "use of name",
            "communiqué de presse", "annonce publique", "utilisation du nom",
            "بيان صحفي", "إعلان عام", "استخدام الاسم",
        ],
        "consequence_terms": [
            "approval", "removal", "injunction", "damages",
            "approbation", "retrait", "injonction", "dommages",
            "موافقة", "إزالة", "أمر قضائي", "تعويض",
        ],
    },
    "severability": {
        "trigger_terms": [
            "invalid provision", "unenforceable provision",
            "clause invalide", "clause inapplicable",
            "حكم غير صحيح", "حكم غير قابل للتنفيذ",
        ],
        "consequence_terms": [
            "severed", "replacement", "remaining agreement",
            "séparée", "remplacement", "reste du contrat",
            "فصل", "استبدال", "باقي العقد",
        ],
    },
    "survival": {
        "trigger_terms": [
            "termination", "expiration", "résiliation", "expiration",
            "إنهاء", "انتهاء",
        ],
        "consequence_terms": [
            "survival", "post-termination obligation", "continue",
            "survie", "obligation postérieure", "continuer",
            "استمرار", "التزام بعد الإنهاء", "تستمر",
        ],
    },
    "amendment": {
        "trigger_terms": [
            "change", "amendment", "variation", "modification",
            "avenant", "changement", "تعديل", "تغيير",
        ],
        "consequence_terms": [
            "written approval", "change order", "authorization",
            "approbation écrite", "ordre de modification", "autorisation",
            "موافقة كتابية", "أمر تغيير", "تفويض",
        ],
    },
    "waiver": {
        "trigger_terms": [
            "failure to enforce", "delay", "waiver",
            "défaut d'exercice", "retard", "renonciation",
            "عدم ممارسة الحق", "تأخر", "تنازل",
        ],
        "consequence_terms": [
            "rights preserved", "written waiver", "future enforcement",
            "droits préservés", "renonciation écrite", "exécution future",
            "الحقوق محفوظة", "تنازل كتابي", "تنفيذ مستقبلي",
        ],
    },
    "assignment": {
        "trigger_terms": [
            "assignment", "transfer", "delegate", "change of control",
            "cession", "transfert", "déléguer", "changement de contrôle",
            "تنازل", "نقل", "تفويض", "تغيير السيطرة",
        ],
        "consequence_terms": [
            "consent", "void assignment", "termination",
            "consentement", "cession nulle", "résiliation",
            "موافقة", "تنازل باطل", "فسخ",
        ],
    },
    "insurance": {
        "trigger_terms": [
            "claim", "loss", "damage", "réclamation", "perte", "dommage",
            "مطالبة", "خسارة", "ضرر",
        ],
        "consequence_terms": [
            "coverage", "certificate of insurance", "indemnification",
            "couverture", "attestation d'assurance", "indemnisation",
            "تغطية", "شهادة تأمين", "تعويض",
        ],
    },
    "export_control": {
        "trigger_terms": [
            "export", "sanctions", "restricted party",
            "exportation", "sanctions", "partie restreinte",
            "تصدير", "عقوبات", "طرف مقيد",
        ],
        "consequence_terms": [
            "termination", "suspension", "blocked transaction",
            "résiliation", "suspension", "transaction bloquée",
            "فسخ", "تعليق", "معاملة محظورة",
        ],
    },
    "open_source": {
        "trigger_terms": [
            "open source", "copyleft", "third-party software",
            "logiciel libre", "copyleft", "logiciel tiers",
            "مفتوح المصدر", "برنامج طرف ثالث",
        ],
        "consequence_terms": [
            "disclosure", "replacement", "license compliance",
            "divulgation", "remplacement", "conformité de licence",
            "إفصاح", "استبدال", "امتثال الترخيص",
        ],
    },
    "escrow": {
        "trigger_terms": [
            "release condition", "bankruptcy", "failure to support",
            "condition de libération", "faillite", "défaut de support",
            "شرط الإفراج", "إفلاس", "فشل الدعم",
        ],
        "consequence_terms": [
            "release", "access", "use rights",
            "libération", "accès", "droits d'utilisation",
            "إفراج", "وصول", "حقوق استخدام",
        ],
    },
    "transition_assistance": {
        "trigger_terms": [
            "termination", "expiry", "migration",
            "résiliation", "expiration", "migration",
            "إنهاء", "انقضاء", "ترحيل",
        ],
        "consequence_terms": [
            "handover", "exit assistance", "knowledge transfer",
            "remise", "assistance à la sortie", "transfert de connaissances",
            "تسليم", "مساعدة الخروج", "نقل المعرفة",
        ],
    },
}


INTERNATIONAL_TRIGGER_TO_CONSEQUENCE = {
    "force majeure": ["suspension", "extension", "termination"],
    "natural disaster": ["suspension", "mitigation", "extension"],
    "pandemic": ["suspension", "continuity plan", "termination"],
    "withholding": ["gross-up", "tax documentation", "invoice adjustment"],
    "vat": ["tax invoice", "payment adjustment"],
    "breach of warranty": ["repair", "replacement", "refund"],
    "misrepresentation": ["damages", "rescission", "indemnification"],
    "expiration": ["renewal", "survival", "transition assistance"],
    "non-renewal notice": ["termination at expiry", "transition assistance"],
    "non-payment": ["suspension", "late fee", "termination"],
    "security risk": ["suspension", "remediation", "cooperation"],
    "disaster": ["business continuity", "disaster recovery", "backup restore"],
    "press release": ["approval", "removal", "injunction"],
    "invalid provision": ["severability", "replacement provision"],
    "termination": ["survival", "return", "transition assistance"],
    "amendment": ["written approval", "change control"],
    "failure to enforce": ["rights preserved", "no waiver"],
    "assignment": ["consent required", "void assignment"],
    "export control": ["suspension", "termination", "blocked transaction"],
    "sanctions": ["suspension", "termination", "blocked transaction"],
    "open source": ["license compliance", "replacement", "disclosure"],
    "escrow release condition": ["release", "access", "use rights"],
    "migration": ["handover", "knowledge transfer", "data portability"],

    "force majeure": ["suspension", "extension", "termination"],
    "cas de force majeure": ["suspension", "prolongation", "résiliation"],
    "retenue à la source": ["majoration fiscale", "documentation fiscale"],
    "violation de garantie": ["réparation", "remplacement", "remboursement"],
    "non-paiement": ["suspension", "intérêt", "résiliation"],
    "sanctions": ["suspension", "résiliation", "transaction bloquée"],
    "open source": ["conformité de licence", "remplacement", "divulgation"],

    "القوة القاهرة": ["تعليق", "تمديد", "فسخ"],
    "اقتطاع": ["تعويض ضريبي", "مستندات ضريبية"],
    "خرق الضمان": ["إصلاح", "استبدال", "رد المبلغ"],
    "عدم الدفع": ["تعليق", "فائدة", "فسخ"],
    "عقوبات": ["تعليق", "فسخ", "معاملة محظورة"],
    "مفتوح المصدر": ["امتثال الترخيص", "استبدال", "إفصاح"],
}


def _merge_unique(base: list[str], extra: list[str]) -> list[str]:
    return list(dict.fromkeys([*base, *extra]))


def _extend_international_ontology() -> None:
    for domain, payload in INTERNATIONAL_LEGAL_ONTOLOGY_EXTENSIONS.items():
        existing = LEGAL_ONTOLOGY.setdefault(domain, {"concepts": [], "roles": []})
        existing["concepts"] = _merge_unique(
            existing.get("concepts", []),
            payload.get("concepts", []),
        )
        existing["roles"] = _merge_unique(
            existing.get("roles", []),
            payload.get("roles", []),
        )

    for domain, payload in INTERNATIONAL_LEGAL_RELATIONS.items():
        existing = LEGAL_RELATIONS.setdefault(
            domain,
            {"trigger_terms": [], "consequence_terms": []},
        )
        existing["trigger_terms"] = _merge_unique(
            existing.get("trigger_terms", []),
            payload.get("trigger_terms", []),
        )
        existing["consequence_terms"] = _merge_unique(
            existing.get("consequence_terms", []),
            payload.get("consequence_terms", []),
        )

    for trigger, consequences in INTERNATIONAL_TRIGGER_TO_CONSEQUENCE.items():
        current = LEGAL_TRIGGER_TO_CONSEQUENCE.setdefault(trigger.lower(), [])
        LEGAL_TRIGGER_TO_CONSEQUENCE[trigger.lower()] = _merge_unique(
            current,
            consequences,
        )


_extend_international_ontology()

