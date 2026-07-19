#!/usr/bin/env python3
from __future__ import annotations

import ast
import shutil
from datetime import datetime
from pathlib import Path


TARGET = Path(
    "app/services/contract_agent/unified_report_from_pipeline.py"
)


GENERIC_MARKERS = r'''GENERIC_REPORT_TEXT_MARKERS = {
    "en": (
        "this clause may create legal or operational exposure",
        "this clause should be reviewed because it may affect",
        "this clause appears administrative or operational in nature",
        "this clause is primarily administrative or definitional",
        "review this clause in the context of the overall contract",
        "consistent with the commercial objective",
        "commercial objectives, operational processes and overall risk allocation",
        "commercial objective, operational processes and overall risk allocation",
        "legal, financial, or operational obligations",
        "legal, financial or operational obligations",
        "manual review required",
        "review manually",
        "source-fidelity validation",
        "source fidelity validation",
        "publication validation failed",
        "publication gate",
        "block_and_replace",
        "internal replacement",
        "blocked status",
    ),
    "fr": (
        "cette clause peut créer une exposition juridique ou opérationnelle",
        "cette clause doit être examinée car elle peut affecter",
        "cette clause semble de nature administrative ou opérationnelle",
        "cette clause est principalement administrative ou définitionnelle",
        "examiner cette clause dans le contexte global du contrat",
        "cohérente avec l'objectif commercial",
        "cohérent avec l'objectif commercial",
        "les processus opérationnels et la répartition globale des risques",
        "obligations juridiques, financières ou opérationnelles",
        "obligations juridiques, financières, ou opérationnelles",
        "examen manuel requis",
        "revue manuelle requise",
        "révision manuelle requise",
        "validation de fidélité à la source",
        "validation de fidelite a la source",
        "fidélité à la source",
        "fidelite a la source",
        "échec de la validation de publication",
        "echec de la validation de publication",
        "publication gate",
        "block_and_replace",
        "remplacement interne",
        "statut bloqué",
        "statut bloque",
    ),
    "ar": (
        "قد ينشئ هذا البند تعرضاً قانونياً أو تشغيلياً",
        "قد ينشئ هذا البند تعرضًا قانونيًا أو تشغيليًا",
        "ينبغي مراجعة هذا البند لأنه قد يؤثر",
        "يبدو هذا البند إدارياً أو تشغيلياً",
        "يبدو هذا البند إداريًا أو تشغيليًا",
        "هذا البند إداري أو تعريفي في المقام الأول",
        "مراجعة هذا البند في سياق العقد ككل",
        "متسقاً مع الهدف التجاري",
        "متسقًا مع الهدف التجاري",
        "العمليات التشغيلية والتوزيع العام للمخاطر",
        "التزامات قانونية أو مالية أو تشغيلية",
        "مراجعة يدوية مطلوبة",
        "المراجعة اليدوية مطلوبة",
        "التحقق من مطابقته للمصدر",
        "التحقق من مطابقة المصدر",
        "فشل التحقق من النشر",
        "بوابة النشر",
        "block_and_replace",
        "استبدال داخلي",
        "حالة محظورة",
    ),
}'''


