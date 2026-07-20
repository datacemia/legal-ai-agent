import re
import logging

try:
    from gliner import GLiNER
except Exception:
    GLiNER = None


_MODEL = None
logger = logging.getLogger(__name__)

print("========== PII_REDACTOR V2 LOADED ==========")
ROLE_KEYWORDS = {
    "PARTY_1": ["party 1", "party a", "first party", "première partie", "partie a", "الطرف الأول", "الطرف أ"],
    "PARTY_2": ["party 2", "party b", "second party", "deuxième partie", "partie b", "الطرف الثاني", "الطرف ب"],

    "CLIENT": ["client", "customer", "the client", "le client", "la cliente", "العميل", "الزبون"],
    "SERVICE_PROVIDER": ["service provider", "provider", "prestataire", "prestataire de services", "contractor", "consultant", "fournisseur", "مقدم الخدمة", "المزود", "المتعاقد", "الاستشاري"],
    "SUPPLIER": ["supplier", "fournisseur", "المورد"],
    "VENDOR": ["vendor", "vendeur professionnel", "المورّد", "البائع"],
    "CONTRACTOR": ["contractor", "entrepreneur", "مقاول", "المقاول"],
    "SUBCONTRACTOR": ["subcontractor", "sous-traitant", "مقاول من الباطن"],

    "EMPLOYER": ["employer", "employeur", "صاحب العمل"],
    "EMPLOYEE": ["employee", "executive", "employé", "salarié", "cadre", "الموظف", "الأجير", "العامل"],
    "CONSULTANT": ["consultant", "conseiller", "استشاري"],

    "COMPANY": ["company", "corporation", "société", "entreprise", "الشركة"],
    "SHAREHOLDER": ["shareholder", "stockholder", "actionnaire", "مساهم"],
    "INVESTOR": ["investor", "investisseur", "مستثمر"],
    "FOUNDER": ["founder", "fondateur", "مؤسس"],
    "DIRECTOR": ["director", "board member", "administrateur", "عضو مجلس الإدارة"],
    "OFFICER": ["officer", "dirigeant", "مسؤول تنفيذي"],
    "ACQUIRER": ["acquirer", "acquéreur", "المستحوذ"],
    "TARGET": ["target company", "société cible", "الشركة المستهدفة"],

    "BUYER": ["buyer", "purchaser", "acheteur", "acquéreur", "المشتري"],
    "SELLER": ["seller", "vendeur", "البائع"],
    "DISTRIBUTOR": ["distributor", "distributeur", "موزع"],
    "RESELLER": ["reseller", "revendeur", "بائع معتمد"],
    "MANUFACTURER": ["manufacturer", "fabricant", "مصنع"],
    "AGENT": ["agent", "commercial agent", "mandataire", "agent commercial", "وكيل"],
    "PRINCIPAL": ["principal", "mandant", "موكل"],

    "LESSOR": ["lessor", "landlord", "bailleur", "المؤجر"],
    "LESSEE": ["lessee", "tenant", "locataire", "المستأجر"],
    "PROPERTY_OWNER": ["property owner", "propriétaire", "مالك العقار"],
    "PROPERTY_MANAGER": ["property manager", "gestionnaire immobilier", "مدير العقار"],

    "LICENSOR": ["licensor", "concédant", "المرخِّص"],
    "LICENSEE": ["licensee", "licencié", "المرخَّص له"],
    "AUTHOR": ["author", "auteur", "مؤلف"],
    "ASSIGNEE": ["assignee", "cessionnaire", "المتنازل له"],
    "ASSIGNOR": ["assignor", "cédant", "المتنازل"],

    "LENDER": ["lender", "creditor", "prêteur", "créancier", "المقرض", "الدائن"],
    "BORROWER": ["borrower", "debtor", "emprunteur", "débiteur", "المقترض", "المدين"],
    "GUARANTOR": ["guarantor", "caution", "garant", "كفيل", "ضامن"],
    "SECURED_PARTY": ["secured party", "créancier garanti", "الدائن المضمون"],
    "PLEDGOR": ["pledgor", "constituant", "راهن"],
    "BANK": ["bank", "banque", "بنك"],

    "CONTROLLER": ["controller", "data controller", "responsable du traitement", "متحكم بالبيانات"],
    "PROCESSOR": ["processor", "data processor", "sous-traitant", "معالج البيانات"],
    "SUBPROCESSOR": ["subprocessor", "sub-processor", "sous-traitant ultérieur", "معالج فرعي"],
    "DATA_SUBJECT": ["data subject", "personne concernée", "صاحب البيانات"],

    "INSURER": ["insurer", "assureur", "شركة التأمين", "المؤمن"],
    "INSURED": ["insured", "assuré", "المؤمن له"],
    "BENEFICIARY": ["beneficiary", "bénéficiaire", "مستفيد"],

    "FRANCHISOR": ["franchisor", "franchiseur", "مانح الامتياز"],
    "FRANCHISEE": ["franchisee", "franchisé", "صاحب الامتياز"],

    "OWNER": ["owner", "project owner", "maître d'ouvrage", "صاحب المشروع", "المالك"],
    "OPERATOR": ["operator", "exploitant", "مشغل"],
    "ENGINEER": ["engineer", "ingénieur", "مهندس"],
    "ARCHITECT": ["architect", "architecte", "مهندس معماري"],

    "CARRIER": ["carrier", "transporteur", "ناقل"],
    "SHIPPER": ["shipper", "expéditeur", "الشاحن"],
    "CONSIGNEE": ["consignee", "destinataire", "المرسل إليه"],
    "FREIGHT_FORWARDER": ["freight forwarder", "transitaire", "وكيل شحن"],

    "PATIENT": ["patient", "مريض"],
    "SPONSOR": ["sponsor", "promoteur", "راعي"],
    "INVESTIGATOR": ["investigator", "chercheur principal", "الباحث"],
    "HOSPITAL": ["hospital", "hôpital", "مستشفى"],

    "AUTHORITY": ["authority", "public authority", "administration", "autorité", "جهة حكومية", "سلطة"],
    "CONCESSIONAIRE": ["concessionaire", "concessionnaire", "صاحب الامتياز"],
}


