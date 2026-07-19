"""Fail-closed final publication enforcement for source-grounded clause text.

Contract-family agnostic. The validator derives a compact semantic profile from
exact clause source text, validates protected generated fields, records receipts
for the exact published value, and asserts those receipts at serialization.
"""
from __future__ import annotations

import hashlib
import json
import re
from typing import Any

from app.services.contract_agent.contract_taxonomy import detect_clause_type_from_taxonomy

PROTECTED_FIELDS = (
    "legal_insight",
    "market_comparison",
    "safer_alternative",
    "recommendation",
    "negotiation_advice",
    "market_practice",
    "fallback_wording",
    "negotiable",
    "acceptable_compromise",
    "never_accept",
    "negotiation_boundary",
)

# Publication policy is field-specific. This prevents compact conclusion fields
# from being treated as source rewrites while still requiring exact final-text
# receipts and final serialization integrity for every published protected field.
_FIELD_POLICIES = {
    "legal_insight": "relevance",
    "market_comparison": "relevance",
    "safer_alternative": "fidelity",
    "recommendation": "relevance",
    "negotiation_advice": "relevance",
    "market_practice": "compact_conclusion",
    "fallback_wording": "fidelity",
    "negotiable": "compact_conclusion",
    "acceptable_compromise": "fidelity",
    "never_accept": "relevance",
    "negotiation_boundary": "relevance",
}

_FIDELITY_FIELDS = {
    field
    for field, policy in _FIELD_POLICIES.items()
    if policy == "fidelity"
}

_RELEVANCE_FIELDS = {
    field
    for field, policy in _FIELD_POLICIES.items()
    if policy == "relevance"
}

_COMPACT_CONCLUSION_FIELDS = {
    field
    for field, policy in _FIELD_POLICIES.items()
    if policy == "compact_conclusion"
}

_MARKET_PRACTICE_ALLOWED = {
    "standard",
    "common",
    "common with variations",
    "negotiable",
    "uncommon",
    "aggressive",
    "highly aggressive",
    "unknown",
    "unclear",
    "not assessed",
    "non évalué",
    "non evalue",
    "inconnu",
    "indéterminé",
    "indetermine",
    "غير معروف",
    "غير محدد",
    "لم يتم التقييم",
}

_NEGOTIABLE_ALLOWED = {
    "yes",
    "no",
    "conditional",
    "depends",
    "unknown",
    "unclear",
    "not assessed",
    "oui",
    "non",
    "conditionnel",
    "conditionnelle",
    "dépend",
    "depend",
    "inconnu",
    "indéterminé",
    "indetermine",
    "نعم",
    "لا",
    "مشروط",
    "يعتمد",
    "غير معروف",
    "غير محدد",
}

_POSITIVE_SAFE = (
    "no significant legal imbalance detected",
    "aucun déséquilibre juridique significatif détecté",
    "لم يتم رصد اختلال قانوني جوهري",
)

_ABSTENTION_MARKERS = (
    "manual review required",
    "manual review is required",
    "revue manuelle requise",
    "une revue manuelle est requise",
    "مراجعة يدوية مطلوبة",
    "تتطلب مراجعة يدوية",
)

_STOP = {
    # English
    "the", "a", "an", "and", "or", "of", "to", "in", "on", "for", "with",
    "without", "by", "from", "at", "as", "is", "are", "be", "been", "being",
    "this", "that", "such", "its", "their", "any", "all", "other", "shall",
    "should", "may", "must", "would", "could", "agreement", "section",
    # French
    "le", "la", "les", "un", "une", "des", "du", "de", "d", "et", "ou",
    "dans", "sur", "pour", "avec", "sans", "par", "est", "sont", "être",
    "cette", "cet", "ces", "son", "sa", "ses", "leur", "leurs", "tout",
    "toute", "tous", "toutes", "doit", "devrait", "peut", "accord", "article",
    # Arabic
    "هذا", "هذه", "ذلك", "تلك", "من", "إلى", "الى", "في", "على", "عن", "مع",
    "دون", "بدون", "أو", "او", "و", "هو", "هي", "يكون", "تكون", "أي", "اي",
    "كل", "أخرى", "اخرى", "يجب", "يجوز", "قد", "الاتفاقية", "الاتفاق", "المادة",
}

