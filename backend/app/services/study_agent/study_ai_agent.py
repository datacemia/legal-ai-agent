import os
import json
import re
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# FINAL_HYBRID_VISUAL_DIAGRAM_ENGINE
# Safe base: Root -> Module
# Smart visual enrichment: Root -> Module -> source-supported children
STRICT_STRUCTURE_MODE = False
ENABLE_DEEP_DIAGRAM_MODE = False
ENABLE_SMART_ENRICHMENT = True
ENABLE_CHATGPT_LIKE_VISUAL = True

SYSTEM_PROMPT = """
You are Runexa Study Agent.

Your job is to help users learn faster from educational course or study material.

You must:
- Summarize the content clearly.
- Generate a short summary.
- Generate a written summary as one clear paragraph.
- Generate a visual summary as a structured text diagram.
- Generate a visual diagram in Mermaid mindmap format.
- Extract key learning points.
- Generate theoretical quiz questions.
- Generate practical quiz questions.
- Generate flashcards.
- Provide explanations for answers.
- Adapt the difficulty to the learner education level.
- Return the entire output in the requested output language.

CRITICAL CONTENT RULES:
- Use ONLY information explicitly present in the provided content.
- Do NOT add external knowledge.
- Do NOT guess.
- Do NOT invent missing information.
- Do NOT introduce generic concepts unless they are present in the content.
- Prefer accuracy over completeness.
- Do NOT create a study structure that is not supported by the text.

ADAPTIVE DIAGRAM ENGINE:
You are also a STRICT academic diagram extraction engine.

Your job for visual_diagram is to extract and organize knowledge into a clean Mermaid mindmap.

CRITICAL DIAGRAM RULES:

FINAL DIAGRAM QUALITY RULES:
- Every final leaf must be explicit and understandable alone.
- Avoid weak labels such as Contenu, Informations générales, Détails, Règles, Rapport, Documents associés, Situer, Par, Des.
- Prefer informative blocks with children over generic category labels.
- If a module has only weak labels, reduce it or use better supported concepts from the source.
- Do not split meaningful phrases into isolated words.
- Preserve complete terms such as Low cost, 30 heures, Évaluations écrites et orales.


1. NO INVENTION
- Do NOT create concepts not present in the text.
- If missing, OMIT it. Never invent.

2. STRUCTURE PRIORITY
- If clear sections or table of contents exist, use them.
- If no clear structure exists, infer a minimal safe structure from visible content only.

3. NO DUPLICATION
- Each concept appears ONLY once.
- If the same concept appears multiple times, keep it in the most precise branch.

4. HIERARCHY
- Root -> Sections -> Concepts.
- Max depth: 3.

VISUAL RULE:
- Parts must be visually dominant.
- Chapters must be grouped under parts.
- Avoid flat structures only when true hierarchy exists.
- Default SaaS diagram should stay clean and faithful, not over-detailed.
- Default hybrid SaaS mode must prefer safe structure:
  Root -> Module -> controlled source-supported children.
- Do NOT add uncontrolled subsections in default mode.
- Do NOT use uncontrolled body details as structure.
- Deep mode may use Root -> Module -> Explicit subsection only when explicitly enabled in code.
- Match module headings strictly.
- Stop at the next major heading.
- Do NOT include other TOC modules as children.
- Preserve pedagogical order such as A -> B -> C -> D -> E -> F.
- Do NOT invent subsections.

5. ADAPTIVE MODE
- If structure is clear, create a full structured diagram.
- If structure is partial, create a simplified structure.
- If structure is weak, create a minimal valid diagram.

6. NEVER FAIL
- NEVER output errors.
- NEVER say "analysis failed".
- ALWAYS return a valid diagram.
- Partial but correct output is better than empty output.

7. LANGUAGE
- Use the requested output language.
- Preserve source terms when possible.

8. CLEANING
- Ignore UI noise, menus, buttons, login labels, website footer text, console errors, and irrelevant metadata.

9. OUTPUT FORMAT
- visual_diagram must be valid Mermaid mindmap text.
- No markdown fences inside visual_diagram.
- No explanations inside visual_diagram.

10. QUALITY PRIORITY
- Prefer correct and incomplete over wrong and complete.
- If uncertain, produce a reduced but valid diagram.

FALLBACK RULE:
If the document is unclear, noisy, or weakly structured:
- Create a minimal Mermaid mindmap with:
  Root
    Main ideas, 2 to 5 max
      Keywords
- Never return empty or error.

COURSE ONLY RULE:
- This agent is strictly for educational course or study material.
- First decide whether the document is actually a course/study material.
- Course/study material may include: textbook chapter, lesson, lecture notes, training material, educational article, study guide, book, or organized learning content.
- If the document is NOT a course or study material (e.g. legal contract, invoice, administrative document, business spreadsheet, random text):
  - Do NOT transform it into a course.
  - Do NOT invent definitions, components, types, steps, quizzes, flashcards, or a study plan.
  - Clearly state that the document does not appear to be educational study material.
  - Briefly state the real nature of the document when recognizable.
  - Provide a short factual summary only.
  - Keep key_points minimal and factual.
  - Keep quiz empty.
  - Keep flashcards empty.
  - Keep study_plan empty.
  - Keep visual_diagram as a simple factual mindmap based only on the real document sections.

EMPTY OUTPUT PREVENTION RULE:
- For valid course/study material, flashcards must never be empty if the document has usable content.
- For valid course/study material, each flashcard must contain non-empty "front" and "back".
- For valid course/study material, study_plan must never be empty if the document has usable content.
- For non-course documents, keep flashcards and study_plan empty as required by COURSE ONLY RULE.

MERMAID SAFETY RULE:
- visual_diagram must always start with "mindmap".
- visual_diagram must contain real line breaks.
- Do not use markdown fences.
- Do not return plain text inside visual_diagram.

Rules:
- Theoretical questions test understanding.
- Practical questions test application using only concepts from the content.
- Each question must have 4 options.
- Include correct_answer.
- Include explanation.
- Flashcards must be simple and useful.
- Return ONLY valid JSON.
- Never return markdown.
- Never include explanations outside JSON.
"""




def get_language_name(output_language: str) -> str:
    languages = {
        "en": "English",
        "fr": "French",
        "ar": "Arabic",
    }
    return languages.get(output_language, "English")


def fallback_mermaid() -> str:
    return """mindmap
  root((Main topic))
    Idea 1
      Keyword
    Idea 2
      Keyword
    Idea 3
      Keyword"""


def remove_ui_noise(text: str) -> str:
    if not isinstance(text, str):
        return ""

    noise_phrases = [
        "Runexa Systems",
        "تسجيل الدخول",
        "إنشاء حساب",
        "تسجيل الخروج",
        "شراء رصيد",
        "اختيار ملف",
        "تحليل",
        "الأعمال",
        "الأسعار",
        "الشروط",
        "الخصوصية",
        "شروط المنتج",
        "Next.js",
        "Webpack",
        "Console Error",
        "Console ChunkLoadError",
    ]

    cleaned_lines = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue

        if any(phrase in stripped for phrase in noise_phrases):
            continue

        if len(stripped) <= 2:
            continue

        cleaned_lines.append(stripped)

    return "\n".join(cleaned_lines).strip()


def normalize_arabic(label: str) -> str:
    """
    Lightweight Arabic/OCR label normalization.
    Keeps meaning, removes extra spacing, and avoids aggressive rewriting.
    """
    if not isinstance(label, str):
        return ""

    label = re.sub(r"\s+", " ", label).strip()

    # Common harmless normalizations
    label = label.replace("الفصل 01", "الفصل 1")
    label = label.replace("الفصل :1", "الفصل 1:")
    label = label.replace("الفصل :2", "الفصل 2:")
    label = label.replace("الفصل :3", "الفصل 3:")
    label = label.replace("الفصل :4", "الفصل 4:")
    label = label.replace("الفصل :5", "الفصل 5:")
    label = label.replace("الفصل :6", "الفصل 6:")
    label = label.replace("الفصل :7", "الفصل 7:")
    label = label.replace("الفصل :8", "الفصل 8:")
    label = label.replace("الفصل :9", "الفصل 9:")
    label = label.replace("الفصل :10", "الفصل 10:")
    label = label.replace("الفصل :11", "الفصل 11:")
    label = label.replace("الفصل :12", "الفصل 12:")

    # Normalize common punctuation spacing
    label = label.replace(" :", ":")
    label = label.replace(": ", ": ")

    label = light_ocr_fix(label)
    return label.strip()


def light_ocr_fix(text: str) -> str:
    if not isinstance(text, str):
        return ""

    fixes = {
        # répétitions lettres
        "اااا": "ا",
        "أهلًاااااا": "أهلًا",

        # OCR mots
        "تحدِّ يات": "تحديات",
        "زٍمعزز": "معزز",
        "تسويقٍ": "تسويق",
        "التنبُّئي": "التنبؤي",
        "اللين:": "اللين",
        "اللي:": "اللين",

        # ponctuation cassée
        "النمو:استقطاب": "النمو: استقطاب",
        "التنبُّئي:التسويق": "التسويق التنبؤي",

        # numéros faux
        "الفصل 21": "الفصل 11",
        "الفصل 1:1": "الفصل 11",

        # French OCR / apostrophe fixes
        "dentreprises": "d'entreprises",
        "demplois": "d'emplois",
        "demploys": "d'emplois",
        "dentrerprises": "d'entreprises",
        "dévaluation": "d'évaluation",
        "devaluation": "d'évaluation",
    }

    for k, v in fixes.items():
        text = text.replace(k, v)

    return text


def clean_toc_label(label):
    if not isinstance(label, str):
        return ""

    label = light_ocr_fix(label)
    label = re.sub(r"\s+", " ", label).strip()

    # Remove trailing page numbers only when the label has enough text before them.
    # This avoids damaging titles such as "التسويق 5.0".
    label = re.sub(r"(?<=\D)\s+[0-9٠-٩]{1,4}$", "", label).strip()

    # enlever ponctuation bizarre but keep Arabic, Latin, digits, colon, dash, dot, spaces
    label = re.sub(r"[^\u0600-\u06FFa-zA-ZÀ-ÿ0-9٠-٩:\-–—\.\s]", "", label)

    # nettoyer espaces
    label = re.sub(r"\s+", " ", label)

    return label.strip()


def smart_truncate(label: str, max_len: int = 70) -> str:
    """
    Safe SaaS truncation.
    Does NOT cut words in the middle.
    """
    if not isinstance(label, str):
        return ""

    label = label.strip()

    if len(label) <= max_len:
        return label

    return safe_truncate(label, max_len=max_len)

def truncate_label(label: str, max_len: int = 70) -> str:
    """
    Backward-compatible wrapper.
    """
    return smart_truncate(label, max_len=max_len)



def detect_root_title(text: str, output_language: str = "ar") -> str:
    """
    Stable root detector with language support.
    Works for:
    - French training modules
    - Arabic / Marketing 5.0 books
    - generic courses
    """
    if not isinstance(text, str):
        return "Main topic" if output_language == "fr" else "الموضوع الرئيسي"

    fixed_text = light_ocr_fix(text)
    normalized = normalize_for_match(fixed_text)

    if "metier et formation" in normalized:
        return "Métier et formation" if output_language == "fr" else "مهنة وتكوين"

    if "marketing 5 0" in normalized or "التسويق 5.0" in fixed_text or "التسويق 5" in fixed_text:
        return "Marketing 5.0" if output_language == "fr" else "التسويق 5.0"

    if "manuel" in normalized and "formation" in normalized:
        return "Manuel de formation — Métiers vol" if output_language == "fr" else "دليل تدريب مهنة الطيران"

    # Prefer first short uppercase French course title.
    for line in fixed_text.splitlines()[:20]:
        raw = line.strip()
        if not raw:
            continue

        clean = clean_toc_label(raw)
        if len(clean) <= 80 and clean:
            letters = [c for c in clean if c.isalpha()]
            if letters:
                upper_ratio = sum(1 for c in letters if c.isupper()) / max(len(letters), 1)
                if upper_ratio > 0.65 and len(clean) >= 5:
                    return clean.title() if output_language == "fr" else clean

    # Generic Arabic / French / English heading fallback.
    for line in fixed_text.splitlines()[:20]:
        clean = clean_toc_label(line.strip())
        if clean and 5 <= len(clean) <= 80 and not re.match(r"^[0-9٠-٩]+$", clean):
            return clean

    return "Main topic" if output_language == "fr" else "الموضوع الرئيسي"


