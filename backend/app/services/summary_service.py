import json
from openai import OpenAI

from app.config import OPENAI_API_KEY
from app.utils.prompt_loader import load_prompt

client = OpenAI(api_key=OPENAI_API_KEY)


def get_labels(language: str = "en") -> dict:
    labels = {
        "en": {
            "type": "Type",
            "parties": "Parties",
            "duration": "Duration",
            "payment": "Payment",
            "summary": "Summary",
            "main_obligations": "Main obligations",
            "key_points": "Key points",
            "things_to_watch": "Things to watch",
            "no_text": "No text found.",
            "summary_unavailable": "Summary unavailable. Preview:",
            "simplified_unavailable": "Simplified version unavailable. Preview:",
        },
        "fr": {
            "type": "Type",
            "parties": "Parties",
            "duration": "Durée",
            "payment": "Paiement",
            "summary": "Résumé",
            "main_obligations": "Obligations principales",
            "key_points": "Points clés",
            "things_to_watch": "Points à surveiller",
            "no_text": "Aucun texte trouvé.",
            "summary_unavailable": "Résumé indisponible. Aperçu :",
            "simplified_unavailable": "Version simplifiée indisponible. Aperçu :",
        },
        "ar": {
            "type": "النوع",
            "parties": "الأطراف",
            "duration": "المدة",
            "payment": "الدفع",
            "summary": "ملخص",
            "main_obligations": "الالتزامات الرئيسية",
            "key_points": "النقاط الرئيسية",
            "things_to_watch": "نقاط يجب الانتباه لها",
            "no_text": "لم يتم العثور على نص.",
            "summary_unavailable": "الملخص غير متاح. معاينة:",
            "simplified_unavailable": "النسخة المبسطة غير متاحة. معاينة:",
        },
    }

    return labels.get(language, labels["en"])


def calculate_global_risk(analysis_results: list[dict]) -> dict:
    high_count = sum(1 for item in analysis_results if item["risk_level"] == "high")
    medium_count = sum(1 for item in analysis_results if item["risk_level"] == "medium")

    if high_count > 0:
        return {"risk_level": "high", "risk_score": 80}

    if medium_count > 0:
        return {"risk_level": "medium", "risk_score": 50}

    return {"risk_level": "low", "risk_score": 20}


def generate_summary(text: str, language: str = "en") -> str:
    t = get_labels(language)

    if not text:
        return t["no_text"]

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

        output = f"{t['type']}: {contract_type}\n"
        output += f"{t['parties']}: {', '.join(parties)}\n"
        output += f"{t['duration']}: {duration}\n"
        output += f"{t['payment']}: {payment_terms}\n\n"

        output += f"{t['summary']}:\n{summary}\n\n"

        if main_obligations:
            output += f"{t['main_obligations']}:\n"
            output += "\n".join([f"- {item}" for item in main_obligations])

        return output

    except Exception:
        preview = text[:700]
        return f"{t['summary_unavailable']} {preview}..."


def generate_simplified_version(text: str, language: str = "en") -> str:
    t = get_labels(language)

    if not text:
        return t["no_text"]

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
            output += f"\n\n{t['key_points']}:\n"
            output += "\n".join([f"- {item}" for item in key_points])

        if things_to_watch:
            output += f"\n\n{t['things_to_watch']}:\n"
            output += "\n".join([f"- {item}" for item in things_to_watch])

        return output

    except Exception:
        preview = text[:1200]
        return f"{t['simplified_unavailable']} {preview}..."