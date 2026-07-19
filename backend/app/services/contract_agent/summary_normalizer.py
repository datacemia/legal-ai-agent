from typing import Any

from app.services.contract_agent.schemas import ContractSummary, SimplifiedContract


SUPPORTED_LANGUAGES = {
    "en",
    "fr",
    "ar",
}


MISSING_VALUES = {
    "",
    "not specified",
    "non spécifié",
    "غير محدد",
    "undefined",
    "unknown",
    "none",
    "null",
    "n/a",
    "na",
    "not applicable",
    "non applicable",
    "غير منطبق",
}


def normalize_language(language: str) -> str:
    language = str(language or "en").lower().strip()

    if language in SUPPORTED_LANGUAGES:
        return language

    return "en"


def get_not_specified(language: str) -> str:
    language = normalize_language(language)

    if language == "fr":
        return "Non spécifié"

    if language == "ar":
        return "غير محدد"

    return "Not specified"


def normalize_missing_value(
    value: Any,
    language: str,
) -> str:
    language = normalize_language(language)

    if value is None:
        return get_not_specified(language)

    value = str(value).strip()

    if value.lower() in MISSING_VALUES:
        return get_not_specified(language)

    return value


def normalize_list(
    value: Any,
    language: str,
) -> list[str]:
    language = normalize_language(language)

    if not value:
        return []

    items = value if isinstance(value, list) else [value]

    cleaned: list[str] = []
    seen = set()

    for item in items:
        item_str = str(item).strip()

        if not item_str:
            continue

        if item_str.lower() in MISSING_VALUES:
            continue

        dedupe_key = item_str.casefold()

        if dedupe_key in seen:
            continue

        seen.add(dedupe_key)
        cleaned.append(item_str)

    return cleaned


PRIVACY_PLACEHOLDER_PREFIXES = (
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
    "[EMPLOYER]",
    "[EMPLOYEE]",
    "[LESSOR]",
    "[LESSEE]",
    "[LENDER]",
    "[BORROWER]",
    "[LICENSOR]",
    "[LICENSEE]",
    "[CONTROLLER]",
    "[PROCESSOR]",
)


def looks_like_privacy_placeholder(value: Any) -> bool:
    text = str(value or "").strip()
    return any(token in text for token in PRIVACY_PLACEHOLDER_PREFIXES)


def normalize_parties(
    value: Any,
    language: str,
) -> list[str]:
    """
    Privacy-first party normalization.

    The upstream pipeline should anonymize parties before AI processing.
    This function preserves anonymized placeholders and rejects obviously
    unsafe free-form personal-looking party values only when no anonymized
    placeholder is present.

    It does not try to reconstruct or infer real identities.
    """
    language = normalize_language(language)
    parties = normalize_list(value, language)

    if not parties:
        return []

    safe = []

    for party in parties:
        if looks_like_privacy_placeholder(party):
            safe.append(party)
            continue

        # Keep generic role labels and legal placeholders. Avoid aggressive
        # name detection to prevent damaging legitimate anonymized labels.
        lowered = party.lower().strip()

        generic_allowed = {
            "party a", "party b",
            "partie a", "partie b",
            "الطرف أ", "الطرف ب",
            "client", "service provider", "supplier", "vendor",
            "buyer", "seller", "employer", "employee",
            "lessor", "lessee", "lender", "borrower",
            "licensor", "licensee", "controller", "processor",
            # Generic organizational nouns that commonly survive PII
            # redaction (e.g. from '(the "Company")' in the source
            # text) are not identifying information -- they should be
            # preserved the same way the specific role terms above are,
            # rather than being rejected as "unsafe free-form" text and
            # replaced with a placeholder. Confirmed real case via
            # direct debug trace on a real contract.
            "company", "société", "societe", "entreprise",
            "الشركة", "المؤسسة",
        }

        if lowered in generic_allowed:
            safe.append(party)
            continue

        # If upstream failed to anonymize, avoid propagating potentially
        # identifying party names in normalized output.
        safe.append(get_not_specified(language))

    return list(dict.fromkeys(safe))


def clamp_score(score: Any) -> int:
    try:
        score = int(score)
    except Exception:
        return 50

    return max(
        0,
        min(score, 100),
    )


