#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

for stream in (sys.stdout, sys.stderr):
    if hasattr(stream, "reconfigure"):
        stream.reconfigure(
            encoding="utf-8",
            errors="backslashreplace",
        )

path = Path(
    "semantic_profile_shadow_v4/"
    "shadow_divergences.json"
)

rows = json.loads(
    path.read_text(encoding="utf-8")
)

print("=" * 100)
print("V4 DIVERGENCE FORENSICS")
print("=" * 100)
print("DIVERGENCES:", len(rows))

for index, row in enumerate(rows, 1):
    print()
    print("#" * 100)
    print(f"[{index}/{len(rows)}]")
    print("LANG:", row.get("language"))
    print("DOC:", row.get("document"))
    print("REF:", row.get("reference"))
    print(
        "PIPELINE:",
        row.get("pipeline_clause_type"),
    )
    print(
        "SHADOW:",
        row.get("shadow_primary_type"),
    )
    print(
        "CONFIDENCE:",
        row.get("shadow_primary_type_confidence"),
    )
    print(
        "ABSTAINED:",
        row.get("shadow_abstained"),
    )
    print(
        "PRIMARY COVERAGE:",
        row.get("shadow_primary_evidence_coverage"),
    )
    print(
        "DOMINANCE MARGIN:",
        row.get("shadow_dominance_margin"),
    )
    print(
        "SUPPORT:",
        row.get("shadow_supporting_mechanisms"),
    )
    print("SOURCE:")
    print(row.get("source_text"))

    print("RANKED MECHANISMS:")
    for mechanism in (
        row.get("ranked_material_mechanisms")
        or []
    ):
        print(
            "-",
            mechanism.get("kind"),
            "| role=",
            mechanism.get("semantic_role"),
            "| primary=",
            mechanism.get("candidate_primary_type"),
            "| eligible=",
            mechanism.get("primary_eligible"),
            "| rank=",
            mechanism.get("rank"),
        )

        for evidence in (
            mechanism.get("source_evidence")
            or []
        ):
            print(
                "  EVIDENCE:",
                repr(evidence.get("text")),
            )

    print("DOMINANCE SCORES:")
    for score in (
        row.get("shadow_dominance_scores")
        or []
    ):
        print(
            "-",
            json.dumps(
                score,
                ensure_ascii=False,
            ),
        )
