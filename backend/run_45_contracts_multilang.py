import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(
        encoding="utf-8",
        errors="backslashreplace",
    )

if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(
        encoding="utf-8",
        errors="backslashreplace",
    )

import json
import sys
import traceback
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

from app.services.contract_agent.contract_parser import extract_text_from_docx
from app.services.contract_agent.clause_splitter import split_into_clause_objects
from app.services.contract_agent.contract_agent import ClauseAnalysisPipeline


INPUT_DIR = Path("regression_docs")
OUTPUT_ROOT = Path("regression_results_multilang")
EXPECTED_PER_LANGUAGE = 15

OUTPUT_ROOT.mkdir(exist_ok=True)


def detect_language(path: Path) -> str:
    stem = path.stem.upper()

    if stem.endswith("_FR"):
        return "fr"

    if stem.endswith("_AR"):
        return "ar"

    return "en"


def audit_result(result: dict) -> dict:
    rows = result.get("clauses", {}).get("results", [])

    receipts = 0
    unsuccessful = 0
    hash_mismatches = 0
    post_gate_mutations = 0
    blocked = []

    for clause in rows:
        clause_receipts = clause.get("validation_receipts") or {}

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

            reasons = receipt.get("validation_reasons") or []

            if reasons:
                blocked.append({
                    "clause_reference": clause.get("clause_reference"),
                    "clause_title": clause.get("clause_title"),
                    "clause_type": clause.get("clause_type"),
                    "field": field,
                    "gate_result": receipt.get("gate_result"),
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

    grouped = {
        "en": [],
        "fr": [],
        "ar": [],
    }

    for path in files:
        grouped[detect_language(path)].append(path)

    print("DOCX FOUND:", len(files))
    print("EN:", len(grouped["en"]))
    print("FR:", len(grouped["fr"]))
    print("AR:", len(grouped["ar"]))

    bad_counts = {
        language: len(paths)
        for language, paths in grouped.items()
        if len(paths) != EXPECTED_PER_LANGUAGE
    }

    if bad_counts or len(files) != EXPECTED_PER_LANGUAGE * 3:
        print("ERROR: expected 15 EN + 15 FR + 15 AR fixtures")

        for language, paths in grouped.items():
            print()
            print(language.upper(), len(paths))

            for path in paths:
                print(" -", path.name)

        return 1

    global_summary = []
    failed = False

    for language in ("en", "fr", "ar"):
        output_dir = OUTPUT_ROOT / language
        output_dir.mkdir(parents=True, exist_ok=True)

        language_summary = []

        print()
        print("#" * 88)
        print(f"LANGUAGE: {language.upper()}")
        print("#" * 88)

        for index, path in enumerate(grouped[language], 1):
            print()
            print("=" * 88)
            print(
                f"[{language.upper()} {index}/"
                f"{EXPECTED_PER_LANGUAGE}] {path.name}"
            )
            print("=" * 88)

            try:
                text = extract_text_from_docx(str(path))
                clause_objects = split_into_clause_objects(text)

                result = ClauseAnalysisPipeline(
                    clauses=clause_objects,
                    language=language,
                    max_clauses=60,
                ).run()

                audit = audit_result(result)

                output_path = output_dir / f"{path.stem}.json"

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
                    "language": language,
                    "file": path.name,
                    "status": "PASS",
                    **audit,
                }

                language_summary.append(row)
                global_summary.append(row)

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
                failed = True

                row = {
                    "language": language,
                    "file": path.name,
                    "status": "ERROR",
                    "error_type": type(exc).__name__,
                    "error": str(exc),
                }

                language_summary.append(row)
                global_summary.append(row)

        language_summary_path = output_dir / "_summary.json"

        language_summary_path.write_text(
            json.dumps(
                language_summary,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        language_errors = [
            row
            for row in language_summary
            if row.get("status") != "PASS"
        ]

        language_integrity_failures = [
            row
            for row in language_summary
            if (
                row.get("unsuccessful", 0) > 0
                or row.get("hash_mismatches", 0) > 0
                or row.get("post_gate_mutations", 0) > 0
            )
        ]

        if language_errors or language_integrity_failures:
            failed = True

        print()
        print("-" * 88)
        print(f"{language.upper()} SUMMARY")
        print("-" * 88)
        print("DOCUMENTS:", len(language_summary))
        print("ERRORS:", len(language_errors))
        print(
            "INTEGRITY FAILURES:",
            len(language_integrity_failures),
        )
        print(
            "TOTAL RECEIPTS:",
            sum(row.get("receipts", 0) for row in language_summary),
        )
        print(
            "TOTAL BLOCKED:",
            sum(len(row.get("blocked", [])) for row in language_summary),
        )
        print("SUMMARY:", language_summary_path)

    global_summary_path = (
        OUTPUT_ROOT / "_summary_all_languages.json"
    )

    global_summary_path.write_text(
        json.dumps(
            global_summary,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    errors = [
        row
        for row in global_summary
        if row.get("status") != "PASS"
    ]

    integrity_failures = [
        row
        for row in global_summary
        if (
            row.get("unsuccessful", 0) > 0
            or row.get("hash_mismatches", 0) > 0
            or row.get("post_gate_mutations", 0) > 0
        )
    ]

    print()
    print("#" * 88)
    print("FINAL MULTILINGUAL SUMMARY")
    print("#" * 88)
    print("EXPECTED RUNS:", EXPECTED_PER_LANGUAGE * 3)
    print("COMPLETED RUNS:", len(global_summary))
    print("ERRORS:", len(errors))
    print("INTEGRITY FAILURES:", len(integrity_failures))
    print(
        "TOTAL RECEIPTS:",
        sum(row.get("receipts", 0) for row in global_summary),
    )
    print(
        "TOTAL BLOCKED:",
        sum(len(row.get("blocked", [])) for row in global_summary),
    )
    print("SUMMARY:", global_summary_path)

    if failed or errors or integrity_failures:
        print("FINAL RESULT: FAIL")
        return 1

    print("FINAL RESULT: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
