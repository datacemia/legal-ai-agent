import os
import json
import re
from typing import Dict, List
from pydantic import BaseModel, Field
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class VisualSummary(BaseModel):
    main_topic: str = ""
    key_points: List[str] = Field(default_factory=list)


class QuizQuestion(BaseModel):
    question: str
    options: List[str]
    correct_answer: str
    explanation: str


class Flashcard(BaseModel):
    front: str
    back: str


class StudyDay(BaseModel):
    day: str
    focus: str
    tasks: List[str]


class QualityReport(BaseModel):
    score: int = 100
    valid: bool = True
    errors: List[str] = Field(default_factory=list)


class StudyAnalyzeResponse(BaseModel):
    summary: str = ""
    detailed_summary: str = ""
    visual_summary: VisualSummary = Field(default_factory=VisualSummary)
    visual_diagram: str = ""
    diagram_explanations: Dict[str, str] = Field(default_factory=dict)
    key_points: List[str] = Field(default_factory=list)
    theoretical_quiz: List[QuizQuestion] = Field(default_factory=list)
    practical_quiz: List[QuizQuestion] = Field(default_factory=list)
    flashcards: List[Flashcard] = Field(default_factory=list)
    study_plan: List[StudyDay] = Field(default_factory=list)
    quality: QualityReport = Field(default_factory=QualityReport)


def validate_study_response(result: dict) -> dict:
    try:
        validated = StudyAnalyzeResponse(**result)
        data = validated.model_dump()

        data["key_points"] = data["key_points"][:8]
        data["flashcards"] = data["flashcards"][:8]
        data["theoretical_quiz"] = data["theoretical_quiz"][:5]
        data["practical_quiz"] = data["practical_quiz"][:5]
        data["study_plan"] = data["study_plan"][:5]

        return data

    except Exception as e:
        print("FINAL SCHEMA VALIDATION ERROR:", e)
        return result


QUALITY_META_KEYWORDS = [
    "course", "student", "students", "lesson", "study method", "study methods",
    "learning advice", "course structure", "summary", "summaries", "introduction",
    "cours", "étudiant", "étudiants", "méthode", "méthodes", "apprentissage",
    "conseil", "conseils", "structure du cours", "résumé", "résumés",
    "مقدمة", "طلاب", "طالب", "طلبة", "الدراسة", "التعلم", "نصائح", "منهجية الدراسة",
]

QUALITY_ACTION_VERBS = {
    "en": ["write", "list", "solve", "compare", "classify", "identify", "summarize", "explain", "calculate", "apply", "draw", "define"],
    "fr": ["écris", "écrire", "liste", "lister", "résume", "résumer", "compare", "comparer", "classe", "classer", "identifie", "identifier", "explique", "expliquer", "calcule", "calculer", "applique", "appliquer", "définis", "définir"],
    "ar": ["اكتب", "اذكر", "عدد", "حل", "قارن", "صنف", "حدد", "لخص", "اشرح", "احسب", "طبق", "ارسم", "عرف", "فسر"],
}


def count_words(text: str) -> int:
    if not isinstance(text, str):
        return 0
    return len([word for word in text.split() if word.strip()])


def is_short_text(text: str, max_words: int) -> bool:
    return isinstance(text, str) and count_words(text) <= max_words


def contains_meta_content(text: str) -> bool:
    if not isinstance(text, str):
        return False

    text = text.lower()

    meta_phrases = [
        # EN
        "according to the text",
        "based on the document",
        "in this document",
        "the text states",

        # FR
        "selon le texte",
        "dans ce document",
        "le texte indique",

        # AR
        "حسب النص",
        "كما ورد في النص",
        "في هذا النص",
        "يشير النص",
    ]

    return any(p in text for p in meta_phrases)


def has_math_or_long_explanation(text: str) -> bool:
    if not isinstance(text, str):
        return False
    markers = ["\\", "$", "{", "}", "\\[", "\\(", "=", "theorem states", "identity states", "proof", "example 1", "example 2"]
    lower = text.lower()
    return any(marker in lower for marker in markers)


def detect_domain(text: str) -> str:
    if not isinstance(text, str):
        return "general"

    text = text.lower()

    math_keywords = [
        "equation", "theorem", "math", "mathematics", "algebra",
        "integral", "derivative", "gcd", "lcm", "mod", "modular",
        "function", "geometry", "calculus", "probability",
        "équation", "théorème", "math", "mathématiques", "algèbre",
        "intégrale", "dérivée", "pgcd", "ppcm", "géométrie",
        "معادلة", "مبرهنة", "نظرية", "رياضيات", "جبر", "تكامل",
        "اشتقاق", "هندسة", "احتمالات", "قسمة", "قاسم",
    ]

    law_keywords = [
        "law", "article", "juridique", "droit", "legal", "contract",
        "constitution", "civil", "criminal", "court", "judge",
        "loi", "contrat", "constitutionnel", "pénal", "tribunal",
        "قانون", "القانون", "عقد", "دستور", "جنائي", "مدني", "محكمة",
    ]

    medical_keywords = [
        "cell", "organ", "disease", "medical", "medicine", "biology",
        "anatomy", "physiology", "diagnosis", "treatment",
        "cellule", "organe", "maladie", "médical", "médecine",
        "biologie", "anatomie", "physiologie", "diagnostic", "traitement",
        "خلية", "عضو", "مرض", "طب", "طبي", "بيولوجيا", "تشريح", "علاج",
    ]

    if any(keyword in text for keyword in math_keywords):
        return "math"
    if any(keyword in text for keyword in law_keywords):
        return "law"
    if any(keyword in text for keyword in medical_keywords):
        return "medical"
    return "general"


def starts_with_action_verb(task: str, lang: str) -> bool:
    if not isinstance(task, str):
        return False

    task = task.strip().lower()

    verbs_en = [
        "write", "list", "solve", "compare", "identify",
        "explain", "apply", "describe", "analyze", "verify"
    ]

    verbs_fr = [
        "écrire", "lister", "résoudre", "comparer",
        "identifier", "expliquer", "appliquer",
        "décrire", "analyser", "vérifier"
    ]

    verbs_ar = [
        "اكتب", "سجل", "اشرح", "قارن", "حدد",
        "طبق", "اقترح", "ناقش", "قيم", "صف",
        "اذكر", "حلل", "استخرج", "بين"
    ]

    # global verbs (multilingual robustness)
    verbs = verbs_en + verbs_fr + verbs_ar

    return any(task.startswith(v) for v in verbs)


def add_quality_error(errors: list, message: str, limit: int = 80) -> None:
    clean = re.sub(r"\s+", " ", str(message)).strip()
    if len(clean) > limit:
        clean = clean[: limit - 3].rstrip() + "..."
    errors.append(clean)


def validate_summary_quality(data: dict, errors: list) -> None:
    summary = data.get("summary", "")
    detailed_summary = data.get("detailed_summary", "")
    if not isinstance(summary, str) or not summary.strip():
        add_quality_error(errors, "Missing summary")
    if not isinstance(detailed_summary, str) or not detailed_summary.strip():
        add_quality_error(errors, "Missing detailed_summary")
    if count_words(summary) > 130:
        add_quality_error(errors, "Summary is too long")
    if count_words(detailed_summary) < 40:
        add_quality_error(errors, "Detailed summary is too short")


