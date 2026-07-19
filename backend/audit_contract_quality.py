#!/usr/bin/env python3
"""
audit_contract_quality.py

Extended, standalone audit tool for a Runexa contract analysis result.
Supersedes audit_negotiation_consistency.py: keeps every check that
script already did (negotiation_consistency_fixed/warning,
negotiation_fidelity_warning) and adds several new ones, discovered
useful over the course of this session's bug-hunting:

  1. STRUCTURE     -- clause count / truncation, exactly as before.
  2. CONSISTENCY    -- FIXED / WARNING / FIDELITY, exactly as before.
  3. DUPLICATE TEXT -- flags when 2+ DIFFERENT clauses share the
                       IDENTICAL fallback_wording, safer_alternative,
                       legal_insight, or recommendation text. This is
                       exactly the failure pattern behind several real
                       bugs this session (every clause silently sharing
                       one generic template regardless of type).
  4. GENERIC TEXT   -- flags when fallback_wording, acceptable_compromise,
                       safer_alternative, or negotiation_boundary is an
                       EXACT match for one of the known, fully generic
                       fallback templates (in EN/FR/AR) -- i.e. this
                       specific clause never got type-specific treatment
                       at all, even if no other clause happens to share
                       its text.
  5. PLACEHOLDER    -- flags any of the tracked text fields that still
     LEAKAGE           contain a raw PII-redaction placeholder token
                       (e.g. "[ORGANIZATION]", "[PARTY_1]", "[LOCATION]")
                       -- these read as broken/ungrammatical to an end
                       user and are worth a manual look even if the
                       underlying data is technically "correct".
  6. EMPTY FIELDS   -- flags clauses missing legal_insight or
                       recommendation entirely.
  7. TYPE SUMMARY   -- clause_type distribution across the contract,
                       highlighting "other"/"general"/empty types (a
                       signal that contract_taxonomy.py may need a new
                       dedicated category, as happened several times
                       this session).

Usage:
    python audit_contract_quality.py path/to/analysis_result.json

Accepts the same input JSON shapes as audit_negotiation_consistency.py
(auto-detected):
  - The full worker/API response, i.e. result["clauses"]["results"]
  - A dict with "clauses" as a bare list
  - A dict with "results" directly at the top level
  - A bare JSON list of clause dicts
"""

import json
import sys
import textwrap
from collections import Counter, defaultdict


# ---------------------------------------------------------------------------
# Known, fully generic fallback templates (EN/FR/AR), copied verbatim from
# negotiation_intelligence.py and clause_wording_library.py. Exact-match
# comparisons against these catch clauses that never received any
# type-specific treatment, even in isolation (i.e. even when no OTHER
# clause in the same contract happens to share the same text).
# ---------------------------------------------------------------------------

GENERIC_FALLBACK_WORDING = {
    "en": (
        "A fallback formulation typically narrows the obligation to an "
        "objective, measurable standard and specifies the remedy or "
        "process that applies if that standard is not met."
    ),
    "fr": (
        "Une formulation de repli consiste généralement à restreindre "
        "l'obligation à une norme objective et mesurable, et à préciser "
        "le recours ou la procédure applicable en cas de non-respect."
    ),
    "ar": (
        "تتمثل الصياغة البديلة عادة في تضييق الالتزام إلى معيار "
        "موضوعي وقابل للقياس، وتحديد وسيلة الانتصاف أو الإجراء "
        "المطبق في حال عدم الوفاء بهذا المعيار."
    ),
}

GENERIC_ACCEPTABLE_COMPROMISE = {
    "en": (
        "A reasonable compromise typically narrows the scope, adds objective "
        "criteria or thresholds, and includes standard exceptions appropriate "
        "to this type of clause."
    ),
    "fr": (
        "Un compromis raisonnable consiste généralement à restreindre la "
        "portée, à ajouter des critères ou seuils objectifs, et à inclure les "
        "exceptions usuelles adaptées à ce type de clause."
    ),
    "ar": (
        "يتمثل التسوية المعقولة عادة في تضييق النطاق، وإضافة معايير أو حدود "
        "موضوعية، وتضمين الاستثناءات المعتادة المناسبة لهذا النوع من البنود."
    ),
}

