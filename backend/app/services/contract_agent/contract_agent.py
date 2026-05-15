import json
from typing import Any

from openai import OpenAI

from app.config import OPENAI_API_KEY
from app.services.contract_agent.risk_engine import analyze_risk
from app.services.contract_agent.clause_title_extractor import extract_clause_title
from app.services.contract_agent.cross_clause_analysis import (
    analyze_cross_clause_risks,
)
from app.services.contract_agent.cross_clause_conflicts import (
    detect_cross_clause_conflicts,
)
from app.services.contract_agent.obligation_extractor import (
    extract_contract_obligations,
)
from app.services.contract_agent.timeline_extractor import (
    extract_contract_timeline,
)
from app.services.contract_agent.enterprise_audit import (
    generate_enterprise_audit,
)
from app.services.contract_agent.semantic_negotiation import (
    get_semantic_negotiation,
)
from app.services.contract_agent.legal_reasoning_templates import (
    get_reasoning_for_text,
)
from app.services.contract_agent.contract_taxonomy import (
    CLAUSE_TYPES,
    CLAUSE_PRIORITY_ORDER,
    detect_clause_type_from_taxonomy,
    get_all_critical_terms,
    has_clause_type_signal,
    is_critical_clause_text,
)
from app.services.contract_agent.jurisdiction_profiles import (
    detect_jurisdiction,
)
from app.utils.prompt_loader import load_prompt

client = OpenAI(api_key=OPENAI_API_KEY)


ALLOWED_CLAUSE_TYPES = {
    "payment",
    "termination",
    "confidentiality",
    "intellectual_property",
    "liability",
    "limitation_of_liability",
    "indemnity",
    "penalty",
    "exclusivity",
    "non_compete",
    "data_protection",
    "arbitration",
    "governing_law",
    "jurisdiction",
    "venue",
    "warranty",
    "service_level",
    "insurance",
    "assignment",
    "amendment",
    "renewal",
    "default",
    "security",
    "maintenance",
    "repair",
    "covenant",
    "other",
}

ALLOWED_RISK_LEVELS = {"low", "medium", "high"}
ALLOWED_FAVOURS = {
    "employer", "employee", "company", "contractor",
    "vendor", "client", "balanced", "unclear"
}
ALLOWED_CONFIDENCE = {"low", "medium", "high"}
ALLOWED_PRIORITY = {"low", "medium", "high"}


CLAUSE_SIGNAL_GROUPS = {
    "critical": [
        "termination",
        "default",
        "acceleration",
        "liability",
        "confidentiality",
        "data protection",
        "service level",
        "governing law",
        "indemnity",
        "security",
        "payment",
        "pricing",
        "maintenance",
        "repair",
        "covenants",
        "loan amount",
        "principal amount",
        "interest",

        "résiliation",
        "défaut",
        "responsabilité",
        "confidentialité",
        "protection des données",
        "niveau de service",
        "droit applicable",
        "paiement",
        "prix",
        "maintenance",
        "réparations",
        "montant du prêt",
        "capital",
        "intérêt",

        "فسخ",
        "إنهاء",
        "الإخلال",
        "المسؤولية",
        "السرية",
        "حماية البيانات",
        "مستوى الخدمة",
        "القانون الواجب التطبيق",
        "الدفع",
        "الأسعار",
        "الصيانة",
        "الإصلاحات",
        "التعهدات",
        "مبلغ القرض",
        "رأس المال",
        "الفائدة",
    ],
    "financial": [
        "payment",
        "pricing",
        "interest",
        "late payment",
        "bonus",
        "invoice",
        "paiement",
        "prix",
        "intérêt",
        "retard de paiement",
        "prime",
        "facture",
        "الدفع",
        "الأسعار",
        "الفائدة",
        "تأخر الدفع",
        "مكافأة",
        "فاتورة",
    ],
    "termination": [
        "termination",
        "default",
        "acceleration",
        "cure period",
        "notice period",
        "résiliation",
        "défaut",
        "délai de correction",
        "préavis",
        "فسخ",
        "إنهاء",
        "الإخلال",
        "مهلة تصحيح",
        "إشعار",
    ],
    "definitions": [
        "defined terms",
        "definition",
        "definitions",
        "means",
        "shall mean",
        "désigne",
        "signifie",
        "définition",
        "définitions",
        "يقصد به",
        "يعني",
        "تعريف",
        "التعريفات",
    ],
}


def get_clause_signal_terms(group: str) -> list[str]:
    return CLAUSE_SIGNAL_GROUPS.get(group, [])


LOW_RISK_CLAUSES = [
    "governing_law",
    "venue",
    "payment_schedule",
    "standard_confidentiality",
    "fixed_term",
    "ip_after_payment",
    "mutual_termination_notice",
    "administrative_amendment",
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
    # Contextual legal / operational escalators.
    # Avoid generic words alone like "unlimited" because
    # "unlimited access" is not the same as "unlimited liability".
    "unlimited liability",
    "perpetual restriction",
    "unilateral amendment",
    "without cure period",
    "without notice termination",
    "without remedy",
    "sole discretion",
    "irreversible assignment",
    "irrevocable assignment",
    "perpetual non-compete",
    "unilateral termination",

    "responsabilité illimitée",
    "restriction perpétuelle",
    "modification unilatérale",
    "sans délai de correction",
    "résiliation sans préavis",
    "sans recours",
    "seule discrétion",
    "cession irréversible",
    "cession irrévocable",
    "non-concurrence perpétuelle",
    "résiliation unilatérale",

    "مسؤولية غير محدودة",
    "قيد دائم",
    "تعديل من جانب واحد",
    "دون مهلة تصحيح",
    "إنهاء دون إشعار",
    "دون تعويض",
    "تقديره المطلق",
    "تنازل غير قابل للإلغاء",
    "عدم منافسة دائم",
    "إنهاء من جانب واحد",
]

