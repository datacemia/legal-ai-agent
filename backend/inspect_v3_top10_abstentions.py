#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

from app.services.contract_agent.semantic_source_profile import (
    build_semantic_source_profile,
)

for stream in (sys.stdout, sys.stderr):
    if hasattr(stream, "reconfigure"):
        stream.reconfigure(
            encoding="utf-8",
            errors="backslashreplace",
        )

root = Path("semantic_profile_shadow_v3")

TARGETS = {
    "intellectual_property",
    "liability",
    "data_protection",
    "confidentiality",
    "payment",
    "termination",
    "indemnity",
    "services",
    "employment",
    "loan",
}

rows: list[dict] = []

for path in root.glob("*.json"):
    if path.name.startswith("_"):
        continue

    try:
        payload = json.loads(
            path.read_text(encoding="utf-8")
        )
    except Exception:
        continue

    if isinstance(payload, list):
        candidates = payload
    elif isinstance(payload, dict):
        candidates = []
        for value in payload.values():
            if isinstance(value, list):
                candidates.extend(value)
    else:
        candidates = []

    rows.extend(
        row
        for row in candidates
        if isinstance(row, dict)
    )

selected: defaultdict[
    tuple[str, str],
    list[dict],
] = defaultdict(list)

for row in rows:
    if row.get("type_verdict") != "ABSTAINED":
        continue

    clause_type = str(
        row.get("pipeline_clause_type")
        or ""
    )

    if clause_type not in TARGETS:
        continue

    language = str(
        row.get("language")
        or "unknown"
    ).lower()

    selected[
        (
            clause_type,
            language,
        )
    ].append(row)

for clause_type in sorted(TARGETS):
    print()
    print("#" * 100)
    print("TYPE:", clause_type)
    print("#" * 100)

    for language in ("en", "fr", "ar"):
        values = selected.get(
            (
                clause_type,
                language,
            ),
            [],
        )

        print()
        print(
            f"--- {language.upper()} "
            f"TOTAL={len(values)} ---"
        )

        for row in values[:5]:
            source = str(
                row.get("source_text")
                or ""
            )

            profile = build_semantic_source_profile(
                source,
                language=language,
            )

            print()
            print("DOC:", row.get("document"))
            print("REF:", row.get("reference"))
            print(
                "PIPELINE:",
                row.get("pipeline_clause_type"),
            )
            print(
                "SHADOW PRIMARY:",
                profile.get("primary_type"),
            )
            print(
                "SHADOW CONFIDENCE:",
                profile.get("confidence"),
            )
            print(
                "ABSTAINED:",
                profile.get("abstained"),
            )
            print(
                "ABSTAIN REASON:",
                profile.get("abstention_reason"),
            )
            print(
                "CANDIDATE:",
                profile.get("candidate_primary_type"),
            )
            print(
                "COVERAGE:",
                profile.get("candidate_coverage"),
            )
            print(
                "DOMINANCE MARGIN:",
                profile.get("dominance_margin"),
            )
            print("SOURCE:")
            print(source)
            print(
                "MECHANISMS:",
                [
                    mechanism.get("kind")
                    for mechanism in (
                        profile.get(
                            "ranked_material_mechanisms"
                        )
                        or []
                    )
                ],
            )
            print(
                "DOMINANCE SCORES:",
                profile.get("dominance_scores")
                or [],
            )
