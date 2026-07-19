from __future__ import annotations

import ast
import hashlib
import shutil
from datetime import datetime
from pathlib import Path


TARGET = Path(
    "app/services/contract_agent/executive_summary.py"
)


def sha256(path: Path) -> str:
    return hashlib.sha256(
        path.read_bytes()
    ).hexdigest()


if not TARGET.exists():
    raise SystemExit(
        f"TARGET NOT FOUND: {TARGET}"
    )


source = TARGET.read_text(
    encoding="utf-8"
)


old = '''                "legal_insight": (
                    get_clause_type_description(
                        c.get("clause_type"),
                        language,
                    )
                    or (
                        get_clause_type_description(
                            "limitation_of_liability_exceptions",
                            language,
                        )
                        if clause_title(c).lower() == "limitation of liability exceptions"
                        else ""
                    )
                    or c.get("legal_insight")
                    or c.get("explanation_simple")
                ),'''


new = '''                "legal_insight": select_top_risk_publication_text(
                    c,
                    language,
                ),'''


if old not in source:
    raise SystemExit(
        "EXPECTED TOP-RISK BLOCK NOT FOUND; "
        "NO FILE MODIFIED"
    )


anchor = '''def build_executive_summary(
'''


helper = r'''
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
'''


if anchor not in source:
    raise SystemExit(
        "BUILD EXECUTIVE SUMMARY ANCHOR NOT FOUND; "
        "NO FILE MODIFIED"
    )


if "def select_top_risk_publication_text(" in source:
    raise SystemExit(
        "V4.1.17A HELPER ALREADY PRESENT; "
        "NO FILE MODIFIED"
    )


timestamp = datetime.now().strftime(
    "%Y%m%d_%H%M%S"
)

backup = TARGET.with_name(
    TARGET.name
    + ".before_v4_1_17a_"
    + timestamp
)


shutil.copy2(
    TARGET,
    backup,
)


source = source.replace(
    anchor,
    helper + "\n\n" + anchor,
    1,
)


source = source.replace(
    old,
    new,
    1,
)


ast.parse(source)


TARGET.write_text(
    source,
    encoding="utf-8",
)


print("=" * 96)
print(
    "V4.1.17A EXECUTIVE TOP-RISK "
    "PUBLICATION INVARIANT APPLIED"
)
print("=" * 96)
print("TARGET :", TARGET)
print("BACKUP :", backup)
print("SHA256 :", sha256(TARGET))
print(
    "A: clause-specific risk evidence "
    "preferred over taxonomy prose"
)
print(
    "B: EN/FR/AR internal diagnostics "
    "blocked from Top Risks"
)
print(
    "C: generic report prose demoted "
    "to fallback-only"
)
print(
    "D: clause-type descriptions retained "
    "as safe backward-compatible fallback"
)
print(
    "UNTOUCHED: semantic profile, RULES, "
    "thresholds, evidence engine, "
    "publication gate, risk scoring, "
    "taxonomy, frontend"
)
print("AST: OK")