def extract_number(text: str) -> int:
    """
    Extracts the first visible Arabic/Latin number from a label for ordering.
    Used only as a safe helper for TOC grouping/order.
    """
    if not isinstance(text, str):
        return 999

    arabic_digit_map = str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")
    normalized = text.translate(arabic_digit_map)

    match = re.search(r"\d+", normalized)
    return int(match.group()) if match else 999



def clean_toc_numbering(label: str) -> str:
    """
    Removes leading TOC numbering:
    1 – Title
    1- Title
    1. Title
    ١ – عنوان
    """
    if not isinstance(label, str):
        return ""

    label = label.strip()
    label = re.sub(r"^[0-9٠-٩]+\s*[-–—.]\s*", "", label)
    label = re.sub(r"^[0-9٠-٩]+\s+", "", label)

    return label.strip()



def detect_table_of_contents(text: str) -> list[str]:
    """
    General hard TOC detection.

    Supports:
    - French: Table des matières
    - Arabic: المحتويات / الفهرس
    - English: Table of Contents

    Rule:
    If TOC exists, capture numbered TOC entries only.
    Do not mix with body content.
    """
    if not isinstance(text, str):
        return []

    lines = [line.strip() for line in text.splitlines()]
    toc = []
    capture = False
    empty_after_start = 0

    toc_markers = [
        "Table des matières",
        "TABLE DES MATIÈRES",
        "Table of Contents",
        "TABLE OF CONTENTS",
        "المحتويات",
        "الفهرس",
    ]

    for line in lines:
        line = light_ocr_fix(line.strip())

        # START
        if any(marker in line for marker in toc_markers):
            capture = True
            empty_after_start = 0
            continue

        if not capture:
            continue

        # STOP after TOC if blank appears after entries
        if not line:
            empty_after_start += 1
            if toc and empty_after_start >= 1:
                break
            continue

        empty_after_start = 0

        # Stop when a real section body begins after TOC
        if toc and (
            line.isupper() and len(line) > 8 and not re.match(r"^[0-9٠-٩]", line)
        ):
            break

        # Keep numbered lines only
        if re.match(r"^[0-9٠-٩]+\s*[-–—.]\s*\S+", line) or re.match(r"^[0-9٠-٩]+\s+\S+", line):
            cleaned = clean_toc_label(line)
            if cleaned:
                toc.append(cleaned)

        # Also keep explicit part/chapter lines if present inside TOC
        elif any(marker in line for marker in ["الجزء", "الفصل", "Part", "Chapter"]):
            cleaned = clean_toc_label(line)
            if cleaned:
                toc.append(cleaned)

        if len(toc) >= 80:
            break

    return sort_toc_items(toc)


def sort_toc_items(items: list[str]) -> list[str]:
    """
    Sorts and cleans TOC items.

    If parts are present:
    preserves part -> chapter grouping.

    If no parts are present:
    returns a simple numbered module list in original/numeric order.
    """
    if not isinstance(items, list):
        return []

    cleaned_items = []
    for item in items:
        label = clean_toc_label(item)
        if not label:
            continue
        cleaned_items.append(label)

    cleaned_items = deduplicate_nodes(cleaned_items)

    has_parts = any("الجزء" in item or "Part" in item for item in cleaned_items)

    if not has_parts:
        return sorted(cleaned_items, key=extract_number)

    groups = []
    current_group = None
    loose_items = []

    for item in cleaned_items:
        if "الجزء" in item or "Part" in item:
            current_group = {
                "part": item,
                "chapters": [],
            }
            groups.append(current_group)
        elif ("الفصل" in item or "Chapter" in item) and current_group:
            current_group["chapters"].append(item)
        else:
            if current_group:
                current_group["chapters"].append(item)
            else:
                loose_items.append(item)

    groups.sort(key=lambda g: extract_number(g["part"]))

    output = []
    output.extend(sorted(loose_items, key=extract_number))

    for group in groups:
        output.append(group["part"])
        chapters = sorted(group["chapters"], key=extract_number)
        output.extend(chapters)

    return deduplicate_nodes(output)


def extract_sections(text: str) -> list[str]:
    """
    Strong generic section detector for course PDFs.

    Detects:
    - A - / B - / C - modules
    - 1. / 1- numbered chapters
    - Arabic numbered headings
    - short uppercase titles
    - colon-based headings

    Goal:
    Avoid falling back to "Main topic / Idea / Keyword" when a real course
    has visible module headings.
    """
    if not isinstance(text, str):
        return []

    sections = []

    patterns = [
        r"^\s*[A-Z]\s*[-–:]\s+\S+.*$",          # A - Fonction...
        r"^\s*الفصل\s*[:：]?\s*\d+.*$",
        r"^\s*الجزء\s+.*$",
        r"^\s*المادة\s+\d+.*$",
        r"^\s*\d+\s*[\.\-–]\s+.*$",
        r"^\s*[٠-٩]+\s*[\.\-–]\s+.*$",
        r"^\s*.+:$",
    ]

    for line in text.splitlines():
        stripped = light_ocr_fix(line.strip())
        if not stripped:
            continue

        if len(stripped) > 140:
            continue

        if any(re.match(pattern, stripped) for pattern in patterns):
            cleaned = clean_toc_label(stripped)
            if cleaned:
                sections.append(truncate_label(cleaned))
            continue

        # Short uppercase French/English headings often appear in PDFs.
        letters = [c for c in stripped if c.isalpha()]
        if letters:
            upper_ratio = sum(1 for c in letters if c.isupper()) / max(len(letters), 1)
            if upper_ratio > 0.75 and 5 <= len(stripped) <= 80:
                cleaned = clean_toc_label(stripped)
                if cleaned:
                    sections.append(truncate_label(cleaned))

    return deduplicate_nodes(sections)

def extract_keywords(text: str, max_keywords: int = 8) -> list[str]:
    if not isinstance(text, str):
        return []

    stop_words = {
        "في", "من", "على", "إلى", "عن", "أن", "إن", "هو", "هي", "هذا", "هذه",
        "the", "and", "of", "to", "in", "is", "are", "a", "an"
    }

    words = []
    for token in re.findall(r"[\u0600-\u06FFa-zA-Z0-9\.]+", text):
        token = token.strip()
        if len(token) < 3:
            continue
        if token.lower() in stop_words:
            continue
        words.append(token)

    counts = {}
    for word in words:
        counts[word] = counts.get(word, 0) + 1

    ranked = sorted(counts.items(), key=lambda item: item[1], reverse=True)
    return [word for word, _ in ranked[:max_keywords]]


def deduplicate_nodes(items: list[str]) -> list[str]:
    """
    Safe deduplication WITHOUT destroying enriched labels.
    Important:
    - Do not call clean_toc_label here after expand_keyword.
    - Keep phrases such as "Définir ses objectifs" and "Communication efficace".
    """
    if not isinstance(items, list):
        return []

    seen = set()
    output = []

    for item in items:
        label = safe_text(item).strip()

        if not label:
            continue

        normalized = normalize_for_match(label)

        if normalized in seen:
            continue

        seen.add(normalized)
        output.append(label)

    return output


def is_valid_chapter_for_part(part_label, chapter_label):
    p = extract_number(part_label)
    c = extract_number(chapter_label)

    if not p or not c:
        return False

    if p == 1:
        return c == 1
    elif p == 2:
        return c in [2, 3, 4]
    elif p == 3:
        return c in [5, 6, 7]
    elif p == 4:
        return c in [8, 9, 10, 11]

    return False


