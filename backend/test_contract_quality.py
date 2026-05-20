import json
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

from app.services.contract_agent.contract_parser import extract_text
from app.services.contract_agent.clause_splitter import split_into_clauses
from app.services.contract_agent.contract_agent import (
    analyze_contract_clauses,
)
from app.services.contract_agent.validator import (
    validate_contract_result,
    is_probably_contract,
)

TEST_DIR = Path("test_contracts")
TEST_FILE = "test1.pdf"

OUTPUT_DIR = Path("debug_output")
OUTPUT_DIR.mkdir(exist_ok=True)


def dump_json(name: str, data):
    path = OUTPUT_DIR / name

    with open(path, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            indent=2,
            ensure_ascii=False,
        )

    print(f"DUMPED: {path}")


def main():

    target_file = TEST_DIR / TEST_FILE

    if not target_file.exists():
        print("FILE NOT FOUND")
        return

    print("=" * 80)
    print("FILE:", target_file.name)

    text = extract_text(
        str(target_file),
        target_file.suffix.lower(),
    )

    print("TEXT LENGTH:", len(text))

    dump_json(
        "01_raw_text.json",
        {
            "text": text,
        },
    )

    is_contract = is_probably_contract(text)

    print("IS CONTRACT:", is_contract)

    clauses = split_into_clauses(text)

    print("CLAUSES FOUND:", len(clauses))

    dump_json(
        "02_split_clauses.json",
        clauses,
    )

    language = "en"

    if target_file.name.startswith("fr_"):
        language = "fr"

    elif target_file.name.startswith("ar_"):
        language = "ar"

    analysis_result = analyze_contract_clauses(
        clauses,
        language=language,
        max_clauses=25,
    )

    dump_json(
        "03_full_analysis.json",
        analysis_result,
    )

    if isinstance(analysis_result, dict):

        analyzed_clauses = (
            analysis_result.get(
                "clauses",
                analysis_result.get(
                    "results",
                    [],
                ),
            )
        )

        dependency_graph = (
            analysis_result.get(
                "dependency_graph",
                {},
            )
        )

        legal_relation_graph = (
            analysis_result.get(
                "legal_relation_graph",
                {},
            )
        )

        clause_groups = (
            analysis_result.get(
                "clause_groups",
                [],
            )
        )

    else:
        analyzed_clauses = analysis_result
        dependency_graph = {}
        legal_relation_graph = {}
        clause_groups = []

    clause_results = (
        analyzed_clauses.get("results", [])
        if isinstance(analyzed_clauses, dict)
        else analyzed_clauses
    )

    dump_json(
        "04_clause_results.json",
        clause_results,
    )

    dump_json(
        "05_dependency_graph.json",
        dependency_graph,
    )

    dump_json(
        "06_legal_relation_graph.json",
        legal_relation_graph,
    )

    dump_json(
        "07_clause_groups.json",
        clause_groups,
    )

    result = {
        "summary": (
            "Temporary summary used "
            "for local testing."
        ),

        "clauses": clause_results,

        "dependency_graph": dependency_graph,

        "legal_relation_graph": legal_relation_graph,

        "clause_groups": clause_groups,

        "risk_score": 50,

        "simplified_version": (
            "Temporary simplified version "
            "used for local testing."
        ),

        "text_length": len(text),

        "is_probably_contract": is_contract,
    }

    quality = validate_contract_result(result)

    dump_json(
        "08_quality_validation.json",
        quality,
    )

    print("QUALITY SCORE:", quality.get("score"))
    print("VALID:", quality.get("valid"))

    print("\nDONE.")
    print(
        f"\nCHECK FOLDER: {OUTPUT_DIR.absolute()}"
    )


if __name__ == "__main__":
    main()