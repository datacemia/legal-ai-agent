def detect_contract_contradictions(
    clauses: list[dict],
) -> list[dict]:

    contradictions = []

    text_blob = " ".join(
        str(c.get("quoted_text") or c.get("clause_text") or "")
        for c in clauses
    ).lower()

    checks = [
        {
            "id": "liability_cap_vs_unlimited_liability",
            "a": ["liability cap", "limitation of liability", "plafond de responsabilité", "حد المسؤولية"],
            "b": ["unlimited liability", "responsabilité illimitée", "مسؤولية غير محدودة"],
            "severity": "high",
            "message": "Liability appears both capped and unlimited in different clauses.",
        },
        {
            "id": "fixed_term_vs_termination_anytime",
            "a": ["fixed term", "durée déterminée", "مدة محددة"],
            "b": ["terminate at any time", "résilier à tout moment", "إنهاء في أي وقت"],
            "severity": "medium",
            "message": "A fixed term may conflict with a right to terminate at any time.",
        },
        {
            "id": "confidentiality_fixed_vs_perpetual",
            "a": ["two years", "three years", "deux ans", "trois ans", "سنتين", "ثلاث سنوات"],
            "b": ["perpetual confidentiality", "confidentiality indefinitely", "confidentialité perpétuelle", "سرية دائمة"],
            "severity": "medium",
            "message": "Confidentiality duration appears both fixed and perpetual.",
        },
        {
            "id": "exclusive_vs_non_exclusive",
            "a": ["exclusive", "exclusif", "حصري"],
            "b": ["non-exclusive", "non exclusive", "non exclusif", "غير حصري"],
            "severity": "high",
            "message": "The contract may contain both exclusive and non-exclusive appointment language.",
        },
        {
            "id": "court_vs_arbitration_only",
            "a": ["exclusive jurisdiction", "courts of", "tribunaux", "محكمة"],
            "b": ["arbitration only", "binding arbitration", "arbitrage obligatoire", "تحكيم إلزامي"],
            "severity": "medium",
            "message": "Court jurisdiction language may conflict with arbitration-only language.",
        },
    ]

    for check in checks:
        has_a = any(term in text_blob for term in check["a"])
        has_b = any(term in text_blob for term in check["b"])

        if has_a and has_b:
            contradictions.append({
                "id": check["id"],
                "severity": check["severity"],
                "message": check["message"],
            })

    return contradictions