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
- Detect the currency exactly as it appears in the bank statement.
- Prefer ISO-4217 currency codes whenever possible.
- Examples: USD, EUR, GBP, MAD, AED, SAR, QAR, KWD, BHD, OMR, JOD, CHF, SEK, NOK, DKK, CAD, AUD, NZD, JPY, CNY, INR, SGD, HKD, ZAR, BRL, MXN.
- If a symbol is used, infer the corresponding ISO code when unambiguous.
- Keep the detected currency code exactly as the standard ISO currency code.
- Only return "unknown" when the currency cannot be determined from the statement.
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

Risk assessment rules:
- Never claim negative cashflow unless expenses exceed income.
- Never claim debt risk unless debt, loan payments, unpaid balances, collections, or debt-related transactions are explicitly visible.
- Never claim overdraft risk unless the statement explicitly shows overdraft usage, negative balances, overdraft fees, NSF fees, unpaid fees, or similar indicators.
- Do not infer financial distress from isolated expenses.
- If observed income exceeds observed expenses, do not describe the financial situation as deteriorating, risky, or negative unless explicit risk indicators are present.
- Positive net cashflow should be treated as a positive financial signal.

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
- This includes summary, period_detected, waste_detected, saving_strategies, risk_notes, and disclaimer.
- Do not mix languages inside any JSON value.
- Keep JSON keys exactly in English.
- Do not translate JSON keys.
- Do not write anything outside JSON.



SUMMARY RULES:
- The summary must contain 1 to 3 complete sentences.
- Prefer observed totals when available.
- If observed income or observed expenses are available, use them instead of AI estimates.
- Do not present estimated values as facts when observed values exist.
- The summary must reference observed income, observed expenses, and net cashflow when those values can be inferred.
- The summary must describe the overall financial situation, not individual categories.
- Avoid generic summaries such as:
  "High spending observed."
  "Expenses detected."
  "Transactions found."
- Summaries should explain whether spending exceeds income, income exceeds spending, or cashflow is approximately balanced.

STRICT RULES:
- NEVER invent the statement period.
- Use only dates explicitly present in the statement.
- If both the earliest and latest transaction dates are visible, you may use them to describe the observed statement period.
- If the exact statement period cannot be determined with certainty, set period_detected to "unknown".
- The summary must never mention months or date ranges that are not explicitly proven by the statement.
- If uncertain, refer to "the observed statement period".
- Do not guess January, February, March, etc.
- Do not infer a statement period from a small sample of transactions.
- The summary must not invent dates, months, or statement periods.
- Never infer specific spending categories if transaction descriptions do not provide category information.
- If categories cannot be determined, use generic wording such as:
  "High overall spending observed."
- Do not claim entertainment, shopping, restaurants, subscriptions, or discretionary spending unless explicitly supported by transaction descriptions.
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
- Detect the currency exactly as it appears in the statement.
- Return the ISO currency code when identifiable.
- Return "unknown" only if the currency cannot be determined.
- financial_score must be an integer between 0 and 100.
- Never claim negative cashflow, debt risk, or overdraft risk unless expenses exceed income or the statement explicitly shows debt, overdraft, unpaid balances, collections, or related fees.
- Positive observed net cashflow should not be described as a financial risk.
- Do not generate risk_notes that contradict observed income, observed expenses, or observed net cashflow.
- NEVER return null values.

Return EXACT JSON:
{{
  "summary": "short summary",
  "period_detected": "exact statement period if explicitly known, otherwise unknown",
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
  "disclaimer": "localized disclaimer"
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