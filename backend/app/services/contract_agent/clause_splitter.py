import hashlib
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

try:
    from app.services.contract_agent.clause_title_extractor import extract_clause_title
except Exception:
    def extract_clause_title(clause_text: str, language: str = "en") -> str:
        text = str(clause_text or "").strip()
        if not text:
            return ""
        first_line = text.splitlines()[0].strip() if text.splitlines() else ""
        return first_line[:120] if first_line else "Untitled Clause"


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
        "القاهرة القوة": "القوة القاهرة",
        "النزاعات تسوية": "تسوية النزاعات",
        "التحكيم مقر": "مقر التحكيم",
        "المعلومات سرية": "سرية المعلومات",
        "الشخصية البيانات": "البيانات الشخصية",
        "الأعمال نطاق": "نطاق الأعمال",
        "العمل بيان": "بيان العمل",
        "الأمن جدول": "جدول الأمن",
        "الأسعار جدول": "جدول الأسعار",
    }

    return replacements.get(title, title)



def normalize_line(line: str) -> str:
    """
    Normalize OCR/PDF extracted text.
    """

    line = line.strip()

    # Strip a leading markdown heading marker ("#", "##", ...) before
    # further normalization. Every contract test document in this
    # pipeline uses markdown-style section headers ("# 1. POSITION AND
    # DUTIES"), but is_clause_heading()'s numbered-heading patterns all
    # anchor on a digit at the very start of the line. This is the
    # THIRD, independent copy of the same fix already applied to
    # legal_document_engine.py and document_structure_builder.py -- this
    # file has its own separate normalize_line() with no shared code, so
    # each had to be fixed individually. Confirmed as the root cause of
    # a first-section-specific bug: "# 1. POSITION AND DUTIES" was
    # invisible to is_clause_heading() and merged into whatever preceded
    # it (the document preamble/definitions), corrupting the clause
    # reference for the section immediately following it.
    line = re.sub(r"^#+\s*", "", line)

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

        r"^(exhibit|schedule|annex|appendix|attachment)\s+[a-z0-9\-]+",
        r"^(technical appendix|pricing schedule|pricing annex|security schedule)",
        r"^(data processing addendum|dpa|statement of work|sow)",
        r"^(order form|purchase order|service description|specifications)",
        r"^(form of)\s+",

        # -------------------------
        # FRENCH
        # -------------------------

        r"^(annexe|appendice|pièce jointe)\s+[a-z0-9\-]+",
        r"^(annexe technique|annexe tarifaire|annexe de sécurité)",
        r"^(avenant de traitement des données|description des services)",
        r"^(bon de commande|cahier des charges)",
        r"^(modèle de|formulaire de)\s+",

        # -------------------------
        # ARABIC
        # -------------------------

        r"^(ملحق|مرفق|الملحق|المرفق|ملاحق|المرفقات|الجدول)\s*[\w\d\-]*",
        r"^(جدول الأسعار|جدول الأمن|ملحق معالجة البيانات|بيان العمل)",
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

        # Allows a PII-redaction placeholder bracket ("[") as the first
        # character after the number, alongside an uppercase letter.
        # Without this, a clause whose very first word happens to be a
        # redacted entity (e.g. "Executive" -> "[EMPLOYEE]", common for
        # employment agreements where the first sentence names a role)
        # became completely invisible to this pattern -- confirmed in
        # testing: "1.1 [EMPLOYEE] shall serve..." silently merged into
        # the preceding section header, losing its own clause number,
        # while sibling clauses starting with an ordinary word ("The
        # Company shall...") were unaffected. This affects any language,
        # since redaction placeholders are always this same bracket
        # format regardless of the surrounding text's language.
        r"^\d+(\.\d+)*[\)\.\-]?\s+[A-ZÀ-ÿ\u0600-\u06FF\[]",

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

        r"^[A-Z0-9][A-Z0-9\s&/,()\-]{3,}$",

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




