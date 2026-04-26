import re


def split_into_clauses(text: str) -> list[str]:
    if not text:
        return []

    patterns = [
        r"\n(?=\d+\.\s)",          # 1. Clause
        r"\n(?=Article\s+\d+)",   # Article 1
        r"\n(?=ARTICLE\s+\d+)",   # ARTICLE 1
        r"\n(?=Section\s+\d+)",   # Section 1
        r"\n(?=SECTION\s+\d+)",   # SECTION 1

        # Arabic
        r"\n(?=المادة\s+\d+)",    # المادة 1
        r"(?=المادة\s+\d+)",      # fallback if text has no newlines
    ]

    combined_pattern = "|".join(patterns)
    clauses = re.split(combined_pattern, text)

    cleaned_clauses = [
        clause.strip()
        for clause in clauses
        if len(clause.strip()) > 50
    ]

    return cleaned_clauses