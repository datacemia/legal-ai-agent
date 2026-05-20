"""
Central contract taxonomy.

This module centralizes clause type metadata so the contract agent can
reuse the same signals, risk defaults, reasoning keys, and negotiation
triggers across:
- rule-based risk calibration
- clause reasoning templates
- fallback legal insight
- negotiation advice
- frontend labeling

Goal:
Reduce duplicated mappings and keep multilingual clause classification
consistent across 1000+ contracts.
"""


SUPPORTED_LANGUAGES = {"en", "fr", "ar"}


CLAUSE_TYPES = {
    "payment": {
        "label": {
            "en": "Payment",
            "fr": "Paiement",
            "ar": "الدفع",
        },
        "signals": [
            "payment",
            "invoice",
            "fee",
            "fees",
            "pricing",
            "price",
            "interest",
            "late payment",
            "principal amount",
            "loan amount",
            "repayment",

            "paiement",
            "facture",
            "frais",
            "prix",
            "intérêt",
            "retard de paiement",
            "capital",
            "montant du prêt",
            "remboursement",

            "الدفع",
            "السداد",
            "فاتورة",
            "الفاتورة",
            "الرسوم",
            "الأسعار",
            "الفائدة",
            "تأخر الدفع",
            "رأس المال",
            "مبلغ القرض",

            "reimbursement",
            "expense reimbursement",
            "remboursement de frais",
            "استرداد",
            "تعويض المصاريف",

            "expenses",
            "expense statements",
            "vouchers",
            "business expenses",
            "paid by",
            "pay or reimburse",
            "remboursement de dépenses",
            "notes de frais",
            "justificatifs",
            "مصاريف",
            "المصاريف",
            "قسائم",
            "إيصالات",
        ],
        "risk_default": "medium",
        "materiality": "high",
        "reasoning_key": "payment",
        "critical": True,
    },

    "termination": {
        "label": {
            "en": "Termination",
            "fr": "Résiliation",
            "ar": "الإنهاء",
        },
        "signals": [
            "termination",
            "terminate",
            "immediate termination",
            "notice period",
            "cure period",
            "default termination",

            "résiliation",
            "résilier",
            "résiliation immédiate",
            "préavis",
            "délai de régularisation",

            "إنهاء",
            "فسخ",
            "إنهاء فوري",
            "إشعار",
            "مهلة معالجة",
        ],
        "risk_default": "medium",
        "materiality": "high",
        "reasoning_key": "termination",
        "critical": True,
    },

    "liability": {
        "label": {
            "en": "Liability",
            "fr": "Responsabilité",
            "ar": "المسؤولية",
        },
        "signals": [
            "liability",
            "liability cap",
            "limitation of liability",
            "unlimited liability",
            "indirect damages",
            "financial exposure",

            "responsabilité",
            "plafond de responsabilité",
            "limitation de responsabilité",
            "responsabilité illimitée",
            "dommages indirects",
            "exposition financière",

            "المسؤولية",
            "حد المسؤولية",
            "مسؤولية غير محدودة",
            "الأضرار غير المباشرة",
            "تعرض مالي",
        ],
        "risk_default": "medium",
        "materiality": "high",
        "reasoning_key": "liability",
        "negotiation_type": "liability",
        "critical": True,
    },

    "confidentiality": {
        "label": {
            "en": "Confidentiality",
            "fr": "Confidentialité",
            "ar": "السرية",
        },
        "signals": [
            "confidentiality",
            "confidential information",
            "trade secret",
            "survive termination",

            "confidentialité",
            "information confidentielle",
            "secret commercial",

            "السرية",
            "معلومات سرية",
            "سر تجاري",
        ],
        "risk_default": "medium",
        "materiality": "medium",
        "reasoning_key": "confidentiality",
        "critical": True,
    },

    "data_protection": {
        "label": {
            "en": "Data Protection",
            "fr": "Protection des données",
            "ar": "حماية البيانات",
        },
        "signals": [
            "data protection",
            "personal data",
            "gdpr",
            "data breach",
            "security incident",
            "cybersecurity",

            "protection des données",
            "données personnelles",
            "violation de données",
            "incident de sécurité",
            "cybersécurité",

            "حماية البيانات",
            "البيانات الشخصية",
            "اختراق البيانات",
            "حادث أمني",
            "الأمن السيبراني",
        ],
        "risk_default": "medium",
        "materiality": "high",
        "reasoning_key": "data",
        "critical": True,
    },

    "sla": {
        "label": {
            "en": "Service Level",
            "fr": "Niveau de service",
            "ar": "مستوى الخدمة",
        },
        "signals": [
            "service level",
            "sla",
            "uptime",
            "availability",
            "downtime",
            "service credit",

            "niveau de service",
            "disponibilité",
            "interruption",
            "crédit de service",

            "مستوى الخدمة",
            "التوافر",
            "انقطاع الخدمة",
            "تعويض الخدمة",
        ],
        "risk_default": "medium",
        "materiality": "high",
        "reasoning_key": "sla",
        "critical": True,
    },

    "indemnity": {
        "label": {
            "en": "Indemnity",
            "fr": "Indemnisation",
            "ar": "التعويض",
        },
        "signals": [
            "indemnity",
            "indemnify",
            "hold harmless",
            "defend",

            "indemnisation",
            "indemniser",
            "tenir indemne",
            "défendre",

            "تعويض",
            "يعوض",
            "الدفاع عن",

            "indemnification",
            "indemnité",
            "تعويضات",

            "losses",
            "claims",
            "third party claims",
            "réclamations",
            "pertes",
            "إبقاء دون ضرر",
            "مطالبات",
            "خسائر",
        ],
        "risk_default": "medium",
        "materiality": "high",
        "reasoning_key": "indemnity",
        "critical": True,
    },

    "exclusivity": {
        "label": {
            "en": "Exclusivity",
            "fr": "Exclusivité",
            "ar": "الحصرية",
        },
        "signals": [
            "exclusive",
            "exclusivity",
            "sole provider",
            "non-exclusive",
            "territory",

            "exclusif",
            "exclusivité",
            "fournisseur unique",
            "non exclusif",
            "territoire",

            "حصري",
            "حصرية",
            "مزود وحيد",
            "غير حصري",
            "منطقة",
        ],
        "risk_default": "medium",
        "materiality": "high",
        "reasoning_key": "exclusivity",
        "critical": True,
    },

    "remedies": {
        "label": {
            "en": "Remedies",
            "fr": "Recours",
            "ar": "وسائل الانتصاف",
        },
        "signals": [
            "remedies",
            "rights and remedies",
            "specific performance",
            "injunctive relief",
            "equitable relief",
            "irreparable injury",
            "money damages",
            "adequate remedy",

            "recours",
            "droits et recours",
            "exécution forcée",
            "injonction",
            "préjudice irréparable",
            "dommages-intérêts",

            "وسائل الانتصاف",
            "الحقوق ووسائل الانتصاف",
            "التنفيذ العيني",
            "أمر قضائي",
            "ضرر لا يمكن إصلاحه",
            "تعويضات مالية",
        ],
        "risk_default": "medium",
        "materiality": "high",
        "reasoning_key": "liability",
        "critical": True,
    },

    "governing_law": {
        "label": {
            "en": "Governing Law",
            "fr": "Droit applicable",
            "ar": "القانون الواجب التطبيق",
        },
        "signals": [
            "governing law",
            "applicable law",
            "laws of",
            "state of",
            "colorado law",
            "california law",
            "new york law",
            "jurisdiction",
            "venue",
            "courts",

            "droit applicable",
            "juridiction",
            "tribunaux compétents",
            "tribunaux",

            "القانون الواجب التطبيق",
            "الاختصاص",
            "المحاكم",
            "محكمة",
        ],
        "risk_default": "medium",
        "materiality": "high",
        "reasoning_key": "governing_law",
        "critical": True,
    },

    "intellectual_property": {
        "label": {
            "en": "Intellectual Property",
            "fr": "Propriété intellectuelle",
            "ar": "الملكية الفكرية",
        },
        "signals": [
            "intellectual property",
            "ip rights",
            "ownership",
            "assignment",
            "license",

            "propriété intellectuelle",
            "droits de propriété intellectuelle",
            "cession",
            "licence",

            "الملكية الفكرية",
            "حقوق الملكية الفكرية",
            "التنازل",
            "ترخيص",

            "invention",
            "patent",
            "work product",
            "employee invention",
            "brevet",
            "création",
            "اختراع",
            "براءة اختراع",
        ],
        "risk_default": "medium",
        "materiality": "high",
        "reasoning_key": "intellectual_property",
        "critical": True,
    },

    "maintenance": {
        "label": {
            "en": "Maintenance and Repair",
            "fr": "Maintenance et réparation",
            "ar": "الصيانة والإصلاح",
        },
        "signals": [
            "maintenance",
            "repair",

            "maintenance",
            "réparation",
            "réparations",
            "entretien",

            "صيانة",
            "الصيانة",
            "إصلاح",
            "إصلاحات",
            "الإصلاحات",
        ],
        "excluded_contexts": [
            "service level",
            "sla",
            "uptime",
            "payment",
            "pricing",

            "niveau de service",
            "disponibilité",
            "paiement",
            "prix",

            "مستوى الخدمة",
            "الدفع",
            "الأسعار",
        ],
        "risk_default": "medium",
        "materiality": "medium",
        "reasoning_key": "maintenance",
        "critical": True,
    },

    "services": {
        "label": {
            "en": "Services",
            "fr": "Services",
            "ar": "الخدمات",
        },
        "signals": [
            "services",
            "service provider",
            "scope of work",
            "deliverables",
            "support",
            "implementation",
            "consulting",
            "professional services",

            "services",
            "prestations",
            "assistance",
            "livrables",
            "mise en œuvre",
            "conseil",
            "services professionnels",

            "خدمات",
            "نطاق العمل",
            "الدعم",
            "التنفيذ",
            "الاستشارات",
            "الخدمات المهنية",
        ],
        "risk_default": "low",
        "materiality": "medium",
        "reasoning_key": "general",
        "critical": False,
    },

    "employment": {
        "label": {
            "en": "Employment",
            "fr": "Emploi",
            "ar": "العمل",
        },
        "signals": [
            "employee",
            "employer",
            "employment",
            "salary",
            "bonus",
            "benefits",
            "vacation",
            "executive",

            "employé",
            "employeur",
            "emploi",
            "salaire",
            "prime",
            "avantages",
            "congés",

            "موظف",
            "صاحب العمل",
            "عمل",
            "راتب",
            "مكافأة",
            "مزايا",
        ],
        "risk_default": "low",
        "materiality": "medium",
        "reasoning_key": "general",
        "critical": False,
    },

    "corporate_governance": {
        "label": {
            "en": "Corporate Governance",
            "fr": "Gouvernance d'entreprise",
            "ar": "حوكمة الشركات",
        },
        "signals": [
            "board",
            "director",
            "shareholder",
            "approval",
            "consent",
            "voting",
            "corporate governance",

            "conseil",
            "administrateur",
            "actionnaire",
            "approbation",
            "consentement",
            "vote",
            "gouvernance",

            "مجلس الإدارة",
            "مدير",
            "مساهم",
            "موافقة",
            "تصويت",
            "حوكمة",
        ],
        "risk_default": "low",
        "materiality": "medium",
        "reasoning_key": "general",
        "critical": False,
    },

    "real_estate": {
        "label": {
            "en": "Real Estate",
            "fr": "Immobilier",
            "ar": "العقار",
        },
        "signals": [
            "lease",
            "tenant",
            "landlord",
            "rent",
            "premises",
            "property",

            "bail",
            "locataire",
            "bailleur",
            "locaux",
            "bien immobilier",

            "إيجار",
            "مستأجر",
            "مؤجر",
            "أجرة",
            "عقار",
        ],
        "risk_default": "low",
        "materiality": "medium",
        "reasoning_key": "general",
        "critical": False,
    },

    "loan_finance": {
        "label": {
            "en": "Loan and Finance",
            "fr": "Prêt et financement",
            "ar": "القرض والتمويل",
        },
        "signals": [
            "loan",
            "credit",
            "principal",
            "interest",
            "repayment",
            "lender",
            "borrower",

            "prêt",
            "crédit",
            "capital",
            "intérêt",
            "remboursement",
            "prêteur",
            "emprunteur",

            "قرض",
            "ائتمان",
            "رأس المال",
            "فائدة",
            "سداد",
            "مقرض",
            "مقترض",
        ],
        "risk_default": "medium",
        "materiality": "high",
        "reasoning_key": "payment",
        "critical": False,
    },

    "supply_distribution": {
        "label": {
            "en": "Supply and Distribution",
            "fr": "Fourniture et distribution",
            "ar": "التوريد والتوزيع",
        },
        "signals": [
            "supply",
            "supplier",
            "distribution",
            "distributor",
            "reseller",
            "purchase order",
            "delivery",

            "fourniture",
            "fournisseur",
            "distribution",
            "distributeur",
            "revendeur",
            "bon de commande",
            "livraison",

            "توريد",
            "مورد",
            "توزيع",
            "موزع",
            "طلب شراء",
            "تسليم",
        ],
        "risk_default": "low",
        "materiality": "medium",
        "reasoning_key": "general",
        "critical": False,
    },

    "administrative": {
        "label": {
            "en": "Administrative",
            "fr": "Administratif",
            "ar": "إداري",
        },
        "signals": [
            "party identification",
            "definitions",
            "headings",
            "headings for reference only",
            "titles",
            "section headings",
            "interpretation",
            "notice address",
            "for reference only",

            "identification des parties",
            "définitions",
            "adresse de notification",
            "à titre indicatif",

            "تعريف",
            "التعريفات",
            "عنوان الإشعار",
            "لأغراض مرجعية",
        ],
        "risk_default": "low",
        "materiality": "low",
        "reasoning_key": "administrative",
        "critical": False,
    },

    "notice": {
        "label": {
            "en": "Notice",
            "fr": "Notification",
            "ar": "الإشعار",
        },
        "signals": [
            "notice",
            "notices",
            "written notice",
            "notification",
            "notify",

            "avis",
            "notification",
            "préavis",

            "إشعار",
            "إخطار",
            "إبلاغ",
        ],
        "risk_default": "low",
        "materiality": "medium",
        "reasoning_key": "administrative",
        "critical": False,
    },

    "arbitration": {
        "label": {
            "en": "Arbitration",
            "fr": "Arbitrage",
            "ar": "التحكيم",
        },
        "signals": [
            "arbitration",
            "arbitrator",
            "arbitral tribunal",

            "arbitrage",
            "arbitre",
            "tribunal arbitral",

            "تحكيم",
            "محكم",
            "هيئة التحكيم",
        ],
        "risk_default": "medium",
        "materiality": "high",
        "reasoning_key": "governing_law",
        "critical": True,
    },

    "dispute_resolution": {
        "label": {
            "en": "Dispute Resolution",
            "fr": "Résolution des litiges",
            "ar": "تسوية النزاعات",
        },
        "signals": [
            "dispute resolution",
            "dispute",
            "mediation",
            "settlement",

            "résolution des litiges",
            "litige",
            "médiation",
            "règlement",

            "تسوية النزاعات",
            "نزاع",
            "وساطة",
            "تسوية",
        ],
        "risk_default": "medium",
        "materiality": "high",
        "reasoning_key": "governing_law",
        "critical": True,
    },

    "conflict_of_interest": {
        "label": {
            "en": "Conflict of Interest",
            "fr": "Conflit d'intérêt",
            "ar": "تضارب المصالح",
        },
        "signals": [
            "conflict of interest",
            "self dealing",
            "related party",

            "conflit d'intérêt",
            "partie liée",

            "تضارب المصالح",
            "طرف ذو صلة",
        ],
        "risk_default": "medium",
        "materiality": "medium",
        "reasoning_key": "general",
        "critical": False,
    },

    "board_approval": {
        "label": {
            "en": "Board Approval",
            "fr": "Approbation du conseil",
            "ar": "موافقة مجلس الإدارة",
        },
        "signals": [
            "board approval",
            "board consent",
            "director approval",

            "approbation du conseil",
            "consentement du conseil",

            "موافقة مجلس الإدارة",
            "موافقة المديرين",
        ],
        "risk_default": "low",
        "materiality": "medium",
        "reasoning_key": "general",
        "critical": False,
    },

    "change_of_control": {
        "label": {
            "en": "Change of Control",
            "fr": "Changement de contrôle",
            "ar": "تغيير السيطرة",
        },
        "signals": [
            "change of control",
            "acquisition",
            "merger",

            "changement de contrôle",
            "acquisition",
            "fusion",

            "تغيير السيطرة",
            "استحواذ",
            "اندماج",
        ],
        "risk_default": "medium",
        "materiality": "high",
        "reasoning_key": "general",
        "critical": True,
    },

    "equity_compensation": {
        "label": {
            "en": "Equity Compensation",
            "fr": "Rémunération en actions",
            "ar": "التعويض بالأسهم",
        },
        "signals": [
            "stock option",
            "equity compensation",
            "restricted stock",
            "vesting",

            "option d'achat",
            "rémunération en actions",
            "acquisition des droits",

            "خيارات الأسهم",
            "التعويض بالأسهم",
            "الاستحقاق",
        ],
        "risk_default": "medium",
        "materiality": "medium",
        "reasoning_key": "payment",
        "critical": False,
    },

    "assignment": {
        "label": {
            "en": "Assignment",
            "fr": "Cession",
            "ar": "التنازل",
        },
        "signals": [
            "assignment",
            "assign",
            "transfer of rights",

            "cession",
            "transfert de droits",

            "التنازل",
            "نقل الحقوق",
        ],
        "risk_default": "medium",
        "materiality": "medium",
        "reasoning_key": "general",
        "critical": False,
    },

    "force_majeure": {
        "label": {
            "en": "Force Majeure",
            "fr": "Force majeure",
            "ar": "القوة القاهرة",
        },
        "signals": [
            "force majeure",
            "act of god",
            "unforeseeable event",

            "force majeure",
            "cas de force majeure",

            "القوة القاهرة",
            "حدث غير متوقع",
        ],
        "risk_default": "medium",
        "materiality": "high",
        "reasoning_key": "general",
        "critical": True,
    },

    "non_solicitation": {
        "label": {
            "en": "Non-Solicitation",
            "fr": "Non-sollicitation",
            "ar": "عدم الاستقطاب",
        },
        "signals": [
            "non solicitation",
            "non-solicitation",
            "solicit employees",

            "non-sollicitation",
            "solliciter les employés",

            "عدم الاستقطاب",
            "استقطاب الموظفين",
        ],
        "risk_default": "medium",
        "materiality": "medium",
        "reasoning_key": "employment",
        "critical": False,
    },

    "compliance": {
        "label": {
            "en": "Compliance",
            "fr": "Conformité",
            "ar": "الامتثال",
        },
        "signals": [
            "compliance",
            "regulatory",
            "applicable regulations",

            "conformité",
            "réglementation",

            "الامتثال",
            "تنظيمي",
            "اللوائح",
        ],
        "risk_default": "medium",
        "materiality": "high",
        "reasoning_key": "general",
        "critical": True,
    },

    "audit_rights": {
        "label": {
            "en": "Audit Rights",
            "fr": "Droits d'audit",
            "ar": "حقوق التدقيق",
        },
        "signals": [
            "audit rights",
            "audit",
            "inspection rights",

            "droits d'audit",
            "audit",
            "droit d'inspection",

            "حقوق التدقيق",
            "تدقيق",
            "حق التفتيش",
        ],
        "risk_default": "medium",
        "materiality": "medium",
        "reasoning_key": "compliance",
        "critical": False,
    },
}