def normalize_for_match(text: str) -> str:
    """
    Normalizes titles for safe matching.
    Used only to locate explicit headings already present in the document.
    """
    if not isinstance(text, str):
        return ""

    text = light_ocr_fix(text)
    text = clean_toc_numbering(text)
    text = clean_toc_label(text)
    text = text.lower()

    replacements = {
        "é": "e", "è": "e", "ê": "e", "ë": "e",
        "à": "a", "â": "a",
        "î": "i", "ï": "i",
        "ô": "o",
        "ù": "u", "û": "u",
        "ç": "c",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    text = re.sub(r"[^a-z0-9\u0600-\u06FF\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    return text


def is_clear_major_heading(line: str) -> bool:
    """
    Detects a major heading that can stop subsection capture.
    Conservative to avoid false splits.
    """
    if not isinstance(line, str):
        return False

    stripped = line.strip()

    if not stripped:
        return False

    if len(stripped) > 80:
        return False

    # French uppercase headings often appear as module starts.
    letters = [c for c in stripped if c.isalpha()]
    if letters:
        upper_ratio = sum(1 for c in letters if c.isupper()) / max(len(letters), 1)
        if upper_ratio > 0.75 and len(stripped) >= 8:
            return True

    # Arabic/English/French explicit module/chapter starts.
    if any(marker in stripped for marker in ["METIER", "ENVIRONNEMENT", "الفصل", "الجزء", "Chapter", "Part"]):
        return True

    return False


def extract_explicit_subsections_for_module(text: str, module_title: str, max_children: int = 3) -> list[str]:
    """
    Extracts only explicit LOCAL subsections under the exact module heading.

    Strict rules:
    - Match ONLY the exact module heading.
    - Stop immediately at the next major heading.
    - Never include other TOC modules as children.
    - Max 3 children for clean SaaS UI.
    """
    if not isinstance(text, str) or not isinstance(module_title, str):
        return []

    module_key = normalize_for_match(module_title)
    if not module_key:
        return []

    module_keywords = [
        "Métier", "Environnement", "Comportements",
        "Interaction", "Procédures", "Embarquement",
        "Service", "Vente", "Arrivée",
        "Metier", "Procedures", "Arrivee"
    ]

    lines = [line.strip() for line in text.splitlines() if line.strip()]
    start_index = None

    for idx, line in enumerate(lines):
        line_key = normalize_for_match(line)

        # STRICT MATCH ONLY
        if line_key == module_key:
            start_index = idx
            break

    if start_index is None:
        return []

    children = []

    for line in lines[start_index + 1:]:
        stripped = line.strip()

        if not stripped:
            continue

        # STRICT STOP: stop at any major heading, even before children exist.
        if is_clear_major_heading(stripped):
            break

        # Anti-module filter: never include other TOC modules as children.
        if any(keyword in stripped for keyword in module_keywords):
            continue

        # A- / B- / C- headings
        letter_match = re.match(r"^[A-Z]\s*[-–]\s*(.+)$", stripped)
        if letter_match:
            child = clean_toc_label(letter_match.group(1))
            child = smart_truncate(child, 55)
            if child and child not in children:
                children.append(child)
            if len(children) >= max_children:
                break
            continue

        # 1- / 2- headings
        number_match = re.match(r"^[0-9٠-٩]+\s*[-–]\s*(.+)$", stripped)
        if number_match:
            child = clean_toc_label(number_match.group(1))
            child = smart_truncate(child, 55)
            if child and child not in children:
                children.append(child)
            if len(children) >= max_children:
                break
            continue

    return children[:max_children]


def extract_letter_order(label: str) -> str:
    """
    Extracts A-F order from labels like:
    A - Fonction...
    B - Types...
    """
    if not isinstance(label, str):
        return "Z"

    match = re.match(r"^\s*([A-F])\s*[-–:]", label.strip(), flags=re.IGNORECASE)
    return match.group(1).upper() if match else "Z"


def semantic_order(label: str) -> int:
    """
    Keeps children in pedagogical order when labels are known.
    Unknown items keep natural alphabetical fallback after known ones.
    """
    if not isinstance(label, str):
        return 999

    normalized = normalize_for_match(label)

    order = {
        "le transport aerien": 1,
        "qualites requises": 2,
        "conditions": 3,

        "compagnies regulieres": 1,
        "low cost": 2,
        "charters": 3,
        "evolution": 4,

        "droits": 1,
        "obligations": 2,

        "modules": 1,
        "evaluations": 2,

        "forces": 1,
        "objectifs": 2,

        "respect": 1,
        "regles de communication": 2,
    }

    for key, value in order.items():
        if key in normalized:
            return value

    return 900 + extract_number(label)






def is_letter_module(label: str) -> bool:
    """
    Detects course modules like:
    A - Fonction...
    B - Types...
    """
    if not isinstance(label, str):
        return False
    return bool(re.match(r"^\s*[A-Z]\s*[-–:]", label.strip(), flags=re.IGNORECASE))


def filter_main_modules(items: list[str]) -> list[str]:
    """
    Keeps main explicit modules when they exist.
    This prevents local subheadings such as Qualités, Conditions, Evolution
    from becoming top-level nodes.
    """
    if not isinstance(items, list):
        return []

    cleaned = []
    for item in items:
        label = clean_toc_numbering(clean_toc_label(safe_text(item).strip()))
        if label:
            cleaned.append(label)

    letter_modules = [item for item in cleaned if is_letter_module(item)]

    if letter_modules:
        return sorted(
            deduplicate_nodes(letter_modules),
            key=lambda item: (extract_letter_order(item), extract_number(item), normalize_for_match(item)),
        )

    return sorted(
        deduplicate_nodes(cleaned),
        key=lambda item: (extract_letter_order(item), extract_number(item), normalize_for_match(item)),
    )


def extract_keywords_from_text(text: str, candidates: list[str]) -> list[str]:
    """
    Controlled keyword extractor.
    Returns only candidate concepts explicitly present in the text.
    No invention.
    """
    if not isinstance(text, str) or not isinstance(candidates, list):
        return []

    normalized_text = normalize_for_match(text)
    found = []

    for candidate in candidates:
        candidate_text = safe_text(candidate).strip()
        candidate_key = normalize_for_match(candidate_text)

        if not candidate_key:
            continue

        if candidate_key in normalized_text:
            found.append(candidate_text)

    return deduplicate_nodes(found)


def extract_local_list_items(text: str, heading_keywords: list[str], max_items: int = 3) -> list[str]:
    """
    Finds a visible heading and extracts bullet-like items that follow it.
    Safe for ChatGPT-like visual maps:
    - only items explicitly present
    - max_items cap
    """
    if not isinstance(text, str) or not isinstance(heading_keywords, list):
        return []

    lines = [line.strip() for line in text.splitlines() if line.strip()]
    heading_keys = [normalize_for_match(k) for k in heading_keywords]

    start = None
    for i, line in enumerate(lines):
        line_key = normalize_for_match(line)
        if any(k and k in line_key for k in heading_keys):
            start = i
            break

    if start is None:
        return []

    output = []
    for line in lines[start + 1:]:
        stripped = line.strip()

        if not stripped:
            continue

        if is_clear_major_heading(stripped) or re.match(r"^[A-Z]\s*[-–:]", stripped):
            break

        # bullet item
        bullet = re.match(r"^[-•]\s*(.+)$", stripped)
        if bullet:
            item = clean_toc_label(bullet.group(1))
            if item:
                output.append(smart_truncate(item, 55))

        # short colon inline facts
        elif len(stripped) <= 70 and ":" not in stripped:
            # avoid full paragraphs
            if len(stripped.split()) <= 7:
                output.append(smart_truncate(clean_toc_label(stripped), 55))

        if len(output) >= max_items:
            break

    return deduplicate_nodes(output[:max_items])


def expand_keyword(keyword: str) -> str:
    """
    Converts raw extracted keywords into cleaner visual labels.
    Keeps output readable while staying source-supported.
    """
    if not isinstance(keyword, str):
        return ""

    keyword = keyword.strip()

    mapping = {
        "objectifs": "Définir ses objectifs",
        "forces": "Identifier ses forces",
        "communication": "Communication efficace",
        "discussion": "Respect des règles de discussion",
        "respect": "Respect des règles",
        "modules": "Modules de formation",
        "évaluations écrites": "Évaluations écrites",
        "evaluations écrites": "Évaluations écrites",
        "évaluations orales": "Évaluations orales",
        "evaluations orales": "Évaluations orales",
        "conditions": "Conditions de travail",
        "qualités requises": "Qualités requises",
        "qualites requises": "Qualités requises",
    }

    return mapping.get(keyword.lower(), keyword.capitalize())


def strip_module_prefix(label: str) -> str:
    """
    Removes common module prefixes while keeping the real course title.

    Examples:
    A - Fonction -> Fonction
    1. Introduction -> Introduction
    الفصل 1: ... -> ...
    """
    label = safe_text(label).strip()
    label = clean_toc_numbering(label)
    label = re.sub(r"^[A-Z]\s*[-–:]\s*", "", label, flags=re.IGNORECASE).strip()
    label = re.sub(r"^[0-9٠-٩]+\s*[-–.:]\s*", "", label).strip()
    return label


def looks_like_bullet(line: str) -> bool:
    if not isinstance(line, str):
        return False
    return bool(re.match(r"^\s*[-•*]\s+\S+", line.strip()))


def looks_like_subheading(line: str) -> bool:
    """
    Generic course subheading detector.
    It is intentionally conservative to avoid turning paragraphs into nodes.
    """
    if not isinstance(line, str):
        return False

    stripped = line.strip()
    if not stripped:
        return False

    if looks_like_bullet(stripped):
        return False

    if len(stripped) > 90:
        return False

    if re.match(r"^[A-Z]\s*[-–:]\s+\S+", stripped, flags=re.IGNORECASE):
        return True

    if re.match(r"^[0-9٠-٩]+\s*[-–.:]\s+\S+", stripped):
        return True

    if stripped.endswith(":") and len(stripped.split()) <= 8:
        return True

    letters = [c for c in stripped if c.isalpha()]
    if letters:
        upper_ratio = sum(1 for c in letters if c.isupper()) / max(len(letters), 1)
        if upper_ratio > 0.70 and 4 <= len(stripped) <= 70:
            return True

    # Short noun-like course headings.
    if len(stripped.split()) <= 5 and not stripped.endswith("."):
        return True

    return False


def extract_module_body(text: str, module_label: str) -> str:
    """
    Extracts the local body of one module/chapter.

    Works for many domains because it searches the real module heading
    and stops at the next major heading or next A/B/C module.
    """
    if not isinstance(text, str) or not isinstance(module_label, str):
        return ""

    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return ""

    module_key = normalize_for_match(module_label)
    module_key_no_prefix = normalize_for_match(strip_module_prefix(module_label))

    start_index = None

    for idx, line in enumerate(lines):
        line_key = normalize_for_match(line)

        if not line_key:
            continue

        if line_key == module_key:
            start_index = idx
            break

        if module_key_no_prefix and line_key == module_key_no_prefix:
            start_index = idx
            break

        # Flexible match for OCR or TOC/body differences.
        if module_key_no_prefix and module_key_no_prefix in line_key and len(module_key_no_prefix) >= 8:
            start_index = idx
            break

    if start_index is None:
        return ""

    body_lines = []

    for line in lines[start_index + 1:]:
        stripped = line.strip()

        if not stripped:
            continue

        # Stop at next A/B/C module or numbered chapter.
        if re.match(r"^[A-Z]\s*[-–:]\s+\S+", stripped, flags=re.IGNORECASE):
            break

        if re.match(r"^[0-9٠-٩]+\s*[-–.]\s+\S+", stripped):
            break

        if body_lines and is_clear_major_heading(stripped):
            break

        body_lines.append(stripped)

        if len(body_lines) >= 120:
            break

    return "\n".join(body_lines).strip()


# Mindmap quality controls
MAX_NODE_WORDS = 4
MIN_BLOCKS_PER_RICH_MODULE = 2
MAX_BLOCKS_PER_MODULE = 3
MAX_DETAILS_PER_BLOCK = 5


def simplify_label(label: str, output_language: str = "fr") -> str:
    """
    Node simplification engine.

    Goal:
    - short labels
    - no sentence-like nodes
    - cleaner mindmap rendering
    - generic across domains
    """
    label = safe_text(label).strip()
    if not label:
        return ""

    label = light_ocr_fix(label)
    label = clean_toc_label(label)
    label = re.sub(r"\s+", " ", label).strip()
    label = label.strip(" .;:,،؛")

    numeric_unit_match = re.search(r"\b\d+\s*(heures?|hours?|minutes?)\b", label, flags=re.IGNORECASE)
    if numeric_unit_match:
        return numeric_unit_match.group(0)

    if not label:
        return ""

    normalized = normalize_for_match(label)

    # French-heavy generic simplifications
    replacements_fr = {
        "respect des règles de communication": "Communication",
        "respect des règles de": "Règles",
        "des": "",
        "gles": "Règles",
        "respect des règles de discussion": "Discussion",
        "règles de communication": "Communication",
        "règles de discussion": "Discussion",
        "identifier ses forces et objectifs": "Forces et objectifs",
        "identifier ses forces": "Forces",
        "identifier ses points à améliorer": "Points à améliorer",
        "définir ses objectifs": "Objectifs",
        "construire sa carrière": "Carrière",
        "évaluations écrites et orales": "Évaluations",
        "modules avec évaluations écrites et orales": "Modules et évaluations",
        "bonne condition physique": "Condition physique",
        "hôtesse/steward": "Hôtesse / Steward",
        "hôtesse steward": "Hôtesse / Steward",
        "types d’entreprises": "Types d’entreprises",
        "types d'entreprises": "Types d’entreprises",
        "fonction et conditions de travail": "Fonction et conditions",
        "droits et responsabilités": "Droits et responsabilités",
        "projet professionnel": "Projet professionnel",
        "travail en équipe": "Travail en équipe",
    }

    replacements_en = {
        "rules of communication": "Communication",
        "rules of discussion": "Discussion",
        "written and oral evaluations": "Evaluations",
        "identify strengths and objectives": "Strengths and goals",
        "define objectives": "Objectives",
        "build career": "Career",
    }

    replacements_ar = {
        "قواعد التواصل": "التواصل",
        "قواعد النقاش": "النقاش",
        "تحديد نقاط القوة والأهداف": "القوة والأهداف",
        "التقييمات الكتابية والشفوية": "التقييمات",
    }

    replacement_sets = []
    if output_language == "ar":
        replacement_sets = [replacements_ar, replacements_fr, replacements_en]
    elif output_language == "en":
        replacement_sets = [replacements_en, replacements_fr, replacements_ar]
    else:
        replacement_sets = [replacements_fr, replacements_en, replacements_ar]

    for mapping in replacement_sets:
        for src_label, dst_label in mapping.items():
            if normalize_for_match(src_label) == normalized:
                return dst_label

    # Remove heavy prefixes while preserving meaning.
    prefix_patterns = [
        r"^respect\s+des\s+règles\s+de\s+",
        r"^identifier\s+ses\s+",
        r"^définir\s+ses\s+",
        r"^les\s+",
        r"^des\s+",
        r"^de\s+la\s+",
        r"^du\s+",
        r"^the\s+",
        r"^rules\s+of\s+",
    ]

    simplified = label
    for pattern in prefix_patterns:
        simplified = re.sub(pattern, "", simplified, flags=re.IGNORECASE).strip()

    # Keep slash labels intact.
    if "/" in simplified and len(simplified.split()) <= 4:
        return simplified

    # Avoid cutting important module titles too aggressively.
    words = simplified.split()
    if len(words) > MAX_NODE_WORDS:
        simplified = " ".join(words[:MAX_NODE_WORDS])

    return simplified[:1].upper() + simplified[1:] if simplified else ""


def is_too_short(label: str) -> bool:
    """
    Removes weak/truncated labels such as 'Par', 'Des', 'Dur'.
    Keeps numeric values such as '30 heures'.
    """
    if not isinstance(label, str):
        return True

    label = label.strip()

    if not label:
        return True

    if any(char.isdigit() for char in label):
        return False

    return len(label) <= 3


def safe_truncate(label: str, max_len: int = 60) -> str:
    """
    Truncates without cutting words.
    """
    if not isinstance(label, str):
        return ""

    label = label.strip()

    if len(label) <= max_len:
        return label

    words = label.split()
    result = ""

    for word in words:
        candidate = (result + " " + word).strip()

        if len(candidate) > max_len:
            break

        result = candidate

    return result.strip()


def polish_leaf_label(label: str) -> str:
    """
    Safe final polish for leaf labels.
    Keeps meaning but improves readability.
    """
    key = normalize_for_match(label)

    replacements = {
        "respect des regles de communication": "Communication",
        "respect des regles de discussion": "Discussion",
        "respect du contrat": "Contrat",
        "bonne condition physique": "Condition physique",
        "identifier ses objectifs": "Objectifs",
        "identifier ses forces": "Forces",
        "low": "Low cost",
        "dur": "Durée",
    }

    return replacements.get(key, label)


def polish_block_label(label: str) -> str:
    """
    Safe final polish for block labels.
    Non-destructive and multi-domain friendly.
    """
    key = normalize_for_match(label)

    mapping = {
        "modules": "Modules de formation",
        "evolution": "Parcours",
        "types": "Types",
    }

    return mapping.get(key, label)

def clean_node_label(label: str, max_len: int = 70, output_language: str = "fr") -> str:
    """
    Clean + simplify node label for professional mindmaps.
    Removes weak/truncated leaves and truncates safely without cutting words.
    Preserves useful numeric-unit values like '30 heures'.
    Applies final safe polish for readability.
    """
    raw_label = safe_text(label).strip()

    numeric_unit_match = re.search(
        r"\b\d+\s*(heures?|hours?|minutes?)\b",
        raw_label,
        flags=re.IGNORECASE,
    )
    if numeric_unit_match:
        return numeric_unit_match.group(0)

    label = clean_toc_label(raw_label)
    label = strip_module_prefix(label)
    label = label.replace(" :", ":").strip()
    label = simplify_label(label, output_language=output_language)
    label = polish_leaf_label(label)

    if is_too_short(label):
        return ""

    return safe_truncate(label, max_len=max_len)

def split_compound_learning_item(item: str, output_language: str = "fr") -> list[str]:
    """
    Safe compound splitter.

    Important:
    - Never split a sentence into isolated words.
    - Only split known pedagogical compound concepts.
    - Prevents broken nodes like "Des" or "Gles".
    """
    item = safe_text(item).strip()
    if not item:
        return []

    normalized = normalize_for_match(item)

    if "communication" in normalized and "discussion" in normalized:
        return ["Communication", "Discussion"]

    if "forces" in normalized and "objectifs" in normalized:
        return ["Forces", "Objectifs"]

    if "ecrites" in normalized and "orales" in normalized:
        return ["Évaluations écrites", "Évaluations orales"]

    if "modules" in normalized and "evaluations" in normalized:
        return ["Modules", "Évaluations"]

    if "droits" in normalized and "responsabilites" in normalized:
        return ["Droits", "Responsabilités"]

    return [clean_node_label(item, 65, output_language=output_language)]

def rebalance_blocks(blocks, module_label: str = "", output_language: str = "fr") -> list[dict]:
    """
    Final quality layer for high-quality multi-domain mindmaps.

    Core rule:
    A good block must be informative.

    Fixes:
    - removes weak blocks like "Contenu", "Règles", "Détails"
    - removes unit-only noise like "heures" while preserving "30 heures"
    - splits colon-based nodes safely
    - prevents broken one-word artifacts
    - falls back to auto_group_items when blocks are too weak
    """
    if not isinstance(blocks, list):
        return []

    broken_labels = {
        "", "des", "de", "du", "gles", "règles", "les", "et", "ou",
        "the", "of", "and", "or",
    }

    unit_only_noise = {
        "heures", "heure", "hours", "hour",
        "minutes", "minute",
    }

    def is_weak_block(label: str) -> bool:
        weak = [
            "contenu", "content",
            "element", "elements", "élément", "éléments",
            "divers", "autres", "others",
            "regle", "regles", "règle", "règles", "rules",
            "information", "informations",
            "detail", "details", "détail", "détails",
            "points clés", "key elements",
        ]
        return normalize_for_match(label) in {normalize_for_match(x) for x in weak}

    def is_good_label(value: str) -> bool:
        key = normalize_for_match(value)

        if key in broken_labels:
            return False

        if key in unit_only_noise:
            return False

        if len(key) <= 2:
            return False

        return True

    def expand_colon_item(value: str):
        value = safe_text(value).strip()
        if ":" not in value:
            return None

        left, right = value.split(":", 1)
        label = clean_node_label(left, 55, output_language=output_language)

        right = right.strip()
        children = []

        # Preserve numeric-unit values like "30 heures" as one child.
        numeric_unit = re.search(
            r"\b\d+\s*(heures?|hours?|minutes?)\b",
            right,
            flags=re.IGNORECASE,
        )
        if numeric_unit:
            children.append(numeric_unit.group(0))
        else:
            raw_values = re.split(r"[,;،]| et | and |\s{2,}", right)

            for raw in raw_values:
                raw = raw.strip()
                if not raw:
                    continue

                # Split compact lists only when they are short and non-numeric.
                words = raw.split()
                if len(words) > 1 and len(words) <= 4 and not any(ch.isdigit() for ch in raw):
                    children.extend(words)
                else:
                    children.append(raw)

        children = [
            clean_node_label(child, 60, output_language=output_language)
            for child in children
            if clean_node_label(child, 60, output_language=output_language)
        ]

        children = [child for child in children if is_good_label(child)]

        if label and children and is_good_label(label) and not is_weak_block(label):
            return {
                "label": label,
                "children": deduplicate_nodes(children)[:MAX_DETAILS_PER_BLOCK],
            }

        return None

    cleaned_blocks = []
    flat_items = []

    for block in blocks:
        if isinstance(block, dict):
            raw_label = safe_text(block.get("label", "")).strip()
            colon_block = expand_colon_item(raw_label)

            if colon_block:
                cleaned_blocks.append(colon_block)
                continue

            label = clean_node_label(raw_label, 55, output_language=output_language)
            children = []

            for child in block.get("children", []):
                colon_child = expand_colon_item(child)

                if colon_child:
                    cleaned_blocks.append(colon_child)
                    continue

                children.extend(split_compound_learning_item(child, output_language=output_language))

            children = [
                clean_node_label(child, 60, output_language=output_language)
                for child in children
                if clean_node_label(child, 60, output_language=output_language)
            ]

            children = [child for child in deduplicate_nodes(children) if is_good_label(child)]

            # Informative block: keep label + children.
            if label and is_good_label(label) and children and not is_weak_block(label):
                cleaned_blocks.append({
                    "label": label,
                    "children": children[:MAX_DETAILS_PER_BLOCK],
                })

            # Weak block: do not keep its label, but recycle children.
            elif children:
                flat_items.extend(children)

            elif label and is_good_label(label) and not is_weak_block(label):
                flat_items.append(label)

        else:
            colon_block = expand_colon_item(block)

            if colon_block:
                cleaned_blocks.append(colon_block)
            else:
                flat_items.extend(split_compound_learning_item(block, output_language=output_language))

    # If we have weak/empty structure, regroup the useful items.
    if len(cleaned_blocks) < MIN_BLOCKS_PER_RICH_MODULE:
        regroup_source = flat_items[:]

        for block in cleaned_blocks:
            regroup_source.extend(block.get("children", []))

        regroup_source = deduplicate_nodes([
            clean_node_label(item, 60, output_language=output_language)
            for item in regroup_source
            if clean_node_label(item, 60, output_language=output_language)
        ])

        regroup_source = [item for item in regroup_source if is_good_label(item)]

        if len(regroup_source) >= 2:
            regrouped = auto_group_items(
                regroup_source,
                output_language=output_language,
                max_groups=MAX_BLOCKS_PER_MODULE,
                max_items=MAX_DETAILS_PER_BLOCK,
            )

            # Replace weak blocks with more meaningful automatic groups.
            if regrouped:
                cleaned_blocks = regrouped

    if not cleaned_blocks and flat_items:
        flat_items = [
            clean_node_label(item, 60, output_language=output_language)
            for item in flat_items
            if clean_node_label(item, 60, output_language=output_language)
        ]

        flat_items = [item for item in deduplicate_nodes(flat_items) if is_good_label(item)]

        cleaned_blocks = auto_group_items(
            flat_items,
            output_language=output_language,
            max_groups=MAX_BLOCKS_PER_MODULE,
            max_items=MAX_DETAILS_PER_BLOCK,
        )

    final_blocks = []
    seen_blocks = set()

    for block in cleaned_blocks:
        if not isinstance(block, dict):
            continue

        label = clean_node_label(block.get("label", ""), 55, output_language=output_language)
        label = polish_block_label(label)

        if not label or not is_good_label(label) or is_weak_block(label):
            # Do not keep weak block labels in final output.
            continue

        block_key = normalize_for_match(label)
        if block_key in seen_blocks:
            continue

        seen_blocks.add(block_key)

        children = [
            clean_node_label(child, 60, output_language=output_language)
            for child in block.get("children", [])
            if clean_node_label(child, 60, output_language=output_language)
        ]

        children = deduplicate_nodes(children)

        children = [
            child for child in children
            if is_good_label(child)
            and normalize_for_match(child) != normalize_for_match(label)
        ]

        final_blocks.append({
            "label": label,
            "children": children[:MAX_DETAILS_PER_BLOCK],
        })

        if len(final_blocks) >= MAX_BLOCKS_PER_MODULE:
            break

    return final_blocks

def normalize_module_label(label: str, output_language: str = "fr") -> str:
    """
    Simplifies module labels without destroying their identity.
    """
    label = safe_text(label).strip()
    if not label:
        return ""

    original = clean_toc_label(label)
    without_prefix = strip_module_prefix(original)

    # Prefer stripped version for A/B/C modules.
    if without_prefix and len(without_prefix) >= 3:
        label = without_prefix
    else:
        label = original

    return simplify_label(label, output_language=output_language)

def extract_generic_blocks_from_body(body: str, max_blocks: int = 3, max_items: int = 4) -> list[dict]:
    """
    Converts local course body into:
    [
      {"label": "Subheading", "children": ["item", "item"]}
    ]

    Generic rules:
    - subheadings become level 2
    - bullets/short items become level 3
    - paragraphs are not forced into the diagram
    """
    if not isinstance(body, str) or not body.strip():
        return []

    lines = [line.strip() for line in body.splitlines() if line.strip()]
    blocks = []
    current = None

    def push_current():
        nonlocal current
        if current and current.get("label"):
            current["children"] = deduplicate_nodes(current.get("children", []))[:max_items]
            blocks.append(current)
        current = None

    for raw in lines:
        line = raw.strip()
        if not line:
            continue

        bullet_match = re.match(r"^[-•*]\s*(.+)$", line)

        if bullet_match:
            item = clean_node_label(bullet_match.group(1), 65)
            if item:
                if current is None:
                    current = {"label": "Points clés", "children": []}
                current["children"].append(item)
            continue

        if looks_like_subheading(line):
            push_current()
            heading = clean_node_label(line, 65)
            if heading:
                current = {"label": heading, "children": []}
            continue

        # Capture short factual lines under an existing block only.
        if current is not None and len(line.split()) <= 8 and not line.endswith("."):
            item = clean_node_label(line, 65)
            if item:
                current["children"].append(item)

        if len(blocks) >= max_blocks:
            break

    push_current()

    # Remove empty blocks and keep balanced output.
    cleaned = []
    seen = set()

    for block in blocks:
        label = clean_node_label(block.get("label", ""), 65)
        if not label:
            continue

        normalized = normalize_for_match(label)
        if normalized in seen:
            continue

        seen.add(normalized)

        children = [
            clean_node_label(child, 65)
            for child in block.get("children", [])
            if clean_node_label(child, 65)
        ]

        cleaned.append({
            "label": label,
            "children": deduplicate_nodes(children)[:max_items],
        })

        if len(cleaned) >= max_blocks:
            break

    return cleaned


def extract_generic_keywords_as_blocks(text: str, module_label: str, max_items: int = 4) -> list[dict]:
    """
    Last safe fallback for any domain:
    creates one generic block from explicit keywords visible near the module.
    """
    body = extract_module_body(text, module_label)
    source = body if body else text

    keywords = extract_keywords(source, max_keywords=max_items)

    keywords = [
        clean_node_label(keyword, 55)
        for keyword in keywords
        if clean_node_label(keyword, 55)
    ]

    keywords = deduplicate_nodes(keywords)[:max_items]

    if not keywords:
        return []

    return [{
        "label": "Points clés",
        "children": keywords,
    }]


def auto_group_items(items, output_language: str = "fr", max_groups: int = 3, max_items: int = 4):
    """
    Universal auto-block intelligence for ANY course/domain.

    No domain-specific hardcoding.
    Groups flat course items into generic pedagogical blocks:
    Concepts, Types, Characteristics, Conditions, Methods/Process, Rules,
    Formulas, Examples, Applications, Results/Limits.
    """
    if not isinstance(items, list):
        return []

    cleaned_items = []
    for item in items:
        label = clean_node_label(item, 65, output_language=output_language)
        if label:
            cleaned_items.append(label)

    cleaned_items = deduplicate_nodes(cleaned_items)
    if not cleaned_items:
        return []

    lang = output_language or "fr"

    if lang == "ar":
        rules = [
            ("المفاهيم", ["تعريف", "مفهوم", "مصطلح", "مبدأ", "نظرية"]),
            ("الأنواع", ["نوع", "أنواع", "تصنيف", "فئة", "قسم"]),
            ("الخصائص", ["خاصية", "خصائص", "ميزة", "مميزات", "صفة"]),
            ("الشروط", ["شرط", "شروط", "حالة", "ظرف", "ظروف"]),
            ("المنهجية", ["طريقة", "منهج", "خطوة", "مرحلة", "عملية"]),
            ("القواعد", ["قاعدة", "قواعد", "قانون", "معيار", "التزام"]),
            ("الصيغ", ["صيغة", "معادلة", "قانون", "حساب"]),
            ("الأمثلة", ["مثال", "أمثلة", "تطبيق"]),
            ("النتائج", ["نتيجة", "أثر", "تأثير", "حدود"]),
        ]
        fallback_label = "محتوى"
    elif lang == "en":
        rules = [
            ("Concepts", ["definition", "concept", "principle", "theory", "notion", "term"]),
            ("Types", ["type", "category", "class", "classification", "kind"]),
            ("Characteristics", ["characteristic", "feature", "property", "quality", "skill", "ability"]),
            ("Conditions", ["condition", "constraint", "requirement", "factor", "context"]),
            ("Methods", ["method", "technique", "approach", "procedure", "step", "process", "phase"]),
            ("Rules", ["rule", "standard", "norm", "obligation", "requirement", "law"]),
            ("Formulas", ["formula", "equation", "calculation", "theorem", "law"]),
            ("Examples", ["example", "case", "illustration", "application"]),
            ("Results", ["result", "effect", "impact", "consequence", "limit", "advantage"]),
        ]
        fallback_label = "Content"
    else:
        rules = [
            ("Concepts", ["définition", "concept", "notion", "principe", "théorie", "terme"]),
            ("Types", ["type", "catégorie", "classe", "classification", "famille", "forme"]),
            ("Caractéristiques", ["caractéristique", "propriété", "qualité", "capacité", "compétence", "aptitude"]),
            ("Conditions", ["condition", "contrainte", "exigence", "facteur", "contexte"]),
            ("Méthodes", ["méthode", "technique", "démarche", "procédure", "étape", "processus", "phase"]),
            ("Règles", ["règle", "norme", "obligation", "exigence", "loi", "standard"]),
            ("Formules", ["formule", "équation", "calcul", "théorème", "loi"]),
            ("Exemples", ["exemple", "cas", "illustration", "application"]),
            ("Résultats", ["résultat", "effet", "impact", "conséquence", "limite", "avantage"]),
        ]
        fallback_label = "Contenu"

    used = set()
    groups = []

    for group_name, keywords in rules:
        group_items = []

        for item in cleaned_items:
            key = normalize_for_match(item)
            if any(normalize_for_match(k) in key for k in keywords):
                group_items.append(item)
                used.add(item)

        if group_items:
            groups.append({
                "label": group_name,
                "children": deduplicate_nodes(group_items)[:max_items],
            })

        if len(groups) >= max_groups:
            break

    remaining = [item for item in cleaned_items if item not in used]

    # Only create fallback when nothing semantic was found.
    if remaining and not groups:
        groups.append({
            "label": fallback_label,
            "children": remaining[:max_items],
        })

    return groups[:max_groups]

def openai_like_cluster_items(items, module_label: str = "", output_language: str = "fr", max_groups: int = 3, max_items: int = 4):
    """
    OpenAI-like clustering fallback.

    Important:
    - It is optional and safe.
    - It asks the model only to group provided items.
    - It must NOT invent new details.
    - If the API fails or output is invalid, it falls back to auto_group_items().
    """
    if not isinstance(items, list):
        return []

    cleaned_items = deduplicate_nodes([clean_node_label(item, 65) for item in items if clean_node_label(item, 65)])

    if not cleaned_items:
        return []

    # For small lists, deterministic auto-grouping is faster and stable.
    if len(cleaned_items) <= 4:
        return auto_group_items(cleaned_items, output_language=output_language, max_groups=max_groups, max_items=max_items)

    language_name = get_language_name(output_language)

    try:
        clustering_prompt = f"""
You are a strict educational mindmap clustering engine.

Task:
Group ONLY the provided course items into {max_groups} logical blocks maximum.

Rules:
- Do NOT invent new details.
- Use ONLY the provided items as children.
- You may create short group labels in {language_name}.
- Each item can appear only once.
- Keep groups pedagogical and balanced.
- Return ONLY valid JSON.

JSON shape:
{{
  "groups": [
    {{
      "label": "short group label",
      "children": ["existing item 1", "existing item 2"]
    }}
  ]
}}

Module:
{module_label}

Items:
{json.dumps(cleaned_items, ensure_ascii=False)}
"""

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "Return only valid JSON. Do not invent content."},
                {"role": "user", "content": clustering_prompt},
            ],
            temperature=0,
        )

        raw = response.choices[0].message.content
        parsed = json.loads(raw)

        groups = parsed.get("groups", [])
        if not isinstance(groups, list):
            return auto_group_items(cleaned_items, output_language=output_language, max_groups=max_groups, max_items=max_items)

        allowed = {normalize_for_match(item): item for item in cleaned_items}
        used = set()
        safe_groups = []

        for group in groups:
            if not isinstance(group, dict):
                continue

            group_label = clean_node_label(group.get("label", ""), 55)
            raw_children = group.get("children", [])

            if not group_label or not isinstance(raw_children, list):
                continue

            safe_children = []

            for child in raw_children:
                child_label = clean_node_label(child, 65)
                child_key = normalize_for_match(child_label)

                # Only accept items that exactly match provided items.
                if child_key in allowed and child_key not in used:
                    safe_children.append(allowed[child_key])
                    used.add(child_key)

            if safe_children:
                safe_groups.append({
                    "label": group_label,
                    "children": safe_children[:max_items],
                })

            if len(safe_groups) >= max_groups:
                break

        remaining = [item for item in cleaned_items if normalize_for_match(item) not in used]
        if remaining and len(safe_groups) < max_groups:
            fallback_groups = auto_group_items(
                remaining,
                output_language=output_language,
                max_groups=max_groups - len(safe_groups),
                max_items=max_items,
            )
            safe_groups.extend(fallback_groups)

        return safe_groups[:max_groups] if safe_groups else auto_group_items(
            cleaned_items,
            output_language=output_language,
            max_groups=max_groups,
            max_items=max_items,
        )

    except Exception as e:
        print("OPENAI-LIKE CLUSTERING FALLBACK:", e)
        return auto_group_items(
            cleaned_items,
            output_language=output_language,
            max_groups=max_groups,
            max_items=max_items,
        )


