def build_executive_risk_narrative(
    executive_summary: dict,
    language: str = "en",
) -> str:
    overview = executive_summary.get("risk_overview", {})
    top_risks = executive_summary.get("top_risks", [])
    dependencies = executive_summary.get("dependency_summary", {})

    high = overview.get("high", 0)
    medium = overview.get("medium", 0)
    edges = dependencies.get("edges_count", 0)

    if language == "fr":
        return (
            f"Ce contrat présente {high} risque(s) élevé(s) "
            f"et {medium} risque(s) moyen(s). "
            f"Les clauses les plus sensibles concernent "
            f"{', '.join([r.get('title', 'clause') for r in top_risks[:3]])}. "
            f"L’analyse croisée identifie {edges} relation(s) importantes entre clauses."
        )

    if language == "ar":
        return (
            f"يتضمن هذا العقد {high} مخاطر عالية "
            f"و {medium} مخاطر متوسطة. "
            f"تركز أهم البنود الحساسة على "
            f"{'، '.join([r.get('title', 'بند') for r in top_risks[:3]])}. "
            f"يكشف التحليل المتقاطع عن {edges} علاقة مهمة بين البنود."
        )

    return (
        f"This contract contains {high} high-risk clause(s) "
        f"and {medium} medium-risk clause(s). "
        f"The most sensitive clauses are "
        f"{', '.join([r.get('title', 'clause') for r in top_risks[:3]])}. "
        f"Cross-clause analysis identified {edges} important clause relationship(s)."
    )