def validate_visual_summary_quality(data: dict, errors: list) -> None:
    visual_summary = data.get("visual_summary", {})
    if not isinstance(visual_summary, dict):
        add_quality_error(errors, "visual_summary must be an object")
        return
    main_topic = visual_summary.get("main_topic", "")
    key_points = visual_summary.get("key_points", [])
    if not isinstance(main_topic, str) or not main_topic.strip():
        add_quality_error(errors, "Missing visual_summary.main_topic")
    if not isinstance(key_points, list):
        add_quality_error(errors, "visual_summary.key_points must be a list")
        return
    if not 3 <= len(key_points) <= 6:
        add_quality_error(errors, "visual_summary.key_points should contain 3 to 6 points")
    for point in key_points:
        if not isinstance(point, str) or not point.strip():
            add_quality_error(errors, "Empty visual summary key point")
            continue
        if not is_short_text(point, 6):
            add_quality_error(errors, f"Visual point too long: {point}")
        if contains_meta_content(point):
            add_quality_error(errors, f"Meta content in visual point: {point}")


def validate_diagram_quality(data: dict, errors: list) -> None:
    diagram = data.get("visual_diagram", "")
    if not isinstance(diagram, str) or not diagram.strip():
        add_quality_error(errors, "Missing visual_diagram")
        return
    lines = [line for line in diagram.splitlines() if line.strip()]
    if not diagram.strip().startswith("mindmap"):
        add_quality_error(errors, "Diagram must start with mindmap")
    if "root((" not in diagram:
        add_quality_error(errors, "Diagram missing root node")
    if len(lines) < 4:
        add_quality_error(errors, "Diagram is too small")
    if len(lines) > 35:
        add_quality_error(errors, "Diagram is too large")


def validate_quiz_quality(quiz: list, errors: list, name: str) -> None:
    if not isinstance(quiz, list):
        add_quality_error(errors, f"{name} must be a list")
        return
    if len(quiz) != 5:
        add_quality_error(errors, f"{name} must contain exactly 5 questions")
    seen_questions = set()
    for index, question in enumerate(quiz, start=1):
        if not isinstance(question, dict):
            add_quality_error(errors, f"{name} question {index} is invalid")
            continue
        text = question.get("question", "")
        options = question.get("options", [])
        correct_answer = question.get("correct_answer", "")
        explanation = question.get("explanation", "")
        normalized_question = re.sub(r"\s+", " ", str(text)).strip().lower()
        if normalized_question in seen_questions:
            add_quality_error(errors, f"{name} has duplicate questions")
        seen_questions.add(normalized_question)
        if not isinstance(text, str) or len(text.strip()) < 10:
            add_quality_error(errors, f"{name} question {index} is too short")
        if contains_meta_content(text):
            add_quality_error(errors, f"{name} question {index} contains meta content")
        if not isinstance(options, list) or len(options) != 4:
            add_quality_error(errors, f"{name} question {index} must have 4 options")
        if correct_answer not in ["A", "B", "C", "D"]:
            add_quality_error(errors, f"{name} question {index} has invalid correct_answer")
        if not isinstance(explanation, str) or len(explanation.strip()) < 10:
            add_quality_error(errors, f"{name} question {index} missing explanation")


def validate_flashcards_quality(cards: list, errors: list) -> None:
    if not isinstance(cards, list):
        add_quality_error(errors, "flashcards must be a list")
        return
    if len(cards) != 8:
        add_quality_error(errors, "flashcards should contain exactly 8 cards")
    seen_fronts = set()
    for index, card in enumerate(cards, start=1):
        if not isinstance(card, dict):
            add_quality_error(errors, f"Flashcard {index} is invalid")
            continue
        front = card.get("front", "")
        back = card.get("back", "")
        if not isinstance(front, str) or not front.strip():
            add_quality_error(errors, f"Flashcard {index} missing front")
        normalized_front = re.sub(r"\s+", " ", str(front)).strip().lower()
        if normalized_front in seen_fronts:
            add_quality_error(errors, "Duplicate flashcard front")
        seen_fronts.add(normalized_front)
        if not isinstance(back, str) or not back.strip():
            add_quality_error(errors, f"Flashcard {index} missing back")
        elif not is_short_text(back, 14):
            add_quality_error(errors, f"Flashcard definition too long: {front}")


def validate_study_plan_quality(plan: list, errors: list, output_language: str) -> None:
    if not isinstance(plan, list):
        add_quality_error(errors, "study_plan must be a list")
        return
    if len(plan) != 5:
        add_quality_error(errors, "study_plan must contain exactly 5 days")
    for index, day in enumerate(plan, start=1):
        if not isinstance(day, dict):
            add_quality_error(errors, f"Study day {index} is invalid")
            continue
        tasks = day.get("tasks", [])
        if not day.get("day"):
            add_quality_error(errors, f"Study day {index} missing day label")
        if not day.get("focus"):
            add_quality_error(errors, f"Study day {index} missing focus")
        if not isinstance(tasks, list) or len(tasks) != 3:
            add_quality_error(errors, f"Study day {index} must have exactly 3 tasks")
            continue
        for task in tasks:
            if not isinstance(task, str) or not task.strip():
                add_quality_error(errors, f"Study day {index} contains empty task")
                continue
            if not is_short_text(task, 14):
                add_quality_error(errors, f"Study task too long: {task}")
            domain = detect_domain(task)
            if "\n" in task or "\r" in task or (domain != "math" and has_math_or_long_explanation(task)):
                add_quality_error(errors, f"Invalid study task content: {task}")
            if not starts_with_action_verb(task, output_language):
                add_quality_error(errors, f"Study task should start with an action verb: {task}")


def quality_validate_study_response(result: dict, output_language: str = "en") -> dict:
    errors = []
    if not isinstance(result, dict):
        return {"score": 0, "valid": False, "errors": ["Result must be a dictionary"]}
    validate_summary_quality(result, errors)
    validate_visual_summary_quality(result, errors)
    validate_diagram_quality(result, errors)
    validate_quiz_quality(result.get("theoretical_quiz", []), errors, "theoretical_quiz")
    validate_quiz_quality(result.get("practical_quiz", []), errors, "practical_quiz")
    validate_flashcards_quality(result.get("flashcards", []), errors)
    validate_study_plan_quality(result.get("study_plan", []), errors, output_language)
    score = max(0, 100 - len(errors) * 3)
    return {"score": score, "valid": score >= 80, "errors": errors[:25]}


SUPPORTED_LANGUAGES = {"en", "fr", "ar"}

SUPPORTED_LEVELS = {
    "primary_school",
    "middle_school",
    "high_school",
    "vocational_training",
    "university",
}


def normalize_output_language(output_language: str) -> str:
    if not isinstance(output_language, str):
        return "en"

    value = output_language.strip().lower()

    aliases = {
        "arabic": "ar",
        "arabe": "ar",
        "العربية": "ar",
        "french": "fr",
        "français": "fr",
        "francais": "fr",
        "english": "en",
        "anglais": "en",
    }

    value = aliases.get(value, value)
    return value if value in SUPPORTED_LANGUAGES else "en"


def get_language_name(output_language: str) -> str:
    output_language = normalize_output_language(output_language)

    return {
        "ar": "Arabic",
        "fr": "French",
        "en": "English",
    }.get(output_language, "English")


def normalize_education_level(education_level: str) -> str:
    if not isinstance(education_level, str):
        return "university"

    value = education_level.strip().lower()
    return value if value in SUPPORTED_LEVELS else "university"