def normalize_complexity(value: Any) -> str:
    value = str(value or "").lower().strip()

    complexity_mapping = {
        "low": "low",
        "simple": "low",
        "basic": "low",
        "low complexity": "low",

        "medium": "medium",
        "moderate": "medium",
        "average": "medium",
        "medium complexity": "medium",

        "high": "high",
        "complex": "high",
        "advanced": "high",
        "high complexity": "high",

        "faible": "low",
        "simple": "low",
        "faible complexité": "low",
        "complexité faible": "low",

        "moyen": "medium",
        "moyenne": "medium",
        "modéré": "medium",
        "moderee": "medium",
        "modérée": "medium",
        "complexité moyenne": "medium",

        "élevé": "high",
        "élevée": "high",
        "eleve": "high",
        "elevee": "high",
        "haute": "high",
        "complexe": "high",
        "complexité élevée": "high",

        "منخفض": "low",
        "منخفضة": "low",
        "بسيط": "low",
        "بسيطة": "low",
        "تعقيد منخفض": "low",

        "متوسط": "medium",
        "متوسطة": "medium",
        "تعقيد متوسط": "medium",

        "مرتفع": "high",
        "مرتفعة": "high",
        "عال": "high",
        "عالية": "high",
        "معقد": "high",
        "معقدة": "high",
        "تعقيد عال": "high",
        "تعقيد عالي": "high",
    }

    return complexity_mapping.get(
        value,
        "medium",
    )


