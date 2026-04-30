import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You are Runexa Study Agent.

Your job is to help users learn faster from text.

You must:
- Summarize the content clearly
- Extract key learning points
- Generate theoretical quiz questions
- Generate practical quiz questions
- Generate flashcards
- Provide explanations for answers

Rules:
- Theoretical questions test understanding
- Practical questions test application
- Each question must have 4 options
- Include correct_answer
- Include explanation
- Flashcards must be simple and useful
- Return ONLY valid JSON
- Never return markdown
"""

def build_user_prompt(text: str, education_level: str) -> str:
    return f"""
Analyze the following content.

IMPORTANT:
Adapt ALL output to this education level: {education_level}

LEVEL RULES:

Primary school:
- Very simple vocabulary
- Short sentences
- Easy concepts
- Very simple questions

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
- Quiz must have 4 options
- Include correct_answer
- Include explanation
- Adapt difficulty to education level
- No empty fields
- No null values

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

def analyze_study_content(text: str, education_level: str):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": build_user_prompt(text, education_level),
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