def safe_json_loads(value: str) -> dict:
    try:
        data = json.loads(value)
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def is_arabic(text: str) -> bool:
    return isinstance(text, str) and any("\u0600" <= c <= "\u06FF" for c in text)


def is_likely_french(text: str) -> bool:
    if not isinstance(text, str):
        return False

    lower = text.lower()
    french_markers = [
        " le ",
        " la ",
        " les ",
        " des ",
        " une ",
        " un ",
        " ce ",
        " cette ",
        " cours ",
        " document ",
        " économie ",
        " étudiants ",
        " matière ",
        " chapitre ",
        " résumé ",
    ]

    accents = any(c in lower for c in "éèêëàâùûôîïç")
    markers = sum(1 for marker in french_markers if marker in f" {lower} ")

    return accents or markers >= 2


def is_likely_english(text: str) -> bool:
    if not isinstance(text, str):
        return False

    lower = text.lower()
    english_markers = [
        " the ",
        " this ",
        " is ",
        " and ",
        " of ",
        " for ",
        " course ",
        " document ",
        " lesson ",
        " students ",
        " includes ",
        " covers ",
    ]

    markers = sum(1 for marker in english_markers if marker in f" {lower} ")

    return markers >= 2


def translate_to_language(text: str, target_language: str) -> str:
    if not isinstance(text, str) or not text.strip():
        return ""

    language_name = {
        "ar": "Arabic",
        "fr": "French",
        "en": "English",
    }.get(target_language, "English")

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        f"Translate the following text strictly into {language_name}. "
                        "Return only the translated text. "
                        "Do not add explanations. Do not summarize. Preserve the meaning."
                    ),
                },
                {"role": "user", "content": text},
            ],
            temperature=0,
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print("STUDY LANGUAGE TRANSLATION ERROR:", e)
        return text


def enforce_output_language(text: str, output_language: str) -> str:
    if not isinstance(text, str) or not text.strip():
        return ""

    output_language = normalize_output_language(output_language)

    if output_language == "ar":
        if not is_arabic(text):
            return translate_to_language(text, "ar")
        return text

    if output_language == "fr":
        if is_arabic(text) or is_likely_english(text):
            return translate_to_language(text, "fr")
        return text

    if output_language == "en":
        if is_arabic(text) or is_likely_french(text):
            return translate_to_language(text, "en")
        return text

    return text



def generate_visual_summary(detailed_summary: str, output_language: str) -> dict:
    if not isinstance(detailed_summary, str) or not detailed_summary.strip():
        return {
            "main_topic": "",
            "key_points": []
        }

    output_language = normalize_output_language(output_language)

    prompt = f"""
You are Runexa Study Agent.

TASK:
Convert the following detailed summary into a simple visual learning structure.

RULES:
- Extract ONE main topic.
- Extract 4 to 6 key points.
- Keep them VERY SHORT (max 3 to 5 words).
- Prefer keywords, not sentences.
- Avoid explanations.
- Make them visually scannable.
- Combine STRUCTURE + KEY CONCEPTS.
- Each key point should reflect either:
  • a main section/chapter
  • or a central concept
- Do NOT use only structure.
- Do NOT use only glossary.
- Keep a balanced representation of the document.
- If chapters/sections exist, include them, but do not remove important central concepts.
- Avoid meta descriptions like course goals or transitions.
- Use ONLY information from the summary.
- Do NOT add new concepts.
- Include at least 1 or 2 structural elements (chapter/section) if clearly present

STRICT:
- DO NOT include:
  • audience (students)
  • course level
  • general introduction
  • study methods
  • study techniques
  • learning advice
  • course introduction
- ONLY include:
  • academic topics
  • concepts
  • chapters
  • sections

CRITICAL:
- DO NOT include:
  • study methods
  • study techniques
  • learning advice
  • course introduction
- ONLY include:
  • academic topics
  • concepts
  • chapters

LANGUAGE:
- Output must be in {output_language}

RETURN JSON:
{{
  "main_topic": "string",
  "key_points": ["point1", "point2", "point3"]
}}

TEXT:
{detailed_summary}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You generate structured visual summaries."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
            response_format={"type": "json_object"},
        )

        data = safe_json_loads(response.choices[0].message.content)

        main_topic = str(data.get("main_topic", "")).strip()
        key_points = data.get("key_points", [])

        if not isinstance(key_points, list):
            key_points = []

        key_points = [str(p).strip() for p in key_points if p]
        # enforce 3–6 key points
        if len(key_points) < 3:
            key_points = key_points + key_points[: (3 - len(key_points))]

        if len(key_points) > 6:
            key_points = key_points[:6]
        key_points = [p.split(":")[0].strip() for p in key_points if p.split(":")[0].strip()]

        visual_meta_keywords = [
            "students", "student", "level", "audience",
            "طلبة", "طلاب", "طالب", "السنة الأولى",
            "introduction", "general introduction", "course introduction", "مقدمة عامة",
            "study methods", "study techniques", "learning advice",
            "study", "learning", "techniques", "methods",
            "méthodes", "apprentissage", "conseils",
            "طرق الدراسة", "تقنيات الدراسة", "نصائح التعلم"
        ]

        key_points = [
            p for p in key_points
            if not any(k in p.lower() for k in visual_meta_keywords)
        ]

        return {
            "main_topic": enforce_output_language(main_topic, output_language),
            "key_points": [enforce_output_language(p, output_language) for p in key_points],
        }

    except Exception as e:
        print("VISUAL SUMMARY ERROR:", e)
        return {
            "main_topic": "",
            "key_points": []
        }


def normalize_mermaid_mindmap(diagram: str) -> str:
    if not diagram:
        return ""

    lines = diagram.splitlines()

    clean = []
    root_found = False

    for line in lines:
        line = line.strip()

        if not line:
            continue

        if line.startswith("mindmap"):
            clean.append("mindmap")
            continue

        if "root((" in line:
            clean.append("  " + line.strip())
            root_found = True
            continue

        if not root_found:
            continue

        # force level 1
        if not line.startswith("  "):
            clean.append("    " + line)
        else:
            clean.append(line)

    return "\n".join(clean)


def limit_subnodes(diagram: str, max_children=4):
    lines = diagram.splitlines()
    result = []
    count = 0

    for line in lines:
        if line.startswith("      "):
            if count >= max_children:
                continue
            count += 1
        else:
            count = 0

        result.append(line)

    return "\n".join(result)


def fix_mermaid_structure(diagram: str) -> str:
    lines = diagram.splitlines()
    result = []
    root_seen = False

    for line in lines:
        line = line.strip()

        if not line:
            continue

        if line.startswith("mindmap"):
            result.append("mindmap")
            continue

        if "root((" in line:
            result.append("  " + line)
            root_seen = True
            continue

        if root_seen:
            # force indentation
            if not line.startswith("  "):
                result.append("    " + line)
            else:
                result.append(line)

    return "\n".join(result)


def deduplicate_lines(diagram: str) -> str:
    seen = set()
    result = []

    for line in diagram.splitlines():
        key = line.strip()

        if key not in seen:
            seen.add(key)
            result.append(line)

    return "\n".join(result)


def enforce_tree_structure(diagram: str) -> str:
    lines = diagram.splitlines()
    result = []
    level1_seen = False

    for line in lines:
        stripped = line.strip()

        if not stripped:
            continue

        if stripped.startswith("mindmap"):
            result.append("mindmap")
            continue

        if "root((" in stripped:
            result.append("  " + stripped)
            level1_seen = True
            continue

        if level1_seen:
            if not line.startswith("    "):
                result.append("    " + stripped)
            else:
                result.append(line)

    return "\n".join(result)


def remove_similar_nodes(diagram: str) -> str:
    seen = set()
    result = []

    for line in diagram.splitlines():
        key = line.strip().lower()

        if key not in seen:
            seen.add(key)
            result.append(line)

    return "\n".join(result)


def limit_children(diagram: str, max_children=4):
    lines = diagram.splitlines()
    result = []
    count = 0

    for line in lines:
        if line.startswith("      "):
            if count >= max_children:
                continue
            count += 1
        else:
            count = 0

        result.append(line)

    return "\n".join(result)


def generate_visual_diagram(
    text: str,
    detailed_summary: str,
    visual_summary: dict,
    output_language: str
) -> str:

    main_topic = visual_summary.get("main_topic", "")
    key_points = visual_summary.get("key_points", [])

    if not main_topic or not key_points:
        return ""

    prompt = f"""
