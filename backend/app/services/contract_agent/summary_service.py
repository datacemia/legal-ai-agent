import logging
import re

from app.utils.prompt_loader import load_prompt
from app.services.contract_agent.ai_client import call_json_ai
from app.services.contract_agent.summary_normalizer import (
    get_not_specified,
    normalize_contract_summary,
    normalize_simplified_contract,
)
from app.services.contract_agent.party_role_detector import (
    get_display_roles,
    apply_display_roles,
    strip_role_articles,
    normalize_ai_role_words,
)
from app.services.contract_agent.validator import (
    validate_contract_result,
)


logger = logging.getLogger(__name__)


MAX_SUMMARY_CHARS = 12_000
MAX_SIMPLIFICATION_CHARS = 12_000


SUPPORTED_LANGUAGES = {"en", "fr", "ar"}


def normalize_language(language: str) -> str:
    language = str(language or "en").lower().strip()
    return language if language in SUPPORTED_LANGUAGES else "en"


ANONYMIZED_PLACEHOLDERS = {
    "[PERSON]",
    "[ORGANIZATION]",
    "[PARTY_1]",
    "[PARTY_2]",
    "[PARTY_3]",
    "[CLIENT]",
    "[SERVICE_PROVIDER]",
    "[SUPPLIER]",
    "[VENDOR]",
    "[BUYER]",
    "[SELLER]",
    "[LENDER]",
    "[BORROWER]",
    "[LESSOR]",
    "[LESSEE]",
    "[LICENSOR]",
    "[LICENSEE]",
    "[EMPLOYER]",
    "[EMPLOYEE]",
    "[CONTROLLER]",
    "[PROCESSOR]",
    "[FRANCHISOR]",
    "[FRANCHISEE]",
    "[DISTRIBUTOR]",
    "[RESELLER]",
}


def contains_anonymized_placeholder(value) -> bool:
    text = str(value or "")
    return any(token in text for token in ANONYMIZED_PLACEHOLDERS)


def party_roles_are_anonymized(party_roles: dict | None) -> bool:
    if not isinstance(party_roles, dict):
        return False

    if party_roles.get("anonymized") is True:
        return True

    return (
        contains_anonymized_placeholder(party_roles.get("party_a"))
        or contains_anonymized_placeholder(party_roles.get("party_b"))
    )


def safe_apply_display_roles(value, party_roles: dict | None, language: str = "en"):
    """
    Privacy-first role display.

    apply_display_roles() is allowed only when party_roles are confirmed
    anonymized. This prevents real party names or inferred role replacements
    from being injected back into summaries or prompts.
    """
    if not party_roles_are_anonymized(party_roles):
        return value

    try:
        return apply_display_roles(value, party_roles, language)
    except Exception:
        return value





def is_employment_contract_context(party_roles: dict | None = None) -> bool:
    """
    Contract-family guard used for international party-role safety.

    Employer/Employee labels are allowed only when the detected contract
    context is actually employment-related or when the detected party roles
    themselves explicitly contain employment roles.
    """
    if not isinstance(party_roles, dict):
        return False

    text = " ".join(
        str(party_roles.get(key) or "")
        for key in [
            "contract_family",
            "contract_type",
            "party_a",
            "party_b",
            "party_a_role",
            "party_b_role",
        ]
    ).lower()

    employment_terms = [
        "employment",
        "employee",
        "employer",
        "employment agreement",
        "employment contract",
        "contrat de travail",
        "contrat d'emploi",
        "emploi",
        "employeur",
        "salarié",
        "salarie",
        "عقد عمل",
        "صاحب العمل",
        "الموظف",
        "العامل",
    ]

    return any(term in text for term in employment_terms)


def build_party_registry_prompt(language: str, party_roles: dict | None = None) -> str:
    """
    Standard international party registry instruction.

    The LLM must not choose roles from a generic catalogue. It must use only
    the roles already detected for the contract. This works across domains
    and across EN / FR / AR because the business logic uses detected roles,
    not hard-coded role names.
    """
    language = normalize_language(language)

    if not isinstance(party_roles, dict):
        return """
PARTY REGISTRY RULES:
- Use only party roles or party labels that appear in the contract text.
- Never invent Employer, Employee, Buyer, Seller, Vendor, Supplier, Client, Provider, Customer, Controller, Processor, Lessor, Lessee, Licensor, Licensee, or any other role.
- If a role is unclear, use neutral labels: Party A / Party B in English, Partie A / Partie B in French, الطرف أ / الطرف ب in Arabic.
""".strip()

    party_a = str(
        party_roles.get("party_a")
        or party_roles.get("party_a_role")
        or ""
    ).strip()
    party_b = str(
        party_roles.get("party_b")
        or party_roles.get("party_b_role")
        or ""
    ).strip()
    contract_family = str(
        party_roles.get("contract_family")
        or party_roles.get("contract_type")
        or ""
    ).strip()

    lines = [
        "PARTY REGISTRY - STRICT:",
    ]

    if party_a:
        lines.append(f"- Party A role: {party_a}")
    if party_b:
        lines.append(f"- Party B role: {party_b}")
    if contract_family:
        lines.append(f"- Detected contract family/type: {contract_family}")

    if not party_a and not party_b:
        lines.append("- No reliable party role was detected; use neutral Party A / Party B labels only.")

    lines.extend([
        "",
        "MANDATORY PARTY RULES:",
        "1. Use only the roles listed in this Party Registry or neutral Party A / Party B labels.",
        "2. Never introduce Employer / Employee unless the Party Registry or the contract text explicitly shows an employment contract.",
        "3. Never introduce Buyer / Seller, Vendor / Supplier, Client / Provider, Customer, Controller / Processor, Lessor / Lessee, Licensor / Licensee, or any other role unless it appears in the Party Registry or the source contract.",
        "4. Do not translate or rewrite party roles into a different legal relationship.",
        "5. Every obligation must keep the same responsible party as the source clause.",
    ])

    return "\n".join(lines).strip()


