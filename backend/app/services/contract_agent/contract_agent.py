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


LOW_RISK_CLAUSES = [
    "governing_law",
    "venue",
    "payment_schedule",
    "standard_confidentiality",
    "fixed_term",
    "ip_after_payment",
    "mutual_termination_notice",
]

MEDIUM_RISK_CLAUSES = [
    "limited_liability",
    "broad_confidentiality",
    "vague_payment_trigger",
    "asymmetrical_termination",
]

HIGH_RISK_CLAUSES = [
    "unlimited_liability",
    "unilateral_amendment",
    "automatic_renewal_trap",
    "perpetual_non_compete",
    "broad_ip_assignment",
    "severe_penalties",
]

RISK_ESCALATORS = [
    "unilateral",
    "perpetual",
    "unlimited",
    "without notice",
    "without remedy",
    "sole discretion",
    "irreversible",

    "unilatéral",
    "perpétuel",
    "illimité",
    "sans préavis",
    "sans recours",
    "seule discrétion",
    "irréversible",

    "منفرد",
    "دائم",
    "غير محدود",
    "دون إشعار",
    "دون تعويض",
]

RISK_REDUCERS = [
    "notice period",
    "mutual termination",
    "cure period",
    "arbitration",
    "insurance",
    "liability cap",
    "compensation remedy",

    "préavis",
    "résiliation mutuelle",
    "délai de correction",
    "arbitrage",
    "assurance",
    "plafond de responsabilité",
    "indemnisation",

    "إشعار",
    "إنهاء متبادل",
    "مهلة تصحيح",
    "تحكيم",
    "تأمين",
    "حد المسؤولية",
    "تعويض",
]


SPECULATIVE_PATTERNS = [
    "may not fully protect",
    "could lead to",
    "might create",
    "future employment opportunities",
    "wide range of potential liabilities",
    "salary adjustments",
    "market changes",
    "not cover all potential liabilities",
    "abrupt contract end",
    "automatic renewal",
    "additional protections",
    "more comprehensive",
    "broader coverage",
    "more types of claims",
    "additional liability",
    "higher coverage",
    "salary review",
    "salary reviews",
    "performance bonus",
    "performance bonuses",
    "minimum production threshold",
    "additional flexibility",
    "more flexibility",
    "enhance compensation",
    "competitive compensation",
    "competitive salary",
    "retain talent",
    "better financial outcomes",
    "more favorable terms",
    "tiered bonus",
    "review policy details",
    "align with company goals",
    "industry standards",
    "attract and retain",
    "comprehensive coverage",
    "comprehensive protection",
    "future acquisitions",
    "market conditions",
    "potential gaps",
    "business needs",
    "more favorable payment terms",
    "more favorable termination conditions",
    "effective decision-making",
    "limit future opportunities",
    "future opportunities",
    "higher maximum bonus",
    "extending the eligibility period",
    "longer-term performance metrics",
    "unexpected early termination",
    "without significant cause",
    "without much recourse",
    "higher guaranteed bonus",
    "capping the financial obligations",
    "tiered payment structure",
    "aggregate coverage limits",
    "cash flow impacts",
    "more flexible termination options",
    "potential lock-in",
    "realistic and achievable",
    "financial penalties",
    "increased risk for the employer",
    "higher premiums",
    "stricter terms",
    "above average for many industries",
    "performance metrics",
    "additional coverage",
    "scope of what is covered",
    "financial obligations for the company",
    "renewal options",
    "flexibility in termination",
    "changing circumstances",
    "longer production window",
    "maximize potential earnings",
    "broader timeframe",
    "specific risks associated",
    "market rates",
    "cash flow stability",
    "financial interests",
    "more favorable termination rights",
    "adequate coverage limits",
    "various potential claims",
    "specific coverage amounts",
    "higher bonus cap",
    "company growth",
    "enhance protection",
    "types of claims included",
    "robust in many industries",
    "financial exposure",
    "adequate coverage",
    "more favorable payout",
    "higher aggregate limit",
    "competitive for executive roles",
    "operational stability",
    "potential misuse",
    "enhance coverage",
    "claims that could exceed",
    "lower limits",
    "financial safety net",
    "full protection",
    "stable financial expectation",
    "fair compensation",
    "excessive financial risk",
    "potential liabilities faced",
    "other potential liabilities",
    "additional types of coverage",
    "remove the cap",
    "enhance motivation",
    "capping the financial obligation",
    "cash flow risks",
    "impacts the employer's financial obligations",
    "lower minimum coverage",
    "financial burden on the employee",
    "employee's compensation package",
    "above average for standard employment agreements",
    "tiered coverage structure",
    "sudden job loss",
    "financial stability",
    "renewal automatique",
    "renouvellement automatique",
    "pénalités de retard",
    "late payment penalties",
    "pénalités pour retard de paiement",
    "mesures de sécurité appropriées",
    "préavis plus long",
    "droit français est le plus favorable",
    "transfert de propriété immédiat",
    "droits de rétention",
    "relation contractuelle est critique",
    "ne répondent pas aux attentes",
    "trouver un remplaçant",
]


