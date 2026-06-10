def get_language_name(output_language: str) -> str:
    languages = {
        "en": "English",
        "fr": "French",
        "ar": "Arabic",
    }

    return languages.get(output_language, "English")


def build_forecast_prompt(
    historical_data: str,
    output_language: str = "en",
) -> str:
    language_name = get_language_name(output_language)

    return f"""
Analyze whether forecasting is possible from the historical business data.

LANGUAGE RULES:
- Output all user-facing text in {language_name}.
- Keep JSON keys in English.
- Return only valid JSON.

FORECASTING RULES:
- Do not invent forecasts.
- Forecast only when there is enough dated historical data.
- If fewer than 3 reliable periods exist, set available to false.
- If revenue data is unavailable, keep next_month_revenue and next_quarter_revenue at 0 and explain why forecasting is unavailable.
- Never infer revenue forecasts from product catalogs, inventory files, CRM exports, reference tables, or non-performance datasets.
- Do not treat missing revenue as revenue equal to 0.
- Explain limitations clearly.
- Keep predictions conservative.

Return EXACT JSON:

{{
  "available": false,
  "next_month_revenue": 0,
  "next_quarter_revenue": 0,
  "trend": "unknown",
  "confidence": "low",
  "cashflow_risk": "unknown",
  "seasonality_detected": false,
  "explanation": "Forecast unavailable because insufficient dated revenue data was provided."
}}

Historical data:
{historical_data[:12000]}
"""