# Canonical semantic aliases. Language-specific surface forms normalize into
# the same small set of cross-domain operative primitives. Validators consume
# only the canonical values below.
_CANONICAL_TOKEN_ALIASES = {
    # affirmative participation / approval
    "vote": "vote",
    "votes": "vote",
    "voting": "vote",
    "voter": "vote",
    "votez": "vote",
    "votent": "vote",
    "تصويت": "vote",
    "التصويت": "vote",
    "يصوت": "vote",
    "يصوتوا": "vote",
    "consent": "consent",
    "consents": "consent",
    "consenting": "consent",
    "consentement": "consent",
    "consentir": "consent",
    "consentiront": "consent",
    "موافقة": "consent",
    "الموافقة": "consent",
    "يوافق": "consent",
    "يوافقوا": "consent",
    "approval": "consent",
    "approve": "consent",
    "approved": "consent",
    "approbation": "consent",
    "approuver": "consent",
    "موافقتها": "consent",
    # notice
    "notice": "notice",
    "notification": "notice",
    "notify": "notice",
    "notified": "notice",
    "notifier": "notice",
    "notification": "notice",
    "préavis": "notice",
    "preavis": "notice",
    "إشعار": "notice",
    "اشعار": "notice",
    "إخطار": "notice",
    "اخطار": "notice",
    "يخطر": "notice",
    # automatic transition
    "terminate": "terminate",
    "terminates": "terminate",
    "termination": "terminate",
    "expire": "terminate",
    "expires": "terminate",
    "end": "terminate",
    "ends": "terminate",
    "résilier": "terminate",
    "résiliation": "terminate",
    "resilier": "terminate",
    "resiliation": "terminate",
    "prend": "terminate",
    "fin": "terminate",
    "إنهاء": "terminate",
    "انهاء": "terminate",
    "ينتهي": "terminate",
    "تنتهي": "terminate",
    "automatic": "automatic",
    "automatically": "automatic",
    "automatique": "automatic",
    "automatiquement": "automatic",
    "تلقائيا": "automatic",
    "تلقائيًا": "automatic",
    "تلقائية": "automatic",
}

_WORD_PATTERN = re.compile(r"[^\W\d_]+", re.UNICODE)

_MANDATORY_PATTERNS = (
    # English
    re.compile(
        r"\b(?:required|obliged|obligated)\s+to\s+"
        r"(.{1,220}?)(?:,\s*subject\s+to|[.;]|$)",
        re.IGNORECASE | re.DOTALL,
    ),
    # French
    re.compile(
        r"\b(?:tenu(?:e|es|s)?|obligé(?:e|es|s)?)\s+de\s+"
        r"(.{1,220}?)(?:,\s*sous\s+réserve|[.;]|$)|"
        r"\bdoit\s+(.{1,220}?)(?:,\s*sous\s+réserve|[.;]|$)",
        re.IGNORECASE | re.DOTALL,
    ),
    # Arabic
    re.compile(
        r"(?:يجب|يتعين)\s+على\s+.{1,100}?\s+أن\s+"
        r"(.{1,220}?)(?:[.؛،]|$)|"
        r"(?:يلتزم)\s+(?:[^.،؛]{1,100}?\s+)?(?:ب|أن\s+)?"
        r"(.{1,220}?)(?:[.؛،]|$)",
        re.IGNORECASE | re.DOTALL,
    ),
)

_CONJUNCTION_SPLIT = re.compile(
    r"\s+(?:and|et)\s+|\s+و(?=[\u0600-\u06FF])",
    re.IGNORECASE,
)

_AUTOMATIC_PATTERNS = (
    r"\b(?:terminate|expire|end)\w*\s+automatically\s+"
    r"(?:upon|on)\b.{0,260}",
    r"\b(?:prend\s+fin|résili\w*|expire\w*)\s+automatiquement\s+"
    r"(?:dès|lors\s+de|à\s+la\s+survenance\s+de|au)\b.{0,260}",
    r"(?:ينتهي|تنتهي|يُنهى|ينهى)\s+(?:هذا\s+الاتفاق|هذه\s+الاتفاقية|"
    r"الاتفاق|الاتفاقية)?\s*تلقائي(?:اً|ًا|ا)?\s+"
    r"(?:عند|بمجرد|لدى)\b.{0,260}",
)