def is_document_preamble_or_cover(text: str) -> bool:
    normalized = re.sub(r"\s+", " ", str(text or "")).strip()
    lowered = normalized.lower()

    if not normalized:
        return True

    has_numbered_clause = bool(
        re.search(r"\b\d+(\.\d+)*\b", normalized)
    )

    has_operational_language = bool(
        re.search(
            r"\b(shall|must|may|means|includes|entitled|liable|terminate|pay|notify|process|"
            r"doit|peut|signifie|comprend|résilier|payer|notifier|traiter|"
            r"يلتزم|يجب|يجوز|يعني|يشمل|إنهاء|دفع|إخطار|معالجة)\b",
            lowered,
        )
    )

    looks_like_intro = bool(
        re.search(
            r"(entered into|effective date|by and between|each a party|collectively the parties|"
            r"conclu|date d'effet|entre les|les parties|"
            r"تم إبرام|تاريخ السريان|بين|الأطراف)",
            lowered,
        )
    )

    if looks_like_intro and not has_numbered_clause:
        return True

    if lowered.startswith("document preamble"):
        return True

    if (
        len(normalized.split()) <= 14
        and not has_operational_language
        and not has_numbered_clause
    ):
        return True

    return False


def is_non_clause_document_block(text: str) -> bool:
    normalized = re.sub(r"\s+", " ", str(text or "")).strip()
    lowered = normalized.lower()

    if not normalized:
        return True

    if is_document_preamble_or_cover(text):
        return True

    words = normalized.split()

    # Document title / cover heading: short, uppercase, no operative language.
    if (
        len(words) <= 12
        and normalized.isupper()
        and not re.search(
            r"\b(shall|must|may|means|includes|agree|entitled|liable|terminate|pay|notify|process)\b",
            lowered,
        )
    ):
        return True

    # Signature block.
    if re.search(
        r"\b(signature|signatures|in witness whereof|name / title|nom / titre|التوقيع|التوقيعات)\b",
        lowered,
        re.IGNORECASE,
    ):
        return True

    # Very short structural headings.
    structural_only_patterns = [
        r"^(definitions|general provisions|services and service levels)$",
        r"^(définitions|dispositions générales)$",
        r"^(التعاريف|الأحكام العامة)$",
    ]

    if len(words) <= 6 and any(
        re.match(pattern, lowered, re.IGNORECASE)
        for pattern in structural_only_patterns
    ):
        return True

    return False


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

    try:
        engine_clauses = parse_legal_document(text)
    except (ValueError, KeyError, RecursionError, MemoryError, TimeoutError, Exception):
        engine_clauses = []

    engine_clauses = [
        c for c in engine_clauses
        if not is_low_value_clause(c)
        and not is_non_clause_document_block(c)
    ]

    # Accept parser result only when document segmentation is sufficiently rich
    if len(engine_clauses) >= 5:
        return engine_clauses

    try:
        structure = build_document_structure(text)
        structured_clauses = flatten_structure_to_clauses(structure)
    except (ValueError, KeyError, RecursionError, MemoryError, TimeoutError, Exception):
        structured_clauses = []

    structured_clauses = [
        c for c in structured_clauses
        if not is_low_value_clause(c)
        and not is_non_clause_document_block(c)
    ]

    if len(structured_clauses) >= 5:
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
            # Annexes / schedules / exhibits may contain legally binding
            # provisions (pricing, SLA, DPA, specifications, etc.).
            # Start a new clause instead of discarding them.
            if current_clause:
                clause_text = clean_clause_text("\n".join(current_clause))
                if len(clause_text) > 30:
                    clauses.append(clause_text)
            current_clause = [line]
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

        # Skip duplicates using stable hash signature for large contracts
        signature = hashlib.sha1(
            normalized.encode("utf-8", errors="ignore")
        ).hexdigest()

        if signature in seen:
            continue

        seen.add(signature)

        if (
            not is_low_value_clause(clause)
            and not is_non_clause_document_block(clause)
        ):
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
                cleaned_clauses = [
                    c for c in fallback_clauses
                    if not is_non_clause_document_block(c)
                ]

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
            cleaned_clauses = [
                c for c in fallback_clauses
                if not is_non_clause_document_block(c)
            ]

    return cleaned_clauses


