from typing import Any

from app.services.contract_agent.schemas import ContractSummary, SimplifiedContract


def get_not_specified(language: str) -> str:
    if language == "fr":
        return "Non spécifié"
    if language == "ar":
        return "غير محدد"
    return "Not specified"


def normalize_missing_value(value: Any, language: str) -> str:
    missing = {
        "",
        "not specified",
        "non spécifié",
        "غير محدد",
        "undefined",
        "unknown",
        "none",
        "null",
    }

    if value is None:
        return get_not_specified(language)

    value = str(value).strip()

    if value.lower() in missing:
        return get_not_specified(language)

    return value


def normalize_list(value: Any) -> list[str]:
    if not value:
        return []

    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]

    return [str(value).strip()]


def clamp_score(score: Any) -> int:
    try:
        score = int(score)
    except Exception:
        return 50

    return max(0, min(score, 100))


def normalize_complexity(value: Any) -> str:
    value = str(value or "").lower().strip()

    if value in {"low", "medium", "high"}:
        return value

    if value in {"faible", "منخفض"}:
        return "low"

    if value in {"moyenne", "متوسط"}:
        return "medium"

    if value in {"élevée", "elevee", "مرتفع"}:
        return "high"

    return "medium"


def translate_balance(value: Any, language: str) -> str:
    value = normalize_missing_value(value, language)
    normalized = value.lower().strip()

    mappings = {
        "balanced": {
            "en": "Balanced",
            "fr": "Équilibré",
            "ar": "متوازن",
        },
        "slightly employer-friendly": {
            "en": "Slightly Employer-Friendly",
            "fr": "Légèrement favorable à l’employeur",
            "ar": "يميل قليلاً لصالح صاحب العمل",
        },
        "employer-friendly": {
            "en": "Employer-Friendly",
            "fr": "Favorable à l’employeur",
            "ar": "لصالح صاحب العمل",
        },
        "employee-friendly": {
            "en": "Employee-Friendly",
            "fr": "Favorable للموظف",
            "ar": "لصالح الموظف",
        },
        "client-friendly": {
            "en": "Client-Friendly",
            "fr": "Favorable au client",
            "ar": "لصالح العميل",
        },
        "vendor-friendly": {
            "en": "Vendor-Friendly",
            "fr": "Favorable au fournisseur",
            "ar": "لصالح المورّد",
        },
    }

    if normalized in mappings:
        return mappings[normalized].get(language, mappings[normalized]["en"])

    return value


def normalize_contract_summary(data: dict, language: str = "en") -> dict:
    not_specified = get_not_specified(language)

    raw = {
        "contract_type": normalize_missing_value(data.get("contract_type"), language),
        "parties": normalize_list(data.get("parties")) or [not_specified],
        "duration": normalize_missing_value(data.get("duration"), language),
        "payment_terms": normalize_missing_value(data.get("payment_terms"), language),
        "main_obligations": normalize_list(data.get("main_obligations")),
        "global_summary": normalize_missing_value(data.get("global_summary"), language),
        "important_points": normalize_list(data.get("important_points")),
        "missing_clauses": normalize_list(data.get("missing_clauses")),
        "dangerous_patterns": normalize_list(data.get("dangerous_patterns")),
        "contract_score": clamp_score(data.get("contract_score")),
        "overall_balance": translate_balance(data.get("overall_balance"), language),
        "negotiation_priorities": normalize_list(data.get("negotiation_priorities")),
        "key_risks": normalize_list(data.get("key_risks")),
        "practical_decision": normalize_missing_value(data.get("practical_decision"), language),
        "jurisdiction_detected": normalize_missing_value(data.get("jurisdiction_detected"), language),
        "jurisdiction_note": normalize_missing_value(data.get("jurisdiction_note"), language),
        "recommended_actions": normalize_list(data.get("recommended_actions")),
        "contract_complexity": normalize_complexity(data.get("contract_complexity")),
    }

    validated = ContractSummary(**raw)
    return validated.model_dump()


def normalize_simplified_contract(data: dict, language: str = "en") -> dict:
    raw = {
        "simplified_version": normalize_missing_value(data.get("simplified_version"), language),
        "key_points": normalize_list(data.get("key_points")),
        "things_to_watch": normalize_list(data.get("things_to_watch")),
    }

    validated = SimplifiedContract(**raw)
    return validated.model_dump()