def normalize_blocks_with_ai(blocks, module_label: str = "", output_language: str = "fr"):
    """
    Professional block normalizer.

    Strategy:
    1. Clean extracted blocks.
    2. Rebalance weak structures.
    3. Use hybrid clustering only when useful.
    4. Apply final node simplification.
    """
    if not isinstance(blocks, list):
        return []

    clean_blocks = []
    flat_items = []

    for block in blocks:
        if not isinstance(block, dict):
            item = clean_node_label(block, 65, output_language=output_language)
            if item:
                flat_items.append(item)
            continue

        label = clean_node_label(block.get("label", ""), 60, output_language=output_language)
        children = []

        for child in block.get("children", []):
            children.extend(split_compound_learning_item(child, output_language=output_language))

        children = [
            clean_node_label(child, 65, output_language=output_language)
            for child in children
            if clean_node_label(child, 65, output_language=output_language)
        ]

        children = deduplicate_nodes(children)

        if label and len(children) >= 2:
            clean_blocks.append({
                "label": label,
                "children": children[:MAX_DETAILS_PER_BLOCK],
            })
        else:
            flat_items.extend(children)
            if label and not children:
                flat_items.append(label)

    # If blocks already look good, just rebalance/simplify.
    if clean_blocks and len(clean_blocks) >= 2:
        return rebalance_blocks(
            clean_blocks,
            module_label=module_label,
            output_language=output_language,
        )

    # Use hybrid clustering for weak/flat structures.
    if flat_items:
        grouped = hybrid_cluster_items(
            flat_items,
            module_label=module_label,
            output_language=output_language,
            max_groups=MAX_BLOCKS_PER_MODULE,
            max_items=MAX_DETAILS_PER_BLOCK,
        )

        return rebalance_blocks(
            grouped,
            module_label=module_label,
            output_language=output_language,
        )

    return rebalance_blocks(
        clean_blocks,
        module_label=module_label,
        output_language=output_language,
    )

