import re
from typing import List


def normalize_line(line: str) -> str:
    """
    Normalize OCR/PDF extracted text.
    """

    line = line.strip()

    # Normalize spaces
    line = re.sub(r"\s+", " ", line)

    # Normalize dashes
    line = line.replace("–", "-").replace("—", "-")

    return line


def is_table_of_contents_line(line: str) -> bool:
    """
    Detect table-of-contents lines from PDFs.
    """

    line = normalize_line(line)

    toc_patterns = [
        r"\.{5,}\s*\d+$",
        r"\.{3,}\s*\d+\s*$",
    ]

    return any(
        re.search(pattern, line)
        for pattern in toc_patterns
    )



def is_structural_attachment_heading(line: str) -> bool:
    """
    Detect annexes, exhibits, schedules, appendices,
    templates and attachment headings.

    These are structural document sections,
    not operational legal clauses.
    """

    line = normalize_line(line).lower()

    patterns = [

        # -------------------------
        # ENGLISH
        # -------------------------

        r"^(exhibit|schedule|annex|appendix)\s+[a-z0-9\-]+",
        r"^(form of)\s+",

        # -------------------------
        # FRENCH
        # -------------------------

        r"^(annexe|appendice)\s+[a-z0-9\-]+",
        r"^(modèle de|formulaire de)\s+",

        # -------------------------
        # ARABIC
        # -------------------------

        r"^(ملحق|مرفق)\s*[\w\d\-]*",
        r"^(نموذج)\s+",
    ]

    return any(
        re.search(pattern, line, re.IGNORECASE)
        for pattern in patterns
    )


def is_clause_heading(line: str) -> bool:
    """
    Detect whether a line is likely a contract clause heading.
    Supports:
    - English
    - French
    - Arabic
    - OCR/PDF malformed extraction
    - Numeric sections
    """

    line = normalize_line(line)

    if not line:
        return False

    patterns = [

        # -----------------------------------
        # ENGLISH / FRENCH STANDARD
        # -----------------------------------

        r"^(article|section|clause)\s+\d+(\.\d+)*",
        r"^(ARTICLE|SECTION|CLAUSE)\s+\d+(\.\d+)*",

        # -----------------------------------
        # NUMERIC HEADINGS
        # 1.
        # 1.1
        # 2.4.1
        # -----------------------------------

        r"^\d+(\.\d+)*[\)\.\-]?\s+[A-ZÀ-ÿ\u0600-\u06FF]",

        # -----------------------------------
        # ARABIC
        # -----------------------------------

        r"^(المادة|البند|الفقرة)\s*\d+",

        # -----------------------------------
        # OCR / BROKEN PDF EXTRACTION
        # -----------------------------------

        r".*[-–]\s*\d+\s+ةداملا$",

        # -----------------------------------
        # ALL CAPS TITLES
        # TERMINATION
        # CONFIDENTIALITY
        # -----------------------------------

        r"^[A-Z][A-Z\s&/,()\-]{3,}$",

        # -----------------------------------
        # ROMAN NUMERALS
        # -----------------------------------

        r"^(ARTICLE|Article)\s+[IVXLC]+",
    ]

    return any(
        re.search(pattern, line, re.IGNORECASE)
        for pattern in patterns
    )


def should_merge_with_previous(line: str) -> bool:
    """
    Detect broken heading continuation lines.
    """

    line = normalize_line(line)

    if not line:
        return False

    short_patterns = [

        # Short continuation fragments
        r"^[a-zà-ÿ]",
        r"^[\(\[]",
        r"^and\b",
        r"^or\b",
        r"^including\b",

        # Arabic continuation
        r"^(و|أو|بما|بخصوص)",

    ]

    if len(line) < 60:
        return any(
            re.search(pattern, line, re.IGNORECASE)
            for pattern in short_patterns
        )

    return False


def clean_clause_text(text: str) -> str:
    """
    Clean extracted clause text.
    """

    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)

    return text.strip()


def is_low_value_clause(clause: str) -> bool:
    text = clause.lower().strip()

    normalized = re.sub(r"\s+", " ", text).strip()

    # Standalone document titles
    document_title_patterns = [
        r"^amended and restated .* agreement$",
        r"^credit agreement$",
        r"^loan agreement$",
        r"^service agreement$",
        r"^employment agreement$",
        r"^non-disclosure agreement$",

        r"^contrat .*",
        r"^accord .*",

        r"^اتفاقية .*",
        r"^عقد .*",
    ]

    if any(
        re.match(pattern, normalized, re.IGNORECASE)
        for pattern in document_title_patterns
    ):
        return True

    low_value_patterns = [

        # English
        "now, therefore",
        "now therefore",
        "in consideration of the foregoing",
        "mutual promises",
        "good and valuable consideration",
        "receipt and sufficiency",
        "hereby expressly acknowledged",
        "headings are for reference only",
        "for reference only",

        # French
        "en considération de ce qui précède",
        "les titres sont fournis à titre indicatif",
        "à titre indicatif uniquement",
        "les intitulés des articles",
        "sans affecter l’interprétation",

        # Arabic
        "بناء على ما سبق",
        "وعليه",
        "مقابل الوعود المتبادلة",
        "تعتبر العناوين لأغراض مرجعية فقط",
        "لا تؤثر العناوين على تفسير",
    ]

    return any(pattern in text for pattern in low_value_patterns)


def split_into_clauses(text: str) -> List[str]:
    """
    Split a contract into logical clauses.

    Improvements:
    - Better multilingual heading detection
    - Better OCR tolerance
    - Better duplicate filtering
    - Avoid tiny garbage clauses
    - Better malformed PDF handling
    - Skip low-value boilerplate clauses
    """

    if not text or not text.strip():
        return []

    lines = [
        normalize_line(line)
        for line in text.splitlines()
        if line.strip()
    ]

    clauses = []
    current_clause = []

    for line in lines:

        if is_table_of_contents_line(line):
            continue

        if is_structural_attachment_heading(line):
            continue

        # New heading detected
        if is_clause_heading(line):

            # Save previous clause
            if current_clause:

                clause_text = clean_clause_text(
                    "\n".join(current_clause)
                )

                if len(clause_text) > 30:
                    clauses.append(clause_text)

            current_clause = [line]

        else:

            # Merge broken heading continuation
            if (
                current_clause
                and should_merge_with_previous(line)
                and len(current_clause[-1]) < 80
            ):
                current_clause[-1] += " " + line

            else:
                current_clause.append(line)

    # Final clause
    if current_clause:

        clause_text = clean_clause_text(
            "\n".join(current_clause)
        )

        if len(clause_text) > 30:
            clauses.append(clause_text)

    # -----------------------------------
    # Deduplicate intelligently
    # -----------------------------------

    cleaned_clauses = []
    seen = set()

    for clause in clauses:

        normalized = re.sub(
            r"\s+",
            " ",
            clause.lower()
        ).strip()

        # Skip near-empty garbage
        if len(normalized) < 30:
            continue

        # Skip duplicates
        if normalized in seen:
            continue

        seen.add(normalized)

        if not is_low_value_clause(clause):
            cleaned_clauses.append(clause)

    if not cleaned_clauses:
        fallback = clean_clause_text(text)

        if len(fallback) > 80:
            return [fallback]

    return cleaned_clauses
