import re
from collections import Counter


def normalize_line(line: str) -> str:
    line = str(line or "").strip()

    # Strip a leading markdown heading marker ("#", "##", ...) before
    # further normalization -- every contract test document in this
    # pipeline uses markdown-style section headers ("# 1. DEFINITIONS"),
    # but every structural pattern in heading_confidence() anchors on
    # the line's own first character (a digit, a letter, "article"...).
    # A leading "#" made every such header invisible to heading
    # detection here, in any language, silently discarding the
    # section's real title. This is a separate, independent copy of the
    # same fix already applied to legal_document_engine.py -- this file
    # is its own standalone fallback engine with no shared code, so the
    # fix has to be applied here too.
    line = re.sub(r"^#+\s*", "", line)

    return re.sub(r"\s+", " ", line)


# Known unnumbered structural headings, matched independent of letter
# case. heading_confidence()'s all-caps pattern gives English/French
# unnumbered headings (e.g. "SIGNATURES") a way to be recognized, but
# scripts with no letter case at all (Arabic) can never satisfy an
# uppercase-only regex character class, so an unnumbered heading like
# "التوقيعات" was silently invisible here. A short, explicit list
# covers the common closing/opening sections that routinely appear
# without a number in any of the three languages.
_STRUCTURAL_HEADING_TERMS = [
    "signatures", "signature", "in witness whereof",
    "en foi de quoi",
    "التوقيعات", "التوقيع",
    "definitions", "définitions", "التعاريف",
    "recitals", "préambule", "الديباجة", "تمهيد",
    "exhibits", "annexes", "الملاحق",
]


def heading_confidence(line: str) -> float:
    line = normalize_line(line)

    if not line:
        return 0.0

    if line.strip(" :.-–—").lower() in _STRUCTURAL_HEADING_TERMS:
        return 0.65

    # The numbered-clause pattern ("1.", "2.1", "3.1.2"...), and the
    # "article/section/المادة N" patterns, are on their own a strong,
    # sufficient signal that this line begins a new clause -- regardless
    # of how long the rest of the sentence is. Previously these
    # contributed only +0.45 each (the same weight as every other
    # pattern), so a numbered pattern match could only cross the 0.65
    # threshold TOGETHER WITH the line-length/word-count bonuses below --
    # bonuses that essentially never apply to a real, full-sentence
    # numbered clause (almost always well over 120 characters / 12
    # words). In practice this made the threshold unreachable for
    # ordinary clause text, silently merging consecutive numbered
    # sub-clauses (e.g. "2.1 ..." and "2.2 ...") into one undifferentiated
    # blob under their shared section header, with only the first
    # clause's number surviving as the merged entry's apparent
    # reference -- confirmed in testing as the root cause of clauses
    # silently disappearing.
    if re.search(r"^\d+(\.\d+)*[\)\.\-]?\s+", line):
        return 1.0

    if re.search(r"^(article|section|clause)\s+\d+", line, re.IGNORECASE):
        return 1.0

    if re.search(r"^(المادة|البند|الفقرة)\s*\d+", line):
        return 1.0

    score = 0.0

    if re.search(r"^[A-Z][A-Z\s&/,()\-]{4,}$", line, re.IGNORECASE):
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
    """
    Flattens the (possibly nested) tree returned by
    build_document_structure() into a flat list of clause texts.

    CRITICAL FIX: the previous version only iterated the top-level
    `structure` list and never descended into a node's own "children" --
    any sub-clause that happened to score high enough on
    heading_confidence() to become a nested CHILD node (rather than a
    plain paragraph line under its parent) was silently dropped from the
    output entirely. Whether a given numbered sub-clause becomes a child
    node or a paragraph line depends only on its own text length/word
    count (heading_confidence()'s length and word-count bonuses), which
    is unrelated to whether it is legally substantive -- confirmed in
    testing: a short sub-clause (e.g. "4.2 ... shall not solicit ...")
    could score as a heading and vanish, while a longer sibling in the
    exact same section (e.g. "4.1 ... shall not ... compete ...")
    happened to fall just below threshold and was correctly kept as a
    paragraph -- an unpredictable, silent, per-clause data loss bug.
    This walks every node recursively so nothing nested is ever skipped.
    """
    clauses = []

    def walk(node: dict):
        title = str(node.get("title", "")).strip()
        body = "\n".join(node.get("paragraphs", [])).strip()

        clause = "\n".join(
            part for part in [title, body]
            if part
        ).strip()

        if len(clause) >= min_length:
            clauses.append(clause)

        for child in node.get("children", []):
            walk(child)

    for node in structure:
        walk(node)

    return clauses
