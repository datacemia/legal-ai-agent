#!/usr/bin/env python3
"""
audit_negotiation_consistency.py

Standalone audit tool for reviewing the negotiation_consistency_fixed /
negotiation_consistency_warning flags across every clause in a Runexa
contract analysis result, in one consolidated table instead of scrolling
through the full report clause by clause.

Usage:
    python audit_negotiation_consistency.py path/to/analysis_result.json

The input JSON can be any of these shapes (this script auto-detects
which one it received, matching the shapes already used elsewhere in
the pipeline):
  - The full worker/API response, i.e. result["clauses"]["results"]
  - A dict with "clauses" as a bare list
  - A dict with "results" directly at the top level
  - A bare JSON list of clause dicts

For each clause, prints:
  - # (row index)
  - Reference (article/section number)
  - Title
  - Clause type
  - Status:
      FIXED    -> negotiation_consistency_fixed is True (auto-corrected)
      WARNING  -> negotiation_consistency_warning is True (needs review)
      -        -> neither flag set (looks fine, or an undetected gap)

Then prints a Fallback Wording / Acceptable Compromise preview for
every clause, so a "-" row can still be eyeballed for a possible
undetected mismatch (e.g. a clause mixing "for cause" and "for
convenience" language in the same sentence, which the automated
detector currently cannot reliably separate -- see the trailing note).

Ends with a summary count and explicitly lists every clause reference
in the WARNING category, since those are the ones that most need a
human look.
"""

import json
import sys
import textwrap


def _load_clauses(data):
    """
    Accepts several possible JSON shapes and returns a flat list of
    clause dicts, matching how "clauses" appears at different points in
    the pipeline (worker response, analyze_contract_clauses() output,
    or a bare list already extracted by the caller).
    """
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


def audit(clauses):
    rows = []

    for index, clause in enumerate(clauses, start=1):
        title = clause.get("clause_title") or clause.get("title") or ""
        reference = clause.get("clause_reference") or clause.get("reference") or ""
        clause_type = clause.get("clause_type") or "other"

        fixed = clause.get("negotiation_consistency_fixed") is True
        warning = clause.get("negotiation_consistency_warning") is True

        if fixed:
            status = "FIXED"
        elif warning:
            status = "WARNING"
        else:
            status = "-"

        rows.append({
            "index": index,
            "reference": reference,
            "title": title,
            "clause_type": clause_type,
            "status": status,
            "fallback": _preview(clause.get("fallback_wording")),
            "compromise": _preview(clause.get("acceptable_compromise")),
        })

    return rows


def print_report(rows):
    if not rows:
        print("Aucune clause trouvée dans le fichier fourni.")
        print(
            "Vérifie que le JSON correspond bien à une sortie d'analyse "
            "Runexa (clé 'clauses' -> 'results', ou une liste brute de "
            "clauses)."
        )
        return

    header = f"{'#':<3} {'Réf.':<10} {'Titre':<34} {'Type':<26} {'Statut':<8}"
    print(header)
    print("-" * len(header))

    for row in rows:
        title = textwrap.shorten(row["title"] or "(sans titre)", width=34, placeholder="…")
        clause_type = textwrap.shorten(row["clause_type"], width=26, placeholder="…")
        reference = textwrap.shorten(row["reference"] or "-", width=10, placeholder="…")

        print(
            f"{row['index']:<3} {reference:<10} {title:<34} "
            f"{clause_type:<26} {row['status']:<8}"
        )

    print()
    print("Détail Fallback Wording / Acceptable Compromise :")
    print("=" * 78)

    status_marker = {
        "FIXED": "🔧",
        "WARNING": "⚠️ ",
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
        print()

    total = len(rows)
    fixed_count = sum(1 for r in rows if r["status"] == "FIXED")
    warning_count = sum(1 for r in rows if r["status"] == "WARNING")
    clean_count = total - fixed_count - warning_count

    print("=" * 78)
    print("RÉSUMÉ")
    print("=" * 78)
    print(f"Total clauses analysées     : {total}")
    print(f"  Corrigées automatiquement : {fixed_count}")
    print(f"  Signalées (à revoir)      : {warning_count}")
    print(f"  Sans incohérence détectée : {clean_count}")

    if warning_count:
        print()
        print("Clauses à revoir manuellement (WARNING) :")

        for row in rows:
            if row["status"] == "WARNING":
                print(f"  - #{row['index']} [{row['reference'] or '-'}] {row['title']}")

    print()
    print(
        "Note : les clauses marquées '-' n'ont déclenché aucune alerte, mais\n"
        "cela ne garantit pas qu'elles soient réellement cohérentes -- la\n"
        "détection reste une heuristique (comparaison numérique + quelques\n"
        "dichotomies conceptuelles courantes : for cause/for convenience,\n"
        "with notice/without notice, exclusive/non-exclusive, limited/\n"
        "unlimited, en EN/FR/AR). Un cas comme 'Termination for Convenience'\n"
        "(qui mélange 'for cause' et 'for convenience' dans la même phrase,\n"
        "chacun attribué à une partie différente) peut encore passer sous le\n"
        "radar. Un coup d'œil rapide sur les clauses à fort enjeu (HIGH/\n"
        "MEDIUM risk, red_flag=true) reste recommandé même sans WARNING."
    )


def main():
    if len(sys.argv) < 2:
        print("Usage: python audit_negotiation_consistency.py <fichier.json>")
        sys.exit(1)

    path = sys.argv[1]

    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    clauses = _load_clauses(data)
    rows = audit(clauses)
    print_report(rows)


if __name__ == "__main__":
    main()
