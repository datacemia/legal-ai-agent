import re


def is_clause_heading(line: str) -> bool:
    line = line.strip()

    patterns = [
        # English
        r"^\d+\.\s+",
        r"^Article\s*\d+",
        r"^ARTICLE\s*\d+",
        r"^Section\s*\d+",
        r"^SECTION\s*\d+",
        r"^Clause\s*\d+",
        r"^CLAUSE\s*\d+",

        # French
        r"^Article\s*\d+",
        r"^ARTICLE\s*\d+",
        r"^Clause\s*\d+",

        # Arabic
        r"^المادة\s*\d+",

        # Arabic reversed / malformed PDF extraction
        r".*[-–]\s*\d+\s+ةداملا$",
    ]

    return any(re.search(pattern, line) for pattern in patterns)


def split_into_clauses(text: str) -> list[str]:
    if not text:
        return []

    lines = [line.strip() for line in text.splitlines() if line.strip()]

    clauses = []
    current_clause = []

    for line in lines:
        if is_clause_heading(line):
            if current_clause:
                clauses.append("\n".join(current_clause).strip())

            current_clause = [line]
        else:
            current_clause.append(line)

    if current_clause:
        clauses.append("\n".join(current_clause).strip())

    cleaned_clauses = []

    for clause in clauses:
        if len(clause) < 15:
            continue

        if clause not in cleaned_clauses:
            cleaned_clauses.append(clause)

    return cleaned_clauses
