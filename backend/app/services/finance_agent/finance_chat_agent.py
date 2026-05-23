import json

from app.services.finance_agent.finance_ai_agent import client


SYSTEM_PROMPT = """
You are Runexa Personal Finance AI Coach.

You help users understand:
- spending
- subscriptions
- savings opportunities
- budgeting
- cashflow
- financial habits
- financial risks

You must:
- be practical
- be concise
- be action-oriented
- explain financial situations clearly

You are NOT:
- a financial advisor
- a tax advisor
- an investment advisor

Never invent information.
Use ONLY the provided financial analysis context.
"""


def build_finance_context(
    analysis_result: dict,
) -> str:
    safe_context = {
        "summary": analysis_result.get("summary"),
        "currency": analysis_result.get(
            "currency_detected"
        ),
        "financial_score": analysis_result.get(
            "financial_score"
        ),
        "cashflow_forecast": analysis_result.get(
            "cashflow_forecast"
        ),
        "recommended_budget": analysis_result.get(
            "recommended_budget"
        ),
        "subscriptions_detected": analysis_result.get(
            "subscriptions_detected"
        ),
        "savings_opportunities": analysis_result.get(
            "savings_opportunities"
        ),
        "financial_habit_scores": analysis_result.get(
            "financial_habit_scores"
        ),
        "financial_insights": analysis_result.get(
            "financial_insights"
        ),
        "waste_detected": analysis_result.get(
            "waste_detected"
        ),
        "saving_strategies": analysis_result.get(
            "saving_strategies"
        ),
        "risk_notes": analysis_result.get(
            "risk_notes"
        ),
    }

    return json.dumps(
        safe_context,
        ensure_ascii=False,
        indent=2,
    )


def answer_finance_question(
    analysis_result: dict,
    question: str,
    output_language: str = "en",
):
    context = build_finance_context(analysis_result)

    prompt = f"""
Answer in this language: {output_language}

Financial analysis context:
{context}

User question:
{question}

Return ONLY valid JSON with this exact structure:
{{
  "answer": "clear coaching answer",
  "suggested_questions": [
    "short follow-up question 1",
    "short follow-up question 2",
    "short follow-up question 3"
  ]
}}

Rules:
- The answer must be practical, concise, and action-oriented.
- Suggested questions must be short.
- Do not include markdown outside JSON.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.3,
    )

    content = response.choices[0].message.content

    try:
        data = json.loads(content)
    except Exception:
        data = {
            "answer": content,
            "suggested_questions": [],
        }

    return {
        "answer": data.get("answer", ""),
        "suggested_questions": data.get("suggested_questions", []),
        "language": output_language,
    }
