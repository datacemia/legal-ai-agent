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


def main():

    if not TEST_DIR.exists():
        print("ERROR: test_contracts folder not found")
        return

    files = [
        file for file in TEST_DIR.iterdir()
        if file.is_file()
        and file.suffix.lower() in {
            ".pdf",
            ".docx",
        }
    ]

    if not files:
        print(
            "ERROR: No PDF/DOCX files found "
            "in test_contracts"
        )
        return

    for file in files:

        print("\n" + "=" * 80)
        print("FILE:", file.name)

        try:

            text = extract_text(
                str(file),
                file.suffix.lower(),
            )

            is_contract = is_probably_contract(text)
            print("IS CONTRACT:", is_contract)

            clauses = split_into_clauses(text)

            analyzed_clauses = (
                analyze_contract_clauses(
                    clauses,
                    language="en",
                    max_clauses=25,
                )
            )

            result = {
                "summary": (
                    "Temporary summary used "
                    "for local testing."
                ),

                "clauses": analyzed_clauses,

                "risk_score": 50,

                "simplified_version": (
                    "Temporary simplified version "
                    "used for local testing."
                ),

                "text_length": len(text),

                "is_probably_contract": is_contract,
            }

            quality = validate_contract_result(
                result
            )

            print(
                "TEXT LENGTH:",
                len(text),
            )

            print(
                "CLAUSES FOUND:",
                len(clauses),
            )

            print(
                "CLAUSES ANALYZED:",
                len(analyzed_clauses),
            )

            print(
                "QUALITY SCORE:",
                quality.get("score"),
            )

            print(
                "VALID:",
                quality.get("valid"),
            )

            print(
                "ISSUES:",
                quality.get("issues"),
            )

            print("\nCLAUSE SAMPLE:\n")

            for clause in analyzed_clauses[:10]:

                print("-" * 60)

                print(
                    "TITLE:",
                    clause.get("title"),
                )

                print(
                    "RISK:",
                    clause.get("risk_level"),
                )

                print(
                    "HAS DETAILS:",
                    clause.get("has_details"),
                )

                print(
                    "EXPLANATION:",
                    clause.get(
                        "explanation_simple"
                    ),
                )

                print(
                    "RECOMMENDATION:",
                    clause.get(
                        "recommendation"
                    ),
                )

                print(
                    "NEGOTIATION:",
                    clause.get(
                        "negotiation_advice"
                    ),
                )

                print(
                    "LEGAL:",
                    clause.get(
                        "legal_insight"
                    ),
                )

        except Exception as e:

            print(
                "ERROR:",
                str(e),
            )


if __name__ == "__main__":
    main()