_PRIOR_CONSENT_PATTERNS = (
    r"\bwithout\b.{0,100}\bprior\s+(?:written\s+)?"
    r"(?:consent|approval)\b|"
    r"\bprior\s+written\s+(?:consent|approval)\b",
    r"\bsans\b.{0,100}\b(?:consentement|approbation)\b.{0,50}"
    r"\bpréalable\b|"
    r"\b(?:consentement|approbation)\s+(?:écrit(?:e)?\s+)?préalable\b",
    r"(?:دون|بدون)\s+.{0,100}(?:موافقة|الموافقة)\s+.{0,40}"
    r"(?:مسبق(?:ة|اً|ًا|ا)?|خطية\s+مسبقة)|"
    r"(?:الموافقة|موافقة)\s+(?:الخطية\s+)?المسبقة",
)

_NOTICE_PATTERNS = (
    r"\b(?:prior|advance)\s+(?:written\s+)?notice\b",
    r"\bnotice\s+period\b",
    r"\b\d+\s*\)?\s*(?:calendar\s+|business\s+)?days?\b"
    r".{0,35}\bnotice\b",
    r"\bpréavis\b",
    r"\bnotification\s+(?:écrite\s+)?préalable\b",
    r"\b\d+\s*\)?\s*jours?\b.{0,35}\b(?:préavis|notification)\b",
    r"(?:إشعار|اشعار|إخطار|اخطار)\s+(?:خطي\s+)?مسبق",
    r"(?:مهلة|فترة)\s+(?:إشعار|اشعار|إخطار|اخطار)",
    r"\d+\s*\)?\s*(?:يوم|يوماً|يومًا|أيام|ايام)\b.{0,35}"
    r"(?:إشعار|اشعار|إخطار|اخطار)",
)

_CONSENT_WORD_PATTERN = re.compile(
    r"\b(?:consent|approval|consentement|approbation)\b|"
    r"(?:موافقة|الموافقة)",
    re.IGNORECASE,
)

_NOTICE_WORD_PATTERN = re.compile(
    r"\b(?:notice|notify|notification|préavis|preavis|notifier)\b|"
    r"(?:إشعار|اشعار|إخطار|اخطار|يخطر)",
    re.IGNORECASE,
)

def _hash(text: str) -> str:
    return hashlib.sha256(str(text or "").encode("utf-8")).hexdigest()


def _canonical_token(word: str) -> str:
    value = str(word or "").lower().strip()

    if value in _CANONICAL_TOKEN_ALIASES:
        return _CANONICAL_TOKEN_ALIASES[value]

    # Arabic conjunction is commonly attached to the operative word
    # (e.g. "والموافقة"). Normalize the surface prefix only when the
    # remaining token is a known canonical semantic alias.
    if value.startswith("و") and len(value) > 2:
        without_conjunction = value[1:]
        if without_conjunction in _CANONICAL_TOKEN_ALIASES:
            return _CANONICAL_TOKEN_ALIASES[without_conjunction]

    if value.endswith("ies") and len(value) > 6:
        value = value[:-3] + "y"
    elif value.endswith("s") and len(value) > 5:
        value = value[:-1]

    return _CANONICAL_TOKEN_ALIASES.get(value, value)


def _tokens(text: str) -> set[str]:
    """Unicode-aware tokens normalized to canonical semantic primitives."""
    result: set[str] = set()

    for raw_word in _WORD_PATTERN.findall(str(text or "").lower()):
        if len(raw_word) < 2 or raw_word in _STOP:
            continue

        word = _canonical_token(raw_word)

        if word and word not in _STOP:
            result.add(word)

    return result


def _argument_signature(text: str) -> list[str]:
    """Return the first canonical operative predicate for an argument."""
    tokens = _tokens(text)

    # Prefer known operative primitives over descriptive nouns. This makes
    # English, French, and Arabic forms converge to the same signature.
    for primitive in ("vote", "consent", "notice", "terminate"):
        if primitive in tokens:
            return [primitive]

    for raw_word in _WORD_PATTERN.findall(str(text or "").lower()):
        if len(raw_word) < 2 or raw_word in _STOP:
            continue

        word = _canonical_token(raw_word)

        if word and word not in _STOP:
            return [word]

    return []


