import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You are Runexa Business Decision Agent.

Your job is to help entrepreneurs understand business data and make better decisions.

You must:
- Analyze business data carefully.
- Use detected column mappings when provided.
- Identify revenue, expenses, profit, margin, and trends when possible.
- Detect risks, inefficiencies, and opportunities.
- Give practical, concrete action steps.
- Compute a business_health_score between 0 and 100.
- Return ONLY valid JSON.
- Never return markdown.
- Never include explanations outside JSON.

You are not a financial advisor, accountant, lawyer, or business consultant.
Your output is for decision support only.
"""


def build_user_prompt(business_data: str) -> str:
    return f"""
Analyze the following business data.

IMPORTANT:
The parser may provide a "Detected column mapping" section.
Use it to understand which columns represent:
- revenue
- expenses
- date
- category

If mapping is missing or incomplete, infer carefully from column names and sample rows.

STRICT RULES:
- business_health_score must be an integer between 0 and 100.
- If exact metrics are unclear, estimate carefully from visible data.
- Do not return null values.
- Use numbers only for numeric fields.
- Keep the output practical for entrepreneurs.
- Focus on what the user should do next.
- If revenue and expense columns exist, calculate profit as revenue minus expenses.
- If profit margin can be calculated, use: profit / revenue * 100.
- If revenue is 0, profit_margin_percent must be 0.
- Detect clear trends only when date/period information exists.

Return EXACT JSON:

{{
  "summary": "short business summary",
  "business_health_score": 0,
  "metrics": {{
    "revenue_estimate": 0,
    "expenses_estimate": 0,
    "profit_estimate": 0,
    "profit_margin_percent": 0
  }},
  "key_insights": ["insight1", "insight2", "insight3"],
  "risks": ["risk1", "risk2"],
  "opportunities": ["opportunity1", "opportunity2"],
  "action_plan": ["action1", "action2", "action3"],
  "disclaimer": "This is for business decision support only. Verify important decisions with a qualified professional."
}}

Business data:
{business_data[:12000]}
"""


def analyze_business_data(business_data: str):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_user_prompt(business_data)},
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
            "disclaimer": "This is for business decision support only.",
        }