ROLE_HELPER = r'''def normalize_published_role_text(
    value: str,
    language: str = "en",
) -> str:
    """
    Final publication-only role localization.

    This function is intentionally lexical and never applies to original_text,
    quoted_text, or exact source evidence. It removes generic party-role leakage
    from already-generated report prose in EN / FR / AR.
    """
    language = normalize_language(language)
    text = normalize_report_text(value)

    if not text:
        return ""

    if language == "fr":
        replacements = (
            (r"\bservice\s+provider\b", "Prestataire"),
            (r"\bprovider\b", "Prestataire"),
            (r"\bcustomer\b", "Client"),
        )

        for pattern, target in replacements:
            text = re.sub(
                pattern,
                target,
                text,
                flags=re.IGNORECASE,
            )

        # Canonical publication labels Client / Prestataire are masculine.
        text = re.sub(
            r"\b[Ll]a\s+(Client|Prestataire)\b",
            r"le \1",
            text,
        )
        text = re.sub(
            r"\b[Dd]e\s+la\s+(Client|Prestataire)\b",
            r"du \1",
            text,
        )
        text = re.sub(
            r"\b[Àà]\s+la\s+(Client|Prestataire)\b",
            r"au \1",
            text,
        )
        text = re.sub(
            r"\b[Dd]u\s+Provider\b",
            "du Prestataire",
            text,
            flags=re.IGNORECASE,
        )
        text = re.sub(
            r"\b[Ll]e\s+Provider\b",
            "le Prestataire",
            text,
            flags=re.IGNORECASE,
        )

    elif language == "ar":
        replacements = (
            (r"\bservice\s+provider\b", "مزود الخدمة"),
            (r"\bprovider\b", "مزود الخدمة"),
            (r"\bprestataire\b", "مزود الخدمة"),
            (r"\bcustomer\b", "العميل"),
            (r"\bclient\b", "العميل"),
        )

        for pattern, target in replacements:
            text = re.sub(
                pattern,
                target,
                text,
                flags=re.IGNORECASE,
            )

    else:
        text = re.sub(
            r"\bprestataire\b",
            "Provider",
            text,
            flags=re.IGNORECASE,
        )

    return normalize_report_text(text)


def finalize_published_text(
    value: str,
    language: str = "en",
) -> str:
    """
    Last-mile publication invariant shared by unified and legacy buckets.
    """
    language = normalize_language(language)
    value = normalize_published_role_text(
        value,
        language,
    )

    if not value:
        return ""

    if is_generic_report_text(value, language):
        return ""

    return value'''