RISK_REDUCERS = [
    "notice period",
    "mutual termination",
    "cure period",
    "arbitration",
    "liability insurance",
    "liability cap",
    "compensation remedy",

    "préavis",
    "résiliation mutuelle",
    "délai de correction",
    "arbitrage",
    "assurance responsabilité",
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
    "déséquilibre de pouvoir",
    "laissant le client vulnérable",
    "leaving the client vulnerable",
    "ne pas couvrir tous les dommages",
    "not cover all damages",
    "entièrement protégé",
    "fully protected",
    "clause de renouvellement",
    "renewal clause",
    "continuité des relations commerciales",
    "business continuity",
    "retarder la fin du contrat",
    "delay contract termination",
    "risques potentiels",
    "potential risks",
    "protections adéquates",
    "adequate protections",
    "options de renouvellement",
    "renewal options",
    "conditions de renouvellement",
    "renewal terms",
    "prolonger la relation contractuelle",
    "extend the contractual relationship",
    "protéger les intérêts financiers",
    "protect financial interests",
    "même en cas de négligence",
    "even in case of negligence",
    "dommages potentiels",
    "potential damages",
    "besoins opérationnels",
    "operational needs",
    "option de renouvellement",
    "renewal option",
    "prolongation est souhaitée",
    "extension is desired",
    "مكان محايد",
    "neutral venue",
    "خيار التحكيم",
    "arbitration alternative",
    "مناسب لجميع الأطراف",
    "appropriate for all parties",
    "قد يسبب مشاكل",
    "may cause problems",
    "إذا لم يتم التخطيط",
    "if not properly planned",
    "operational disruption",
    "اضطراب تشغيلي",
]