CLAUSE_PRIORITY_ORDER = [
    # High-impact universal legal clause types first.
    "remedies",
    "liability",
    "termination",
    "change_of_control",

    "conflict_of_interest",

    "intellectual_property",
    "indemnity",
    "assignment",

    "arbitration",
    "dispute_resolution",

    # Payment is important but intentionally kept below
    # more specific legal concepts to avoid over-classification.
    "payment",

    "data_protection",
    "sla",
    "exclusivity",
    "confidentiality",

    "notice",
    "force_majeure",
    "compliance",
    "audit_rights",
    "maintenance",

    # Forum / governing law after remedies and specific legal concepts.
    "governing_law",

    # General business / operational domains second.
    "services",
    "employment",
    "corporate_governance",
    "real_estate",
    "loan_finance",
    "supply_distribution",

    # Fallback / administrative last.
    "administrative",
]


def normalize_language(language: str) -> str:
    language = str(language or "en").lower()

    if language not in SUPPORTED_LANGUAGES:
        return "en"

    return language


def get_clause_type_definition(clause_type: str) -> dict:
    return CLAUSE_TYPES.get(
        str(clause_type or "").lower(),
        {},
    )


def get_clause_type_label(
    clause_type: str,
    language: str = "en",
) -> str:
    language = normalize_language(language)
    definition = get_clause_type_definition(clause_type)

    return definition.get(
        "label",
        {},
    ).get(
        language,
        str(clause_type or "other"),
    )