SEMANTIC_HELPERS = r'''def _canonical_report_type(value: str) -> str:
    value = normalize_family_name_for_optional_fields(
        value,
    )

    aliases = {
        "cybersecurity": "security",
        "cyber_security": "security",
        "information_security": "security",
        "data_processing": "data_protection",
        "privacy": "data_protection",
        "non_compete": "restrictive_covenants",
        "non_solicitation": "restrictive_covenants",
    }

    return aliases.get(value, value)


def clause_semantic_candidate_types(
    clause: dict,
) -> set[str]:
    """
    Read semantic candidate types already attached to the clause.

    No new analysis is run here. The helper is deliberately permissive:
    primary type and all grounded mechanism candidate types are accepted.
    If semantic metadata is absent, callers preserve historical behavior.
    """
    found: set[str] = set()

    containers = [
        clause.get("semantic_source_profile"),
        clause.get("source_semantic_profile"),
        clause.get("source_evidence_model"),
        clause.get("_semantic_source_profile"),
    ]

    for container in containers:
        if not isinstance(container, dict):
            continue

        for key in (
            "primary_type",
            "candidate_primary_type",
        ):
            value = _canonical_report_type(
                container.get(key, "")
            )
            if value and value not in {
                "unknown",
                "other",
                "general",
            }:
                found.add(value)

        for list_key in (
            "mechanisms",
            "supporting_mechanisms",
            "ranked_material_mechanisms",
        ):
            for mechanism in (
                container.get(list_key)
                or []
            ):
                if not isinstance(mechanism, dict):
                    continue

                value = _canonical_report_type(
                    mechanism.get(
                        "candidate_primary_type",
                        "",
                    )
                    or mechanism.get(
                        "primary_type",
                        "",
                    )
                )

                if value and value not in {
                    "unknown",
                    "other",
                    "general",
                }:
                    found.add(value)

    return found


def clause_type_semantically_supported(
    clause: dict,
) -> bool:
    semantic_types = clause_semantic_candidate_types(
        clause,
    )

    # Preserve historical output when semantic metadata is unavailable.
    if not semantic_types:
        return True

    clause_type = _canonical_report_type(
        clause.get("clause_type", "")
    )

    if not clause_type or clause_type in {
        "unknown",
        "other",
        "general",
    }:
        return False

    return clause_type in semantic_types


DANGEROUS_PATTERN_MARKERS = {
    "en": (
        "unlimited",
        "uncapped",
        "without limitation",
        "sole discretion",
        "unilateral",
        "without notice",
        "without a cure",
        "no opportunity to cure",
        "waive",
        "waiver of",
        "exclusive remedy",
        "broad indemn",
        "all losses",
        "consequential damages",
        "indirect damages",
        "liquidated damages",
        "penalty",
        "non-refundable",
        "automatic renewal",
        "irrevocable",
        "perpetual",
        "immediate termination",
    ),
    "fr": (
        "illimitée",
        "illimitee",
        "sans limitation",
        "seule discrétion",
        "seule discretion",
        "unilatéral",
        "unilateral",
        "sans préavis",
        "sans preavis",
        "sans possibilité de régularisation",
        "sans possibilite de regularisation",
        "aucune possibilité de remédier",
        "aucune possibilite de remedier",
        "renonce",
        "renonciation",
        "recours exclusif",
        "indemnisation générale",
        "indemnisation generale",
        "toutes les pertes",
        "dommages indirects",
        "dommages consécutifs",
        "dommages consecutifs",
        "dommages-intérêts forfaitaires",
        "dommages-interets forfaitaires",
        "pénalité",
        "penalite",
        "non remboursable",
        "renouvellement automatique",
        "irrévocable",
        "irrevocable",
        "perpétuel",
        "perpetuel",
        "résiliation immédiate",
        "resiliation immediate",
    ),
    "ar": (
        "غير محدودة",
        "دون حد",
        "بدون حد",
        "وفق تقديره المنفرد",
        "من جانب واحد",
        "دون إشعار",
        "بدون إشعار",
        "دون مهلة للمعالجة",
        "بدون مهلة للمعالجة",
        "لا فرصة للمعالجة",
        "تنازل",
        "سبيل الانتصاف الحصري",
        "تعويض واسع",
        "جميع الخسائر",
        "الأضرار غير المباشرة",
        "الأضرار التبعية",
        "تعويضات مقطوعة",
        "غرامة",
        "غير قابل للاسترداد",
        "تجديد تلقائي",
        "غير قابل للإلغاء",
        "دائم",
        "إنهاء فوري",
    ),
}


def risk_is_dangerous_pattern(
    risk: dict,
    language: str = "en",
) -> bool:
    if bool(risk.get("red_flag")):
        return True

    language = normalize_language(language)

    text = " ".join(
        normalize_report_text(
            risk.get(field, "")
        ).lower()
        for field in (
            "explanation",
            "risk_reason",
            "red_flag_reason",
        )
    )

    if not text:
        return False

    return any(
        marker in text
        for marker in DANGEROUS_PATTERN_MARKERS[
            language
        ]
    )'''


SELECTOR = r'''def select_clause_report_text(
    clause: dict,
    language: str = "en",
    *,
    purpose: str = "explanation",
) -> str:
    """
    Select one already-produced field by purpose and publication suitability.

    Internal diagnostics and generic legal/business filler are skipped. For
    type-specific negotiation guidance, a contradictory semantic profile
    prevents publication of the advice. Missing semantic metadata preserves
    the historical path.
    """
    language = normalize_language(language)

    field_orders = {
        "explanation": (
            "explanation_simple",
            "why_it_matters",
            "legal_insight",
            "business_impact",
            "commercial_impact",
            "operational_impact",
        ),
        "risk": (
            "risk_reason",
            "business_impact",
            "commercial_impact",
            "operational_impact",
            "legal_insight",
            "explanation_simple",
            "why_it_matters",
        ),
        "action": (
            "recommendation",
            "negotiation_advice",
            "safer_alternative",
        ),
        "negotiation": (
            "negotiation_advice",
            "recommendation",
            "safer_alternative",
        ),
    }

    type_specific_purposes = {
        "negotiation",
    }

    if (
        purpose in type_specific_purposes
        and not clause_type_semantically_supported(
            clause,
        )
    ):
        return ""

    for field in field_orders.get(
        purpose,
        field_orders["explanation"],
    ):
        value = finalize_published_text(
            clause.get(field, ""),
            language,
        )

        if value:
            return value

    return ""'''


