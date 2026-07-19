from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DEFAULT_SOURCE = Path("semantic_audit_final/semantic_discovery_details.json")
DEFAULT_OUTPUT = Path("gold_review_queue")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def stable_candidate_id(item: dict[str, Any]) -> str:
    identity = {
        "document": item.get("document"),
        "reference": item.get("reference"),
        "source_language": item.get("source_language"),
        "source_text": item.get("source_text"),
    }
    digest = hashlib.sha256(
        json.dumps(identity, ensure_ascii=False, sort_keys=True).encode("utf-8")
    ).hexdigest()[:12]
    language = str(item.get("source_language") or "unknown").lower()
    return f"{language}_{digest}"


def verdict_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.upper()
    if isinstance(value, bool):
        return "PASS" if value else "FAIL"
    if isinstance(value, dict):
        return " ".join(
            str(value[key])
            for key in ("verdict", "status", "result", "reason")
            if key in value
        ).upper()
    return str(value).upper()


def is_failure_verdict(value: Any) -> bool:
    text = verdict_text(value)
    return any(
        marker in text
        for marker in (
            "FAIL",
            "MISMATCH",
            "PARTIAL",
            "MISSING",
            "UNSUPPORTED",
            "REVIEW",
            "INCOMPLETE",
        )
    )


def has_items(value: Any) -> bool:
    return isinstance(value, list) and bool(value)


def classify_candidate(item: dict[str, Any]) -> tuple[list[str], str]:
    """
    Reproduce the semantic audit summary exactly.

    Gold review population:
      - REVIEW_REQUIRED comes only from primary_type_verdict.
      - PARTIAL_EXTRACTION comes only from mechanism_extraction_verdict == PARTIAL.
      - PRIMARY_TYPE_MISMATCH comes only from primary_type_verdict == MISMATCH.

    FAIL and unsupported mechanisms are audit failures, not Gold-review
    candidates, and must not be silently promoted into this queue.
    """
    reasons: list[str] = []

    primary_verdict = verdict_text(item.get("primary_type_verdict"))
    extraction_verdict = verdict_text(
        item.get("mechanism_extraction_verdict")
    )

    if primary_verdict == "REVIEW_REQUIRED":
        reasons.append("REVIEW_REQUIRED")

    if extraction_verdict == "PARTIAL":
        reasons.append("PARTIAL_EXTRACTION")

    if primary_verdict == "MISMATCH":
        reasons.append("PRIMARY_TYPE_MISMATCH")

    if not reasons:
        return [], "NOT_REQUIRED"

    if (
        "PARTIAL_EXTRACTION" in reasons
        or "PRIMARY_TYPE_MISMATCH" in reasons
    ):
        return reasons, "A"

    return reasons, "B"