You are Runexa Study Agent.

TASK:
Create a Mermaid mindmap.

RULES:
- Use EXACT Mermaid mindmap syntax
- Root = main topic
- First level = key points
- Second level = sub ideas from detailed summary
- Max 2 levels under root
- Keep labels SHORT (2-5 words)
- Use ONLY provided content
- Do NOT invent
- Language = {output_language}

STRICT STRUCTURE RULE:
STRICT INDENTATION:
- Each sub-node must be properly nested under its parent
- Use consistent 2-space indentation
- No broken hierarchy

- Every child node MUST be correctly indented under its parent
- Do NOT break hierarchy

STRICT INDENTATION RULE:
- All first-level nodes must be directly under root
- All sub-nodes must be indented under their parent
- Never leave a node without a parent

DEDUPLICATION RULE:
- Avoid repeating similar concepts
- Merge overlapping ideas into one node

LABEL RULE:
- Keep labels SHORT (2–4 words)
- Simplify long titles into concise labels

QUALITY RULE:
- Exclude audience info (students, level)
- Focus only on core learning content

SIMPLICITY RULE:
- Limit sub-nodes to 2–4 per main node
- Avoid too much detail

STRICT INDENTATION RULE:
- Every main node must be under root
- Every sub-node must be under its parent
- No floating nodes allowed

DEDUPLICATION RULE:
- Do NOT repeat the same concept in multiple branches
- Merge duplicated nodes

SIMPLICITY RULE:
- Max 4 sub-nodes per main node
- Group similar items into one label

FINAL CLEANING RULE:
- Remove meta nodes (intro, study advice, goals)
- Simplify labels (no "Chapter", "Intro", etc.)
- Keep only core learning concepts

FINAL DIAGRAM RULES:
- strict indentation
- no floating nodes

STRICT STRUCTURE:
- Every child MUST be nested under its parent
- No flat or floating nodes
- Use consistent indentation (2 spaces)

STRICT MERMAID:
- 2 spaces indentation EXACTLY
- every child MUST be under parent
- no flat nodes

FORMAT:

mindmap
  root((MAIN))
    Topic 1
      Sub 1
      Sub 2
    Topic 2
      Sub 1

DATA:
Main topic: {main_topic}

Key points:
{key_points}

Detailed summary:
{detailed_summary[:4000]}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You generate Mermaid mindmaps."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
        )

        diagram = response.choices[0].message.content.strip()

        diagram = diagram.replace("```mermaid", "").replace("```", "").strip()

        diagram = enforce_tree_structure(diagram)
        diagram = remove_similar_nodes(diagram)
        diagram = limit_children(diagram)

        return diagram

    except Exception as e:
        print("VISUAL DIAGRAM ERROR:", e)
        return ""


def extract_mermaid_labels(mermaid_code: str) -> list:
    if not mermaid_code:
        return []

    import re

    lines = mermaid_code.splitlines()
    labels = []

    for line in lines:
        line = line.strip()

        if not line or line.startswith("mindmap"):
            continue

        # remove root((...))
        line = re.sub(r"root\(\((.*?)\)\)", r"\1", line)

        # remove indentation
        label = line.strip()

        # ignore code artifacts
        if "```" in label:
            continue

        if label:
            labels.append(label)

    return list(set(labels))


def generate_diagram_explanations(
    labels: list,
    detailed_summary: str,
    output_language: str
) -> dict:

    if not labels:
        return {}

    prompt = f"""
You are Runexa Study Agent.

TASK:
Explain each concept in a simple way.

RULES:
- 1 short explanation per label
- Use ONLY the summary
- No external info
- Simple and clear
- Language = {output_language}

LABELS:
{labels}

TEXT:
{detailed_summary[:4000]}

RETURN JSON:
{{
  "label": "explanation"
}}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You explain concepts simply."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
            response_format={"type": "json_object"},
        )

        return safe_json_loads(response.choices[0].message.content)

    except Exception as e:
        print("EXPLANATIONS ERROR:", e)
        return {}


def get_language_instruction(output_language: str) -> str:
    output_language = normalize_output_language(output_language)

    if output_language == "ar":
        return """
اكتب الملخص باللغة العربية فقط.
يجب أن تكون كل الجمل عربية.
لا تستعمل الإنجليزية ولا الفرنسية.
"""

    if output_language == "fr":
        return """
Écris le résumé uniquement en français.
Toute la réponse doit être en français.
N’utilise pas l’anglais ni l’arabe.
"""

    return """
Write the summary only in English.
The whole summary must be in English.
Do not use Arabic or French.
"""


def build_summary_prompt(output_language: str) -> str:
    language_instruction = get_language_instruction(output_language)

    return f"""
You are Runexa Study Agent.

PART 1 + PART 2 TASK:
Generate:
1. summary: short summary
2. detailed_summary: detailed educational summary

SUPPORTED EDUCATION LEVELS:
- primary_school
- middle_school
- high_school
- vocational_training
- university

SUPPORTED OUTPUT LANGUAGES:
- en: English
- fr: French
- ar: Arabic

UNIVERSAL DOMAIN RULE:
The content may be from any educational domain:
law, religion, science, medicine, economics, business, language, history,
mathematics, technology, philosophy, engineering, aviation, finance, etc.

CONTENT RULES:
- Use ONLY the provided content.
- Do NOT add external knowledge.
- Do NOT guess.
- Do NOT invent missing information.
- Do NOT transform the document into another subject.
- If the document is an exam, say it is an exam.
- If the document is a lesson, say it is a lesson.
- If the document is a worksheet, say it is a worksheet.
- If the document is a course chapter, say it is a course chapter.
- If the document type is unclear, do not invent the type.

SUMMARY RULES:
- Write one short paragraph only.
- Mention the main topic.
- Mention the document type when recognizable.
- Mention the main ideas covered.

LEVEL ADAPTATION RULE (VERY IMPORTANT):
You MUST adapt the explanation to the learner education level:

- primary_school:
  Use very simple words, very short sentences, basic ideas only.

- middle_school:
  Use simple vocabulary, avoid technical terms, explain ideas clearly.

- high_school:
  Use moderate vocabulary, introduce basic concepts with clarity.

- vocational_training:
  Focus on practical understanding and real-world application.

- university:
  Use academic and precise language with correct terminology.

IMPORTANT:
- Do NOT just describe the document.
- You MUST SIMPLIFY or ADAPT the explanation depending on the level.

