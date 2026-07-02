import json
from typing import Any

from sqlalchemy.orm import Session

from app.models.business_analysis import BusinessAnalysis


def _safe_float(value: Any) -> float:
    if value is None:
        return 0.0

    if isinstance(value, bool):
        return 0.0

    if isinstance(value, (int, float)):
        return float(value)

    try:
        return float(str(value).replace(",", "").strip())
    except Exception:
        return 0.0


def _safe_percent_change(previous: float, current: float) -> float:
    if previous == 0:
        return 0.0

    return ((current - previous) / previous) * 100


def _extract_kpis(result: dict[str, Any]) -> dict[str, float]:
    kpis = result.get("kpis") or {}

    return {
        "revenue": _safe_float(kpis.get("revenue")),
        "expenses": _safe_float(kpis.get("expenses")),
        "profit": _safe_float(kpis.get("profit")),
        "profit_margin_percent": _safe_float(
            kpis.get("profit_margin_percent")
        ),
        "growth_rate_percent": _safe_float(
            kpis.get("growth_rate_percent")
        ),
    }


def get_latest_business_analysis(
    db: Session,
    user_id: int,
) -> BusinessAnalysis | None:
    """
    Return the latest stored business analysis for a user.
    """

    return (
        db.query(BusinessAnalysis)
        .filter(BusinessAnalysis.user_id == user_id)
        .order_by(BusinessAnalysis.id.desc())
        .first()
    )


def get_previous_business_result(
    db: Session,
    user_id: int,
) -> dict[str, Any] | None:
    """
    Return the parsed JSON result of the latest business analysis.
    """

    latest = get_latest_business_analysis(
        db=db,
        user_id=user_id,
    )

    if not latest:
        return None

    try:
        return json.loads(latest.result)
    except Exception:
        return None


def compare_business_results(
    previous_result: dict[str, Any] | None,
    current_result: dict[str, Any],
) -> dict[str, Any]:
    """
    Compare previous and current business analysis results.

    This does not call AI.
    It creates deterministic memory/evolution signals.
    """

    if not previous_result:
        return {
            "available": False,
            "summary": "First available analysis. No historical comparison yet.",
            "changes": {},
            "signals": [
                "First available analysis. No historical comparison yet."
            ],
        }

    previous_kpis = _extract_kpis(previous_result)
    current_kpis = _extract_kpis(current_result)

    changes = {}

    for key in [
        "revenue",
        "expenses",
        "profit",
        "profit_margin_percent",
        "growth_rate_percent",
    ]:
        previous_value = previous_kpis.get(key, 0)
        current_value = current_kpis.get(key, 0)

        changes[key] = {
            "previous": round(previous_value, 2),
            "current": round(current_value, 2),
            "absolute_change": round(
                current_value - previous_value,
                2,
            ),
            "percent_change": round(
                _safe_percent_change(
                    previous=previous_value,
                    current=current_value,
                ),
                2,
            ),
        }

    signals = []

    revenue_change = changes["revenue"]["percent_change"]
    expense_change = changes["expenses"]["percent_change"]
    profit_change = changes["profit"]["percent_change"]

    if revenue_change > 10:
        signals.append(
            "Revenue increased significantly compared with the previous analysis."
        )
    elif revenue_change < -10:
        signals.append(
            "Revenue decreased significantly compared with the previous analysis."
        )

    if expense_change > 10:
        signals.append(
            "Expenses increased significantly compared with the previous analysis."
        )
    elif expense_change < -10:
        signals.append(
            "Expenses decreased compared with the previous analysis."
        )

    if profit_change > 10:
        signals.append(
            "Profit improved compared with the previous analysis."
        )
    elif profit_change < -10:
        signals.append(
            "Profit weakened compared with the previous analysis."
        )

    previous_score = _safe_float(
        previous_result.get("business_health_score")
    )

    current_score = _safe_float(
        current_result.get("business_health_score")
    )

    score_change = current_score - previous_score

    if score_change >= 10:
        signals.append(
            "Business health score improved meaningfully."
        )
    elif score_change <= -10:
        signals.append(
            "Business health score declined meaningfully."
        )

    if not signals:
        signals.append(
            "No major business change detected compared with the previous analysis."
        )

    summary = " ".join(signals)

    return {
        "available": True,
        "summary": summary,
        "previous_business_model": previous_result.get(
            "business_model",
            "general",
        ),
        "current_business_model": current_result.get(
            "business_model",
            "general",
        ),
        "previous_business_health_score": previous_score,
        "current_business_health_score": current_score,
        "business_health_score_change": round(score_change, 2),
        "changes": changes,
        "signals": signals,
    }


def build_memory_context_for_ai(
    memory_comparison: dict[str, Any],
) -> str:
    """
    Convert memory comparison into a compact text context
    that can be injected into future prompts if needed.
    """

    if not memory_comparison.get("available"):
        return "First available analysis. No historical comparison yet."

    lines = [
        "Business memory comparison:",
        memory_comparison.get("summary", ""),
        "",
        "KPI changes:",
    ]

    changes = memory_comparison.get("changes", {})

    for key, value in changes.items():
        lines.append(
            f"- {key}: previous={value.get('previous')}, "
            f"current={value.get('current')}, "
            f"change={value.get('absolute_change')}, "
            f"percent_change={value.get('percent_change')}%"
        )

    return "\n".join(lines)


def attach_business_memory(
    db: Session,
    user_id: int,
    current_result: dict[str, Any],
) -> dict[str, Any]:
    """
    Add memory comparison to the current result.

    Important:
    Call this BEFORE saving the current result.
    """

    previous_result = get_previous_business_result(
        db=db,
        user_id=user_id,
    )

    memory = compare_business_results(
        previous_result=previous_result,
        current_result=current_result,
    )

    current_result["business_memory"] = memory

    return current_result
