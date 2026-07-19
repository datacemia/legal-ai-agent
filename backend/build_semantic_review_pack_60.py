#!/usr/bin/env python3
"""Build a 60-clause multilingual human review pack from gold_review_set.jsonl.

Read-only with respect to the contract-agent pipeline.

Selection goals:
- exactly 20 EN, 20 FR, 20 AR when enough rows exist;
- prioritize shadow abstentions;
- stratify across high-impact P0 legal families;
- avoid over-selecting one pipeline type;
- preserve exact source text and current runtime context;
- leave gold fields blank for human annotation.

Outputs:
- review_pack_60.jsonl
- review_pack_60.csv
- review_pack_60_summary.json
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

for stream in (sys.stdout, sys.stderr):
    if hasattr(stream, "reconfigure"):
        stream.reconfigure(
            encoding="utf-8",
            errors="backslashreplace",
        )


TARGET_TYPES = (
    "termination",
    "renewal",
    "automatic_renewal",
    "liability",
    "limitation_of_liability",
    "indemnity",
    "payment",
    "pricing",
    "fees",
    "intellectual_property",
    "ownership",
    "license",
    "work_product",
    "confidentiality",
    "data_protection",
    "data_processing",
    "security",
    "cybersecurity",
    "loan",
    "security_interest",
    "guarantee",
    "employment",
    "compensation",
    "services",
    "service_level",
    "delivery",
    "corporate_governance",
    "governance",
    "share_transfer_rights",
    "anti_dilution_preemptive_rights",
    "investor_information_rights",
)

TYPE_PRIORITY = {
    clause_type: index
    for index, clause_type in enumerate(TARGET_TYPES)
}


def read_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []

    with path.open(
        "r",
        encoding="utf-8",
    ) as handle:
        for line_number, line in enumerate(
            handle,
            1,
        ):
            stripped = line.strip()

            if not stripped:
                continue

            try:
                value = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise RuntimeError(
                    f"{path}:{line_number}: {exc}"
                ) from exc

            if not isinstance(value, dict):
                raise RuntimeError(
                    f"{path}:{line_number}: "
                    "expected JSON object"
                )

            rows.append(value)

    return rows


def row_identity(row: dict) -> tuple[str, str]:
    return (
        str(row.get("document") or ""),
        str(row.get("reference") or ""),
    )


def normalized_type(row: dict) -> str:
    return str(
        row.get("pipeline_primary_type")
        or "unknown"
    ).strip().lower()


def mechanism_names(row: dict) -> list[str]:
    names = []

    for mechanism in (
        row.get("shadow_ranked_material_mechanisms")
        or []
    ):
        if not isinstance(mechanism, dict):
            continue

        kind = str(
            mechanism.get("kind")
            or ""
        ).strip()

        if kind:
            names.append(kind)

    return names


def review_priority(row: dict) -> tuple:
    clause_type = normalized_type(row)

    return (
        0 if row.get("shadow_abstained") is True else 1,
        TYPE_PRIORITY.get(clause_type, len(TYPE_PRIORITY) + 1),
        0 if not mechanism_names(row) else 1,
        str(row.get("document") or ""),
        str(row.get("reference") or ""),
    )


def select_language_rows(
    rows: list[dict],
    *,
    target: int,
) -> list[dict]:
    candidates = sorted(
        rows,
        key=review_priority,
    )

    by_type: defaultdict[str, list[dict]] = defaultdict(list)

    for row in candidates:
        by_type[normalized_type(row)].append(row)

    selected: list[dict] = []
    seen: set[tuple[str, str]] = set()
    selected_type_counts: Counter[str] = Counter()

    # First pass:
    # one row from each priority legal family when available.
    for clause_type in TARGET_TYPES:
        bucket = by_type.get(clause_type) or []

        for row in bucket:
            identity = row_identity(row)

            if identity in seen:
                continue

            selected.append(row)
            seen.add(identity)
            selected_type_counts[clause_type] += 1
            break

        if len(selected) >= target:
            return selected[:target]

    # Second pass:
    # round-robin by type, with a soft cap to avoid one family dominating.
    soft_cap = 3

    while len(selected) < target:
        added = False

        ordered_types = sorted(
            by_type,
            key=lambda clause_type: (
                selected_type_counts[clause_type],
                TYPE_PRIORITY.get(
                    clause_type,
                    len(TYPE_PRIORITY) + 1,
                ),
                clause_type,
            ),
        )

        for clause_type in ordered_types:
            if selected_type_counts[clause_type] >= soft_cap:
                continue

            for row in by_type[clause_type]:
                identity = row_identity(row)

                if identity in seen:
                    continue

                selected.append(row)
                seen.add(identity)
                selected_type_counts[clause_type] += 1
                added = True
                break

            if len(selected) >= target:
                break

        if not added:
            break

    # Final fill:
    # use any remaining high-priority abstained rows.
    if len(selected) < target:
        for row in candidates:
            identity = row_identity(row)

            if identity in seen:
                continue

            selected.append(row)
            seen.add(identity)

            if len(selected) >= target:
                break

    return selected[:target]


def clean_gold_fields(row: dict) -> dict:
    output = dict(row)

    output["review_status"] = "PENDING"
    output["reviewer"] = ""
    output["review_notes"] = ""

    output["gold_primary_type"] = ""
    output["gold_material_mechanisms"] = []
    output["gold_actor_object_arguments"] = []
    output["gold_polarity"] = []
    output["gold_procedural_states"] = []
    output["gold_numeric_semantic_roles"] = []
    output["gold_source_evidence_spans"] = []

    return output


def write_jsonl(
    path: Path,
    rows: list[dict],
) -> None:
    with path.open(
        "w",
        encoding="utf-8",
    ) as handle:
        for row in rows:
            handle.write(
                json.dumps(
                    row,
                    ensure_ascii=False,
                )
            )
            handle.write("\n")


def csv_value(value: Any) -> str:
    if isinstance(value, (dict, list)):
        return json.dumps(
            value,
            ensure_ascii=False,
        )

    if value is None:
        return ""

    return str(value)


def write_csv(
    path: Path,
    rows: list[dict],
) -> None:
    fields = [
        "review_status",
        "reviewer",
        "review_notes",
        "language",
        "document",
        "reference",
        "title",
        "source_text",
        "pipeline_primary_type",
        "pipeline_confidence",
        "shadow_primary_type",
        "shadow_confidence",
        "shadow_abstained",
        "shadow_abstention_reason",
        "shadow_candidate_primary_type",
        "shadow_candidate_coverage",
        "shadow_ranked_material_mechanisms",
        "gold_primary_type",
        "gold_material_mechanisms",
        "gold_actor_object_arguments",
        "gold_polarity",
        "gold_procedural_states",
        "gold_numeric_semantic_roles",
        "gold_source_evidence_spans",
    ]

    with path.open(
        "w",
        encoding="utf-8-sig",
        newline="",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fields,
            extrasaction="ignore",
        )

        writer.writeheader()

        for row in rows:
            writer.writerow({
                field: csv_value(
                    row.get(field)
                )
                for field in fields
            })


def main() -> int:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "input",
        type=Path,
    )

    parser.add_argument(
        "--out",
        type=Path,
        default=Path("semantic_gold/review_pack_60"),
    )

    parser.add_argument(
        "--per-language",
        type=int,
        default=20,
    )

    args = parser.parse_args()

    rows = read_jsonl(args.input)

    args.out.mkdir(
        parents=True,
        exist_ok=True,
    )

    selected = []

    language_counts = Counter()

    for language in ("en", "fr", "ar"):
        language_rows = [
            row
            for row in rows
            if str(
                row.get("language")
                or ""
            ).strip().lower() == language
        ]

        chosen = select_language_rows(
            language_rows,
            target=max(
                1,
                args.per_language,
            ),
        )

        selected.extend(
            clean_gold_fields(row)
            for row in chosen
        )

        language_counts[language] = len(chosen)

    jsonl_path = (
        args.out / "review_pack_60.jsonl"
    )

    csv_path = (
        args.out / "review_pack_60.csv"
    )

    summary_path = (
        args.out / "review_pack_60_summary.json"
    )

    write_jsonl(
        jsonl_path,
        selected,
    )

    write_csv(
        csv_path,
        selected,
    )

    type_counts = Counter(
        normalized_type(row)
        for row in selected
    )

    abstention_counts = Counter(
        str(
            row.get("language")
            or ""
        )
        for row in selected
        if row.get("shadow_abstained") is True
    )

    documents = Counter(
        str(
            row.get("document")
            or ""
        )
        for row in selected
    )

    summary = {
        "input_rows": len(rows),
        "selected_rows": len(selected),
        "selected_by_language": dict(
            language_counts
        ),
        "selected_by_pipeline_type": dict(
            type_counts.most_common()
        ),
        "selected_abstentions_by_language": dict(
            abstention_counts
        ),
        "distinct_documents": len(documents),
        "gold_fields_reset_to_blank": True,
        "human_review_required": True,
        "publication_gate_modified": False,
        "pipeline_modified": False,
        "jsonl": str(jsonl_path),
        "csv": str(csv_path),
    }

    summary_path.write_text(
        json.dumps(
            summary,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print("=" * 88)
    print("SEMANTIC HUMAN REVIEW PACK")
    print("=" * 88)
    print(
        "INPUT ROWS:",
        summary["input_rows"],
    )
    print(
        "SELECTED ROWS:",
        summary["selected_rows"],
    )
    print(
        "SELECTED BY LANGUAGE:",
        summary["selected_by_language"],
    )
    print(
        "ABSTENTIONS BY LANGUAGE:",
        summary[
            "selected_abstentions_by_language"
        ],
    )
    print(
        "DISTINCT DOCUMENTS:",
        summary["distinct_documents"],
    )
    print("JSONL:", jsonl_path)
    print("CSV:", csv_path)
    print("SUMMARY:", summary_path)

    print("\nSELECTED TYPES")

    for clause_type, count in (
        type_counts.most_common()
    ):
        print(
            f"{count:4d}  {clause_type}"
        )

    expected_total = (
        max(
            1,
            args.per_language,
        )
        * 3
    )

    if len(selected) != expected_total:
        print(
            "\nWARNING: expected",
            expected_total,
            "selected rows but produced",
            len(selected),
        )

        return 3

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
