"""
unified_summary_service.py

Full orchestration of the mandatory improvements (points 1-14).

Pipeline:
    1. Extract actual contractual definitions            (point 3)
    2. Detect contract family                             (point 5)
    3. Extract arbitration mechanics if present            (point 4)
    4. Single AI call producing the 7-section hierarchy   (point 1)
       with legal-reasoning, market-practice, negotiation,
       wording, and explainable-score rules baked into the
       prompt itself                                       (points 2,6,7,9,10,11,13,14)
    5. Code-level validation:
         - fill any missing keys defensively                (point 12)
         - de-duplicate overlapping sections                (point 1)
         - cross-check arbitration facts against output      (point 4)
         - enforce missing_clauses business_reason present   (point 8)
         - enforce risk_score explanation cites real ids     (point 7/13)

Replaces: generate_summary_data(), generate_simplified_version_data(),
build_executive_report(). Those three are kept as deprecated adapters at
the bottom of this file so existing callers don't break during migration.
"""

import re
import logging
from datetime import datetime, timezone

from app.utils.prompt_loader import load_prompt
from app.services.contract_agent.ai_client import call_json_ai
from app.services.contract_agent.definitions_extractor import (
    extract_definitions,
    build_definitions_block,
)
from app.services.contract_agent.contract_family_detector import (
    detect_contract_family,
    build_family_hint,
)
from app.services.contract_agent.arbitration_analyzer import (
    analyze_arbitration,
    build_arbitration_hint,
)

MAX_UNIFIED_CHARS = 14_000

SUPPORTED_LANGUAGES = {"en", "fr", "ar"}

DEFAULT_VALUES = {
    "not_specified": {
        "en": "Not specified",
        "fr": "Non spécifié",
        "ar": "غير محدد",
    },
    "not_applicable": {
        "en": "Not applicable",
        "fr": "Non applicable",
        "ar": "غير منطبق",
    },
    "unknown": {
        "en": "Unknown",
        "fr": "Inconnu",
        "ar": "غير معروف",
    },
}

logger = logging.getLogger(__name__)

ANALYSIS_ENGINE = "unified_contract_report_v2_international"

OPTIONAL_PAYMENT_FAMILIES = {
    "nda",
    "confidentiality",
    "power_of_attorney",
    "power of attorney",
    "corporate_resolution",
    "corporate resolution",
    "board_resolution",
    "board resolution",
    "ip_assignment",
    "ip assignment",
    "data_processing_addendum",
    "data processing addendum",
    "memorandum",
    "policy",
    "terms_of_use",
    "terms of use",
    "privacy_policy",
    "privacy policy",
    "bylaws",
    "minutes",
    "shareholder_resolution",
    "shareholder resolution",
}


def normalize_language(language: str) -> str:
    language = str(language or "en").lower().strip()
    return language if language in SUPPORTED_LANGUAGES else "en"


def localized_default(key: str, language: str = "en") -> str:
    language = normalize_language(language)
    return DEFAULT_VALUES.get(key, DEFAULT_VALUES["not_specified"]).get(language, DEFAULT_VALUES["not_specified"]["en"])


def current_analysis_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalize_family_key(value: str) -> str:
    return str(value or "").lower().strip().replace("-", "_")


def is_payment_optional_family(family: str) -> bool:
    normalized = normalize_family_key(family)
    return normalized in OPTIONAL_PAYMENT_FAMILIES


def normalize_default_text(value, language: str = "en", default_key: str = "not_specified") -> str:
    language = normalize_language(language)
    missing = {"", "not specified", "non spécifié", "غير محدد", "unknown", "inconnu", "غير معروف", "none", "null"}
    if value is None:
        return localized_default(default_key, language)
    text_value = str(value).strip()
    if text_value.lower() in missing:
        return localized_default(default_key, language)
    return text_value


def calculate_report_coverage(report: dict) -> float:
    if not isinstance(report, dict):
        return 0.0

    populated = 0
    total = len(REQUIRED_KEYS)

    for key in REQUIRED_KEYS:
        value = report.get(key)
        if value not in [None, "", [], {}]:
            populated += 1

    return round(populated / max(total, 1), 2)


def calculate_confidence_score(report: dict) -> int:
    coverage = calculate_report_coverage(report)
    notes = report.get("confidence_notes", []) if isinstance(report, dict) else []
    note_penalty = min(30, len(notes) * 5)
    score = int(coverage * 100) - note_penalty
    return max(0, min(score, 100))


def enrich_report_metadata(report: dict, language: str = "en") -> dict:
    language = normalize_language(language)

    report.setdefault("contract_version", "Not specified")
    report.setdefault("analysis_timestamp", current_analysis_timestamp())
    report.setdefault("analysis_engine", ANALYSIS_ENGINE)
    report["coverage"] = calculate_report_coverage(report)
    report["confidence_score"] = calculate_confidence_score(report)
    report["language"] = language

    return report



