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


def extract_deadline(text: str) -> str:
    patterns = [
        r"within\s+\d+\s+(days?|months?|years?)",
        r"\d+\s+(days?|months?|years?)",
        r"notice period",
        r"cure period",
        r"due date",
        r"dans\s+un\s+délai\s+de\s+\d+\s+jours?",
        r"\d+\s+jours?",
        r"préavis",
        r"délai de régularisation",
        r"date d['’]échéance",
        r"خلال\s+\d+\s+يوم",
        r"\d+\s+يوماً",
        r"\d+\s+يوم",
        r"مهلة",
        r"إشعار",
    ]

    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            return match.group(0)

    return ""


TRIGGER_SIGNALS = {
    "payment": [
        "invoice", "delivery", "milestone", "due date",
        "expense statement", "voucher",
        "facture", "livraison", "jalon", "échéance",
        "note de frais", "justificatif",
        "فاتورة", "تسليم", "مرحلة", "استحقاق", "إيصال",
    ],
    "termination": [
        "breach", "default", "material breach", "non-payment",
        "failure to perform", "notice",
        "manquement", "défaut", "violation substantielle",
        "non-paiement", "préavis",
        "إخلال", "تقصير", "إخلال جوهري", "عدم الدفع", "إشعار",
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
        "données personnelles", "violation de données",
        "incident de sécurité", "traitement",
        "البيانات الشخصية", "اختراق البيانات", "حادث أمني", "معالجة",
    ],
    "maintenance": [
        "repair", "maintenance request", "defect", "damage",
        "réparation", "demande de maintenance", "défaut", "dommage",
        "إصلاح", "طلب صيانة", "عيب", "ضرر",
    ],
    "intellectual_property": [
        "invention", "patent", "work product", "assignment",
        "invention", "brevet", "création", "cession",
        "اختراع", "براءة اختراع", "تنازل",
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
        "résiliation", "indemnité", "dommages", "suspension",
        "إنهاء", "تعويض", "أضرار", "تعليق",
    ],
    "confidentiality": [
        "damages", "injunction", "termination",
        "dommages", "injonction", "résiliation",
        "تعويض", "أمر قضائي", "فسخ",
    ],
    "data_protection": [
        "liability", "notification", "remediation", "penalty",
        "responsabilité", "notification", "correction", "pénalité",
        "مسؤولية", "إخطار", "معالجة", "غرامة",
    ],
    "maintenance": [
        "repair", "replacement", "costs", "termination",
        "réparation", "remplacement", "coûts", "résiliation",
        "إصلاح", "استبدال", "تكاليف", "فسخ",
    ],
    "intellectual_property": [
        "assignment", "license", "ownership", "damages",
        "cession", "licence", "propriété", "dommages",
        "تنازل", "ترخيص", "ملكية", "تعويض",
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


def extract_obligations_from_clause(
    clause: dict,
    language: str = "en",
) -> list[dict]:

    language = normalize_language(language)

    text = normalize_text(" ".join([
        str(clause.get("clause_title", "")),
        str(clause.get("quoted_text", "")),
        str(clause.get("explanation_simple", "")),
        str(clause.get("legal_insight", "")),
    ]))

    obligations = []

    obligation_patterns = [
        {
            "type": "payment",
            "signals": [
                "payment", "pay", "invoice", "rent", "reimbursement",
                "expense reimbursement", "expenses", "fees", "paid by",
                "paiement", "loyer", "remboursement", "frais", "facture",
                "الدفع", "يدفع", "الكراء", "السداد", "المصاريف",
                "تعويض المصاريف", "فاتورة",
            ],
            "party": {
                "en": "paying party",
                "fr": "partie payeuse",
                "ar": "الطرف الملزم بالدفع",
            },
            "obligation": {
                "en": "make payment or reimbursement when due",
                "fr": "effectuer le paiement ou le remboursement à l'échéance",
                "ar": "أداء المبلغ أو تعويض المصاريف عند الاستحقاق",
            },
        },
        {
            "type": "confidentiality",
            "signals": [
                "confidentiality", "confidential", "trade secret",
                "non-disclosure",
                "confidentialité", "information confidentielle",
                "secret commercial",
                "السرية", "سرية", "معلومات سرية", "سر تجاري",
            ],
            "party": {
                "en": "receiving party",
                "fr": "partie destinataire",
                "ar": "الطرف المتلقي للمعلومات",
            },
            "obligation": {
                "en": "protect confidential information and avoid unauthorized disclosure",
                "fr": "protéger les informations confidentielles et éviter toute divulgation non autorisée",
                "ar": "حماية المعلومات السرية وتجنب الإفصاح غير المصرح به",
            },
        },
        {
            "type": "termination",
            "signals": [
                "termination", "terminate", "default", "breach",
                "material breach", "cure period", "notice period",
                "résiliation", "résilier", "manquement",
                "violation substantielle", "préavis",
                "فسخ", "إنهاء", "إخلال", "إخلال جوهري", "إشعار",
            ],
            "party": {
                "en": "terminating party",
                "fr": "partie résiliante",
                "ar": "الطرف الذي ينهي العقد",
            },
            "obligation": {
                "en": "follow termination conditions, notice requirements, and cure periods",
                "fr": "respecter les conditions de résiliation, les exigences de préavis et les délais de régularisation",
                "ar": "احترام شروط الإنهاء ومتطلبات الإشعار ومهل المعالجة",
            },
        },
        {
            "type": "data_protection",
            "signals": [
                "data protection", "personal data", "gdpr",
                "data breach", "security incident",
                "protection des données", "données personnelles",
                "violation de données", "incident de sécurité",
                "حماية البيانات", "البيانات الشخصية",
                "اختراق البيانات", "حادث أمني",
            ],
            "party": {
                "en": "data processor/provider",
                "fr": "prestataire ou sous-traitant",
                "ar": "مقدم الخدمة أو معالج البيانات",
            },
            "obligation": {
                "en": "protect personal, client, or regulated data",
                "fr": "protéger les données personnelles, client ou réglementées",
                "ar": "حماية البيانات الشخصية أو بيانات العميل أو البيانات المنظمة",
            },
        },
        {
            "type": "maintenance",
            "signals": [
                "maintenance", "repair", "defect",
                "entretien", "réparation", "défaut",
                "الصيانة", "الإصلاح", "عيب",
            ],
            "party": {
                "en": "responsible party",
                "fr": "partie responsable",
                "ar": "الطرف المسؤول",
            },
            "obligation": {
                "en": "perform maintenance or repairs when required",
                "fr": "assurer l'entretien ou les réparations lorsque requis",
                "ar": "تنفيذ الصيانة أو الإصلاحات عند الاقتضاء",
            },
        },
        {
            "type": "intellectual_property",
            "signals": [
                "intellectual property", "invention", "patent",
                "work product", "assignment", "license",
                "propriété intellectuelle", "invention", "brevet",
                "création", "cession", "licence",
                "الملكية الفكرية", "اختراع", "براءة اختراع",
                "تنازل", "ترخيص",
            ],
            "party": {
                "en": "creating or assigning party",
                "fr": "partie créatrice ou cédante",
                "ar": "الطرف المنشئ أو المتنازل",
            },
            "obligation": {
                "en": "respect ownership, assignment, or license conditions for intellectual property",
                "fr": "respecter les conditions de propriété, de cession ou de licence de la propriété intellectuelle",
                "ar": "احترام شروط الملكية أو التنازل أو الترخيص المتعلقة بالملكية الفكرية",
            },
        },
        {
            "type": "indemnity",
            "signals": [
                "indemnity", "indemnification", "indemnify",
                "hold harmless", "claims", "losses",
                "indemnisation", "indemniser", "tenir indemne",
                "réclamations", "pertes",
                "تعويض", "تعويضات", "مطالبات", "خسائر",
            ],
            "party": {
                "en": "indemnifying party",
                "fr": "partie indemnisante",
                "ar": "الطرف الملتزم بالتعويض",
            },
            "obligation": {
                "en": "indemnify or protect the other party against covered claims or losses",
                "fr": "indemniser ou protéger l'autre partie contre les réclamations ou pertes couvertes",
                "ar": "تعويض أو حماية الطرف الآخر من المطالبات أو الخسائر المشمولة",
            },
        },
        {
            "type": "notice",
            "signals": [
                "notice", "written notice", "notification", "notify",
                "avis", "notification", "préavis", "notifier",
                "إشعار", "إخطار", "إبلاغ",
            ],
            "party": {
                "en": "notifying party",
                "fr": "partie notificatrice",
                "ar": "الطرف المرسل للإشعار",
            },
            "obligation": {
                "en": "send notices using the required method and address",
                "fr": "envoyer les notifications selon la méthode et l'adresse requises",
                "ar": "إرسال الإشعارات بالطريقة والعنوان المطلوبين",
            },
        },
    ]

    for pattern in obligation_patterns:
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
        clause_obligations = extract_obligations_from_clause(
            clause,
            language,
        )

        for obligation in clause_obligations:
            obligation["source_clause"] = clause.get(
                "clause_title",
                clause.get("title", ""),
            )
            obligations.append(obligation)

    return obligations
