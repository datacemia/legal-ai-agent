def build_executive_summary(
    clauses: list[dict],
    dependency_graph: dict | None = None,
) -> dict:
    dependency_graph = dependency_graph or {}

    high_risks = [
        c for c in clauses
        if c.get("risk_level") == "high"
    ]

    medium_risks = [
        c for c in clauses
        if c.get("risk_level") == "medium"
    ]

    negotiation_priorities = [
        c for c in clauses
        if c.get("negotiation_advice")
        or c.get("recommendation")
    ]

    top_risks = sorted(
        high_risks + medium_risks,
        key=lambda c: c.get("importance_score", 0),
        reverse=True,
    )[:5]

    return {
        "risk_overview": {
            "high": len(high_risks),
            "medium": len(medium_risks),
            "low": len([
                c for c in clauses
                if c.get("risk_level") == "low"
            ]),
        },
        "top_risks": [
            {
                "title": c.get("clause_title") or c.get("title"),
                "risk_level": c.get("risk_level"),
                "importance_score": c.get("importance_score"),
                "legal_insight": c.get("legal_insight"),
            }
            for c in top_risks
        ],
        "negotiation_priorities": [
            {
                "title": c.get("clause_title") or c.get("title"),
                "risk_level": c.get("risk_level"),
                "recommendation": c.get("recommendation"),
                "negotiation_advice": c.get("negotiation_advice"),
            }
            for c in negotiation_priorities[:5]
        ],
        "dependency_summary": {
            "edges_count": len(
                dependency_graph.get("edges", [])
            ),
            "key_dependencies": dependency_graph.get("edges", [])[:5],
        },
    }