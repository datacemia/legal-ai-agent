import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You are Runexa Personal Finance Coach Agent.

Your job is to analyze bank statement text and help users understand their personal spending.

You are not a financial advisor.

You must:
- Analyze bank statements carefully.
- Extract and SUM monetary values.
- Separate income, expenses, and transfers.
- Detect avoidable spending patterns.
- Provide practical saving strategies.
- Detect the currency used in the bank statement.
- Compute a financial_score between 0 and 100.
- financial_score must be an integer.
- Return ONLY valid JSON.
- Never return markdown.
- Never include explanations outside JSON.

Currency detection rules:
- currency_detected must be one of: USD, EUR, MAD, GBP, CAD, unknown.
- If the statement shows $, USD, or dollar, use USD.
- If it shows €, EUR, or euro, use EUR.
- If it shows MAD, DH, DHS, dirham, or dirhams, use MAD.
- If it shows £, GBP, or pound, use GBP.
- If it shows CAD or Canadian dollar, use CAD.
- Keep all numeric values without currency symbols.

Financial score rules:
- 90–100: Excellent (low waste, controlled spending, strong savings behavior)
- 70–89: Good (minor inefficiencies, generally healthy finances)
- 50–69: Moderate (noticeable waste or inconsistent control)
- 0–49: Poor (high waste, lack of control, risky financial behavior)

The financial_score must be based on:
- Ratio of spending vs income
- Presence of waste_detected items
- Amount of discretionary spending such as shopping, entertainment, subscriptions
- Financial risks such as fees, debt, overdraft patterns

Never return null for financial_score. Always compute a score.
"""


def get_language_name(output_language: str) -> str:
    languages = {
        "en": "English",
        "fr": "French",
        "ar": "Arabic",
    }

    return languages.get(output_language, "English")


def build_user_prompt(statement_text: str, output_language: str = "en") -> str:
    language_name = get_language_name(output_language)

    return f"""
Analyze the following bank statement text.

IMPORTANT LANGUAGE RULES:
- Return the ENTIRE JSON content in this language: {language_name}.
- All user-facing values must be written in {language_name}.
- Keep JSON keys exactly in English.
- Do not translate JSON keys.
- Do not write anything outside JSON.

STRICT RULES:
- Deposits, credits, salary, refunds = income.
- Debits, payments, checks, withdrawals, card payments = expenses.
- Outgoing transfers = expenses unless clearly internal.
- Internal transfers = transfers.
- If a transaction line shows an amount in a debit/payment column → COUNT IT as expense.
- You MUST sum all visible outgoing amounts to compute total_spending_estimate.
- total_spending_estimate MUST NOT be 0 if outgoing amounts exist.
- If unclear, estimate conservatively but NEVER return 0 when debits exist.
- Extract numbers even if formatting is messy, for example 1,200.50 or 1200.50.
- NEVER use thousand separators in numbers. Use 103000.00 NOT 103,000.00.
- Use numbers only. No currency symbols.
- Detect currency and return it in currency_detected.
- currency_detected must be one of: USD, EUR, MAD, GBP, CAD, unknown.
- financial_score must be an integer between 0 and 100.
- NEVER return null values.

Return EXACT JSON:
{{
  "summary": "short summary",
  "period_detected": "detected period or unknown",
  "currency_detected": "unknown",
  "total_income_estimate": 0,
  "total_spending_estimate": 0,
  "total_transfers_estimate": 0,
  "main_categories": {{
    "food": 0,
    "rent": 0,
    "subscriptions": 0,
    "utilities": 0,
    "transport": 0,
    "shopping": 0,
    "debt": 0,
    "fees": 0,
    "insurance": 0,
    "healthcare": 0,
    "entertainment": 0,
    "transfers": 0,
    "other": 0
  }},
  "waste_detected": ["item"],
  "saving_strategies": ["item"],
  "risk_notes": ["item"],
  "financial_score": 0,
  "disclaimer": "This is not financial advice. It is for informational purposes only."
}}

Bank statement:
{statement_text[:12000]}
"""


def analyze_bank_statement(
    statement_text: str,
    output_language: str = "en",
):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": build_user_prompt(statement_text, output_language),
            },
        ],
        temperature=0.1,
    )

    content = response.choices[0].message.content

    try:
        return json.loads(content)
    except Exception:
        return {
            "error": "Invalid JSON returned",
            "raw": content,
            "disclaimer": "This is not financial advice. It is for informational purposes only.",
        }