# Hybrid clustering controls
ENABLE_OPENAI_LIKE_CLUSTERING = True
AI_CLUSTER_MIN_ITEMS = 7
AI_CLUSTER_MAX_ITEMS = 18
_AI_CLUSTER_CACHE = {}


def should_use_ai_clustering(items, blocks=None) -> bool:
    """
    Decides when AI clustering is worth the latency.

    Uses AI only when:
    - enough items exist
    - items are not too many
    - deterministic grouping is weak or too generic
    """
    if not ENABLE_OPENAI_LIKE_CLUSTERING:
        return False

    if not isinstance(items, list):
        return False

    cleaned_items = deduplicate_nodes([
        clean_node_label(item, 65)
        for item in items
        if clean_node_label(item, 65)
    ])

    count = len(cleaned_items)

    if count < AI_CLUSTER_MIN_ITEMS:
        return False

    if count > AI_CLUSTER_MAX_ITEMS:
        return False

    if len(set(normalize_for_match(item) for item in cleaned_items)) < 5:
        return False

    # If deterministic blocks are already good, do not spend an API call.
    if isinstance(blocks, list):
        good_blocks = 0
        for block in blocks:
            if isinstance(block, dict):
                children = block.get("children", [])
                if isinstance(children, list) and len(children) >= 2:
                    good_blocks += 1

        if good_blocks >= 2:
            return False

    return True


def make_cluster_cache_key(items, module_label: str = "", output_language: str = "fr") -> str:
    cleaned_items = deduplicate_nodes([
        clean_node_label(item, 65)
        for item in items
        if clean_node_label(item, 65)
    ])

    normalized_items = sorted(normalize_for_match(item) for item in cleaned_items)
    normalized_module = normalize_for_match(module_label)

    return json.dumps(
        {
            "lang": output_language,
            "module": normalized_module,
            "items": normalized_items,
        },
        ensure_ascii=False,
        sort_keys=True,
    )


