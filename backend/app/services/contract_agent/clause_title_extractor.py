"""
clause_title_extractor.py

Deterministic clause-title extractor for international contract analysis.

Goals:
- Works across contract families and sectors.
- Supports English, French, Arabic.
- Handles OCR/PDF noise.
- Handles common numbering formats.
- Provides localized fallbacks.
- Avoids returning generic document titles as clause titles.
"""

import re


SUPPORTED_LANGUAGES = {"en", "fr", "ar"}


AR_TITLE_FIXES = {
    "المحل استعمال": "استعمال المحل",
    "الفكرية الملكية": "الملكية الفكرية",
    "المهام الوظيفة": "الوظيفة والمهام",
    "السداد الفائدة": "الفائدة والسداد",
    "البيانات حماية": "حماية البيانات",
    "المسؤولية تحديد": "تحديد المسؤولية",
    "التطبيق الواجب القانون": "القانون الواجب التطبيق",
    "التجاري المحل - 1 المادة": "المحل التجاري",
    "الأداء عدم": "عدم الأداء",
    "القرض مبلغ - 1 المادة": "مبلغ القرض",
    "والدفع الرسوم": "الرسوم والدفع",
    "الخدمة مستوى": "مستوى الخدمة",
    "المكافأة الأجر": "الأجر والمكافأة",
    "العقد إنهاء": "إنهاء العقد",
    "القاهرة القوة": "القوة القاهرة",
    "النزاعات تسوية": "تسوية النزاعات",
    "التحكيم مقر": "مقر التحكيم",
    "المعلومات سرية": "سرية المعلومات",
    "الشخصية البيانات": "البيانات الشخصية",
}


AR_COMMON_BIGRAM_FIXES = {
    ("المحل", "استعمال"): "استعمال المحل",
    ("الفكرية", "الملكية"): "الملكية الفكرية",
    ("المهام", "الوظيفة"): "الوظيفة والمهام",
    ("السداد", "الفائدة"): "الفائدة والسداد",
    ("البيانات", "حماية"): "حماية البيانات",
    ("المسؤولية", "تحديد"): "تحديد المسؤولية",
    ("التطبيق", "الواجب"): "القانون الواجب التطبيق",
    ("الخدمة", "مستوى"): "مستوى الخدمة",
    ("العقد", "إنهاء"): "إنهاء العقد",
    ("القاهرة", "القوة"): "القوة القاهرة",
    ("النزاعات", "تسوية"): "تسوية النزاعات",
    ("التحكيم", "مقر"): "مقر التحكيم",
    ("المعلومات", "سرية"): "سرية المعلومات",
    ("الشخصية", "البيانات"): "البيانات الشخصية",
}


GENERIC_TITLES = {
    # EN
    "agreement",
    "contract",
    "section",
    "clause",
    "article",
    "schedule",
    "exhibit",
    "appendix",
    "annex",
    "page",
    "signature",
    "signatures",

    # FR
    "contrat",
    "accord",
    "section",
    "clause",
    "article",
    "annexe",
    "appendice",
    "page",
    "signature",
    "signatures",

    # AR
    "عقد",
    "اتفاقية",
    "المادة",
    "البند",
    "الفقرة",
    "ملحق",
    "مرفق",
    "صفحة",
    "التوقيع",
    "التوقيعات",
}


NOISE_PATTERNS = [
    # Page / footer / header noise
    r"^\s*page\s+\d+\s*(of\s+\d+)?\s*$",
    r"^\s*\d+\s*/\s*\d+\s*$",
    r"^\s*-\s*\d+\s*-\s*$",
    r"^\s*confidential\s*$",
    r"^\s*strictly confidential\s*$",
    r"^\s*draft\s*$",
    r"^\s*privileged and confidential\s*$",

    # French
    r"^\s*page\s+\d+\s*(sur\s+\d+)?\s*$",
    r"^\s*confidentiel\s*$",
    r"^\s*strictement confidentiel\s*$",
    r"^\s*projet\s*$",

    # Arabic
    r"^\s*صفحة\s+\d+\s*$",
    r"^\s*سري\s*$",
    r"^\s*سري للغاية\s*$",
    r"^\s*مسودة\s*$",

    # TOC lines
    r".*\.{3,}\s*\d+\s*$",

    # Common disclaimer fragments
    r".*not intended as legal advice.*",
    r".*consult.*counsel.*",
    r".*ne constitue pas.*conseil juridique.*",
    r".*استشارة قانونية.*",
]


def normalize_language(language: str) -> str:
    language = str(language or "en").lower().strip()
    return language if language in SUPPORTED_LANGUAGES else "en"


def localized_untitled(language: str) -> str:
    language = normalize_language(language)

    if language == "fr":
        return "Clause sans titre"

    if language == "ar":
        return "بند بدون عنوان"

    return "Untitled Clause"


def normalize_spaces(text: str) -> str:
    text = str(text or "")
    text = text.replace("–", "-").replace("—", "-")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def is_arabic_text(text: str) -> bool:
    return bool(re.search(r"[\u0600-\u06FF]", str(text or "")))


def is_noise_line(line: str) -> bool:
    normalized = normalize_spaces(line)

    if not normalized:
        return True

    for pattern in NOISE_PATTERNS:
        if re.search(pattern, normalized, flags=re.IGNORECASE):
            return True

    return False


def is_generic_title(title: str) -> bool:
    normalized = normalize_spaces(title).lower().strip(" -–—:.")
    return normalized in GENERIC_TITLES


