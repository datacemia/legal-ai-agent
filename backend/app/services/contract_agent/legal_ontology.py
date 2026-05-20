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

            "résiliation",
            "licenciement",
            "démission",

            "إنهاء",
            "فسخ",
            "استقالة",
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

            "paiement",
            "salaire",
            "prime",

            "دفع",
            "راتب",
            "مكافأة",
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
            "trade secret",

            "confidentialité",
            "secret commercial",

            "السرية",
            "معلومات سرية",
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
            "limitation of liability",

            "responsabilité",
            "dommages",

            "المسؤولية",
            "التعويض",
        ],

        "roles": [
            "financial_exposure",
            "risk_allocation",
            "indemnity",
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

            "droit applicable",
            "juridiction",

            "القانون الواجب التطبيق",
            "الاختصاص",
        ],

        "roles": [
            "forum",
            "dispute_resolution",
            "jurisdiction_selection",
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

    "dispute": [
        "arbitration",
    ],

    "claim": [
        "arbitration",
    ],
}


def get_trigger_consequences(
    trigger: str,
) -> list[str]:

    return LEGAL_TRIGGER_TO_CONSEQUENCE.get(
        str(trigger or "").lower(),
        [],
    )