CRITICAL LANGUAGE RULE:
{language_instruction}

DETAILED SUMMARY RULES:
- Write one developed paragraph.
- Explain the main ideas more clearly than summary.
- Stay strictly faithful to the document.
- Do NOT add external knowledge.
- Adapt the explanation to the learner education level.
CRITICAL STRUCTURE RULE:
- You MUST extract and preserve the STRUCTURE of the document (chapters, sections, progression)
- Do NOT mix structure with glossary terms or isolated concepts
- Prefer chapter/section organization over lists of concepts
- The summary must reflect how the document is organized, not just what it contains

RETURN ONLY VALID JSON:
{{
  "summary": "string",
  "detailed_summary": "string"
}}
"""


def generate_key_points(text: str, education_level: str, output_language: str) -> list[str]:
    language = get_language_name(output_language)

    prompt = f"""
Extract key learning points from the following study material.

RULES:
- Extract 5 to 8 key points.
- Each point must be SHORT (3–5 words max).
- Use keyword-style only.
- No full sentences.
- Each point must represent an important idea.
- Keep them clear and scannable.
- Do NOT repeat the summary.
- Use ONLY information from the text.
- Do NOT add new concepts.
- Adapt to {education_level} level.
- Return in {language}.
- Use ONLY {language}.
- No mixed-language phrases.
- No "-" or bullets.
- Only clean text.

QUALITY RULES:
- Each point must be 3–5 words max
- Use clean keyword style only
- Do NOT write sentences
- Focus on one concept per point
- Prefer core concepts over explanations
- Avoid repeating summary content

FINAL QUALITY RULES:
- Avoid definition style ("is defined as", "يُعرّف بأنه")
- Prefer simple explanatory sentences
- Avoid course descriptions (e.g., "this course aims")
- Focus on actual knowledge learned
- Keep each point under 5 words
- Make points easy to memorize

FINAL STRICT RULES:
- Do NOT describe the course itself (no "this course", "the course aims")
- Do NOT use definition style ("is defined as", "يُعرّف بأنه")
- Focus ONLY on knowledge and concepts learned
- Keep each point under 5 words
- Make each point easy to memorize

FINAL RULES:
- Each key point must be 3 to 5 words MAX
- 3–5 words max
- Use keywords ONLY (no full sentences)
- keywords only
- no sentences
- no mixed languages
- No explanations
- No punctuation at the end
- No "-" or bullets
- Use ONLY {language}
- Definitions must match the education level (more precise for advanced levels)

CRITICAL:
- DO NOT include:
  • study methods
  • learning advice
  • course structure
- ONLY include academic concepts and topics

FINAL RULE:
- Prefer 2–4 words
- Max 3–5 words
- Remove unnecessary words like:
  • history
  • basics
  • introduction

Text:
{text[:4000]}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You extract key learning points."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
        )

        content = response.choices[0].message.content.strip()

        # Convert to list
        points = [
            re.sub(r"^[-•\s]*\d*[\.\-\)]?\s*", "", line).strip()
            for line in content.split("\n")
            if line.strip()
        ]

        meta_keywords = [
            "course", "this course", "aims", "designed",
            "students", "learning", "reviewing", "summarizing",
            "examples", "figures", "understanding",
            "study methods", "study process", "learning advice",
            "course structure", "transition", "review", "synthesis",
            "introduction", "elementary notion"
        ]

        removable_words = [
            "history", "basics", "introduction",
            "historique", "bases", "introduction",
            "تاريخ", "أساسيات", "مقدمة"
        ]

        filtered_points = []

        for p in points:
            if not any(k in p.lower() for k in meta_keywords):
                for word in removable_words:
                    p = re.sub(rf"\b{re.escape(word)}\b", "", p, flags=re.IGNORECASE).strip()
                p = re.sub(r"\s+", " ", p).strip()
                if p:
                    filtered_points.append(p)

        return filtered_points[:8]

    except Exception as e:
        print("KEY POINTS ERROR:", e)
        return []


def generate_theoretical_quiz(text, education_level, output_language):
    language = get_language_name(output_language)

    prompt = f"""
Generate EXACTLY 5 theoretical quiz questions.
- Do not return fewer than 5 questions.
- Do not return more than 5 questions.
- Proofread all text before returning JSON.

RULES:
- Each question has 4 options (A, B, C, D)
- Only one correct answer
- Include explanation
- Use ONLY the text
- No external knowledge

QUIZ STRICT RULES:
- Do NOT ask meta questions
- Do NOT ask about the course itself
- Do NOT ask about objectives, structure, or teaching methods
- Questions must focus ONLY on knowledge and concepts
- Theoretical quiz = definitions and concepts
- Avoid repeating the same concept in both quizzes
- Prefer concept-based questions
- All options MUST be in the same language
- correct_answer must be ONLY A, B, C, or D

CRITICAL QUIZ RULES:
- Do NOT ask about course, objectives, or structure
- Questions must test knowledge ONLY
- All options MUST be in the SAME language
- Options must NOT include A), B), etc.
- correct_answer must be ONLY: A, B, C, or D
- Avoid simple definition questions
- Avoid definition-only questions when possible
- Prefer reasoning and application questions

CRITICAL:
- correct_answer MUST be A/B/C/D ONLY
- NEVER use Arabic letters
- NEVER ask about course or study methods
- ALL text in {language}
- Question AND ALL options MUST be in {language}
- NEVER mix languages
- If language = English → ONLY English
- If language = French → ONLY French
- If language = Arabic → ONLY Arabic
- correct_answer MUST be ONLY one letter: A, B, C, or D
- Do NOT return full sentence as answer
- Do NOT return words like "La généralité"

STRICT CONTENT RULE:
- NEVER ask about:
  • course purpose
  • summaries
  • study methods
  • examples or figures
- Questions must test ONLY concepts

- NEVER ask about:
  • course purpose
  • course structure
  • teaching methods

- Return JSON:

{{
  "questions": [
    {{
      "question": "...",
      "options": ["A", "B", "C", "D"],
      "correct_answer": "A",
      "explanation": "..."
    }}
  ]
}}

Language: {language}

CRITICAL:
- Do NOT include:
  • course structure
  • study process
  • learning advice
- Include ONLY concepts and topics

Text:
{text[:4000]}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You generate quizzes."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            response_format={"type": "json_object"},
        )

        data = safe_json_loads(response.choices[0].message.content)
        return data.get("questions", [])

    except Exception as e:
        print("THEORETICAL QUIZ ERROR:", e)
        return []


def generate_practical_quiz(text, education_level, output_language):
    language = get_language_name(output_language)

    prompt = f"""
Generate EXACTLY 5 practical (application-based) questions.
- Do not return fewer than 5 questions.
- Do not return more than 5 questions.
- Proofread all text before returning JSON.

RULES:
- Real-life scenarios based ONLY on text
- 4 options (A, B, C, D)
- One correct answer
- Include explanation

QUIZ STRICT RULES:
- Do NOT ask meta questions
- Do NOT ask about the course itself
- Do NOT ask about objectives, structure, or teaching methods
- Questions must focus ONLY on knowledge and concepts
- Practical quiz = real-world applications and scenarios
- Avoid repeating the same concept in both quizzes
- Prefer reasoning and application over definitions
- All options MUST be in the same language
- correct_answer must be ONLY A, B, C, or D

