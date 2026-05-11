import re


def extract_clause_title(text: str) -> str:
    patterns = [
        r"المادة\s*\d+\s*[-–]\s*(.+)",
        r"Article\s*\d+\s*[-–]\s*(.+)",
        r"ARTICLE\s*\d+\s*[-–]\s*(.+)",
        r"Section\s*\d+\s*[-–]\s*(.+)",
        r"SECTION\s*\d+\s*[-–]\s*(.+)",
        r"Clause\s*\d+\s*[-–]\s*(.+)",
        r"CLAUSE\s*\d+\s*[-–]\s*(.+)",
    ]

    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1).strip()

    first_line = text.strip().split("\n")[0].strip()

    if len(first_line) < 80:
        return first_line

    return "Clause"