REQUIRED_KEYS = [
    "contract_family",
    "contract_overview",
    "executive_summary",
    "key_clauses",
    "risks_identified",
    "negotiation_priorities",
    "suggested_wording",
    "fallback_position",
    "action_checklist",
    "risk_score",
    "missing_clauses",
    "confidence_notes",
    "contract_version",
    "analysis_timestamp",
    "analysis_engine",
    "coverage",
    "confidence_score",
]


def build_empty_unified_report(language: str = "en") -> dict:
    language = normalize_language(language)

    not_specified = localized_default("not_specified", language)

    return {
        "contract_family": "unknown",
        "contract_overview": {
            "contract_type": not_specified,
            "parties": [not_specified],
            "duration": not_specified,
            "payment_terms": not_specified,
            "jurisdiction_detected": not_specified,
            "jurisdiction_note": "",
            "contract_complexity": "medium",
            "overall_balance": not_specified,
        },
        "executive_summary": "",
        "key_clauses": [],
        "risks_identified": [],
        "negotiation_priorities": [],
        "suggested_wording": [],
        "fallback_position": "",
        "action_checklist": [],
        "risk_score": {
            "value": 0,
            "explanation": "",
            "improves_if": "",
            "confidence": "low",
            "coverage": 0.0,
            "high_count": 0,
            "medium_count": 0,
            "low_count": 0,
        },
        "missing_clauses": [],
        "confidence_notes": [],
        "contract_version": not_specified,
        "analysis_timestamp": current_analysis_timestamp(),
        "analysis_engine": ANALYSIS_ENGINE,
        "coverage": 0.0,
        "confidence_score": 0,
        "language": language,
    }



# ---------------------------------------------------------------------
# Code-level validators (point 12: deterministic reasoning — never trust
# the model's compliance with a prompt rule alone when it can be checked).
# ---------------------------------------------------------------------

def _fill_missing_keys(data: dict) -> dict:
    empty = build_empty_unified_report()
    for key in REQUIRED_KEYS:
        if key not in data or data[key] is None:
            data[key] = empty[key]
    return data


def _token_overlap(a: str, b: str) -> float:
    ta, tb = set((a or "").lower().split()), set((b or "").lower().split())
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / min(len(ta), len(tb))




def _sentence_units(text: str) -> list[str]:
    raw = str(text or "")
    units = re.split(r"(?<=[.!?؟])\s+", raw)
    return [u.strip() for u in units if u.strip()]


def _dedupe_sentence_overlap(primary: str, secondary: str, threshold: float = 0.82) -> str:
    kept = []

    for sentence in _sentence_units(primary):
        if _token_overlap(sentence, secondary) <= threshold:
            kept.append(sentence)

    return " ".join(kept).strip() or primary


def _dedupe_sections(data: dict) -> dict:
    """Point 1: enforce non-redundancy even if the model drifts."""
    summary = data.get("executive_summary", "")

    for risk in data.get("risks_identified", []):
        explanation = risk.get("explanation", "")

        if _token_overlap(summary, explanation) > 0.8:
            data["executive_summary"] = _dedupe_sentence_overlap(summary, explanation)
            summary = data["executive_summary"]

    return data



def _enforce_missing_clause_reasons(data: dict) -> dict:
    """Point 8: every missing-clause recommendation must carry a business reason or equivalent risk explanation."""
    cleaned = []

    for item in data.get("missing_clauses", []):
        if not isinstance(item, dict):
            data.setdefault("confidence_notes", []).append(
                f"Dropped invalid missing_clauses entry: {item}"
            )
            continue

        has_reason = any(
            str(item.get(field, "")).strip()
            for field in [
                "business_reason",
                "why_missing",
                "risk_if_missing",
                "recommended_wording",
            ]
        )

        if has_reason:
            cleaned.append(item)
        else:
            data.setdefault("confidence_notes", []).append(
                f"Dropped missing_clauses entry without a business reason or risk explanation: {item}"
            )

    data["missing_clauses"] = cleaned

    return data



