NEGOTIATION_TEMPLATES = {
    "liability": {
        "en": "Consider negotiating liability caps, carve-outs for serious breaches, and clearer exclusions for indirect or consequential damages.",
        "fr": "Envisager de négocier les plafonds de responsabilité, les exceptions pour les violations graves et les exclusions relatives aux dommages indirects ou consécutifs.",
        "ar": "يمكن التفاوض على حدود المسؤولية، والاستثناءات الخاصة بالإخلالات الجسيمة، وتوضيح استبعاد الأضرار غير المباشرة أو التبعية.",
    },
    "confidentiality": {
        "en": "Consider narrowing the scope of confidential information and limiting the duration of post-termination confidentiality obligations.",
        "fr": "Envisager de restreindre le périmètre des informations confidentielles et de limiter la durée des obligations de confidentialité après la fin du contrat.",
        "ar": "يمكن التفاوض على تضييق نطاق المعلومات السرية وتحديد مدة الالتزام بالسرية بعد انتهاء العقد.",
    },
    "termination": {
        "en": "Consider negotiating longer cure periods, clearer breach definitions, and reciprocal termination rights.",
        "fr": "Envisager de négocier des délais de régularisation plus longs, des définitions plus précises des manquements et des droits de résiliation réciproques.",
        "ar": "يمكن التفاوض على تمديد مهلة المعالجة، وتوضيح حالات الإخلال، وإضافة حقوق إنهاء متبادلة.",
    },
    "payment": {
        "en": "Consider negotiating payment deadlines, grace periods, late-payment interest, and suspension rights.",
        "fr": "Envisager de négocier les délais de paiement, les délais de grâce, les intérêts de retard et les droits de suspension.",
        "ar": "يمكن التفاوض على آجال الدفع، وفترات السماح، وفوائد التأخير، وحقوق تعليق الخدمة أو الالتزامات.",
    },
    "data_protection": {
        "en": "Consider clarifying security measures, breach notification timelines, audit rights, and data processing responsibilities.",
        "fr": "Envisager de clarifier les mesures de sécurité, les délais de notification des violations, les droits d’audit et les responsabilités de traitement des données.",
        "ar": "يمكن التفاوض على توضيح تدابير الأمن، ومهل الإشعار بالاختراقات، وحقوق التدقيق، ومسؤوليات معالجة البيانات.",
    },
    "service_level": {
        "en": "Consider negotiating measurable uptime commitments, service credits, exclusions, reporting duties, and escalation procedures.",
        "fr": "Envisager de négocier des engagements de disponibilité mesurables, des crédits de service, des exclusions, des obligations de reporting et des procédures d’escalade.",
        "ar": "يمكن التفاوض على التزامات توفر قابلة للقياس، وائتمانات خدمة، والاستثناءات، والتقارير، وإجراءات التصعيد.",
    },
    "governing_law": {
        "en": "Consider negotiating the governing law, dispute forum, arbitration mechanism, venue, and language of proceedings.",
        "fr": "Envisager de négocier la loi applicable, le tribunal compétent, le mécanisme d’arbitrage, le lieu de règlement des litiges et la langue de procédure.",
        "ar": "يمكن التفاوض على القانون الواجب التطبيق، والجهة المختصة، وآلية التحكيم، ومكان النزاع، ولغة الإجراءات.",
    },
    "intellectual_property": {
        "en": "Consider clarifying ownership, permitted use, licensing scope, approval rights, and post-termination restrictions.",
        "fr": "Envisager de clarifier la propriété, les usages autorisés, l’étendue de la licence, les droits d’approbation et les restrictions après la fin du contrat.",
        "ar": "يمكن التفاوض على توضيح الملكية، والاستخدامات المسموح بها، ونطاق الترخيص، وحقوق الموافقة، والقيود بعد انتهاء العقد.",
    },
}


def detect_negotiation_type(text: str) -> str | None:
    normalized = str(text or "").lower()

    ordered_signals = [
        (
            "liability",
            [
                "limitation of liability",
                "liability cap",
                "liability",
                "responsabilité",
                "limitation de responsabilité",
                "المسؤولية",
                "تحديد المسؤولية",
            ],
        ),
        (
            "data_protection",
            [
                "data protection",
                "personal data",
                "security measures",
                "breach notification",
                "protection des données",
                "données personnelles",
                "mesures de sécurité",
                "حماية البيانات",
                "البيانات",
                "الأمن السيبراني",
            ],
        ),
        (
            "service_level",
            [
                "service level",
                "uptime",
                "availability",
                "service credits",
                "niveau de service",
                "disponibilité",
                "مستوى الخدمة",
                "التوفر",
            ],
        ),
        (
            "confidentiality",
            [
                "confidentiality",
                "confidential information",
                "confidentialité",
                "informations confidentielles",
                "السرية",
                "معلومات سرية",
            ],
        ),
        (
            "termination",
            [
                "termination",
                "terminate",
                "cure period",
                "material breach",
                "résiliation",
                "préavis",
                "manquement",
                "فسخ",
                "إنهاء",
                "إشعار",
                "إخلال جوهري",
            ],
        ),
        (
            "payment",
            [
                "payment",
                "fees",
                "invoice",
                "late payment",
                "rent",
                "paiement",
                "loyer",
                "facture",
                "intérêts de retard",
                "الدفع",
                "الرسوم",
                "الفاتورة",
                "فوائد التأخير",
                "الكراء",
                "السداد",
            ],
        ),
        (
            "governing_law",
            [
                "governing law",
                "jurisdiction",
                "arbitration",
                "droit applicable",
                "tribunal compétent",
                "arbitrage",
                "القانون الواجب التطبيق",
                "المحكمة المختصة",
                "التحكيم",
            ],
        ),
        (
            "intellectual_property",
            [
                "intellectual property",
                "trademark",
                "license",
                "propriété intellectuelle",
                "marque",
                "licence",
                "الملكية الفكرية",
                "العلامات التجارية",
                "ترخيص",
            ],
        ),
    ]

    for negotiation_type, signals in ordered_signals:
        if any(signal in normalized for signal in signals):
            return negotiation_type

    return None


def get_semantic_negotiation(
    clause: dict,
    language: str = "en",
) -> str:
    text = " ".join([
        str(clause.get("clause_title", "")),
        str(clause.get("title", "")),
        str(clause.get("quoted_text", "")),
        str(clause.get("explanation_simple", "")),
        str(clause.get("legal_insight", "")),
    ])

    negotiation_type = detect_negotiation_type(text)

    if not negotiation_type:
        return ""

    template = NEGOTIATION_TEMPLATES.get(
        negotiation_type,
        {},
    )

    return template.get(language, template.get("en", ""))