GENERIC_NEGOTIATION_BOUNDARY = {
    "en": (
        "Avoid accepting terms that are open-ended, lack objective criteria, "
        "or are materially more one-sided than standard market practice for "
        "this type of clause."
    ),
    "fr": (
        "Éviter d'accepter des conditions ouvertes, dépourvues de critères "
        "objectifs, ou nettement plus déséquilibrées que la pratique de "
        "marché habituelle pour ce type de clause."
    ),
    "ar": (
        "ينبغي تجنب قبول شروط مفتوحة أو تفتقر إلى معايير موضوعية أو غير "
        "متوازنة بشكل واضح مقارنة بممارسة السوق المعتادة لهذا النوع من "
        "البنود."
    ),
}

GENERIC_SAFER_ALTERNATIVE = {
    "en": (
        "A safer alternative is to clarify the scope, objective standards, notice requirements, "
        "exceptions, remedies, and proportional limits so the clause remains enforceable and balanced."
    ),
    "fr": (
        "Une alternative plus sûre consiste à clarifier la portée, les critères objectifs, "
        "les exigences de notification, les exceptions, les recours et les limites proportionnées "
        "afin que la clause reste applicable et équilibrée."
    ),
    "ar": (
        "البديل الأكثر أماناً هو توضيح النطاق والمعايير الموضوعية ومتطلبات الإخطار "
        "والاستثناءات ووسائل الانتصاف والحدود المتناسبة حتى يبقى البند قابلاً للتنفيذ ومتوازناً."
    ),
}

ALL_GENERIC_TEXTS = set()
for _bucket in (
    GENERIC_FALLBACK_WORDING,
    GENERIC_ACCEPTABLE_COMPROMISE,
    GENERIC_NEGOTIATION_BOUNDARY,
    GENERIC_SAFER_ALTERNATIVE,
):
    for _text in _bucket.values():
        ALL_GENERIC_TEXTS.add(_text.strip())


# Fields checked for duplicate-across-clauses text and for generic-template
# matches. Extend this list if new negotiation/reasoning fields are added.
TRACKED_TEXT_FIELDS = [
    "fallback_wording",
    "acceptable_compromise",
    "safer_alternative",
    "negotiation_boundary",
    "legal_insight",
    "recommendation",
]

# Fields checked for empty/missing content (worth a look even without an
# explicit WARNING/FIDELITY flag).
REQUIRED_NONEMPTY_FIELDS = [
    "legal_insight",
    "recommendation",
]

# Placeholder token patterns considered worth flagging if found verbatim in
# any tracked text field -- these read as broken/ungrammatical to an end
# user regardless of whether the underlying substitution was technically
# "correct" for privacy purposes.
PLACEHOLDER_TOKENS = [
    "[PARTY_1]", "[PARTY_2]", "[PARTY_3]",
    "[ORGANIZATION]", "[PERSON]", "[LOCATION]", "[COMPANY]",
    "[EMPLOYER]", "[EMPLOYEE]", "[CLIENT]", "[SERVICE_PROVIDER]",
    "[SUPPLIER]", "[VENDOR]", "[BUYER]", "[SELLER]", "[LENDER]",
    "[BORROWER]", "[LICENSOR]", "[LICENSEE]", "[LESSOR]", "[LESSEE]",
    "[SHAREHOLDER]", "[SENSITIVE_DATA]",
]

# clause_type values that signal a possible taxonomy gap (the clause
# didn't confidently match any dedicated category).
WEAK_TYPE_VALUES = {"", "other", "general", None}


def _load_clauses(data):
    if isinstance(data, list):
        return data

    if not isinstance(data, dict):
        return []

    clauses = data.get("clauses")

    if isinstance(clauses, dict):
        if isinstance(clauses.get("results"), list):
            return clauses["results"]
        if isinstance(clauses.get("clauses"), dict) and isinstance(
            clauses["clauses"].get("results"), list
        ):
            return clauses["clauses"]["results"]

    if isinstance(clauses, list):
        return clauses

    if isinstance(data.get("results"), list):
        return data["results"]

    return []