def _span(text: str, pattern: str, label: str) -> dict | None:
    match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
    if not match:
        return None
    return {
        "label": label,
        "start": match.start(),
        "end": match.end(),
        "text": match.group(0),
    }


def _normalize_actor_label(value: str) -> str:
    """Normalize an expressly named consent-holder/approver label."""
    text = str(value or "").lower().strip()
    text = re.sub(r"[’']s\b", "", text)
    text = re.sub(r"\s+", " ", text).strip()

    # Keep the noun phrase nearest the consent construction. This removes
    # generic framing such as "the requirement for" without mapping any
    # contract family or named party.
    parts = re.split(
        r"\b(?:for|of|to|by|from|without|pour|de|du|des|par|sans)\b",
        text,
        flags=re.IGNORECASE,
    )
    if len(parts) > 1 and parts[-1].strip():
        text = parts[-1].strip()

    text = re.sub(
        r"^(?:the|a|an|le|la|les|l['’]|un|une|ال)\s*",
        "",
        text,
        flags=re.IGNORECASE,
    ).strip()

    return text


def _extract_consent_holder(text: str) -> dict | None:
    """Extract an explicit actor tied to prior consent or approval.

    Syntax-driven and multilingual. Ambiguous references remain UNKNOWN.
    """
    value = str(text or "")

    patterns = (
        # English possessive and "consent of X"
        re.compile(
            r"\b(?:without\s+)?(?:the\s+)?"
            r"([^,.;:]{1,70}?)[’']s\s+prior\s+"
            r"(?:written\s+)?(?:consent|approval)\b",
            re.IGNORECASE,
        ),
        re.compile(
            r"\bprior\s+(?:written\s+)?(?:consent|approval)\s+of\s+"
            r"(?:the\s+)?([^,.;:]{1,70}?)"
            r"(?=\s+(?:to|before|for|is|was|shall|must|may)\b|[,.;:]|$)",
            re.IGNORECASE,
        ),
        # French: consentement préalable de X
        re.compile(
            r"\b(?:consentement|approbation)\s+"
            r"(?:écrit(?:e)?\s+)?préalable\s+d(?:e|u|es|['’])\s*"
            r"([^,.;:]{1,70}?)"
            r"(?=\s+(?:pour|avant|à|de|est|sera|doit|peut)\b|[,.;:]|$)",
            re.IGNORECASE,
        ),
        # Arabic: الموافقة الخطية المسبقة لـ/من [actor]
        re.compile(
            r"(?:الموافقة|موافقة)\s+(?:الخطية\s+)?المسبقة\s+"
            r"(?:ل|من)\s*([\u0600-\u06FF][\u0600-\u06FF\s]{0,60}?)"
            r"(?=[،؛.]|$)",
            re.IGNORECASE,
        ),
    )

    for pattern in patterns:
        match = pattern.search(value)

        if not match:
            continue

        raw = match.group(1).strip()
        normalized = _normalize_actor_label(raw)

        if not normalized:
            continue

        return {
            "raw": raw,
            "normalized": normalized,
            "start": match.start(1),
            "end": match.end(1),
        }

    return None


def _first_group(match: re.Match[str]) -> str:
    for group in match.groups():
        if group:
            return group
    return ""


