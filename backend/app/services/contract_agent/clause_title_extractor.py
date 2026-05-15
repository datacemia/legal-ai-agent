import re


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
}


def extract_clause_title(clause_text: str) -> str:
    """
    Extract a short clause title from raw clause text.

    This function is intentionally deterministic and lightweight:
    - uses the first meaningful short line when available
    - removes numbering prefixes
    - supports English, French, and Arabic clause headings
    - avoids returning overly long titles
    """

    text = str(clause_text or "").strip()

    if not text:
        return ""

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    if not lines:
        return ""

    candidate_lines = []

    for line in lines[:5]:
        cleaned = line.strip()

        if len(cleaned) < 3:
            continue

        if len(cleaned) > 120:
            continue

        candidate_lines.append(cleaned)

    if not candidate_lines:
        return ""

    first_line = candidate_lines[0]

    # Remove common numbering prefixes:
    # 1. Title
    # 1) Title
    # Article 1 - Title
    # Clause 2: Title
    # المادة 3: العنوان
    first_line = re.sub(
        r"^\s*(article|clause|section)\s+\d+\s*[-:.–—]?\s*",
        "",
        first_line,
        flags=re.IGNORECASE,
    )

    first_line = re.sub(
        r"^\s*(المادة|البند|الفقرة)\s*\d*\s*[-:.–—]?\s*",
        "",
        first_line,
    )

    first_line = re.sub(
        r"^\s*\d+(\.\d+)*\s*[).:-]?\s*",
        "",
        first_line,
    )

    first_line = first_line.strip(" -–—:.")

    if len(first_line) > 120:
        first_line = first_line[:120].strip()

    if first_line.strip() in AR_TITLE_FIXES:
        first_line = AR_TITLE_FIXES[first_line.strip()]

    if not first_line.strip():
        return "Untitled Clause"

    return first_line
