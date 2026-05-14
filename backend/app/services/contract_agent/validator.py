from typing import Any


REQUIRED_FIELDS = [
    "summary",
    "clauses",
    "risk_score",
    "simplified_version",
]


def validate_contract_result(result: dict) -> dict:
    issues = []
    score = 100

    for field in REQUIRED_FIELDS:
        value = result.get(field)

        if value in [None, "", [], {}]:
            issues.append(f"Missing field: {field}")
            score -= 10

    contract_score = result.get(
        "contract_quality_score"
    )

    if (
        contract_score is not None
        and not isinstance(contract_score, int)
    ):
        issues.append(
            "contract_quality_score must be integer"
        )
        score -= 10

    clauses = result.get("clauses", [])

    if isinstance(clauses, list) and len(clauses) == 0:
        issues.append("No clauses extracted")
        score -= 20

    summary = str(result.get("summary", ""))

    if len(summary) < 40:
        issues.append("Summary too short")
        score -= 10

    score = max(0, min(score, 100))

    return {
        "valid": score >= 70,
        "score": score,
        "issues": issues,
    }

def is_probably_contract(text: str) -> bool:
    text = str(text or "").lower()

    legal_keywords = [
        # English
        "contract",
        "agreement",
        "party",
        "parties",
        "payment",
        "termination",
        "liability",
        "clause",
        "governing law",

        # French
        "contrat",
        "accord",
        "partie",
        "parties",
        "paiement",
        "résiliation",
        "responsabilité",
        "clause",
        "droit applicable",

        # Arabic
        "العقد",
        "عقد",
        "الطرف",
        "الأطراف",
        "المادة",
        "البند",
        "الدفع",
        "السداد",
        "الفسخ",
        "إنهاء",
        "الالتزام",
        "القانون",
    ]

    score = sum(
        1 for keyword in legal_keywords
        if keyword in text
    )

    return score >= 3