CRITICAL QUIZ RULES:
- Do NOT ask about course, objectives, or structure
- Questions must test knowledge ONLY
- All options MUST be in the SAME language
- Options must NOT include A), B), etc.
- correct_answer must be ONLY: A, B, C, or D
- Avoid simple definition questions
- Avoid definition-only questions when possible
- Prefer reasoning and application questions

CRITICAL:
- correct_answer MUST be A/B/C/D ONLY
- NEVER use Arabic letters
- NEVER ask about course or study methods
- ALL text in {language}
- Question AND ALL options MUST be in {language}
- NEVER mix languages
- If language = English → ONLY English
- If language = French → ONLY French
- If language = Arabic → ONLY Arabic
- correct_answer MUST be ONLY one letter: A, B, C, or D
- Do NOT return full sentence as answer
- Do NOT return words like "La généralité"

STRICT CONTENT RULE:
- NEVER ask about:
  • course purpose
  • summaries
  • study methods
  • examples or figures
- Questions must test ONLY concepts

- NEVER ask about:
  • course purpose
  • course structure
  • teaching methods

- Return JSON format:

{{
  "questions": [
    {{
      "question": "...",
      "options": ["A", "B", "C", "D"],
      "correct_answer": "A",
      "explanation": "..."
    }}
  ]
}}

Language: {language}

CRITICAL:
- Do NOT include:
  • course structure
  • study process
  • learning advice
- Include ONLY concepts and topics

Text:
{text[:4000]}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You generate practical quizzes."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.4,
            response_format={"type": "json_object"},
        )

        data = safe_json_loads(response.choices[0].message.content)
        return data.get("questions", [])

    except Exception as e:
        print("PRACTICAL QUIZ ERROR:", e)
        return []





def generate_flashcards(text, education_level, output_language):
    language = get_language_name(output_language)

    prompt = f"""
Generate EXACTLY 8 flashcards from the study material.

RULES:
- Each flashcard must have:
  - front
  - back
- front = clean academic concept only
- back = very short definition (max 12 words)
- Flashcards must be definition-based, not question-based
- Do not use questions like "What is..."
- Use clean concept → definition format
- Use ONLY the text
- No external knowledge
- No course meta
- No study advice
- Keep answers concise
- Avoid long sentences
- Prefer simple memorization style
- Use ONLY {language}
- Definitions must match the education level (more precise for advanced levels)

IMPORTANT:
- Output MUST be entirely in {output_language}.
- Do not use any other language.
- Translate concepts accurately, not word-by-word.
- Use standard academic terminology in the target language.
- Avoid literal translations that change meaning.
- If a concept has a known academic equivalent in the language, use it.
- Only generate real academic concepts.
- Avoid incorrect or artificial terms.
- Use only terms present or implied in the document.

Return JSON:
{{
  "flashcards": [
    {{
      "front": "...",
      "back": "..."
    }}
  ]
}}

Text:
{text[:4000]}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You generate revision flashcards."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            response_format={"type": "json_object"},
        )

        data = safe_json_loads(response.choices[0].message.content)
        return data.get("flashcards", [])

    except Exception as e:
        print("FLASHCARDS ERROR:", e)
        return []


def generate_study_plan(detailed_summary, key_points, education_level, output_language):
    language = get_language_name(output_language)

    prompt = f"""
Create a simple study plan from the summary and key points.

RULES:
- Generate EXACTLY 5 days.
- Each day must have:
  - day
  - focus
  - tasks
- tasks must contain exactly 3 short actions.
- Use ONLY the provided content.
- No external topics.
- No invented chapters.
- Adapt to {education_level}.
- Use ONLY {language}.
- Output MUST be entirely in {output_language}.
- Do not use any other language.
- Make tasks specific to the document content.
- Avoid generic tasks like "review concepts".
- Tasks must be actionable and concrete.
- Each task must describe a clear activity (read, summarize, answer, compare).
- Increase difficulty progressively over days.
- Start with understanding → then analysis → then application.
- Each task must produce an output (write, explain, solve, compare).
- Avoid passive tasks like only "read" or "review".
- Avoid repeating the same learning action across days.
- Each day must introduce new cognitive skills (understand → analyze → apply → evaluate).
- Tasks must NOT include theoretical explanations or long paragraphs.
- Tasks must be short actionable instructions only.
- Tasks must be short (max 1 sentence).
- Tasks must NOT contain explanations, examples, or theory.
- Tasks must only be actionable instructions.
- Tasks must be achievable without external research.
- Ensure smooth progression in difficulty (easy → medium → advanced).
- Each task must be a single short sentence (max 15 words)
- Tasks must NEVER include explanations, examples, or theory
- Tasks must NEVER include formulas or multi-line content
- If output becomes explanatory, STOP and rewrite as tasks
- Tasks must be specific and measurable

STUDY PLAN RULES:
- Each task must be a single short sentence (max 12–15 words)
- Each task must start with an action verb
- Tasks must be actionable, not explanatory
- Tasks must NOT contain:
  - explanations
  - paragraphs
  - formulas or LaTeX
  - examples
  - multi-line text
- If a concept requires explanation (e.g., theorem), convert it into a simple task
- Tasks must be specific and directly executable
- Tasks must be directly executable without ambiguity

CRITICAL PRIORITY RULE:
Study plan formatting rules OVERRIDE ALL other instructions,
including mathematics, theorems, and formulas.

MATH-SPECIFIC CONSTRAINTS:
- Do NOT include formulas, LaTeX, or mathematical derivations
- Do NOT explain theorems or identities
- Convert all math concepts into simple action tasks

STRUCTURE RULES:
- Each day MUST contain exactly 3 tasks
- Tasks must never be empty
- Study plan MUST be written in the output_language

TASK QUALITY RULES:
- Tasks must be SPECIFIC and MEASURABLE
- Avoid vague verbs like: analyze, apply, understand
- Prefer concrete actions like:
  - solve 1 example
  - list 3 elements
  - write 1 definition
  - compare 2 items

STRICT TASK FORMAT:
- Each task MUST be ONE short sentence
- Max 12 words
- NO explanations
- NO formulas
- NO paragraphs
- NO line breaks
- NO examples inside tasks

LANGUAGE RULE:
- All study plan fields (day, focus, tasks) MUST match output_language

Return JSON:
{{
  "study_plan": [
    {{
      "day": "Day 1",
      "focus": "...",
      "tasks": ["...", "..."]
    }}
  ]
}}

Detailed summary:
{detailed_summary[:3000]}

Key points:
{key_points}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You generate study plans."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            response_format={"type": "json_object"},
        )

        data = safe_json_loads(response.choices[0].message.content)
        return data.get("study_plan", [])

    except Exception as e:
        print("STUDY PLAN ERROR:", e)
        return []

def clean_quiz_text(value):
    if not isinstance(value, str):
        return value

    value = value.replace("GCof", "GCD of")
    value = value.replace("GC of", "GCD of")
    value = re.sub(r"\s+", " ", value).strip()

    return value


def clean_options(options):
    return [
        clean_quiz_text(
            opt.replace("A) ", "").replace("B) ", "").replace("C) ", "").replace("D) ", "")
        )
        for opt in options
    ]


