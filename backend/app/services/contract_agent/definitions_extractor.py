"""
definitions_extractor.py

Point 3 (Definitions Matter): definitions determine the scope of every
downstream obligation. This module extracts the ACTUAL defined terms from
the contract text before any clause-level reasoning happens, so the model
never falls back on an assumed market-standard definition (e.g. assuming
"Confidential Information" requires marking when the contract says
otherwise).

This is intentionally rule-based (regex), not an AI call: definitions are
structurally predictable in contracts, and a deterministic extractor is
cheaper, faster, and auditable compared to asking the model to "remember"
to check definitions.
"""

import re

# Concepts the reasoning engine must never assume a default for.
# Each concept maps to its surface forms across the product's 3 supported
# languages, since a defined term almost never appears in English inside
# a French or Arabic contract.
WATCHED_CONCEPTS = {
    "confidential_information": {
        "en": ["Confidential Information"],
        "fr": ["Information Confidentielle", "Informations Confidentielles"],
        "ar": ["المعلومات السرية", "معلومات سرية"],
    },
    "affiliate": {
        "en": ["Affiliate"],
        "fr": ["Affilié", "Société Affiliée"],
        "ar": ["الشركة التابعة", "الشركة الشقيقة"],
    },
    "business_day": {
        "en": ["Business Day"],
        "fr": ["Jour Ouvré", "Jour Ouvrable"],
        "ar": ["يوم عمل"],
    },
    "force_majeure": {
        "en": ["Force Majeure"],
        "fr": ["Force Majeure"],
        "ar": ["القوة القاهرة"],
    },
    "deliverables": {
        "en": ["Deliverables"],
        "fr": ["Livrables"],
        "ar": ["المخرجات", "مخرجات العمل"],
    },
    "services": {
        "en": ["Services"],
        "fr": ["Services", "Prestations"],
        "ar": ["الخدمات"],
    },
    "personal_data": {
        "en": ["Personal Data"],
        "fr": ["Données Personnelles"],
        "ar": ["البيانات الشخصية"],
    },
}

# Kept for readability in build_definitions_block(); resolved per-language
# at call time from WATCHED_CONCEPTS.
WATCHED_TERMS = list(WATCHED_CONCEPTS.keys())

# Pattern A: "Term" means ... / "Term" shall mean ... (English)
PATTERN_EXPLICIT_MEANS_EN = re.compile(
    r'"([A-Z][A-Za-z0-9 /\-]{2,60})"\s+(?:means|shall mean|refers to)\s+(.+?)'
    r'(?=(?:\n\s*"[A-Z][A-Za-z0-9 /\-]{2,60}"\s+(?:means|shall mean|refers to))|\Z)',
    re.DOTALL,
)

# Pattern A-FR: « Terme » désigne / signifie ... (French contracts commonly
# use guillemets « » or straight quotes, and "désigne"/"signifie" instead of "means")
PATTERN_EXPLICIT_MEANS_FR = re.compile(
    r'[«"]\s*([A-ZÀ-Ÿ][A-Za-zÀ-ÿ0-9 /\-]{2,60})\s*[»"]\s+(?:désigne|signifie)\s+(.+?)'
    r'(?=(?:\n\s*[«"][A-ZÀ-Ÿ][A-Za-zÀ-ÿ0-9 /\-]{2,60}[»"]\s+(?:désigne|signifie))|\Z)',
    re.DOTALL,
)

# Pattern A-AR: "المصطلح" تعني / يقصد بـ ... (Arabic definition clauses)
PATTERN_EXPLICIT_MEANS_AR = re.compile(
    r'"([\u0600-\u06FF][\u0600-\u06FF0-9 /\-]{1,60})"\s*(?:تعني|يقصد بـ|يُقصد بـ)\s+(.+?)'
    r'(?=(?:\n\s*"[\u0600-\u06FF][\u0600-\u06FF0-9 /\-]{1,60}"\s*(?:تعني|يقصد بـ|يُقصد بـ))|\Z)',
    re.DOTALL,
)

