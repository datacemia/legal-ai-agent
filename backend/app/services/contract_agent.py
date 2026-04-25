import json
from openai import OpenAI

from app.config import OPENAI_API_KEY
from app.services.risk_engine import analyze_risk
from app.utils.prompt_loader import load_prompt

client = OpenAI(api_key=OPENAI_API_KEY)


def analyze_clause(clause: str, language: str = "en") -> dict:
    prompt_template = load_prompt("clause_analysis_prompt.txt")

    prompt = f"""
{prompt_template}

Output language: {language}

Clause:
{clause}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        response_format={"type": "json_object"},
    )

    content = response.choices[0].message.content

    try:
        ai_result = json.loads(content)
    except Exception:
        ai_result = {
            "clause_type": "unknown",
            "risk_level": "low",
            "explanation_simple": "Could not parse AI response",
            "recommendation": "Review manually",
            "why_it_matters": "Not specified",
            "confidence": "low",
        }

    rule_result = analyze_risk(clause, language)

    if rule_result["risk_level"] == "high":
        ai_result["risk_level"] = "high"
    elif rule_result["risk_level"] == "medium" and ai_result.get("risk_level") == "low":
        ai_result["risk_level"] = "medium"

    ai_result["trigger"] = rule_result["trigger"]

    return ai_result


def analyze_contract_clauses(clauses: list[str], language: str = "en") -> list[dict]:
    results = []

    for clause in clauses[:10]:
        results.append({
            "original_text": clause[:1000],
            **analyze_clause(clause, language)
        })

    return results