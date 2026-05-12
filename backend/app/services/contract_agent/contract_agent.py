import json
from typing import Any

from openai import OpenAI

from app.config import OPENAI_API_KEY
from app.services.contract_agent.risk_engine import analyze_risk
from app.services.contract_agent.clause_title_extractor import extract_clause_title
from app.utils.prompt_loader import load_prompt

client = OpenAI(api_key=OPENAI_API_KEY)


ALLOWED_CLAUSE_TYPES = {
    "payment", "termination", "confidentiality", "intellectual_property",
    "liability", "penalty", "exclusivity", "non_compete", "other"
}

ALLOWED_RISK_LEVELS = {"low", "medium", "high"}
ALLOWED_FAVOURS = {
    "employer", "employee", "company", "contractor",
    "vendor", "client", "balanced", "unclear"
}
ALLOWED_CONFIDENCE = {"low", "medium", "high"}
ALLOWED_PRIORITY = {"low", "medium", "high"}


def safe_str(value: Any) -> str:
    if value is None:
        return ""

    if isinstance(value, str):
        return value.strip()

    return str(value).strip()


def safe_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value

    if isinstance(value, str):
        return value.strip().lower() in {
            "true",
            "yes",
            "1",
        }

    return False


def clamp_enum(
    value: Any,
    allowed: set[str],
    default: str,
) -> str:
    value = safe_str(value).lower()

    return value if value in allowed else default


def fallback_clause_result(
    language: str = "en"
) -> dict:

    fallback_text = {
        "en": {
            "parse": "Could not parse AI response.",
            "missing": "Not specified",
            "review": (
                "Review this clause manually because "
                "the automated analysis failed."
            ),
        },

        "fr": {
            "parse": (
                "Impossible d’analyser correctement "
                "la réponse de l’IA."
            ),
            "missing": "Non spécifié",
            "review": (
                "Vérifiez cette clause manuellement "
                "car l’analyse automatique a échoué."
            ),
        },

        "ar": {
            "parse": (
                "تعذر تحليل رد الذكاء الاصطناعي "
                "بشكل صحيح."
            ),
            "missing": "غير محدد",
            "review": (
                "راجع هذا البند يدويًا لأن "
                "التحليل التلقائي فشل."
            ),
        },
    }

    t = fallback_text.get(
        language,
        fallback_text["en"]
    )

    return {
        "clause_title": "",
        "clause_reference": "",
        "quoted_text": "",
        "clause_type": "other",
        "risk_level": "low",
        "explanation_simple": t["parse"],
        "why_it_matters": t["missing"],
        "legal_insight": "",
        "favours": "unclear",
        "market_comparison": "",
        "red_flag": False,
        "red_flag_reason": "",
        "recommendation": t["review"],
        "confidence": "low",
        "safer_alternative": "",
        "negotiation_advice": t["review"],
        "negotiation_priority": "medium",
    }


def normalize_clause_result(
    ai_result: dict
) -> dict:

    return {
        "clause_title": safe_str(
            ai_result.get("clause_title")
        ),

        "clause_reference": safe_str(
            ai_result.get("clause_reference")
        ),

        "quoted_text": safe_str(
            ai_result.get("quoted_text")
        )[:600],

        "clause_type": clamp_enum(
            ai_result.get("clause_type"),
            ALLOWED_CLAUSE_TYPES,
            "other",
        ),

        "risk_level": clamp_enum(
            ai_result.get("risk_level"),
            ALLOWED_RISK_LEVELS,
            "low",
        ),

        "explanation_simple": safe_str(
            ai_result.get("explanation_simple")
        ),

        "why_it_matters": safe_str(
            ai_result.get("why_it_matters")
        ),

        "legal_insight": safe_str(
            ai_result.get("legal_insight")
        ),

        "favours": clamp_enum(
            ai_result.get("favours"),
            ALLOWED_FAVOURS,
            "unclear",
        ),

        "market_comparison": safe_str(
            ai_result.get("market_comparison")
        ),

        "red_flag": safe_bool(
            ai_result.get("red_flag")
        ),

        "red_flag_reason": safe_str(
            ai_result.get("red_flag_reason")
        ),

        "recommendation": safe_str(
            ai_result.get("recommendation")
        ),

        "confidence": clamp_enum(
            ai_result.get("confidence"),
            ALLOWED_CONFIDENCE,
            "low",
        ),

        "safer_alternative": safe_str(
            ai_result.get("safer_alternative")
        ),

        "negotiation_advice": safe_str(
            ai_result.get("negotiation_advice")
        ),

        "negotiation_priority": clamp_enum(
            ai_result.get("negotiation_priority"),
            ALLOWED_PRIORITY,
            "medium",
        ),
    }