def build_record(
    item: dict[str, Any],
    reasons: list[str],
    priority: str,
    source_file: Path,
) -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "candidate_id": stable_candidate_id(item),
        "status": "PENDING",
        "priority": priority,
        "review_reasons": reasons,
        "source": {
            "audit_file": str(source_file),
            "document": item.get("document"),
            "reference": item.get("reference"),
            "language": item.get("source_language"),
            "text": item.get("source_text"),
        },
        "classification": {
            "primary_type": item.get("primary_type"),
            "primary_type_verdict": item.get("primary_type_verdict"),
        },
        "mechanisms": {
            "expected": item.get("expected_source_mechanisms") or [],
            "extracted": item.get("extracted_mechanisms") or [],
            "missing_high_confidence": item.get(
                "missing_high_confidence_mechanisms"
            ) or [],
            "unsupported": item.get("unsupported_extracted_mechanisms") or [],
            "material_without_evidence": item.get(
                "material_mechanisms_without_evidence"
            ) or [],
        },
        "verdicts": {
            "mechanism_extraction": item.get("mechanism_extraction_verdict"),
            "grounding": item.get("grounding_verdict"),
        },
        "review": {
            "decision": None,
            "reviewer": None,
            "reviewed_at": None,
            "notes": "",
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    source_file = args.source.resolve()
    output_dir = args.out.resolve()

    if not source_file.exists():
        print(f"ABORT: source not found: {source_file}")
        return 1

    if (
        output_dir == source_file
        or output_dir == source_file.parent
        or output_dir in source_file.parents
    ):
        print("ABORT: output path overlaps the source audit location.")
        return 1

    source_hash_before = hashlib.sha256(source_file.read_bytes()).hexdigest()

    try:
        records = load_json(source_file)
    except Exception as exc:
        print(f"ABORT: invalid source: {exc}")
        return 1

    if not isinstance(records, list):
        print("ABORT: source JSON must contain a top-level list.")
        return 1

    candidates: list[dict[str, Any]] = []
    skipped = 0

    for index, item in enumerate(records):
        if not isinstance(item, dict):
            print(f"ABORT: item {index} is not an object.")
            return 1

        reasons, priority = classify_candidate(item)
        if not reasons:
            skipped += 1
            continue

        candidates.append(build_record(item, reasons, priority, source_file))

    candidates.sort(
        key=lambda c: (
            c["priority"],
            c["source"]["language"] or "",
            c["source"]["document"] or "",
            c["source"]["reference"] or "",
            c["candidate_id"],
        )
    )

    priority_counts = Counter(c["priority"] for c in candidates)
    language_counts = Counter(
        c["source"]["language"] or "unknown" for c in candidates
    )
    reason_counts = Counter(
        reason for c in candidates for reason in c["review_reasons"]
    )

    expected_counts = {
        "REVIEW_REQUIRED": 301,
        "PARTIAL_EXTRACTION": 11,
        "PRIMARY_TYPE_MISMATCH": 6,
    }
    actual_counts = {
        key: reason_counts.get(key, 0)
        for key in expected_counts
    }

    if actual_counts != expected_counts:
        print("ABORT: classification does not match audit summary.")
        print("EXPECTED:", expected_counts)
        print("ACTUAL:", actual_counts)
        return 3

    print("=" * 72)
    print("GOLD REVIEW QUEUE")
    print("=" * 72)
    print("SOURCE:", source_file)
    print("SOURCE SHA256:", source_hash_before)
    print("DISCOVERY RECORDS:", len(records))
    print("REVIEW CANDIDATES:", len(candidates))
    print("NOT REQUIRED:", skipped)
    print("BY PRIORITY:", dict(priority_counts))
    print("BY LANGUAGE:", dict(language_counts))
    print("BY REASON:", dict(reason_counts))

    if args.dry_run:
        print("DRY RUN: no files written.")
        return 0

    if output_dir.exists():
        if not args.force:
            print(f"ABORT: output already exists: {output_dir}")
            print("Use --force only to replace the generated queue.")
            return 1
        shutil.rmtree(output_dir)

    for candidate in candidates:
        target = (
            output_dir
            / "pending"
            / candidate["priority"]
            / (candidate["source"]["language"] or "unknown")
            / f"{candidate['candidate_id']}.json"
        )
        write_json(target, candidate)

    manifest = {
        "schema_version": "1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "mode": "READ_ONLY_DERIVED_QUEUE",
        "source": {
            "file": str(source_file),
            "sha256": source_hash_before,
            "records": len(records),
        },
        "summary": {
            "review_candidates": len(candidates),
            "not_required": skipped,
            "by_priority": dict(sorted(priority_counts.items())),
            "by_language": dict(sorted(language_counts.items())),
            "by_reason": dict(sorted(reason_counts.items())),
        },
        "candidate_ids": [c["candidate_id"] for c in candidates],
    }
    write_json(output_dir / "manifest.json", manifest)
    write_json(
        output_dir / "decisions.json",
        {"schema_version": "1.0", "decisions": []},
    )

    source_hash_after = hashlib.sha256(source_file.read_bytes()).hexdigest()
    if source_hash_after != source_hash_before:
        print("CRITICAL: source audit file changed during generation.")
        return 2

    print("QUEUE WRITTEN:", output_dir)
    print("SOURCE INTEGRITY: PASS")
    print("NO GOLD OR ENGINE FILE WAS MODIFIED.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