def extract_leading_clause_number(clause_text: str) -> str:
    """
    Extracts the leading numbered-clause reference (e.g. "1.1", "3.1.2")
    from the start of a clause's own text, if present. Script-agnostic:
    section numbering in this pipeline is always plain digits, in any of
    the three supported languages.

    Used to populate the "number" field in the fallback wrapping paths
    below, which previously omitted it entirely -- downstream code
    (contract_agent.py's attach_clause_object_metadata()) relies on this
    field as the authoritative source for clause_reference, and a
    clause object with no "number" field at all silently fell back to
    whatever the LLM itself inferred (or nothing), producing an
    incorrect or missing reference for any clause routed through this
    fallback path instead of the primary tree-based engine.
    """
    match = re.match(r"\s*(\d+(?:\.\d+)+)", str(clause_text or ""))
    return match.group(1) if match else ""


def split_into_clause_objects(
    text: str,
    language: str = "en",
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

    arabic_article_pattern = re.compile(
        r"(?=^المادة\s+[0-9٠-٩]+\s*[-–—:]?\s*)",
        re.MULTILINE,
    )

    if "المادة" in text:
        parts = [
            p.strip()
            for p in arabic_article_pattern.split(text)
            if p.strip().startswith("المادة")
        ]

        if len(parts) >= 5:
            return [
                {
                    "id": f"ar_article_{i}",
                    "title": extract_clause_title(part, language=language),
                    "text": part,
                    "number": (
                        re.match(r"المادة\s+([0-9٠-٩]+)", part).group(1)
                        if re.match(r"المادة\s+([0-9٠-٩]+)", part)
                        else ""
                    ),
                    "level": 1,
                    "depth": 1,
                    "parent_id": None,
                    "parent_clause_id": None,
                    "semantic_parent": None,
                    "section_path": [],
                    "children": [],
                    "confidence": 0.8,
                }
                for i, part in enumerate(
                    [
                        p for p in parts
                        if not is_non_clause_document_block(p)
                    ]
                )
            ]

    try:
        objects = parse_legal_document_objects(text)
    except (ValueError, KeyError, RecursionError, MemoryError, TimeoutError, Exception):
        objects = []

    objects = [
        obj for obj in objects
        if isinstance(obj, dict)
        and not is_non_clause_document_block(
            obj.get("text") or obj.get("title") or ""
        )
    ]

    fallback_clauses = [
        c for c in split_into_clauses(text)
        if not is_non_clause_document_block(c)
    ]

    if len(fallback_clauses) > len(objects):
        return [
            {
                "id": f"fallback_{i}",
                "title": extract_clause_title(clause, language=language),
                "text": clause,
                "number": extract_leading_clause_number(clause),
                "level": 1,
                "depth": 1,
                "parent_id": None,
                "parent_clause_id": None,
                "semantic_parent": None,
                "section_path": [],
                "children": [],
                "confidence": 0.6,
            }
            for i, clause in enumerate(fallback_clauses)
        ]

    if len(objects) >= 5:
        return objects

    return [
        {
            "id": f"fallback_{i}",
            "title": extract_clause_title(clause, language=language),
            "text": clause,
            "number": extract_leading_clause_number(clause),
            "level": 1,
            "depth": 1,
            "parent_id": None,
            "parent_clause_id": None,
            "semantic_parent": None,
            "section_path": [],
            "children": [],
            "confidence": 0.3,
        }
        for i, clause in enumerate(fallback_clauses)
    ]