def build_source_evidence_model(source_text: str) -> dict:
    """Build one canonical EN/FR/AR source profile from exact clause text."""
    source = str(source_text or "")
    spans: list[dict] = []
    mechanisms: list[dict] = []

    mandatory = None
    mandatory_body = ""

    for pattern in _MANDATORY_PATTERNS:
        match = pattern.search(source)

        if match:
            mandatory = match
            mandatory_body = _first_group(match)
            break

    if mandatory and mandatory_body:
        arguments = [
            part.strip()
            for part in _CONJUNCTION_SPLIT.split(mandatory_body)
            if part.strip()
        ]

        if len(arguments) >= 2:
            spans.append({
                "label": "MANDATORY_CONJUNCTION",
                "start": mandatory.start(),
                "end": mandatory.end(),
                "text": mandatory.group(0),
            })
            mechanisms.append({
                "kind": "MANDATORY_CONJUNCTION",
                "polarity": "REQUIRED",
                "arguments": [
                    {
                        "tokens": sorted(_tokens(argument)),
                        "signature": _argument_signature(argument),
                    }
                    for argument in arguments
                ],
            })

    automatic = None

    for pattern in _AUTOMATIC_PATTERNS:
        automatic = _span(
            source,
            pattern,
            "AUTOMATIC_EVENT_TRANSITION",
        )

        if automatic:
            break

    if automatic:
        spans.append(automatic)
        mechanisms.append({
            "kind": "PROCEDURAL_STATE",
            "state": "AUTOMATIC_EVENT",
            "notice_prerequisite": False,
        })

    prior_consent = None

    for pattern in _PRIOR_CONSENT_PATTERNS:
        prior_consent = _span(
            source,
            pattern,
            "PRIOR_CONSENT_PREREQUISITE",
        )

        if prior_consent:
            break

    if prior_consent:
        spans.append(prior_consent)
        consent_holder = _extract_consent_holder(source)

        prerequisite: dict[str, Any] = {
            "kind": "PREREQUISITE",
            "state": "PRIOR_CONSENT",
        }

        if consent_holder:
            prerequisite["consent_holder"] = consent_holder["normalized"]
            prerequisite["consent_holder_text"] = consent_holder["raw"]
            spans.append({
                "label": "CONSENT_HOLDER",
                "start": consent_holder["start"],
                "end": consent_holder["end"],
                "text": consent_holder["raw"],
            })

        mechanisms.append(prerequisite)

    source_type = detect_clause_type_from_taxonomy(source)

    mechanisms.append({
        "kind": "SOURCE_PROFILE",
        "primary_type": source_type,
        "anchors": sorted(_tokens(source)),
    })

    canonical = json.dumps(
        mechanisms,
        sort_keys=True,
        ensure_ascii=False,
    )

    return {
        "evidence_spans": spans,
        "mechanisms": mechanisms,
        "semantic_profile_hash": _hash(canonical),
    }


def rank_grounded_mechanisms(profile: dict) -> list[dict]:
    rank = {
        "PREREQUISITE": 100,
        "PROCEDURAL_STATE": 95,
        "MANDATORY_CONJUNCTION": 90,
        "SOURCE_PROFILE": 10,
    }
    return sorted(
        profile.get("mechanisms", []),
        key=lambda item: rank.get(item.get("kind"), 0),
        reverse=True,
    )


def _semantic_coverage(source_text: str, generated_text: str) -> float | None:
    source_tokens = _tokens(source_text)
    generated_tokens = _tokens(generated_text)
    if not source_tokens or not generated_tokens:
        return None
    denominator = max(1, min(len(source_tokens), 12))
    return round(len(source_tokens & generated_tokens) / denominator, 4)


def _is_abstention(text: str) -> bool:
    low = str(text or "").lower()
    return any(marker in low for marker in _ABSTENTION_MARKERS)


def _normalized_compact_value(value: str) -> str:
    return re.sub(
        r"\\s+",
        " ",
        str(value or "").strip().lower(),
    )


def _validate_compact_conclusion(
    field: str,
    generated_text: str,
) -> list[str]:
    """Validate compact published conclusion fields without prose validators."""
    value = _normalized_compact_value(generated_text)
    reasons: list[str] = []

    if not value:
        return reasons

    if field == "market_practice":
        if value not in _MARKET_PRACTICE_ALLOWED:
            reasons.append("INVALID_MARKET_PRACTICE_VALUE")

    elif field == "negotiable":
        if value not in _NEGOTIABLE_ALLOWED:
            reasons.append("INVALID_NEGOTIABLE_VALUE")

    return reasons


