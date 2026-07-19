import re


SUPPORTED_LANGUAGES = {"en", "fr", "ar"}


TIME_PATTERNS = [
    # English
    r"\b\d+\s+calendar\s+days?\b",
    r"\b\d+\s+business\s+days?\b",
    r"\b\d+\s+working\s+days?\b",
    r"\b\d+\s+days?\b",
    r"\b\d+\s+weeks?\b",
    r"\b\d+\s+months?\b",
    r"\b\d+\s+years?\b",
    r"\b\d+\s+hours?\b",
    r"\bannually\b",
    r"\bquarterly\b",
    r"\bmonthly\b",
    r"\bweekly\b",

    # French
    r"\b\d+\s+jours?\s+calendaires?\b",
    r"\b\d+\s+jours?\s+ouvrables?\b",
    r"\b\d+\s+jours?\s+ouvrés?\b",
    r"\b\d+\s+jours?\b",
    r"\b\d+\s+semaines?\b",
    r"\b\d+\s+mois\b",
    r"\b\d+\s+ans?\b",
    r"\b\d+\s+heures?\b",
    r"\bannuellement\b",
    r"\btrimestriellement\b",
    r"\bmensuellement\b",
    r"\bhebdomadairement\b",

    # Arabic
    r"\d+\s*يوم(?:اً|ا)?",
    r"\d+\s*أيام",
    r"\d+\s*أسبوع",
    r"\d+\s*أسابيع",
    r"\d+\s*شهر",
    r"\d+\s*أشهر",
    r"\d+\s*سنة",
    r"\d+\s*سنوات",
    r"\d+\s*ساعة",
    r"سنوياً",
    r"سنويًا",
    r"ربع\s*سنوي",
    r"شهرياً",
    r"شهريًا",
    r"أسبوعياً",
    r"أسبوعيًا",
]


EVENT_SIGNALS = {
    "payment": [
        "payment", "invoice", "rent", "fee", "fees", "price",
        "paiement", "loyer", "facture", "frais", "prix",
        "الدفع", "السداد", "الكراء", "فاتورة", "رسوم", "ثمن",
    ],
    "termination": [
        "termination", "terminate", "cure period", "breach",
        "résiliation", "résilier", "délai de régularisation", "manquement",
        "فسخ", "إنهاء", "مهلة معالجة", "إخلال",
    ],
    "notice": [
        "notice", "written notice", "prior notice", "notification",
        "préavis", "avis écrit", "notification",
        "إشعار", "إخطار", "إشعار خطي",
    ],
    "renewal": [
        "renewal", "renew", "automatic renewal", "non-renewal",
        "renouvellement", "renouveler", "renouvellement automatique",
        "تجديد", "التجديد التلقائي", "عدم التجديد",
    ],
    "confidentiality": [
        "confidentiality", "confidential", "trade secret", "survive",
        "confidentialité", "information confidentielle", "secret commercial", "survie",
        "السرية", "سرية", "سر تجاري", "تستمر",
    ],
    "data_protection": [
        "personal data", "data protection", "security incident", "data breach",
        "breach notification", "subprocessor",
        "données personnelles", "protection des données", "incident de sécurité",
        "violation de données", "sous-traitant",
        "البيانات الشخصية", "حماية البيانات", "حادث أمني",
        "اختراق البيانات", "معالج فرعي",
    ],
    "delivery_acceptance": [
        "delivery", "deliverable", "acceptance", "acceptance criteria",
        "milestone", "testing",
        "livraison", "livrable", "acceptation", "réception",
        "critères d'acceptation", "jalon", "test",
        "تسليم", "مخرج", "قبول", "معايير القبول", "مرحلة", "اختبار",
    ],
    "audit": [
        "audit", "inspection", "records", "access to records",
        "audit", "inspection", "registres", "accès aux registres",
        "تدقيق", "تفتيش", "سجلات", "الوصول إلى السجلات",
    ],
    "insurance": [
        "insurance", "policy", "coverage", "certificate of insurance",
        "assurance", "police", "couverture", "attestation d'assurance",
        "تأمين", "وثيقة التأمين", "تغطية", "شهادة تأمين",
    ],
    "dispute_resolution": [
        "dispute", "arbitration", "mediation", "court", "claim",
        "litige", "arbitrage", "médiation", "tribunal", "réclamation",
        "نزاع", "تحكيم", "وساطة", "محكمة", "مطالبة",
    ],
    "service_level": [
        "service level", "uptime", "availability", "service credit",
        "incident response", "support",
        "niveau de service", "disponibilité", "crédit de service",
        "réponse aux incidents", "support",
        "مستوى الخدمة", "التوافر", "تعويض الخدمة", "الاستجابة للحوادث", "الدعم",
    ],
    "assignment": [
        "assignment", "transfer", "delegate", "change of control",
        "cession", "transfert", "déléguer", "changement de contrôle",
        "تنازل", "نقل", "تفويض", "تغيير السيطرة",
    ],
    "general": [],
}