# Pattern B: Term (the "X") / Terme (le « X ») — inline declaration without
# an explicit "means" clause. Latin-script only; Arabic contracts rarely use
# this parenthetical-alias convention, so no AR variant is needed here.
PATTERN_INLINE_DECLARATION = re.compile(
    r'([^.]{0,200}?)\(\s*(?:the|le|la|l\')?\s*["«]\s*([A-Za-zÀ-ÿ0-9 /\-]{2,60})\s*["»]\s*\)',
)


def _clean(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def extract_definitions(contract_text: str) -> dict:
    """
    Returns:
        {
            "found": [
                {"term": str, "definition": str, "source": "explicit_means_en" |
                 "explicit_means_fr" | "explicit_means_ar" | "inline_reference"}
            ],
            "watched_terms_missing": [str, ...],   # concept keys not present in the text in ANY supported language
            "watched_terms_undefined": [str, ...], # concept mentioned but never formally defined
        }
    """
    if not contract_text or not contract_text.strip():
        return {"found": [], "watched_terms_missing": list(WATCHED_TERMS), "watched_terms_undefined": []}

    found = []
    seen_terms = set()

    pattern_sources = [
        (PATTERN_EXPLICIT_MEANS_EN, "explicit_means_en"),
        (PATTERN_EXPLICIT_MEANS_FR, "explicit_means_fr"),
        (PATTERN_EXPLICIT_MEANS_AR, "explicit_means_ar"),
    ]
    for pattern, source in pattern_sources:
        for match in pattern.finditer(contract_text):
            term = _clean(match.group(1))
            definition = _clean(match.group(2))[:1200]
            if term.lower() not in seen_terms:
                found.append({"term": term, "definition": definition, "source": source})
                seen_terms.add(term.lower())

    for match in PATTERN_INLINE_DECLARATION.finditer(contract_text):
        context = _clean(match.group(1))
        term = _clean(match.group(2))
        if term.lower() not in seen_terms:
            found.append({"term": term, "definition": context[-400:], "source": "inline_reference"})
            seen_terms.add(term.lower())

    watched_terms_missing = []
    watched_terms_undefined = []
    lowered_text = contract_text.lower()

    for concept_key, variants_by_lang in WATCHED_CONCEPTS.items():
        all_variants = [v for variants in variants_by_lang.values() for v in variants]
        # Arabic has no case-folding needs; lower() is a no-op on Arabic script.
        mentioned = any(variant.lower() in lowered_text for variant in all_variants)
        defined = any(variant.lower() in seen_terms for variant in all_variants)
        if not mentioned:
            watched_terms_missing.append(concept_key)
        elif mentioned and not defined:
            watched_terms_undefined.append(concept_key)

    return {
        "found": found,
        "watched_terms_missing": watched_terms_missing,
        "watched_terms_undefined": watched_terms_undefined,
    }


def build_definitions_block(extraction: dict) -> str:
    """
    Renders the extraction result as a prompt-ready block. This is what gets
    injected into the unified prompt so the model reasons from the literal
    text instead of guessing.
    """
    if not extraction["found"] and not extraction["watched_terms_missing"] and not extraction["watched_terms_undefined"]:
        return "No definitions section detected."

    lines = ["ACTUAL CONTRACTUAL DEFINITIONS FOUND (reason ONLY from these, never assume a market default):"]
    for item in extraction["found"]:
        lines.append(f'- "{item["term"]}" [{item["source"]}]: {item["definition"]}')

    if extraction["watched_terms_undefined"]:
        lines.append(
            "\nTERMS USED BUT NEVER FORMALLY DEFINED (do not assume scope; flag in confidence_notes): "
            + ", ".join(extraction["watched_terms_undefined"])
        )

    if extraction["watched_terms_missing"]:
        lines.append(
            "\nWATCHED TERMS NOT PRESENT AT ALL IN THIS CONTRACT (only note as missing_clauses if genuinely "
            "expected for this contract family): " + ", ".join(extraction["watched_terms_missing"])
        )

    return "\n".join(lines)
