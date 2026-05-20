import re
from typing import List

from app.services.contract_agent.legal_document_engine import (
    parse_legal_document,
    parse_legal_document_objects,
)

from app.services.contract_agent.document_structure_builder import (
    build_document_structure,
    flatten_structure_to_clauses,
)


def normalize_arabic_title(title: str) -> str:
    title = title.strip()

    replacements = {
        "المحل استعمال": "استعمال المحل",
        "تجاري كراء عقد": "عقد كراء تجاري",
        "الأداء عدم": "عدم الأداء",
        "الشراء أهداف": "أهداف الشراء",
        "الفكرية الملكية": "الملكية الفكرية",
        "والدفع الأسعار": "الأسعار والدفع",
        "الإصلاحات الصيانة": "الصيانة والإصلاحات",
        "السداد الفائدة": "الفائدة والسداد",
        "الإخلال حالات": "حالات الإخلال",
        "الدفع الرسوم": "الرسوم والدفع",
        "البيانات حماية": "حماية البيانات",
        "المسؤولية تحديد": "تحديد المسؤولية",
        "الخدمة مستوى": "مستوى الخدمة",
        "العقد إنهاء": "إنهاء العقد",
        "المهام الوظيفة": "الوظيفة والمهام",
        "التطبيق الواجب القانون": "القانون الواجب التطبيق",
        "المكافأة الأجر": "الأجر والمكافأة",
        "تجاري قرض عقد": "عقد قرض تجاري",
        "توزيع عقد": "عقد توزيع",
        "سحابية برمجية خدمات عقد": "عقد خدمات برمجية سحابية",
        "القرض مبلغ": "مبلغ القرض",
    }

    return replacements.get(title, title)



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

    noise_signals = [

        # ENGLISH
        "not intended as advice",
        "professional services",
        "consult competent counsel",
        "for reference only",

        # FRENCH
        "à titre informatif",
        "consultez un professionnel",
        "services professionnels",

        # ARABIC
        "استشارة قانونية",
        "خدمات مهنية",
        "لأغراض مرجعية فقط",
    ]

    noise_hits = sum(
        1
        for signal in noise_signals
        if signal in normalized
    )

    if (
        noise_hits >= 2
        and len(normalized) < 1200
    ):
        return True

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

    engine_clauses = parse_legal_document(text)

    if len(engine_clauses) >= 3:
        return engine_clauses

    structure = build_document_structure(text)
    structured_clauses = flatten_structure_to_clauses(structure)

    if len(structured_clauses) >= 3:
        return structured_clauses

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
            cleaned_clauses = [fallback]

    # Fallback simple title splitter
    if len(cleaned_clauses) <= 1:
        fallback_parts = re.split(
            r"\n(?=[A-ZÀ-ÖØ-Þ\u0600-\u06FF][^\n]{3,60}\n)",
            text
        )

        if len(fallback_parts) > 2:
            fallback_clauses = []

            for part in fallback_parts:
                part = part.strip()

                if len(part) < 40:
                    continue

                lines = [
                    line.strip()
                    for line in part.splitlines()
                    if line.strip()
                ]

                if len(lines) < 2:
                    continue

                title = lines[0][:80].strip()
                title = normalize_arabic_title(title)
                body = "\n".join(lines[1:]).strip()

                clause_text = clean_clause_text(
                    "\n".join([
                        title,
                        body,
                    ])
                )

                if len(clause_text) > 40:
                    fallback_clauses.append(clause_text)

            if len(fallback_clauses) > len(cleaned_clauses):
                cleaned_clauses = fallback_clauses

    # Fallback semantic splitter for weak PDFs
    if len(cleaned_clauses) <= 1:

        fallback_parts = re.split(
            r"\n(?=[A-ZÀ-ÖØ-Þ\u0600-\u06FF][^\n]{3,80}\n)",
            text
        )

        fallback_clauses = []

        for part in fallback_parts:
            part = part.strip()

            if len(part) < 60:
                continue

            lines = [
                l.strip()
                for l in part.splitlines()
                if l.strip()
            ]

            if len(lines) < 2:
                continue

            title = lines[0][:120].strip()
            title = normalize_arabic_title(title)
            body = "\n".join(lines[1:]).strip()

            if len(body) < 40:
                continue

            clause_text = clean_clause_text(
                "\n".join([
                    title,
                    body,
                ])
            )

            if len(clause_text) > 60:
                fallback_clauses.append(clause_text)

        if len(fallback_clauses) > len(cleaned_clauses):
            cleaned_clauses = fallback_clauses

    return cleaned_clauses


def split_into_clause_objects(
    text: str,
) -> list[dict]:
    """
    Return structured clause objects while preserving hierarchy metadata.

    Primary path:
    - legal_document_engine.parse_legal_document_objects()

    Fallback path:
    - existing split_into_clauses() string splitter
    - wrap each string into a normalized object shape
    """

    if not text or not text.strip():
        return []

    objects = parse_legal_document_objects(text)

    if len(objects) >= 3:
        return objects

    clauses = split_into_clauses(text)

    return [
        {
            "id": f"fallback_{i}",
            "title": clause.split("\n")[0][:120],
            "text": clause,
            "level": 1,
            "depth": 1,
            "parent_id": None,
            "parent_clause_id": None,
            "semantic_parent": None,
            "section_path": [],
            "children": [],
            "confidence": 0.3,
        }
        for i, clause in enumerate(clauses)
    ]