RISKS = r'''def build_risks_identified(
    clauses: list,
    language: str = "en",
) -> list:
    risks = []
    language = normalize_language(language)

    for i, clause in enumerate(clauses):
        risk_level = str(
            clause.get("risk_level", "low")
        ).lower()

        if (
            risk_level == "low"
            and not clause.get("red_flag")
        ):
            continue

        explanation = select_clause_report_text(
            clause,
            language,
            purpose="risk",
        )

        if not explanation:
            continue

        risks.append({
            "id": f"risk_{_clause_id(clause, i)}",
            "clause_ref": _clause_id(clause, i),
            "title": (
                clause.get("clause_title")
                or clause.get("title")
                or ""
            ),
            "clause_type": clause.get(
                "clause_type",
                "other",
            ),
            "risk_level": risk_level,
            "market_practice": infer_market_practice(
                clause
            ),
            "market_practice_score": clause.get(
                "market_practice_score"
            ),
            "exposure": infer_exposure_dimensions(
                clause,
                risk_level,
            ),
            "explanation": explanation,
            "risk_reason": finalize_published_text(
                clause.get("risk_reason", ""),
                language,
            ),
            "red_flag_reason": finalize_published_text(
                clause.get("red_flag_reason", ""),
                language,
            ),
            "red_flag": bool(
                clause.get("red_flag")
            ),
        })

    return risks'''


NEGOTIATION = r'''def build_negotiation_priorities(
    clauses: list,
    language: str = "en",
) -> list:
    priorities = []
    language = normalize_language(language)

    for i, clause in enumerate(clauses):
        priority = str(
            clause.get(
                "negotiation_priority",
                "low",
            )
        ).lower()

        if priority == "low":
            continue

        advice = select_clause_report_text(
            clause,
            language,
            purpose="negotiation",
        )

        if not advice:
            continue

        priorities.append({
            "risk_ref": f"risk_{_clause_id(clause, i)}",
            "priority": priority,
            "negotiable": infer_negotiability(clause),
            "what_should_change": advice,
            "commercial_objective": finalize_published_text(
                clause.get("commercial_objective", ""),
                language,
            ),
            "acceptable_compromise": finalize_published_text(
                clause.get("acceptable_compromise", ""),
                language,
            ),
            "never_accept": finalize_published_text(
                clause.get("never_accept", ""),
                language,
            ),
        })

    return priorities'''