def scrub_unsupported_employment_roles(value, language: str = "en", party_roles: dict | None = None):
    """
    Last-mile role-leakage guard.

    If a non-employment contract still contains Employer/Employee language,
    replace it with a neutral contractual-party label instead of guessing
    whether it means Party A or Party B. This avoids false role attribution
    across SaaS, MSA, NDA, lease, loan, franchise, procurement, IP, data,
    construction, insurance, and other contract families in EN / FR / AR.
    """
    language = normalize_language(language)

    if is_employment_contract_context(party_roles):
        return value

    neutral = {
        "en": "the relevant contractual party",
        "fr": "la partie contractuelle concernée",
        "ar": "الطرف التعاقدي المعني",
    }.get(language, "the relevant contractual party")

    if isinstance(value, list):
        return [
            scrub_unsupported_employment_roles(item, language, party_roles)
            for item in value
        ]

    if isinstance(value, dict):
        return {
            key: scrub_unsupported_employment_roles(item, language, party_roles)
            for key, item in value.items()
        }

    if not isinstance(value, str):
        return value

    output = value

    replacements = [
        (r"\bEmployers'\b", f"{neutral}'s"),
        (r"\bEmployer's\b", f"{neutral}'s"),
        (r"\bEmployer’s\b", f"{neutral}'s"),
        (r"\bEmployees'\b", f"{neutral}'s"),
        (r"\bEmployee's\b", f"{neutral}'s"),
        (r"\bEmployee’s\b", f"{neutral}'s"),
        (r"\bEmployers\b", neutral),
        (r"\bEmployer\b", neutral),
        (r"\bEmployees\b", neutral),
        (r"\bEmployee\b", neutral),
    ]

    for pattern, replacement in replacements:
        output = re.sub(pattern, replacement, output)

    fr_replacements = {
        "Employeur": neutral,
        "employeur": neutral,
        "Salarié": neutral,
        "salarié": neutral,
        "Salarie": neutral,
        "salarie": neutral,
    }

    ar_replacements = {
        "صاحب العمل": neutral,
        "الموظف": neutral,
        "الموظفين": neutral,
        "العامل": neutral,
    }

    for old, new in {**fr_replacements, **ar_replacements}.items():
        output = output.replace(old, new)

    return output


def ensure_ai_input_is_anonymized(contract_text: str) -> str:
    """
    Last-mile privacy guard.

    The main anonymization is expected upstream. This function does not try
    to reconstruct or classify real identities; it only reinforces that the
    prompt instructs the AI not to restore personal data.
    """
    return str(contract_text or "")




SUMMARY_SPECULATIVE_PATTERNS = [
    "risques significatifs",
    "significant risks",
    "major legal exposure",
    "dangerous contract",
    "highly risky",
    "serious legal risk",
    "critical legal concern",
]



def contains_arabic(text: str) -> bool:
    return any(
        "\u0600" <= char <= "\u06FF"
        for char in str(text or "")
    )


def contains_latin_letters(text: str) -> bool:
    return any(
        ("a" <= char.lower() <= "z")
        for char in str(text or "")
    )


def language_mismatch_score(
    value,
    language: str,
) -> int:
    """
    Lightweight multilingual consistency detector.

    This does not try to perfectly identify a language.
    It only detects obvious cross-language leakage:
    - Arabic text inside FR/EN generated fields
    - Latin-heavy text inside AR generated fields

    Names, dates, amounts, article references, and court names are
    allowed to remain as-is by the repair prompt.
    """

    if value is None:
        return 0

    if isinstance(value, list):
        return sum(
            language_mismatch_score(item, language)
            for item in value
        )

    if isinstance(value, dict):
        return sum(
            language_mismatch_score(item, language)
            for item in value.values()
        )

    text = str(value or "").strip()

    if not text:
        return 0

    if language in {"en", "fr"}:
        return 1 if contains_arabic(text) else 0

    if language == "ar":
        latin_letters = sum(
            1 for char in text
            if "a" <= char.lower() <= "z"
        )

        # Allow short legal references / acronyms / party names.
        return 1 if latin_letters >= 12 else 0

    return 0


def needs_language_repair(
    data: dict,
    language: str,
    fields: list[str],
) -> bool:
    for field in fields:
        if language_mismatch_score(
            data.get(field),
            language,
        ):
            return True

    return False


SUMMARY_LANGUAGE_FIELDS = [
    "contract_type",
    "duration",
    "payment_terms",
    "main_obligations",
    "global_summary",
    "important_points",
    "missing_clauses",
    "dangerous_patterns",
    "overall_balance",
    "negotiation_priorities",
    "key_risks",
    "practical_decision",
    "jurisdiction_detected",
    "jurisdiction_note",
    "recommended_actions",
]

SIMPLIFIED_LANGUAGE_FIELDS = [
    "simplified_version",
    "key_points",
    "things_to_watch",
]