def hybrid_cluster_items(items, module_label: str = "", output_language: str = "fr", max_groups: int = 3, max_items: int = 4):
    """
    Fast-first hybrid clustering.

    1. Deterministic auto_group_items first.
    2. If result is good, return it immediately.
    3. If result is weak and item complexity justifies it, use AI.
    4. Cache AI results to avoid repeated API calls.
    5. Always fallback safely.
    """
    if not isinstance(items, list):
        return []

    cleaned_items = deduplicate_nodes([
        clean_node_label(item, 65)
        for item in items
        if clean_node_label(item, 65)
    ])

    if not cleaned_items:
        return []

    deterministic = auto_group_items(
        cleaned_items,
        output_language=output_language,
        max_groups=max_groups,
        max_items=max_items,
    )

    if not should_use_ai_clustering(cleaned_items, deterministic):
        return deterministic

    cache_key = make_cluster_cache_key(cleaned_items, module_label, output_language)

    if cache_key in _AI_CLUSTER_CACHE:
        return _AI_CLUSTER_CACHE[cache_key]

    ai_result = openai_like_cluster_items(
        cleaned_items,
        module_label=module_label,
        output_language=output_language,
        max_groups=max_groups,
        max_items=max_items,
    )

    # Keep AI only if it gives a real structured result.
    if isinstance(ai_result, list) and ai_result:
        _AI_CLUSTER_CACHE[cache_key] = ai_result
        return ai_result

    _AI_CLUSTER_CACHE[cache_key] = deterministic
    return deterministic

def enrich_modules(tree, text, output_language: str = "fr"):
    """
    95% quality generic mindmap enrichment.

    Output:
    Root -> Module/Chapter -> Clean logical block -> Short details

    Includes:
    - deterministic extraction
    - auto-block intelligence
    - hybrid AI clustering when useful
    - node simplification
    - final rebalance
    """
    if not isinstance(tree, list):
        return []

    enriched = []

    for module in tree:
        if isinstance(module, dict):
            raw_module_label = safe_text(module.get("label", "")).strip()
            existing_children = module.get("children", [])
        else:
            raw_module_label = safe_text(module).strip()
            existing_children = []

        if not raw_module_label:
            continue

        module_label = normalize_module_label(raw_module_label, output_language=output_language)
        children = []

        # 1) Preserve existing structured children if useful.
        if isinstance(existing_children, list) and existing_children:
            structured_children = []

            for child in existing_children:
                if isinstance(child, dict):
                    child_label = clean_node_label(child.get("label", ""), 65, output_language=output_language)
                    sub_children = []

                    for sub in child.get("children", []):
                        sub_children.extend(split_compound_learning_item(sub, output_language=output_language))

                    sub_children = [
                        clean_node_label(sub, 65, output_language=output_language)
                        for sub in sub_children
                        if clean_node_label(sub, 65, output_language=output_language)
                    ]

                    if child_label:
                        structured_children.append({
                            "label": child_label,
                            "children": deduplicate_nodes(sub_children)[:MAX_DETAILS_PER_BLOCK],
                        })

                else:
                    child_label = clean_node_label(child, 65, output_language=output_language)
                    if child_label:
                        structured_children.append({
                            "label": child_label,
                            "children": [],
                        })

            children = normalize_blocks_with_ai(
                structured_children,
                module_label=module_label,
                output_language=output_language,
            )

        # 2) Extract local body blocks.
        if not children:
            body = extract_module_body(text, raw_module_label)
            raw_blocks = extract_generic_blocks_from_body(
                body,
                max_blocks=4,
                max_items=6,
            )

            children = normalize_blocks_with_ai(
                raw_blocks,
                module_label=module_label,
                output_language=output_language,
            )

        # 3) Safe keyword fallback.
        if not children and ENABLE_CHATGPT_LIKE_VISUAL:
            body = extract_module_body(text, raw_module_label)
            source = body if body else text
            keywords = extract_keywords(source, max_keywords=8)
            grouped = hybrid_cluster_items(
                keywords,
                module_label=module_label,
                output_language=output_language,
                max_groups=MAX_BLOCKS_PER_MODULE,
                max_items=MAX_DETAILS_PER_BLOCK,
            )
            children = rebalance_blocks(
                grouped,
                module_label=module_label,
                output_language=output_language,
            )

        # 4) Final quality pass.
        children = rebalance_blocks(
            children,
            module_label=module_label,
            output_language=output_language,
        )

        # Final generic cleanup.
        # Core rule: a good block must be informative.
        # No domain-specific hardcoding.

        module_key = normalize_for_match(module_label)

        # Helper: flatten current children.
        flat = []
        for block in children:
            if isinstance(block, dict):
                flat.append(block.get("label", ""))
                flat.extend(block.get("children", []))
            else:
                flat.append(block)

        # 1) Universal separation: classification/types vs progression/temporal sequence.
        if any(k in module_key for k in ["type", "categorie", "classification", "classe", "famille"]) and flat:
            progression_keywords = ["evolution", "progression", "etape", "phase", "cycle", "niveau", "sequence", "version"]

            types = []
            progression = []

            for x in flat:
                key = normalize_for_match(x)
                if any(k in key for k in progression_keywords):
                    progression.append(x)
                else:
                    types.append(x)

            fixed_children = []

            if types:
                fixed_children.append({
                    "label": "Types" if output_language != "ar" else "الأنواع",
                    "children": deduplicate_nodes(types)[:MAX_DETAILS_PER_BLOCK],
                })

            if progression:
                fixed_children.append({
                    "label": "Progression" if output_language != "ar" else "التدرج",
                    "children": deduplicate_nodes(progression)[:MAX_DETAILS_PER_BLOCK],
                })

            if fixed_children:
                children = rebalance_blocks(
                    fixed_children,
                    module_label=module_label,
                    output_language=output_language,
                )

        # 2) Communication/collaboration cleanup:
        # avoid a weak single "Règles" node.
        if any(k in module_key for k in ["communication", "discussion", "collaboration", "groupe", "team", "equipe"]) and flat:
            flat_key = " ".join(normalize_for_match(x) for x in flat)
            fixed_children = []

            if "communication" in flat_key:
                fixed_children.append({"label": "Communication", "children": []})

            if "discussion" in flat_key or "dialogue" in flat_key:
                fixed_children.append({"label": "Discussion", "children": []})

            if "collaboration" in flat_key or "equipe" in flat_key or "team" in flat_key:
                fixed_children.append({"label": "Collaboration", "children": []})

            # Keep respect only if it is the only real concept available.
            if not fixed_children and "respect" in flat_key:
                fixed_children.append({"label": "Respect", "children": []})

            if fixed_children:
                children = fixed_children[:MAX_BLOCKS_PER_MODULE]

        # 3) Project/objective cleanup:
        if any(k in module_key for k in ["projet", "objectif", "orientation", "plan", "strategie", "strategy", "carriere", "career"]) and flat:
            flat_key = " ".join(normalize_for_match(x) for x in flat)
            fixed_children = []

            if "force" in flat_key or "strength" in flat_key:
                fixed_children.append({"label": "Forces", "children": []})

            if "objectif" in flat_key or "goal" in flat_key:
                fixed_children.append({"label": "Objectifs", "children": []})

            if "plan" in flat_key or "strategie" in flat_key or "strategy" in flat_key:
                fixed_children.append({"label": "Plan", "children": []})

            if fixed_children:
                children = fixed_children[:MAX_BLOCKS_PER_MODULE]

        # 4) Empty/weak block replacement:
        # If all blocks were removed because they were weak, rebuild from flat items.
        if not children and flat:
            children = auto_group_items(
                flat,
                output_language=output_language,
                max_groups=MAX_BLOCKS_PER_MODULE,
                max_items=MAX_DETAILS_PER_BLOCK,
            )

        enriched.append({
            "label": module_label,
            "children": children,
        })

    return enriched

def build_toc_plus_tree(cleaned_text: str, structure: list[str]) -> list:
    """
    Safe base structure:
    Root -> Module

    If A-Z modules exist, keep only those as top-level nodes.
    Smart enrichment is applied later by enrich_modules().
    """
    if not isinstance(structure, list):
        return []

    tree = filter_main_modules(structure)
    return deduplicate_nodes(tree[:40])


def build_tree(structure: list[str], depth: int = 3):
    """
    General structure builder.

    - If parts exist: create part -> chapter hierarchy.
    - If letter modules exist: keep those modules only.
    - Otherwise: return cleaned flat list.
    """
    if not isinstance(structure, list):
        return []

    cleaned_items = []
    for item in structure:
        label = safe_text(item).strip()
        if not label:
            continue

        label = clean_toc_label(label)
        display_label = clean_toc_numbering(label)

        if display_label:
            cleaned_items.append(smart_truncate(display_label, 70))

    cleaned_items = deduplicate_nodes(cleaned_items)

    has_parts = any("الجزء" in item or "Part" in item for item in cleaned_items)

    if not has_parts:
        return filter_main_modules(cleaned_items)[:40 if depth >= 3 else 18]

    tree = []
    current_part = None

    for item in cleaned_items[:80]:
        if "الجزء" in item or "Part" in item:
            current_part = {
                "type": "part",
                "label": item,
                "children": []
            }
            tree.append(current_part)

        elif ("الفصل" in item or "Chapter" in item) and current_part:
            if "التسويق 5.0" in " ".join(cleaned_items):
                if is_valid_chapter_for_part(current_part["label"], item):
                    current_part["children"].append(item)
            else:
                current_part["children"].append(item)

        elif current_part:
            current_part["children"].append(item)

    return tree


def build_minimal_tree(keywords: list[str]) -> list[str]:
    if not isinstance(keywords, list):
        return []

    return keywords[:8]


def generate_mermaid(tree, root: str = "الموضوع الرئيسي", output_language: str = "fr") -> str:
    """
    Mermaid-safe generator with true 3-level support and simplified labels.

    Supports:
    Root -> Module
    Root -> Module -> Block
    Root -> Module -> Block -> Detail
    """
    if not tree:
        return fallback_mermaid()

    root_label = simplify_label(smart_truncate(root, 55), output_language=output_language)
    lines = ["mindmap", f"  root(({root_label}))"]

    for item in tree[:40]:
        if isinstance(item, dict):
            module_label = normalize_module_label(
                safe_text(item.get("label", "")),
                output_language=output_language,
            )

            module_label = smart_truncate(module_label, 70)

            if module_label:
                lines.append(f"    {module_label}")

            children = item.get("children", [])

            if isinstance(children, list):
                for child in children[:MAX_BLOCKS_PER_MODULE]:
                    if isinstance(child, dict):
                        child_label = clean_node_label(
                            child.get("label", ""),
                            60,
                            output_language=output_language,
                        )
                        child_label = polish_block_label(child_label)

                        if child_label:
                            lines.append(f"      {child_label}")

                        sub_children = child.get("children", [])

                        if isinstance(sub_children, list):
                            for sub in sub_children[:MAX_DETAILS_PER_BLOCK]:
                                sub_label = clean_node_label(
                                    sub,
                                    60,
                                    output_language=output_language,
                                )

                                if sub_label:
                                    lines.append(f"        {sub_label}")

                    else:
                        child_label = clean_node_label(
                            child,
                            60,
                            output_language=output_language,
                        )

                        if child_label:
                            lines.append(f"      {child_label}")

        else:
            label = normalize_module_label(
                safe_text(item).strip(),
                output_language=output_language,
            )

            if label:
                lines.append(f"    {smart_truncate(label, 70)}")

    return "\n".join(lines)

def is_bad_mermaid_fallback(diagram: str) -> bool:
    """
    Detects weak fallback diagrams that should not be shown when real content exists.
    """
    if not isinstance(diagram, str):
        return True

    normalized = normalize_for_match(diagram)

    bad_markers = [
        "main topic",
        "idea 1",
        "idea 2",
        "idea 3",
        "keyword",
        "الموضوع الرئيسي",
        "فكرة رئيسية",
        "كلمة مفتاحية",
    ]

    return any(marker in normalized for marker in bad_markers)


