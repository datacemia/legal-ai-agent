def get_language_name(output_language: str) -> str:
    languages = {
        "en": "English",
        "fr": "French",
        "ar": "Arabic",
    }

    return languages.get(output_language, "English")


def build_recommendation_prompt(
    analysis_result: dict,
    output_language: str = "en",
) -> str:
    language_name = get_language_name(output_language)

    return f"""
Create ranked business recommendations from the analysis result.

LANGUAGE RULES:
- Output all user-facing text in {language_name}.
- Keep JSON keys in English.
- Return only valid JSON.

RECOMMENDATION RULES:
- Rank by expected business impact.
- Use only issues supported by the data.
- Avoid generic advice.
- Include clear action steps.
- Do not invent unsupported metrics.
- Use only verified backend KPIs.
- Never invent a Business Health Score.
- Never display None, null, Unknown, N/A, or 0 as a valid score.
- If business_health_score is unavailable, state that it could not be calculated.
- If revenue, profit, margin, growth, churn, ROAS, or cashflow are unavailable, clearly state they are unavailable.

Return EXACT JSON:

{{
  "recommendations": [
    {{
      "title": "",
      "priority": "low | medium | high",
      "expected_impact": "",
      "action_steps": []
    }}
  ],
  "quick_wins": [],
  "strategic_actions": [],
  "avoid_doing": []
}}

Analysis result:
{analysis_result}
"""