def get_clause_type_signals(clause_type: str) -> list[str]:
    definition = get_clause_type_definition(clause_type)

    return list(
        definition.get(
            "signals",
            [],
        )
    )


def get_all_critical_terms() -> list[str]:
    terms = []

    for definition in CLAUSE_TYPES.values():
        if not definition.get("critical"):
            continue

        terms.extend(
            definition.get(
                "signals",
                [],
            )
        )

    return dedupe_terms(terms)


def get_reasoning_key_for_clause_type(
    clause_type: str,
) -> str:
    definition = get_clause_type_definition(clause_type)

    return definition.get(
        "reasoning_key",
        "general",
    )


def get_risk_default_for_clause_type(
    clause_type: str,
) -> str:
    definition = get_clause_type_definition(clause_type)

    return definition.get(
        "risk_default",
        "low",
    )


def get_materiality_for_clause_type(
    clause_type: str,
) -> str:
    definition = get_clause_type_definition(clause_type)

    return definition.get(
        "materiality",
        "low",
    )


def get_excluded_contexts_for_clause_type(
    clause_type: str,
) -> list[str]:
    definition = get_clause_type_definition(clause_type)

    return list(
        definition.get(
            "excluded_contexts",
            [],
        )
    )


def dedupe_terms(terms: list[str]) -> list[str]:
    seen = set()
    output = []

    for term in terms:
        normalized = str(term or "").strip()

        if not normalized:
            continue

        lowered = normalized.lower()

        if lowered in seen:
            continue

        seen.add(lowered)
        output.append(normalized)

    return output



