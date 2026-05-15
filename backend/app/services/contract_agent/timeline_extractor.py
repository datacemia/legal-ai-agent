import re


def extract_contract_timeline(
    clauses: list[dict],
    language: str = "en",
) -> list[dict]:

    timeline = []

    for clause in clauses:
        source_clause = clause.get("clause_title", "")

        text = " ".join([
            str(clause.get("clause_title", "")),
            str(clause.get("quoted_text", "")),
            str(clause.get("explanation_simple", "")),
            str(clause.get("legal_insight", "")),
        ])

        patterns = [
            r"\b\d+\s+days?\b",
            r"\b\d+\s+months?\b",
            r"\b\d+\s+years?\b",
            r"\b\d+\s+jours?\b",
            r"\b\d+\s+mois\b",
            r"\b\d+\s+ans?\b",
            r"\d+\s*يوم",
            r"\d+\s*أيام",
            r"\d+\s*شهر",
            r"\d+\s*سنة",
        ]

        matches = []

        for pattern in patterns:
            matches.extend(
                re.findall(
                    pattern,
                    text,
                    flags=re.IGNORECASE,
                )
            )

        for match in matches:
            normalized_text = text.lower()

            event = "general"

            if any(k in normalized_text for k in [
                "payment", "invoice", "rent",
                "paiement", "loyer",
                "الدفع", "السداد", "الكراء",
            ]):
                event = "payment"

            elif any(k in normalized_text for k in [
                "termination", "terminate", "notice",
                "résiliation", "préavis",
                "فسخ", "إنهاء", "إشعار",
            ]):
                event = "termination"

            elif any(k in normalized_text for k in [
                "confidentiality", "confidential",
                "confidentialité",
                "السرية", "سرية",
            ]):
                event = "confidentiality"

            timeline.append({
                "event": event,
                "time_period": match,
                "source_clause": source_clause,
                "confidence": "medium",
            })

    return timeline