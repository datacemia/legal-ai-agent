import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You are Runexa Study Agent.

Your job is to help users learn faster from text.

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
- Do NOT introduce generic AI concepts unless they are present in the content.
- Prefer accuracy over completeness.

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


def fix_mermaid(diagram: str) -> str:
    """
    Ensures Mermaid diagram is safe before sending it to frontend.

    Why:
    - LLMs can sometimes return Mermaid on one single line.
    - Mermaid mindmap requires line breaks and indentation.
    - This prevents frontend render crashes.
    """
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
    """
    Converts any value into a React-safe string.
    Prevents frontend crash: Objects are not valid as a React child.
    """
    if value is None:
        return ""

    if isinstance(value, str):
        return value

    if isinstance(value, (int, float, bool)):
        return str(value)

    if isinstance(value, dict):
        parts = []
        for key, val in value.items():
            parts.append(f"{safe_text(key)}: {safe_text(val)}")
        return " | ".join(parts)

    if isinstance(value, list):
        return " | ".join(safe_text(item) for item in value)

    return str(value)


def safe_string_list(value) -> list[str]:
    """
    Converts lists containing strings/dicts/numbers into a list of strings.
    """
    if value is None:
        return []

    if isinstance(value, list):
        return [safe_text(item) for item in value if safe_text(item)]

    text = safe_text(value)
    return [text] if text else []


def normalize_question(question) -> dict:
    """
    Ensures quiz question fields are React-safe.
    """
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
    """
    Ensures flashcard fields are React-safe.
    """
    if not isinstance(card, dict):
        return {
            "front": safe_text(card),
            "back": "",
        }

    return {
        "front": safe_text(card.get("front", "")),
        "back": safe_text(card.get("back", "")),
    }


def strip_internal_fields(result: dict) -> dict:
    """
    Returns only the frontend-safe public JSON shape.
    Prevents UI issues caused by internal objects.
    """
    if not isinstance(result, dict):
        result = {}

    quiz = result.get("quiz", {})
    if not isinstance(quiz, dict):
        quiz = {}

    flashcards = result.get("flashcards", [])
    if not isinstance(flashcards, list):
        flashcards = []

    return {
        "summary": safe_text(result.get("summary", "")),
        "written_summary": safe_text(result.get("written_summary", "")),
        "visual_summary": safe_text(result.get("visual_summary", "")),
        "visual_diagram": fix_mermaid(safe_text(result.get("visual_diagram", ""))),
        "key_points": safe_string_list(result.get("key_points", [])),
        "quiz": {
            "theory_questions": [
                normalize_question(q)
                for q in quiz.get("theory_questions", [])
                if isinstance(quiz.get("theory_questions", []), list)
            ],
            "practice_questions": [
                normalize_question(q)
                for q in quiz.get("practice_questions", [])
                if isinstance(quiz.get("practice_questions", []), list)
            ],
        },
        "flashcards": [
            normalize_flashcard(card)
            for card in flashcards
        ],
        "study_plan": safe_string_list(result.get("study_plan", [])),
        "disclaimer": safe_text(
            result.get("disclaimer", "This is for educational support only.")
        ),
    }


def normalize_result(result: dict) -> dict:
    """
    Keeps the existing JSON shape stable and prevents missing fields
    from breaking the frontend.

    Also converts non-renderable objects into React-safe strings.
    """
    if not isinstance(result, dict):
        result = {
            "error": "Invalid result format",
            "summary": "",
            "written_summary": "",
            "visual_summary": "",
            "visual_diagram": fallback_mermaid(),
            "key_points": [],
            "quiz": {
                "theory_questions": [],
                "practice_questions": [],
            },
            "flashcards": [],
            "study_plan": [],
            "disclaimer": "This is for educational support only.",
        }

    result["summary"] = safe_text(result.get("summary", ""))
    result["written_summary"] = safe_text(result.get("written_summary", ""))
    result["visual_summary"] = safe_text(result.get("visual_summary", ""))
    result["visual_diagram"] = fix_mermaid(safe_text(result.get("visual_diagram", "")))

    result["key_points"] = safe_string_list(result.get("key_points", []))

    quiz = result.get("quiz", {})
    if not isinstance(quiz, dict):
        quiz = {}

    theory_questions = quiz.get("theory_questions", [])
    practice_questions = quiz.get("practice_questions", [])

    if not isinstance(theory_questions, list):
        theory_questions = []

    if not isinstance(practice_questions, list):
        practice_questions = []

    result["quiz"] = {
        "theory_questions": [
            normalize_question(question) for question in theory_questions
        ],
        "practice_questions": [
            normalize_question(question) for question in practice_questions
        ],
    }

    flashcards = result.get("flashcards", [])
    if not isinstance(flashcards, list):
        flashcards = []

    result["flashcards"] = [
        normalize_flashcard(card) for card in flashcards
    ]

    result["study_plan"] = safe_string_list(result.get("study_plan", []))

    result["disclaimer"] = safe_text(
        result.get("disclaimer", "This is for educational support only.")
    )

    return result


