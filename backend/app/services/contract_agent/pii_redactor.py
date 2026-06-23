import re

try:
    from gliner import GLiNER
except Exception:
    GLiNER = None


_MODEL = None


ROLE_KEYWORDS = {
    "CLIENT": ["client", "the client", "le client", "la cliente", "العميل", "الزبون"],
    "SERVICE_PROVIDER": ["prestataire", "service provider", "provider", "contractor", "consultant", "fournisseur", "مقدم الخدمة", "المزود", "المتعاقد", "الاستشاري"],
    "EMPLOYER": ["employer", "employeur", "صاحب العمل"],
    "EMPLOYEE": ["employee", "executive", "employé", "salarié", "cadre", "الموظف", "الأجير", "العامل"],
    "COMPANY": ["company", "corporation", "société", "entreprise", "الشركة"],
    "BUYER": ["buyer", "purchaser", "acheteur", "المشتري"],
    "SELLER": ["seller", "vendor", "vendeur", "البائع"],
    "LESSOR": ["lessor", "landlord", "bailleur", "المؤجر"],
    "LESSEE": ["lessee", "tenant", "locataire", "المستأجر"],
    "LICENSOR": ["licensor", "concédant", "المرخِّص"],
    "LICENSEE": ["licensee", "licencié", "المرخَّص له"],
    "LENDER": ["lender", "prêteur", "المقرض"],
    "BORROWER": ["borrower", "emprunteur", "المقترض"],
}


def get_gliner_model():
    global _MODEL
    if GLiNER is None:
        return None

    if _MODEL is None:
        try:
            _MODEL = GLiNER.from_pretrained("urchade/gliner_multi_pii-v1")
        except Exception as e:
            print(f"GLiNER unavailable, using regex-only redaction: {e}")
            _MODEL = False

    return _MODEL if _MODEL is not False else None


