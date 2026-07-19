import json
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path("regression_results_multilang")
LANGUAGES = ("en", "fr", "ar")
OUTPUT_JSON = ROOT / "_blocked_diagnostic_all_languages.json"

PROTECTED_FIELDS = (
    "legal_insight",
    "market_comparison",
    "safer_alternative",
    "recommendation",
    "negotiation_advice",
    "market_practice",
    "fallback_wording",
    "negotiable",
    "acceptable_compromise",
    "never_accept",
    "negotiation_boundary",
)


def load_summary(language: str) -> list[dict]:
    path = ROOT / language / "_summary.json"

    if not path.exists():
        raise FileNotFoundError(path)

    data = json.loads(path.read_text(encoding="utf-8"))

    if not isinstance(data, list):
        raise TypeError(f"{path}: expected list")

    return data


def main() -> int:
    cases = []

    by_language = Counter()
    by_reason = Counter()
    by_type = Counter()
    by_field = Counter()
    by_language_field = Counter()
    by_language_type = Counter()
    by_type_field = Counter()
    by_language_type_field = Counter()

    for language in LANGUAGES:
        data = load_summary(language)

        for row in data:
            for blocked in row.get("blocked", []):
                field = blocked.get("field") or "UNKNOWN"
                clause_type = blocked.get("clause_type") or "UNKNOWN"
                reasons = blocked.get("reasons") or ["UNKNOWN"]

                case = {
                    "language": language,
                    "file": row.get("file"),
                    "clause_reference": blocked.get("clause_reference"),
                    "clause_title": blocked.get("clause_title"),
                    "clause_type": clause_type,
                    "field": field,
                    "gate_result": blocked.get("gate_result"),
                    "reasons": reasons,
                    "text_before_validation": blocked.get(
                        "text_before_validation"
                    ),
                    "final_text": blocked.get("final_text"),
                }

                cases.append(case)

                by_language[language] += 1
                by_type[clause_type] += 1
                by_field[field] += 1
                by_language_field[(language, field)] += 1
                by_language_type[(language, clause_type)] += 1
                by_type_field[(clause_type, field)] += 1
                by_language_type_field[
                    (language, clause_type, field)
                ] += 1

                for reason in reasons:
                    by_reason[reason] += 1

    payload = {
        "total_blocked": len(cases),
        "protected_fields": list(PROTECTED_FIELDS),
        "by_language": [
            {"language": key, "count": value}
            for key, value in by_language.most_common()
        ],
        "by_reason": [
            {"reason": key, "count": value}
            for key, value in by_reason.most_common()
        ],
        "by_type": [
            {"clause_type": key, "count": value}
            for key, value in by_type.most_common()
        ],
        "by_field": [
            {"field": key, "count": value}
            for key, value in by_field.most_common()
        ],
        "by_language_field": [
            {
                "language": key[0],
                "field": key[1],
                "count": value,
            }
            for key, value in by_language_field.most_common()
        ],
        "by_language_type": [
            {
                "language": key[0],
                "clause_type": key[1],
                "count": value,
            }
            for key, value in by_language_type.most_common()
        ],
        "by_type_field": [
            {
                "clause_type": key[0],
                "field": key[1],
                "count": value,
            }
            for key, value in by_type_field.most_common()
        ],
        "by_language_type_field": [
            {
                "language": key[0],
                "clause_type": key[1],
                "field": key[2],
                "count": value,
            }
            for key, value in by_language_type_field.most_common()
        ],
        "cases": cases,
    }

    OUTPUT_JSON.write_text(
        json.dumps(
            payload,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print("=== GLOBAL BLOCKED DIAGNOSTIC ===")
    print("TOTAL BLOCKED:", len(cases))
    print("OUTPUT:", OUTPUT_JSON)

    print()
    print("=== BY LANGUAGE ===")
    for key, value in by_language.most_common():
        print(f"{key:4} {value}")

    print()
    print("=== BY REASON ===")
    for key, value in by_reason.most_common():
        print(value, key)

    print()
    print("=== BY FIELD ===")
    for key, value in by_field.most_common():
        print(f"{value:3} {key}")

    print()
    print("=== BY CLAUSE TYPE ===")
    for key, value in by_type.most_common():
        print(f"{value:3} {key}")

    print()
    print("=== LANGUAGE / FIELD ===")
    for key, value in by_language_field.most_common():
        print(f"{value:3} {key}")

    print()
    print("=== TYPE / FIELD ===")
    for key, value in by_type_field.most_common():
        print(f"{value:3} {key}")

    print()
    print("=== LANGUAGE / TYPE / FIELD ===")
    for key, value in by_language_type_field.most_common():
        print(f"{value:3} {key}")

    print()
    print("=== FULL CASES ===")

    for case in cases:
        print()
        print("=" * 100)
        print("LANGUAGE:", case["language"].upper())
        print("FILE:", case["file"])
        print("CLAUSE:", case["clause_reference"])
        print("TITLE:", case["clause_title"])
        print("TYPE:", case["clause_type"])
        print("FIELD:", case["field"])
        print("GATE RESULT:", case["gate_result"])
        print("REASONS:", case["reasons"])
        print()
        print("TEXT BEFORE VALIDATION:")
        print(case["text_before_validation"])
        print()
        print("FINAL TEXT:")
        print(case["final_text"])

    if len(cases) != 84:
        print()
        print(
            "WARNING: expected baseline total 84, got",
            len(cases),
        )
        return 1

    print()
    print("DIAGNOSTIC RESULT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