def normalize_quiz(questions):
    fixed = []

    if not isinstance(questions, list):
        return []

    for q in questions:
        if not isinstance(q, dict):
            continue

        if "question" in q:
            q["question"] = clean_quiz_text(q["question"])

        if "explanation" in q:
            q["explanation"] = clean_quiz_text(q["explanation"])

        valid_answers = ["A", "B", "C", "D"]
        arabic_map = {"أ": "A", "ب": "B", "ج": "C", "د": "D"}

        if q.get("correct_answer") in arabic_map:
            q["correct_answer"] = arabic_map[q["correct_answer"]]

        if q.get("correct_answer") not in valid_answers:
            # try to match with options
            for i, opt in enumerate(q.get("options", [])):
                if q["correct_answer"] in opt:
                    q["correct_answer"] = ["A", "B", "C", "D"][i]
                    break

        if "options" in q:
            q["options"] = clean_options(q["options"])

        if len(q.get("options", [])) == 4:
            fixed.append(q)

    return fixed[:5]


def remove_duplicate_questions(questions):
    if not isinstance(questions, list):
        return []

    seen = set()
    clean = []

    for q in questions:
        if not isinstance(q, dict):
            continue

        key = re.sub(r"\s+", " ", str(q.get("question", "")).lower()).strip()

        if not key or key in seen:
            continue

        seen.add(key)
        clean.append(q)

    return clean[:5]


def remove_duplicate_flashcards(cards):
    if not isinstance(cards, list):
        return []

    seen = set()
    clean = []

    for card in cards:
        if not isinstance(card, dict):
            continue

        front = str(card.get("front", "")).strip().lower()
        key = re.sub(r"\s+", " ", front)

        if not key or key in seen:
            continue

        seen.add(key)
        clean.append(card)

    return clean


def deduplicate_quiz(quiz: list) -> list:
    seen = set()
    clean = []

    if not isinstance(quiz, list):
        return clean

    for q in quiz:
        if not isinstance(q, dict):
            continue

        text = re.sub(r"\s+", " ", q.get("question", "")).strip().lower()

        if text not in seen:
            seen.add(text)
            clean.append(q)

    return clean[:5]


def deduplicate_flashcards(cards: list) -> list:
    seen = set()
    clean = []

    if not isinstance(cards, list):
        return clean

    for c in cards:
        if not isinstance(c, dict):
            continue

        front = re.sub(r"\s+", " ", c.get("front", "")).strip().lower()

        if front not in seen:
            seen.add(front)
            clean.append(c)

    return clean[:8]


def fix_study_plan(plan: list, domain: str) -> list:
    fallback_focus = f"{domain.capitalize()} review"

    clean = []

    if not isinstance(plan, list):
        return clean

    for i, day in enumerate(plan):
        if not isinstance(day, dict):
            continue

        tasks = day.get("tasks", [])[:3]

        clean.append({
            "day": day.get("day") or f"Day {i+1}",
            "focus": day.get("focus") or fallback_focus,
            "tasks": tasks
        })

    return clean[:5]


meta_keywords = ["course", "study", "introduction"]

def filter_meta_questions(questions):
    clean = [
        q for q in questions
        if not any(k in q["question"].lower() for k in meta_keywords)
    ]

    return clean[:5]


def clean_quiz_questions(questions):
    clean = []

    if not isinstance(questions, list):
        return clean

    for q in questions:
        if not isinstance(q, dict):
            continue

        question = str(q.get("question", "")).strip()

        # skip meta content
        if contains_meta_content(question):
            continue

        if len(question.split()) < 5:
            continue

        clean.append(q)

    return clean[:5]


def fill_missing_quiz(questions):
    if not isinstance(questions, list):
        return []

    filled = questions.copy()

    while len(filled) < 5:
        filled.append({
            "question": "Identify one key concept from the lesson",
            "options": [
                "Main idea",
                "Secondary detail",
                "Example",
                "Irrelevant point"
            ],
            "correct_answer": "A",
            "explanation": "This checks understanding of the main concept."
        })

    return filled[:5]


def fill_missing_flashcards(cards):
    if not isinstance(cards, list):
        return []

    filled = cards.copy()

    i = 1
    while len(filled) < 8:
        filled.append({
            "front": f"Key concept {i}",
            "back": "Main idea of the lesson"
        })
        i += 1

    return filled[:8]

def clean_study_task(task: str) -> str:
    if not isinstance(task, str):
        return ""

    # reject long content (hard rule)
    if len(task) > 120:
        return ""

    # reject multi-line content
    if "\n" in task or "\r" in task:
        return ""

    # reject latex/math blocks
    if any(sym in task for sym in ["\\", "$", "{", "}", "[", "]"]):
        return ""

    task = task.replace("\n", " ").replace("\r", " ")
    task = re.sub(r"\$.*?\$", "", task)
    task = re.sub(r"\\\[.*?\\\]", "", task)
    task = re.sub(r"\\\(.*?\\\)", "", task)
    task = re.sub(r"\s+", " ", task).strip()

    # remove academic verbosity
    task = task.replace("Présenter oralement", "Présenter")
    task = task.replace("Rédiger un paragraphe", "Rédiger")
    task = task.replace("Comparer en deux phrases", "Comparer")

    forbidden_markers = [
        " states that ", " means that ", " for any ", " for all ",
        " example", "examples", "e.g.", "i.e.", "proof", "therefore",
        "theorem states", "identity states", "is defined as",
        "definition is", "can be written", "where", "such that",
        "=", "\\", "{", "}", "$", "\n", "\r"
    ]

    lower = task.lower()

    if any(marker in lower for marker in forbidden_markers):
        if "bézout" in lower or "bezout" in lower:
            return "Apply Bézout's identity to solve one simple equation"
        if "gauss" in lower:
            return "Apply Gauss's theorem to one divisibility problem"
        if "fermat" in lower:
            return "Apply Fermat's theorem to one modular exercise"
        if "theorem" in lower:
            return "Apply the theorem to one short exercise"
        if "identity" in lower:
            return "Apply the identity to one short exercise"
        return ""

    # cut hard length
    words = task.split()
    if len(words) > 12:
        task = " ".join(words[:12]).strip()

    return task


def get_domain_tasks(domain):
    if domain == "math":
        return [
            "Solve 1 example exercise",
            "Apply one formula to a problem",
            "Verify one calculation step",
        ]

    if domain == "law":
        return [
            "Explain one legal concept",
            "Compare two legal rules",
            "Apply rule to case",
        ]

    if domain == "medical":
        return [
            "Describe one process",
            "Identify 3 key elements",
            "Explain one function",
        ]

    return [
        "Write 1 definition",
        "List 3 key elements",
        "Explain one concept",
    ]



def enforce_tasks_quality(tasks, lang):
    clean = []

    if not isinstance(tasks, list):
        return clean

    lang = normalize_output_language(lang)

    for task in tasks:
        if not isinstance(task, str):
            continue

        task = task.strip()
        if not task:
            continue

        # reject too short tasks
        if len(task.split()) < 3:
            continue

        # must start with action verb
        if not starts_with_action_verb(task, lang):
            continue

        clean.append(task)

    return clean[:3]


def clean_study_plan(study_plan, domain_context: str = "", output_language: str = "en"):
    if not isinstance(study_plan, list):
        return []

    domain = detect_domain(domain_context or str(study_plan))
    fallback_tasks = get_domain_tasks(domain)

    cleaned_plan = []

    for day in study_plan:
        if not isinstance(day, dict):
            continue

        tasks = []
        for task in day.get("tasks", []):
            cleaned_task = clean_study_task(task)
            if cleaned_task:
                tasks.append(cleaned_task)

        # enforce quality (V2.3 stable)
        tasks = enforce_tasks_quality(tasks, output_language)

        while len(tasks) < 3:
            tasks.append(fallback_tasks[len(tasks)])

        cleaned_plan.append({
            "day": day.get("day", ""),
            "focus": day.get("focus") or f"{domain.capitalize()} review",
            "tasks": tasks[:3],
        })

    return cleaned_plan

