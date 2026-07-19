from typing import Any


SUPPORTED_LANGUAGES = {"en", "fr", "ar"}


def _safe_int(value: Any) -> int:
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return 0


def _normalize_language(language: str = "en") -> str:
    language = str(language or "en").lower().strip()
    return language if language in SUPPORTED_LANGUAGES else "en"


def _dependency_edges_count(
    executive_summary: dict | None = None,
    dependency_graph: dict | None = None,
) -> int:
    """
    Single source of truth for dependency counts.

    Prefer the final dependency graph when available. Fall back to
    executive_summary["dependency_summary"]["edges_count"] only for
    backward compatibility.
    """

    graph = dependency_graph or {}

    edges = graph.get("edges")

    if isinstance(edges, list):
        return len(edges)

    graph_count = graph.get("edges_count")

    if graph_count is not None:
        return _safe_int(graph_count)

    summary = executive_summary or {}
    dependency_summary = summary.get("dependency_summary", {}) or {}

    return _safe_int(
        dependency_summary.get("edges_count", 0)
    )


def build_executive_risk_narrative(
    executive_summary: dict,
    language: str = "en",
    dependency_graph: dict | None = None,
) -> str:
    """
    Build a generic executive narrative.

    Compatible with all contract families, industries, and jurisdictions.
    Does not assume any specific legal system.
    EN / FR / AR compatible.
    Privacy-first: does not reconstruct or infer personal data.
    Backward compatible with the previous signature.

    Optional dependency_graph:
    - when provided, the narrative uses the final graph count;
    - this keeps the narrative count identical to the UI dependency count.
    """

    executive_summary = executive_summary or {}
    language = _normalize_language(language)

    overview = executive_summary.get("risk_overview", {}) or {}
    top_risks = executive_summary.get("top_risks", []) or []

    high = _safe_int(
        overview.get("high", 0)
    )

    medium = _safe_int(
        overview.get("medium", 0)
    )

    titles = []
    seen = set()

    if not isinstance(top_risks, list):
        top_risks = []

    for item in top_risks:
        if not isinstance(item, dict):
            continue

        title = str(
            item.get("title")
            or item.get("clause_title")
            or item.get("name")
            or ""
        ).strip()

        if not title:
            continue

        dedupe_key = title.casefold()

        if dedupe_key in seen:
            continue

        seen.add(dedupe_key)
        titles.append(title)

        if len(titles) >= 3:
            break

    if language == "fr":
        if high or medium:
            text = (
                f"Ce contrat présente {high} risque(s) élevé(s) "
                f"et {medium} risque(s) moyen(s)."
            )
        else:
            text = (
                "Ce contrat ne présente pas de concentration "
                "évidente de risques élevés ou moyens."
            )

        if titles:
            text += (
                " Les clauses les plus sensibles concernent "
                f"{', '.join(titles)}."
            )

            text += (
                " Ces clauses doivent être examinées attentivement avant signature, "
                "car elles peuvent affecter la responsabilité, la continuité opérationnelle, "
                "l’exposition financière ou la marge de négociation."
            )

        return text

    if language == "ar":
        if high or medium:
            text = (
                f"يتضمن هذا العقد {high} مخاطر عالية "
                f"و{medium} مخاطر متوسطة."
            )
        else:
            text = (
                "لا يظهر هذا العقد تركيزاً واضحاً "
                "لمخاطر عالية أو متوسطة."
            )

        if titles:
            text += (
                " تتركز البنود الأكثر حساسية حول "
                f"{'، '.join(titles)}."
            )

            text += (
                " ويجب مراجعة هذه البنود بعناية قبل التوقيع، "
                "لأنها قد تؤثر على المسؤولية أو استمرارية التشغيل "
                "أو التعرض المالي أو هامش التفاوض."
            )

        return text

    if high or medium:
        text = (
            f"This contract contains {high} high-risk clause(s) "
            f"and {medium} medium-risk clause(s)."
        )
    else:
        text = (
            "This contract does not show a clear concentration "
            "of high or medium risks."
        )

    if titles:
        text += (
            " The most sensitive clauses are "
            f"{', '.join(titles)}."
        )

        text += (
            " These clauses should be reviewed carefully before signing "
            "because they may affect liability, operational continuity, "
            "financial exposure, or negotiation leverage."
        )

    return text
