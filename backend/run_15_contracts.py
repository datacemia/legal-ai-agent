import json
import sys
import traceback
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

from app.services.contract_agent.contract_parser import (
    extract_text_from_docx,
)
from app.services.contract_agent.clause_splitter import (
    split_into_clause_objects,
)
from app.services.contract_agent.contract_agent import (
    ClauseAnalysisPipeline,
)


INPUT_DIR = Path("regression_docs")
OUTPUT_DIR = Path("regression_results_15")

OUTPUT_DIR.mkdir(exist_ok=True)


def audit_result(result: dict) -> dict:
    rows = result.get("clauses", {}).get("results", [])

    receipts = 0
    unsuccessful = 0
    hash_mismatches = 0
    post_gate_mutations = 0
    blocked = []

    for clause in rows:
        clause_receipts = (
            clause.get("validation_receipts") or {}
        )

        for field, receipt in clause_receipts.items():
            receipts += 1

            if receipt.get("successful") is not True:
                unsuccessful += 1

            if (
                receipt.get("validated_text_hash")
                != receipt.get("final_text_hash")
            ):
                hash_mismatches += 1

            if receipt.get("post_gate_mutators"):
                post_gate_mutations += 1

            reasons = (
                receipt.get("validation_reasons") or []
            )

            if reasons:
                blocked.append({
                    "clause_reference": clause.get(
                        "clause_reference"
                    ),
                    "clause_title": clause.get(
                        "clause_title"
                    ),
                    "clause_type": clause.get(
                        "clause_type"
                    ),
                    "field": field,
                    "gate_result": receipt.get(
                        "gate_result"
                    ),
                    "reasons": reasons,
                    "text_before_validation": receipt.get(
                        "text_before_validation"
                    ),
                    "final_text": clause.get(field),
                })

    return {
        "clauses": len(rows),
        "receipts": receipts,
        "unsuccessful": unsuccessful,
        "hash_mismatches": hash_mismatches,
        "post_gate_mutations": post_gate_mutations,
        "blocked": blocked,
    }


def main() -> int:
    files = sorted(INPUT_DIR.glob("*.docx"))

    print("DOCX FOUND:", len(files))

    if len(files) != 15:
        print(
            "ERROR: expected exactly 15 DOCX fixtures, "
            f"found {len(files)}"
        )

        for path in files:
            print(" -", path.name)

        return 1

    summary = []

    for index, path in enumerate(files, 1):
        print()
        print("=" * 80)
        print(f"[{index}/15] {path.name}")
        print("=" * 80)

        try:
            text = extract_text_from_docx(str(path))

            clause_objects = split_into_clause_objects(
                text
            )

            result = ClauseAnalysisPipeline(
                clauses=clause_objects,
                language="en",
                max_clauses=60,
            ).run()

            audit = audit_result(result)

            output_path = (
                OUTPUT_DIR / f"{path.stem}.json"
            )

            output_path.write_text(
                json.dumps(
                    result,
                    ensure_ascii=False,
                    indent=2,
                    default=str,
                ),
                encoding="utf-8",
            )

            row = {
                "file": path.name,
                "status": "PASS",
                **audit,
            }

            summary.append(row)

            print(
                "PASS"
                f" | clauses={audit['clauses']}"
                f" | receipts={audit['receipts']}"
                f" | unsuccessful={audit['unsuccessful']}"
                f" | hash_mismatch={audit['hash_mismatches']}"
                f" | post_gate={audit['post_gate_mutations']}"
                f" | blocked={len(audit['blocked'])}"
            )

            for blocked in audit["blocked"]:
                print(
                    "  BLOCKED:"
                    f" clause={blocked['clause_reference']}"
                    f" field={blocked['field']}"
                    f" reasons={blocked['reasons']}"
                )

        except Exception as exc:
            traceback.print_exc()

            summary.append({
                "file": path.name,
                "status": "ERROR",
                "error_type": type(exc).__name__,
                "error": str(exc),
            })

    summary_path = OUTPUT_DIR / "_summary.json"

    summary_path.write_text(
        json.dumps(
            summary,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    errors = [
        row
        for row in summary
        if row.get("status") != "PASS"
    ]

    integrity_failures = [
        row
        for row in summary
        if (
            row.get("unsuccessful", 0) > 0
            or row.get("hash_mismatches", 0) > 0
            or row.get("post_gate_mutations", 0) > 0
        )
    ]

    total_receipts = sum(
        row.get("receipts", 0)
        for row in summary
    )

    total_blocked = sum(
        len(row.get("blocked", []))
        for row in summary
    )

    print()
    print("=" * 80)
    print("FINAL 15-DOCUMENT SUMMARY")
    print("=" * 80)
    print("DOCUMENTS:", len(summary))
    print("ERRORS:", len(errors))
    print(
        "INTEGRITY FAILURES:",
        len(integrity_failures),
    )
    print("TOTAL RECEIPTS:", total_receipts)
    print("TOTAL BLOCKED:", total_blocked)
    print("SUMMARY:", summary_path)

    if errors or integrity_failures:
        print("FINAL RESULT: FAIL")
        return 1

    print("FINAL RESULT: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())