def normalize_day_label(day: str, lang: str) -> str:
    if not isinstance(day, str):
        day = ""

    lang = normalize_output_language(lang)
    num = re.search(r"\d+", day)
    n = num.group() if num else ""

    if lang == "fr":
        return f"Jour {n}"
    if lang == "ar":
        return f"اليوم {n}"
    return f"Day {n}"


def ensure_five_unique(q):
    if not isinstance(q, list):
        return []

    if len(q) >= 5:
        return q[:5]

    # do not duplicate questions after deduplication
    return q

def is_wrong_language(text, lang):
    if not isinstance(text, str):
        return False

    lang = normalize_output_language(lang)

    if lang == "en":
        return any(
            word in text.lower()
            for word in ["droit", "euclidienne", "connecteurs"]
        )

    return False



def stabilize_result(result: dict, output_language: str) -> dict:
    domain = detect_domain(result.get("detailed_summary", ""))

    result["theoretical_quiz"] = fill_missing_quiz(
        remove_duplicate_questions(result.get("theoretical_quiz", []))
    )

    result["practical_quiz"] = fill_missing_quiz(
        remove_duplicate_questions(result.get("practical_quiz", []))
    )

    result["flashcards"] = remove_duplicate_flashcards(
        fill_missing_flashcards(
            remove_duplicate_flashcards(result.get("flashcards", []))
        )
    )

    fixed_plan = []
    for i, day in enumerate(result.get("study_plan", [])[:5]):
        if not isinstance(day, dict):
            continue

        fixed_plan.append({
            "day": day.get("day") or normalize_day_label(f"Day {i+1}", output_language),
            "focus": day.get("focus") or enforce_output_language("Review key concepts", output_language),
            "tasks": day.get("tasks", [])[:3],
        })

    result["study_plan"] = fixed_plan

    return result


def generate_study_summary_only(
    text: str,
    education_level: str = "university",
    output_language: str = "ar",
) -> dict:
    if not isinstance(text, str) or not text.strip():
        return {"summary": ""}

    education_level = normalize_education_level(education_level)
    output_language = normalize_output_language(output_language)

    system_prompt = build_summary_prompt(output_language)
    language_instruction = get_language_instruction(output_language)

    user_prompt = f"""
Education level: {education_level}
Output language code: {output_language}

Mandatory language instruction:
{language_instruction}

Educational content:
{text[:8000]}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0,
            response_format={"type": "json_object"},
        )

        data = safe_json_loads(response.choices[0].message.content)

        summary = str(data.get("summary", "")).strip()
        detailed_summary = str(data.get("detailed_summary", "")).strip()

        summary = enforce_output_language(summary, output_language)
        detailed_summary = enforce_output_language(detailed_summary, output_language)

        visual_summary = generate_visual_summary(detailed_summary, output_language)

        key_points = generate_key_points(text, education_level, output_language)

        theoretical_quiz = generate_theoretical_quiz(text, education_level, output_language)
        practical_quiz = generate_practical_quiz(text, education_level, output_language)

        theoretical_quiz = remove_duplicate_questions(normalize_quiz(theoretical_quiz))
        practical_quiz = remove_duplicate_questions(normalize_quiz(practical_quiz))

        theoretical_quiz = filter_meta_questions(theoretical_quiz)
        practical_quiz = filter_meta_questions(practical_quiz)

        theoretical_quiz = clean_quiz_questions(theoretical_quiz)
        practical_quiz = clean_quiz_questions(practical_quiz)

        theoretical_quiz = fill_missing_quiz(theoretical_quiz)
        practical_quiz = fill_missing_quiz(practical_quiz)

        flashcards = generate_flashcards(text, education_level, output_language)
        flashcards = flashcards if isinstance(flashcards, list) else []
        flashcards = remove_duplicate_flashcards(flashcards)
        flashcards = fill_missing_flashcards(flashcards)
        flashcards = remove_duplicate_flashcards(flashcards)

        flashcards = [
            {
                "front": enforce_output_language(card.get("front", ""), output_language),
                "back": enforce_output_language(card.get("back", ""), output_language),
            }
            for card in flashcards
            if isinstance(card, dict)
        ]

        flashcards = [
            card for card in flashcards
            if not is_wrong_language(card.get("front", ""), output_language)
        ]

        flashcards = remove_duplicate_flashcards(flashcards)
        flashcards = fill_missing_flashcards(flashcards)
        flashcards = remove_duplicate_flashcards(flashcards)

        study_plan = generate_study_plan(
            detailed_summary,
            key_points,
            education_level,
            output_language,
        )
        study_plan = study_plan if isinstance(study_plan, list) else []
        study_plan = clean_study_plan(study_plan, detailed_summary, output_language)

        study_plan = [
            {
                "day": normalize_day_label(d.get("day", ""), output_language),
                "focus": enforce_output_language(
                    d.get("focus") or "Review key concepts",
                    output_language
                ),
                "tasks": [
                    enforce_output_language(t, output_language)
                    for t in d.get("tasks", [])
                    if isinstance(t, str)
                ],
            }
            for d in study_plan
            if isinstance(d, dict)
        ]

        visual_diagram = generate_visual_diagram(
            text=text,
            detailed_summary=detailed_summary,
            visual_summary=visual_summary,
            output_language=output_language,
        )

        labels = extract_mermaid_labels(visual_diagram)

        diagram_explanations = generate_diagram_explanations(
            labels,
            detailed_summary,
            output_language,
        )

        domain = detect_domain(detailed_summary)

        theoretical_quiz = deduplicate_quiz(theoretical_quiz)
        practical_quiz = deduplicate_quiz(practical_quiz)

        flashcards = deduplicate_flashcards(flashcards)

        study_plan = fix_study_plan(study_plan, domain)

        result = {
            "summary": summary,
            "detailed_summary": detailed_summary,
            "visual_summary": visual_summary,
            "visual_diagram": visual_diagram,
            "diagram_explanations": diagram_explanations,
            "key_points": key_points,
            "theoretical_quiz": theoretical_quiz,
            "practical_quiz": practical_quiz,
            "flashcards": flashcards,
            "study_plan": study_plan,
        }

        result["quality"] = quality_validate_study_response(result, output_language)

        if result["quality"]["score"] < 95:
            result = stabilize_result(result, output_language)
            result["quality"] = quality_validate_study_response(result, output_language)

        return validate_study_response(result)

    except Exception as e:
        print("STUDY SUMMARY ONLY ERROR:", e)
        return {"summary": "", "detailed_summary": ""}


def analyze_study_content(
    text: str,
    education_level: str = "university",
    output_language: str = "ar",
    level: str = None,
    language: str = None,
    target_language: str = None,
    **kwargs,
) -> dict:
    final_level = level or education_level or kwargs.get("education_level") or "university"
    final_language = (
        language
        or output_language
        or target_language
        or kwargs.get("language")
        or kwargs.get("output_language")
        or kwargs.get("target_language")
        or "ar"
    )

    return generate_study_summary_only(
        text=text,
        education_level=final_level,
        output_language=final_language,
    )