SIGNAL_WEIGHTS = {
    # Indemnity / claims: highly specific.
    "indemnity": 5,
    "indemnification": 5,
    "indemnify": 5,
    "hold harmless": 5,
    "third party claims": 5,
    "claims": 4,
    "losses": 4,

    "indemnisation": 5,
    "indemniser": 5,
    "tenir indemne": 5,
    "réclamations": 4,
    "pertes": 4,

    "تعويضات": 5,
    "مطالبات": 4,
    "خسائر": 4,
    "إبقاء دون ضرر": 5,

    # Remedies: highly specific.
    "rights and remedies": 5,
    "specific performance": 5,
    "injunctive relief": 5,
    "equitable relief": 4,
    "irreparable injury": 5,
    "adequate remedy": 4,

    "droits et recours": 5,
    "exécution forcée": 5,
    "injonction": 5,
    "préjudice irréparable": 5,

    "الحقوق ووسائل الانتصاف": 5,
    "التنفيذ العيني": 5,
    "أمر قضائي": 5,
    "ضرر لا يمكن إصلاحه": 5,

    # IP: highly specific.
    "intellectual property": 5,
    "ip rights": 5,
    "invention": 5,
    "patent": 5,
    "work product": 4,
    "employee invention": 5,

    "propriété intellectuelle": 5,
    "droits de propriété intellectuelle": 5,
    "brevet": 5,
    "création": 4,

    "الملكية الفكرية": 5,
    "حقوق الملكية الفكرية": 5,
    "اختراع": 5,
    "براءة اختراع": 5,

    # Conflict / governance specific.
    "conflict of interest": 5,
    "self dealing": 5,
    "related party": 4,
    "conflit d'intérêt": 5,
    "partie liée": 4,
    "تضارب المصالح": 5,
    "طرف ذو صلة": 4,

    # Payment: important but often generic.
    "payment": 2,
    "pay": 2,
    "paid by": 2,
    "invoice": 3,
    "fee": 1,
    "fees": 1,
    "reimbursement": 4,
    "expense reimbursement": 5,
    "pay or reimburse": 5,
    "expenses": 3,
    "expense statements": 4,
    "vouchers": 3,

    "paiement": 2,
    "facture": 3,
    "frais": 2,
    "remboursement": 4,
    "remboursement de frais": 5,
    "notes de frais": 4,

    "الدفع": 2,
    "السداد": 2,
    "فاتورة": 3,
    "الرسوم": 2,
    "تعويض المصاريف": 5,
    "مصاريف": 3,
    "المصاريف": 3,
}