def _enforce_risk_score_explainability(data: dict) -> dict:
    """Point 7/13: the score must be explainable and reference real risk ids."""
    risk_score = data.get("risk_score", {}) or {}
    risks = data.get("risks_identified", []) or []
    risk_ids = {r.get("id") for r in risks if isinstance(r, dict)}
    explanation = risk_score.get("explanation", "")

    cites_a_real_id = any(
        rid and rid in explanation
        for rid in risk_ids
    )

    if risks and not cites_a_real_id:
        data.setdefault("confidence_notes", []).append(
            "risk_score.explanation did not reference a specific risk id; "
            "score may not be fully traceable to risks_identified."
        )

    high_count = sum(1 for r in risks if isinstance(r, dict) and r.get("risk_level") == "high")
    medium_count = sum(1 for r in risks if isinstance(r, dict) and r.get("risk_level") == "medium")
    low_count = sum(1 for r in risks if isinstance(r, dict) and r.get("risk_level") == "low")

    risk_score.setdefault("high_count", high_count)
    risk_score.setdefault("medium_count", medium_count)
    risk_score.setdefault("low_count", low_count)
    risk_score.setdefault("coverage", calculate_report_coverage(data))
    risk_score.setdefault(
        "confidence",
        "high" if calculate_confidence_score(data) >= 80 else "medium" if calculate_confidence_score(data) >= 55 else "low",
    )

    data["risk_score"] = risk_score

    return data



def _cross_check_arbitration(data: dict, arbitration_facts: dict | None) -> dict:
    """
    Point 4: if the rule-based extractor found arbitration mechanics that
    never surface anywhere in the model's key_clauses/risks_identified
    text, flag it instead of silently trusting the model covered it.
    """
    if not arbitration_facts:
        return data

    combined_text = " ".join(
        [data.get("executive_summary", "")]
        + [kc.get("why_it_matters", "") for kc in data.get("key_clauses", []) if isinstance(kc, dict)]
        + [r.get("explanation", "") for r in data.get("risks_identified", []) if isinstance(r, dict)]
        + [str(data.get("contract_overview", {}).get("jurisdiction_note", ""))]
    ).lower()

    checks = {
        "seat": arbitration_facts.get("seat"),
        "institution": ", ".join(arbitration_facts.get("institution") or []),
        "language": arbitration_facts.get("language"),
        "governing_law": arbitration_facts.get("governing_law"),
        "number_of_arbitrators": arbitration_facts.get("number_of_arbitrators"),
        "emergency_arbitrator": arbitration_facts.get("emergency_arbitrator"),
        "expedited_procedure": arbitration_facts.get("expedited_procedure"),
        "consolidation": arbitration_facts.get("consolidation"),
        "interim_measures": arbitration_facts.get("interim_measures"),
    }

    for label, value in checks.items():
        if value is None or value == "" or value == []:
            continue

        value_text = ", ".join(value) if isinstance(value, list) else str(value)

        if value_text and value_text.lower() not in combined_text:
            data.setdefault("confidence_notes", []).append(
                f"Arbitration {label} ('{value_text}') was found in the contract text but not "
                f"explicitly discussed in the analysis output — verify coverage."
            )

    return data



def _build_prompt(contract_text: str, language: str) -> tuple[str, dict | None]:
    language = normalize_language(language)
    prompt_template = load_prompt("unified_report_prompt.txt")

    definitions = extract_definitions(contract_text)
    family_detection = detect_contract_family(contract_text)
    arbitration_facts = analyze_arbitration(contract_text)

    filled = (
        prompt_template
        .replace("{definitions_block}", build_definitions_block(definitions))
        .replace("{family_hint}", build_family_hint(family_detection))
        .replace("{arbitration_hint}", build_arbitration_hint(arbitration_facts))
        .replace("{contract_text}", contract_text)
    )

    prompt = f"""
{filled}

Output language: {language}

LANGUAGE CONSISTENCY:
Translate every generated JSON value into {language}. Preserve anonymized
party identities ([PERSON], [ORGANIZATION], [PARTY_1], [PARTY_2], [PARTY_3]),
dates, amounts, article references, and court names exactly as provided.

PRIVACY-FIRST RULE:
Never reconstruct, infer, restore, request, or output real names, emails, addresses, phone numbers, identifiers, or other personal data. Always preserve anonymized placeholders exactly as received.

DEFAULT VALUE RULE:
Use localized default values only:
- en: Not specified / Not applicable / Unknown
- fr: Non spécifié / Non applicable / Inconnu
- ar: غير محدد / غير منطبق / غير معروف
""".strip()

    return prompt, arbitration_facts


def generate_unified_report(text: str, language: str = "en") -> dict:
    language = normalize_language(language)
    if not text or not text.strip():
        return enrich_report_metadata(build_empty_unified_report(language), language)

    contract_text = text[:MAX_UNIFIED_CHARS]
    prompt, arbitration_facts = _build_prompt(contract_text, language)

    try:
        data = call_json_ai(prompt, temperature=0.0)
    except Exception as e:
        logger.exception("Unified report AI error: %s", e)
        return enrich_report_metadata(build_empty_unified_report(language), language)

    data = _fill_missing_keys(data)

    family_key = normalize_family_key(data.get("contract_family", ""))
    overview = data.get("contract_overview", {}) or {}

    if is_payment_optional_family(family_key):
        payment_terms = overview.get("payment_terms")
        if not payment_terms or str(payment_terms).lower() in {"not specified", "non spécifié", "غير محدد"}:
            overview["payment_terms"] = localized_default("not_applicable", language)
            data["contract_overview"] = overview

    data = _dedupe_sections(data)
    data = _enforce_missing_clause_reasons(data)
    data = _enforce_risk_score_explainability(data)
    data = _cross_check_arbitration(data, arbitration_facts)
    data = enrich_report_metadata(data, language)
    return data


