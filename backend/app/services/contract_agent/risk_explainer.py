from typing import Dict, List


def build_risk_explanation(
    analysis: Dict,
    clause_text: str,
) -> Dict:

    reasons: List[str] = []

    lowered = clause_text.lower()

    if analysis.get("risk_level") in {"medium", "high"}:

        if any(
            k in lowered
            for k in [
                "terminate",
                "termination",
                "résiliation",
                "فسخ",
            ]
        ):
            reasons.append(
                "termination rights may create operational or legal exposure"
            )

        if any(
            k in lowered
            for k in [
                "liability",
                "responsibility",
                "responsabilité",
                "المسؤولية",
            ]
        ):
            reasons.append(
                "liability allocation may limit available remedies"
            )

        if any(
            k in lowered
            for k in [
                "confidentiality",
                "secret",
                "سرية",
                "confidentialité",
            ]
        ):
            reasons.append(
                "confidentiality obligations may survive contract termination"
            )

        if any(
            k in lowered
            for k in [
                "exclusive",
                "exclusif",
                "حصري",
            ]
        ):
            reasons.append(
                "exclusive obligations may restrict commercial flexibility"
            )

    analysis["risk_reasons"] = reasons

    return analysis