GENERIC_NEGOTIATION_PATTERNS = [
    "consider negotiating",
    "ensure that",
    "review the policy",
    "more favorable",
    "better protection",
]


GENERIC_AI_PATTERNS = [
    "ensure clarity",
    "ensure comprehensive",
    "consider negotiating",
    "evaluate the implications",
    "to avoid ambiguity",
    "to avoid disputes",
    "ensure adequate",
    "highlight the importance",
    "protect financial interests",
    "enhance protection",
    "justify a higher",
    "seek to enhance",
    "appears competitive",
    "generally favorable",
    "avoid ambiguity",
    "focus on defining",
    "to ensure fair",
    "to avoid excessive",
    "providing a stable",
    "to ensure full",
]


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

    ai_result = remove_speculative_analysis(
        ai_result
    )

    return ai_result


def remove_speculative_analysis(
    analysis: dict,
) -> dict:

    fields = [
        "legal_insight",
        "recommendation",
        "negotiation_advice",
        "market_comparison",
        "safer_alternative",
    ]

    for field in fields:

        value = analysis.get(field, "")

        lowered = value.lower()

        if any(
            p in lowered
            for p in GENERIC_NEGOTIATION_PATTERNS
        ):

            if analysis.get("risk_level") == "low":

                analysis[field] = ""

                continue

        if any(
            p in lowered
            for p in GENERIC_AI_PATTERNS
        ):

            if analysis.get("risk_level") == "low":

                analysis[field] = ""

                continue

        for pattern in SPECULATIVE_PATTERNS:

            if pattern.lower() in lowered:

                analysis[field] = ""

                break

    return analysis


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



def validate_protective_clause(
    analysis: dict,
    clause_text: str,
) -> dict:

    text = clause_text.lower()

    protective_patterns = [
        "will maintain insurance",
        "liability insurance",
        "named insured",
        "coverage",
        "shall indemnify",
        "indemnification",

        "assurance responsabilité",
        "assuré",
        "indemniser",

        "تأمين",
        "تعويض",
    ]

    if any(p in text for p in protective_patterns):

        if analysis.get("red_flag"):
            analysis["red_flag"] = False
            analysis["red_flag_reason"] = ""

        protective_negative_patterns = [
            "financial strain",
            "claims exceed",
            "claims exceeding",
            "exceeding the coverage limit",
            "coverage limit",
            "leaving the employee exposed",
            "employee exposed",
            "financial exposure",
            "personally exposed",
            "personal liability",
        ]

        legal_insight = analysis.get(
            "legal_insight",
            ""
        )

        for pattern in protective_negative_patterns:

            if pattern in legal_insight.lower():

                analysis["legal_insight"] = ""

                break

    return analysis



def validate_standard_market_protection(
    analysis: dict,
    clause_text: str,
) -> dict:

    text = clause_text.lower()

    standard_protection_patterns = [
        "liability insurance",
        "indemnify",
        "expense reimbursement",
        "paid vacation",
        "benefit plans",
        "health insurance",

        "assurance",
        "indemnisation",
        "remboursement",

        "تأمين",
        "تعويض",
        "سداد المصاريف",
    ]

    if any(p in text for p in standard_protection_patterns):

        if analysis.get("risk_level") == "medium":
            analysis["risk_level"] = "low"

        analysis["negotiation_priority"] = "low"

    return analysis


