import json
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

from app.services.contract_agent.contract_parser import  (
    extract_text_from_docx,
)
from app.services.contract_agent.clause_splitter import (
    split_into_clause_objects,
)
from app.services.contract_agent.contract_taxonomy import (
    detect_clause_type_candidates,
)


SUMMARY_PATH = Path(
    "regression_results_multilang/ar/_summary.json"
)
INPUT_DIR = Path("regression_docs")
OUTPUT_PATH = Path(
    "regression_results_multilang/ar/_blocked_diagnostic.json"
)


def get_clause_reference(clause_obj: dict) -> str:
    return str(
        clause_obj.get("clause_reference")
        or clause_obj.get("reference")
        or clause_obj.get("number")
        or ""
    ).strip()


def main() -> None:
    summary = json.loads(
        SUMMARY_PATH.read_text(encoding="utf-8")
    )

    output = []

    for row in summary:
        blocked_rows = row.get("blocked", [])

        if not blocked_rows:
            continue

        document_path = INPUT_DIR / row["file"]

        text = extract_text_from_docx(
            str(document_path)
        )

        clause_objects = split_into_clause_objects(
            text
        )

        clauses_by_reference = {}

        if isinstance(clause_objects, dict):
            raw_clauses = (
                clause_objects.get("clauses")
                or clause_objects.get("results")
                or []
            )
        else:
            raw_clauses = clause_objects or []

        for clause_obj in raw_clauses:
            if not isinstance(clause_obj, dict):
                continue

            reference = get_clause_reference(
                clause_obj
            )

            if reference:
                clauses_by_reference[
                    reference
                ] = clause_obj

        for blocked in blocked_rows:
            reference = str(
                blocked.get("clause_reference")
                or ""
            ).strip()

            clause_obj = clauses_by_reference.get(
                reference,
                {},
            )

            clause_text = str(
                clause_obj.get("text")
                or ""
            )

            candidates = (
                detect_clause_type_candidates(
                    clause_text
                )
                if clause_text
                else []
            )

            output.append({
                "file": row.get("file"),
                "clause_reference": reference,
                "clause_title": blocked.get(
                    "clause_title"
                ),
                "final_clause_type": blocked.get(
                    "clause_type"
                ),
                "field": blocked.get("field"),
                "reasons": blocked.get(
                    "reasons"
                ),
                "source_text": clause_text,
                "text_before_validation": (
                    blocked.get(
                        "text_before_validation"
                    )
                ),
                "taxonomy_candidates": [
                    {
                        "type": candidate.get(
                            "type"
                        ),
                        "score": candidate.get(
                            "score"
                        ),
                        "base_score": candidate.get(
                            "base_score"
                        ),
                        "specificity_bonus": (
                            candidate.get(
                                "specificity_bonus"
                            )
                        ),
                        "context_bonus": candidate.get(
                            "context_bonus"
                        ),
                        "context_penalty": (
                            candidate.get(
                                "context_penalty"
                            )
                        ),
                        "signals": candidate.get(
                            "signals"
                        ),
                    }
                    for candidate in candidates[:10]
                ],
            })

    OUTPUT_PATH.write_text(
        json.dumps(
            output,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print("BLOCKED:", len(output))
    print("OUTPUT:", OUTPUT_PATH)

    print()
    print("=== COMPACT DIAGNOSTIC ===")

    for item in output:
        print()
        print("=" * 100)
        print(
            "FILE:",
            item["file"],
        )
        print(
            "CLAUSE:",
            item["clause_reference"],
        )
        print(
            "TITLE:",
            item["clause_title"],
        )
        print(
            "FINAL TYPE:",
            item["final_clause_type"],
        )
        print(
            "FIELD:",
            item["field"],
        )

        print("CANDIDATES:")

        for candidate in (
            item["taxonomy_candidates"][:5]
        ):
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

        print("GENERATED:")
        print(
            item["text_before_validation"]
        )


if __name__ == "__main__":
    main()