def _preview(text, width=400):
    text = str(text or "").strip()

    if not text:
        return "(vide)"

    text = " ".join(text.split())

    if len(text) <= width:
        return text

    return text[: width - 1] + "…"


STATUS_DISPLAY_NAME = {
    "FIXED": "AUTO-REVISED",
    "REVIEW_REQUIRED": "REVIEW REQUIRED",
    "WARNING": "WARNING",
    "FIDELITY": "FIDELITY",
    "-": "-",
}


def _clause_label(row):
    return f"#{row['index']} [{row['reference'] or '-'}] {row['title'] or '(sans titre)'}"


def audit(clauses):
    rows = []

    for index, clause in enumerate(clauses, start=1):
        title = clause.get("clause_title") or clause.get("title") or ""
        reference = clause.get("clause_reference") or clause.get("reference") or ""
        clause_type = clause.get("clause_type") or "other"

        fixed = clause.get("negotiation_consistency_fixed") is True
        review_required = clause.get("negotiation_consistency_review_required") is True
        warning = clause.get("negotiation_consistency_warning") is True
        fidelity_issue = clause.get("negotiation_fidelity_warning") is True

        if review_required:
            status = "REVIEW_REQUIRED"
        elif fixed:
            status = "FIXED"
        elif fidelity_issue:
            status = "FIDELITY"
        elif warning:
            status = "WARNING"
        else:
            status = "-"

        row = {
            "index": index,
            "reference": reference,
            "title": title,
            "clause_type": clause_type,
            "status": status,
            "fallback": _preview(clause.get("fallback_wording")),
            "compromise": _preview(clause.get("acceptable_compromise")),
            "fidelity_note": clause.get("negotiation_fidelity_note") or "",
            "raw": clause,
        }

        for field in TRACKED_TEXT_FIELDS:
            row[field] = str(clause.get(field) or "").strip()

        rows.append(row)

    return rows


def find_duplicate_text_groups(rows):
    """
    For each tracked text field, groups clauses sharing IDENTICAL,
    non-empty text. Returns {field: [[row, row, ...], ...]} for groups
    of size >= 2 only.
    """
    duplicates_by_field = {}

    for field in TRACKED_TEXT_FIELDS:
        by_text = defaultdict(list)

        for row in rows:
            text = row.get(field, "")
            if text:
                by_text[text].append(row)

        groups = [group for group in by_text.values() if len(group) >= 2]

        if groups:
            duplicates_by_field[field] = groups

    return duplicates_by_field


def find_generic_text_rows(rows):
    """
    Returns {field: [row, ...]} for every row whose field value is an
    EXACT match for one of the known fully-generic templates, in any
    supported language -- flags clauses that never got type-specific
    treatment, independent of whether any other clause shares the text.
    """
    generic_by_field = defaultdict(list)

    for row in rows:
        for field in TRACKED_TEXT_FIELDS:
            text = row.get(field, "")
            if text and text in ALL_GENERIC_TEXTS:
                generic_by_field[field].append(row)

    return generic_by_field


def find_placeholder_leakage(rows):
    """
    Returns [(row, field, token), ...] for every tracked field
    containing a raw PII-redaction placeholder token.
    """
    findings = []

    for row in rows:
        for field in TRACKED_TEXT_FIELDS:
            text = row.get(field, "")
            if not text:
                continue
            for token in PLACEHOLDER_TOKENS:
                if token in text:
                    findings.append((row, field, token))

    return findings


def find_empty_required_fields(rows):
    """
    Returns [(row, field), ...] for every row missing a field that
    should generally be present.
    """
    findings = []

    for row in rows:
        for field in REQUIRED_NONEMPTY_FIELDS:
            if not row.get(field, "").strip():
                findings.append((row, field))

    return findings


def type_distribution(rows):
    counter = Counter(row["clause_type"] for row in rows)
    weak = [row for row in rows if row["clause_type"] in WEAK_TYPE_VALUES]
    return counter, weak