# ---------------------------------------------------------------------------
# GLiNER safe-chunking layer.
#
# Root-cause fix for silent PII-detection truncation: GLiNER's underlying
# model has a hard ~384 subword-token window. When gliner_redact() used to
# hand it the ENTIRE document text in a single call, GLiNER's own internal
# sentence splitter would sometimes fail to find a paragraph/sentence break
# for a very long stretch of text (contracts often have no blank lines
# between clauses), causing it to treat a huge span -- in observed logs, as
# large as ~2000+ tokens -- as a single "sentence" that gets silently
# truncated to 384 tokens before any entity scanning happens. Any
# unstructured PII (e.g. a person's name mentioned in prose) located past
# that truncation point is never even attempted, let alone redacted.
#
# The fix is to pre-chunk the text ourselves, BEFORE calling GLiNER, into
# pieces small enough that this truncation cannot occur, regardless of
# whether GLiNER's own splitter finds a natural break. This is language
# agnostic (works the same for EN/FR/AR prose) and domain agnostic (does
# not depend on contract type): it only depends on generic paragraph and
# sentence boundaries, with a hard character-based fallback that guarantees
# a safe chunk size even for a single run-on clause with no punctuation for
# a long stretch (which does occur in dense legal drafting, e.g. long
# defined-term paragraphs).
#
# Budgets are deliberately conservative (well under the raw 384-token
# limit) because subword tokenizers can split a single word into multiple
# tokens -- more so for morphologically rich languages -- so counting in
# words/characters must leave generous headroom rather than assuming a
# roughly 1:1 word-to-token ratio.
# ---------------------------------------------------------------------------

_GLINER_SAFE_WORD_BUDGET = 150
_GLINER_HARD_CHAR_BUDGET = 900

_PARAGRAPH_SPLIT_PATTERN = re.compile(r"\n\s*\n")
_SENTENCE_SPLIT_PATTERN = re.compile(r"(?<=[.!?؟۔])\s+")


def _chunk_fits_budget(chunk: str) -> bool:
    return (
        len(chunk.split()) <= _GLINER_SAFE_WORD_BUDGET
        and len(chunk) <= _GLINER_HARD_CHAR_BUDGET
    )


