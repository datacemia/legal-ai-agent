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

    "governing_law": {
        "label": {
            "en": "Governing Law",
            "fr": "Droit applicable",
            "ar": "القانون الواجب التطبيق",
        },
        "signals": [
            "governing law",
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
}


CLAUSE_PRIORITY_ORDER = [
    "liability",
    "termination",
    "payment",
    "data_protection",
    "sla",
    "indemnity",
    "exclusivity",
    "confidentiality",
    "intellectual_property",
    "maintenance",
    "governing_law",
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


def detect_clause_type_from_taxonomy(text: str) -> str:
    normalized = str(text or "").lower()

    best_type = "other"
    best_score = 0

    for clause_type in CLAUSE_PRIORITY_ORDER:
        definition = CLAUSE_TYPES.get(clause_type, {})

        signals = definition.get(
            "signals",
            [],
        )

        excluded_contexts = definition.get(
            "excluded_contexts",
            [],
        )

        if any(
            excluded.lower() in normalized
            for excluded in excluded_contexts
        ):
            continue

        score = sum(
            1
            for signal in signals
            if signal.lower() in normalized
        )

        if score > best_score:
            best_score = score
            best_type = clause_type

    return best_type


def has_clause_type_signal(
    text: str,
    clause_type: str,
) -> bool:
    normalized = str(text or "").lower()

    return any(
        signal.lower() in normalized
        for signal in get_clause_type_signals(clause_type)
    )


def is_critical_clause_text(text: str) -> bool:
    normalized = str(text or "").lower()

    return any(
        term.lower() in normalized
        for term in get_all_critical_terms()
    )
