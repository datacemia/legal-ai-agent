import json
from pathlib import Path

from app.services.contract_agent.semantic_source_profile import (
    build_semantic_source_profile,
)

AUDIT = Path(
    "semantic_audit_final/"
    "semantic_gold_high_failures.json"
)

TARGETS = {
    "INDEPENDENT_CONTRACTOR",
    "EXIT_ASSISTANCE",
    "TERM_DURATION",
    "RENT_OBLIGATION",
    "SECURITY_INTEREST",
    "GUARANTEE",
}

rows = json.loads(
    AUDIT.read_text(encoding="utf-8")
)

def collect_kinds(value):
    kinds = set()

    if isinstance(value, dict):
        kind = value.get("kind")
        if isinstance(kind, str):
            kinds.add(kind)

        for child in value.values():
            kinds.update(collect_kinds(child))

    elif isinstance(value, list):
        for child in value:
            kinds.update(collect_kinds(child))

    return kinds

checked = 0
missing = []

for row in rows:
    required = {
        failure.partition(":")[2]
        for failure in row.get("high", [])
        if failure.startswith(
            "MISSING_MATERIAL_MECHANISM:"
        )
    } & TARGETS

    if not required:
        continue

    profile = build_semantic_source_profile(
        row["source_text"],
        language=row["language"],
    )

    detected = collect_kinds(profile)
    absent = required - detected

    checked += len(required)

    print(
        row["fixture_id"],
        "required=", sorted(required),
        "detected=", sorted(required & detected),
    )

    if absent:
        missing.append({
            "fixture_id": row["fixture_id"],
            "language": row["language"],
            "missing": sorted(absent),
        })

print()
print("TARGET EVENTS:", checked)
print("MISSING:", len(missing))

for failure in missing:
    print(failure)

assert checked == 18, checked
assert not missing, missing

print("LOT 7B-1 TARGETED TEST: PASS")