def _hard_split_for_gliner(unit: str, base_offset: int) -> list:
    """
    Last-resort safety net: split at whitespace boundaries so that even a
    single run-on clause with no sentence-ending punctuation for a long
    stretch is guaranteed to be chunked under the safe budget, rather than
    silently truncated by the model.
    """
    chunks = []
    cursor = 0

    while cursor < len(unit):
        remaining = unit[cursor:]

        if len(remaining) <= _GLINER_HARD_CHAR_BUDGET:
            chunks.append((base_offset + cursor, remaining))
            break

        split_at = remaining.rfind(" ", 0, _GLINER_HARD_CHAR_BUDGET)

        if split_at <= 0:
            split_at = _GLINER_HARD_CHAR_BUDGET

        chunks.append((base_offset + cursor, remaining[:split_at]))
        cursor += split_at

    return chunks


def _split_unit_for_gliner(unit: str, base_offset: int) -> list:
    if not unit.strip():
        return []

    if _chunk_fits_budget(unit):
        return [(base_offset, unit)]

    return _hard_split_for_gliner(unit, base_offset)


def _split_paragraph_for_gliner(paragraph: str, base_offset: int) -> list:
    if not paragraph.strip():
        return []

    if _chunk_fits_budget(paragraph):
        return [(base_offset, paragraph)]

    chunks = []
    cursor = 0

    for sentence_match in _SENTENCE_SPLIT_PATTERN.finditer(paragraph):
        sentence = paragraph[cursor:sentence_match.end()]
        chunks.extend(_split_unit_for_gliner(sentence, base_offset + cursor))
        cursor = sentence_match.end()

    tail = paragraph[cursor:]
    chunks.extend(_split_unit_for_gliner(tail, base_offset + cursor))

    return chunks


def split_into_gliner_chunks(text: str) -> list:
    """
    Split text into chunks small enough that GLiNER's underlying model
    cannot silently truncate part of a chunk before scanning it for
    entities.

    Returns a list of (start_offset, chunk_text) tuples so entity spans
    found within each chunk can be translated back to absolute character
    positions in the original text.

    Splitting strategy, in order of preference (so sentence/clause
    boundaries are kept intact wherever possible, preserving the context
    GLiNER uses to detect entities):
      1. Split on blank lines (paragraph breaks).
      2. Any paragraph still over budget is split on sentence-ending
         punctuation (. ! ? and the Arabic question mark ؟), keeping the
         punctuation attached to the preceding sentence.
      3. Any sentence still over budget (e.g. a single long defined-term
         clause with no punctuation for a long stretch) is hard-split at
         the nearest whitespace before the budget.
    """
    if not text:
        return []

    chunks = []
    cursor = 0

    for paragraph_match in _PARAGRAPH_SPLIT_PATTERN.finditer(text):
        paragraph = text[cursor:paragraph_match.start()]
        chunks.extend(_split_paragraph_for_gliner(paragraph, cursor))
        cursor = paragraph_match.end()

    tail = text[cursor:]
    chunks.extend(_split_paragraph_for_gliner(tail, cursor))

    return chunks


def get_gliner_model():
    global _MODEL
    if GLiNER is None:
        return None

    if _MODEL is None:
        try:
            _MODEL = GLiNER.from_pretrained("urchade/gliner_multi_pii-v1")
        except Exception as e:
            logger.debug("GLiNER unavailable, using regex-only redaction: %s", e)
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


# ---------------------------------------------------------------------------
# Generic legal structural-term guard.
#
# GLiNER occasionally mistags bare, capitalized defined-term references --
# "Party", "Affiliate", "Services", "Business Day", "Deliverables",
# "Confidential Information", "Force Majeure Event" -- as an
# organization/person/location entity, because they are capitalized and
# structurally resemble named entities. These are drafting vocabulary
# common to virtually any contract in any domain, not PII, and redacting
# them corrupts the clause text itself: e.g. "the Parties shall establish
# a joint security governance committee" becomes "the [ORGANIZATION] shall
# establish a [ORGANIZATION]", which then breaks downstream reasoning
# (wrong clause title, nonsensical legal_insight) and can even break
# jurisdiction detection if a defined term is consumed where a real
# location was expected nearby.
#
# This list is deliberately restricted to genuinely generic, structural
# contract vocabulary (present in EN/FR/AR, independent of contract type)
# -- not specific business names, addresses, or other real identifying
# information, which should still be redacted normally.
# ---------------------------------------------------------------------------

