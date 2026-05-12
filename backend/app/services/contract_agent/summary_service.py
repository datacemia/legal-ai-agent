import re

from app.utils.prompt_loader import load_prompt
from app.services.contract_agent.ai_client import call_json_ai
from app.services.contract_agent.summary_normalizer import (
    get_not_specified,
    normalize_contract_summary,
    normalize_simplified_contract,
)


MAX_SUMMARY_CHARS = 12_000
MAX_SIMPLIFICATION_CHARS = 12_000


def extract_jurisdiction(text: str) -> dict:
    text_lower = text.lower()

    governing_law_patterns = [
        r"laws of the state of ([a-zA-Z\s]+)",
        r"governed by the laws of ([a-zA-Z\s]+)",
        r"governed under the laws of ([a-zA-Z\s]+)",
        r"laws of ([a-zA-Z\s]+)",
    ]

    arbitration_patterns = [
        r"arbitrated.*?in ([a-zA-Z\s,]+)",
        r"resolved.*?in ([a-zA-Z\s,]+)",
        r"courts of ([a-zA-Z\s,]+)",
    ]

    governing_law = None
    dispute_location = None

    for pattern in governing_law_patterns:
        match = re.search(pattern, text_lower)

        if match:
            governing_law = match.group(1).strip().title()
            break

    for pattern in arbitration_patterns:
        match = re.search(pattern, text_lower)

        if match:
            dispute_location = match.group(1).strip().title()
            break

    return {
        "governing_law": governing_law,
        "dispute_location": dispute_location,
    }


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
            "contract_score": "Contract Score",
            "contract_complexity": "Contract Complexity",
            "overall_balance": "Overall Balance",
            "jurisdiction": "Jurisdiction",
            "jurisdiction_note": "Jurisdiction Note",
            "missing_clauses": "Missing Clauses",
            "dangerous_patterns": "Dangerous Patterns",
            "key_risks": "Key Risks",
            "negotiation_priorities": "Negotiation Priorities",
            "recommended_actions": "Recommended Actions",
            "practical_decision": "Practical Decision",
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
            "contract_score": "Score du contrat",
            "contract_complexity": "Complexité du contrat",
            "overall_balance": "Équilibre du contrat",
            "jurisdiction": "Juridiction",
            "jurisdiction_note": "Note sur la juridiction",
            "missing_clauses": "Clauses manquantes",
            "dangerous_patterns": "Schémas dangereux",
            "key_risks": "Risques clés",
            "negotiation_priorities": "Priorités de négociation",
            "recommended_actions": "Actions recommandées",
            "practical_decision": "Décision pratique",
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
            "contract_score": "درجة العقد",
            "contract_complexity": "تعقيد العقد",
            "overall_balance": "توازن العقد",
            "jurisdiction": "الاختصاص القضائي",
            "jurisdiction_note": "ملاحظة الاختصاص",
            "missing_clauses": "البنود المفقودة",
            "dangerous_patterns": "الأنماط الخطيرة",
            "key_risks": "المخاطر الرئيسية",
            "negotiation_priorities": "أولويات التفاوض",
            "recommended_actions": "الإجراءات الموصى بها",
            "practical_decision": "القرار العملي",
        },
    }

    return labels.get(language, labels["en"])


def translate_complexity(value: str, language: str) -> str:
    mapping = {
        "en": {"low": "Low", "medium": "Medium", "high": "High"},
        "fr": {"low": "Faible", "medium": "Moyenne", "high": "Élevée"},
        "ar": {"low": "منخفض", "medium": "متوسط", "high": "مرتفع"},
    }

    return mapping.get(language, mapping["en"]).get(value, value)


def build_empty_summary(language: str = "en") -> dict:
    ns = get_not_specified(language)

    return normalize_contract_summary(
        {
            "contract_type": ns,
            "parties": [ns],
            "duration": ns,
            "payment_terms": ns,
            "main_obligations": [],
            "global_summary": ns,
            "important_points": [],
            "missing_clauses": [],
            "dangerous_patterns": [],
            "contract_score": 0,
            "overall_balance": ns,
            "negotiation_priorities": [],
            "key_risks": [],
            "practical_decision": ns,
            "jurisdiction_detected": ns,
            "jurisdiction_note": ns,
            "recommended_actions": [],
            "contract_complexity": "medium",
        },
        language,
    )


