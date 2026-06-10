def get_language_name(output_language: str) -> str:
    languages = {
        "en": "English",
        "fr": "French",
        "ar": "Arabic",
    }

    return languages.get(output_language, "English")


def build_analysis_prompt(
    business_data: str,
    output_language: str = "en",
) -> str:
    language_name = get_language_name(output_language)

    return f"""
Analyze the following business data.

LANGUAGE RULES:
- The uploaded business data may be in any language.
- The input language and output language may be different.
- Understand the business data regardless of input language.
- Return the entire JSON content in {language_name}.
- Keep all JSON keys exactly in English.
- Do not translate JSON keys.
- Translate all user-facing explanations into {language_name}.
- Keep company names, product names, dates, amounts, currencies, and column names unchanged when appropriate.
- Mixed-language explanatory output is forbidden.
- Do not write anything outside JSON.

DATA RULES:
- Use detected column mappings when provided.
- If revenue, expenses, date, or category mappings exist, use them.
- Column names may be in English, French, Arabic, Spanish, or another language.
- Infer business meaning from multilingual column names when possible.
- If a column name is ambiguous, explain the uncertainty in data_quality.limitations.
- If data is incomplete, say so clearly.
- Do not invent missing numbers.
- Do not invent trends without date or period data.
- If the file is not business data, explain that clearly.

BUSINESS MODEL DETECTION:
Detect one of:
- saas
- ecommerce
- agency
- restaurant
- marketplace
- general

DOMAIN RULES:
- Work for any business domain.
- Do not force SaaS/ecommerce/agency logic when the data does not support it.
- Use general business analysis when the domain is unclear.

ANTI-HALLUCINATION RULES:
- If a metric is not directly supported, keep it unavailable or explain the limitation.
- Do not create fake CAC, LTV, churn, MRR, ARR, AOV, ROAS, runway, or conversion rate.
- Do not infer exact values from vague text.
- Prefer fewer accurate insights over many unsupported insights.

STRICT OUTPUT RULES:
- Return only valid JSON.
- business_health_score must be an integer between 0 and 100 only when enough business performance data exists.\n- If there is not enough business performance data, set business_health_score to null.
- confidence_level must be: low, medium, or high.
- risk severity must be: low, medium, or high.
- opportunity impact must be: low, medium, or high.
- recommendation priority must be: low, medium, or high.
- charts must be an empty array for now.
- Do not invent forecasts.
- If there is not enough dated historical data, set forecast.available to false.
- data_quality.score must be an integer between 0 and 100.
- Do not return null values except for unavailable KPI scores such as business_health_score.
- Never mention backend, backend-calculated, deterministic backend, internal engine, server, database, API, or system architecture in any user-facing text.
- Use "Business Health Score" instead of any technical score wording.
- Use "verified business metrics" instead of "backend-calculated metrics".

Return EXACT JSON:

{{
  "business_model": "general",
  "confidence_level": "low",
  "executive_summary": "short business summary",
  "business_health_score": null,
  "kpis": {{
    "revenue": 0,
    "expenses": 0,
    "profit": 0,
    "profit_margin_percent": 0,
    "growth_rate_percent": 0,
    "cashflow_status": "unknown"
  }},
  "smart_insights": {{
    "most_important_decision": {{
      "title": "Most important decision this month",
      "decision": "decision text",
      "why": "reason based on data",
      "impact": "high",
      "timeframe": "30 days"
    }},
    "key_insights": ["insight1", "insight2", "insight3"]
  }},
  "risks": [],
  "opportunities": [],
  "recommendations": [],
  "charts": [],
  "forecast": {{
    "available": false,
    "next_month_revenue": 0,
    "next_quarter_revenue": 0,
    "trend": "unknown",
    "explanation": "Forecast requires enough dated revenue data."
  }},
  "data_quality": {{
    "score": 0,
    "limitations": [],
    "missing_fields": []
  }},
  "disclaimer": "This is for business decision support only. Verify important decisions with a qualified professional."
}}

Business data:
{business_data[:12000]}
"""
