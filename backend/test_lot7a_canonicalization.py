import json
from pathlib import Path

path = Path(
    "semantic_audit_lot7a/"
    "semantic_gold_high_failures.json"
)

if not path.exists():
    raise SystemExit(
        f"Missing audit file: {path}. "
        "Run audit_semantic_correctness.py first."
    )

rows = json.loads(path.read_text(encoding="utf-8"))

aliases = {
    "NON_COMPETE_RESTRICTION": "NON_COMPETE",
    "BOARD_COMPOSITION_STRUCTURE": "BOARD_COMPOSITION",
    "LOAN_PRINCIPAL_DISBURSEMENT": "LOAN_DISBURSEMENT",
    "TRANSITION_SERVICE_OBLIGATION": "TRANSITION_PLAN",
}

lot7a_targets = set(aliases.values())

remaining = []
raw_aliases_found = []

for row in rows:
    expected = row.get("expected_semantics", {})
    actual = row.get("actual_semantics", {})

    required = set(expected.get("required_mechanisms", []))
    actual_mechanisms = set(actual.get("mechanisms", []))

    relevant = required & lot7a_targets

    if relevant and not relevant.issubset(actual_mechanisms):
        remaining.append({
            "fixture_id": row.get("fixture_id"),
            "language": row.get("language"),
            "required": sorted(relevant),
            "actual": sorted(actual_mechanisms),
            "high": row.get("high", []),
        })

    for raw_alias in aliases:
        if raw_alias in actual_mechanisms:
            raw_aliases_found.append({
                "fixture_id": row.get("fixture_id"),
                "language": row.get("language"),
                "raw_alias": raw_alias,
            })

print("HIGH FAILURES:", len(rows))
print("REMAINING LOT 7A FAILURES:", len(remaining))

for item in remaining:
    print(item)

print("RAW ALIASES FOUND:", len(raw_aliases_found))

for item in raw_aliases_found:
    print(item)

assert not raw_aliases_found, (
    "Raw Lot 7A detector aliases remain in the fresh audit output"
)

assert len(remaining) == 1, (
    f"Expected exactly one true Lot 7A failure, got {len(remaining)}"
)

failure = remaining[0]

assert failure["fixture_id"] == "12_1_1_ar", failure
assert failure["language"] == "ar", failure
assert failure["required"] == ["LOAN_DISBURSEMENT"], failure
assert failure["actual"] == ["PAY_FREQUENCY"], failure
assert (
    "MISSING_MATERIAL_MECHANISM:LOAN_DISBURSEMENT"
    in failure["high"]
), failure

print("LOT 7A FRESH AUDIT CANONICALIZATION: PASS")