def print_structure_section(truncation_info):
    if truncation_info is None:
        return

    total = truncation_info.get("total_clauses_detected")
    analyzed = truncation_info.get("clauses_analyzed")
    truncated = truncation_info.get("clauses_truncated")

    if truncated:
        print("=" * 78)
        print(
            f"⚠️  ANALYSE PARTIELLE : {analyzed}/{total} clauses détectées ont été "
            f"analysées."
        )
        print(
            f"    {total - analyzed} clause(s) n'ont PAS été analysées "
            f"(au-delà de la limite max_clauses)."
        )
        print("=" * 78)
        print()
    else:
        print(
            f"✅ Toutes les clauses détectées ont été analysées "
            f"({analyzed}/{total})."
        )
        print()


def print_consistency_table(rows):
    header = f"{'#':<3} {'Réf.':<10} {'Titre':<34} {'Type':<26} {'Statut':<8}"
    print(header)
    print("-" * len(header))

    for row in rows:
        title = textwrap.shorten(row["title"] or "(sans titre)", width=34, placeholder="…")
        clause_type = textwrap.shorten(row["clause_type"], width=26, placeholder="…")
        reference = textwrap.shorten(row["reference"] or "-", width=10, placeholder="…")

        print(
            f"{row['index']:<3} {reference:<10} {title:<34} "
            f"{clause_type:<26} {STATUS_DISPLAY_NAME.get(row['status'], row['status']):<13}"
        )


def print_consistency_detail(rows):
    print()
    print("Détail Fallback Wording / Acceptable Compromise :")
    print("=" * 78)

    status_marker = {
        "FIXED": "🔧",
        "REVIEW_REQUIRED": "🔍",
        "WARNING": "⚠️ ",
        "FIDELITY": "🚩",
        "-": "  ",
    }

    for row in rows:
        marker = status_marker[row["status"]]

        print(
            f"{marker} #{row['index']} [{row['reference'] or '-'}] "
            f"{row['title'] or '(sans titre)'} ({row['clause_type']})"
        )
        print(f"     Fallback Wording      : {row['fallback']}")
        print(f"     Acceptable Compromise : {row['compromise']}")

        if row["status"] == "FIDELITY":
            structured_issues = row["raw"].get("fidelity_issues")
            if structured_issues:
                _severity_icon = {"high": "🔴", "medium": "🟠", "low": "⚪"}
                for issue in structured_issues:
                    icon = _severity_icon.get(issue.get("severity"), "⚪")
                    print(
                        f"     ⤷ {icon} [{str(issue.get('severity', '')).upper()}] "
                        f"{issue.get('kind', '')} (champ: {issue.get('field', '-')}) : "
                        f"{issue.get('note', '')}"
                    )
            elif row["fidelity_note"]:
                print(f"     ⤷ Problème de fidélité : {row['fidelity_note']}")

        if row["status"] == "FIXED":
            before_fallback = row["raw"].get("fallback_wording_before_autofix")
            before_compromise = row["raw"].get("acceptable_compromise_before_autofix")
            if before_fallback or before_compromise:
                print("     ⤷ AUTO-REVISED -- le texte du LLM a été remplacé par la version cohérente de la bibliothèque :")
                if before_fallback:
                    print(f"         Avant (Fallback Wording)      : {_preview(before_fallback)}")
                if before_compromise:
                    print(f"         Avant (Acceptable Compromise) : {_preview(before_compromise)}")
                print("       Une revue manuelle est recommandée pour confirmer que ce remplacement reste fidèle à l'intention négociée.")

        if row["status"] == "REVIEW_REQUIRED":
            note = row["raw"].get("negotiation_consistency_note") or ""
            suggested_fallback = row["raw"].get("suggested_fallback_wording")
            suggested_compromise = row["raw"].get("suggested_acceptable_compromise")
            print("     ⤷ REVIEW REQUIRED -- incohérence interne détectée sur un type de clause à portée juridique matérielle.")
            print("       Le texte ci-dessus est celui généré par le LLM, INCHANGÉ -- aucun remplacement automatique n'a été appliqué.")
            if note:
                print(f"       {note}")
            if suggested_fallback:
                print(f"         Suggestion (Fallback Wording)      : {_preview(suggested_fallback)}")
            if suggested_compromise:
                print(f"         Suggestion (Acceptable Compromise) : {_preview(suggested_compromise)}")
            print("       Cette suggestion nécessite une approbation humaine explicite avant application.")

        print()