# ---------------------------------------------------------------------
# Legacy-schema converters.
#
# IMPORTANT: these take an ALREADY-GENERATED report and reshape it in pure
# Python — they make NO additional AI call. This is deliberate: calling
# generate_unified_report() once per legacy field (as an earlier draft of
# this module did) would silently reintroduce the exact redundancy problem
# (point 1) that this whole pipeline exists to remove. Callers must call
# generate_unified_report() exactly once per contract, then derive whatever
# legacy shapes they need from that single result.
# ---------------------------------------------------------------------

def to_legacy_summary_data(report: dict, language: str = "en") -> dict:
    language = normalize_language(language)
    """
    Reshapes a unified report into the exact dict shape
    summary_service.render_summary_text() expects, so the existing
    formatter keeps working unmodified while the underlying generation
    is now the deduplicated, definitions-first, family-aware pipeline.
    """
    overview = report.get("contract_overview", {})
    negotiation = report.get("negotiation_priorities", [])
    risks = report.get("risks_identified", [])

    return {
        "contract_type": overview.get("contract_type", "Not specified"),
        "parties": overview.get("parties", ["Not specified"]),
        "duration": overview.get("duration", "Not specified"),
        "payment_terms": overview.get("payment_terms", "Not specified"),
        "main_obligations": [
            kc.get("why_it_matters", "")
            for kc in report.get("key_clauses", [])
            if isinstance(kc, dict) and kc.get("why_it_matters")
        ] or [
            a.get("action", "")
            for a in report.get("action_checklist", [])
            if isinstance(a, dict) and a.get("action")
        ],
        "global_summary": report.get("executive_summary", ""),
        "important_points": [kc["why_it_matters"] for kc in report.get("key_clauses", [])],
        "missing_clauses": [
            (
                f"{m.get('clause_type', 'unknown')}: "
                f"{m.get('business_reason') or m.get('risk_if_missing') or m.get('why_missing') or ''}"
            ).strip()
            for m in report.get("missing_clauses", [])
            if isinstance(m, dict)
        ],
        "dangerous_patterns": [r["explanation"] for r in risks if r.get("risk_level") == "high"],
        "contract_quality_score": report.get("risk_score", {}).get("value", 0),
        "overall_balance": overview.get("overall_balance", "Not specified"),
        "negotiation_priorities": [n.get("what_should_change", "") for n in negotiation],
        "key_risks": [r.get("explanation", "") for r in risks],
        "practical_decision": report.get("fallback_position", ""),
        "jurisdiction_detected": overview.get("jurisdiction_detected", "Not specified"),
        "jurisdiction_note": overview.get("jurisdiction_note", ""),
        "recommended_actions": [a.get("action", "") for a in report.get("action_checklist", [])],
        "contract_complexity": overview.get("contract_complexity", "medium"),
    }


def to_legacy_simplified_string(report: dict, language: str = "en") -> str:
    language = normalize_language(language)
    """
    Reshapes a unified report into the plain string
    generate_simplified_version() used to return — WITHOUT re-running the
    simplification generation, since the unified report already contains
    the same information without the duplicated narrative.
    """
    labels = {
        "en": "Things to watch",
        "fr": "Points à surveiller",
        "ar": "نقاط يجب الانتباه لها",
    }
    label = labels.get(language, labels["en"])

    output = report.get("executive_summary", "")
    watch_items = [r["explanation"] for r in report.get("risks_identified", []) if r.get("risk_level") != "low"]
    if watch_items:
        output += f"\n\n{label}:\n" + "\n".join(f"- {item}" for item in watch_items)
    return output.strip()


# ---------------------------------------------------------------------
# Deprecated single-call adapters — kept ONLY for call sites that cannot
# be updated immediately. Each one calls generate_unified_report() on its
# own, so using BOTH generate_summary_data() and generate_simplified_version()
# in the same request still makes two AI calls. Prefer calling
# generate_unified_report() once and using to_legacy_summary_data() /
# to_legacy_simplified_string() above instead.
# ---------------------------------------------------------------------

def generate_summary_data(text: str, language: str = "en") -> dict:
    language = normalize_language(language)
    report = generate_unified_report(text, language)
    return to_legacy_summary_data(report, language)


def generate_simplified_version(text: str, language: str = "en") -> str:
    language = normalize_language(language)
    report = generate_unified_report(text, language)
    return to_legacy_simplified_string(report, language)
