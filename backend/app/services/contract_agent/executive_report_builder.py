def build_executive_report(
    analysis_result: dict,
    language: str = "en",
) -> dict:

    clauses_data = analysis_result.get(
        "clauses",
        [],
    )

    if isinstance(
        clauses_data,
        dict,
    ):
        clauses = clauses_data.get(
            "results",
            [],
        )
    else:
        clauses = clauses_data

    executive_summary = analysis_result.get(
        "executive_summary",
        {},
    )

    dependency_graph = analysis_result.get(
        "dependency_graph",
        {},
    )

    contradictions = analysis_result.get(
        "contradictions",
        [],
    )

    narrative = analysis_result.get(
        "executive_risk_narrative",
        "",
    )

    return {
        "report_type": "executive_contract_report",
        "language": language,
        "contract_overview": {
            "clauses_analyzed": len(clauses),
            "risk_overview": executive_summary.get("risk_overview", {}),
        },
        "executive_narrative": narrative,
        "top_risks": executive_summary.get("top_risks", []),
        "negotiation_priorities": executive_summary.get(
            "negotiation_priorities",
            [],
        ),
        "contradictions": contradictions,
        "dependency_insights": {
            "edges_count": len(dependency_graph.get("edges", [])),
            "key_dependencies": dependency_graph.get("edges", [])[:10],
        },
    }