_GENERIC_LEGAL_STRUCTURAL_TERMS = {
    # English
    "party", "parties", "affiliate", "affiliates",
    "services", "service", "agreement",
    "business day", "business days",
    "deliverable", "deliverables",
    "confidential information", "personal data",
    "force majeure event", "force majeure",
    "effective date", "initial term", "renewal term",
    "statement of work",
    "exhibit a", "exhibit b", "exhibit c", "exhibit d", "exhibit e",

    # French
    "partie", "parties", "filiale", "filiales",
    "services", "service", "accord", "contrat",
    "jour ouvrable", "jours ouvrables",
    "livrable", "livrables",
    "informations confidentielles", "données personnelles",
    "cas de force majeure", "force majeure",
    "date d'effet", "date d’effet", "durée initiale", "durée de renouvellement",
    "énoncé des travaux", "bon de commande",
    "annexe a", "annexe b", "annexe c", "annexe d", "annexe e",

    # Arabic
    "الطرف", "الأطراف", "الشركة التابعة", "الشركات التابعة",
    "الخدمات", "الخدمة", "الاتفاقية", "العقد",
    "يوم عمل", "أيام عمل",
    "المخرجات", "المخرج",
    "المعلومات السرية", "البيانات الشخصية",
    "حدث القوة القاهرة", "القوة القاهرة",
    "تاريخ النفاذ", "المدة الأولية", "مدة التجديد",
    "بيان نطاق العمل", "أمر الشراء",
    "الملحق أ", "الملحق ب", "الملحق ج", "الملحق د", "الملحق هـ",
    "الملحق 1", "الملحق 2", "الملحق 3", "الملحق 4", "الملحق 5",
}


_GENERIC_PARTY_REFERENCE_PATTERN = re.compile(
    r"^("
    # English: "one of the parties", "either party", "either of the
    # parties", "any party", "both parties", "the other party", "each
    # party"...
    r"(one|either|any|both|the\s+other|each)\s+(of\s+the\s+)?part(y|ies)"
    r"|"
    # French: "l'une des Parties", "l'une ou l'autre (des) Partie(s)",
    # "chaque Partie", "toute Partie", "l'autre Partie"...
    r"(l['’]?(?:une|autre)(?:\s+ou\s+l['’]?(?:une|autre))?|chaque|toute?)\s+"
    r"(des\s+|les\s+)?parties?"
    r"|"
    # Arabic: "أحد الطرفين", "كلا الطرفين", "أي طرف", "أي من الطرفين",
    # "كل طرف"... (quantifiers like أي/كل commonly precede the
    # INDEFINITE noun, without the ال prefix, unlike أحد/كلا which
    # precede the definite "الطرفين")
    r"(أحد|كلا|أي|كل)\s*(من\s*)?(الطرفين|الطرف|الأطراف|طرفين|طرف|أطراف)"
    r")$"
)


def looks_like_generic_legal_term(value: str) -> bool:
    """
    True if value is a bare defined-term reference to generic contract
    structure (Party, Services, Affiliate, Business Day, Deliverables,
    Confidential Information, Force Majeure Event, ...) rather than an
    actual named entity. Universal across EN/FR/AR and any contract
    domain -- these terms are drafting vocabulary, not PII.

    Also covers quantified references to a party ("one of the Parties",
    "either Party", "l'une des Parties", "أحد الطرفين"...) via a pattern
    match rather than requiring an exact literal entry in the exclusion
    set above -- otherwise only the bare noun ("party"/"partie") would be
    protected, while the (very common) quantified phrasing around it
    would still be misflagged as a PERSON entity.
    """
    normalized = normalize_spaces(value).lower().strip(" «»\"'.,;:()[]")

    normalized_no_article = re.sub(
        r"^(the|le|la|les|l’|l')\s+",
        "",
        normalized,
        flags=re.IGNORECASE,
    )

    if normalized_no_article in _GENERIC_LEGAL_STRUCTURAL_TERMS:
        return True

    return bool(_GENERIC_PARTY_REFERENCE_PATTERN.match(normalized))


def replace_by_spans(text: str, replacements: list) -> str:
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
        r"\1[PARTY_1]",
        text,
    )

    text = re.sub(
        r"(الطرف\s+الثاني\s*:\s*)([^\n\r]+)",
        r"\1[PARTY_2]",
        text,
    )

    return text


