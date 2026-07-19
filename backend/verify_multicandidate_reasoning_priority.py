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
        "required_producers": {
            "recommendation": "warranty",
            "market_comparison": "warranty",
        },
        "forbidden_producers": {
            "legal_insight": "confidentiality",
            "recommendation": "confidentiality",
            "negotiation": "loan",
        },
        "forbidden_detected_types": (
            "loan",
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
        "required_producers": {
            "legal_insight": "non_compete",
            "recommendation": "non_compete",
            "negotiation": "non_compete",
        },
    },
    {
        "name": "Arabic loan financial covenant",
        "language": "ar",
        "clause_type": "loan",
        "text": (
            "يلتزم المقترض بالحفاظ على نسبة تغطية خدمة الدين المحددة في الاتفاقية."
        ),
        "required_producers": {
            "legal_insight": "loan",
            "recommendation": "loan",
            "negotiation": "loan",
            "market_comparison": "loan",
        },
        "forbidden_producers": {
            "legal_insight": "insurance",
            "recommendation": "insurance",
            "negotiation": "insurance",
        },
    },
    {
        "name": "French warranty",
        "language": "fr",
        "clause_type": "warranty",
        "text": (
            "Le Fournisseur garantit que les Biens seront exempts de défauts "
            "et conformes aux Spécifications pendant vingt-quatre mois."
        ),
        "required_producers": {
            "legal_insight": "warranty",
            "recommendation": "warranty",
            "negotiation": "warranty",
            "market_comparison": "warranty",
        },
        "forbidden_producers": {
            "legal_insight": "supply_distribution",
            "recommendation": "supply_distribution",
        },
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
        "safer_required": (
            "parts égales et indivises",
            "sans avoir à rendre de comptes",
            "droit de première négociation",
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
        producers = (
            result.get("selected_reasoning_producers")
            or {}
        )

        print()
        print("=" * 100)
        print("CASE:", case["name"])
        print("SOURCE TYPE:", source_type)
        print(
            "DETECTED TYPES:",
            result.get("source_reasoning_detected_types"),
        )
        print(
            "CANDIDATES:",
            result.get("source_reasoning_candidate_types"),
        )
        print("SELECTED PRODUCERS:", producers)

        for field, expected in (
            case.get("required_producers")
            or {}
        ).items():
            actual = producers.get(field)
            print(
                "ASSERT PRODUCER:",
                field,
                "expected=",
                expected,
                "actual=",
                actual,
            )
            if actual != expected:
                failed = True
                print("ERROR: required producer mismatch")

        for field, forbidden in (
            case.get("forbidden_producers")
            or {}
        ).items():
            actual = producers.get(field)
            if actual == forbidden:
                failed = True
                print(
                    "ERROR: forbidden producer selected:",
                    field,
                    forbidden,
                )

        detected_types = (
            result.get("source_reasoning_detected_types")
            or []
        )

        for forbidden_type in case.get(
            "forbidden_detected_types",
            (),
        ):
            if forbidden_type in detected_types:
                failed = True
                print(
                    "ERROR: context-only type survived producer filtering:",
                    forbidden_type,
                )

        safer = str(
            result.get("safer_alternative")
            or ""
        )

        for marker in case.get("safer_required", ()):
            if marker not in safer:
                failed = True
                print(
                    "ERROR: safer_alternative missing:",
                    marker,
                )

    print()
    print(
        "VERIFY RESULT:",
        "FAIL" if failed else "PASS",
    )

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