BALANCE_MAPPINGS = {
    "balanced": {
        "en": "Balanced",
        "fr": "Équilibré",
        "ar": "متوازن",
    },
    "متوازن": {
        "en": "Balanced",
        "fr": "Équilibré",
        "ar": "متوازن",
    },
    "équilibré": {
        "en": "Balanced",
        "fr": "Équilibré",
        "ar": "متوازن",
    },
    "acceptable": {
        "en": "Acceptable",
        "fr": "Acceptable",
        "ar": "مقبول",
    },
    "acceptable but contains meaningful risks": {
        "en": "Acceptable but contains meaningful risks",
        "fr": "Acceptable mais contient des risques significatifs",
        "ar": "مقبول لكنه يتضمن مخاطر ذات أهمية",
    },

    # Employment.
    "slightly employer-friendly": {
        "en": "Slightly Party A-Friendly",
        "fr": "Légèrement favorable à la Partie A",
        "ar": "يميل قليلاً لصالح الطرف أ",
    },
    "employer-friendly": {
        "en": "Party A-Friendly",
        "fr": "Favorable à la Partie A",
        "ar": "لصالح الطرف أ",
    },
    "لصالح صاحب العمل": {
        "en": "Party A-Friendly",
        "fr": "Favorable à la Partie A",
        "ar": "لصالح الطرف أ",
    },
    "employee-friendly": {
        "en": "Party B-Friendly",
        "fr": "Favorable à la Partie B",
        "ar": "لصالح الطرف ب",
    },
    "لصالح الموظف": {
        "en": "Party B-Friendly",
        "fr": "Favorable à la Partie B",
        "ar": "لصالح الطرف ب",
    },

    # Services / procurement.
    "client-friendly": {
        "en": "Client-Friendly",
        "fr": "Favorable au client",
        "ar": "لصالح العميل",
    },
    "customer-friendly": {
        "en": "Customer-Friendly",
        "fr": "Favorable au client",
        "ar": "لصالح العميل",
    },
    "لصالح العميل": {
        "en": "Client-Friendly",
        "fr": "Favorable au client",
        "ar": "لصالح العميل",
    },
    "vendor-friendly": {
        "en": "Vendor-Friendly",
        "fr": "Favorable au fournisseur / prestataire",
        "ar": "لصالح المورّد / مقدم الخدمة",
    },
    "supplier-friendly": {
        "en": "Supplier-Friendly",
        "fr": "Favorable au fournisseur",
        "ar": "لصالح المورّد",
    },
    "provider-friendly": {
        "en": "Provider-Friendly",
        "fr": "Favorable au prestataire",
        "ar": "لصالح مقدم الخدمة",
    },
    "service-provider-friendly": {
        "en": "Service Provider-Friendly",
        "fr": "Favorable au prestataire",
        "ar": "لصالح مقدم الخدمة",
    },
    "service provider-friendly": {
        "en": "Service Provider-Friendly",
        "fr": "Favorable au prestataire",
        "ar": "لصالح مقدم الخدمة",
    },

    # Sale / purchase.
    "buyer-friendly": {
        "en": "Buyer-Friendly",
        "fr": "Favorable à l’acheteur",
        "ar": "لصالح المشتري",
    },
    "seller-friendly": {
        "en": "Seller-Friendly",
        "fr": "Favorable au vendeur",
        "ar": "لصالح البائع",
    },

    # Finance.
    "lender-friendly": {
        "en": "Lender-Friendly",
        "fr": "Favorable au prêteur",
        "ar": "لصالح المقرض",
    },
    "borrower-friendly": {
        "en": "Borrower-Friendly",
        "fr": "Favorable à l’emprunteur",
        "ar": "لصالح المقترض",
    },
    "creditor-friendly": {
        "en": "Creditor-Friendly",
        "fr": "Favorable au créancier",
        "ar": "لصالح الدائن",
    },
    "debtor-friendly": {
        "en": "Debtor-Friendly",
        "fr": "Favorable au débiteur",
        "ar": "لصالح المدين",
    },

    # Real estate.
    "landlord-friendly": {
        "en": "Landlord-Friendly",
        "fr": "Favorable au bailleur",
        "ar": "لصالح المؤجر",
    },
    "lessor-friendly": {
        "en": "Lessor-Friendly",
        "fr": "Favorable au bailleur",
        "ar": "لصالح المؤجر",
    },
    "tenant-friendly": {
        "en": "Tenant-Friendly",
        "fr": "Favorable au locataire",
        "ar": "لصالح المستأجر",
    },
    "lessee-friendly": {
        "en": "Lessee-Friendly",
        "fr": "Favorable au locataire",
        "ar": "لصالح المستأجر",
    },

    # Licensing / IP.
    "licensor-friendly": {
        "en": "Licensor-Friendly",
        "fr": "Favorable au concédant",
        "ar": "لصالح المرخِّص",
    },
    "licensee-friendly": {
        "en": "Licensee-Friendly",
        "fr": "Favorable au licencié",
        "ar": "لصالح المرخَّص له",
    },

    # Corporate / investment.
    "company-friendly": {
        "en": "Company-Friendly",
        "fr": "Favorable à l’entreprise",
        "ar": "لصالح الشركة",
    },
    "founder-friendly": {
        "en": "Founder-Friendly",
        "fr": "Favorable au fondateur",
        "ar": "لصالح المؤسس",
    },
    "investor-friendly": {
        "en": "Investor-Friendly",
        "fr": "Favorable à l’investisseur",
        "ar": "لصالح المستثمر",
    },
    "shareholder-friendly": {
        "en": "Shareholder-Friendly",
        "fr": "Favorable à l’actionnaire",
        "ar": "لصالح المساهم",
    },


    # Franchise.
    "franchisor-friendly": {
        "en": "Franchisor-Friendly",
        "fr": "Favorable au franchiseur",
        "ar": "لصالح مانح الامتياز",
    },
    "franchisee-friendly": {
        "en": "Franchisee-Friendly",
        "fr": "Favorable au franchisé",
        "ar": "لصالح صاحب الامتياز",
    },

    # Insurance.
    "insurer-friendly": {
        "en": "Insurer-Friendly",
        "fr": "Favorable à l’assureur",
        "ar": "لصالح المؤمّن",
    },
    "insured-friendly": {
        "en": "Insured-Friendly",
        "fr": "Favorable à l’assuré",
        "ar": "لصالح المؤمّن له",
    },

    # Agency.
    "principal-friendly": {
        "en": "Principal-Friendly",
        "fr": "Favorable au mandant",
        "ar": "لصالح الموكل",
    },
    "agent-friendly": {
        "en": "Agent-Friendly",
        "fr": "Favorable au mandataire",
        "ar": "لصالح الوكيل",
    },

    # Data processing.
    "controller-friendly": {
        "en": "Controller-Friendly",
        "fr": "Favorable au responsable du traitement",
        "ar": "لصالح المتحكم بالبيانات",
    },
    "processor-friendly": {
        "en": "Processor-Friendly",
        "fr": "Favorable au sous-traitant",
        "ar": "لصالح معالج البيانات",
    },

    # Construction / works.
    "contractor-friendly": {
        "en": "Contractor-Friendly",
        "fr": "Favorable à l’entrepreneur",
        "ar": "لصالح المقاول",
    },
    "owner-friendly": {
        "en": "Owner-Friendly",
        "fr": "Favorable au maître d’ouvrage",
        "ar": "لصالح صاحب المشروع",
    },

    # General imbalance.
    "one-sided": {
        "en": "One-Sided",
        "fr": "Déséquilibré",
        "ar": "منحاز لطرف واحد",
    },
    "heavily one-sided": {
        "en": "Heavily One-Sided",
        "fr": "Fortement déséquilibré",
        "ar": "منحاز بشدة لطرف واحد",
    },
    "party a-friendly": {
        "en": "Party A-Friendly",
        "fr": "Favorable à la Partie A",
        "ar": "لصالح الطرف أ",
    },
    "party b-friendly": {
        "en": "Party B-Friendly",
        "fr": "Favorable à la Partie B",
        "ar": "لصالح الطرف ب",
    },
}