TYPE_SPECIFICITY_BONUS = {
    # More specific legal concepts get a modest bonus.
    "remedies": 4,
    "indemnity": 4,
    "intellectual_property": 4,
    "conflict_of_interest": 4,
    "assignment": 3,
    "change_of_control": 3,
    "arbitration": 3,
    "dispute_resolution": 3,
    "data_protection": 3,
    "liability": 3,
    "termination": 3,
    "notice": 2,
    "maintenance": 2,

    # Broad categories get no bonus.
    "payment": 0,
    "services": 0,
    "employment": 0,
    "corporate_governance": 0,
    "governing_law": 0,
    "administrative": 0,
}



TYPE_CONTEXT_ANCHORS = {
    "employment": [
        "employee",
        "employer",
        "employment",
        "salary",
        "bonus",
        "benefits",
        "vacation",
        "position",
        "duties",
        "executive",

        "employé",
        "employeur",
        "emploi",
        "salaire",
        "prime",
        "avantages",
        "congés",
        "poste",
        "fonctions",

        "موظف",
        "صاحب العمل",
        "عمل",
        "راتب",
        "مكافأة",
        "مزايا",
        "إجازة",
        "منصب",
        "مهام",
    ],
    "corporate_governance": [
        "board",
        "director",
        "shareholder",
        "voting",
        "governance",
        "committee",
        "board approval",
        "board consent",

        "conseil",
        "administrateur",
        "actionnaire",
        "vote",
        "gouvernance",
        "comité",

        "مجلس الإدارة",
        "مدير",
        "مساهم",
        "تصويت",
        "حوكمة",
        "لجنة",
    ],
    "services": [
        "services",
        "service provider",
        "scope of work",
        "deliverables",
        "support",
        "implementation",
        "consulting",

        "services",
        "prestations",
        "assistance",
        "livrables",
        "mise en œuvre",
        "conseil",

        "خدمات",
        "نطاق العمل",
        "الدعم",
        "التنفيذ",
        "الاستشارات",
    ],
    "payment": [
        "payment",
        "pay",
        "invoice",
        "fees",
        "salary",
        "bonus",
        "reimbursement",
        "expense reimbursement",

        "paiement",
        "payer",
        "facture",
        "frais",
        "salaire",
        "prime",
        "remboursement",

        "الدفع",
        "السداد",
        "فاتورة",
        "الرسوم",
        "راتب",
        "مكافأة",
        "تعويض المصاريف",
    ],
}