def validate_explicit_permission_clause(
    analysis: dict,
    clause_text: str,
) -> dict:

    text = clause_text.lower()

    permission_patterns = [
        "permitted",
        "allowed",
        "authorized",
        "will not be deemed",
        "will not be considered",
        "so long as",
        "provided that",
        "will continue to be engaged",
        "engaged in other business activities",
        "other business activities",

        "autorisé",
        "permis",
        "ne sera pas considéré",
        "à condition que",

        "مسموح",
        "مرخص",
        "لا يعتبر",
        "بشرط أن",
    ]

    if any(p in text for p in permission_patterns):

        analysis["red_flag"] = False
        analysis["red_flag_reason"] = ""
        analysis["risk_level"] = "low"
        analysis["negotiation_priority"] = "low"
        analysis["legal_insight"] = ""

        permission_negative_patterns = [
            "divided attention",
            "loyalty",
            "outside business",
        ]

        legal_insight = analysis.get(
            "legal_insight",
            ""
        )

        for pattern in permission_negative_patterns:

            if pattern in legal_insight.lower():

                analysis["legal_insight"] = ""

                break

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



def detect_clause_baseline(
    analysis: dict,
    clause_text: str,
) -> str:

    text = clause_text.lower()

    low_patterns = {
        "governing_law": [
            "governing law",
            "droit français",
            "droit applicable",
            "القانون الواجب التطبيق",
        ],
        "venue": [
            "venue",
            "jurisdiction",
            "tribunaux compétents",
            "tribunaux compétents de paris",
            "juridiction",
            "محكمة",
            "الاختصاص",
        ],
        "payment_schedule": [
            "payment schedule",
            "payment date",
            "invoice",
            "échéancier de paiement",
            "date de paiement",
            "facture",
            "جدول الدفع",
            "فاتورة",
        ],
        "standard_confidentiality": [
            "confidentiality",
            "confidential information",
            "confidentialité",
            "information confidentielle",
            "سرية",
            "معلومات سرية",
        ],
        "fixed_term": [
            "term of this agreement",
            "fixed term",
            "durée du contrat",
            "durée déterminée",
            "مدة العقد",
        ],
        "ip_after_payment": [
            "transfer of ownership upon full payment",
            "ownership transfers after full payment",
            "assignment after payment",
            "cession après paiement",
            "transfert de propriété après paiement",
            "الملكية بعد السداد",
        ],
        "mutual_termination_notice": [
            "mutual termination",
            "either party may terminate",
            "notice period",
            "préavis",
            "résiliation mutuelle",
            "إنهاء متبادل",
        ],
    }

    medium_patterns = {
        "limited_liability": [
            "limitation of liability",
            "liability cap",
            "responsabilité limitée",
            "plafond de responsabilité",
            "حد المسؤولية",
        ],
        "broad_confidentiality": [
            "all confidential information",
            "toute information confidentielle",
            "جميع المعلومات السرية",
        ],
        "vague_payment_trigger": [
            "subject to approval",
            "at discretion",
            "déclenchement du paiement",
            "à sa discrétion",
            "حسب تقديره",
        ],
        "asymmetrical_termination": [
            "company may terminate",
            "client may terminate",
            "la société peut résilier",
            "le client peut résilier",
            "يجوز للشركة إنهاء",
        ],
    }

    high_patterns = {
        "unlimited_liability": [
            "unlimited liability",
            "responsabilité illimitée",
            "مسؤولية غير محدودة",
        ],
        "unilateral_amendment": [
            "may amend at any time",
            "unilaterally amend",
            "modifier unilatéralement",
            "تعديل من جانب واحد",
        ],
        "automatic_renewal_trap": [
            "automatic renewal unless",
            "renouvellement automatique sauf",
            "تجديد تلقائي ما لم",
        ],
        "perpetual_non_compete": [
            "perpetual non-compete",
            "non-compete forever",
            "non-concurrence perpétuelle",
            "عدم منافسة دائم",
        ],
        "broad_ip_assignment": [
            "assign any and all rights",
            "all intellectual property",
            "cession de tous les droits",
            "التنازل عن جميع الحقوق",
        ],
        "severe_penalties": [
            "liquidated damages",
            "severe penalty",
            "pénalité sévère",
            "dommages-intérêts forfaitaires",
            "تعويضات مقطوعة",
        ],
    }

    for label, patterns in high_patterns.items():
        if any(p in text for p in patterns):
            return label

    for label, patterns in medium_patterns.items():
        if any(p in text for p in patterns):
            return label

    for label, patterns in low_patterns.items():
        if any(p in text for p in patterns):
            return label

    clause_type = analysis.get("clause_type", "other")

    if clause_type == "penalty":
        return "severe_penalties"

    if clause_type == "non_compete":
        return "perpetual_non_compete" if "perpetual" in text else "asymmetrical_termination"

    if clause_type == "intellectual_property":

        broad_ip_patterns = [
            "assign any and all rights",
            "all intellectual property",
            "irrevocable",
            "perpetual",
            "cession de tous les droits",
            "irrévocable",
            "perpétuel",
            "التنازل عن جميع الحقوق",
            "غير قابل للإلغاء",
            "دائم",
        ]

        if any(
            pattern in text
            for pattern in broad_ip_patterns
        ):
            return "broad_ip_assignment"

        return "ip_after_payment"

    if clause_type == "liability":
        return "limited_liability"

    if clause_type == "confidentiality":
        return "standard_confidentiality"

    if clause_type == "payment":
        return "payment_schedule"

    if clause_type == "termination":
        return "mutual_termination_notice"

    return "other"


