def extract_obligations_from_clause(
    clause: dict,
    language: str = "en",
) -> list[dict]:

    text = " ".join([
        str(clause.get("clause_title", "")),
        str(clause.get("quoted_text", "")),
        str(clause.get("explanation_simple", "")),
        str(clause.get("legal_insight", "")),
    ]).lower()

    obligations = []

    obligation_patterns = [
        {
            "type": "payment",
            "signals": ["payment", "pay", "invoice", "rent", "paiement", "loyer", "الدفع", "يدفع", "الكراء"],
            "party": {"en": "paying party", "fr": "partie payeuse", "ar": "الطرف الملزم بالدفع"},
            "obligation": {"en": "make payment", "fr": "effectuer le paiement", "ar": "أداء المبلغ المستحق"},
        },
        {
            "type": "confidentiality",
            "signals": ["confidentiality", "confidential", "confidentialité", "السرية", "سرية"],
            "party": {"en": "receiving party", "fr": "partie destinataire", "ar": "الطرف المتلقي للمعلومات"},
            "obligation": {"en": "protect confidential information", "fr": "protéger les informations confidentielles", "ar": "حماية المعلومات السرية"},
        },
        {
            "type": "termination",
            "signals": ["termination", "terminate", "résiliation", "فسخ", "إنهاء"],
            "party": {"en": "terminating party", "fr": "partie résiliante", "ar": "الطرف الذي ينهي العقد"},
            "obligation": {"en": "follow termination conditions", "fr": "respecter les conditions de résiliation", "ar": "احترام شروط إنهاء العقد"},
        },
        {
            "type": "data_protection",
            "signals": ["data protection", "personal data", "gdpr", "données", "حماية البيانات", "البيانات"],
            "party": {"en": "data processor/provider", "fr": "prestataire ou sous-traitant", "ar": "مقدم الخدمة أو معالج البيانات"},
            "obligation": {"en": "protect personal or client data", "fr": "protéger les données personnelles ou client", "ar": "حماية البيانات الشخصية أو بيانات العميل"},
        },
        {
            "type": "maintenance",
            "signals": ["maintenance", "repair", "entretien", "réparation", "الصيانة", "الإصلاح"],
            "party": {"en": "responsible party", "fr": "partie responsable", "ar": "الطرف المسؤول"},
            "obligation": {"en": "perform maintenance or repairs", "fr": "assurer l'entretien ou les réparations", "ar": "تنفيذ الصيانة أو الإصلاحات"},
        },
    ]

    for pattern in obligation_patterns:
        if any(signal in text for signal in pattern["signals"]):
            obligations.append({
                "type": pattern["type"],
                "party": pattern["party"].get(language, pattern["party"]["en"]),
                "obligation": pattern["obligation"].get(language, pattern["obligation"]["en"]),
                "trigger": "",
                "deadline": "",
                "consequence": "",
                "confidence": "medium",
            })

    return obligations


def extract_contract_obligations(
    clauses: list[dict],
    language: str = "en",
) -> list[dict]:

    obligations = []

    for clause in clauses:
        clause_obligations = extract_obligations_from_clause(
            clause,
            language,
        )

        for obligation in clause_obligations:
            obligation["source_clause"] = clause.get(
                "clause_title",
                "",
            )
            obligations.append(obligation)

    return obligations