RESTRICTED_RECOMMENDATION_ONLY_PATTERNS = [
    "responsabilité illimitée",
    "unlimited liability",
    "dommages indirects",
    "indirect damages",
    "conséquences juridiques",
    "legal consequences",
    "financial exposure",
    "protection adéquate",
    "adequate protection",
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


def localize_clause_reference(
    reference: str,
    language: str,
) -> str:

    if not reference:
        return ""

    reference = str(reference).strip()

    replacements = {
        "en": {
            "المادة": "Article",
            "البند": "Clause",
            "الفقرة": "Section",
        },
        "fr": {
            "المادة": "Article",
            "البند": "Clause",
            "الفقرة": "Section",
        },
        "ar": {
            "Article": "المادة",
            "Clause": "البند",
            "Section": "الفقرة",
        },
    }

    localized = reference

    for source_text, target_text in replacements.get(language, {}).items():
        localized = localized.replace(source_text, target_text)

    return localized


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

        "clause_reference": localize_clause_reference(
            safe_str(
                ai_result.get("clause_reference")
            ),
            ai_result.get("language", "en"),
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



def apply_reasoning_quality_gate(
    analysis: dict,
    clause_text: str,
    language: str,
) -> dict:
    """
    Final deterministic text-quality gate only.

    This function intentionally does NOT modify:
    - risk_level
    - red_flag
    - red_flag_reason
    - negotiation_priority
    - favours

    Risk/business calibration must stay in the dedicated risk and
    calibration functions.
    """

    text = safe_str(clause_text).lower()

    detail_fields = [
        "recommendation",
        "negotiation_advice",
        "legal_insight",
        "market_comparison",
        "safer_alternative",
    ]

    dangerous_terms = [
        "dangerous",
        "hazardous",
        "illegal",
        "unlawful",
        "criminal",
        "fraud",
        "dangerous activity",

        "dangereux",
        "illégal",
        "fraude",

        "خطير",
        "خطيرة",
        "مخالفة",
        "غير قانوني",
        "احتيال",
    ]

    cleanup_fields = [
        "explanation_simple",
        "recommendation",
        "legal_insight",
        "negotiation_advice",
        "market_comparison",
        "safer_alternative",
    ]

    for field in cleanup_fields:
        value = safe_str(
            analysis.get(field)
        )

        lowered_value = value.lower()

        for term in dangerous_terms:
            if (
                term in lowered_value
                and term not in text
            ):
                analysis[field] = ""
                break

    hallucination_guard = {
        "illegal activity": [
            "illegal",
            "unlawful",
            "criminal",
            "crime",
            "activité illégale",
            "illégal",
            "criminel",
            "نشاط غير قانوني",
            "غير قانوني",
            "جريمة",
        ],
        "fraud": [
            "fraud",
            "fraudulent",
            "misrepresentation",
            "fraude",
            "frauduleux",
            "احتيال",
            "تدليس",
        ],
        "abusive conduct": [
            "abusive",
            "abuse",
            "bad faith",
            "abusif",
            "abus",
            "سلوك تعسفي",
            "تعسف",
        ],
        "penalties": [
            "penalty",
            "fine",
            "liquidated damages",
            "late payment penalty",
            "pénalité",
            "amende",
            "dommages-intérêts forfaitaires",
            "غرامة",
            "جزاء",
            "تعويضات مقطوعة",
        ],
        "obligations": [
            "shall",
            "must",
            "is required to",
            "obligation",
            "obligé",
            "doit",
            "est tenu",
            "يلتزم",
            "يجب",
            "التزام",
        ],
    }

    for concept, evidence_terms in hallucination_guard.items():
        concept_present = any(
            term in text
            for term in evidence_terms
        )

        if concept_present:
            continue

        for field in detail_fields + [
            "explanation_simple",
            "why_it_matters",
        ]:
            value = safe_str(
                analysis.get(field)
            )

            if concept in value.lower():
                analysis[field] = ""

    generic_detail_phrases = [
        "avoid disputes",
        "future disputes",
        "ensure clarity",
        "consider negotiating",
        "market standards",
        "potential disputes",
        "may lead to",
        "could impact",
        "more favorable",
        "business growth",
        "operational flexibility",
        "sets the foundation",
        "while this clause is standard",
        "avoid ambiguity",
        "market conditions change",
        "cash flow is a concern",
        "work-life balance",

        "éviter les litiges",
        "éviter toute ambiguïté",
        "assurer la clarté",
        "envisager de négocier",
        "normes du marché",
        "risques potentiels",
        "conditions du marché",

        "تجنب النزاعات",
        "تجنب الغموض",
        "ضمان الوضوح",
        "معايير السوق",
        "مخاطر محتملة",
        "ظروف السوق",
    ]

    for field in detail_fields:
        value = safe_str(
            analysis.get(field)
        ).lower()

        if any(
            phrase in value
            for phrase in generic_detail_phrases
        ):
            analysis[field] = ""

    analysis["has_details"] = any(
        safe_str(
            analysis.get(field)
        )
        for field in detail_fields
    )

    if (
        not safe_str(analysis.get("explanation_simple"))
        and analysis.get("risk_level") in {"medium", "high"}
    ):
        analysis["explanation_simple"] = (
            "This clause may create important legal or "
            "commercial obligations."
            if language == "en"
            else
            "Cette clause peut créer des obligations "
            "juridiques ou commerciales importantes."
            if language == "fr"
            else
            "قد تنشئ هذه المادة التزامات قانونية أو "
            "تجارية مهمة."
        )

    return analysis

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

    ai_result["language"] = language

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

    if is_truncated_clause(clause):
        ai_result["confidence"] = "low"
        ai_result["red_flag"] = False
        ai_result["red_flag_reason"] = ""

        if ai_result.get("risk_level") == "high":
            ai_result["risk_level"] = "medium"

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

    if analysis.get("risk_level") == "low":
        return analysis

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

        if field in {
            "recommendation",
            "negotiation_advice",
            "safer_alternative",
        }:

            for pattern in RESTRICTED_RECOMMENDATION_ONLY_PATTERNS:

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
    language: str = "en",
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

        unsupported_messages = {
            "en": (
                "The clause does not explicitly contain "
                "a legally identifiable "
                f"{clause_type.replace('_', ' ')} provision."
            ),
            "fr": (
                "La clause ne contient pas explicitement "
                "une disposition juridiquement identifiable de type "
                f"{clause_type.replace('_', ' ')}."
            ),
            "ar": (
                "لا يتضمن هذا البند صراحةً حكماً قانونياً "
                f"يمكن تصنيفه على أنه {clause_type.replace('_', ' ')}."
            ),
        }

        analysis["legal_insight"] = unsupported_messages.get(
            language,
            unsupported_messages["en"],
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



def is_truncated_clause(
    clause_text: str,
) -> bool:
    """
    Detect clauses that look cut off by OCR/PDF extraction.

    This is a quality rule, not a business-risk rule.
    """

    text = safe_str(clause_text)

    if not text:
        return False

    lowered = text.lower().strip()

    truncated_endings = [
        ",",
        ";",
        ":",
        "(",
        "[",
        "{",
        "and",
        "or",
        "including",
        "including but not limited to",
        "et",
        "ou",
        "notamment",
        "y compris",
        "و",
        "أو",
        "بما في ذلك",
    ]

    if any(
        lowered.endswith(ending)
        for ending in truncated_endings
    ):
        return True

    opening_pairs = [
        ("(", ")"),
        ("[", "]"),
        ("{", "}"),
        ("“", "”"),
        ('"', '"'),
    ]

    for opener, closer in opening_pairs:
        if opener == closer:
            if text.count(opener) % 2 != 0:
                return True
        elif text.count(opener) > text.count(closer):
            return True

    return False


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
        "administrative_amendment": [
            "amended and restated",
            "restatement of existing",
            "restated agreement",
            "amendment and restatement",
            "amendment to the agreement",

            "modifié et reformulé",
            "modification de l’accord",
            "modification du contrat",

            "معدل ومعاد صياغته",
            "إعادة صياغة",
            "تعديل الاتفاقية",
            "تعديل العقد",
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

    if baseline == "limited_liability":

        standard_liability_patterns = [
            "limited to the total amount paid",
            "limited to amounts paid",
            "plafonnée au montant payé",
            "limitée au montant total payé",
            "حد المسؤولية",
        ]

        severe_liability_patterns = [
            "gross negligence excluded",
            "intentional misconduct excluded",
            "all damages excluded",
            "indirect damages only",
            "faute lourde exclue",
            "dol exclu",
        ]

        standard_cap = any(
            p in text
            for p in standard_liability_patterns
        )

        severe_cap = any(
            p in text
            for p in severe_liability_patterns
        )

        if standard_cap and not severe_cap:

            analysis["red_flag"] = False
            analysis["red_flag_reason"] = ""

            if analysis.get("risk_level") == "high":
                analysis["risk_level"] = "medium"

            if analysis.get("negotiation_priority") == "high":
                analysis["negotiation_priority"] = "medium"

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
        "courts of paris",
        "french law",
        "المحاكم المختصة بمدينة الدار البيضاء",
        "قوانين المملكة المغربية",
        "courts of casablanca",
        "laws of morocco",
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

    broad_confidentiality_patterns = [
        "trade secret",
        "trade secrets",
        "all confidential information",
        "perpetual confidentiality",
        "confidentiality obligations survive indefinitely",
        "indefinitely confidential",

        "secret commercial",
        "secrets commerciaux",
        "toute information confidentielle",
        "confidentialité perpétuelle",
        "obligations de confidentialité survivent indéfiniment",
        "confidentiel indéfiniment",

        "سر تجاري",
        "أسرار تجارية",
        "جميع المعلومات السرية",
        "سرية دائمة",
        "تظل التزامات السرية إلى أجل غير مسمى",
    ]

    standard_confidentiality_patterns = [
        "confidentiality",
        "confidential information",
        "confidentialité",
        "information confidentielle",
        "سرية",
        "معلومات سرية",
    ]

    if any(
        pattern in text
        for pattern in broad_confidentiality_patterns
    ):
        return "high"

    if any(
        pattern in text
        for pattern in standard_confidentiality_patterns
    ):
        return "medium"

    high_materiality_patterns = [
        "payment",
        "bonus",
        "termination",
        "liability",
        "intellectual property",
        "ownership",
        "non-compete",
        "exclusivity",
        "penalty",
        "liquidated damages",

        "paiement",
        "prime",
        "résiliation",
        "responsabilité",
        "propriété intellectuelle",
        "non-concurrence",
        "exclusivité",
        "pénalité",

        "دفع",
        "مكافأة",
        "إنهاء",
        "مسؤولية",
        "ملكية فكرية",
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

    if clause_type == "confidentiality":
        return "medium"

    if clause_type in {
        "payment",
        "termination",
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
    # Do not reduce importance when the clause contains explicit escalation.
    if (
        baseline in LOW_RISK_CLAUSES
        and not analysis.get("risk_escalated")
    ):
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
        score -= 25

    standard_clause_patterns = [
        "tribunaux compétents de paris",
        "droit français",
        "standard confidentiality",
        "information confidentielle",
        "confidential information",
        "responsabilité limitée",
        "limitation of liability",
        "assurance responsabilité",
        "liability insurance",
    ]

    if any(
        pattern in text
        for pattern in standard_clause_patterns
    ):

        if not analysis.get("risk_escalated"):
            score -= 15

    # Automatic renewal is not globally standard-safe.
    # It is reduced only when the clause clearly gives
    # an opt-out or cancellation right with notice.
    safe_renewal_patterns = [
        "may opt out with notice",
        "cancel with notice",
        "résiliation avec préavis",
        "يمكن الإلغاء بإشعار",
    ]

    if (
        (
            "automatic renewal" in text
            or "renouvellement automatique" in text
        )
        and any(
            pattern in text
            for pattern in safe_renewal_patterns
        )
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





def extract_reasoning_evidence(
    clause_text: str,
    max_length: int = 160,
) -> str:

    text = str(clause_text or "").strip()

    if not text:
        return ""

    text = " ".join(text.split())

    return text[:max_length]



def compute_analysis_metadata(
    analysis: dict,
    clause_text: str,
    title: str = "",
) -> dict:
    """
    Compute derived display/search metadata in one place.

    This avoids scattering has_details / signal checks across the
    clause-analysis loop.
    """

    detail_fields = [
        "recommendation",
        "negotiation_advice",
        "legal_insight",
        "market_comparison",
        "safer_alternative",
    ]

    combined_text = f"{title} {clause_text}".lower()

    has_details = any(
        safe_str(
            analysis.get(field)
        )
        for field in detail_fields
    )

    has_reasoning = any([
        safe_str(analysis.get("explanation_simple")),
        safe_str(analysis.get("why_it_matters")),
        safe_str(analysis.get("legal_insight")),
    ])

    has_negotiation = bool(
        safe_str(
            analysis.get("negotiation_advice")
        )
    )

    has_legal_signal = any(
        term in combined_text
        for term in get_clause_signal_terms("critical")
    )

    has_semantic_signal = any([
        has_legal_signal,
        analysis.get("risk_level") in {"medium", "high"},
        bool(analysis.get("red_flag")),
        bool(analysis.get("risk_escalated")),
    ])

    evidence_strength = "low"

    if analysis.get("risk_level") in {"medium", "high"}:
        evidence_strength = "medium"

    if analysis.get("red_flag") or analysis.get("risk_escalated"):
        evidence_strength = "high"

    analysis["has_details"] = any([
        has_details,
        has_reasoning,
        has_negotiation,
        has_semantic_signal,
    ])

    analysis["has_reasoning"] = has_reasoning
    analysis["has_negotiation"] = has_negotiation
    analysis["has_semantic_signal"] = has_semantic_signal
    analysis["has_legal_signal"] = has_legal_signal
    analysis["evidence_strength"] = evidence_strength

    return analysis


def _analyze_contract_clauses_impl(
    clauses: list[str],
    language: str = "en",
    max_clauses: int = 25,
) -> list[dict]:

    critical_terms = get_clause_signal_terms("critical")

    full_contract_text = " ".join([
        str(c)
        for c in clauses
    ]).lower()

    jurisdiction_profile = detect_jurisdiction(
        full_contract_text
    )

    contract_domain_reasoning = (
        get_reasoning_for_text(
            full_contract_text,
            language,
        )
    )

    results = []

    for clause in clauses[:max_clauses]:

        analysis = analyze_clause(
            clause,
            language,
        )

        analysis = validate_clause_type(
            analysis,
            clause,
            language,
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

        if analysis.get("risk_level") in {"medium", "high"}:
            semantic_negotiation = get_semantic_negotiation(
                analysis,
                language=language,
            )

            if semantic_negotiation:
                analysis["negotiation_advice"] = semantic_negotiation

        else:
            analysis["negotiation_advice"] = ""

        ADMINISTRATIVE_KEYWORDS = [
            "assignment",
            "acceptance",
            "commitment",
            "schedule",
            "exhibit",
            "appendix",
            "definition",
            "effective date",
            "reference",
            "designation",
            "form of",

            "cession",
            "acceptation",
            "engagement",
            "annexe",
            "définition",
            "date d’effet",

            "التنازل",
            "القبول",
            "الالتزام",
            "ملحق",
            "تعريف",
        ]

        if (
            analysis.get("risk_level") == "medium"
            and not analysis.get("red_flag")
        ):
            lowered = clause.lower()

            matches = sum(
                1 for keyword in ADMINISTRATIVE_KEYWORDS
                if keyword in lowered
            )

            if matches >= 2:
                analysis["risk_level"] = "low"
                analysis["negotiation_priority"] = "low"

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

        # Only downgrade generic clauses when the conceptual baseline
        # is explicitly low-risk. This avoids hiding real medium-risk
        # "other" clauses that do not match a safe baseline.
        if (
            analysis.get("risk_level") == "medium"
            and not analysis.get("red_flag")
            and analysis.get("clause_type") == "other"
            and analysis.get("risk_baseline") in LOW_RISK_CLAUSES
        ):
            analysis["risk_level"] = "low"
            analysis["negotiation_priority"] = "low"

        title = (
            analysis.get("clause_title")
            or extract_clause_title(clause)
        )

        clause_text = clause

        analysis = compute_analysis_metadata(
            analysis,
            clause_text,
            title,
        )

        if (
            analysis.get("risk_level") == "low"
            and not analysis.get("has_legal_signal")
            and not analysis.get("has_semantic_signal")
        ):
            analysis["negotiation_priority"] = "low"

        medium_risk_keywords = [
            "terminate immediately",
            "confidentiality",
            "limitation of liability",
            "late payment penalty",
            "default",
            "acceleration",
            "exclusive",
            "non-exclusive",
            "interest rate",
            "liability cap",

            "résiliation immédiate",
            "confidentialité",
            "limitation de responsabilité",
            "défaut",
            "taux d'intérêt",

            "فسخ",
            "سرية",
            "المسؤولية",
            "الإخلال",
            "الفائدة",
        ]

        combined = " ".join([
            title,
            clause_text,
        ]).lower()

        keyword_match = any(
            k in combined
            for k in medium_risk_keywords
        )

        risky_wording_terms = [
            "immediately",
            "without notice",
            "without cure",
            "sole discretion",
            "unilateral",
            "late payment penalty",
            "acceleration",
            "exclusive",
            "non-compete",
            "unlimited",
            "material breach",

            "immédiatement",
            "sans préavis",
            "sans délai de correction",
            "seule discrétion",
            "unilatéral",
            "pénalité",
            "défaut",
            "exclusif",

            "فوري",
            "دون إشعار",
            "دون مهلة",
            "تقديره المطلق",
            "من جانب واحد",
            "غرامة",
            "إخلال جوهري",
            "حصري",
        ]

        risky_wording_match = any(
            term in combined
            for term in risky_wording_terms
        )

        if (
            analysis.get("risk_level") == "low"
            and keyword_match
            and (
                analysis.get("risk_escalated")
                or analysis.get("red_flag")
                or risky_wording_match
            )
        ):
            analysis["risk_level"] = "medium"

        analysis["importance_score"] = (
            calculate_clause_importance(
                analysis,
                clause,
            )
        )

        definition_keywords = [
            "defined terms",
            "definition",
            "definitions",
            "means",
            "shall mean",

            "définition",
            "définitions",
            "désigne",
            "signifie",

            "التعريفات",
            "تعريف",
            "يقصد به",
            "يعني",
        ]

        lowered_clause = clause.lower()

        definition_matches = sum(
            1 for keyword in definition_keywords
            if keyword in lowered_clause
        )

        if (
            definition_matches >= 2
            and analysis.get("risk_level") == "low"
            and analysis.get("materiality_level") != "high"
        ):
            analysis["risk_level"] = "low"
            analysis["negotiation_priority"] = "low"
            analysis["recommendation"] = ""
            analysis["negotiation_advice"] = ""
            analysis["safer_alternative"] = ""

        normalized_clause = " ".join(
            clause.strip().split()
        )

        word_count = len(normalized_clause.split())

        critical_short_clause = any(
            term in normalized_clause.lower()
            for term in get_clause_signal_terms("critical")
        )

        fragment_like = (
            not critical_short_clause
            and (
                normalized_clause.endswith(",")
                or normalized_clause.endswith(";")
                or (
                    normalized_clause.isupper()
                    and word_count <= 8
                )
            )
        )

        if fragment_like:
            analysis["risk_level"] = "low"
            analysis["negotiation_priority"] = "low"

            analysis["recommendation"] = (
                "This text appears to be a heading or incomplete clause fragment."
            )

            analysis["negotiation_advice"] = ""
            analysis["legal_insight"] = ""
            analysis["market_comparison"] = ""
            analysis["safer_alternative"] = ""

        lowered_clause = clause.lower()

        definition_or_fragment = (
            " means " in lowered_clause
            or " shall mean " in lowered_clause
            or " désigne " in lowered_clause
            or " signifie " in lowered_clause
            or " يقصد به " in lowered_clause
            or " يعني " in lowered_clause
        )

        critical_definition_terms = [
            "breach",
            "default",
            "liability",
            "payment",
            "termination",
            "indemnity",
            "material breach",
            "acceleration",
            "confidentiality",
            "intellectual property",
            "data protection",
            "service level",

            "manquement",
            "défaut",
            "responsabilité",
            "paiement",
            "résiliation",
            "indemnisation",
            "confidentialité",
            "propriété intellectuelle",
            "protection des données",
            "niveau de service",

            "إخلال",
            "الإخلال",
            "المسؤولية",
            "الدفع",
            "فسخ",
            "إنهاء",
            "تعويض",
            "السرية",
            "الملكية الفكرية",
            "حماية البيانات",
            "مستوى الخدمة",
        ]

        is_critical_definition = any(
            term in lowered_clause
            for term in critical_definition_terms
        )

        if definition_or_fragment and not is_critical_definition:
            analysis["risk_level"] = "low"
            analysis["red_flag"] = False
            analysis["red_flag_reason"] = ""
            analysis["negotiation_priority"] = "low"

            analysis["explanation_simple"] = (
                "This clause is primarily administrative or definitional."
            )

            if language == "fr":
                analysis["explanation_simple"] = (
                    "Cette clause est principalement administrative ou définitionnelle."
                )

            elif language == "ar":
                analysis["explanation_simple"] = (
                    "هذا البند ذو طبيعة تعريفية أو إدارية بشكل أساسي."
                )

            analysis["recommendation"] = ""
            analysis["negotiation_advice"] = ""
            analysis["legal_insight"] = ""
            analysis["market_comparison"] = ""
            analysis["safer_alternative"] = ""

        quoted_text = str(
            analysis.get("quoted_text", "")
        ).strip()

        weak_context = (
            not analysis.get("has_legal_signal")
            and not analysis.get("risk_escalated")
            and len(quoted_text.split()) < 6
        )

        if weak_context:
            analysis["negotiation_advice"] = ""
            analysis["safer_alternative"] = ""

            if not analysis.get("legal_insight"):
                analysis["legal_insight"] = ""

        detail_fields = [
            "recommendation",
            "negotiation_advice",
            "legal_insight",
            "market_comparison",
            "safer_alternative",
        ]

        always_important_keywords = [
            # English
            "default",
            "termination",
            "liability",
            "confidentiality",
            "interest",
            "payment",
            "penalty",
            "indemnity",

            "maintenance",
            "repair",

            "governing law",
            "exclusive",
            "non-compete",

            # French
            "défaut",
            "résiliation",
            "responsabilité",
            "confidentialité",
            "paiement",
            "pénalité",
            "indemnisation",

            "maintenance",
            "réparation",
            "entretien",

            "droit applicable",
            "exclusif",

            # Arabic
            "فسخ",
            "إنهاء",
            "المسؤولية",
            "السرية",
            "الدفع",
            "غرامة",
            "تعويض",

            "صيانة",
            "إصلاحات",

            "القانون",
            "حصري",
        ]

        combined_text = " ".join([
            title,
            clause_text,
        ]).lower()

        important_keywords = [
            "termination",
            "default",
            "payment",
            "liability",
            "confidentiality",
            "intellectual property",

            "résiliation",
            "défaut",
            "paiement",
            "responsabilité",

            "فسخ",
            "الإخلال",
            "الدفع",
            "الملكية الفكرية",
        ]

        meaningful_content = any([
            analysis.get("quoted_text"),
            analysis.get("explanation_simple"),
            any(
                safe_str(analysis.get(field))
                for field in detail_fields
            ),
        ])

        if not meaningful_content:
            continue

        generic_detail_phrases = [
            "avoid disputes",
            "future disputes",
            "ensure clarity",
            "consider negotiating",
            "potential disputes",
            "may lead to",
            "could impact",
            "market standards",
            "more favorable",
            "business growth",
            "operational flexibility",
        ]

        generic_detail_phrases = [
            "while this clause is standard",
            "could lead to disputes",
            "potential disputes",
            "may limit",
            "could impact",
            "may face",
            "may create",
            "standard but",
            "avoid ambiguity",
            "ensure clarity",
            "consider negotiating",

            "peut limiter",
            "pourrait",
            "peut entraîner",
            "risques potentiels",
            "éviter toute ambiguïté",

            "قد",
            "يمكن أن",
            "قد يؤدي",
        ]

        detail_fields = [
            "recommendation",
            "negotiation_advice",
            "legal_insight",
            "market_comparison",
            "safer_alternative",
        ]

        for field in detail_fields:
            value = str(
                analysis.get(field, "")
            ).lower()

            if any(
                phrase in value
                for phrase in generic_detail_phrases
            ):
                analysis[field] = ""

        # Keep all analyzed clauses, including low-risk clauses.
        # Low-risk clauses are useful for transparency in FR/EN/AR.

        important_clause_keywords = [
            "termination", "default", "acceleration", "liability",
            "confidentiality", "intellectual property", "data protection",
            "service level", "maintenance", "repair",

            "résiliation", "défaut", "responsabilité",
            "confidentialité", "propriété intellectuelle",
            "protection des données", "disponibilité", "entretien",

            "فسخ", "إنهاء", "الإخلال", "المسؤولية",
            "السرية", "الملكية الفكرية", "حماية البيانات",
            "مستوى الخدمة", "الصيانة", "الإصلاحات",
        ]

        combined_text = f"{title} {clause}".lower()

        domain_reasoning = contract_domain_reasoning

        domain_reasoning_allowed = (
            analysis.get("risk_level") in {"medium", "high"}
            or any(
                safe_str(analysis.get(field))
                for field in detail_fields
            )
            or any(
                k in combined_text
                for k in critical_terms
            )
        )

        if any(
            k in combined_text
            for k in important_clause_keywords
        ):
            if (
                "administrative"
                in analysis.get(
                    "explanation_simple",
                    ""
                ).lower()
            ):
                analysis["explanation_simple"] = (
                    "This clause contains operational or legal obligations."
                    if language == "en"
                    else
                    "Cette clause contient des obligations juridiques ou opérationnelles."
                    if language == "fr"
                    else
                    "تتضمن هذه المادة التزامات قانونية أو تشغيلية."
                )

        if (
            analysis.get("risk_level") in {"medium", "high"}
            and not analysis.get("legal_insight")
        ):
            analysis["legal_insight"] = (
                "This clause should be reviewed because it may affect legal, financial, or operational obligations."
                if language == "en"
                else
                "Cette clause doit être examinée car elle peut affecter des obligations juridiques, financières ou opérationnelles."
                if language == "fr"
                else
                "ينبغي مراجعة هذه المادة لأنها قد تؤثر على الالتزامات القانونية أو المالية أو التشغيلية."
            )

        medium_risk_terms = [
            "material breach", "default", "acceleration", "late payment",
            "termination", "confidentiality", "liability cap",
            "service level", "data protection",

            "manquement important", "défaut", "résiliation",
            "retard de paiement", "confidentialité",
            "plafond de responsabilité", "protection des données",

            "إخلال جوهري", "الإخلال", "فسخ", "إنهاء",
            "تأخر الدفع", "السرية", "حد المسؤولية",
            "حماية البيانات",
        ]

        if (
            analysis.get("risk_level") == "low"
            and any(
                term in combined_text
                for term in medium_risk_terms
            )
        ):
            analysis["risk_level"] = "medium"

        clause_type_text = f"{title} {clause}".lower()

        critical_terms = [
            "termination",
            "default",
            "acceleration",
            "liability",
            "confidentiality",
            "data protection",
            "service level",
            "governing law",
            "indemnity",
            "security",

            "résiliation",
            "défaut",
            "responsabilité",
            "confidentialité",
            "protection des données",
            "niveau de service",
            "droit applicable",

            "فسخ",
            "إنهاء",
            "الإخلال",
            "المسؤولية",
            "السرية",
            "حماية البيانات",
            "مستوى الخدمة",
            "القانون الواجب التطبيق",
            "payment",

            "pricing",

            "maintenance",

            "repair",

            "covenants",

            "paiement",

            "prix",

            "maintenance",

            "réparations",

            "الدفع",

            "الأسعار",

            "الصيانة",

            "الإصلاحات",

            "التعهدات",

        ]

        if any(
            t in clause_type_text
            for t in critical_terms
        ):

            maintenance_terms = [
                "maintenance",
                "repair",
                "صيانة",
                "إصلاح",
            ]

            excluded_contexts = [
                "service level",
                "sla",
                "uptime",
                "disponibilité",
                "payment",
                "pricing",
                "الدفع",
                "الأسعار",
                "مستوى الخدمة",
            ]

            disable_maintenance_override = (
                "service level" in clause_type_text
                or "uptime" in clause_type_text
                or "disponibilité" in clause_type_text
                or "مستوى الخدمة" in clause_type_text
            )

            if (
                not disable_maintenance_override
                and any(
                    term in clause_type_text
                    for term in maintenance_terms
                )
                and not any(
                    term in clause_type_text
                    for term in excluded_contexts
                )
            ):
                analysis["explanation_simple"] = (
                    "This clause allocates maintenance and repair "
                    "responsibilities between the parties."
                    if language == "en"
                    else
                    "Cette clause répartit les responsabilités de "
                    "maintenance et de réparation entre les parties."
                    if language == "fr"
                    else
                    "تحدد هذه المادة توزيع مسؤوليات الصيانة "
                    "والإصلاح بين الأطراف."
                )

            elif (
                "administrative"
                in analysis.get(
                    "explanation_simple",
                    ""
                ).lower()
                or
                "تعريفية"
                in analysis.get(
                    "explanation_simple",
                    ""
                )
            ):
                analysis["explanation_simple"] = (
                    "This clause defines operational responsibilities, "
                    "maintenance obligations, or commercial duties."
                    if language == "en"
                    else
                    "Cette clause définit des responsabilités "
                    "opérationnelles, des obligations de maintenance "
                    "ou des engagements commerciaux."
                    if language == "fr"
                    else
                    "تحدد هذه المادة التزامات تشغيلية أو مسؤوليات "
                    "صيانة أو التزامات تجارية."
                )

            if not analysis.get("recommendation"):
                analysis["recommendation"] = (
                    "Review the allocation of obligations and risk exposure in this clause."
                    if language == "en"
                    else
                    "Examiner attentivement la répartition des obligations et des risques dans cette clause."
                    if language == "fr"
                    else
                    "ينبغي مراجعة توزيع الالتزامات والمخاطر في هذه المادة بعناية."
                )
        high_risk_terms = [
            "unlimited liability",
            "acceleration",
            "immediate termination",
            "exclusive jurisdiction",
            "data breach",
            "security incident",
            "cross default",

            "responsabilité illimitée",
            "résiliation immédiate",
            "violation de données",

            "مسؤولية غير محدودة",
            "إنهاء فوري",
            "اختراق البيانات",
        ]

        if any(
            term in clause_type_text
            for term in high_risk_terms
        ):
            analysis["risk_level"] = "high"

        if (
            domain_reasoning_allowed
            and not analysis.get("legal_insight")
            and domain_reasoning.get("reasoning")
        ):
            analysis["legal_insight"] = (
                domain_reasoning["reasoning"]
            )

        meaningful_legal_signals = [
            "exclusive",
            "non-exclusive",
            "termination",
            "payment",
            "confidentiality",
            "liability",
            "distribution",
        ]


        analysis = compute_analysis_metadata(
            analysis,
            clause_text,
            title,
        )

        analysis = apply_reasoning_quality_gate(
            analysis,
            clause_text,
            language,
        )

        analysis = compute_analysis_metadata(
            analysis,
            clause_text,
            title,
        )

        results.append({
            "title": title,
            "original_text": clause[:1000],
            "reasoning_evidence": extract_reasoning_evidence(
                clause_text
            ),
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

    # Keep all deduplicated clauses.
    # Do not truncate results; sorting by importance_score is preserved.

    normalized_contract_score = normalize_importance_score(
        deduped
    )

    for item in deduped:
        item["normalized_contract_score"] = normalized_contract_score

    return deduped


class ClauseAnalysisPipeline:
    """
    Explicit orchestration wrapper for clause analysis.

    The heavy deterministic helpers remain pure functions, while this
    object makes the analysis entrypoint testable and easier to extend.
    """

    def __init__(
        self,
        clauses: list[str],
        language: str = "en",
        max_clauses: int = 25,
    ) -> None:
        self.clauses = clauses
        self.language = language
        self.max_clauses = max_clauses

    def run_detection(self) -> list[dict]:
        return _analyze_contract_clauses_impl(
            self.clauses,
            self.language,
            self.max_clauses,
        )

    def run_validation(self, results: list[dict]) -> list[dict]:
        return results

    def run_risk(self, results: list[dict]) -> list[dict]:
        return results

    def run_calibration(self, results: list[dict]) -> list[dict]:
        return results

    def run_negotiation(self, results: list[dict]) -> list[dict]:
        return results

    def run_scoring(self, results: list[dict]) -> list[dict]:
        return results

    def run_cleanup(self, results: list[dict]) -> list[dict]:
        return results

    def run(self) -> list[dict]:
        results = self.run_detection()
        results = self.run_validation(results)
        results = self.run_risk(results)
        results = self.run_calibration(results)
        results = self.run_negotiation(results)
        results = self.run_scoring(results)
        results = self.run_cleanup(results)

        return results


def analyze_contract_clauses(
    clauses: list[str],
    language: str = "en",
    max_clauses: int = 25,
) -> list[dict]:
    return ClauseAnalysisPipeline(
        clauses=clauses,
        language=language,
        max_clauses=max_clauses,
    ).run()

