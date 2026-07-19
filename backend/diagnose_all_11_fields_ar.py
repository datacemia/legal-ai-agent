import json
from collections import Counter, defaultdict
from pathlib import Path

from app.services.contract_agent.contract_taxonomy import (
    detect_clause_type_candidates,
    detect_clause_type_from_taxonomy,
)
from app.services.contract_agent.publication_gate import (
    PROTECTED_FIELDS,
    _FIELD_POLICIES,
)

SUMMARY_PATH = Path("regression_results_multilang/ar/_summary.json")
OUTPUT_PATH = Path(
    "regression_results_multilang/ar/_all_11_fields_diagnostic.json"
)


def compact_candidates(text: str, limit: int = 5) -> list[dict]:
    candidates = detect_clause_type_candidates(text or "")

    return [
        {
            "type": item.get("type"),
            "score": item.get("score"),
            "base_score": item.get("base_score"),
            "specificity_bonus": item.get("specificity_bonus"),
            "context_bonus": item.get("context_bonus"),
            "context_penalty": item.get("context_penalty"),
            "signals": item.get("signals"),
        }
        for item in candidates[:limit]
    ]


def main() -> None:
    data = json.loads(
        SUMMARY_PATH.read_text(encoding="utf-8")
    )

    rows = []
    by_field = Counter()
    by_policy = Counter()
    by_type_field = Counter()
    by_generated_type = Counter()
    by_transition = Counter()

    for document in data:
        for blocked in document.get("blocked", []):
            field = blocked.get("field") or "UNKNOWN"
            source_text = str(
                blocked.get("source_text")
                or blocked.get("clause_text")
                or blocked.get("quoted_text")
                or ""
            )
            generated = str(
                blocked.get("text_before_validation")
                or ""
            )

            source_type = (
                detect_clause_type_from_taxonomy(source_text)
                if source_text
                else "SOURCE_NOT_IN_SUMMARY"
            )
            generated_type = (
                detect_clause_type_from_taxonomy(generated)
                if generated
                else "EMPTY"
            )

            row = {
                "file": document.get("file"),
                "clause_reference": blocked.get("clause_reference"),
                "clause_title": blocked.get("clause_title"),
                "final_clause_type": blocked.get("clause_type"),
                "field": field,
                "field_policy": _FIELD_POLICIES.get(field, "UNKNOWN"),
                "reasons": blocked.get("reasons") or [],
                "source_text_available": bool(source_text),
                "source_type": source_type,
                "generated_type": generated_type,
                "generated_text": generated,
                "source_candidates": (
                    compact_candidates(source_text)
                    if source_text
                    else []
                ),
                "generated_candidates": compact_candidates(generated),
            }
            rows.append(row)

            by_field[field] += 1
            by_policy[row["field_policy"]] += 1
            by_type_field[
                (row["final_clause_type"], field)
            ] += 1
            by_generated_type[generated_type] += 1
            by_transition[
                (row["final_clause_type"], generated_type, field)
            ] += 1

    OUTPUT_PATH.write_text(
        json.dumps(
            rows,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print("=== PROTECTED FIELDS ===")
    for field in PROTECTED_FIELDS:
        print(
            f"{field:<28}",
            "policy=",
            _FIELD_POLICIES.get(field),
            "blocked=",
            by_field.get(field, 0),
        )

    print()
    print("TOTAL BLOCKED:", len(rows))

    print()
    print("=== BY POLICY ===")
    for key, value in by_policy.most_common():
        print(value, key)

    print()
    print("=== GENERATED TYPES ===")
    for key, value in by_generated_type.most_common():
        print(value, key)

    print()
    print("=== FINAL TYPE -> GENERATED TYPE -> FIELD ===")
    for key, value in by_transition.most_common():
        print(value, key)

    print()
    print("=== FULL CASES ===")

    for row in rows:
        print()
        print("=" * 100)
        print("FILE:", row["file"])
        print("CLAUSE:", row["clause_reference"])
        print("TITLE:", row["clause_title"])
        print("FINAL TYPE:", row["final_clause_type"])
        print("FIELD:", row["field"])
        print("POLICY:", row["field_policy"])
        print("SOURCE TYPE:", row["source_type"])
        print("GENERATED TYPE:", row["generated_type"])
        print("GENERATED CANDIDATES:")
        for candidate in row["generated_candidates"]:
            print(
                " ",
                candidate["type"],
                "score=",
                candidate["score"],
                "base=",
                candidate["base_score"],
                "specificity=",
                candidate["specificity_bonus"],
                "context+=",
                candidate["context_bonus"],
                "context-=",
                candidate["context_penalty"],
                "signals=",
                candidate["signals"],
            )
        print("TEXT BEFORE VALIDATION:")
        print(row["generated_text"])

    print()
    print("OUTPUT:", OUTPUT_PATH)


if __name__ == "__main__":
    main()
