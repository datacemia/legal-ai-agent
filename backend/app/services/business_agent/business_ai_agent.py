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


def get_language_name(output_language: str) -> str:
    languages = {
        "en": "English",
        "fr": "French",
        "ar": "Arabic",
    }

    return languages.get(output_language, "English")


def build_user_prompt(business_data: str, output_language: str = "en") -> str:
    language_name = get_language_name(output_language)

    return f"""
Analyze the following business data.

IMPORTANT LANGUAGE RULES:
- Return the ENTIRE JSON content in this language: {language_name}.
- All user-facing values must be written in {language_name}.
- Keep JSON keys exactly in English.
- Do not translate JSON keys.
- Do not write anything outside JSON.

IMPORTANT DATA RULES:
The parser may provide a "Detected column mapping" section.
Use it to understand which columns represent:
- revenue
- expenses
- date
- category

If mapping is missing or incomplete, infer carefully from column names and sample rows.

DOMAIN DETECTION RULE:
- First identify whether the provided content is actually business data.
- If the content is not business data, do NOT invent revenue, expenses, profit, margin, risks, or opportunities.
- If the content looks like a legal contract, academic course, random text, or unrelated document, say so clearly in the summary.
- When the domain is not business data, keep numeric metrics at 0 and business_health_score low.
- Do not transform non-business content into fake business analysis.

ANTI-HALLUCINATION RULE:
- If a metric, trend, category, risk, or opportunity is not supported by the provided data, do NOT invent it.
- Do not create fake numbers.
- Do not infer exact values from vague text.
- If only partial information exists, use cautious language in user-facing text.
- Prefer fewer accurate insights over many unsupported insights.

DATA QUALITY RULE:
- Assess whether the data is complete enough for reliable business analysis.
- If important fields are missing, mention the limitation in key_insights or risks.
- If revenue or expenses are missing, do not calculate fake profit.
- If date or period fields are missing, do not claim trends.
- If rows are too few, avoid strong conclusions.

COLUMN MAPPING RULE:
- Use detected mappings when provided.
- Do not override detected mappings unless they are clearly impossible.
- If columns are ambiguous, explain the uncertainty in insights.
- Never treat unrelated columns as revenue or expenses just to fill metrics.

STRICT RULES:
- business_health_score must be an integer between 0 and 100.
- If exact metrics are unclear, estimate carefully only from visible numeric data.
- Do not return null values.
- Use numbers only for numeric fields.
- Keep the output practical for entrepreneurs.
- Focus on what the user should do next.
- If revenue and expense columns exist, calculate profit as revenue minus expenses.
- If profit margin can be calculated, use: profit / revenue * 100.
- If revenue is 0, profit_margin_percent must be 0.
- Detect clear trends only when date/period information exists.

FINAL VALIDATION:
- Check that all numbers are supported by visible data or clearly cautious estimates.
- Check that no unsupported business concepts were invented.
- Check that non-business documents are not forced into business analysis.
- Check that risks, opportunities, and action_plan items are practical and grounded in the provided data.
- If any rule is broken, fix it before returning JSON.

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


def analyze_business_data(
    business_data: str,
    output_language: str = "en",
):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": build_user_prompt(business_data, output_language),
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
            "disclaimer": "This is for business decision support only.",
        }