def apply_conceptual_risk_calibration(
    analysis: dict,
    clause_text: str,
) -> dict:

    text = clause_text.lower()

    baseline = detect_clause_baseline(
        analysis,
        clause_text,
    )

    has_escalator = any(
        pattern in text
        for pattern in RISK_ESCALATORS
    )

    has_reducer = any(
        pattern in text
        for pattern in RISK_REDUCERS
    )

    analysis["risk_baseline"] = baseline
    analysis["risk_escalated"] = has_escalator
    analysis["risk_reduced"] = has_reducer

    if baseline in LOW_RISK_CLAUSES:

        if not has_escalator:

            analysis["red_flag"] = False
            analysis["red_flag_reason"] = ""

            if analysis.get("risk_level") in {"high", "medium"}:
                analysis["risk_level"] = "low"

            analysis["negotiation_priority"] = "low"

        elif analysis.get("risk_level") == "high":

            analysis["risk_level"] = "medium"

            if analysis.get("negotiation_priority") == "high":
                analysis["negotiation_priority"] = "medium"

    elif baseline in MEDIUM_RISK_CLAUSES:

        if has_reducer and not has_escalator:

            if analysis.get("risk_level") == "high":
                analysis["risk_level"] = "medium"

            analysis["red_flag"] = False
            analysis["red_flag_reason"] = ""

        elif not has_escalator and analysis.get("risk_level") == "high":

            analysis["risk_level"] = "medium"

    elif baseline in HIGH_RISK_CLAUSES:

        if has_reducer and not has_escalator:

            if analysis.get("risk_level") == "high":
                analysis["risk_level"] = "medium"

        else:

            if analysis.get("risk_level") == "low":
                analysis["risk_level"] = "medium"

    if has_reducer and analysis.get("risk_level") == "high":

        analysis["risk_level"] = "medium"

        if analysis.get("negotiation_priority") == "high":
            analysis["negotiation_priority"] = "medium"

    return analysis


