import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You are Runexa Study Agent.

Your job is to help users learn faster from text.

You must:
- Summarize the content clearly.
- Extract key learning points.
- Generate theoretical quiz questions.
- Generate practical quiz questions.
- Generate flashcards.
- Provide explanations for answers.
- Adapt the difficulty to the learner education level.
- Return the entire output in the requested output language.

Rules:
- Theoretical questions test understanding.
- Practical questions test application.
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


def build_user_prompt(
    text: str,
    education_level: str,
    output_language: str,
) -> str:
    language_name = get_language_name(output_language)

    return f"""
Analyze the following content.

IMPORTANT:
- Adapt ALL output to this education level: {education_level}
- Return the ENTIRE JSON content in this language: {language_name}
- All values inside the JSON must be written in {language_name}.
- Keep the JSON keys exactly in English as specified.
- Do not translate JSON keys.
- Do not return markdown.
- Do not write anything outside the JSON.

LEVEL RULES:

Primary school:
- Very simple vocabulary
- Short sentences
- Easy concepts
- Very simple questions
- Use simple examples

Middle school:
- Simple explanations
- Basic reasoning
- Slightly more detail

High school:
- Moderate complexity
- Clear explanations
- Analytical questions

Vocational training:
- Practical and real-world examples
- Job-oriented examples
- Application-focused questions

University:
- Advanced vocabulary
- Deep explanations
- Complex reasoning
- Critical thinking questions

Generate:

1. Summary (short and clear)
2. Key points (5 max)
3. Quiz:
   - 5 theoretical questions
   - 5 practical questions
4. Flashcards (5 items)
5. Study plan (3 steps)

STRICT RULES:
- Quiz must have 4 options.
- Include correct_answer.
- Include explanation.
- Adapt difficulty to education level.
- Return all user-facing values in {language_name}.
- No empty fields.
- No null values.

Return EXACT JSON:

{{
  "summary": "short summary",
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
    response = client.chat.completions.create(
        model="gpt-4o-mini",
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
        temperature=0.2,
    )

    content = response.choices[0].message.content

    try:
        return json.loads(content)
    except Exception:
        return {
            "error": "Invalid JSON returned",
            "raw": content,
            "disclaimer": "This is for educational support only.",
        }