def remove_numbering_prefix(title: str) -> str:
    value = normalize_spaces(title)

    value = re.sub(
        r"^\s*(article|clause|section)\s+\d+(\.\d+)*\s*[-:.–—]?\s*",
        "",
        value,
        flags=re.IGNORECASE,
    )

    value = re.sub(
        r"^\s*(annex|appendix|schedule|exhibit)\s+[a-z0-9ivxlcdm]+\s*[-:.–—]?\s*",
        "",
        value,
        flags=re.IGNORECASE,
    )

    value = re.sub(
        r"^\s*(article|section|clause)\s+[ivxlcdm]+\s*[-:.–—]?\s*",
        "",
        value,
        flags=re.IGNORECASE,
    )

    value = re.sub(
        r"^\s*(article|clause|section|annexe|appendice)\s+\d+(\.\d+)*\s*[-:.–—]?\s*",
        "",
        value,
        flags=re.IGNORECASE,
    )

    value = re.sub(
        r"^\s*(المادة|البند|الفقرة|الملحق|المرفق)\s*[\d٠-٩]*\s*[-:.–—]?\s*",
        "",
        value,
    )

    value = re.sub(
        r"^\s*\d+(\.\d+)*\s*[).:-]?\s*",
        "",
        value,
    )

    value = re.sub(
        r"^\s*[\(（]?\s*([a-z]|[ivxlcdm]+)\s*[\)）]\s+",
        "",
        value,
        flags=re.IGNORECASE,
    )

    return value.strip(" -–—:.")


def normalize_arabic_title(title: str) -> str:
    value = normalize_spaces(title).strip(" -–—:.")

    if value in AR_TITLE_FIXES:
        return AR_TITLE_FIXES[value]

    # Handle OCR reversed "Title - 1 المادة"
    value = re.sub(
        r"^(.+?)\s*[-–—]\s*[\d٠-٩]+\s*(المادة|البند|الفقرة)\s*$",
        r"\1",
        value,
    ).strip(" -–—:.")

    if value in AR_TITLE_FIXES:
        return AR_TITLE_FIXES[value]

    words = value.split()

    if len(words) == 2:
        fixed = AR_COMMON_BIGRAM_FIXES.get((words[0], words[1]))
        if fixed:
            return fixed

    if len(words) == 3:
        # Common OCR reversal for "القانون الواجب التطبيق"
        if words == ["التطبيق", "الواجب", "القانون"]:
            return "القانون الواجب التطبيق"

    return value


def clean_title_candidate(title: str, language: str = "en") -> str:
    language = normalize_language(language)

    value = normalize_spaces(title)
    value = remove_numbering_prefix(value)
    value = value.strip(" -–—:.،؛")

    if is_arabic_text(value):
        value = normalize_arabic_title(value)

    if len(value) > 120:
        value = value[:120].strip(" -–—:.،؛")

    title_fixes = {
        "Non-Solicitation of personnels": "Non-Solicitation",
        "Non Solicitation of personnels": "Non-Solicitation",
        "Non-Solicitation of personnel": "Non-Solicitation",
        "Non Solicitation of personnel": "Non-Solicitation",
    }

    value = title_fixes.get(value, value)

    return value


def extract_meaningful_lines(text: str, max_lines: int = 8) -> list[str]:
    lines = []

    for raw_line in str(text or "").splitlines():
        line = normalize_spaces(raw_line)

        if not line:
            continue

        if is_noise_line(line):
            continue

        lines.append(line)

        if len(lines) >= max_lines:
            break

    return lines


def choose_title_line(lines: list[str], language: str = "en") -> str:
    candidates = []

    for line in lines:
        cleaned = clean_title_candidate(line, language)

        if len(cleaned) < 2:
            continue

        if len(cleaned) > 120:
            continue

        if is_generic_title(cleaned):
            continue

        # Prefer obvious heading-like lines.
        score = 0

        if re.search(r"^(article|clause|section|annex|appendix|schedule|exhibit)\b", line, re.IGNORECASE):
            score += 3

        if re.search(r"^\d+(\.\d+)*[\).:-]?\s+", line):
            score += 2

        if re.search(r"^(المادة|البند|الفقرة|الملحق|المرفق)", line):
            score += 3

        if len(cleaned.split()) <= 10:
            score += 2

        if line.isupper() and len(line) <= 80:
            score += 1

        candidates.append((score, cleaned))

    if not candidates:
        return ""

    candidates.sort(key=lambda item: item[0], reverse=True)

    return candidates[0][1]


def fallback_title_from_body(text: str, language: str = "en") -> str:
    cleaned = normalize_spaces(text).strip(" -–—:.،؛")
    cleaned = remove_numbering_prefix(cleaned)

    if is_arabic_text(cleaned):
        cleaned = normalize_arabic_title(cleaned)

    words = cleaned.split()

    if len(words) >= 4:
        return " ".join(words[:4]).strip(" -–—:.،؛")

    if len(words) >= 2:
        return " ".join(words[:2]).strip(" -–—:.،؛")

    return localized_untitled(language)


def extract_clause_title(
    clause_text: str,
    language: str = "en",
) -> str:
    """
    Extract a short clause title from raw clause text.

    Deterministic and lightweight:
    - uses the first meaningful short heading-like line when available
    - removes numbering prefixes
    - supports English, French, and Arabic clause headings
    - ignores OCR/PDF noise
    - localizes fallback titles
    - avoids returning overly generic document titles
    """

    language = normalize_language(language)

    text = str(clause_text or "").strip()

    if not text:
        return ""

    meaningful_lines = extract_meaningful_lines(text)

    if not meaningful_lines:
        return localized_untitled(language)

    title = choose_title_line(
        meaningful_lines,
        language=language,
    )

    if title:
        return title

    return fallback_title_from_body(
        text,
        language=language,
    )
