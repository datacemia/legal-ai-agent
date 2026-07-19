from typing import Any


SUPPORTED_LANGUAGES = {"en", "fr", "ar"}

RISK_LEVEL_ALIASES = {
    "critical": "high",
    "very_high": "high",
    "very high": "high",
    "high": "high",
    "medium": "medium",
    "moderate": "medium",
    "average": "medium",
    "low": "low",
    "none": "low",
    "informational": "low",
}


def normalize_language(language: str = "en") -> str:
    language = str(language or "en").lower().strip()
    return language if language in SUPPORTED_LANGUAGES else "en"


def normalize_risk_level(level: Any) -> str:
    return RISK_LEVEL_ALIASES.get(
        str(level or "").lower().strip(),
        "low",
    )


def safe_list(value):
    if isinstance(value, list):
        return value
    return []


def safe_dict(value):
    if isinstance(value, dict):
        return value
    return {}


def safe_str(value):
    return str(value or "").strip()


def safe_groups(value):
    if isinstance(value, (dict, list)):
        return value
    return {}


def dependency_edges_count(dependency_graph: dict) -> int:
    graph = safe_dict(dependency_graph)

    edges = graph.get("edges")

    if isinstance(edges, list):
        return len(edges)

    try:
        return int(graph.get("edges_count", 0) or 0)
    except (TypeError, ValueError):
        return 0


def extract_clauses(analysis_result: dict) -> list[dict]:
    clauses_data = safe_dict(analysis_result).get("clauses", [])

    if isinstance(clauses_data, dict):
        return safe_list(clauses_data.get("results", []))

    return safe_list(clauses_data)


def build_risk_distribution(clauses: list[dict]) -> dict:
    counts = {
        "high": 0,
        "medium": 0,
        "low": 0,
    }

    for clause in clauses:
        if not isinstance(clause, dict):
            continue

        level = normalize_risk_level(
            clause.get("risk_level")
        )

        counts[level] += 1

    total = sum(counts.values())

    if total <= 0:
        return {
            "counts": counts,
            "percentages": {
                "high": 0,
                "medium": 0,
                "low": 0,
            },
        }

    return {
        "counts": counts,
        "percentages": {
            key: round((value / total) * 100)
            for key, value in counts.items()
        },
    }


def get_localized_fallback_narrative(
    clauses_count: int,
    language: str = "en",
) -> str:
    language = normalize_language(language)

    if language == "fr":
        return (
            f"{clauses_count} clause(s) ont été analysées. "
            "Le rapport exécutif résume les risques principaux, "
            "les priorités de négociation et les dépendances importantes."
        )

    if language == "ar":
        return (
            f"تم تحليل {clauses_count} بنداً. "
            "يلخص التقرير التنفيذي أهم المخاطر وأولويات التفاوض "
            "والعلاقات المهمة بين البنود."
        )

    return (
        f"{clauses_count} clause(s) were analyzed. "
        "The executive report summarizes key risks, negotiation priorities, "
        "and important cross-clause dependencies."
    )


def build_dependency_insights(
    dependency_graph: dict,
    max_dependencies: int = 10,
) -> dict:
    graph = safe_dict(dependency_graph)
    edges = safe_list(graph.get("edges", []))
    final_edges_count = dependency_edges_count(graph)

    return {
        "edges_count": final_edges_count,
        "key_dependencies": edges[
            :max(0, int(max_dependencies or 10))
        ],
    }


def build_executive_report(
    analysis_result: dict,
    language: str = "en",
) -> dict:
    """
    Build a stable, generic executive contract report.

    International standard:
    - contract-type agnostic
    - jurisdiction-neutral
    - EN / FR / AR compatible
    - privacy-first: does not reconstruct, infer, or expose personal data
    - works across employment, SaaS, services, NDA, finance, lease,
      licensing, procurement, distribution, corporate, construction,
      insurance, banking, and other commercial agreements.
    """

    analysis_result = safe_dict(analysis_result)
    language = normalize_language(language)

    clauses = extract_clauses(analysis_result)

    executive_summary = safe_dict(
        analysis_result.get("executive_summary")
    )

    dependency_graph = safe_dict(
        analysis_result.get("dependency_graph")
    )

    final_dependency_count = dependency_edges_count(
        dependency_graph
    )

    # Keep executive_summary aligned with the final graph count so every
    # downstream consumer reads the same number.
    if executive_summary:
        dependency_summary = safe_dict(
            executive_summary.get("dependency_summary")
        )

        dependency_summary["edges_count"] = final_dependency_count
        executive_summary["dependency_summary"] = dependency_summary

    contradictions = safe_list(
        analysis_result.get("contradictions")
    )[:10]

    clause_groups = safe_groups(
        analysis_result.get(
            "clause_groups",
            analysis_result.get("groups", {}),
        )
    )

    summary = safe_dict(
        analysis_result.get("summary")
    )

    narrative = safe_str(
        analysis_result.get("executive_risk_narrative")
    )

    if not narrative:
        narrative = safe_str(
            executive_summary.get("narrative")
        )

    if not narrative:
        narrative = get_localized_fallback_narrative(
            len(clauses),
            language,
        )

    risk_distribution = build_risk_distribution(
        clauses
    )

    dependency_insights = build_dependency_insights(
        dependency_graph
    )

    return {
        "report_type": "executive_contract_report",
        "language": language,
        "privacy_first": True,

        "contract_overview": {
            "clauses_analyzed": len(clauses),
            "risk_overview": safe_dict(
                executive_summary.get("risk_overview")
            ),
            "risk_distribution": risk_distribution,
            "dependencies_count": final_dependency_count,

            # Optional fields preserved when upstream provides them.
            "risk_score": analysis_result.get(
                "risk_score",
                executive_summary.get("risk_score"),
            ),
            "contract_score": analysis_result.get(
                "contract_score",
                summary.get("contract_score"),
            ),
            "contract_quality": analysis_result.get(
                "contract_quality",
                summary.get("contract_quality"),
            ),
            "contract_complexity": analysis_result.get(
                "contract_complexity",
                summary.get("contract_complexity"),
            ),
            "overall_balance": analysis_result.get(
                "overall_balance",
                summary.get("overall_balance"),
            ),
            "jurisdiction_detected": analysis_result.get(
                "jurisdiction_detected",
                summary.get("jurisdiction_detected"),
            ),
        },

        "executive_narrative": narrative,

        "top_risks": safe_list(
            executive_summary.get("top_risks")
        )[:10],

        "negotiation_priorities": safe_list(
            executive_summary.get("negotiation_priorities")
        )[:10],

        "recommended_actions": safe_list(
            executive_summary.get(
                "recommended_actions",
                summary.get("recommended_actions", []),
            )
        )[:10],

        "contradictions": contradictions,

        "clause_groups": clause_groups,

        "dependency_insights": dependency_insights,

        # Backward-compatible raw references for consumers that already
        # expect these names elsewhere in the pipeline.
        "risk_overview": safe_dict(
            executive_summary.get("risk_overview")
        ),
        "dependency_graph": dependency_graph,
    }