def build_clause_prompt(
    clause: str,
    language: str,
) -> str:

    prompt_template = load_prompt(
        "clause_analysis_prompt.txt"
    )

    return f"""
{prompt_template}

Output language: {language}

Analyze this single clause only.

Clause:
{clause}
""".strip()


def call_clause_ai(
    prompt: str
) -> dict:

    response = client.chat.completions.create(
        model="gpt-4o-mini",

        messages=[
            {
                "role": "system",

                "content": (
                    "You are a strict JSON "
                    "contract analysis engine. "
                    "Return only valid JSON "
                    "and never add markdown."
                ),
            },

            {
                "role": "user",
                "content": prompt,
            },
        ],

        temperature=0.1,

        response_format={
            "type": "json_object"
        },
    )

    content = (
        response
        .choices[0]
        .message
        .content
        or "{}"
    )

    return json.loads(content)


def apply_rule_based_risk(
    ai_result: dict,
    clause: str,
    language: str,
) -> dict:

    rule_result = analyze_risk(
        clause,
        language
    )

    rule_level = rule_result.get(
        "risk_level",
        "low"
    )

    if rule_level == "high":

        ai_result["risk_level"] = "high"
        ai_result["negotiation_priority"] = "high"

        if not ai_result.get("red_flag"):
            ai_result["red_flag"] = True

        if not ai_result.get("red_flag_reason"):

            ai_result["red_flag_reason"] = (
                safe_str(
                    rule_result.get("trigger")
                )
            )

    elif (
        rule_level == "medium"
        and ai_result.get("risk_level") == "low"
    ):

        ai_result["risk_level"] = "medium"

        if (
            ai_result.get(
                "negotiation_priority"
            ) == "low"
        ):
            ai_result[
                "negotiation_priority"
            ] = "medium"

    ai_result["trigger"] = rule_result.get(
        "trigger"
    )

    return ai_result


def analyze_clause(
    clause: str,
    language: str = "en",
) -> dict:

    if not clause or not clause.strip():

        return normalize_clause_result(
            fallback_clause_result(language)
        )

    prompt = build_clause_prompt(
        clause,
        language,
    )

    try:
        ai_result = call_clause_ai(prompt)

    except Exception as e:

        print("CLAUSE AI ERROR:", str(e))

        ai_result = fallback_clause_result(
            language
        )

    ai_result = normalize_clause_result(
        ai_result
    )

    if not ai_result["clause_title"]:

        ai_result["clause_title"] = (
            extract_clause_title(clause)
        )

    ai_result = apply_rule_based_risk(
        ai_result,
        clause,
        language,
    )

    return ai_result


def should_force_red_flag_false(
    clause_title: str,
    clause_text: str,
) -> bool:

    text = (
        f"{clause_title} {clause_text}"
    ).lower()

    safe_patterns = [

        # Universal contract intro / boilerplate only
        "effective as of",
        "entered into by and between",
        "desires to enter into",
        "whereas",
        "now therefore",
        "mutual promises",
        "good and valuable consideration",
        "receipt and sufficiency",
        "for reference only",

        # French boilerplate
        "conclu entre",
        "considérant que",
        "en foi de quoi",
        "à titre indicatif",
        "les titres sont fournis",

        # Arabic boilerplate
        "تم إبرام هذا العقد بين",
        "حيث إن",
        "بناء على ما سبق",
        "وعليه",
        "مقابل الوعود المتبادلة",
        "لأغراض مرجعية فقط",
    ]

    return any(
        pattern in text
        for pattern in safe_patterns
    )



