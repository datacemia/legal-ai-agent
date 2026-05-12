import json
from openai import OpenAI

from app.config import OPENAI_API_KEY
from app.utils.prompt_loader import load_prompt

client = OpenAI(api_key=OPENAI_API_KEY)


def get_not_specified(language: str) -> str:
    if language == "fr":
        return "Non spécifié"

    if language == "ar":
        return "غير محدد"

    return "Not specified"


def normalize_missing_value(value: str, language: str) -> str:
    missing_values = [
        "Not specified",
        "غير محدد",
        "Non spécifié",
        "undefined",
        "unknown",
    ]

    if not value or str(value).strip() in missing_values:
        if language == "fr":
            return "Non spécifié"

        if language == "ar":
            return "غير محدد"

        return "Not specified"

    return value



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
            "not_specified": "Not specified",
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
            "not_specified": "Non spécifié",
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
            "not_specified": "غير محدد",
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

        try:
            data = json.loads(content)

        except Exception:
            not_specified = get_not_specified(language)

            data = {
                "contract_type": not_specified,
                "parties": [not_specified],
                "duration": not_specified,
                "payment_terms": not_specified,
                "main_obligations": [not_specified],
                "global_summary": not_specified,
                "important_points": [not_specified],
                "missing_clauses": [],
                "dangerous_patterns": [],
                "contract_score": 0,
                "overall_balance": not_specified,
                "negotiation_priorities": [],
                "key_risks": [],
                "practical_decision": not_specified,
                "jurisdiction_detected": not_specified,
                "jurisdiction_note": not_specified,
                "recommended_actions": [],
                "contract_complexity": (
                    "منخفض"
                    if language == "ar"
                    else "Faible"
                    if language == "fr"
                    else "Low"
                ),
            }

        if language == "ar":
            for key in [
                "global_summary",
                "practical_decision",
            ]:
                value = data.get(key)

                if isinstance(value, str):
                    if "Not specified" in value:
                        data[key] = "غير محدد"

        summary = data.get("global_summary", "")
        contract_type = data.get(
            "contract_type",
            get_not_specified(language)
        )
        parties = data.get(
            "parties",
            [get_not_specified(language)]
        )
        duration = data.get(
            "duration",
            get_not_specified(language)
        )
        payment_terms = data.get(
            "payment_terms",
            get_not_specified(language)
        )
        main_obligations = data.get("main_obligations", [])

        important_points = data.get("important_points", [])

        missing_clauses = data.get("missing_clauses", [])

        dangerous_patterns = data.get("dangerous_patterns", [])

        contract_score = data.get("contract_score", 0)

        overall_balance = data.get("overall_balance", "")

        negotiation_priorities = data.get(
            "negotiation_priorities",
            []
        )

        key_risks = data.get("key_risks", [])

        practical_decision = data.get(
            "practical_decision",
            ""
        )

        jurisdiction_detected = data.get(
            "jurisdiction_detected",
            get_not_specified(language)
        )

        jurisdiction_note = data.get(
            "jurisdiction_note",
            ""
        )

        recommended_actions = data.get(
            "recommended_actions",
            []
        )

        contract_complexity = data.get(
            "contract_complexity",
            "medium"
        )

        complexity_map = {
            "en": {
                "low": "Low",
                "medium": "Medium",
                "high": "High",
            },
            "fr": {
                "low": "Faible",
                "medium": "Moyenne",
                "high": "Élevée",
            },
            "ar": {
                "low": "منخفض",
                "medium": "متوسط",
                "high": "مرتفع",
            }
        }

        contract_complexity = complexity_map.get(
            language,
            complexity_map["en"]
        ).get(contract_complexity, contract_complexity)

        # 🔥 FIX: translate missing values
        if not contract_type or str(contract_type).lower() == "not specified":
            contract_type = get_not_specified(language)

        if (
            not parties
            or not isinstance(parties, list)
            or all(str(p).lower() == "not specified" for p in parties)
        ):
            parties = [get_not_specified(language)]

        if not duration or str(duration).lower() == "not specified":
            duration = get_not_specified(language)

        if not payment_terms or str(payment_terms).lower() == "not specified":
            payment_terms = get_not_specified(language)

        if (
            not jurisdiction_detected
            or str(jurisdiction_detected).lower() == "not specified"
        ):
            jurisdiction_detected = get_not_specified(language)

        contract_type = normalize_missing_value(
            contract_type,
            language
        )

        duration = normalize_missing_value(
            duration,
            language
        )

        payment_terms = normalize_missing_value(
            payment_terms,
            language
        )

        overall_balance = normalize_missing_value(
            overall_balance,
            language
        )

        jurisdiction_detected = normalize_missing_value(
            jurisdiction_detected,
            language
        )

        jurisdiction_note = normalize_missing_value(
            jurisdiction_note,
            language
        )

        output = f"{t['type']}: {contract_type}\n"
        output += f"{t['parties']}: {', '.join(parties)}\n"
        output += f"{t['duration']}: {duration}\n"
        output += f"{t['payment']}: {payment_terms}\n\n"

        output += f"{t['summary']}:\n{summary}\n\n"
        output += f"{t['contract_score']}: {contract_score}/100\n"

        output += f"{t['contract_complexity']}: {contract_complexity}\n"

        output += f"{t['overall_balance']}: {overall_balance}\n"

        output += f"{t['jurisdiction']}: {jurisdiction_detected}\n"

        if jurisdiction_note:
            output += f"{t['jurisdiction_note']}: {jurisdiction_note}\n"

        output += "\n"

        if main_obligations:
            output += f"{t['main_obligations']}:\n"
            output += "\n".join([f"- {item}" for item in main_obligations])

        if important_points:
            output += f"\n\n{t['key_points']}:\n"
            output += "\n".join(
                [f"- {item}" for item in important_points]
            )

        if missing_clauses:
            output += f"\n\n{t['missing_clauses']}:\n"
            output += "\n".join(
                [f"- {item}" for item in missing_clauses]
            )

        if dangerous_patterns:
            output += f"\n\n{t['dangerous_patterns']}:\n"
            output += "\n".join(
                [f"- {item}" for item in dangerous_patterns]
            )

        if key_risks:
            output += f"\n\n{t['key_risks']}:\n"
            output += "\n".join(
                [f"- {item}" for item in key_risks]
            )

        if negotiation_priorities:
            output += f"\n\n{t['negotiation_priorities']}:\n"
            output += "\n".join(
                [f"- {item}" for item in negotiation_priorities]
            )

        if recommended_actions:
            output += f"\n\n{t['recommended_actions']}:\n"
            output += "\n".join(
                [f"- {item}" for item in recommended_actions]
            )

        if practical_decision:
            output += (
                f"\n\n{t['practical_decision']}:\n"
                f"{practical_decision}"
            )

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