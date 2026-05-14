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

    speculative_terms = [
        "may",
        "could",
        "possibility",
        "potential",
        "limited recourse",
        "may have limited recourse",

        "peut",
        "pourrait",
        "potentiel",

        "قد",
        "يمكن",
    ]

    weak_detail_count = 0

    if isinstance(clauses, list):
        for clause in clauses:
            combined = " ".join([
                str(clause.get("explanation_simple", "")),
                str(clause.get("recommendation", "")),
                str(clause.get("negotiation_advice", "")),
                str(clause.get("legal_insight", "")),
                str(clause.get("market_comparison", "")),
                str(clause.get("safer_alternative", "")),
            ]).lower()

            if any(
                term in combined
                for term in speculative_terms
            ):
                weak_detail_count += 1

    if weak_detail_count:
        issues.append(
            f"Speculative clause analysis: "
            f"{weak_detail_count}"
        )
        score -= min(
            25,
            weak_detail_count * 10
        )

    summary = str(result.get("summary", ""))

    if len(summary) < 40:
        issues.append("Summary too short")
        score -= 10

    text_length = result.get("text_length", 0)

    if text_length < 150:
        issues.append("Very little text extracted")
        score -= 30

    if result.get("is_probably_contract") is False:
        issues.append("Document does not look like a contract")
        score -= 40

    weak_detail_count = 0

    if isinstance(clauses, list):
        for clause in clauses:
            has_details = clause.get("has_details")
            explanation = str(
                clause.get(
                    "explanation_simple",
                    ""
                )
            ).lower()

            if has_details and not any([
                clause.get("recommendation"),
                clause.get("negotiation_advice"),
                clause.get("legal_insight"),
                clause.get("market_comparison"),
                clause.get("safer_alternative"),
            ]):
                weak_detail_count += 1

            if "may" in explanation or "could" in explanation:
                weak_detail_count += 1

    if weak_detail_count:
        issues.append(
            f"Weak clause details: {weak_detail_count}"
        )
        score -= min(20, weak_detail_count * 5)

    score = max(0, min(score, 100))

    return {
        "valid": score >= 75,
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

        # Additional Arabic legal/business terms
        "تم إبرام",
        "يلتزم",
        "يجوز",
        "إشعار",
        "الفاتورة",
        "المبالغ",
        "مسؤولية",
        "الأطراف",
        "معلومات سرية",
    ]

    score = sum(
        1 for keyword in legal_keywords
        if keyword in text
    )

    return score >= 2
