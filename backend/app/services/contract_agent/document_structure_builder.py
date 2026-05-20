import re
from collections import Counter


def normalize_line(line: str) -> str:
    return re.sub(r"\s+", " ", str(line or "").strip())


def heading_confidence(line: str) -> float:
    line = normalize_line(line)

    if not line:
        return 0.0

    patterns = [
        r"^(article|section|clause)\s+\d+",
        r"^\d+(\.\d+)*[\)\.\-]?\s+",
        r"^(المادة|البند|الفقرة)\s*\d+",
        r"^[A-Z][A-Z\s&/,()\-]{4,}$",
    ]

    score = 0.0

    for pattern in patterns:
        if re.search(pattern, line, re.IGNORECASE):
            score += 0.45

    if len(line) <= 120:
        score += 0.2

    if len(line.split()) <= 12:
        score += 0.2

    return min(score, 1.0)


def is_repeated_noise(line: str, counts: Counter) -> bool:
    normalized = normalize_line(line).lower()

    noise_signals = [
        "not intended as advice",
        "professional services",
        "consult competent counsel",
        "readers should consult",
        "à titre informatif",
        "ne constitue pas un conseil",
        "services professionnels",
        "استشارة قانونية",
        "خدمات مهنية",
        "تنبيه",
    ]

    if any(signal in normalized for signal in noise_signals):
        return True

    return counts[normalize_line(line)] >= 3 and len(normalized) > 60


def detect_heading_level(line: str) -> int:
    line = normalize_line(line)

    if re.search(r"^(article|المادة)\s+\d+", line, re.IGNORECASE):
        return 1

    if re.search(r"^(section|clause|البند)\s+\d+", line, re.IGNORECASE):
        return 2

    if re.search(r"^\d+\.\d+\.\d+", line):
        return 3

    if re.search(r"^\d+\.\d+", line):
        return 2

    if re.search(r"^\d+[\)\.\-]?\s+", line):
        return 1

    return 1


def build_document_structure(text: str) -> list[dict]:
    lines = [
        normalize_line(line)
        for line in str(text or "").splitlines()
        if normalize_line(line)
    ]

    counts = Counter(lines)

    roots = []
    stack = []

    for line in lines:
        if is_repeated_noise(line, counts):
            continue

        confidence = heading_confidence(line)

        if confidence >= 0.65:
            level = detect_heading_level(line)

            node = {
                "title": line,
                "level": level,
                "confidence": confidence,
                "paragraphs": [],
                "children": [],
            }

            while stack and stack[-1]["level"] >= level:
                stack.pop()

            if stack:
                stack[-1]["children"].append(node)
            else:
                roots.append(node)

            stack.append(node)
            continue

        if not stack:
            node = {
                "title": "Untitled Section",
                "level": 1,
                "confidence": 0.3,
                "paragraphs": [],
                "children": [],
            }
            roots.append(node)
            stack.append(node)

        stack[-1]["paragraphs"].append(line)

    return roots


def flatten_structure_to_clauses(
    structure: list[dict],
    min_length: int = 80,
) -> list[str]:
    clauses = []

    for node in structure:
        title = node.get("title", "").strip()
        body = "\n".join(node.get("paragraphs", [])).strip()

        clause = "\n".join(
            part for part in [title, body]
            if part
        ).strip()

        if len(clause) >= min_length:
            clauses.append(clause)

    return clauses