def generate_summary_data(text: str, language: str = "en") -> dict:
    """
    New structured summary function.

    Returns a clean dict that can later be rendered by the frontend.
    generate_summary() below still returns text for backward compatibility.
    """

    if not text or not text.strip():
        return build_empty_summary(language)

    prompt_template = load_prompt("summary_prompt.txt")
    contract_text = text[:MAX_SUMMARY_CHARS]

    prompt = f"""
{prompt_template}

Output language: {language}

Contract text:
{contract_text}
""".strip()

    try:
        data = call_json_ai(prompt)
    except Exception as e:
        print("SUMMARY AI ERROR:", str(e))
        return build_empty_summary(language)

    jurisdiction_data = extract_jurisdiction(text)

    if jurisdiction_data["governing_law"]:
        data["jurisdiction_detected"] = (
            jurisdiction_data["governing_law"]
        )

        data["jurisdiction_note"] = (
            f"The contract is governed by "
            f"{jurisdiction_data['governing_law']} law."
        )

        missing = data.get("missing_clauses", [])

        filtered = []

        for item in missing:
            item_lower = item.lower()

            if "governing law" in item_lower:
                continue

            if "juridiction" in item_lower:
                continue

            if "القانون" in item_lower:
                continue

            filtered.append(item)

        data["missing_clauses"] = filtered

    if jurisdiction_data["dispute_location"]:
        if not data.get("jurisdiction_note"):
            data["jurisdiction_note"] = ""

        data["jurisdiction_note"] += (
            f" Disputes are resolved in "
            f"{jurisdiction_data['dispute_location']}."
        )

        missing = data.get("missing_clauses", [])

        filtered = []

        for item in missing:
            item_lower = item.lower()

            if "dispute" in item_lower:
                continue

            if "arbitration" in item_lower:
                continue

            if "litige" in item_lower:
                continue

            if "نزاع" in item_lower:
                continue

            filtered.append(item)

        data["missing_clauses"] = filtered

    data = normalize_contract_summary(data, language)

    return data


def render_summary_text(data: dict, language: str = "en") -> str:
    """
    Backward-compatible text renderer.

    Keep this while your frontend still expects a formatted string.
    Later, your frontend should render generate_summary_data() directly.
    """

    t = get_labels(language)

    output = ""
    output += f"{t['type']}: {data['contract_type']}\n"
    output += f"{t['parties']}: {', '.join(data['parties'])}\n"
    output += f"{t['duration']}: {data['duration']}\n"
    output += f"{t['payment']}: {data['payment_terms']}\n\n"

    output += f"{t['summary']}:\n{data['global_summary']}\n\n"
    output += f"{t['contract_score']}: {data['contract_score']}/100\n"
    output += (
        f"{t['contract_complexity']}: "
        f"{translate_complexity(data['contract_complexity'], language)}\n"
    )
    output += f"{t['overall_balance']}: {data['overall_balance']}\n"
    output += f"{t['jurisdiction']}: {data['jurisdiction_detected']}\n"

    if data.get("jurisdiction_note"):
        output += f"{t['jurisdiction_note']}: {data['jurisdiction_note']}\n"

    sections = [
        ("main_obligations", "main_obligations"),
        ("important_points", "key_points"),
        ("missing_clauses", "missing_clauses"),
        ("dangerous_patterns", "dangerous_patterns"),
        ("key_risks", "key_risks"),
        ("negotiation_priorities", "negotiation_priorities"),
        ("recommended_actions", "recommended_actions"),
    ]

    for data_key, label_key in sections:
        items = data.get(data_key, [])
        if items:
            output += f"\n{t[label_key]}:\n"
            output += "\n".join([f"- {item}" for item in items])
            output += "\n"

    if data.get("practical_decision"):
        output += f"\n{t['practical_decision']}:\n"
        output += data["practical_decision"]

    return output.strip()


def generate_summary(text: str, language: str = "en") -> str:
    """
    Backward-compatible function.

    Your current app can keep calling this and receiving a string.
    """

    data = generate_summary_data(text, language)
    return render_summary_text(data, language)


def build_empty_simplified(language: str = "en") -> dict:
    ns = get_not_specified(language)

    return normalize_simplified_contract(
        {
            "simplified_version": ns,
            "key_points": [],
            "things_to_watch": [],
        },
        language,
    )


def generate_simplified_version_data(text: str, language: str = "en") -> dict:
    """
    Structured simplification result.
    """

    if not text or not text.strip():
        return build_empty_simplified(language)

    prompt_template = load_prompt("simplification_prompt.txt")
    contract_text = text[:MAX_SIMPLIFICATION_CHARS]

    prompt = f"""
{prompt_template}

Output language: {language}

Contract text:
{contract_text}
""".strip()

    try:
        data = call_json_ai(prompt)
    except Exception as e:
        print("SIMPLIFICATION AI ERROR:", str(e))
        return build_empty_simplified(language)

    return normalize_simplified_contract(data, language)


def render_simplified_text(data: dict, language: str = "en") -> str:
    t = get_labels(language)

    output = data.get("simplified_version", "")

    if data.get("key_points"):
        output += f"\n\n{t['key_points']}:\n"
        output += "\n".join([f"- {item}" for item in data["key_points"]])

    if data.get("things_to_watch"):
        output += f"\n\n{t['things_to_watch']}:\n"
        output += "\n".join([f"- {item}" for item in data["things_to_watch"]])

    return output.strip()


def generate_simplified_version(text: str, language: str = "en") -> str:
    """
    Backward-compatible function.

    Your current app can keep calling this and receiving a string.
    """

    data = generate_simplified_version_data(text, language)
    return render_simplified_text(data, language)


def calculate_global_risk(analysis_results: list[dict]) -> dict:
    high_count = sum(
        1
        for item in analysis_results
        if item.get("risk_level") == "high"
    )

    medium_count = sum(
        1
        for item in analysis_results
        if item.get("risk_level") == "medium"
    )

    if high_count > 0:
        return {
            "risk_level": "high",
            "risk_score": 80,
        }

    if medium_count > 0:
        return {
            "risk_level": "medium",
            "risk_score": 50,
        }

    return {
        "risk_level": "low",
        "risk_score": 20,
    }