def normalize_spaces(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def tag_for_role(role_text: str, fallback: str) -> str:
    role = normalize_spaces(role_text).lower()

    for tag, keywords in ROLE_KEYWORDS.items():
        for keyword in keywords:
            if keyword.lower() in role:
                return f"[{tag}]"

    return fallback


def looks_like_placeholder(value: str) -> bool:
    return bool(re.fullmatch(r"\[[A-Z_0-9]+\]", value.strip()))


def looks_like_contract_role(value: str) -> bool:
    normalized = normalize_spaces(value).lower().strip(" «»\"'.,;:()[]")

    normalized = re.sub(
        r"^(the|le|la|l’|l')\s+",
        "",
        normalized,
        flags=re.IGNORECASE,
    )

    role_words = set()

    for keywords in ROLE_KEYWORDS.values():
        for keyword in keywords:
            keyword = keyword.lower().strip()

            role_words.add(keyword)

            keyword_no_article = re.sub(
                r"^(the|le|la|l’|l')\s+",
                "",
                keyword,
                flags=re.IGNORECASE,
            )

            role_words.add(keyword_no_article)

    return normalized in role_words


def replace_by_spans(text: str, replacements: list[tuple[int, int, str]]) -> str:
    replacements = sorted(replacements, key=lambda x: x[0], reverse=True)

    redacted = text
    for start, end, replacement in replacements:
        redacted = redacted[:start] + replacement + redacted[end:]

    return redacted


def redact_arabic_contract_parties(text: str) -> str:
    if not text:
        return text

    text = re.sub(
        r"(الطرف\s+الأول\s*:\s*)([^\n\r]+)",
        r"\1[ORGANIZATION]",
        text,
    )

    text = re.sub(
        r"(الطرف\s+الثاني\s*:\s*)([^\n\r]+)",
        r"\1[PERSON]",
        text,
    )

    return text


def redact_labeled_contract_parties(text: str) -> str:
    if not text:
        return text

    patterns = [
        # Arabic
        (
            r"(الطرف\s+الأول\s*:\s*)([^\n\r]+)",
            r"\1[ORGANIZATION]",
        ),
        (
            r"(الطرف\s+الثاني\s*:\s*)([^\n\r]+)",
            r"\1[PERSON]",
        ),

        # English
        (
            r"((?:Company|Employer|Client)\s*:\s*)([^\n\r]+)",
            r"\1[ORGANIZATION]",
        ),
        (
            r"((?:Employee|Executive|Consultant|Contractor|Service Provider)\s*:\s*)([^\n\r]+)",
            r"\1[PERSON]",
        ),

        # French
        (
            r"((?:Société|Employeur|Client)\s*:\s*)([^\n\r]+)",
            r"\1[ORGANIZATION]",
        ),
        (
            r"((?:Employé|Salarié|Prestataire|Consultant)\s*:\s*)([^\n\r]+)",
            r"\1[PERSON]",
        ),
    ]

    for pattern, replacement in patterns:
        text = re.sub(
            pattern,
            replacement,
            text,
            flags=re.IGNORECASE,
        )

    return text


def role_aware_party_pseudonymize(text: str) -> str:
    if not text:
        return ""

    patterns = [
        re.compile(
            r"\b(?:between|by\s+and\s+between)\s+(.{2,220}?),\s*(?:a\s+[^,\n()]{2,120}\s*)?\([^)]*[\"'](?:the\s+)?([^\"']{2,70})[\"'][^)]*\)\s*,?\s+and\s+(.{2,180}?)\s*\([^)]*[\"'](?:the\s+)?([^\"']{2,70})[\"'][^)]*\)",
            re.IGNORECASE | re.DOTALL,
        ),
        re.compile(
            r"(?:conclu|signé|établi|passé)?\s*(?:entre)\s+(.{2,180}?),\s*ci-après\s+[«\"]\s*(?:le|la|l’|l')?\s*([^»\"]{2,70})\s*[»\"]\s*,?\s+(?:et|avec)\s+(.{2,180}?)(?:,\s*[^,\n]{0,120})?,\s*ci-après\s+[«\"]\s*(?:le|la|l’|l')?\s*([^»\"]{2,70})\s*[»\"]",
            re.IGNORECASE | re.DOTALL,
        ),
        re.compile(
            r"(?:between|by\s+and\s+between)\s+(.{2,180}?),\s*(?:hereinafter|referred\s+to\s+as|known\s+as|called)\s+[\"'](?:the\s+)?([^\"']{2,70})[\"']\s*,?\s+(?:and|with)\s+(.{2,180}?),\s*(?:hereinafter|referred\s+to\s+as|known\s+as|called)\s+[\"'](?:the\s+)?([^\"']{2,70})[\"']",
            re.IGNORECASE | re.DOTALL,
        ),
        re.compile(
            r"(?:agreement|contract)\s+(?:is\s+)?(?:made|entered\s+into)?\s*(?:by\s+and\s+)?between\s+(.{2,180}?),\s*(?:a\s+[^,\n]{2,80},\s*)?(?:and)\s+([A-Z][A-Za-z.'-]+(?:\s+[A-Z][A-Za-z.'-]+){0,5})(?:,|\s)+(?:as\s+)?(?:the\s+)?(employee|executive|consultant)",
            re.IGNORECASE | re.DOTALL,
        ),
        re.compile(
            r"بين\s+(.{2,180}?)\s*(?:،|,)?\s*(?:ويشار\s+إليه|المشار\s+إليه)\s+(?:بـ|ب|على\s+أنه)?\s*[\"«]([^\"»]{2,70})[\"»]\s*(?:،|,)?\s*و\s+(.{2,180}?)\s*(?:،|,)?\s*(?:ويشار\s+إليه|المشار\s+إليه)\s+(?:بـ|ب|على\s+أنه)?\s*[\"«]([^\"»]{2,70})[\"»]",
            re.IGNORECASE | re.DOTALL,
        ),
    ]

    for pattern in patterns:
        match = pattern.search(text)
        if not match:
            continue

        if len(match.groups()) == 4:
            party_1_start, party_1_end = match.start(1), match.end(1)
            role_1 = match.group(2)

            party_2_start, party_2_end = match.start(3), match.end(3)
            role_2 = match.group(4)

            return replace_by_spans(
                text,
                [
                    (party_1_start, party_1_end, tag_for_role(role_1, "[PARTY_1]")),
                    (party_2_start, party_2_end, tag_for_role(role_2, "[PARTY_2]")),
                ],
            )

        if len(match.groups()) == 3:
            party_1_start, party_1_end = match.start(1), match.end(1)
            party_2_start, party_2_end = match.start(2), match.end(2)
            role_2 = match.group(3)

            tag_1 = "[EMPLOYER]" if tag_for_role(role_2, "") == "[EMPLOYEE]" else "[PARTY_1]"
            tag_2 = tag_for_role(role_2, "[PARTY_2]")

            return replace_by_spans(
                text,
                [
                    (party_1_start, party_1_end, tag_1),
                    (party_2_start, party_2_end, tag_2),
                ],
            )

    return text


def regex_redact(text: str) -> str:
    if not text:
        return ""

    redacted = text

    redacted = re.sub(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b", "[EMAIL]", redacted)
    redacted = re.sub(r"\b[A-Z]{2}\d{2}[A-Z0-9]{10,30}\b", "[IBAN]", redacted)
    redacted = re.sub(r"(?<!\w)(?:\+?\d{1,3}[\s.-]?)?(?:\(?\d{2,4}\)?[\s.-]?)?\d{3,4}[\s.-]?\d{3,4}(?!\w)", "[PHONE]", redacted)
    redacted = re.sub(r"\b[A-Z]{1,3}\d{5,12}\b", "[ID_NUMBER]", redacted)
    redacted = re.sub(r"\b\d{3}-\d{2}-\d{4}\b", "[ID_NUMBER]", redacted)

    redacted = re.sub(
        r"\b\d{1,6}\s+(?:[A-Za-zÀ-ÿ0-9.'’-]+\s+){0,8}(?:Street|St\.|Avenue|Ave\.|Road|Rd\.|Boulevard|Blvd\.|Lane|Ln\.|Drive|Dr\.|Highway|Route|Rue)\s*\d{0,6}\b",
        "[ADDRESS]",
        redacted,
        flags=re.IGNORECASE,
    )

    return redacted


def gliner_redact(text: str) -> str:
    model = get_gliner_model()

    if not model or not text:
        return text

    labels = [
        "person",
        "organization",
        "company",
        "location",
        "address",
        "email",
        "phone number",
        "passport number",
        "national id",
        "tax id",
        "bank account",
    ]

    try:
        entities = model.predict_entities(text, labels, threshold=0.40)
    except Exception as e:
        print(f"GLiNER prediction failed, using regex-only redaction: {e}")
        return text

    replacements = []

    for entity in entities:
        start = entity.get("start")
        end = entity.get("end")
        label = entity.get("label", "").lower()

        if start is None or end is None:
            continue

        value = text[start:end].strip()

        if (
            not value
            or looks_like_placeholder(value)
            or looks_like_contract_role(value)
        ):
            continue

        if label == "person":
            tag = "[PERSON]"
        elif label in {"organization", "company"}:
            tag = "[ORGANIZATION]"
        elif label in {"location", "address"}:
            tag = "[LOCATION]"
        else:
            tag = "[SENSITIVE_DATA]"

        replacements.append((start, end, tag))

    return replace_by_spans(text, replacements)


def redact_sensitive_data(text: str) -> str:
    if not text:
        return ""

    text = redact_labeled_contract_parties(text)

    redacted = role_aware_party_pseudonymize(text)
    redacted = regex_redact(redacted)
    redacted = gliner_redact(redacted)

    return redacted