def repair_summary_language(
    data: dict,
    language: str,
) -> dict:
    """
    Repair only language leakage in summary JSON values.

    This is intentionally narrow:
    - no new legal facts
    - no risk changes
    - no structure changes
    - no extra keys
    """

    if not needs_language_repair(
        data,
        language,
        SUMMARY_LANGUAGE_FIELDS,
    ):
        return data

    prompt = f"""
You are a strict multilingual legal JSON repair engine.

Output language: {language}

TASK:
Rewrite ONLY the JSON values so that all user-facing generated text is in the requested output language.

RULES:
- Return ONLY valid JSON.
- Keep the exact same keys.
- Do not add keys.
- Do not remove keys.
- Do not change the legal meaning.
- Do not invent facts.
- Do not add risks, obligations, clauses, warnings, or recommendations.
- Preserve anonymized party labels, dates, amounts, article references, addresses, court names, and legal identifiers.
- Never reconstruct, infer, restore, request, or output real names, emails, addresses, phone numbers, account numbers, IDs, or personal data.
- Translate surrounding explanatory text into the requested output language.
PARTY IDENTITY RULES:
- Preserve all party references exactly.
- Never shorten party references.
- Never replace a specific party reference with a generic word.
- Never rewrite "الطرف الأول" as "الطرف".
- Never rewrite "الطرف الثاني" as "الطرف".
- Every obligation must explicitly identify the responsible party.
- Mixed-language output is forbidden except for preserved legal identifiers.

JSON to repair:
{data}
""".strip()

    try:
        repaired = call_json_ai(prompt)

        if isinstance(repaired, dict):
            for key in data.keys():
                if key in repaired:
                    data[key] = repaired[key]

    except Exception as e:
        logger.debug("SUMMARY LANGUAGE REPAIR ERROR: %s", e)

    return data


def repair_simplified_language(
    data: dict,
    language: str,
) -> dict:
    """
    Repair only language leakage in simplified JSON values.
    """

    if not needs_language_repair(
        data,
        language,
        SIMPLIFIED_LANGUAGE_FIELDS,
    ):
        return data

    prompt = f"""
You are a strict multilingual legal JSON repair engine.

Output language: {language}

TASK:
Rewrite ONLY the JSON values so that all generated explanatory text is in the requested output language.

RULES:
- Return ONLY valid JSON.
- Keep exactly these keys: simplified_version, key_points, things_to_watch.
- Do not add keys.
- Do not remove keys.
- Do not change the legal meaning.
- Do not invent facts.
- Do not add risks, obligations, warnings, or recommendations.
- Preserve anonymized party labels, dates, amounts, article references, addresses, court names, and legal identifiers.
- Never reconstruct, infer, restore, request, or output real names, emails, addresses, phone numbers, account numbers, IDs, or personal data.
- Translate surrounding explanatory text into the requested output language.
PARTY IDENTITY RULES:
- Preserve all party references exactly.
- Never shorten party references.
- Never replace a specific party reference with a generic word.
- Never rewrite "الطرف الأول" as "الطرف".
- Never rewrite "الطرف الثاني" as "الطرف".
- Every obligation must explicitly identify the responsible party.
- Mixed-language output is forbidden except for preserved legal identifiers.

JSON to repair:
{data}
""".strip()

    try:
        repaired = call_json_ai(prompt)

        if isinstance(repaired, dict):
            for key in [
                "simplified_version",
                "key_points",
                "things_to_watch",
            ]:
                if key in repaired:
                    data[key] = repaired[key]

    except Exception as e:
        logger.debug("SIMPLIFIED LANGUAGE REPAIR ERROR: %s", e)

    return data


def extract_jurisdiction(text: str) -> dict:
    text_value = str(text or "")
    text_lower = text_value.lower()

    governing_law_patterns = [
        r"laws of the state of ([a-zA-Z\s]{2,40})(?:\.|,|;|\n)",
        r"governed by the laws of ([a-zA-Z\s]{2,40})(?:\.|,|;|\n)",
        r"governed under the laws of ([a-zA-Z\s]{2,40})(?:\.|,|;|\n)",
        r"laws of ([a-zA-Z\s]{2,40})(?:\.|,|;|\n)",

        r"régi par le droit de ([a-zA-ZÀ-ÿ\s]{2,40})(?:\.|,|;|\n)",
        r"régie par le droit de ([a-zA-ZÀ-ÿ\s]{2,40})(?:\.|,|;|\n)",
        r"droit de ([a-zA-ZÀ-ÿ\s]{2,40})(?:\.|,|;|\n)",
        r"lois de ([a-zA-ZÀ-ÿ\s]{2,40})(?:\.|,|;|\n)",

        r"يخضع.*?لقوانين\s+([^\.\n،,؛]{2,60})",
        r"القانون الواجب التطبيق.*?هو\s+([^\.\n،,؛]{2,60})",
        r"قوانين\s+([^\.\n،,؛]{2,60})",
    ]

    dispute_patterns = [
        r"arbitrated.*?in ([a-zA-Z\s,]{2,60})",
        r"resolved.*?in ([a-zA-Z\s,]{2,60})",
        r"courts of ([a-zA-Z\s,]{2,60})",
        r"exclusive jurisdiction.*?of ([a-zA-Z\s,]{2,60})",

        r"arbitrage.*?à ([a-zA-ZÀ-ÿ\s,]{2,60})",
        r"litiges.*?à ([a-zA-ZÀ-ÿ\s,]{2,60})",
        r"tribunaux de ([a-zA-ZÀ-ÿ\s,]{2,60})",
        r"juridiction exclusive.*?de ([a-zA-ZÀ-ÿ\s,]{2,60})",

        r"التحكيم.*?في\s+([^\.\n،,؛]{2,60})",
        r"النزاعات.*?في\s+([^\.\n،,؛]{2,60})",
        r"محاكم\s+([^\.\n،,؛]{2,60})",
    ]

    arbitration_centers = [
        "icc", "international chamber of commerce",
        "lcia", "siac", "diac", "aaa", "icdr",
        "cci", "chambre de commerce internationale",
        "محكمة التحكيم الدولية", "غرفة التجارة الدولية",
    ]

    governing_law = None
    dispute_location = None
    arbitration_center = None

    for pattern in governing_law_patterns:
        match = re.search(pattern, text_lower, flags=re.IGNORECASE)
        if match:
            candidate = match.group(1).strip(" .،,;؛").title()
            if 1 <= len(candidate.split()) <= 8:
                governing_law = candidate
                break

    for pattern in dispute_patterns:
        match = re.search(pattern, text_lower, flags=re.IGNORECASE)
        if match:
            candidate = match.group(1).strip(" .،,;؛").title()
            if 1 <= len(candidate.split()) <= 10:
                dispute_location = candidate
                break

    for center in arbitration_centers:
        if center.lower() in text_lower:
            arbitration_center = center.upper() if len(center) <= 5 else center
            break

    return {
        "governing_law": governing_law,
        "dispute_location": dispute_location,
        "arbitration_center": arbitration_center,
    }


