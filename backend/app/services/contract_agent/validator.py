from typing import Any


REQUIRED_FIELDS = [
    "contract_type",
    "global_summary",
    "contract_score",
    "overall_balance",
]


def validate_contract_result(result: dict) -> dict:
    issues = []
    score = 100

    for field in REQUIRED_FIELDS:
        value = result.get(field)

        if value in [None, "", [], {}]:
            issues.append(f"Missing field: {field}")
            score -= 10

    contract_score = result.get("contract_score")

    if not isinstance(contract_score, int):
        issues.append("contract_score must be integer")
        score -= 15

    clauses = result.get("clauses", [])

    if isinstance(clauses, list) and len(clauses) == 0:
        issues.append("No clauses extracted")
        score -= 20

    summary = str(result.get("global_summary", ""))

    if len(summary) < 40:
        issues.append("Summary too short")
        score -= 10

    score = max(0, min(score, 100))

    return {
        "valid": score >= 70,
        "score": score,
        "issues": issues,
    }