LEGACY = r'''def to_legacy_summary_data(
    report: dict,
    language: str = "en",
) -> dict:
    language = normalize_language(language)
    not_specified = localized_default(
        "not_specified",
        language,
    )

    overview = (
        report.get("contract_overview", {})
        or {}
    )
    negotiation = (
        report.get("negotiation_priorities", [])
        or []
    )
    risks = (
        report.get("risks_identified", [])
        or []
    )

    contract_family = (
        report.get("contract_family")
        or overview.get("contract_type")
        or ""
    )
    optional_fields = get_optional_fields_for_family(
        contract_family
    )

    parties = canonicalize_party_labels(
        overview.get("parties"),
        language,
    )

    payment_terms = overview.get("payment_terms")
    if not payment_terms:
        payment_terms = (
            localized_default(
                "not_applicable",
                language,
            )
            if "payment_terms" in optional_fields
            else not_specified
        )

    main_obligations, important_points = (
        build_legacy_clause_sections(
            report,
            language,
        )
    )

    action_texts = [
        finalize_published_text(
            action.get("action", ""),
            language,
        )
        for action in report.get(
            "action_checklist",
            [],
        )
        if isinstance(action, dict)
    ]

    dangerous_risks = [
        risk
        for risk in risks
        if isinstance(risk, dict)
        and risk_is_dangerous_pattern(
            risk,
            language,
        )
    ]

    high_risk_texts = [
        finalize_published_text(
            title_aware_clause_text(
                {
                    "title": risk.get("title", ""),
                    "clause_type": risk.get(
                        "clause_type",
                        "other",
                    ),
                    "why_it_matters": risk.get(
                        "explanation",
                        "",
                    ),
                },
                language,
            ),
            language,
        )
        for risk in dangerous_risks
    ]

    all_risk_texts = [
        finalize_published_text(
            title_aware_clause_text(
                {
                    "title": risk.get("title", ""),
                    "clause_type": risk.get(
                        "clause_type",
                        "other",
                    ),
                    "why_it_matters": risk.get(
                        "explanation",
                        "",
                    ),
                },
                language,
            ),
            language,
        )
        for risk in risks
        if isinstance(risk, dict)
    ]

    negotiation_texts = [
        finalize_published_text(
            item.get("what_should_change", ""),
            language,
        )
        for item in negotiation
        if isinstance(item, dict)
    ]

    missing_texts = [
        finalize_published_text(
            (
                f"{item.get('clause_type', 'unknown')}: "
                f"{item.get('business_reason') or item.get('risk_if_missing') or item.get('why_missing') or ''}"
            ).strip(),
            language,
        )
        for item in report.get(
            "missing_clauses",
            [],
        )
        if isinstance(item, dict)
    ]

    return {
        "contract_type": (
            overview.get("contract_type")
            or report.get("contract_family")
            or not_specified
        ),
        "parties": parties,
        "duration": (
            overview.get("duration")
            or not_specified
        ),
        "payment_terms": payment_terms,
        "main_obligations": compact_unique_texts(
            [
                finalize_published_text(
                    item,
                    language,
                )
                for item in main_obligations
            ],
            language,
            limit=8,
        ),
        "global_summary": finalize_published_text(
            report.get("executive_summary", ""),
            language,
        ),
        "important_points": compact_unique_texts(
            [
                finalize_published_text(
                    item,
                    language,
                )
                for item in important_points
            ],
            language,
            limit=8,
        ),
        "missing_clauses": compact_unique_texts(
            missing_texts,
            language,
            limit=5,
            drop_generic=False,
        ),
        "dangerous_patterns": compact_unique_texts(
            high_risk_texts,
            language,
            limit=5,
        ),
        "contract_quality_score": int(
            report.get("confidence_score")
            if report.get("confidence_score")
            is not None
            else 0
        ),
        "overall_balance": (
            overview.get("overall_balance")
            or not_specified
        ),
        "negotiation_priorities": compact_unique_texts(
            negotiation_texts,
            language,
            limit=5,
        ),
        "key_risks": compact_unique_texts(
            all_risk_texts,
            language,
            limit=5,
        ),
        "practical_decision": finalize_published_text(
            report.get("fallback_position", ""),
            language,
        ),
        "jurisdiction_detected": (
            overview.get("jurisdiction_detected")
            or not_specified
        ),
        "jurisdiction_note": finalize_published_text(
            overview.get("jurisdiction_note", ""),
            language,
        ),
        "recommended_actions": compact_unique_texts(
            action_texts,
            language,
            limit=5,
        ),
        "contract_complexity": overview.get(
            "contract_complexity",
            "medium",
        ),
    }'''


def _offsets(
    source: str,
    node: ast.AST,
) -> tuple[int, int]:
    lines = source.splitlines(
        keepends=True,
    )

    return (
        sum(
            len(line)
            for line in lines[
                : node.lineno - 1
            ]
        ),
        sum(
            len(line)
            for line in lines[
                : node.end_lineno
            ]
        ),
    )


def _find_assignment(
    source: str,
    name: str,
) -> tuple[int, int]:
    tree = ast.parse(source)
    found = []

    for node in tree.body:
        targets = []

        if isinstance(node, ast.Assign):
            targets = node.targets
        elif isinstance(node, ast.AnnAssign):
            targets = [node.target]

        if any(
            isinstance(target, ast.Name)
            and target.id == name
            for target in targets
        ):
            found.append(node)

    if len(found) != 1:
        raise RuntimeError(
            f"{name}: expected 1 assignment, "
            f"found {len(found)}"
        )

    return _offsets(source, found[0])


def _find_function(
    source: str,
    name: str,
) -> tuple[int, int]:
    tree = ast.parse(source)

    found = [
        node
        for node in ast.walk(tree)
        if isinstance(
            node,
            (
                ast.FunctionDef,
                ast.AsyncFunctionDef,
            ),
        )
        and node.name == name
    ]

    if len(found) != 1:
        raise RuntimeError(
            f"{name}: expected 1 function, "
            f"found {len(found)}"
        )

    return _offsets(source, found[0])