TYPE_CONTEXT_PENALTIES = {
    # Services must not dominate employment clauses just because they mention duties or work.
    "services": [
        "employee",
        "employer",
        "employment",
        "salary",
        "bonus",
        "benefits",
        "vacation",

        "employé",
        "employeur",
        "emploi",
        "salaire",
        "prime",
        "avantages",
        "congés",

        "موظف",
        "صاحب العمل",
        "عمل",
        "راتب",
        "مكافأة",
        "مزايا",
    ],

    # Corporate governance must not dominate employment clauses unless board/director/shareholder anchors are strong.
    "corporate_governance": [
        "employee",
        "employer",
        "employment",
        "salary",
        "benefits",
        "vacation",

        "employé",
        "employeur",
        "emploi",
        "salaire",
        "avantages",
        "congés",

        "موظف",
        "صاحب العمل",
        "عمل",
        "راتب",
        "مزايا",
    ],

    # Payment should not dominate highly specific indemnity/IP/remedies clauses.
    "payment": [
        "indemnification",
        "indemnity",
        "hold harmless",
        "third party claims",
        "specific performance",
        "injunctive relief",
        "invention",
        "patent",

        "indemnisation",
        "tenir indemne",
        "réclamations",
        "exécution forcée",
        "injonction",
        "brevet",

        "تعويضات",
        "مطالبات",
        "التنفيذ العيني",
        "أمر قضائي",
        "اختراع",
        "براءة اختراع",
    ],
}