def normalize_importance_score(
    results: list[dict],
) -> int:

    risk_weights = {
        "low": 0,
        "medium": 8,
        "high": 20,
    }

    materiality_weights = {
        "low": 8,
        "medium": 16,
        "high": 24,
    }

    if not results:
        return 0

    total_risk_points = 0
    total_materiality_points = 0

    for item in results:

        risk_level = item.get("risk_level", "low")
        materiality_level = item.get(
            "materiality_level",
            "medium",
        )

        total_risk_points += risk_weights.get(
            risk_level,
            0,
        )

        total_materiality_points += materiality_weights.get(
            materiality_level,
            16,
        )

    if total_materiality_points <= 0:
        return 0

    return round(
        min(
            100,
            (
                total_risk_points
                / total_materiality_points
            ) * 100,
        )
    )


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
    # Calculation / metric clauses
    # -------------------

    calculation_patterns = [
        "counted toward",
        "calculated based on",
        "maximum bonus",
        "threshold",
        "limit applicable",

        "plafond",
        "calculé sur",
        "seuil",

        "حد أقصى",
        "يحسب على",
        "عتبة",
    ]

    explicit_high_risk_patterns = [
        "penalty",
        "liquidated damages",
        "fine",
        "exclusive",
        "exclusivity",
        "non-compete",
        "restriction",
        "restrictive covenant",
        "unlimited liability",
        "indemnify",
        "indemnification",

        "pénalité",
        "amende",
        "exclusivité",
        "non-concurrence",
        "responsabilité illimitée",
        "indemniser",

        "غرامة",
        "حصري",
        "عدم المنافسة",
        "مسؤولية غير محدودة",
        "تعويض",
    ]

    if any(p in text for p in calculation_patterns):

        explicit_high_risk = any(
            p in text
            for p in explicit_high_risk_patterns
        )

        if not explicit_high_risk:

            if analysis.get("red_flag"):

                analysis["red_flag"] = False
                analysis["red_flag_reason"] = ""

            if analysis.get("risk_level") == "medium":

                analysis["risk_level"] = "low"
                analysis["negotiation_priority"] = "low"


    # -------------------
    # Payment calculation / bonus mechanics
    # -------------------

    payment_calculation_patterns = [
        "bonus",
        "commercial quantities",
        "production",
        "threshold",
        "maximum bonus",
        "performance-based",

        "prime",
        "seuil",
        "production",

        "مكافأة",
        "إنتاج",
        "حد أقصى",
    ]

    severe_payment_risk_patterns = [
        "penalty",
        "liquidated damages",
        "unlimited liability",
        "sole discretion",
        "unilateral",
        "must pay",
        "shall pay regardless",
        "impossible payment",

        "pénalité",
        "responsabilité illimitée",
        "seule discrétion",
        "unilatéral",

        "غرامة",
        "مسؤولية غير محدودة",
        "تقديره المطلق",
    ]

    if (
        analysis.get("clause_type") == "payment"
        and any(
            p in text
            for p in payment_calculation_patterns
        )
    ):

        severe_payment_risk = any(
            p in text
            for p in severe_payment_risk_patterns
        )

        if not severe_payment_risk:

            analysis["red_flag"] = False
            analysis["red_flag_reason"] = ""

            if analysis.get("risk_level") == "high":
                analysis["risk_level"] = "medium"

            if analysis.get("negotiation_priority") == "high":
                analysis["negotiation_priority"] = "medium"


    # -------------------
    # Standard / safe jurisdiction clauses
    # -------------------

    safe_jurisdiction_patterns = [
        "tribunaux compétents de paris",
        "droit français",
    ]

    if any(
        p in text
        for p in safe_jurisdiction_patterns
    ):

        analysis["red_flag"] = False
        analysis["red_flag_reason"] = ""

        if analysis.get("risk_level") == "medium":
            analysis["risk_level"] = "low"

        if analysis.get("negotiation_priority") == "medium":
            analysis["negotiation_priority"] = "low"


    # -------------------
    # IP transfer after payment protection
    # -------------------

    ip_transfer_patterns = [
        "transfer of ownership upon full payment",
        "ownership transfers after full payment",
        "assignment after payment",
        "cession après paiement",
        "transfert de propriété après paiement",
        "transfer of property after payment",
        "الملكية بعد السداد",
    ]

    if any(
        p in text
        for p in ip_transfer_patterns
    ):

        analysis["red_flag"] = False
        analysis["red_flag_reason"] = ""

        if analysis.get("risk_level") == "high":
            analysis["risk_level"] = "medium"

        if analysis.get("negotiation_priority") == "high":
            analysis["negotiation_priority"] = "medium"


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



def detect_clause_materiality(
    analysis: dict,
    clause_text: str,
) -> str:

    text = clause_text.lower()

    high_materiality_patterns = [
        "payment",
        "bonus",
        "termination",
        "liability",
        "intellectual property",
        "ownership",
        "confidentiality",
        "non-compete",
        "exclusivity",
        "penalty",
        "liquidated damages",

        "paiement",
        "prime",
        "résiliation",
        "responsabilité",
        "propriété intellectuelle",
        "confidentialité",
        "non-concurrence",
        "exclusivité",
        "pénalité",

        "دفع",
        "مكافأة",
        "إنهاء",
        "مسؤولية",
        "ملكية فكرية",
        "سرية",
        "عدم المنافسة",
        "حصري",
        "غرامة",
    ]

    medium_materiality_patterns = [
        "governing law",
        "jurisdiction",
        "venue",
        "notice",
        "term",
        "fixed term",

        "droit applicable",
        "droit français",
        "juridiction",
        "tribunaux compétents",
        "préavis",
        "durée",

        "القانون الواجب التطبيق",
        "الاختصاص",
        "إشعار",
        "مدة",
    ]

    if any(
        pattern in text
        for pattern in high_materiality_patterns
    ):
        return "high"

    if any(
        pattern in text
        for pattern in medium_materiality_patterns
    ):
        return "medium"

    clause_type = analysis.get("clause_type", "other")

    if clause_type in {
        "payment",
        "termination",
        "confidentiality",
        "intellectual_property",
        "liability",
        "penalty",
        "exclusivity",
        "non_compete",
    }:
        return "high"

    return "low"


