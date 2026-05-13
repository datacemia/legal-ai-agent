import re


def extract_clause_title(text: str) -> str:
    """
    Extract a clean clause title from multilingual contracts.

    Supports:
    - Arabic
    - English
    - French
    - Numeric clauses
    - Standalone uppercase titles
    - Section references with or without separators

    Returns:
    - Clean clause title
    - "Clause" fallback if nothing reliable found
    """

    if not text or not text.strip():
        return "Clause"

    text = text.strip()

    patterns = [
        # Arabic
        r"^(?:المادة|البند|الفقرة)\s*[\d\.]+\s*[-–:\.]?\s*([^\n\r]+)",

        # English
        r"^(?:Article|ARTICLE|Section|SECTION|Clause|CLAUSE)\s*[\d\.]+\s*[-–:\.]?\s*([^\n\r]+)",

        # French
        r"^(?:Article|ARTICLE|Section|SECTION|Clause|CLAUSE)\s*[\d\.]+\s*[-–:\.]?\s*([^\n\r]+)",

        # Numeric only
        r"^\s*[\d\.]+\s*[-–:\.]?\s*([^\n\r]+)",

        # ALL CAPS titles
        r"^([A-Z][A-Z\s&/,()-]{3,})$",
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.MULTILINE)

        if match:
            title = match.group(1).strip()

            # Cleanup
            title = re.sub(r"\s+", " ", title)
            title = re.sub(r"^[\-–:\.\s]+", "", title)
            title = re.sub(r"[\-–:\.\s]+$", "", title)

            # Avoid garbage extraction
            if (
                title
                and len(title) <= 120
                and not re.fullmatch(r"[\d\W_]+", title)
            ):
                return title

    # Fallback to first meaningful short line
    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    for line in lines[:5]:
        clean = re.sub(r"\s+", " ", line)

        # Skip very long paragraphs
        if len(clean) > 120:
            continue

        # Skip obvious legal body text
        if len(clean.split()) > 15:
            continue

        return clean

    return "Clause"
