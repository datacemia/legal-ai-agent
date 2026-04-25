import json
from openai import OpenAI

from app.config import OPENAI_API_KEY
from app.utils.prompt_loader import load_prompt

client = OpenAI(api_key=OPENAI_API_KEY)


def calculate_global_risk(analysis_results: list[dict]) -> dict:
    high_count = sum(1 for item in analysis_results if item["risk_level"] == "high")
    medium_count = sum(1 for item in analysis_results if item["risk_level"] == "medium")

    if high_count > 0:
        return {"risk_level": "high", "risk_score": 80}

    if medium_count > 0:
        return {"risk_level": "medium", "risk_score": 50}

    return {"risk_level": "low", "risk_score": 20}


# 🔥 UPDATED SUMMARY WITH GPT
def generate_summary(text: str, language: str = "en") -> str:
    if not text:
        return "No text found."

    prompt_template = load_prompt("summary_prompt.txt")
    contract_text = text[:6000]

    prompt = f"""
{prompt_template}

Output language: {language}

Contract text:
{contract_text}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            response_format={"type": "json_object"}
        )

        content = response.choices[0].message.content
        data = json.loads(content)

        summary = data.get("global_summary", "")
        contract_type = data.get("contract_type", "")
        parties = data.get("parties", [])
        duration = data.get("duration", "")
        payment_terms = data.get("payment_terms", "")
        main_obligations = data.get("main_obligations", [])

        # 🧠 Build readable output
        output = f"Type: {contract_type}\n"
        output += f"Parties: {', '.join(parties)}\n"
        output += f"Duration: {duration}\n"
        output += f"Payment: {payment_terms}\n\n"

        output += f"Summary:\n{summary}\n\n"

        if main_obligations:
            output += "Main obligations:\n"
            output += "\n".join([f"- {item}" for item in main_obligations])

        return output

    except Exception:
        preview = text[:700]
        return f"Summary unavailable. Preview: {preview}..."


# 🔥 SIMPLIFIED VERSION (GPT)
def generate_simplified_version(text: str, language: str = "en") -> str:
    if not text:
        return "No text found."

    prompt_template = load_prompt("simplification_prompt.txt")
    contract_text = text[:6000]

    prompt = f"""
{prompt_template}

Output language: {language}

Contract text:
{contract_text}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            response_format={"type": "json_object"}
        )

        content = response.choices[0].message.content
        data = json.loads(content)

        simplified = data.get("simplified_version", "")
        key_points = data.get("key_points", [])
        things_to_watch = data.get("things_to_watch", [])

        output = simplified

        if key_points:
            output += "\n\nKey points:\n"
            output += "\n".join([f"- {item}" for item in key_points])

        if things_to_watch:
            output += "\n\nThings to watch:\n"
            output += "\n".join([f"- {item}" for item in things_to_watch])

        return output

    except Exception:
        preview = text[:1200]
        return f"Simplified version unavailable. Preview: {preview}..."