def _replace_span(
    source: str,
    span: tuple[int, int],
    replacement: str,
) -> str:
    start, end = span

    return (
        source[:start]
        + replacement.rstrip()
        + source[end:]
    )


def main() -> int:
    if not TARGET.exists():
        raise SystemExit(
            f"MISSING TARGET: {TARGET}"
        )

    source = TARGET.read_text(
        encoding="utf-8",
    )
    ast.parse(source)

    anchors = (
        "GENERIC_REPORT_TEXT_MARKERS",
        "normalize_published_role_text",
        "select_clause_report_text",
        "build_risks_identified",
        "build_negotiation_priorities",
        "to_legacy_summary_data",
    )

    for anchor in anchors:
        if anchor not in source:
            raise SystemExit(
                f"ANCHOR MISSING: {anchor}"
            )

    if "DANGEROUS_PATTERN_MARKERS" in source:
        raise SystemExit(
            "REFUSING DOUBLE PATCH: "
            "V4.1.16 markers already present"
        )

    stamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )
    backup = TARGET.with_name(
        TARGET.name
        + f".before_v4_1_16_{stamp}"
    )
    shutil.copy2(
        TARGET,
        backup,
    )

    source = _replace_span(
        source,
        _find_assignment(
            source,
            "GENERIC_REPORT_TEXT_MARKERS",
        ),
        GENERIC_MARKERS,
    )

    source = _replace_span(
        source,
        _find_function(
            source,
            "normalize_published_role_text",
        ),
        ROLE_HELPER,
    )

    selector_start, _ = _find_function(
        source,
        "select_clause_report_text",
    )

    source = (
        source[:selector_start]
        + SEMANTIC_HELPERS.rstrip()
        + "\n\n\n"
        + source[selector_start:]
    )

    source = _replace_span(
        source,
        _find_function(
            source,
            "select_clause_report_text",
        ),
        SELECTOR,
    )

    source = _replace_span(
        source,
        _find_function(
            source,
            "build_risks_identified",
        ),
        RISKS,
    )

    source = _replace_span(
        source,
        _find_function(
            source,
            "build_negotiation_priorities",
        ),
        NEGOTIATION,
    )

    source = _replace_span(
        source,
        _find_function(
            source,
            "to_legacy_summary_data",
        ),
        LEGACY,
    )

    old_call = (
        "    negotiation_priorities = "
        "build_negotiation_priorities(clauses)"
    )
    new_call = (
        "    negotiation_priorities = "
        "build_negotiation_priorities("
        "clauses, language)"
    )

    if source.count(old_call) != 1:
        raise SystemExit(
            "NEGOTIATION CALL ANCHOR: "
            f"expected 1, found "
            f"{source.count(old_call)}"
        )

    source = source.replace(
        old_call,
        new_call,
        1,
    )

    ast.parse(source)
    compile(
        source,
        str(TARGET),
        "exec",
    )

    TARGET.write_text(
        source,
        encoding="utf-8",
        newline="\n",
    )

    print("=" * 96)
    print(
        "V4.1.16 FINAL PUBLICATION "
        "INVARIANT APPLIED"
    )
    print("=" * 96)
    print("TARGET :", TARGET)
    print("BACKUP :", backup)
    print(
        "A: fixed final EN/FR/AR role regex "
        "normalization"
    )
    print(
        "B: expanded generic fallback "
        "suppression"
    )
    print(
        "C: semantic metadata corroboration "
        "for type-specific negotiation advice"
    )
    print(
        "D: dangerous_patterns restricted to "
        "red flags or substantive danger markers"
    )
    print(
        "E: final publication normalization "
        "applied to legacy summary buckets"
    )
    print(
        "UNTOUCHED: semantic_source_profile.py, "
        "RULES, dominance thresholds,"
    )
    print(
        "           evidence engine, publication "
        "gate validation logic, risk scoring,"
    )
    print(
        "           missing-clause taxonomy, "
        "frontend"
    )
    print("=" * 96)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