def mermaid_has_real_content(diagram: str) -> bool:
    """
    Checks that a Mermaid mindmap has real content and is not the generic fallback.
    """
    if not isinstance(diagram, str):
        return False

    lines = [line.strip() for line in diagram.splitlines() if line.strip()]

    if len(lines) < 3:
        return False

    if not diagram.strip().startswith("mindmap"):
        return False

    if is_bad_mermaid_fallback(diagram):
        return False

    return True

def build_safe_tree_from_text(cleaned_text: str, output_language: str = "fr") -> list:
    """
    Final safety net:
    creates a real tree from visible educational text instead of using
    generic fallback nodes.

    This prevents:
    Main topic -> Idea -> Keyword
    when the document contains usable headings or keywords.
    """
    if not isinstance(cleaned_text, str):
        return []

    sections = extract_sections(cleaned_text)

    if sections:
        base_tree = build_toc_plus_tree(cleaned_text, sections)

        if base_tree:
            return enrich_modules(
                base_tree,
                cleaned_text,
                output_language=output_language,
            )

        tree = build_tree(sections, depth=3)

        if tree:
            return enrich_modules(
                tree,
                cleaned_text,
                output_language=output_language,
            )

    keywords = extract_keywords(cleaned_text, max_keywords=8)
    keywords = deduplicate_nodes([
        clean_node_label(keyword, 55, output_language=output_language)
        for keyword in keywords
        if clean_node_label(keyword, 55, output_language=output_language)
    ])

    if keywords:
        return [
            {
                "label": "Points clés" if output_language != "ar" else "نقاط أساسية",
                "children": [
                    {
                        "label": "Notions principales" if output_language != "ar" else "المفاهيم الرئيسية",
                        "children": keywords[:MAX_DETAILS_PER_BLOCK],
                    }
                ],
            }
        ]

    return []

def process_document_text(text: str, output_language: str = "ar") -> dict:
    """
    Production-stable deterministic diagram pipeline.

    Priority:
    1. TOC if clearly detected.
    2. Visible headings/sections.
    3. Safe real-content keyword tree.
    4. Only then fallback.

    Guarantees:
    - never returns weak fallback if real sections exist
    - always tries Root -> Module -> Block -> Detail
    - generic for any course domain
    """
    cleaned_text = light_ocr_fix(remove_ui_noise(text))
    root = detect_root_title(cleaned_text, output_language)

    toc = detect_table_of_contents(cleaned_text)
    sections = extract_sections(cleaned_text)

    if toc:
        mode = "toc"
        confidence = "high"
        structure = deduplicate_nodes(toc)

        has_parts = any("الجزء" in safe_text(item) or "Part" in safe_text(item) for item in structure)

        if has_parts:
            tree = build_tree(structure, depth=3)
        else:
            tree = build_toc_plus_tree(cleaned_text, structure)

        if ENABLE_SMART_ENRICHMENT:
            tree = enrich_modules(tree, cleaned_text, output_language)

    elif sections:
        mode = "chapter"
        confidence = "medium"
        structure = deduplicate_nodes(sections)

        tree = build_toc_plus_tree(cleaned_text, structure)

        if not tree:
            tree = build_tree(structure, depth=3)

        if ENABLE_SMART_ENRICHMENT:
            tree = enrich_modules(tree, cleaned_text, output_language)

    else:
        mode = "weak"
        confidence = "low"
        structure = extract_keywords(cleaned_text)
        tree = build_safe_tree_from_text(cleaned_text, output_language)

        if not tree:
            tree = build_minimal_tree(structure)

    fallback_diagram = generate_mermaid(tree, root=root, output_language=output_language)

    # Last safety repair: if the diagram is still generic, rebuild from text.
    if is_bad_mermaid_fallback(fallback_diagram):
        safe_tree = build_safe_tree_from_text(cleaned_text, output_language)
        if safe_tree:
            tree = safe_tree
            fallback_diagram = generate_mermaid(tree, root=root, output_language=output_language)

    return {
        "cleaned_text": cleaned_text,
        "root": root,
        "mode": mode,
        "confidence": confidence,
        "structure": structure,
        "tree": tree,
        "fallback_diagram": fallback_diagram,
    }

def fix_mermaid(diagram: str) -> str:
    if not isinstance(diagram, str):
        return fallback_mermaid()

    cleaned = diagram.strip()

    if not cleaned:
        return fallback_mermaid()

    if not cleaned.startswith("mindmap"):
        return fallback_mermaid()

    if "\n" not in cleaned:
        return fallback_mermaid()

    return cleaned


def safe_text(value) -> str:
    if value is None:
        return ""

    if isinstance(value, str):
        return value

    if isinstance(value, (int, float, bool)):
        return str(value)

    if isinstance(value, dict):
        return " | ".join(f"{safe_text(k)}: {safe_text(v)}" for k, v in value.items())

    if isinstance(value, list):
        return " | ".join(safe_text(item) for item in value)

    return str(value)


def safe_string_list(value) -> list[str]:
    if value is None:
        return []

    if isinstance(value, list):
        return [safe_text(item) for item in value if safe_text(item)]

    text = safe_text(value)
    return [text] if text else []


def normalize_question(question) -> dict:
    if not isinstance(question, dict):
        return {
            "question": safe_text(question),
            "options": [],
            "correct_answer": "",
            "explanation": "",
        }

    return {
        "question": safe_text(question.get("question", "")),
        "options": safe_string_list(question.get("options", []))[:4],
        "correct_answer": safe_text(question.get("correct_answer", "")),
        "explanation": safe_text(question.get("explanation", "")),
    }


def normalize_flashcard(card) -> dict:
    if not isinstance(card, dict):
        return {
            "front": safe_text(card),
            "back": "",
        }

    return {
        "front": safe_text(card.get("front", "")).strip(),
        "back": safe_text(card.get("back", "")).strip(),
    }



def clean_mermaid_duplicates(diagram: str) -> str:
    """
    Removes duplicate Mermaid node labels while preserving order and indentation.
    Mermaid mindmap classDef/style lines are not used because they can break rendering.
    """
    if not isinstance(diagram, str):
        return fallback_mermaid()

    lines = diagram.splitlines()
    cleaned_lines = []
    seen = set()

    for line in lines:
        stripped = line.strip()

        if not stripped:
            continue

        if stripped == "mindmap":
            cleaned_lines.append(line)
            continue

        if stripped.startswith("root(("):
            cleaned_lines.append(line)
            continue

        # Drop unsupported Mermaid styling lines if the model returns them.
        if stripped.startswith("classDef") or stripped.startswith("style "):
            continue

        # Remove unsupported class suffixes if the model returns them.
        cleaned_output_line = line.replace(":::part", "").replace(":::chapter", "")
        compare_label = stripped.replace(":::part", "").replace(":::chapter", "")

        compare_label = smart_truncate(clean_toc_label(compare_label), 70)
        normalized = compare_label.replace("  ", " ").strip()

        if normalized in seen:
            continue

        seen.add(normalized)
        cleaned_lines.append(cleaned_output_line)

    return "\n".join(cleaned_lines)


def enforce_mermaid_template(diagram: str) -> str:
    """
    Final Mermaid safety layer:
    - valid mindmap
    - real line breaks
    - no duplicate labels
    - frontend-safe fallback
    """
    diagram = fix_mermaid(diagram)
    diagram = clean_mermaid_duplicates(diagram)

    if not diagram.startswith("mindmap") or "\n" not in diagram:
        return fallback_mermaid()

    return diagram

def normalize_result(result: dict) -> dict:
    if not isinstance(result, dict):
        result = {}

    result["summary"] = safe_text(result.get("summary", ""))
    result["written_summary"] = safe_text(result.get("written_summary", ""))
    result["visual_summary"] = safe_text(result.get("visual_summary", ""))
    result["visual_diagram"] = enforce_mermaid_template(safe_text(result.get("visual_diagram", "")))

    result["key_points"] = safe_string_list(result.get("key_points", []))

    quiz = result.get("quiz", {})
    if not isinstance(quiz, dict):
        quiz = {}

    result["quiz"] = {
        "theory_questions": [
            normalize_question(q) for q in quiz.get("theory_questions", [])
        ],
        "practice_questions": [
            normalize_question(q) for q in quiz.get("practice_questions", [])
        ],
    }

    # 🔥 FIX FLASHCARDS VIDES
    raw_flashcards = result.get("flashcards", [])
    if not isinstance(raw_flashcards, list):
        raw_flashcards = []

    result["flashcards"] = [
        card for card in (normalize_flashcard(card) for card in raw_flashcards)
        if card["front"] and card["back"]
    ]

    result["study_plan"] = safe_string_list(result.get("study_plan", []))

    result["disclaimer"] = safe_text(
        result.get("disclaimer", "This is for educational support only.")
    )

    return result