def redact_labeled_contract_parties(text: str) -> str:
    if not text:
        return text

    label_pattern = re.compile(
        r"(?P<label>"
        r"Company|Employer|Client|Customer|Service Provider|Provider|Supplier|Vendor|"
        r"Employee|Executive|Consultant|Contractor|Buyer|Seller|Lessor|Lessee|"
        r"Landlord|Tenant|Licensor|Licensee|Lender|Borrower|Guarantor|"
        r"Controller|Processor|Franchisor|Franchisee|Distributor|Reseller|"
        r"Société|Employeur|Prestataire|Fournisseur|Employé|Salarié|Acheteur|Vendeur|"
        r"Bailleur|Locataire|Concédant|Licencié|Prêteur|Emprunteur|Garant|"
        r"الطرف\s+الأول|الطرف\s+الثاني|الشركة|صاحب\s+العمل|العميل|مقدم\s+الخدمة|"
        r"الموظف|المشتري|البائع|المؤجر|المستأجر|المقرض|المقترض|الكفيل|"
        r"المتحكم\s+بالبيانات|معالج\s+البيانات"
        r")\s*:\s*(?P<value>[^\n\r]+)",
        re.IGNORECASE,
    )

    replacements = []
    party_counter = 0

    for match in label_pattern.finditer(text):
        label = match.group("label")
        value = match.group("value").strip()

        if (
            not value
            or looks_like_placeholder(value)
            or looks_like_contract_role(value)
            or looks_like_generic_legal_term(value)
        ):
            continue

        if re.search(r"الطرف\s+الأول", label):
            tag = "[PARTY_1]"
        elif re.search(r"الطرف\s+الثاني", label):
            tag = "[PARTY_2]"
        else:
            tag = tag_for_role(label, "")

        if not tag:
            party_counter += 1
            if party_counter == 1:
                tag = "[PARTY_1]"
            elif party_counter == 2:
                tag = "[PARTY_2]"
            else:
                tag = "[ORGANIZATION]"

        replacements.append((match.start("value"), match.end("value"), tag))

    return replace_by_spans(text, replacements)