def normalize_language(language: str) -> str:
    language = str(language or "en").lower().strip()
    return language if language in SUPPORTED_LANGUAGES else "en"


def normalize_text(text: str) -> str:
    text = str(text or "").lower()
    text = text.replace("–", "-").replace("—", "-")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def find_time_periods(text: str) -> list[str]:
    matches = []

    for pattern in TIME_PATTERNS:
        matches.extend(
            re.findall(
                pattern,
                text,
                flags=re.IGNORECASE,
            )
        )

    clean = []
    seen = set()

    for match in matches:
        value = match if isinstance(match, str) else " ".join(match)
        value = str(value).strip()

        if not value:
            continue

        key = value.casefold()

        if key in seen:
            continue

        seen.add(key)
        clean.append(value)

    return clean


def detect_timeline_event(
    title: str,
    text: str,
) -> tuple[str, str]:

    title_normalized = normalize_text(title)
    text_normalized = normalize_text(text)

    for event, signals in EVENT_SIGNALS.items():
        if event == "general":
            continue

        title_hit = any(
            signal.lower() in title_normalized
            for signal in signals
        )

        body_hit = any(
            signal.lower() in text_normalized
            for signal in signals
        )

        if title_hit:
            return event, "high"

        if body_hit:
            return event, "medium"

    return "general", "low"


def extract_contract_timeline(
    clauses: list[dict],
    language: str = "en",
) -> list[dict]:

    language = normalize_language(language)
    timeline = []
    seen = set()

    if not isinstance(clauses, list):
        return []

    for clause in clauses:
        if not isinstance(clause, dict):
            continue

        source_clause = (
            clause.get("clause_title")
            or clause.get("title")
            or ""
        )

        source_clause_id = (
            clause.get("id")
            or clause.get("clause_id")
            or ""
        )

        clause_type = (
            clause.get("clause_type")
            or clause.get("type")
            or ""
        )

        risk_level = clause.get("risk_level", "")

        text = " ".join([
            str(clause.get("clause_title", "")),
            str(clause.get("title", "")),
            str(clause.get("quoted_text", "")),
            str(clause.get("original_text", "")),
            str(clause.get("clause_text", "")),
            str(clause.get("text", "")),
            str(clause.get("explanation_simple", "")),
            str(clause.get("legal_insight", "")),
        ])

        matches = find_time_periods(text)

        if not matches:
            continue

        event, confidence = detect_timeline_event(
            source_clause,
            text,
        )

        for match in matches:
            dedupe_key = (
                str(source_clause_id),
                str(source_clause).casefold(),
                str(event),
                str(match).casefold(),
            )

            if dedupe_key in seen:
                continue

            seen.add(dedupe_key)

            timeline.append({
                "event": event,
                "time_period": match,
                "source_clause": source_clause,
                "source_clause_id": source_clause_id,
                "clause_type": clause_type,
                "risk_level": risk_level,
                "confidence": confidence,
            })

    return timeline