def translate_balance(
    value: Any,
    language: str,
) -> str:
    language = normalize_language(language)

    value = normalize_missing_value(
        value,
        language,
    )

    normalized = value.lower().strip()

    if normalized in BALANCE_MAPPINGS:
        return BALANCE_MAPPINGS[normalized].get(
            language,
            BALANCE_MAPPINGS[normalized]["en"],
        )

    return value


def normalize_contract_summary(
    data: dict | None,
    language: str = "en",
) -> dict:
    language = normalize_language(language)
    data = data or {}

    not_specified = get_not_specified(language)

    raw = {
        "contract_type": normalize_missing_value(
            data.get("contract_type"),
            language,
        ),
        "parties": normalize_parties(
            data.get("parties"),
            language,
        ) or [not_specified],
        "duration": normalize_missing_value(
            data.get("duration"),
            language,
        ),
        "payment_terms": normalize_missing_value(
            data.get("payment_terms"),
            language,
        ),
        "main_obligations": normalize_list(
            data.get("main_obligations"),
            language,
        ),
        "global_summary": normalize_missing_value(
            data.get("global_summary"),
            language,
        ),
        "important_points": normalize_list(
            data.get("important_points"),
            language,
        ),
        "missing_clauses": normalize_list(
            data.get("missing_clauses"),
            language,
        ),
        "dangerous_patterns": normalize_list(
            data.get("dangerous_patterns"),
            language,
        ),
        "contract_score": clamp_score(
            data.get("contract_score"),
        ),
        "overall_balance": translate_balance(
            data.get("overall_balance"),
            language,
        ),
        "negotiation_priorities": normalize_list(
            data.get("negotiation_priorities"),
            language,
        ),
        "key_risks": normalize_list(
            data.get("key_risks"),
            language,
        ),
        "practical_decision": normalize_missing_value(
            data.get("practical_decision"),
            language,
        ),
        "jurisdiction_detected": normalize_missing_value(
            data.get("jurisdiction_detected"),
            language,
        ),
        "jurisdiction_note": normalize_missing_value(
            data.get("jurisdiction_note"),
            language,
        ),
        "recommended_actions": normalize_list(
            data.get("recommended_actions"),
            language,
        ),
        "contract_complexity": normalize_complexity(
            data.get("contract_complexity"),
        ),
    }

    validated = ContractSummary(**raw)

    return validated.model_dump()


def normalize_simplified_contract(
    data: dict | None,
    language: str = "en",
) -> dict:
    language = normalize_language(language)
    data = data or {}

    raw = {
        "simplified_version": normalize_missing_value(
            data.get("simplified_version"),
            language,
        ),
        "key_points": normalize_list(
            data.get("key_points"),
            language,
        ),
        "things_to_watch": normalize_list(
            data.get("things_to_watch"),
            language,
        ),
    }

    validated = SimplifiedContract(**raw)

    return validated.model_dump()
