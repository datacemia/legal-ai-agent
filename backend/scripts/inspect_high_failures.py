from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


SOURCE = Path(
    "semantic_audit/high_failure_review/high_failure_review.jsonl"
)

OUTPUT = Path(
    "semantic_audit/high_failure_review/high_failure_analysis.md"
)


def pretty(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
    )


if not SOURCE.exists():
    raise SystemExit(f"Missing file: {SOURCE}")

rows = []

for line_number, line in enumerate(
    SOURCE.read_text(encoding="utf-8").splitlines(),
    start=1,
):
    line = line.strip()

    if not line:
        continue

    try:
        row = json.loads(line)
    except json.JSONDecodeError as exc:
        raise SystemExit(
            f"Invalid JSON on line {line_number}: {exc}"
        ) from exc

    rows.append(row)

if len(rows) != 12:
    raise SystemExit(
        f"Expected 12 high failures, found {len(rows)}"
    )

by_family: dict[str, list[dict[str, Any]]] = defaultdict(list)

for row in rows:
    fixture_id = str(row.get("fixture_id") or "")
    parts = fixture_id.rsplit("_", 1)
    family_id = parts[0] if len(parts) == 2 else fixture_id
    by_family[family_id].append(row)

stage_counts = Counter(
    str(row.get("first_bad_stage") or "UNKNOWN")
    for row in rows
)

language_counts = Counter(
    str(row.get("language") or "unknown")
    for row in rows
)

lines = [
    "# High Failure Analysis",
    "",
    f"- Total failures: **{len(rows)}**",
    f"- Fixture families: **{len(by_family)}**",
    f"- Languages: `{dict(language_counts)}`",
    f"- First bad stages: `{dict(stage_counts)}`",
    "",
]

for family_id in sorted(by_family):
    family_rows = sorted(
        by_family[family_id],
        key=lambda row: str(row.get("language") or ""),
    )

    lines.extend([
        f"## Fixture family `{family_id}`",
        "",
    ])

    for row in family_rows:
        fixture_id = row.get("fixture_id", "")
        language = row.get("language", "")
        stage = row.get("first_bad_stage", "")
        root_cause = row.get("root_cause", "")
        source_text = row.get("source_text", "")
        source_evidence = row.get("source_evidence", [])
        expected = row.get("expected_semantics", {})
        actual = row.get("actual_semantics", {})

        lines.extend([
            f"### `{fixture_id}` — `{language}`",
            "",
            f"**First bad stage:** `{stage}`",
            "",
            f"**Root cause:** {root_cause}",
            "",
            "**Source text**",
            "",
            "```text",
            str(source_text),
            "```",
            "",
            "**Source evidence**",
            "",
            "```json",
            pretty(source_evidence),
            "```",
            "",
            "**Expected semantics**",
            "",
            "```json",
            pretty(expected),
            "```",
            "",
            "**Actual semantics**",
            "",
            "```json",
            pretty(actual),
            "```",
            "",
            "**Human review**",
            "",
            "- Decision: `PENDING`",
            "- Classification: `ENGINE_BUG / GOLD_BUG / AUDIT_BUG / ACCEPTABLE_ABSTENTION`",
            "- Comment:",
            "",
            "---",
            "",
        ])

OUTPUT.write_text(
    "\n".join(lines),
    encoding="utf-8",
)

print("=" * 72)
print("HIGH FAILURE ANALYSIS CREATED")
print("=" * 72)
print("ROWS      :", len(rows))
print("FAMILIES  :", len(by_family))
print("LANGUAGES :", dict(language_counts))
print("STAGES    :", dict(stage_counts))
print("OUTPUT    :", OUTPUT)