def print_duplicate_section(duplicates_by_field):
    print("=" * 78)
    print("DOUBLONS DE TEXTE (clauses DIFFERENTES partageant un texte IDENTIQUE)")
    print("=" * 78)

    if not duplicates_by_field:
        print("Aucun doublon détecté sur les champs suivis.")
        print()
        return

    field_labels = {
        "fallback_wording": "Fallback Wording",
        "acceptable_compromise": "Acceptable Compromise",
        "safer_alternative": "Safer Alternative",
        "negotiation_boundary": "Negotiation Boundary",
        "legal_insight": "Legal Insight",
        "recommendation": "Recommendation",
    }

    for field, groups in duplicates_by_field.items():
        label = field_labels.get(field, field)
        print(f"\n[{label}] -- {len(groups)} groupe(s) de doublon(s) :")

        for group in groups:
            clause_labels = ", ".join(_clause_label(row) for row in group)
            print(f"  • {len(group)} clauses partagent le même texte : {clause_labels}")
            print(f"    Texte : {_preview(group[0][field], width=200)}")

    print()


def print_generic_section(generic_by_field):
    print("=" * 78)
    print("TEXTE GENERIQUE (correspondance EXACTE avec un template non spécifique)")
    print("=" * 78)

    if not generic_by_field:
        print("Aucune clause ne retombe sur un texte pleinement générique.")
        print()
        return

    field_labels = {
        "fallback_wording": "Fallback Wording",
        "acceptable_compromise": "Acceptable Compromise",
        "safer_alternative": "Safer Alternative",
        "negotiation_boundary": "Negotiation Boundary",
        "legal_insight": "Legal Insight",
        "recommendation": "Recommendation",
    }

    for field, field_rows in generic_by_field.items():
        label = field_labels.get(field, field)
        clause_labels = ", ".join(_clause_label(row) for row in field_rows)
        print(f"[{label}] -- {len(field_rows)} clause(s) : {clause_labels}")

    print()
    print(
        "Note : un texte générique n'est pas forcément une erreur -- certains\n"
        "types de clause n'ont pas encore de template dédié et retombent\n"
        "honnêtement sur un texte générique plutôt que de risquer un texte\n"
        "faux. Mais si PLUSIEURS clauses de types DIFFERENTS apparaissent\n"
        "ici, ça vaut la peine de vérifier si une catégorie dédiée manque."
    )
    print()


def print_placeholder_section(findings):
    print("=" * 78)
    print("FUITES DE PLACEHOLDER (jetons de rédaction PII bruts dans le texte)")
    print("=" * 78)

    if not findings:
        print("Aucun jeton de type [PARTY_1], [ORGANIZATION], etc. détecté.")
        print()
        return

    for row, field, token in findings:
        print(f"  • {_clause_label(row)} -- champ '{field}' contient {token}")

    print()


def print_empty_fields_section(findings):
    print("=" * 78)
    print("CHAMPS MANQUANTS (legal_insight / recommendation vides)")
    print("=" * 78)

    if not findings:
        print("Tous les champs requis sont renseignés.")
        print()
        return

    for row, field in findings:
        print(f"  • {_clause_label(row)} -- champ '{field}' vide")

    print()


def print_type_distribution_section(counter, weak_rows):
    print("=" * 78)
    print("RÉPARTITION DES TYPES DE CLAUSE")
    print("=" * 78)

    for clause_type, count in counter.most_common():
        marker = " ⚠️ " if clause_type in WEAK_TYPE_VALUES else "   "
        print(f"{marker}{clause_type or '(vide)':<30} {count}")

    if weak_rows:
        print()
        print(
            "⚠️  Clauses avec un type faible ('other'/'general'/vide) -- "
            "signal possible d'une categorie manquante dans contract_taxonomy.py :"
        )
        for row in weak_rows:
            print(f"  • {_clause_label(row)}")

    print()