def calculate_clause_importance(
    analysis: dict,
    clause_text: str,
) -> int:

    text = clause_text.lower()

    baseline = analysis.get(
        "risk_baseline",
        detect_clause_baseline(analysis, clause_text),
    )

    materiality_level = detect_clause_materiality(
        analysis,
        clause_text,
    )

    analysis["materiality_level"] = materiality_level

    materiality_points = {
        "low": 8,
        "medium": 16,
        "high": 24,
    }

    risk_points = {
        "low": 0,
        "medium": 18,
        "high": 45,
    }

    score = materiality_points.get(
        materiality_level,
        16,
    )

    score += risk_points.get(
        analysis.get("risk_level", "low"),
        0,
    )

    # Baseline calibrates legal risk, not business importance.
    if baseline in LOW_RISK_CLAUSES:
        score -= 20

    elif baseline in MEDIUM_RISK_CLAUSES:
        score += 5

    elif baseline in HIGH_RISK_CLAUSES:
        score += 20

    if analysis.get("risk_escalated"):
        score += 25

    if analysis.get("risk_reduced"):
        score -= 20

    if analysis.get("red_flag"):
        score += 25

    if (
        baseline == "limited_liability"
        and not analysis.get("risk_escalated")
        and analysis.get("favours") != "unclear"
    ):
        score -= 15

    standard_clause_patterns = [
        "tribunaux compétents de paris",
        "droit français",
        "confidentialité",
        "confidentiality",
        "responsabilité limitée",
        "limitation of liability",
        "assurance",
        "insurance",
    ]

    if any(
        pattern in text
        for pattern in standard_clause_patterns
    ):

        if not analysis.get("risk_escalated"):
            score -= 15

    # Automatic renewal is not globally standard-safe.
    # It is only reduced when there is no trap/escalator language.
    if (
        (
            "automatic renewal" in text
            or "renouvellement automatique" in text
        )
        and baseline != "automatic_renewal_trap"
        and not analysis.get("risk_escalated")
    ):
        score -= 10

    if (
        "tribunaux compétents de paris" in text
        or "droit français" in text
    ):
        score = min(score, 20)

    return max(
        0,
        min(score, 100),
    )



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



def detect_protective_beneficiary(
    clause_text: str,
) -> bool:

    text = clause_text.lower()

    protective_patterns = [
        "company will maintain insurance",
        "will maintain officers and directors liability insurance",
        "company shall indemnify",
        "company will reimburse",
        "coverage for",
        "named insured",

        "la société indemnisera",
        "la société maintiendra",

        "تلتزم الشركة",
        "تقوم الشركة بالتعويض",
    ]

    return any(
        p in text
        for p in protective_patterns
    )



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

        analysis = validate_protective_clause(
            analysis,
            clause,
        )

        analysis = validate_standard_market_protection(
            analysis,
            clause,
        )

        analysis = validate_explicit_permission_clause(
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

        analysis = apply_conceptual_risk_calibration(
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

        if detect_protective_beneficiary(clause):

            analysis["favours"] = "employee"

            if analysis.get("risk_level") == "medium":
                analysis["risk_level"] = "low"

            analysis["negotiation_priority"] = "low"

        if (
            analysis.get("risk_level") == "medium"
            and not analysis.get("red_flag")
            and analysis.get("clause_type") == "other"
            and analysis.get("risk_baseline") in LOW_RISK_CLAUSES
        ):
            analysis["risk_level"] = "low"
            analysis["negotiation_priority"] = "low"

        if analysis.get("risk_level") == "low":

            analysis["negotiation_priority"] = "low"

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

    seen_quotes = set()
    deduped = []

    for item in results:

        quote = (
            item.get("quoted_text", "")
            .lower()
            .strip()
        )[:80]

        if quote and quote in seen_quotes:
            continue

        seen_quotes.add(quote)
        deduped.append(item)

    deduped = deduped[:12]

    normalized_contract_score = normalize_importance_score(
        deduped
    )

    for item in deduped:
        item["normalized_contract_score"] = normalized_contract_score

    return deduped
