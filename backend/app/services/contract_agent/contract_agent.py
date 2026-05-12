import json
from openai import OpenAI

from app.config import OPENAI_API_KEY
from app.services.contract_agent.risk_engine import analyze_risk
from app.services.contract_agent.clause_title_extractor import extract_clause_title
from app.utils.prompt_loader import load_prompt

client = OpenAI(api_key=OPENAI_API_KEY)


def normalize_clause_result(ai_result: dict) -> dict:
    return {
        "clause_title": ai_result.get("clause_title", ""),
        "clause_type": ai_result.get("clause_type", "other"),
        "risk_level": ai_result.get("risk_level", "low"),
        "explanation_simple": ai_result.get("explanation_simple", ""),
        "why_it_matters": ai_result.get("why_it_matters", ""),
        "recommendation": ai_result.get("recommendation", ""),
        "confidence": ai_result.get("confidence", "low"),
        "safer_alternative": ai_result.get("safer_alternative", ""),
        "negotiation_advice": ai_result.get("negotiation_advice", ""),
        "negotiation_priority": ai_result.get("negotiation_priority", "medium"),
    }


def analyze_clause(clause: str, language: str = "en") -> dict:
    prompt_template = load_prompt("clause_analysis_prompt.txt")

    prompt = f"""
{prompt_template}

Output language: {language}

Clause:
{clause}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            response_format={"type": "json_object"},
        )

        content = response.choices[0].message.content
        ai_result = json.loads(content)

    except Exception:
        ai_result = {
            "clause_title": "",
            "clause_type": "unknown",
            "risk_level": "low",
            "explanation_simple": "Could not parse AI response",
            "recommendation": "Review manually",
            "why_it_matters": "Not specified",
            "confidence": "low",
            "safer_alternative": "",
            "negotiation_advice": "Review this clause manually.",
            "negotiation_priority": "medium",
        }

    ai_result = normalize_clause_result(ai_result)

    rule_result = analyze_risk(clause, language)

    if rule_result["risk_level"] == "high":
        ai_result["risk_level"] = "high"
        ai_result["negotiation_priority"] = "high"

    elif (
        rule_result["risk_level"] == "medium"
        and ai_result.get("risk_level") == "low"
    ):
        ai_result["risk_level"] = "medium"

        if ai_result.get("negotiation_priority") == "low":
            ai_result["negotiation_priority"] = "medium"

    ai_result["trigger"] = rule_result.get("trigger")

    return ai_result


def analyze_contract_clauses(
    clauses: list[str],
    language: str = "en"
) -> list[dict]:
    results = []

    for clause in clauses[:10]:
        analysis = analyze_clause(clause, language)

        results.append({
            "title": analysis.get("clause_title") or extract_clause_title(clause),
            "original_text": clause[:1000],
            **analysis,
        })

    return results