def print_summary(rows, duplicates_by_field, generic_by_field, placeholder_findings, empty_findings):
    total = len(rows)
    fixed_count = sum(1 for r in rows if r["status"] == "FIXED")
    warning_count = sum(1 for r in rows if r["status"] == "WARNING")
    fidelity_count = sum(1 for r in rows if r["status"] == "FIDELITY")
    clean_count = total - fixed_count - warning_count - fidelity_count

    duplicate_clause_count = len(
        {row["index"] for groups in duplicates_by_field.values() for group in groups for row in group}
    )
    generic_clause_count = len(
        {row["index"] for field_rows in generic_by_field.values() for row in field_rows}
    )

    print("=" * 78)
    print("RÉSUMÉ GLOBAL")
    print("=" * 78)
    print(f"Total clauses analysées              : {total}")
    print(f"  Corrigées automatiquement (FIXED)  : {fixed_count}")
    print(f"  Signalées (incohérence, WARNING)   : {warning_count}")
    print(f"  Signalées (fidélité source)        : {fidelity_count}")
    print(f"  Sans incohérence détectée          : {clean_count}")
    print()
    print(f"  Clauses avec du texte en doublon    : {duplicate_clause_count}")
    print(f"  Clauses avec du texte générique     : {generic_clause_count}")
    print(f"  Fuites de placeholder détectées     : {len(placeholder_findings)}")
    print(f"  Champs requis manquants             : {len(empty_findings)}")

    if warning_count:
        print()
        print("Clauses à revoir manuellement (incohérence interne, WARNING) :")
        for row in rows:
            if row["status"] == "WARNING":
                print(f"  - {_clause_label(row)}")

    if fidelity_count:
        print()
        print("Clauses à revoir manuellement (fidélité au texte source, FIDELITY) :")
        for row in rows:
            if row["status"] == "FIDELITY":
                structured_issues = row["raw"].get("fidelity_issues")
                if structured_issues:
                    print(f"  - {_clause_label(row)}:")
                    for issue in structured_issues:
                        print(f"      [{str(issue.get('severity', '')).upper()}] {issue.get('kind', '')}: {issue.get('note', '')}")
                else:
                    print(f"  - {_clause_label(row)}: {row['fidelity_note']}")

    print()
    print(
        "Note : les clauses marquées '-' n'ont déclenché aucune alerte de\n"
        "cohérence/fidélité, mais cela ne garantit pas qu'elles soient\n"
        "réellement parfaites -- la détection reste une heuristique. Un\n"
        "coup d'œil rapide sur les sections DOUBLONS, TEXTE GENERIQUE et\n"
        "FUITES DE PLACEHOLDER ci-dessus reste recommandé même pour les\n"
        "clauses sans WARNING ni FIDELITY."
    )


def main():
    if len(sys.argv) < 2:
        print("Usage: python audit_contract_quality.py <fichier.json>")
        sys.exit(1)

    path = sys.argv[1]

    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    clauses = _load_clauses(data)
    rows = audit(clauses)

    truncation_info = None
    if isinstance(data, dict) and "clauses_truncated" in data:
        truncation_info = {
            "total_clauses_detected": data.get("total_clauses_detected"),
            "clauses_analyzed": data.get("clauses_analyzed"),
            "clauses_truncated": data.get("clauses_truncated"),
        }

    print_structure_section(truncation_info)

    if not rows:
        print("Aucune clause trouvée dans le fichier fourni.")
        print(
            "Vérifie que le JSON correspond bien à une sortie d'analyse "
            "Runexa (clé 'clauses' -> 'results', ou une liste brute de "
            "clauses)."
        )
        return

    print_consistency_table(rows)
    print_consistency_detail(rows)

    duplicates_by_field = find_duplicate_text_groups(rows)
    generic_by_field = find_generic_text_rows(rows)
    placeholder_findings = find_placeholder_leakage(rows)
    empty_findings = find_empty_required_fields(rows)
    type_counter, weak_type_rows = type_distribution(rows)

    print_duplicate_section(duplicates_by_field)
    print_generic_section(generic_by_field)
    print_placeholder_section(placeholder_findings)
    print_empty_fields_section(empty_findings)
    print_type_distribution_section(type_counter, weak_type_rows)
    print_summary(rows, duplicates_by_field, generic_by_field, placeholder_findings, empty_findings)


if __name__ == "__main__":
    main()