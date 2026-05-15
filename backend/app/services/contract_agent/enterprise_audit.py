def generate_enterprise_audit(
    clauses: list[dict],
    obligations: list[dict] | None = None,
    timeline: list[dict] | None = None,
    conflicts: list[dict] | None = None,
    jurisdiction: dict | None = None,
) -> dict:

    obligations = obligations or []
    timeline = timeline or []
    conflicts = conflicts or []
    jurisdiction = jurisdiction or {}

    high_risk_clauses = [
        c for c in clauses
        if c.get("risk_level") == "high"
    ]

    medium_risk_clauses = [
        c for c in clauses
        if c.get("risk_level") == "medium"
    ]

    negotiation_points = [
        {
            "clause": c.get("clause_title", ""),
            "advice": c.get("negotiation_advice", ""),
        }
        for c in clauses
        if c.get("negotiation_advice")
    ]

    critical_obligations = [
        o for o in obligations
        if o.get("type") in {
            "payment",
            "termination",
            "confidentiality",
            "data_protection",
        }
    ]

    critical_timeline = [
        t for t in timeline
        if t.get("event") in {
            "payment",
            "termination",
            "confidentiality",
        }
    ]

    return {
        "risk_overview": {
            "high_risk_count": len(high_risk_clauses),
            "medium_risk_count": len(medium_risk_clauses),
            "conflict_count": len(conflicts),
        },
        "top_risks": [
            {
                "title": c.get("clause_title", ""),
                "risk_level": c.get("risk_level", ""),
                "legal_insight": c.get("legal_insight", ""),
            }
            for c in high_risk_clauses + medium_risk_clauses
        ][:10],
        "critical_obligations": critical_obligations[:10],
        "important_deadlines": critical_timeline[:10],
        "negotiation_priorities": negotiation_points[:10],
        "conflicts": conflicts,
        "jurisdiction": jurisdiction,
    }