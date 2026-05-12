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


def split_into_clauses(text: str) -> List[str]:
    """
    Split a contract into logical clauses.

    Improvements:
    - Better multilingual heading detection
    - Better OCR tolerance
    - Better duplicate filtering
    - Avoid tiny garbage clauses
    - Better malformed PDF handling
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

        cleaned_clauses.append(clause)

    return cleaned_clauses