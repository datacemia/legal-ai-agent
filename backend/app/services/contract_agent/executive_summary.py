from __future__ import annotations

from copy import deepcopy
from typing import Any

from app.services.contract_agent.contract_taxonomy import (
    get_clause_type_description,
)

from app.services.contract_agent.jurisdiction_profiles import (
    detect_jurisdiction,
    summarize_jurisdiction_detection,
)


SUPPORTED_LANGUAGES = {"en", "fr", "ar"}

RISK_NORMALIZATION = {
    "critical": "high",
    "very_high": "high",
    "high": "high",
    "medium": "medium",
    "moderate": "medium",
    "low": "low",
    "none": "low",
    "informational": "low",
}


def safe_str(value: Any) -> str:
    return str(value or "").strip()


def safe_list(value: Any) -> list:
    return value if isinstance(value, list) else []


def clause_title(clause: dict) -> str:
    return (
        safe_str(clause.get("clause_title"))
        or safe_str(clause.get("title"))
        or safe_str(clause.get("name"))
        or "Untitled clause"
    )


def normalize_risk_level(level: Any) -> str:
    return RISK_NORMALIZATION.get(
        safe_str(level).lower(),
        "low",
    )


def risk_rank(level: Any) -> int:
    return {
        "high": 3,
        "medium": 2,
        "low": 1,
    }.get(
        normalize_risk_level(level),
        0,
    )


def dependency_edges_count(
    dependency_graph: dict | None = None,
) -> int:
    graph = dependency_graph or {}

    edges = graph.get("edges")

    if isinstance(edges, list):
        return len(edges)

    try:
        return int(graph.get("edges_count", 0) or 0)
    except (TypeError, ValueError):
        return 0



_INTERNAL_PUBLICATION_DIAGNOSTIC_MARKERS = {
    "en": (
        "manual review required",
        "generated text did not pass",
        "source fidelity validation",
        "automated analysis failed",
        "could not parse ai response",
    ),
    "fr": (
        "revue manuelle requise",
        "examen manuel requis",
        "texte généré n'a pas passé",
        "texte généré n’a pas passé",
        "validation de fidélité à la source",
        "l'analyse automatique a échoué",
        "l’analyse automatique a échoué",
        "impossible d’analyser correctement la réponse de l’ia",
    ),
    "ar": (
        "مراجعة يدوية مطلوبة",
        "راجع هذه المادة يدوياً",
        "راجع هذه المادة يدويًا",
        "لم يجتز النص المولد",
        "التحقق من مطابقته للمصدر",
        "فشل التحليل التلقائي",
        "تعذر تحليل رد الذكاء الاصطناعي",
    ),
}


_GENERIC_TOP_RISK_MARKERS = {
    "en": (
        "this clause may create legal or operational exposure",
        "this clause should be reviewed because it may affect",
        "creates contractual or operational obligations that should be reviewed",
    ),
    "fr": (
        "cette clause peut créer une exposition juridique ou opérationnelle",
        "cette clause peut créer une exposition juridique ou opérationnelle.",
        "cette clause doit être examinée car elle peut affecter",
        "crée des obligations contractuelles ou opérationnelles qui doivent être examinées",
    ),
    "ar": (
        "قد تنشئ هذه المادة تعرضاً قانونياً أو تشغيلياً",
        "قد تنشئ هذه المادة تعرضًا قانونيًا أو تشغيليًا",
        "ينبغي مراجعة هذه المادة لأنها قد تؤثر",
        "تنشئ التزامات تعاقدية أو تشغيلية ينبغي مراجعتها",
    ),
}


def _normalize_publication_language(language: str) -> str:
    value = str(language or "en").strip().lower()

    if value.startswith("fr"):
        return "fr"

    if value.startswith("ar"):
        return "ar"

    return "en"


def _clean_top_risk_candidate(value) -> str:
    return " ".join(
        str(value or "").split()
    ).strip()


def _contains_publication_marker(
    text: str,
    markers: tuple[str, ...],
) -> bool:
    normalized = text.casefold()

    return any(
        marker.casefold() in normalized
        for marker in markers
    )


def _is_internal_publication_diagnostic(
    text: str,
    language: str,
) -> bool:
    lang = _normalize_publication_language(
        language
    )

    markers = (
        _INTERNAL_PUBLICATION_DIAGNOSTIC_MARKERS[
            lang
        ]
        + _INTERNAL_PUBLICATION_DIAGNOSTIC_MARKERS[
            "en"
        ]
    )

    return _contains_publication_marker(
        text,
        markers,
    )


def _is_generic_top_risk_text(
    text: str,
    language: str,
) -> bool:
    lang = _normalize_publication_language(
        language
    )

    markers = (
        _GENERIC_TOP_RISK_MARKERS[lang]
        + _GENERIC_TOP_RISK_MARKERS["en"]
    )

    return _contains_publication_marker(
        text,
        markers,
    )


