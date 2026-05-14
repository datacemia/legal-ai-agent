import re

from app.utils.prompt_loader import load_prompt
from app.services.contract_agent.ai_client import call_json_ai
from app.services.contract_agent.summary_normalizer import (
    get_not_specified,
    normalize_contract_summary,
    normalize_simplified_contract,
)
from app.services.contract_agent.validator import (
    validate_contract_result,
)


MAX_SUMMARY_CHARS = 12_000
MAX_SIMPLIFICATION_CHARS = 12_000

SUMMARY_SPECULATIVE_PATTERNS = [
    "risques significatifs",
    "significant risks",
    "major legal exposure",
    "dangerous contract",
    "highly risky",
    "serious legal risk",
    "critical legal concern",
]


def extract_jurisdiction(text: str) -> dict:
    text_lower = text.lower()

    governing_law_patterns = [
        r"laws of the state of ([a-zA-Z\s]{2,40})(?:\.|,|;|\n)",
        r"governed by the laws of ([a-zA-Z\s]{2,40})(?:\.|,|;|\n)",
        r"governed under the laws of ([a-zA-Z\s]{2,40})(?:\.|,|;|\n)",
        r"laws of ([a-zA-Z\s]{2,40})(?:\.|,|;|\n)",
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

            if len(governing_law.split()) > 6:
                governing_law = None
                continue

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


def build_jurisdiction_note(
    governing_law,
    dispute_location,
    language,
):
    parts = []

    if governing_law:
        if language == "fr":
            parts.append(
                f"Le contrat est régi par le droit de {governing_law}."
            )
        elif language == "ar":
            parts.append(
                f"يخضع العقد لقوانين {governing_law}."
            )
        else:
            parts.append(
                f"The contract is governed by {governing_law} law."
            )

    if dispute_location:
        if language == "fr":
            parts.append(
                f"Les litiges sont résolus à {dispute_location}."
            )
        elif language == "ar":
            parts.append(
                f"يتم حل النزاعات في {dispute_location}."
            )
        else:
            parts.append(
                f"Disputes are resolved in {dispute_location}."
            )

    return " ".join(parts)


def detect_balancing_protections(
    clauses: list[str],
) -> dict:

    text = "\n".join(clauses).lower()

    protections = {
        "arbitration": False,
        "cure_period": False,
        "severance": False,
        "insurance": False,
        "limitation_scope": False,
    }

    arbitration_patterns = [
        "arbitration",
        "arbitrage",
        "تحكيم",
    ]

    cure_patterns = [
        "cure within",
        "period to cure",
        "diligently pursue a cure",

        "délai de correction",

        "مهلة لتصحيح",
    ]

    severance_patterns = [
        "lump sum",
        "severance",
        "salary continuation",

        "indemnité",

        "تعويض",
    ]

    insurance_patterns = [
        "liability insurance",
        "insured",

        "assurance responsabilité",

        "تأمين",
    ]

    limitation_patterns = [
        "except as provided",
        "notwithstanding",
        "does not include",

        "sauf",
        "ne comprend pas",

        "لا يشمل",
    ]

    for p in arbitration_patterns:
        if p in text:
            protections["arbitration"] = True

    for p in cure_patterns:
        if p in text:
            protections["cure_period"] = True

    for p in severance_patterns:
        if p in text:
            protections["severance"] = True

    for p in insurance_patterns:
        if p in text:
            protections["insurance"] = True

    for p in limitation_patterns:
        if p in text:
            protections["limitation_scope"] = True

    return protections



def apply_balancing_protections(
    summary_data: dict,
    protections: dict,
) -> dict:

    # -------------------
    # Termination balancing
    # -------------------

    if (
        protections.get("cure_period")
        or protections.get("arbitration")
        or protections.get("severance")
    ):

        risk_filters = [
            "sudden termination",
            "unilateral termination",
            "unexpected job loss",
            "without clear recourse",
            "vague termination",
        ]

        for field in [
            "key_risks",
            "dangerous_patterns",
            "things_to_watch",
        ]:

            items = summary_data.get(field, [])

            summary_data[field] = [
                item for item in items
                if not any(
                    rf in item.lower()
                    for rf in risk_filters
                )
            ]

    # -------------------
    # Liability balancing
    # -------------------

    if (
        protections.get("insurance")
    ):

        liability_filters = [
            "financial exposure",
            "lack of protection",
            "personal liability",
        ]

        for field in [
            "key_risks",
            "dangerous_patterns",
        ]:

            items = summary_data.get(field, [])

            summary_data[field] = [
                item for item in items
                if not any(
                    rf in item.lower()
                    for rf in liability_filters
                )
            ]

    return summary_data



def remove_protective_constructive_termination_danger(
    data: dict,
    full_text: str,
) -> dict:

    text = full_text.lower()

    protective_termination_terms = [
        "constructive termination",
        "lump sum",
        "fully vested",
        "compensation",
        "indemnité",
        "تعويض",
    ]

    if (
        "constructive termination" in text
        and any(
            term in text
            for term in protective_termination_terms
        )
    ):

        data["dangerous_patterns"] = [
            item
            for item in data.get("dangerous_patterns", [])
            if "constructive termination" not in item.lower()
        ]

    return data


def remove_balanced_termination_dangers(
    data: dict,
    full_text: str,
) -> dict:

    text = full_text.lower()

    termination_balance_terms = [
        "cure within",
        "notice",
        "arbitrator",
        "arbitration",
        "compensation",
        "not justified",

        "délai",
        "avis",
        "arbitrage",
        "indemnité",

        "إشعار",
        "تحكيم",
        "تعويض",
    ]

    if any(
        term in text
        for term in termination_balance_terms
    ):

        data["dangerous_patterns"] = [
            item
            for item in data.get("dangerous_patterns", [])
            if "termination" not in item.lower()
        ]

        data["key_risks"] = [
            item
            for item in data.get("key_risks", [])
            if "termination" not in item.lower()
        ]

    return data


def remove_false_missing_payment_deadline(
    data: dict,
    full_text: str,
) -> dict:

    text = full_text.lower()

    payment_mechanism_terms = [
        "salary",
        "bonus",
        "reimburse",
        "payment",
        "compensation",
        "paid",
        "invoice",

        "salaire",
        "paiement",
        "remboursement",
        "compensation",

        "راتب",
        "دفع",
        "تعويض",
        "سداد",
    ]

    if any(
        term in text
        for term in payment_mechanism_terms
    ):

        data["missing_clauses"] = [
            clause
            for clause in data.get("missing_clauses", [])
            if "payment deadline" not in clause.lower()
        ]

    return data


def remove_jurisdiction_false_actions(data: dict) -> dict:
    remove_terms = [
        "governing law",
        "jurisdiction",
        "dispute resolution",
        "arbitration",
        "droit applicable",
        "juridiction",
        "résolution des litiges",
        "arbitrage",
        "القانون الواجب التطبيق",
        "الاختصاص",
        "حل النزاعات",
        "التحكيم",
    ]

    for key in [
        "recommended_actions",
        "negotiation_priorities",
        "missing_clauses",
        "key_risks",
        "dangerous_patterns",
    ]:
        items = data.get(key, [])

        data[key] = [
            item for item in items
            if not any(
                term in item.lower()
                for term in remove_terms
            )
        ]

    return data



def remove_alarmist_language(
    data: dict,
    contract_quality_score: int,
) -> dict:

    if contract_quality_score >= 60:
        return data

    fields = [
        "global_summary",
        "practical_decision",
        "overall_balance",
    ]

    for field in fields:

        value = data.get(field, "")

        lowered = value.lower()

        for pattern in SUMMARY_SPECULATIVE_PATTERNS:

            if pattern in lowered:

                value = value.replace(
                    pattern,
                    ""
                )

        data[field] = " ".join(
            value.split()
        )

    return data



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
            "contract_quality_score": "Contract Quality",
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
            "contract_quality_score": "Qualité du contrat",
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
            "contract_quality_score": "جودة العقد",
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
            "contract_quality_score": 0,
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

CRITICAL:
Translate every generated JSON value into this output language.
The contract source language may be different.
Do not copy source-language sentences into generated fields.
Only keep company names, person names, dates, amounts, article references, and court names unchanged.

Contract text:
{contract_text}
""".strip()

    try:
        data = call_json_ai(prompt)
    except Exception as e:
        print("SUMMARY AI ERROR:", str(e))
        return build_empty_summary(language)

    protections = detect_balancing_protections(
        [text]
    )

    data = apply_balancing_protections(
        data,
        protections,
    )

    jurisdiction_data = extract_jurisdiction(text)

    if jurisdiction_data["governing_law"]:
        data["jurisdiction_detected"] = (
            jurisdiction_data["governing_law"]
        )

        data["jurisdiction_note"] = build_jurisdiction_note(
            jurisdiction_data.get("governing_law"),
            jurisdiction_data.get("dispute_location"),
            language,
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
        data["jurisdiction_note"] = build_jurisdiction_note(
            jurisdiction_data.get("governing_law"),
            jurisdiction_data.get("dispute_location"),
            language,
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

    if (
        jurisdiction_data.get("governing_law")
        or jurisdiction_data.get("dispute_location")
    ):
        data = remove_jurisdiction_false_actions(data)

    data = remove_protective_constructive_termination_danger(
        data,
        text,
    )

    data = remove_balanced_termination_dangers(
        data,
        text,
    )

    data = remove_false_missing_payment_deadline(
        data,
        text,
    )

    data = normalize_contract_summary(data, language)

    if (
        "contract_quality_score" not in data
        and "contract_score" in data
    ):
        data["contract_quality_score"] = data.pop(
            "contract_score"
        )

    data = remove_alarmist_language(
        data,
        data.get("contract_quality_score", 0),
    )

    quality_check = validate_contract_result(data)

    data["quality_check"] = quality_check

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
    output += f"{t['contract_quality_score']}: {data['contract_quality_score']}/100\n"
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

CRITICAL:
Translate every generated JSON value into this output language.
The contract source language may be different.
Do not copy source-language sentences into generated fields.
Only keep company names, person names, dates, amounts, article references, and court names unchanged.

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

    # key_points intentionally hidden in simplified rendering.

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
