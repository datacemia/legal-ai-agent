from __future__ import annotations

import csv
import json
from pathlib import Path

SOURCE = Path("semantic_audit/semantic_gold_high_failures.json")
OUTDIR = Path("semantic_audit/high_failure_review")

OUTDIR.mkdir(parents=True, exist_ok=True)

if not SOURCE.exists():
    raise SystemExit(f"Missing: {SOURCE}")

rows = json.loads(SOURCE.read_text(encoding="utf-8"))

csv_path = OUTDIR / "high_failure_review.csv"
jsonl_path = OUTDIR / "high_failure_review.jsonl"

fieldnames = [
    "fixture_id",
    "language",
    "critical",
    "high",
    "first_bad_stage",
    "root_cause",
    "source_text",
    "source_evidence",
    "expected_semantics",
    "actual_semantics",
    "review_decision",
    "reviewer",
    "review_date",
    "review_comment",
]

with csv_path.open(
    "w",
    encoding="utf-8-sig",
    newline="",
) as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()

    for row in rows:
        out = {
            "fixture_id": row.get("fixture_id"),
            "language": row.get("language"),
            "critical": row.get("critical"),
            "high": row.get("high"),
            "first_bad_stage": row.get("first_bad_stage"),
            "root_cause": row.get("root_cause"),
            "source_text": row.get("source_text"),
            "source_evidence": json.dumps(
                row.get("source_evidence", []),
                ensure_ascii=False,
            ),
            "expected_semantics": json.dumps(
                row.get("expected_semantics", {}),
                ensure_ascii=False,
            ),
            "actual_semantics": json.dumps(
                row.get("actual_semantics", {}),
                ensure_ascii=False,
            ),
            "review_decision": "PENDING",
            "reviewer": "",
            "review_date": "",
            "review_comment": "",
        }

        writer.writerow(out)

with jsonl_path.open("w", encoding="utf-8") as f:
    for row in rows:
        row["review_decision"] = "PENDING"
        row["reviewer"] = ""
        row["review_date"] = ""
        row["review_comment"] = ""
        f.write(json.dumps(row, ensure_ascii=False) + "\n")

print("=" * 70)
print("HIGH FAILURE REVIEW PACKAGE CREATED")
print("=" * 70)
print("FAILURES :", len(rows))
print("CSV       :", csv_path)
print("JSONL     :", jsonl_path)
