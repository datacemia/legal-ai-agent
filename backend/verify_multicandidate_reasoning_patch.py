from __future__ import annotations

from app.services.contract_agent.contract_taxonomy import (
    detect_clause_type_from_taxonomy,
)
from app.services.contract_agent.legal_reasoning_templates import (
    get_reasoning_for_text,
)


CASES = [
    {
        "name": "NDA ownership/license/warranty multi-signal",
        "language": "en",
        "clause_type": "confidentiality",
        "text": (
            'Nothing in this Agreement grants any license or ownership interest '
            'in the Confidential Information. All Confidential Information is '
            'provided "as is" without warranty of any kind.'
        ),
    },
    {
        "name": "Employment non-solicitation multi-signal",
        "language": "en",
        "clause_type": "non_compete",
        "text": (
            "During employment and for twenty-four (24) months thereafter, "
            "Executive shall not solicit for employment any employee of the Company."
        ),
    },
    {
        "name": "Arabic loan financial covenant",
        "language": "ar",
        "clause_type": "loan",
        "text": (
            "يلتزم المقترض بالحفاظ على نسبة تغطية خدمة الدين المحددة في الاتفاقية."
        ),
    },
    {
        "name": "French warranty",
        "language": "fr",
        "clause_type": "warranty",
        "text": (
            "Le Fournisseur garantit que les Biens seront exempts de défauts "
            "et conformes aux Spécifications pendant vingt-quatre mois."
        ),
    },
    {
        "name": "Joint IP first-negotiation safer alternative",
        "language": "fr",
        "clause_type": "intellectual_property",
        "text": (
            "Chaque Partie conserve la propriété de sa propriété intellectuelle "
            "préexistante. La PI Conjointe sera détenue conjointement par les "
            "Parties en parts égales et indivises, chaque Partie étant en droit "
            "de l'exploiter sans avoir à rendre de comptes à l'autre, sous réserve "
            "d'un droit de première négociation avant toute concession de licence "
            "de PI Conjointe à un concurrent direct de l'autre Partie."
        ),
    },
]


def main() -> int:
    failed = False

    for case in CASES:
        result = get_reasoning_for_text(
            case["text"],
            case["language"],
            clause_type=case["clause_type"],
        )

        source_type = detect_clause_type_from_taxonomy(
            case["text"]
        )

        print()
        print("=" * 100)
        print("CASE:", case["name"])
        print("SOURCE TYPE:", source_type)
        print(
            "CANDIDATES:",
            result.get("source_reasoning_candidate_types"),
        )
        print(
            "SELECTED PRODUCERS:",
            result.get("selected_reasoning_producers"),
        )

        for field in (
            "legal_insight",
            "recommendation",
            "negotiation",
            "market_comparison",
        ):
            text = str(result.get(field) or "")
            generated_type = detect_clause_type_from_taxonomy(
                text
            )
            print(
                field,
                "-> generated_type=",
                generated_type,
            )
            print(text)

        safer = str(
            result.get("safer_alternative")
            or ""
        )

        print("safer_alternative:")
        print(safer)

        if case["name"].startswith("Joint IP"):
            required = (
                "parts égales et indivises",
                "sans avoir à rendre de comptes",
                "droit de première négociation",
            )

            for marker in required:
                if marker not in safer:
                    print(
                        "ERROR: safer_alternative missing:",
                        marker,
                    )
                    failed = True

    print()
    print(
        "VERIFY RESULT:",
        "FAIL" if failed else "PASS",
    )

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