def validate_source_grounding(
    source_text: str,
    generated_text: str,
    field: str,
    profile: dict,
) -> tuple[list[str], float | None]:
    reasons: list[str] = []
    generated = str(generated_text or "")
    low = generated.lower()
    generated_tokens = _tokens(generated)
    coverage = _semantic_coverage(source_text, generated)
    policy = _FIELD_POLICIES.get(field, "relevance")

    if policy == "compact_conclusion":
        reasons.extend(
            _validate_compact_conclusion(
                field,
                generated,
            )
        )
        return list(dict.fromkeys(reasons)), coverage

    if _is_abstention(generated):
        return reasons, coverage

    for mechanism in rank_grounded_mechanisms(profile):
        kind = mechanism.get("kind")

        if kind == "MANDATORY_CONJUNCTION" and field in _FIDELITY_FIELDS:
            arguments = mechanism.get("arguments", [])

            # Only enforce full conjunctive coverage when the generated
            # text actually engages the same operative source mechanism.
            # A collateral recommendation about a different protection
            # must not be forced to restate every mandatory source action.
            source_signatures = {
                token
                for argument in arguments
                for token in argument.get("signature", [])
            }

            engages_same_mechanism = bool(
                source_signatures & generated_tokens
            )

            if engages_same_mechanism:
                missing_arguments = []

                for argument in arguments:
                    argument_tokens = set(argument.get("tokens", []))
                    signature_tokens = set(argument.get("signature", []))

                    if signature_tokens:
                        covered = bool(
                            signature_tokens & generated_tokens
                        )
                    else:
                        covered = bool(
                            argument_tokens & generated_tokens
                        )

                    if argument_tokens and not covered:
                        missing_arguments.append(argument)

                if missing_arguments:
                    reasons.extend([
                        "SEMANTIC_ARGUMENT_COVERAGE_LOSS",
                        "RIGHT_POLARITY_OR_SCOPE_WEAKENING",
                    ])

        elif kind == "PROCEDURAL_STATE" and field in _FIDELITY_FIELDS:
            if mechanism.get("state") == "AUTOMATIC_EVENT":
                introduces_notice = any(
                    re.search(
                        pattern,
                        low,
                        re.IGNORECASE | re.DOTALL,
                    )
                    for pattern in _NOTICE_PATTERNS
                )
                if introduces_notice:
                    reasons.append("PROCEDURAL_STATE_MISMATCH_AUTOMATIC_TO_NOTICE")

        elif kind == "PREREQUISITE":
            if mechanism.get("state") == "PRIOR_CONSENT":
                has_consent = bool(_CONSENT_WORD_PATTERN.search(low))
                has_notice = bool(_NOTICE_WORD_PATTERN.search(low))

                if field in _FIDELITY_FIELDS and has_notice and not has_consent:
                    reasons.append("CONSENT_PREREQUISITE_WEAKENED_TO_NOTICE")

                # Compare the holder only when both source and generated text
                # expressly attribute the same prior-consent mechanism.
                source_holder = _normalize_actor_label(
                    str(mechanism.get("consent_holder") or "")
                )
                generated_holder_data = _extract_consent_holder(generated)
                generated_holder = _normalize_actor_label(
                    generated_holder_data.get("normalized", "")
                    if generated_holder_data
                    else ""
                )

                if (
                    has_consent
                    and source_holder
                    and generated_holder
                    and source_holder != generated_holder
                ):
                    reasons.append("CONSENT_HOLDER_ACTOR_MISMATCH")

    if field in _RELEVANCE_FIELDS:
        source_type = detect_clause_type_from_taxonomy(source_text)
        generated_type = detect_clause_type_from_taxonomy(generated)
        weak_types = {"", "other", "general", None}
        if (
            source_type not in weak_types
            and generated_type not in weak_types
            and source_type != generated_type
            and coverage == 0.0
        ):
            reasons.append("FINAL_TEXT_SOURCE_CONTAMINATION")

    return list(dict.fromkeys(reasons)), coverage


def _blocked_text(language: str) -> str:
    return {
        "fr": "Revue manuelle requise : le texte généré n'a pas passé la validation de fidélité à la source.",
        "ar": "مراجعة يدوية مطلوبة: لم يجتز النص المُنشأ التحقق من مطابقته للمصدر.",
    }.get(language, "Manual review required: generated text did not pass source-fidelity validation.")


def _issue(field: str, reason: str) -> dict:
    high_markers = ("POLARITY", "PROCEDURAL", "CONSENT", "ACTOR", "CONTAMINATION")
    return {
        "kind": reason.lower(),
        "field": field,
        "severity": "high" if any(marker in reason for marker in high_markers) else "medium",
        "note": reason,
    }