def build_jurisdiction_note(
    governing_law,
    dispute_location,
    language,
    arbitration_center=None,
):
    language = normalize_language(language)
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

    if arbitration_center:
        if language == "fr":
            parts.append(
                f"Le contrat mentionne {arbitration_center} comme institution ou mécanisme d'arbitrage."
            )
        elif language == "ar":
            parts.append(
                f"يشير العقد إلى {arbitration_center} كجهة أو آلية للتحكيم."
            )
        else:
            parts.append(
                f"The contract references {arbitration_center} as an arbitration institution or mechanism."
            )

    return " ".join(parts)



def detect_balancing_protections(
    clauses: list[str],
) -> dict:

    text = "\n".join(str(c or "") for c in clauses).lower()

    protections = {
        "arbitration": False,
        "cure_period": False,
        "termination_compensation": False,
        "transition_support": False,
        "insurance": False,
        "liability_cap": False,
        "liability_carveouts": False,
        "notice_period": False,
        "mutuality": False,
        "audit_rights": False,
        "data_security_controls": False,
    }

    pattern_groups = {
        "arbitration": ["arbitration", "arbitrage", "تحكيم"],
        "cure_period": [
            "cure within", "period to cure", "diligently pursue a cure",
            "cure period", "remedy period", "délai de correction",
            "délai de régularisation", "مهلة لتصحيح", "مهلة معالجة",
        ],
        "termination_compensation": [
            "termination payment", "termination compensation", "transition payment",
            "severance", "lump sum", "salary continuation",
            "indemnité", "indemnité de résiliation", "تعويض الإنهاء", "تعويض",
        ],
        "transition_support": [
            "transition assistance", "handover", "migration assistance",
            "return of data", "return or destruction", "assistance de transition",
            "restitution", "remise", "مساعدة انتقالية", "إرجاع البيانات",
        ],
        "insurance": [
            "liability insurance", "insured", "insurance coverage",
            "assurance responsabilité", "couverture d'assurance", "تأمين",
        ],
        "liability_cap": [
            "liability cap", "limited to", "aggregate liability",
            "plafond de responsabilité", "responsabilité est limitée",
            "حد المسؤولية", "تقتصر المسؤولية",
        ],
        "liability_carveouts": [
            "except as provided", "notwithstanding", "does not include",
            "excluding", "carve-out", "sauf", "nonobstant", "ne comprend pas",
            "لا يشمل", "باستثناء", "مع عدم الإخلال",
        ],
        "notice_period": [
            "notice period", "written notice", "prior notice",
            "préavis", "avis écrit", "إشعار", "إخطار مسبق",
        ],
        "mutuality": [
            "either party", "both parties", "mutual", "reciprocal",
            "chaque partie", "les deux parties", "réciproque",
            "أي من الطرفين", "كلا الطرفين", "متبادل",
        ],
        "audit_rights": [
            "audit right", "inspection right", "access to records",
            "droit d'audit", "droit d'inspection", "حق التدقيق", "حق التفتيش",
        ],
        "data_security_controls": [
            "security measures", "technical and organizational measures",
            "encryption", "access controls", "mesures de sécurité",
            "mesures techniques et organisationnelles", "تدابير أمنية", "التشفير",
        ],
    }

    for key, patterns in pattern_groups.items():
        protections[key] = any(pattern in text for pattern in patterns)

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

    text = str(full_text or "").lower()

    protective_termination_terms = [
        "constructive termination",
        "termination compensation",
        "transition payment",
        "lump sum",
        "fully vested",
        "compensation",
        "cure period",
        "notice period",
        "indemnité",
        "délai de régularisation",
        "préavis",
        "تعويض",
        "مهلة معالجة",
        "إشعار",
    ]

    if any(term in text for term in protective_termination_terms):
        data["dangerous_patterns"] = [
            item
            for item in data.get("dangerous_patterns", [])
            if "constructive termination" not in str(item).lower()
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


def generate_summary_data(text: str, language: str = "en", party_roles: dict | None = None) -> dict:
    language = normalize_language(language)
    """
    New structured summary function.

    Returns a clean dict that can later be rendered by the frontend.
    generate_summary() below still returns text for backward compatibility.
    """

    if not text or not text.strip():
        return build_empty_summary(language)

    prompt_template = load_prompt("summary_prompt.txt")
    contract_text = ensure_ai_input_is_anonymized(text[:MAX_SUMMARY_CHARS])
    party_registry_block = build_party_registry_prompt(language, party_roles)

    prompt = f"""
{prompt_template}

Output language: {language}

{party_registry_block}

SUMMARY PURPOSE:

Produce a structured legal summary suitable for lawyers, business users,
and contract reviewers.

Requirements:
- Summarize the contract objectively.
- Identify the principal obligations of each party.
- Summarize important commercial terms.
- Mention the principal legal risks.
- Mention missing or ambiguous clauses when relevant.
- Provide practical negotiation priorities.
- Do not repeat the Executive Narrative.
- Do not explain the contract in simplified language.
- Do not produce marketing language.

CRITICAL:
Translate every generated JSON value into this output language.
The contract source language may be different.
Do not copy source-language sentences into generated fields.
Preserve anonymized party identities exactly as provided.

Anonymized entities may include:

[PERSON]
[ORGANIZATION]
[PARTY_1]
[PARTY_2]
[PARTY_3]

These labels represent legal parties.

Do not reconstruct, infer, restore, request, or replace real names or personal data.

If rights, ownership, payments,
confidentiality obligations,
termination rights,
intellectual property rights,
or liabilities belong to an anonymized party,
preserve the recipient exactly as written.

Never transfer a right or obligation
from one anonymized party to another.
Dates, amounts, article references, and court names must remain accurate.

LANGUAGE CONSISTENCY ENFORCEMENT:
Before returning JSON, verify every generated value.
For output language "fr", generated values must be in French.
For output language "en", generated values must be in English.
For output language "ar", generated values must be in Arabic.
Do not copy source-language sentences into generated fields.
Clause titles, contract type, duration, payment terms, obligations, summaries, risks, and practical decision must be translated into the requested output language.
Mixed-language explanatory output is forbidden.

Contract text:
{contract_text}
""".strip()

    try:
        data = call_json_ai(prompt)
    except Exception as e:
        logger.debug("SUMMARY AI ERROR: %s", e)
        return build_empty_summary(language)

    data = repair_summary_language(
        data,
        language,
    )

    if party_roles:
        data = normalize_ai_role_words(
            data,
            party_roles,
            language,
        )

    data = scrub_unsupported_employment_roles(data, language, party_roles)

    if language == "ar":
        data["main_obligations"] = [
            item
            .replace("يلتزم الطرف بتقديم", "يلتزم الطرف ب بتقديم")
            .replace("يلتزم الطرف بالحفاظ", "يلتزم الطرف ب بالحفاظ")
            for item in data.get("main_obligations", [])
        ]
   

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
            jurisdiction_data.get("arbitration_center"),
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
            jurisdiction_data.get("arbitration_center"),
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

    data = display_safe_party_labels(data, language, party_roles)
    data = force_generic_parties(data, language, party_roles)
    data = scrub_unsupported_employment_roles(data, language, party_roles)
    data = normalize_contract_summary(data, language)

    if party_roles:
        data = normalize_ai_role_words(
            data,
            party_roles,
            language,
        )

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

    if party_roles:
        data = safe_apply_display_roles(data, party_roles, language)
        data = normalize_ai_role_words(
            data,
            party_roles,
            language,
        )

    data = scrub_unsupported_employment_roles(data, language, party_roles)

    quality_check = validate_contract_result(data)

    data["quality_check"] = quality_check

    return data


def display_safe_party_labels(value, language: str = "en", party_roles: dict | None = None):
    """
    Security-safe party display.

    International rule:
    - Preserve real contractual roles when they are already generic/legal roles:
      Client, Supplier, Provider, Buyer, Seller, Lender, Borrower, Lessor,
      Lessee, Licensor, Licensee, Employer, Employee, etc.
    - Replace only anonymized placeholders such as [PARTY_1], [PARTY_2],
      [ORGANIZATION], [PERSON].
    - Do not reconstruct real names.
    - Do not force every contract into Party A / Party B unless the source
      itself is anonymized.
    """

    language = normalize_language(language)

    role_party_a = None
    role_party_b = None
    if isinstance(party_roles, dict):
        role_party_a = str(party_roles.get("party_a") or "").strip() or None
        role_party_b = str(party_roles.get("party_b") or "").strip() or None

    labels = {
        "en": {
            "[PARTY_1]": "Contracting Party A",
            "[PARTY_2]": "Contracting Party B",
            "[PARTY_3]": "Contracting Party C",
            "[ORGANIZATION]": "Organization",
            "[PERSON]": "Person",
            "[COMPANY]": "Company",
            "[CLIENT]": "Client",
            "[SERVICE_PROVIDER]": "Service Provider",
            "[SUPPLIER]": "Supplier",
            "[VENDOR]": "Vendor",
            "[BUYER]": "Buyer",
            "[SELLER]": "Seller",
            "[LENDER]": "Lender",
            "[BORROWER]": "Borrower",
            "[LESSOR]": "Lessor",
            "[LESSEE]": "Lessee",
            "[LICENSOR]": "Licensor",
            "[LICENSEE]": "Licensee",
            "[EMPLOYER]": "Employer",
            "[EMPLOYEE]": "Employee",
        },
        "fr": {
            "[PARTY_1]": "Partie contractante A",
            "[PARTY_2]": "Partie contractante B",
            "[PARTY_3]": "Partie contractante C",
            "[ORGANIZATION]": "Organisation",
            "[PERSON]": "Personne",
            "[COMPANY]": "Société",
            "[CLIENT]": "Client",
            "[SERVICE_PROVIDER]": "Prestataire",
            "[SUPPLIER]": "Fournisseur",
            "[VENDOR]": "Fournisseur",
            "[BUYER]": "Acheteur",
            "[SELLER]": "Vendeur",
            "[LENDER]": "Prêteur",
            "[BORROWER]": "Emprunteur",
            "[LESSOR]": "Bailleur",
            "[LESSEE]": "Locataire",
            "[LICENSOR]": "Concédant",
            "[LICENSEE]": "Licencié",
            "[EMPLOYER]": "Employeur",
            "[EMPLOYEE]": "Salarié",
        },
        "ar": {
            "[PARTY_1]": "الطرف أ",
            "[PARTY_2]": "الطرف ب",
            "[PARTY_3]": "الطرف ج",
            "[ORGANIZATION]": "المنظمة",
            "[PERSON]": "الشخص",
            "[COMPANY]": "الشركة",
            "[CLIENT]": "العميل",
            "[SERVICE_PROVIDER]": "مقدم الخدمة",
            "[SUPPLIER]": "المورّد",
            "[VENDOR]": "المورّد",
            "[BUYER]": "المشتري",
            "[SELLER]": "البائع",
            "[LENDER]": "المقرض",
            "[BORROWER]": "المقترض",
            "[LESSOR]": "المؤجر",
            "[LESSEE]": "المستأجر",
            "[LICENSOR]": "المرخِّص",
            "[LICENSEE]": "المرخَّص له",
            "[EMPLOYER]": "صاحب العمل",
            "[EMPLOYEE]": "الموظف",
        },
    }

    mapping = dict(labels.get(language, labels["en"]))

    if role_party_a:
        mapping["[PARTY_1]"] = role_party_a
        mapping["[PARTY_A]"] = role_party_a
    if role_party_b:
        mapping["[PARTY_2]"] = role_party_b
        mapping["[PARTY_B]"] = role_party_b

    # International safety rule:
    # Employer / Employee are not generic placeholders. They are valid only
    # for real employment contracts. For all other contract families, avoid
    # displaying employment labels because they create false legal roles.
    if not is_employment_contract_context(party_roles):
        neutral_party = {
            "en": "the relevant contractual party",
            "fr": "la partie contractuelle concernée",
            "ar": "الطرف التعاقدي المعني",
        }.get(language, "the relevant contractual party")
        mapping["[EMPLOYER]"] = neutral_party
        mapping["[EMPLOYEE]"] = neutral_party

    if isinstance(value, list):
        return [display_safe_party_labels(item, language, party_roles) for item in value]

    if isinstance(value, dict):
        return {
            key: display_safe_party_labels(item, language, party_roles)
            for key, item in value.items()
        }

    if not isinstance(value, str):
        return value

    output = value

    for old, new in mapping.items():
        output = output.replace(old, new)

    if language == "ar":
        cleanup = {
            "الطرف الطرف أ": "الطرف أ",
            "الطرف الطرف ب": "الطرف ب",
            "الطرف الطرف ج": "الطرف ج",
        }

        for old, new in cleanup.items():
            output = output.replace(old, new)

    return output



def force_generic_parties(data: dict, language: str, party_roles: dict | None = None) -> dict:
    """
    Preserve security without destroying contract roles.

    Use Party A / Party B only when the party list is anonymized or generic.
    Never replace explicit legal roles such as Client, Provider, Buyer, Seller,
    Lender, Borrower, Lessor, Lessee, Licensor, Licensee, Employer, Employee,
    Supplier, Vendor, Contractor, Consultant, Distributor, Franchisee, etc.
    """

    language = normalize_language(language)

    # If the caller already detected contract-family roles such as
    # Client / Service Provider, Buyer / Seller, etc., never force the
    # summary back to Contracting Party A / B.
    if isinstance(party_roles, dict):
        detected_a = str(party_roles.get("party_a") or "").strip()
        detected_b = str(party_roles.get("party_b") or "").strip()
        if detected_a and detected_b:
            parties = data.get("parties")

            # The LLM sometimes produces no "parties" key at all (not
            # even a placeholder list) -- confirmed real case. Treat
            # this the same as a placeholder-only list: use the
            # already-known, reliable party_roles labels rather than
            # leaving the field empty/absent.
            if not isinstance(parties, list) or not parties:
                data["parties"] = [detected_a, detected_b]
                return data

            if isinstance(parties, list):
                joined = " ".join(str(p) for p in parties).lower()
                generic_markers = [
                    "contracting party a", "contracting party b",
                    "partie contractante a", "partie contractante b",
                    "الطرف أ", "الطرف ب",
                    "[party_1]", "[party_2]",
                    # "Not specified" (and its FR/AR equivalents) is the
                    # actual placeholder text the LLM produces for a
                    # party it could not resolve -- confirmed real case.
                    # Without recognizing it here, this fast-path (which
                    # runs whenever party_roles IS available, i.e. the
                    # common case) silently returned early without ever
                    # replacing it, even though a reliable, already-
                    # detected label (party_a/party_b) was sitting right
                    # there unused.
                    "not specified", "non spécifié", "non specifie",
                    "غير محدد",
                    # The LLM commonly produces a bare, generic noun like
                    # "Company" instead of "Not specified" or a bracketed
                    # placeholder -- confirmed via direct debug trace on a
                    # real contract. "Company" is a generic structural
                    # term (the kind that survives PII redaction, e.g.
                    # from '(the "Company")' in the source text), not a
                    # specific role or an identifying name, yet it was
                    # previously invisible to this fast-path. Left
                    # unrecognized here, it fell through unchanged to
                    # normalize_parties() downstream, which rejects it
                    # (it is not in that function's own safe-role
                    # whitelist) and replaces it with "Not specified" --
                    # destroying information that was actually
                    # recoverable right here, using the already-known,
                    # reliable party_roles labels. Covers the equivalent
                    # generic organizational nouns in all three
                    # languages, not just "company" specifically.
                    "company", "société", "societe", "entreprise",
                    "الشركة", "المؤسسة",
                ]
                if any(marker in joined for marker in generic_markers):
                    data["parties"] = [detected_a, detected_b]
            return data

    generic_labels = {
        "en": ["Contracting Party A", "Contracting Party B"],
        "fr": ["Partie contractante A", "Partie contractante B"],
        "ar": ["الطرف أ", "الطرف ب"],
    }

    parties = data.get("parties")

    if not isinstance(parties, list):
        return data

    if len(parties) < 2:
        return data

    role_terms = {
        "client", "customer", "provider", "service provider", "supplier",
        "vendor", "buyer", "seller", "lender", "borrower", "lessor",
        "lessee", "licensor", "licensee", "employer", "employee",
        "contractor", "consultant", "distributor", "franchisee",
        "franchisor", "controller", "processor",

        "client", "prestataire", "fournisseur", "acheteur", "vendeur",
        "prêteur", "preteur", "emprunteur", "bailleur", "locataire",
        "concédant", "concedant", "licencié", "licencie", "employeur",
        "salarié", "salarie", "entrepreneur", "consultant",
        "distributeur", "franchisé", "franchise",

        "العميل", "مقدم الخدمة", "المورّد", "المورد", "المشتري",
        "البائع", "المقرض", "المقترض", "المؤجر", "المستأجر",
        "المرخِّص", "المرخص", "المرخَّص له", "صاحب العمل",
        "الموظف", "المقاول", "المستشار", "الموزع",
    }

    joined = " ".join(str(p) for p in parties).lower()

    has_explicit_role = any(
        role in joined
        for role in role_terms
    )

    if has_explicit_role:
        return data

    anonymized_tokens = [
        "[PARTY_1]",
        "[PARTY_2]",
        "[PARTY_3]",
        "[ORGANIZATION]",
        "[PERSON]",
        "contracting party a",
        "contracting party b",
        "partie contractante a",
        "partie contractante b",
        "الطرف أ",
        "الطرف ب",
        "الطرف ج",
        "not specified",
        "non spécifié",
        "non specifie",
        "غير محدد",
        "company",
        "société",
        "societe",
        "entreprise",
        "الشركة",
        "المؤسسة",
    ]

    anonymized_or_generic = any(
        token.lower() in joined
        for token in anonymized_tokens
    )

    if anonymized_or_generic:
        data["parties"] = generic_labels.get(language, generic_labels["en"])[:2]

    return data



def render_summary_text(data: dict, language: str = "en", party_roles: dict | None = None) -> str:
    language = normalize_language(language)
    """
    Backward-compatible text renderer.

    Keep this while your frontend still expects a formatted string.
    Later, your frontend should render generate_summary_data() directly.
    """

    t = get_labels(language)

    if party_roles:
        data = normalize_ai_role_words(
            data,
            party_roles,
            language,
        )

    data = display_safe_party_labels(data, language, party_roles)
    data = scrub_unsupported_employment_roles(data, language, party_roles)

    if party_roles:
        data = safe_apply_display_roles(data, party_roles, language)
        data = normalize_ai_role_words(
            data,
            party_roles,
            language,
        )
    elif language != "ar":
        roles = get_display_roles(
            contract_type=data.get("contract_type", ""),
            text=data.get("global_summary", ""),
            language=language,
        )
        data = safe_apply_display_roles(data, roles, language)

    output = ""
    output += f"{t['type']}: {data['contract_type']}\n"
    if language == "ar":
        display_parties = data["parties"]
    else:
        display_parties = [
            strip_role_articles(p, language)
            for p in data["parties"]
        ]

    output += f"{t['parties']}: {', '.join(display_parties)}\n"
    output += f"{t['duration']}: {data['duration']}\n"
    output += f"{t['payment']}: {data['payment_terms']}\n\n"

    global_summary = str(data.get("global_summary") or "").strip()
    global_summary_lower = global_summary.lower()

    executive_like_markers = [
        "this contract contains",
        "ce contrat présente",
        "يتضمن هذا العقد",
        "the most sensitive clauses",
        "les clauses les plus sensibles",
        "تتركز البنود الأكثر حساسية",
    ]

    if global_summary and not any(
        marker in global_summary_lower for marker in executive_like_markers
    ):
        output += f"{t['summary']}:\n{global_summary}\n\n"
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


def generate_summary(text: str, language: str = "en", party_roles: dict | None = None) -> str:
    language = normalize_language(language)
    """
    Backward-compatible function.

    Your current app can keep calling this and receiving a string.
    """

    data = generate_summary_data(text, language, party_roles)
    return render_summary_text(data, language, party_roles)


def build_empty_simplified(language: str = "en") -> dict:
    language = normalize_language(language)
    ns = get_not_specified(language)

    return normalize_simplified_contract(
        {
            "simplified_version": ns,
            "key_points": [],
            "things_to_watch": [],
        },
        language,
    )


def generate_simplified_version_data(text: str, language: str = "en", party_roles: dict | None = None) -> dict:
    language = normalize_language(language)
    """
    Structured simplification result.
    """

    if not text or not text.strip():
        return build_empty_simplified(language)

    prompt_template = load_prompt("simplification_prompt.txt")
    contract_text = ensure_ai_input_is_anonymized(text[:MAX_SIMPLIFICATION_CHARS])
    party_registry_block = build_party_registry_prompt(language, party_roles)

    prompt = f"""
{prompt_template}

Output language: {language}

{party_registry_block}

SIMPLIFIED VERSION PURPOSE:
Explain the contract in plain language for a non-lawyer.

The simplified version must be different from the executive narrative and from the legal summary.

Rules:
- Use short, simple sentences.
- Avoid legal jargon.
- Explain what the contract is about.
- Explain what each party mainly has to do.
- Explain the most practical consequences.
- Mention only the most important risks in everyday language.
- Do not repeat risk counts.
- Do not mention internal scoring, clause relationships, graphs or technical analysis.

CRITICAL:
Translate every generated JSON value into this output language.
The contract source language may be different.
Do not copy source-language sentences into generated fields.
Preserve anonymized party identities exactly as provided.

Anonymized entities may include:

[PERSON]
[ORGANIZATION]
[PARTY_1]
[PARTY_2]
[PARTY_3]

These labels represent legal parties.

Do not reconstruct, infer, restore, request, or replace real names or personal data.

If rights, ownership, payments,
confidentiality obligations,
termination rights,
intellectual property rights,
or liabilities belong to an anonymized party,
preserve the recipient exactly as written.

Never transfer a right or obligation
from one anonymized party to another.
Dates, amounts, article references, and court names must remain accurate.

LANGUAGE CONSISTENCY ENFORCEMENT:
Before returning JSON, verify every generated value.
For output language "fr", generated values must be in French.
For output language "en", generated values must be in English.
For output language "ar", generated values must be in Arabic.
Do not copy source-language sentences into generated fields.
Clause titles, contract type, duration, payment terms, obligations, summaries, risks, and practical decision must be translated into the requested output language.
Mixed-language explanatory output is forbidden.

Contract text:
{contract_text}
""".strip()

    try:
        data = call_json_ai(prompt)
    except Exception as e:
        logger.debug("SIMPLIFICATION AI ERROR: %s", e)
        return build_empty_simplified(language)

    data = repair_simplified_language(
        data,
        language,
    )

    if party_roles:
        data = normalize_ai_role_words(
            data,
            party_roles,
            language,
        )

    data = display_safe_party_labels(data, language, party_roles)
    data = scrub_unsupported_employment_roles(data, language, party_roles)

    if party_roles:
        data = safe_apply_display_roles(data, party_roles, language)
        data = normalize_ai_role_words(
            data,
            party_roles,
            language,
        )

    if party_roles:
        data = normalize_ai_role_words(
            data,
            party_roles,
            language,
        )

    return normalize_simplified_contract(data, language)


def render_simplified_text(data: dict, language: str = "en", party_roles: dict | None = None) -> str:
    language = normalize_language(language)
    t = get_labels(language)

    if party_roles:
        data = normalize_ai_role_words(
            data,
            party_roles,
            language,
        )

    data = display_safe_party_labels(data, language, party_roles)
    data = scrub_unsupported_employment_roles(data, language, party_roles)

    if party_roles:
        data = safe_apply_display_roles(data, party_roles, language)
        data = normalize_ai_role_words(
            data,
            party_roles,
            language,
        )
    elif language != "ar":
        roles = get_display_roles(
            contract_type=data.get("contract_type", ""),
            text=data.get("simplified_version", ""),
            language=language,
        )
        data = safe_apply_display_roles(data, roles, language)

    output = data.get("simplified_version", "")

    # key_points intentionally hidden in simplified rendering.

    if data.get("things_to_watch"):
        output += f"\n\n{t['things_to_watch']}:\n"
        output += "\n".join([f"- {item}" for item in data["things_to_watch"]])

    return output.strip()


def generate_simplified_version(text: str, language: str = "en", party_roles: dict | None = None) -> str:
    language = normalize_language(language)
    """
    Backward-compatible function.

    Your current app can keep calling this and receiving a string.
    """

    data = generate_simplified_version_data(text, language, party_roles)
    return render_simplified_text(data, language, party_roles)


def calculate_global_risk(clause_results):
    if isinstance(clause_results, dict):
        if isinstance(clause_results.get("results"), list):
            clause_results = clause_results["results"]
        elif (
            isinstance(clause_results.get("clauses"), dict)
            and isinstance(clause_results["clauses"].get("results"), list)
        ):
            clause_results = clause_results["clauses"]["results"]
        else:
            clause_results = []

    if not isinstance(clause_results, list):
        clause_results = []

    clause_results = [
        item
        for item in clause_results
        if isinstance(item, dict)
    ]

    total = len(clause_results)

    if total <= 0:
        return {
            "risk_level": "low",
            "risk_score": 20,
        }

    high_count = sum(
        1
        for item in clause_results
        if str(item.get("risk_level", "")).lower() == "high"
    )

    medium_count = sum(
        1
        for item in clause_results
        if str(item.get("risk_level", "")).lower() == "medium"
    )

    low_count = sum(
        1
        for item in clause_results
        if str(item.get("risk_level", "")).lower() == "low"
    )

    material_high = 0

    material_markers = [
        "unlimited",
        "uncapped",
        "without notice",
        "unilateral",
        "all rights",
        "any and all rights",
        "liquidated damages",
        "responsabilité illimitée",
        "sans préavis",
        "غير محدودة",
        "دون إشعار",
    ]

    for item in clause_results:
        if str(item.get("risk_level", "")).lower() != "high":
            continue

        text_blob = " ".join([
            str(item.get("title", "")),
            str(item.get("clause_title", "")),
            str(item.get("quoted_text", "")),
            str(item.get("original_text", "")),
            str(item.get("legal_insight", "")),
            str(item.get("risk_explanation", "")),
        ]).lower()

        if any(marker in text_blob for marker in material_markers):
            material_high += 1

    base_score = 20
    base_score += min(45, material_high * 18)
    base_score += min(25, max(0, high_count - material_high) * 8)
    base_score += min(25, medium_count * 4)

    risk_ratio = (high_count * 2 + medium_count) / max(total, 1)

    if risk_ratio < 0.25 and base_score > 55:
        base_score = 55

    if risk_ratio >= 0.5:
        base_score += 10

    risk_score = max(0, min(int(base_score), 100))

    if risk_score >= 70:
        risk_level = "high"
    elif risk_score >= 40:
        risk_level = "medium"
    else:
        risk_level = "low"

    return {
        "risk_level": risk_level,
        "risk_score": risk_score,
        "risk_breakdown": {
            "total_clauses": total,
            "high": high_count,
            "medium": medium_count,
            "low": low_count,
            "material_high": material_high,
        },
    }