def build_user_prompt(
    text: str,
    education_level: str,
    output_language: str,
) -> str:
    language_name = get_language_name(output_language)

    return f"""
Analyze the following content.

CRITICAL OBJECTIVE:
You must extract knowledge ONLY from the provided content.
Do NOT add external knowledge.
Do NOT guess.
Do NOT generalize beyond the text.
Do NOT invent missing structure.
If something is not clearly present in the content, do NOT include it.

IMPORTANT:
- Adapt ALL output to this education level: {education_level}
- Return the ENTIRE JSON content in this language: {language_name}
- All values inside the JSON must be written in {language_name}.
- Keep the JSON keys exactly in English.
- Do not translate JSON keys.
- Do not return markdown.
- Do not write anything outside the JSON.

LANGUAGE RULES:
- Output MUST be in: {language_name}
- JSON keys MUST stay in English.
- Values MUST be in {language_name}.

STRICT CONTENT RULES:
- Use ONLY information explicitly present in the content.
- Do NOT add external knowledge.
- Do NOT invent concepts.
- Do NOT infer missing categories.
- Do NOT introduce new ideas not found in the content.
- Prefer incomplete accuracy over invented completeness.
- If the content is short, keep the output short and faithful.
- If the source text does not support 5 rich ideas, use simple direct ideas from the source.

STRUCTURE EXTRACTION RULE:
You must follow the ORIGINAL structure of the course when it is present.

Priority order:
1. Definitions
2. Components
3. Types
4. Processes / steps
5. Practical application
6. Conclusion

CATEGORY SEPARATION RULE:
- Do NOT mix components with processes.
- Components are parts of the agent/system, such as environment, sensors, actuators, or decision unit when these are present in the content.
- Processes / steps are actions or workflow stages, such as perception, analysis, decision-making, or execution when these are present in the content.
- Do NOT reuse process steps as components.
- Do NOT reuse components as process steps.
- In visual_summary and visual_diagram, keep each concept under its correct original category.

If a section does NOT exist in the content, do NOT invent it.

LEVEL RULES:

Primary school:
- Very simple vocabulary
- Short sentences

Middle school:
- Simple explanations

High school:
- Moderate complexity

Vocational training:
- Practical examples only if they are supported by the content

University:
- Advanced explanations only if supported by the content


QUANTITY FLEXIBILITY RULE:
- If the content does not support 5 items, generate fewer items.
- Never invent content to meet a fixed number.
- Prefer fewer accurate questions, flashcards, or key points over invented completeness.

LIST PRESERVATION RULE:
- If the content contains a clear list such as types, components, process steps, names, dates, formulas, or numbered items, preserve that list EXACTLY.
- Do NOT replace listed items with alternative categories or similar concepts.
- Do NOT summarize a clear list into vague labels.
- Preserve the original order of listed items when the source gives an order.

WORDING PRECISION RULE:
- When the source provides exact terms (especially in lists),
  preserve the same wording in quiz answers and options.
- Avoid unnecessary singular/plural changes unless required by grammar.
- Prefer exact phrasing from the content over rephrased versions.

LEVEL SAFETY RULE:
- Do NOT simplify or change core concepts when adapting level.
- Only simplify explanation, not the content itself.
- Preserve exact terms from the source regardless of level.

TYPE WORDING RULE:
- Keep original type names even for lower levels.
- Do NOT convert plural forms into simplified singular forms.

LEVEL QUIZ RULE:
- For middle/high school:
  use simple language BUT keep logical questions.
- Include at least one before/after question even for lower levels.


TERMINOLOGY PRESERVATION RULE:
- Do NOT replace technical terms with simplified synonyms.
- Keep original terms from the source even for lower levels.
- You may explain them, but do not rename them.

TYPE STRICT RULE:
- Types must match EXACTLY the source list.
- Do NOT simplify, merge, or rename types.

LEVEL SIMPLIFICATION RULE:
- Simplify sentences, not concepts.
- Keep original structure and terms.
- Add short explanations if needed instead of replacing terms.


QUIZ DIFFICULTY ADAPTATION RULE:
- Adapt quiz complexity to education_level.

Primary school:
- Use very simple recognition questions.
- Avoid complex process reasoning.
- Focus on names and basic roles.

Middle school:
- Use direct understanding questions.
- Include simple before/after process questions.

High school:
- Include process order questions.
- Include simple component-role relationships.

Vocational training:
- Include practical usage questions.
- Focus on what each component does in a real workflow.

University:
- Include system-thinking questions.
- Test relationships between components and process steps.
- Ask before/after, cause/effect, and full workflow questions.

QUIZ INTELLIGENCE RULE:
- Generate questions according to education_level.
- Do NOT make all quiz questions equally difficult.
- For lower levels, prioritize clarity and confidence.
- For higher levels, prioritize reasoning and relationships.
- Practical questions must match the learner level.
- When the content contains a process, include before/after questions when appropriate for the learner level.
- When the content contains components and steps, include relationship questions when appropriate for the learner level.
- Avoid questions that only test memorization, especially for high school, vocational training, and university levels.

Generate:

1. Summary (short and clear):
   - Based only on the provided content
   - No external examples
   - No invented claims

2. Written summary:
   - one single paragraph
   - at least 5 sentences when the content supports it
   - MUST use connectors translated naturally into {language_name}
   - must include the meaning of: first, then, moreover, finally
   - clear and complete
   - no bullet points
   - no opinions
   - no external knowledge

3. Visual summary:
   MUST follow this structure:

CENTRAL TOPIC
│
├── Main idea 1 → keyword
├── Main idea 2 → keyword
└── Main idea 3 → keyword

   - 3 to 5 branches
   - keywords only
   - easy to memorize
   - use ONLY real concepts from the content
   - do NOT use generic labels unless they exist in the content
   - prefer the course section titles when available

4. Visual diagram:

You MUST generate a VALID Mermaid mindmap.

CRITICAL RULE:
The value of "visual_diagram" MUST start EXACTLY with:

mindmap

If it does NOT start with "mindmap", the answer is invalid.

STRICT FORMAT:
The value of visual_diagram MUST follow this exact Mermaid structure:

mindmap
  root((Central topic))
    Main concept from text
      Sub-element from text
    Main concept from text
      Sub-element from text
    Main concept from text
      Sub-element from text

STRICT MERMAID RULES:
- The diagram MUST start with the word: mindmap
- Use real line breaks inside the JSON string.
- Each Mermaid node MUST be on its own line.
- Use indentation with spaces.
- Do NOT write the diagram in one single line.
- Do NOT add markdown fences.
- Do NOT add explanations inside visual_diagram.
- Use 3 to 5 main branches when supported by the content.
- Use short keywords only.
- Avoid special symbols that can break Mermaid parsing.
- Avoid quotes inside Mermaid nodes.
- Avoid parentheses except for root((Central topic)).
- If the content language is Arabic, keep Mermaid text simple and short.
- Do NOT translate the Mermaid keyword "mindmap".
- Do NOT return plain text.
- Do NOT return a list instead of Mermaid.
- Do NOT include generic words like "importance" unless explicitly present in the content.
- Do NOT include external AI concepts.
- Use the same terminology as the content whenever possible.
- Keep components under the components branch only.
- Keep workflow/process steps under the process or cycle branch only.
- Do NOT place perception, analysis, decision-making, or execution under components unless the source explicitly calls them components.
- Do NOT place environment, sensors, actuators, or decision unit under processes unless the source explicitly calls them steps.
- If any node is not supported by the original content, remove it.

DIAGRAM COMPLETENESS VALIDATION:
- Do NOT leave empty main branches.
- Each main branch MUST have at least one child node.
- If a section exists in the content, include its key elements.
- If the content lists items under a section, include those items as children.
- Do NOT create a main branch without children.
- If a branch has no child, remove the branch or add a real child from the content.

HIERARCHY DEPTH RULE:
- The diagram MUST contain at least 3 levels when the content supports it:
  1. Main branches from real sections or real concepts
  2. Sub-elements from listed items or direct details
  3. Detail elements when they are available in the content
- Avoid flat diagrams with only main branches and direct labels.
- If the content allows deeper structure, expand each branch with supported details.
- Do NOT invent details only to create depth.

SYSTEM RELATION RULE:
- The diagram MUST reflect logical relationships between elements when the source content supports them.
- Components must stay under components, and processes must stay under processes.
- If a process exists, show its sequence or workflow order.
- Avoid isolated branches when the source shows a relationship between ideas.
- Do NOT create relationships that are not supported by the content.

TYPE ENRICHMENT RULE:
- If a types section exists, include the listed types under it.
- If the content gives characteristics for a type, include those characteristics as children.
- If the content only lists type names, keep the type names without inventing characteristics.
- Avoid replacing specific types with generic categories.

VALIDATION BEFORE RETURNING JSON:
- Check that visual_diagram starts with "mindmap".
- Check that visual_diagram contains multiple lines.
- Check that each idea is on a separate line.
- Check that every Mermaid node is supported by the source content.
- Check that components and process steps are not mixed.

- Check that every main Mermaid branch has at least one child.
- Check that listed items from the source appear under the correct branch.
- Check that no important section from the content is left empty.
- Check that the diagram is not flat when the source content supports deeper structure.
- Check that process steps are ordered when the source presents an order.
- Check that type names are not replaced by generic labels.

- If invalid, fix it internally before returning JSON.

5. Key points:
   - max 5
   - only from the provided content
   - no generalization

6. Quiz:
   - Up to 5 theoretical questions (based on content)
   - Up to 5 practical questions (based on content)
   - Questions must be based ONLY on the content
   - No external knowledge
   - No unsupported scenarios
   - If practical application is limited in the source, make the practical questions simple and directly connected to the given content
   - The difficulty must match education_level
   - Preserve exact source lists in quiz options and answers
   - Do NOT create questions from concepts not present in the content
   - For university level, include relationship or process-order questions when the content supports them

7. Flashcards:
   - 5 flashcards
   - direct question/answer from the content
   - no invented facts

8. Study plan:
   - 3 steps
   - based on actual sections in the content
   - no external activities unless directly supported by the content

STRICT RULES:
- Quiz must have 4 options
- Include correct_answer
- Include explanation
- No empty fields
- No null values
- visual_summary must be plain text
- visual_diagram must contain real line breaks
- visual_diagram must NOT be one single line
- written_summary must be one paragraph

FINAL VALIDATION:
- Return valid JSON only.
- Ensure all JSON keys are exactly as specified.
- Ensure visual_diagram is valid Mermaid mindmap.
- Ensure visual_diagram contains real line breaks.
- Ensure visual_diagram is NOT a single line.
- Ensure no invented concepts are included.
- Ensure all information exists in the provided content.
- Ensure components and processes are separated correctly.

- Ensure no main branch is empty.
- Ensure all important sections from the content are represented.
- Ensure listed elements from the content are included under their correct branch.
- Ensure the diagram is not flat when hierarchy is supported by the content.
- Ensure branches are not just labels when the source provides meaningful details.
- Ensure logical flow exists when processes are present in the content.
- Ensure no type, component, or process is replaced by a generic category.

- Ensure process branches are nested, not flat.
- Ensure at least one branch reaches depth 4 when hierarchy or process exists.
- Ensure component roles are included when supported by the content.
- Ensure exact source terminology is preferred over vague labels.
- Ensure no weak or generic node remains.
- Ensure clear lists from the source are preserved exactly.
- Ensure quiz difficulty matches education_level.
- Ensure quiz answers and options are supported by the source content.
- Ensure no invented question is added only to reach a fixed count.

- If any rule is broken, fix it before returning JSON.

SELF-CORRECTION ENGINE:
Before returning the final JSON, internally review the visual_diagram.

Step 1 — Extract source sections:
- Identify the real sections in the content.
- Identify listed items under each section.

Step 2 — Check diagram accuracy:
- Every main branch must match a real section or real concept from the content.
- Every child node must come from the content.
- No generic replacement is allowed.
- No empty branch is allowed.

Step 3 — Fix common errors:
- If a definition branch is too vague, add the key definition elements from the text.
- If a practical example is replaced by a generic category, restore the specific example.
- If components and process steps are mixed, separate them.
- If a hierarchy exists in the content, preserve it.
- If the diagram is flat and the content supports hierarchy, expand it using real content only.
- If processes are listed without order, enforce the order supported by the content.
- If components exist without their supported role, connect them to their role only when the content clearly supports it.

Step 4 — Final decision:
- If a node is not supported by the content, remove it.
- If an important listed item is missing, add it under the correct branch.
- If a branch has no child, add supported children or remove the branch.

Step 5 — Fusion 10/10 final check:
- If process steps are flat, convert them into nested sequence.
- If a branch is vague, replace it with exact source terminology.
- If component roles are supported, attach them under the correct component.
- If no branch reaches depth 4 while hierarchy exists, deepen the process branch.
- If a weak node remains, remove it or replace it with source content.

Only after this review, return the final JSON.

GOD MODE ZERO-PROBLEM RULES:

TERMINOLOGY LOCK RULE:
- Use the exact section titles from the source content whenever they are available.
- Do NOT replace source section titles with simplified or vague words.
- Prefer precise source titles such as "خطوات عمل الوكيل" over vague labels such as "العملية" when present.
- Prefer precise source titles such as "مكونات الوكيل" over vague labels such as "المكونات" when present.
- Prefer precise source titles such as "أنواع الوكلاء" over vague labels such as "الأنواع" when present.

ROLE ATTACHMENT RULE:
- Each component should include its role when the content supports it.
- Sensors must connect to perception when both are present.
- Decision unit must connect to decision-making when both are present.
- Actuators or effectors must connect to execution when both are present.
- Avoid listing components without functional meaning when roles are available.
- Do NOT invent component roles that are not supported by the content.

TYPE ENRICHMENT HARD RULE:
- Each type MUST include at least one distinguishing characteristic if available in the content.
- Do NOT leave types as plain labels when the source provides differences.
- If the source only lists type names without characteristics, keep the type names specific and do not invent details.

MANDATORY FLOW STRUCTURE:
- Process branches MUST be nested, not side-by-side.
- Correct structure:
  Process branch
    First step
      Second step
        Third step
          Fourth step
- Incorrect structure:
  Process branch
    First step
    Second step
    Third step
    Fourth step

ZERO WEAK NODE POLICY:
- Weak nodes are not allowed.
- Replace vague nodes with source-specific nodes.
- Remove unsupported vague nodes.
- Never use placeholders to fill missing information.

FUSION 10/10 FINAL RULES:

FLOW STRUCTURE HARD RULE:
- Process branches MUST be nested, never flat.
- Reject flat process representation internally before returning JSON.
- If the source contains ordered steps, represent them as a nested sequence.
- Correct Mermaid structure:
  Steps branch
    First step
      Second step
        Third step
          Fourth step
- Incorrect Mermaid structure:
  Steps branch
    First step
    Second step
    Third step
    Fourth step

SYSTEM LOGIC RULE:
- The diagram must reflect the agent loop when the source supports it.
- If sensors and perception exist, sensors should connect meaningfully to perception.
- If decision unit and decision-making exist, decision unit should connect meaningfully to decision-making.
- If actuators/effectors and execution exist, actuators/effectors should connect meaningfully to execution.
- The diagram should show how the agent works, not only what it contains.
- Do NOT invent relationships that are not supported by the source.

MINIMUM DEPTH RULE:
- At least one branch must reach depth 4 when the source supports ordered steps or hierarchy.
- Depth 4 means: root → main branch → child → subchild → sub-subchild.
- Flat diagrams are invalid when the source contains a process, sequence, or hierarchy.

ROLE ATTACHMENT RULE:
- Components should include their role when the content supports it.
- Sensors → perception when supported.
- Decision unit → decision-making when supported.
- Actuators/effectors → execution when supported.
- Avoid listing components without functional meaning when roles are available.

TYPE ENRICHMENT HARD RULE:
- Each type MUST include at least one distinguishing characteristic if available in the content.
- Do NOT invent characteristics.
- If the source only lists type names, keep type names specific and do not add fake details.

TERMINOLOGY LOCK RULE:
- Use exact section titles from the source content whenever available.
- Prefer precise titles such as "خطوات عمل الوكيل" over vague labels such as "العملية".
- Prefer precise titles such as "مكونات الوكيل" over vague labels such as "المكونات".
- Prefer precise titles such as "أنواع الوكلاء" over vague labels such as "الأنواع".

ZERO WEAK NODE POLICY:
- Weak nodes are forbidden.
- Do NOT use vague nodes such as:
  "general definition", "multiple applications", "various types",
  "تعريف عام", "تطبيقات متعددة", "أنواع مختلفة", "نقاط مهمة".
- Replace weak nodes with exact source concepts or remove them.

FINAL DIAGRAM TARGET:
- The diagram must be stable for frontend rendering.
- The diagram must be a valid Mermaid mindmap.
- The diagram must be pedagogically useful, not only visually correct.
- Prioritize: source faithfulness, nested flow, useful hierarchy, and no generic placeholders.

Return EXACT JSON:

{{
  "summary": "short summary",
  "written_summary": "one complete paragraph summary",
  "visual_summary": "CENTRAL TOPIC\\n│\\n├── Main idea 1 → keyword\\n├── Main idea 2 → keyword\\n└── Main idea 3 → keyword",
  "visual_diagram": "mindmap\\n  root((Central topic))\\n    Main concept from text\\n      Sub-element from text\\n    Main concept from text\\n      Sub-element from text\\n    Main concept from text\\n      Sub-element from text",
  "key_points": ["point1", "point2"],
  "quiz": {{
    "theory_questions": [
      {{
        "question": "string",
        "options": ["A", "B", "C", "D"],
        "correct_answer": "string",
        "explanation": "string"
      }}
    ],
    "practice_questions": [
      {{
        "question": "string",
        "options": ["A", "B", "C", "D"],
        "correct_answer": "string",
        "explanation": "string"
      }}
    ]
  }},
  "flashcards": [
    {{
      "front": "string",
      "back": "string"
    }}
  ],
  "study_plan": ["step1", "step2", "step3"],
  "disclaimer": "This is for educational support only."
}}

Content:
{text[:12000]}
"""


def analyze_study_content(
    text: str,
    education_level: str,
    output_language: str = "en",
):
    """
    Fusion 10/10 final:
    - One OpenAI call only to avoid timeout.
    - Strong prompt intelligence for nested Mermaid flow.
    - React-safe output only.
    - No internal metadata exposed to frontend.
    - Always returns the expected JSON shape.
    """
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

        response_content = response.choices[0].message.content
        result = json.loads(response_content)
        result = normalize_result(result)

        return strip_internal_fields(result)

    except Exception:
        fallback = {
            "summary": "Analysis failed. Please try again with shorter or clearer content.",
            "written_summary": "The analysis could not be completed because the generated response was invalid or the request failed. Please try again.",
            "visual_summary": "MAIN TOPIC\n│\n└── Analysis failed → retry",
            "visual_diagram": fallback_mermaid(),
            "key_points": [
                "Analysis could not be completed.",
                "Try again with shorter content.",
            ],
            "quiz": {
                "theory_questions": [],
                "practice_questions": [],
            },
            "flashcards": [],
            "study_plan": [
                "Retry the analysis.",
                "Use clearer content.",
                "Check backend logs if the problem continues.",
            ],
            "disclaimer": "This is for educational support only.",
        }

        return strip_internal_fields(fallback)