def count_context_matches(
    text: str,
    terms: list[str],
) -> int:
    normalized = str(text or "").lower()

    return sum(
        1
        for term in terms
        if term.lower() in normalized
    )


def context_bonus_for_clause_type(
    text: str,
    clause_type: str,
) -> int:
    matches = count_context_matches(
        text,
        TYPE_CONTEXT_ANCHORS.get(clause_type, []),
    )

    if matches >= 3:
        return 4

    if matches == 2:
        return 2

    if matches == 1:
        return 1

    return 0


def context_penalty_for_clause_type(
    text: str,
    clause_type: str,
) -> int:
    matches = count_context_matches(
        text,
        TYPE_CONTEXT_PENALTIES.get(clause_type, []),
    )

    if matches >= 3:
        return 4

    if matches == 2:
        return 2

    if matches == 1:
        return 1

    return 0


def score_clause_type(
    text: str,
    clause_type: str,
) -> dict:
    normalized = str(text or "").lower()
    definition = CLAUSE_TYPES.get(clause_type, {})

    signals = definition.get(
        "signals",
        [],
    )

    excluded_contexts = definition.get(
        "excluded_contexts",
        [],
    )

    matched_signals = []

    if any(
        excluded.lower() in normalized
        for excluded in excluded_contexts
    ):
        return {
            "type": clause_type,
            "score": 0,
            "base_score": 0,
            "context_bonus": 0,
            "context_penalty": 0,
            "signals": [],
            "excluded": True,
        }

    base_score = 0

    for signal in signals:
        signal_normalized = signal.lower()

        if signal_normalized in normalized:
            matched_signals.append(signal)
            base_score += SIGNAL_WEIGHTS.get(
                signal_normalized,
                1,
            )

    specificity_bonus = 0

    if matched_signals:
        specificity_bonus = TYPE_SPECIFICITY_BONUS.get(
            clause_type,
            0,
        )

    context_bonus = context_bonus_for_clause_type(
        text,
        clause_type,
    )

    context_penalty = context_penalty_for_clause_type(
        text,
        clause_type,
    )

    score = max(
        0,
        base_score
        + specificity_bonus
        + context_bonus
        - context_penalty,
    )

    return {
        "type": clause_type,
        "score": score,
        "base_score": base_score,
        "specificity_bonus": specificity_bonus,
        "context_bonus": context_bonus,
        "context_penalty": context_penalty,
        "signals": dedupe_terms(matched_signals),
        "excluded": False,
    }


