def detect_cross_clause_conflicts(clauses: list[dict]) -> list[dict]:
    conflicts = []

    combined = " ".join(
        f"{c.get('clause_title', '')} {c.get('quoted_text', '')} {c.get('explanation_simple', '')}"
        for c in clauses
    ).lower()

    if (
        ("liability" in combined or "responsabilité" in combined or "المسؤولية" in combined)
        and ("unlimited" in combined or "illimitée" in combined or "غير محدودة" in combined)
        and ("cap" in combined or "plafond" in combined or "حد" in combined)
    ):
        conflicts.append({
            "type": "liability_conflict",
            "severity": "high",
            "message": "The contract appears to contain both capped and uncapped liability language.",
        })

    if (
        ("termination" in combined or "résiliation" in combined or "فسخ" in combined or "إنهاء" in combined)
        and ("without notice" in combined or "sans préavis" in combined or "دون إشعار" in combined)
        and ("notice period" in combined or "préavis" in combined or "إشعار" in combined)
    ):
        conflicts.append({
            "type": "termination_notice_conflict",
            "severity": "medium",
            "message": "The contract may contain inconsistent termination notice language.",
        })

    if (
        ("governing law" in combined or "droit applicable" in combined or "القانون الواجب التطبيق" in combined)
        and sum(x in combined for x in ["france", "morocco", "uae", "new york", "england", "maroc", "الإمارات"]) >= 2
    ):
        conflicts.append({
            "type": "governing_law_conflict",
            "severity": "high",
            "message": "The contract may reference multiple governing laws or jurisdictions.",
        })

    if (
        ("payment" in combined or "paiement" in combined or "الدفع" in combined or "السداد" in combined)
        and ("15 days" in combined or "15 jours" in combined or "15 يوم" in combined)
        and ("30 days" in combined or "30 jours" in combined or "30 يوم" in combined)
    ):
        conflicts.append({
            "type": "payment_deadline_conflict",
            "severity": "medium",
            "message": "The contract may contain inconsistent payment deadlines.",
        })

    return conflicts