def role_aware_party_pseudonymize(text: str) -> str:
    if not text:
        return ""

    patterns = [
        re.compile(
            r"\b(?:between|by\s+and\s+between)\s*:?\s*"
            r"(.{2,220}?)\s*,?\s*(?:a\s+[^()\n]{0,300}\s*)?\([^)]*[\"'](?:the\s+)?([^\"']{2,70})[\"'][^)]*\)"
            r"\s*[,;]?\s+and\s+"
            r"(.{2,180}?)\s*\([^)]*[\"'](?:the\s+)?([^\"']{2,70})[\"'][^)]*\)",
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
            r"بين\s+(.{2,180}?)\s*(?:،|,)?\s*(?:ويشار\s+إليه(?:ا|ما)?|المشار\s+إليه(?:ا|ما)?)\s+(?:بـ|ب|على\s+أنه(?:ا|ما)?)?\s*[\"«]([^\"»]{2,70})[\"»]\s*(?:،|,)?\s*و\s+(.{2,180}?)\s*(?:،|,)?\s*(?:ويشار\s+إليه(?:ا|ما)?|المشار\s+إليه(?:ا|ما)?)\s+(?:بـ|ب|على\s+أنه(?:ا|ما)?)?\s*[\"«]([^\"»]{2,70})[\"»]",
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


# ---------------------------------------------------------------------------
# Jurisdiction-location guard.
#
# A dispute-resolution seat/venue (e.g. "the seat of arbitration shall be
# Geneva, Switzerland") is substantive contract information the legal
# reasoning pipeline needs (jurisdiction detection, governing-law analysis)
# -- not personal data. Redacting it to "[LOCATION]" both loses that
# information and can corrupt downstream text (observed: jurisdiction
# detection falling back to an unrelated stray word once the real city was
# replaced).
#
# The signal list here is deliberately NARROW and specific to arbitration
# venue / dispute-forum language. It intentionally does NOT include
# generic "governing law" / "laws of" phrasing, because that phrasing
# commonly appears in a party-identification preamble immediately followed
# by the party's real registered address (e.g. "a company incorporated
# under the laws of France with its registered office at 12 Rue de la
# Convention, 75015 Paris, France") -- a genuinely real address that MUST
# still be redacted. Using a broad "governing law" signal there would
# create a new leak by protecting that real address from redaction. The
# narrower "seat of arbitration" / "place of arbitration" style phrasing
# used here does not, in practice, co-occur with a business address in the
# same sentence, so it is safe to treat as a jurisdiction-only signal.
# ---------------------------------------------------------------------------

_JURISDICTION_CONTEXT_SIGNALS = [
    # English -- arbitration / court venue
    "seat of arbitration", "place of arbitration",
    "arbitration shall be conducted in", "arbitration proceedings shall take place in",
    "venue for arbitration", "arbitration shall take place in",
    "exclusive jurisdiction of the courts of", "courts located in",
    "disputes shall be resolved in", "hearing shall be held in",
    # English -- governing law / choice of law
    # (a narrower, clause-construction-specific set deliberately kept
    # separate from a bare "laws of" match, so ordinary business-address
    # phrasing elsewhere in the contract is not swept up)
    "governed by the laws of", "governed by the law of",
    "shall be governed by", "construed in accordance with the laws of",
    # English -- party's jurisdiction of incorporation (same rationale:
    # a company's state/country of incorporation is generic structural
    # information, not personally identifying, and destroying it breaks
    # jurisdiction detection just as much as redacting the governing-law
    # clause does)
    "incorporated under the laws of", "organized under the laws of",
    "a corporation of the state of", "a corporation organized under",

    # French -- arbitration / court venue
    "siège de l'arbitrage", "siège de l’arbitrage", "lieu de l'arbitrage", "lieu de l’arbitrage",
    "l'arbitrage se déroulera à", "l’arbitrage se déroulera à",
    "compétence exclusive des tribunaux de", "tribunaux compétents de",
    # French -- droit applicable
    "régi par le droit de", "régi par les lois de",
    "régie par le droit de", "régie par les lois de",
    "soumis au droit de", "soumis aux lois de",
    # French -- constitution / droit d'incorporation de la partie
    "constituée en vertu des lois de", "constituée selon les lois de",
    "société de droit", "société constituée en vertu du droit de",

    # Arabic -- arbitration / court venue
    "مقر التحكيم", "مكان التحكيم", "يجري التحكيم في",
    "الاختصاص القضائي الحصري لمحاكم", "تعقد جلسات التحكيم في",
    # Arabic -- القانون الواجب التطبيق
    "يخضع هذا العقد لقانون", "يخضع لقانون", "تحكمه قوانين",
    "وفقاً لقوانين", "طبقاً لقوانين",
    # Arabic -- تأسيس الطرف بموجب قانون بلد/ولاية معينة
    "مؤسسة بموجب قوانين", "شركة تأسست بموجب قانون", "مسجلة بموجب قوانين",
]


_TERRITORIAL_SCOPE_CONTEXT_SIGNALS = [
    # English -- non-compete / exclusivity / license territorial scope
    "competitive with", "compete with", "competing business",
    "engage in a business", "directly or indirectly, engage in",
    "provide services to any business", "carry on business",
    "within the territory of", "territory of", "sales territory",
    "licensed territory", "exclusive territory", "restricted territory",

    # French
    "concurrente à", "activité concurrente", "exercer une activité",
    "directement ou indirectement", "sur le territoire de",
    "territoire concédé", "territoire exclusif", "zone territoriale",

    # Arabic
    "منافسة لـ", "نشاط منافس", "بشكل مباشر أو غير مباشر",
    "داخل إقليم", "الإقليم المرخص", "الإقليم الحصري", "النطاق الجغرافي",
]


def _has_territorial_scope_context(text: str, start: int, end: int) -> bool:
    context_start = max(0, start - 120)
    context_end = min(len(text), end + 40)
    surrounding = text[context_start:context_end].lower()

    return any(
        signal.lower() in surrounding
        for signal in _TERRITORIAL_SCOPE_CONTEXT_SIGNALS
    )


def _has_jurisdiction_context(text: str, start: int, end: int) -> bool:
    context_start = max(0, start - 120)
    context_end = min(len(text), end + 40)
    surrounding = text[context_start:context_end].lower()

    return any(
        signal.lower() in surrounding
        for signal in _JURISDICTION_CONTEXT_SIGNALS
    )


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

    replacements = []
    organization_index = 0

    # Pre-chunk before calling GLiNER (see module-level comment above) so
    # a long, blank-line-free document -- or a single very long clause --
    # cannot be silently truncated past the model's ~384-token window.
    # Entities are still discovered in left-to-right document order, since
    # chunks are generated sequentially by offset and each chunk's
    # entities are processed in the order GLiNER returns them, so
    # PARTY_1 / PARTY_2 assignment by order of first appearance is
    # unaffected by chunking.
    for chunk_offset, chunk_text in split_into_gliner_chunks(text):
        try:
            entities = model.predict_entities(chunk_text, labels, threshold=0.40)
        except Exception as e:
            logger.debug(
                "GLiNER prediction failed on a chunk, using regex-only "
                "redaction for that portion of text: %s",
                e,
            )
            continue

        for entity in entities:
            start = entity.get("start")
            end = entity.get("end")
            label = entity.get("label", "").lower()

            if start is None or end is None:
                continue

            absolute_start = chunk_offset + start
            absolute_end = chunk_offset + end

            value = text[absolute_start:absolute_end].strip()

            if (
                not value
                or looks_like_placeholder(value)
                or looks_like_contract_role(value)
                or looks_like_generic_legal_term(value)
            ):
                continue

            if label in {"organization", "company", "person"}:
                # Look at the sentence surrounding this entity for a role
                # keyword (Provider, Client, Employer, etc.) before falling
                # back to a generic tag. Without this, gliner_redact can
                # silently collapse two distinct parties into the same
                # [ORGANIZATION] tag when role_aware_party_pseudonymize's
                # regex didn't already catch them — losing role distinction
                # even after the regex patch.
                # Asymmetric, forward-only: a defined-term role marker
                # (e.g. '("Role")') consistently comes AFTER the entity
                # name in standard contract drafting, never before, so no
                # backward allowance is needed. Even a small backward
                # window risks catching a stray closing quote from a
                # DIFFERENT, PRECEDING entity's own defined term (e.g.
                # '...("Company"), and Dr. Jane Doe (the "Executive")' --
                # scanning back from "Dr. Jane Doe" could otherwise catch
                # the trailing '"' from "Company"'s own marker, throwing
                # off quote-pairing for this entity's actual role text).
                context_start = absolute_start
                context_end = min(len(text), absolute_end + 80)
                surrounding_context = text[context_start:context_end]

                # Only consider role keywords that appear inside a
                # genuine defined-term marker -- quotation marks
                # immediately following a parenthesis, e.g. '("Provider")'
                # or "(the 'Lender')". A role word appearing anywhere
                # else in the wide surrounding window (ordinary prose,
                # unrelated to this specific entity) must NOT be treated
                # as this entity's own role, however close it happens to
                # be. Confirmed real bug: "business" was being tagged
                # [SHAREHOLDER] purely because "shareholders" appeared
                # earlier in the same sentence with no defined-term
                # marker linking it to "business" at all.
                quoted_spans = re.findall(
                    r"[\"'\u201c\u2018]([^\"'\u201d\u2019]{1,60})[\"'\u201d\u2019]",
                    surrounding_context,
                )
                quoted_role_text = " ".join(quoted_spans)

                role_based_tag = tag_for_role(quoted_role_text, "")

                if role_based_tag:
                    tag = role_based_tag
                elif label == "person":
                    tag = "[PERSON]"
                else:
                    organization_index += 1
                    if organization_index == 1:
                        tag = "[PARTY_1]"
                    elif organization_index == 2:
                        tag = "[PARTY_2]"
                    else:
                        tag = "[ORGANIZATION]"
            elif label in {"location", "address"}:
                if _has_jurisdiction_context(text, absolute_start, absolute_end):
                    # A genuine arbitration seat / dispute venue: keep it
                    # as-is, it is substantive contract information, not
                    # personal data.
                    continue
                if _has_territorial_scope_context(text, absolute_start, absolute_end):
                    # A broad geographic/territorial scope term (e.g. a
                    # non-compete's "within North America", a license's
                    # "exclusive territory of the EU") -- substantive
                    # contract information defining the scope of a
                    # restriction, not personal data. Confirmed real
                    # bug: "North America" in a non-compete clause was
                    # being redacted to "[LOCATION]", destroying one of
                    # the most heavily-negotiated terms in that clause
                    # type.
                    continue
                tag = "[LOCATION]"
            else:
                tag = "[SENSITIVE_DATA]"

            replacements.append((absolute_start, absolute_end, tag))

    return replace_by_spans(text, replacements)


def redact_sensitive_data(text: str) -> str:
    if not text:
        return ""

    text = redact_labeled_contract_parties(text)

    redacted = role_aware_party_pseudonymize(text)
    redacted = regex_redact(redacted)
    redacted = gliner_redact(redacted)

    return redacted