def validate_clause_type(
    analysis: dict,
    clause_text: str,
) -> dict:

    text = clause_text.lower()

    clause_type = analysis.get("clause_type")

    explicit_patterns = {

        "non_compete": [
            "non-compete",
            "non compete",
            "shall not compete",
            "may not compete",
            "cannot compete",
            "restriction on competition",
            "restrictive covenant",

            "non-concurrence",
            "clause de non-concurrence",

            "عدم المنافسة",
        ],

        "exclusivity": [
            "exclusive",
            "exclusivity",
            "sole provider",
            "exclusive rights",

            "exclusivité",
            "exclusif",

            "حصري",
            "حصرية",
        ],

        "penalty": [
            "penalty",
            "liquidated damages",
            "fine",

            "pénalité",
            "amende",

            "غرامة",
        ],
    }

    # No validation needed
    if clause_type not in explicit_patterns:
        return analysis

    matched = any(
        pattern in text
        for pattern in explicit_patterns[clause_type]
    )

    # HARD RESET if unsupported
    if not matched:

        analysis["clause_type"] = "other"

        analysis["red_flag"] = False

        analysis["red_flag_reason"] = ""

        analysis["risk_level"] = "low"

        analysis["confidence"] = "low"

        analysis["recommendation"] = ""

        analysis["negotiation_advice"] = ""

        analysis["safer_alternative"] = ""

        analysis["legal_insight"] = (
            "The clause does not explicitly contain "
            "a legally identifiable "
            f"{clause_type.replace('_', ' ')} provision."
        )

    return analysis



def validate_quoted_text(
    analysis: dict,
    clause_text: str,
) -> dict:

    quoted = (
        analysis.get("quoted_text", "")
        .strip()
    )

    if not quoted:
        return analysis

    clause_lower = clause_text.lower()

    quoted_lower = quoted.lower()

    # Quote not actually found in clause
    if quoted_lower not in clause_lower:

        analysis["quoted_text"] = (
            clause_text[:300].strip()
        )

        if analysis.get("confidence") == "high":
            analysis["confidence"] = "medium"

    # Extremely short quotes are unreliable
    if len(quoted.split()) < 6:

        analysis["quoted_text"] = (
            clause_text[:300].strip()
        )

    return analysis



def calibrate_risk_level(
    analysis: dict,
    clause_text: str,
) -> dict:

    text = clause_text.lower()

    clause_type = analysis.get("clause_type")

    red_flag = analysis.get("red_flag")

    # -------------------
    # Low-materiality / informational clauses
    # -------------------

    low_materiality_patterns = [

        # Generic informational terms
        "effective as of",
        "notice address",
        "contact information",
        "headings",
        "table of contents",
        "reference only",
        "entire agreement",

        # Payment/admin
        "invoice number",
        "billing address",
        "payment date",

        # French
        "à titre indicatif",
        "adresse de notification",
        "intégralité de l'accord",

        # Arabic
        "لأغراض مرجعية فقط",
        "عنوان الإشعار",
        "الاتفاق الكامل",
    ]

    informational_types = {
        "other",
    }

    if (
        not red_flag
        and clause_type in informational_types
    ):

        for pattern in low_materiality_patterns:

            if pattern in text:

                analysis["risk_level"] = "low"

                if analysis.get(
                    "negotiation_priority"
                ) == "medium":

                    analysis[
                        "negotiation_priority"
                    ] = "low"

                break

    # -------------------
    # High-risk validation
    # -------------------

    if analysis.get("risk_level") == "high":

        high_risk_patterns = [

            # Liability / indemnity
            "unlimited liability",
            "indemnify",
            "indemnification",
            "waiver of liability",

            # Restrictions
            "non-compete",
            "exclusive",
            "exclusivity",

            # Financial penalties
            "liquidated damages",
            "penalty",
            "fine",

            # IP transfer
            "assign any and all rights",
            "irrevocable",

            # French
            "responsabilité illimitée",
            "non-concurrence",
            "exclusivité",
            "pénalité",
            "cession des droits",

            # Arabic
            "مسؤولية غير محدودة",
            "عدم المنافسة",
            "حصري",
            "غرامة",
            "التنازل عن الحقوق",
        ]

        matched = any(
            pattern in text
            for pattern in high_risk_patterns
        )

        if not matched and not red_flag:

            analysis["risk_level"] = "medium"

    return analysis



