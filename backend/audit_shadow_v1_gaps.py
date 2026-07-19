#!/usr/bin/env python3
"""Read-only diagnosis of shadow-p0-v1 abstentions and generic type overrides."""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

for stream in (sys.stdout, sys.stderr):
    if hasattr(stream, "reconfigure"):
        stream.reconfigure(encoding="utf-8", errors="backslashreplace")

GENERIC_KINDS = {
    "PRIOR_CONSENT_PREREQUISITE",
    "PROHIBITION",
    "MANDATORY_OBLIGATION",
    "MANDATORY_CONJUNCTION",
    "EXPRESS_RIGHT",
}

DOMAIN_KINDS = {
    "CONFIDENTIALITY_DUTY",
    "AUTOMATIC_RENEWAL",
    "AUTOMATIC_EVENT_TRANSITION",
    "EXCLUDED_DAMAGE_CATEGORY",
    "LIABILITY_CAP",
    "FINANCIAL_REPORTING_OBLIGATION",
    "BOARD_COMPOSITION_STRUCTURE",
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "details",
        type=Path,
        default=Path("semantic_profile_shadow/shadow_details.json"),
    )
    ap.add_argument(
        "--out",
        type=Path,
        default=Path("semantic_profile_shadow/shadow_gap_inventory.json"),
    )
    args = ap.parse_args()

    rows = json.loads(args.details.read_text(encoding="utf-8"))
    if not isinstance(rows, list):
        raise SystemExit("shadow_details.json must contain a JSON list")

    abstained = [r for r in rows if r.get("type_verdict") == "ABSTAINED"]
    divergences = [r for r in rows if r.get("type_verdict") == "DIVERGENCE"]

    abstain_by_type = Counter(str(r.get("pipeline_clause_type") or "UNKNOWN") for r in abstained)
    abstain_by_language = Counter(str(r.get("language") or "UNKNOWN") for r in abstained)

    generic_override = []
    domain_conflict = []
    mixed = []

    for row in divergences:
        kinds = {
            str(m.get("kind"))
            for m in (row.get("ranked_material_mechanisms") or [])
            if isinstance(m, dict)
        }
        if kinds and kinds <= GENERIC_KINDS:
            generic_override.append(row)
        elif kinds & DOMAIN_KINDS and kinds & GENERIC_KINDS:
            mixed.append(row)
        else:
            domain_conflict.append(row)

    examples = defaultdict(list)
    for row in abstained:
        clause_type = str(row.get("pipeline_clause_type") or "UNKNOWN")
        if len(examples[clause_type]) < 3:
            examples[clause_type].append({
                "language": row.get("language"),
                "document": row.get("document"),
                "reference": row.get("reference"),
                "source_text": row.get("source_text"),
            })

    report = {
        "rows": len(rows),
        "abstained": len(abstained),
        "abstain_rate": round(len(abstained) / len(rows), 6) if rows else 0,
        "abstain_by_language": dict(abstain_by_language),
        "abstain_by_pipeline_type": dict(abstain_by_type.most_common()),
        "divergences": len(divergences),
        "generic_only_primary_overrides": len(generic_override),
        "mixed_generic_and_domain_divergences": len(mixed),
        "domain_conflict_candidates": len(domain_conflict),
        "abstention_examples_by_pipeline_type": dict(examples),
        "generic_only_divergences": generic_override,
        "mixed_divergences": mixed,
        "domain_conflict_candidates_details": domain_conflict,
    }

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("=" * 88)
    print("SHADOW P0 V1 — GAP INVENTORY")
    print("=" * 88)
    print("ROWS:", len(rows))
    print("ABSTAINED:", len(abstained))
    print("ABSTAIN RATE:", f"{report['abstain_rate']:.2%}")
    print("ABSTAIN BY LANGUAGE:", dict(abstain_by_language))
    print("DIVERGENCES:", len(divergences))
    print("GENERIC-ONLY PRIMARY OVERRIDES:", len(generic_override))
    print("MIXED GENERIC+DOMAIN DIVERGENCES:", len(mixed))
    print("DOMAIN CONFLICT CANDIDATES:", len(domain_conflict))
    print("REPORT:", args.out)

    print("\nTOP ABSTAINED PIPELINE TYPES")
    for clause_type, count in abstain_by_type.most_common(40):
        print(f"{count:4d}  {clause_type}")

    print("\nDOMAIN CONFLICT CANDIDATES")
    for row in domain_conflict[:40]:
        kinds = [
            m.get("kind")
            for m in (row.get("ranked_material_mechanisms") or [])
            if isinstance(m, dict)
        ]
        print(
            f"{str(row.get('language')).upper()} | {row.get('document')} | "
            f"{row.get('reference')} | pipeline={row.get('pipeline_clause_type')} | "
            f"shadow={row.get('shadow_primary_type')} | mechanisms={kinds}"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