def enforce_final_publication_gate(
    results: list[dict],
    language: str = "en",
    *,
    final_pass: bool = False,
) -> list[dict]:
    """Validate and fail closed. A final pass emits exact-text receipts."""
    for item in results:
        if not isinstance(item, dict):
            continue

        source = str(
            item.get("_source_text_exact")
            or item.get("original_text")
            or item.get("clause_text")
            or item.get("quoted_text")
            or ""
        )
        profile = build_source_evidence_model(source)
        history = item.setdefault("_publication_validation_history", {})
        emitted: list[dict] = []
        current_failures: list[str] = []

        for field in PROTECTED_FIELDS:
            text = str(item.get(field) or "")
            if not text.strip():
                continue

            reasons, coverage = validate_source_grounding(source, text, field, profile)
            if reasons:
                history[field] = {
                    "input_text": text,
                    "input_text_hash": _hash(text),
                    "validation_reasons": reasons,
                    "semantic_coverage": coverage,
                }
                item[field] = _blocked_text(language)
                current_failures.extend(reasons)
                emitted.extend(_issue(field, reason) for reason in reasons)

        positive_field = str(item.get("legal_insight") or "")
        positive_low = positive_field.lower()
        prior_failures = [
            reason
            for entry in history.values()
            for reason in entry.get("validation_reasons", [])
        ]
        if any(marker in positive_low for marker in _POSITIVE_SAFE) and (current_failures or prior_failures):
            reason = "UNKNOWN_IS_NOT_SAFE_POSITIVE_CONCLUSION"
            history["legal_insight"] = {
                "input_text": positive_field,
                "input_text_hash": _hash(positive_field),
                "validation_reasons": [reason],
                "semantic_coverage": _semantic_coverage(source, positive_field),
            }
            item["legal_insight"] = _blocked_text(language)
            emitted.append(_issue("legal_insight", reason))

        if emitted:
            existing = item.setdefault("fidelity_issues", [])
            existing.extend(emitted)
            item["negotiation_fidelity_warning"] = True
            item["negotiation_fidelity_note"] = emitted[0]["note"]

        item["source_evidence_model"] = profile

        if final_pass:
            receipts: dict[str, dict] = {}
            for field in PROTECTED_FIELDS:
                final_text = str(item.get(field) or "")
                if not final_text.strip():
                    continue

                final_reasons, final_coverage = validate_source_grounding(
                    source, final_text, field, profile
                )
                if final_reasons:
                    raise AssertionError(
                        f"final publication field failed validation: {field}: {final_reasons}"
                    )

                prior = history.get(field, {})
                prior_reasons = list(prior.get("validation_reasons", []))
                receipts[field] = {
                    "field": field,
                    "field_policy": _FIELD_POLICIES.get(field, "relevance"),
                    "publication_gate_called": True,
                    "gate_result": "BLOCK_AND_REPLACE_REVALIDATED" if prior_reasons else "PASS",
                    "validation_reasons": prior_reasons,
                    "semantic_coverage": final_coverage,
                    "semantic_profile_hash": profile["semantic_profile_hash"],
                    "validated_text_hash": _hash(final_text),
                    "final_text_hash": _hash(final_text),
                    "source_text_hash": _hash(source),
                    "input_text_hash": prior.get("input_text_hash", _hash(final_text)),
                    "text_before_validation": prior.get("input_text", final_text),
                    "successful": True,
                    "post_gate_mutators": [],
                }
            item["validation_receipts"] = receipts

    return results


def assert_final_serialization(results: list[dict]) -> None:
    """Assert exact final-text and semantic-profile receipt integrity."""
    for item in results:
        if not isinstance(item, dict):
            continue
        source = str(
            item.get("_source_text_exact")
            or item.get("original_text")
            or item.get("clause_text")
            or item.get("quoted_text")
            or ""
        )
        profile_hash = build_source_evidence_model(source)["semantic_profile_hash"]
        receipts = item.get("validation_receipts") or {}

        for field in PROTECTED_FIELDS:
            text = str(item.get(field) or "")
            if not text.strip():
                continue
            receipt = receipts.get(field)
            if not receipt or receipt.get("successful") is not True:
                raise AssertionError(f"missing successful validation receipt for {field}")
            final_hash = _hash(text)
            if receipt.get("validated_text_hash") != final_hash:
                raise AssertionError(f"validated text hash mismatch for {field}")
            if receipt.get("final_text_hash") != final_hash:
                raise AssertionError(f"final text hash mismatch for {field}")
            if receipt.get("semantic_profile_hash") != profile_hash:
                raise AssertionError(f"semantic profile hash mismatch for {field}")
            if receipt.get("post_gate_mutators"):
                raise AssertionError(f"post-gate mutation recorded for {field}")