def build_user_prompt(text: str, education_level: str, output_language: str) -> str:
    language_name = get_language_name(output_language)

    pipeline = process_document_text(text, output_language)
    cleaned_text = pipeline["cleaned_text"]
    mode = pipeline["mode"]
    confidence = pipeline["confidence"]
    structure = pipeline["structure"]
    fallback_diagram = pipeline["fallback_diagram"]

    structure_preview = "\n".join(f"- {truncate_label(clean_toc_label(item))}" for item in structure[:40])

    return f"""
Analyze the following content.

LANGUAGE: {output_language}

FINAL DIAGRAM RULE:
- Client-facing visual_diagram must be generated by the deterministic pipeline.
- Use Root -> Module in default SaaS mode.
- Never add unsupported body details as mindmap children. Controlled source-supported enrichment from deterministic pipeline is allowed.
- Never use Mermaid classDef/style syntax.

PRIORITY:
1. Respect document structure.
2. Avoid hallucination.
3. Never fail.

CRITICAL OBJECTIVE:
You must extract knowledge ONLY from the provided content.
Do NOT add external knowledge.
Do NOT guess.
Do NOT invent missing structure.
Do NOT force a non-course document into an educational course format.

ROBUSTNESS RULE:
If the extracted text appears corrupted, incomplete, too short, or partially noisy:
- Do NOT fail completely.
- Extract only visible supported keywords and sections.
- Produce a minimal but valid JSON response.
- Produce a minimal but valid Mermaid mindmap.
- Partial but correct output is better than empty output.

ADAPTIVE MODE:
- If structure is clear, produce a full structured result.
- If structure is partial, produce a simplified but correct result.
- If structure is weak, produce a minimal valid result.
- Never return empty output.
- Never say "Analysis failed".

TOC GOLDEN RULE:
- If Detected diagram mode is "toc", the table of contents is the source of truth.
- In toc mode, visual_diagram MUST follow the extracted TOC order.
- In toc mode, do NOT enrich the diagram with chapter body concepts.
- In toc mode, do NOT add technologies, definitions, keywords, or examples unless they appear in the extracted TOC.
- TOC > EVERYTHING.
- Never mix table of contents with chapter content.

VISUAL RULE:
- Parts must be visually dominant.
- Chapters must be grouped under parts.
- Avoid flat structures only when true hierarchy exists.
- Default SaaS diagram should stay clean and faithful, not over-detailed.
- Default hybrid SaaS mode must prefer safe structure:
  Root -> Module -> controlled source-supported children.
- Do NOT add uncontrolled subsections in default mode.
- Do NOT use uncontrolled body details as structure.
- Deep mode may use Root -> Module -> Explicit subsection only when explicitly enabled in code.
- Match module headings strictly.
- Stop at the next major heading.
- Do NOT include other TOC modules as children.
- Preserve pedagogical order such as A -> B -> C -> D -> E -> F.
- Do NOT invent subsections.

PIPELINE CONTEXT:
- Detected diagram mode: {mode}
- Detected structure confidence: {confidence}
- Extracted structure hints:
{structure_preview if structure_preview else "- No clear structure detected"}
- Safe fallback diagram:
{fallback_diagram}

IMPORTANT:
- Adapt ALL output to this education level: {education_level}
- Return the ENTIRE JSON content in this language: {language_name}
- Keep JSON keys exactly in English.
- Do not translate JSON keys.
- Return ONLY JSON.

----------------------------------
STEP 1 — DOCUMENT TYPE CHECK
----------------------------------

Before generating the learning output, decide if the content is educational study material.

Treat as course/study material ONLY if it is clearly:
- textbook chapter
- lesson
- lecture notes
- training module
- educational article
- study guide
- book
- organized learning content
- academic explanation

If the content is NOT course/study material, for example:
- legal contract
- invoice
- administrative document
- business dataset
- random text

Then:
- Do NOT generate educational quiz questions.
- Do NOT generate flashcards.
- Do NOT generate a study plan.
- Do NOT invent definitions, components, types, or steps.
- Clearly state in summary that the document does not appear to be educational study material.
- Briefly identify the real document type if recognizable.
- Summarize only real sections or clauses present in the content.
- Keep key_points minimal and factual.
- Use a simple Mermaid mindmap based only on the real document sections.

----------------------------------
STRICT EXTRACTION RULES
----------------------------------

- Use ONLY information explicitly present in the text.
- Preserve exact terms from the source when possible.
- If a list exists, preserve its items.
- If a section exists, represent it.
- Do NOT add examples that are not present.
- Do NOT invent study weeks, activities, or learning tasks not supported by the content.
- Do NOT use the same concept twice in different branches unless the source clearly uses it in two different roles.

----------------------------------
COURSE OUTPUT RULES
----------------------------------

If the content IS a course/study material:
- summary must mention the real topic.
- written_summary must be one clear paragraph.
- visual_summary must show real main ideas.
- visual_diagram must be valid Mermaid mindmap.
- key_points must contain only supported points.
- quiz must be based only on the content.
- flashcards must have non-empty front/back.
- study_plan must be based only on real sections in the content.

----------------------------------
DIAGRAM ADAPTIVE 10/10 RULES
----------------------------------

The visual_diagram must be a production-ready Mermaid mindmap.

CORE DIAGRAM PRINCIPLES:
- The diagram must reflect the real structure of the content.
- Prefer section titles and explicit lists from the source.
- Do NOT create visually attractive but logically weak diagrams.
- Do NOT duplicate the same idea under multiple branches.
- Do NOT use generic branches if the source has precise branches.
- Do NOT omit important listed elements from the source when they are clearly visible.

ADAPTIVE DIAGRAM MODE:
- If Detected diagram mode is "toc", use ONLY the extracted table of contents as the main structure.
- If Detected diagram mode is "chapter", organize by visible headings and key lists.
- If Detected diagram mode is "weak", use a minimal diagram with 2 to 5 main ideas.
- Never block.
- Never output an empty diagram.
- Never output error text.

MANDATORY MINIMAL FALLBACK:
If unsure, return a valid diagram like:
mindmap
  root((الموضوع الرئيسي))
    فكرة رئيسية
      كلمة مفتاحية
    فكرة رئيسية أخرى
      كلمة مفتاحية

IMPORTANT:
- Only include branches that are supported by the content.
- Rename branch labels using the source wording in {language_name}.
- If the source lists exactly 3 challenges, include exactly those 3 challenges.
- If the source lists technologies, include the complete list visible in the content.
- If the source has evolution stages, include them under one branch only.
- If an item fits under one branch, do not repeat it under another branch.

MARKETING 5.0 SPECIFIC RULE:
If the content is about Marketing 5.0 and the source supports these ideas:
- If Detected diagram mode is "toc", use ONLY book order from the extracted table of contents.
- In toc mode, do NOT add chapter 1 technologies, definitions, or elements into the TOC diagram.
- If Detected diagram mode is "chapter" and the content focuses on chapter 1 only, use:
  تعريف التسويق 5.0
  تطور التسويق
  التحديات
  التقنيات
  العناصر الخمسة للتسويق 5.0
- Under التحديات, include exactly:
  فجوة الأجيال
  استقطاب النمو
  الفجوة الرقمية
- Under التقنيات, include supported technologies such as:
  الذكاء الاصطناعي
  معالجة اللغة الطبيعية
  تقنيات الاستشعار
  الروبوتات
  الواقع المعزز والافتراضي
  إنترنت الأشياء
  قواعد البيانات المتسلسلة
- Under العناصر الخمسة للتسويق 5.0, include supported items such as:
  التسويق المبني على البيانات
  التسويق اللين
  التسويق التنبئي
  التسويق السياقي
  التسويق المعزز
- Do NOT duplicate "تحسين تجربة الزبون" or "خدمة الإنسان" in multiple branches.

ANTI-DUPLICATION RULE:
- Before returning JSON, compare all Mermaid node labels.
- If the same label appears twice, keep it only in the most precise branch.
- Remove repeated nodes unless the source explicitly requires repetition.

ANTI-HALLUCINATION DIAGRAM RULE:
- Every Mermaid node must be directly traceable to the source.
- If a node is not clearly in the source, remove it.
- Do NOT add concepts only because they sound related.
- Do NOT add missing technologies or examples unless present in the provided content.

----------------------------------
NON-COURSE OUTPUT RULES
----------------------------------

If the content is NOT a course/study material:
- summary: say it is not educational study material and identify the document type.
- written_summary: factual short paragraph about the real content.
- visual_summary: factual list/diagram of real sections only.
- visual_diagram: simple Mermaid mindmap of real sections only.
- key_points: factual clauses/sections only.
- quiz: empty arrays.
- flashcards: empty array.
- study_plan: empty array.

----------------------------------
MERMAID FORMAT RULES
----------------------------------

visual_diagram MUST:
- start exactly with: mindmap
- contain multiple lines
- use indentation with spaces
- use only text from the content
- avoid unsupported nodes
- avoid markdown fences
- avoid quotes
- avoid complex punctuation
- avoid very long nodes
- be stable for frontend rendering

----------------------------------
FINAL VALIDATION
----------------------------------

Before returning:
- Check that the document type decision is correct.
- Check that no non-course document is converted into a course.
- Check that no unsupported concepts are added.
- Check that quiz, flashcards, and study_plan are empty for non-course documents.
- Check that flashcards and study_plan are non-empty for valid course content with usable information.
- Check that Mermaid starts with "mindmap".
- Check that Mermaid contains real line breaks.
- Check that Mermaid has no duplicated node labels.
- Check that Mermaid uses source structure when available.
- If Detected diagram mode is "toc", check that Mermaid does not include body concepts outside the TOC.
- Check that JSON is valid.
- If something is uncertain, reduce detail instead of failing.

Return EXACT JSON:

{{
  "summary": "string",
  "written_summary": "string",
  "visual_summary": "string",
  "visual_diagram": "mindmap\\n  root((...))\\n    ...",
  "key_points": ["..."],
  "quiz": {{
    "theory_questions": [],
    "practice_questions": []
  }},
  "flashcards": [],
  "study_plan": [],
  "disclaimer": "This is for educational support only."
}}

Content:
{cleaned_text[:12000]}
"""
def diagram_quality_score(diagram: str) -> int:
    """
    Scores a Mermaid mindmap for pedagogical quality.

    Higher is better.
    Generic criteria:
    - no fallback nodes
    - enough depth
    - few weak labels
    - leaves are explicit
    - not overfilled with intro/UI noise
    """
    if not isinstance(diagram, str) or not diagram.strip().startswith("mindmap"):
        return -1000

    lines = [line.rstrip() for line in diagram.splitlines() if line.strip()]
    if len(lines) < 3:
        return -500

    weak_terms = {
        "contenu", "content",
        "informations generales", "general information",
        "contexte et position",
        "documents associes",
        "rapport",
        "situer",
        "tier",
        "par",
        "des",
        "gles",
        "details",
        "elements",
        "autres",
        "divers",
        "main topic",
        "idea 1",
        "keyword",
    }

    score = 0
    labels = []

    for line in lines:
        stripped = line.strip()
        if stripped == "mindmap" or stripped.startswith("root(("):
            continue

        label = stripped
        labels.append(label)

        indent = len(line) - len(line.lstrip(" "))

        # Reward hierarchy
        if indent == 4:
            score += 5
        elif indent == 6:
            score += 8
        elif indent >= 8:
            score += 10

        key = normalize_for_match(label)

        if key in weak_terms:
            score -= 35

        if len(key) <= 3 and not any(ch.isdigit() for ch in key):
            score -= 25

        # Sentence-like labels are harder to read in mindmaps
        if len(label.split()) > 7:
            score -= 8

        if len(label.split()) <= 2:
            score += 3  # short clear label bonus

        # Useful explicit numeric facts
        if re.search(r"\d+\s*(heures?|hours?|minutes?)", label, flags=re.IGNORECASE):
            score += 5

    # Reward enough meaningful nodes
    score += min(len(labels), 25)

    # Penalize duplicated nodes
    normalized = [normalize_for_match(label) for label in labels]
    duplicates = len(normalized) - len(set(normalized))
    score -= duplicates * 12

    if is_bad_mermaid_fallback(diagram):
        score -= 200

    return score


def choose_best_visual_diagram(model_diagram: str, deterministic_diagram: str) -> str:
    """
    Selects the best diagram instead of blindly overriding with deterministic output.

    This is the final safety layer:
    - if deterministic is clean, use it
    - if deterministic has weak/noisy branches, keep the model diagram
    - if one is invalid, use the valid one
    """
    model_diagram = safe_text(model_diagram)
    deterministic_diagram = safe_text(deterministic_diagram)

    model_ok = mermaid_has_real_content(model_diagram)
    deterministic_ok = mermaid_has_real_content(deterministic_diagram)

    if deterministic_ok and not model_ok:
        return deterministic_diagram

    if model_ok and not deterministic_ok:
        return model_diagram

    if not model_ok and not deterministic_ok:
        return deterministic_diagram if deterministic_diagram else fallback_mermaid()

    model_score = diagram_quality_score(model_diagram)
    deterministic_score = diagram_quality_score(deterministic_diagram)

    # Prefer model when deterministic is clearly noisier.
    if model_score >= deterministic_score:
        return model_diagram

    return deterministic_diagram

def analyze_study_content(text: str, education_level: str, output_language: str = "en"):
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": build_user_prompt(
                        text=text,
                        education_level=education_level,
                        output_language=output_language,
                    ),
                },
            ],
            temperature=0,
        )

        content = response.choices[0].message.content

        try:
            result = json.loads(content)
        except Exception as json_error:
            print("JSON PARSE ERROR:", json_error)
            print("RAW MODEL OUTPUT:", content)

            pipeline = process_document_text(text, output_language)

            return normalize_result({
                "summary": "Partial analysis",
                "written_summary": "The model returned invalid JSON. A safe fallback response was generated.",
                "visual_summary": "Fallback used",
                "visual_diagram": generate_mermaid(
                    pipeline.get("tree", []),
                    root=pipeline.get("root", "Main topic"),
                    output_language=output_language,
                ),
                "key_points": [],
                "quiz": {},
                "flashcards": [],
                "study_plan": [],
                "disclaimer": "This is for educational support only.",
            })

        # Keep model diagram before deterministic override.
        model_diagram = safe_text(result.get("visual_diagram", ""))

        # Deterministic diagram candidate.
        pipeline = process_document_text(text, output_language)
        deterministic_diagram = generate_mermaid(
            pipeline.get("tree", []),
            root=pipeline.get("root", "Main topic"),
            output_language=output_language,
        )

        result["visual_diagram"] = choose_best_visual_diagram(
            model_diagram=model_diagram,
            deterministic_diagram=deterministic_diagram,
        )

        return normalize_result(result)

    except Exception as e:
        print("ERROR:", e)

        pipeline = process_document_text(text, output_language)
        diagram = generate_mermaid(
            pipeline.get("tree", []),
            root=pipeline.get("root", "Main topic"),
            output_language=output_language,
        )

        return normalize_result({
            "summary": "Partial analysis",
            "written_summary": "The system could not fully analyze the content, but the response remains valid.",
            "visual_summary": "MAIN TOPIC\n│\n└── Partial content",
            "visual_diagram": diagram,
            "key_points": ["Partial content extracted"],
            "quiz": {},
            "flashcards": [],
            "study_plan": ["Review the available extracted content"],
            "disclaimer": "This is for educational support only."
        })