def calculate_clause_importance(
    analysis: dict,
    clause_text: str,
) -> int:
    score = 0
    text = clause_text.lower()

    if analysis.get("risk_level") == "high":
        score += 40
    elif analysis.get("risk_level") == "medium":
        score += 20

    if analysis.get("red_flag"):
        score += 30

    important_types = {
        "termination",
        "liability",
        "intellectual_property",
        "payment",
        "confidentiality",
        "non_compete",
        "exclusivity",
        "penalty",
    }

    if analysis.get("clause_type") in important_types:
        score += 25

    high_materiality_patterns = [
        # Money / payment exposure
        "lump sum", "severance", "bonus", "penalty", "liquidated damages",
        "late payment", "unpaid", "refund", "fee", "commission",
        "montant forfaitaire", "indemnité", "pénalité", "retard de paiement",
        "مبلغ مقطوع", "تعويض", "غرامة", "تأخير الدفع",

        # Termination / control
        "termination", "terminate", "change of control", "constructive termination",
        "résiliation", "mettre fin", "changement de contrôle",
        "إنهاء", "فسخ", "تغيير السيطرة",

        # Liability / indemnity
        "liability", "indemnify", "indemnification", "damages", "irreparable injury",
        "responsabilité", "indemniser", "dommages",
        "مسؤولية", "تعويض", "أضرار",

        # IP / ownership
        "intellectual property", "assign any and all rights", "ownership",
        "propriété intellectuelle", "cession des droits", "titularité",
        "الملكية الفكرية", "التنازل عن الحقوق", "ملكية",

        # Confidentiality / restrictions
        "confidential information", "trade secrets", "non-compete", "exclusive",
        "informations confidentielles", "secret commercial", "non-concurrence", "exclusivité",
        "معلومات سرية", "أسرار تجارية", "عدم المنافسة", "حصري",

        # Dispute / jurisdiction
        "arbitration", "court", "governing law", "jurisdiction",
        "arbitrage", "tribunal", "droit applicable", "juridiction",
        "تحكيم", "محكمة", "القانون الواجب التطبيق", "الاختصاص",

        # Assignment / unilateral control
        "assign this agreement", "unilateral", "sole discretion", "automatic renewal",
        "cession du contrat", "unilatéral", "seule discrétion", "renouvellement automatique",
        "التنازل عن العقد", "منفرد", "تقديره المطلق", "التجديد التلقائي",
    ]

    for pattern in high_materiality_patterns:
        if pattern in text:
            score += 40

    boilerplate_patterns = [
        # English
        "whereas",
        "now therefore",
        "good and valuable consideration",
        "receipt and sufficiency",
        "for reference only",
        "desires to enter into",
        "desires to employ",
        "accept such employment",

        # French
        "considérant que",
        "en foi de quoi",
        "à titre indicatif",
        "les titres sont fournis",

        # Arabic
        "حيث إن",
        "بناء على ما سبق",
        "وعليه",
        "لأغراض مرجعية فقط",
    ]

    for pattern in boilerplate_patterns:
        if pattern in text:
            score -= 30

    return score



def analyze_contract_clauses(
    clauses: list[str],
    language: str = "en",
    max_clauses: int = 25,
) -> list[dict]:

    results = []

    for clause in clauses[:max_clauses]:

        analysis = analyze_clause(
            clause,
            language,
        )

        analysis = validate_clause_type(
            analysis,
            clause,
        )

        analysis = validate_quoted_text(
            analysis,
            clause,
        )

        analysis = calibrate_risk_level(
            analysis,
            clause,
        )

        if should_force_red_flag_false(
            analysis.get(
                "clause_title",
                "",
            ),
            clause,
        ):

            analysis["red_flag"] = False
            analysis["red_flag_reason"] = ""

        title = (
            analysis.get("clause_title")
            or extract_clause_title(clause)
        )

        analysis["importance_score"] = (
            calculate_clause_importance(
                analysis,
                clause,
            )
        )

        if (
            analysis.get("risk_level") == "medium"
            and not analysis.get("red_flag")
            and analysis.get("clause_type") == "other"
            and analysis.get("importance_score", 0) < 50
        ):
            analysis["risk_level"] = "low"
            analysis["negotiation_priority"] = "low"

        if analysis.get("importance_score", 0) < 10:
            continue

        results.append({
            "title": title,
            "original_text": clause[:1000],
            **analysis,
        })

    results = sorted(
        results,
        key=lambda x: x.get(
            "importance_score",
            0,
        ),
        reverse=True,
    )

    return results[:12]
