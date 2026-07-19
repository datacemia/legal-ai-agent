#!/usr/bin/env python3
from __future__ import annotations

import ast
import hashlib
import shutil
from datetime import datetime
from pathlib import Path

TARGET = Path("app/services/contract_agent/contract_family_detector.py")

OLD_PICK = '''def pick_primary_family(ranked: list[tuple[str, int]]) -> tuple[str, int]:
    if not ranked:
        return "General", 0

    top_score = ranked[0][1]
    close = [
        item
        for item in ranked
        if item[1] >= top_score * 0.85
    ]

    if len(close) == 1:
        return ranked[0]

    # Prefer structural family among close candidates.
    for preferred in PRIMARY_FAMILY_PRIORITY:
        for family, score in close:
            if family == preferred:
                return family, score

    return ranked[0]
'''

NEW_PICK = '''def _family_evidence_quality(
    family: str,
    family_evidence: list[dict] | None,
) -> dict:
    """Summarize evidence using the existing 5/3/1 specificity tiers."""
    weighted_groups = FAMILY_INDICATORS.get(family, {}) or {}
    term_weight = {}

    for weight, terms in weighted_groups.items():
        for term in terms:
            normalized = normalize_text(term)
            if normalized:
                term_weight[normalized] = max(
                    int(weight),
                    term_weight.get(normalized, 0),
                )

    distinct_by_weight = {5: set(), 3: set(), 1: set()}
    points_by_weight = {5: 0, 3: 0, 1: 0}

    for item in family_evidence or []:
        if not isinstance(item, dict):
            continue

        term = normalize_text(item.get("term"))
        base_weight = term_weight.get(term)

        if base_weight not in distinct_by_weight:
            continue

        distinct_by_weight[base_weight].add(term)

        try:
            points = int(item.get("points") or 0)
        except (TypeError, ValueError):
            points = 0

        points_by_weight[base_weight] += max(points, 0)

    total_points = sum(points_by_weight.values())
    generic_points = points_by_weight[1]

    return {
        "identity_count": len(distinct_by_weight[5]),
        "specific_count": len(distinct_by_weight[3]),
        "generic_count": len(distinct_by_weight[1]),
        "identity_points": points_by_weight[5],
        "specific_points": points_by_weight[3],
        "generic_points": generic_points,
        "generic_ratio": (
            generic_points / total_points
            if total_points
            else 0.0
        ),
    }


def pick_primary_family(
    ranked: list[tuple[str, int]],
    evidence: dict | None = None,
) -> tuple[str, int]:
    """Resolve close candidates without changing raw family scores."""
    if not ranked:
        return "General", 0

    top_score = ranked[0][1]
    close = [
        item
        for item in ranked
        if item[1] >= top_score * 0.85
    ]

    if len(close) == 1:
        return ranked[0]

    legacy_choice = ranked[0]

    for preferred in PRIMARY_FAMILY_PRIORITY:
        for family, score in close:
            if family == preferred:
                legacy_choice = (family, score)
                break
        else:
            continue
        break

    raw_winner = ranked[0]

    if (
        raw_winner[0] == legacy_choice[0]
        or not isinstance(evidence, dict)
    ):
        return legacy_choice

    raw_quality = _family_evidence_quality(
        raw_winner[0],
        evidence.get(raw_winner[0], []),
    )
    legacy_quality = _family_evidence_quality(
        legacy_choice[0],
        evidence.get(legacy_choice[0], []),
    )

    rich_specific_support = (
        raw_quality["specific_count"] >= 3
        and raw_quality["specific_points"] >= 12
        and raw_quality["specific_count"]
        >= legacy_quality["specific_count"] + 2
    )

    legacy_is_generic_dependent = (
        legacy_quality["identity_count"] == 0
        and legacy_quality["generic_count"] >= 1
        and legacy_quality["generic_ratio"] >= 0.60
    )

    raw_is_materially_competitive = (
        raw_winner[1] >= legacy_choice[1]
        and raw_winner[1] >= top_score * 0.95
    )

    if (
        rich_specific_support
        and legacy_is_generic_dependent
        and raw_is_materially_competitive
    ):
        return raw_winner

    return legacy_choice
'''

OLD_CALL = '''    top_family, top_score = pick_primary_family(ranked)
'''
NEW_CALL = '''    top_family, top_score = pick_primary_family(
        ranked,
        evidence,
    )
'''


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    if not TARGET.exists():
        raise SystemExit(f"TARGET NOT FOUND: {TARGET}")

    source = TARGET.read_text(encoding="utf-8")
    ast.parse(source)

    if "def _family_evidence_quality(" in source:
        raise SystemExit(
            "REFUSING DOUBLE PATCH: V4.1.20 resolver already present"
        )

    pick_count = source.count(OLD_PICK)
    call_count = source.count(OLD_CALL)

    if pick_count != 1:
        raise SystemExit(
            f"PICK_PRIMARY_FAMILY BLOCK MISMATCH: expected 1, found {pick_count}"
        )
    if call_count != 1:
        raise SystemExit(
            f"PICK_PRIMARY_FAMILY CALL MISMATCH: expected 1, found {call_count}"
        )

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = TARGET.with_name(
        TARGET.name + ".before_v4_1_20_" + stamp
    )
    shutil.copy2(TARGET, backup)

    updated = source.replace(OLD_PICK, NEW_PICK, 1)
    updated = updated.replace(OLD_CALL, NEW_CALL, 1)

    ast.parse(updated)
    compile(updated, str(TARGET), "exec")
    TARGET.write_text(updated, encoding="utf-8", newline="\n")

    print("=" * 96)
    print("V4.1.20 GENERAL CLOSE-CANDIDATE DOMINANCE RESOLVER APPLIED")
    print("=" * 96)
    print("TARGET :", TARGET)
    print("BACKUP :", backup)
    print("SHA256 :", sha256(TARGET))
    print("A: raw scores and evidence generation preserved")
    print("B: clear winners preserve historical behavior")
    print("C: historical close-candidate priority remains baseline")
    print("D: rich specific evidence may override generic-dependent priority")
    print("E: existing 5/3/1 tiers used as identity/specific/generic")
    print("F: no family name or language literal in dominance decision")
    print("UNTOUCHED: FAMILY_INDICATORS, TITLE_PATTERNS, title_zone,")
    print("           raw score calculation, semantic profile, publication gate,")
    print("           clause risk scoring, taxonomy, frontend")
    print("AST: OK")
    print("=" * 96)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