def detect_clause_type_candidates(
    text: str,
) -> list[dict]:
    candidates = []

    for clause_type in CLAUSE_PRIORITY_ORDER:
        candidate = score_clause_type(
            text,
            clause_type,
        )

        if candidate.get("score", 0) > 0:
            candidates.append(candidate)

    candidates.sort(
        key=lambda item: (
            item.get("score", 0),
            -CLAUSE_PRIORITY_ORDER.index(item.get("type")),
        ),
        reverse=True,
    )

    return candidates


def select_best_clause_type(
    candidates: list[dict],
) -> str:
    if not candidates:
        return "other"

    strong_candidates = [
        candidate
        for candidate in candidates
        if candidate.get("score", 0) > 0
    ]

    if not strong_candidates:
        return "other"

    strong_candidates.sort(
        key=lambda item: (
            item.get("score", 0),
            TYPE_SPECIFICITY_BONUS.get(item.get("type"), 0),
            -CLAUSE_PRIORITY_ORDER.index(item.get("type")),
        ),
        reverse=True,
    )

    return strong_candidates[0].get(
        "type",
        "other",
    )


def detect_clause_type_from_taxonomy(text: str) -> str:
    candidates = detect_clause_type_candidates(text)

    return select_best_clause_type(candidates)


def has_clause_type_signal(
    text: str,
    clause_type: str,
) -> bool:
    candidate = score_clause_type(
        text,
        clause_type,
    )

    return candidate.get("score", 0) > 0



def detect_secondary_clause_types(
    text: str,
    limit: int = 3,
) -> list[str]:
    candidates = detect_clause_type_candidates(text)
    primary = select_best_clause_type(candidates)

    secondary = []

    for candidate in candidates:
        clause_type = candidate.get("type")

        if clause_type == primary:
            continue

        if candidate.get("score", 0) <= 0:
            continue

        secondary.append(clause_type)

        if len(secondary) >= limit:
            break

    return secondary


def detect_clause_type_labels(
    text: str,
    max_secondary: int = 3,
) -> dict:

    candidates = detect_clause_type_candidates(text)

    primary = select_best_clause_type(candidates)

    secondary = []

    for candidate in candidates:
        clause_type = candidate.get("type")

        if clause_type == primary:
            continue

        score = candidate.get("score", 0)

        if score >= 2:
            secondary.append(clause_type)

        if len(secondary) >= max_secondary:
            break

    return {
        "primary_type": primary,
        "secondary_types": secondary,
        "candidates": candidates,
    }


def is_critical_clause_text(text: str) -> bool:
    normalized = str(text or "").lower()

    return any(
        term.lower() in normalized
        for term in get_all_critical_terms()
    )