def select_top_risk_publication_text(
    clause: dict,
    language: str,
) -> str:
    """
    Select the first substantive publication-safe explanation for a top risk.

    Invariant:
    - never publish internal validation diagnostics;
    - prefer clause-specific risk/exposure evidence;
    - generic taxonomy prose is fallback-only;
    - EN / FR / AR compatible;
    - contract-family and jurisdiction neutral.
    """
    language = _normalize_publication_language(
        language
    )

    primary_fields = (
        "risk_reason",
        "why_it_matters",
        "business_impact",
        "commercial_impact",
        "operational_impact",
        "legal_insight",
        "explanation_simple",
    )

    generic_fallback = ""

    for field in primary_fields:
        candidate = _clean_top_risk_candidate(
            clause.get(field)
        )

        if not candidate:
            continue

        if _is_internal_publication_diagnostic(
            candidate,
            language,
        ):
            continue

        if _is_generic_top_risk_text(
            candidate,
            language,
        ):
            if not generic_fallback:
                generic_fallback = candidate
            continue

        return candidate

    clause_type_description = (
        get_clause_type_description(
            clause.get("clause_type"),
            language,
        )
        or (
            get_clause_type_description(
                "limitation_of_liability_exceptions",
                language,
            )
            if clause_title(clause).lower()
            == "limitation of liability exceptions"
            else ""
        )
    )

    clause_type_description = (
        _clean_top_risk_candidate(
            clause_type_description
        )
    )

    if (
        clause_type_description
        and not _is_internal_publication_diagnostic(
            clause_type_description,
            language,
        )
    ):
        return clause_type_description

    red_flag_reason = _clean_top_risk_candidate(
        clause.get("red_flag_reason")
    )

    if (
        red_flag_reason
        and not _is_internal_publication_diagnostic(
            red_flag_reason,
            language,
        )
        and not _is_generic_top_risk_text(
            red_flag_reason,
            language,
        )
    ):
        return red_flag_reason

    return generic_fallback


def build_executive_summary(
    clauses: list[dict],
    dependency_graph: dict | None = None,
    language: str = "en",
    contract_text: str = "",
) -> dict:
    """
    International, privacy-first executive summary.

    - Works for any contract family and industry.
    - EN / FR / AR compatible.
    - Never reconstructs or infers personal data.
    - Does not mutate input clauses.
    - Uses the final dependency graph as the single dependency-count source.
    """

    language = language if language in SUPPORTED_LANGUAGES else "en"
    dependency_graph = dependency_graph or {}

    normalized = []

    for c in safe_list(clauses):
        if not isinstance(c, dict):
            continue

        item = deepcopy(c)
        item["_normalized_risk_level"] = normalize_risk_level(
            item.get("risk_level")
        )

        normalized.append(item)

    high = [
        c for c in normalized
        if c["_normalized_risk_level"] == "high"
    ]

    medium = [
        c for c in normalized
        if c["_normalized_risk_level"] == "medium"
    ]

    low = [
        c for c in normalized
        if c["_normalized_risk_level"] == "low"
    ]

    ranked = sorted(
        [
            c for c in normalized
            if c["_normalized_risk_level"] in {"high", "medium"}
        ],
        key=lambda c: (
            risk_rank(c["_normalized_risk_level"]),
            c.get("importance_score") or 0,
        ),
        reverse=True,
    )[:5]

    negotiation = sorted(
        [
            c for c in normalized
            if any(
                c.get(k)
                for k in (
                    "recommendation",
                    "negotiation_advice",
                    "safer_alternative",
                    "fallback_position",
                )
            )
        ],
        key=lambda c: (
            risk_rank(c["_normalized_risk_level"]),
            c.get("importance_score") or 0,
        ),
        reverse=True,
    )[:5]

    actions = []

    for c in negotiation:
        action = (
            safe_str(c.get("recommendation"))
            or safe_str(c.get("negotiation_advice"))
            or safe_str(c.get("safer_alternative"))
            or safe_str(c.get("fallback_position"))
        )

        if action:
            actions.append({
                "title": clause_title(c),
                "risk_level": c["_normalized_risk_level"],
                "action": action,
            })

    edges = safe_list(
        dependency_graph.get("edges")
    )

    final_edges_count = dependency_edges_count(
        dependency_graph
    )

    jurisdiction_detection = (
        detect_jurisdiction(contract_text, language)
        if contract_text
        else {}
    )

    jurisdiction_summary = (
        summarize_jurisdiction_detection(
            jurisdiction_detection,
            language,
        )
        if jurisdiction_detection
        else ""
    )

    return {
        "language": language,
        "privacy_first": True,
        "jurisdiction": jurisdiction_detection,
        "jurisdiction_summary": jurisdiction_summary,
        "risk_overview": {
            "high": len(high),
            "medium": len(medium),
            "low": len(low),
        },
        "top_risks": [
            {
                "title": clause_title(c),
                "risk_level": c["_normalized_risk_level"],
                "importance_score": c.get("importance_score"),
                "legal_insight": select_top_risk_publication_text(
                    c,
                    language,
                ),
            }
            for c in ranked
        ],
        "negotiation_priorities": [
            {
                "title": clause_title(c),
                "risk_level": c["_normalized_risk_level"],
                "recommendation": c.get("recommendation"),
                "negotiation_advice": c.get("negotiation_advice"),
                "safer_alternative": c.get("safer_alternative"),
                "fallback_position": c.get("fallback_position"),
            }
            for c in negotiation
        ],
        "recommended_actions": actions,
        "dependency_summary": {
            "edges_count": final_edges_count,
            "key_dependencies": edges[:5],
        },
    }
