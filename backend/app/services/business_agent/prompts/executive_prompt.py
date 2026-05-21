def get_language_name(output_language: str) -> str:
    languages = {
        "en": "English",
        "fr": "French",
        "ar": "Arabic",
    }

    return languages.get(output_language, "English")


def build_executive_prompt(
    analysis_result: dict,
    output_language: str = "en",
) -> str:
    language_name = get_language_name(output_language)

    return f"""
Create executive-level business insights from this analysis result.

LANGUAGE RULES:
- Output all user-facing text in {language_name}.
- Keep JSON keys in English.
- Return only valid JSON.

EXECUTIVE RULES:
- Focus on the single most important decision.
- Explain why the decision matters now.
- Avoid generic advice.
- Every insight must be supported by the analysis result.
- Do not invent metrics.

Return EXACT JSON:

{{
  "most_important_decision": {{
    "title": "",
    "decision": "",
    "why": "",
    "impact": "low | medium | high",
    "timeframe": ""
  }},
  "executive_insights": [],
  "priority_focus": "",
  "ceo_brief": ""
}}

Analysis result:
{analysis_result}
"""
