import json
import os
from datetime import datetime
from typing import Any

from openai import OpenAI
from sqlalchemy.orm import Session

from app.models.business_analysis import BusinessAnalysis


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_language_name(output_language: str) -> str:
    languages = {
        "en": "English",
        "fr": "French",
        "ar": "Arabic",
    }

    return languages.get(output_language, "English")


def _safe_json_loads(value: str | None) -> dict[str, Any]:
    if not value:
        return {}

    try:
        parsed = json.loads(value)
        return parsed if isinstance(parsed, dict) else {}
    except Exception:
        return {}


def get_latest_business_result(
    db: Session,
    user_id: int,
) -> dict[str, Any] | None:
    """
    Return the latest saved business analysis result for a user.
    """

    latest_analysis = (
        db.query(BusinessAnalysis)
        .filter(BusinessAnalysis.user_id == user_id)
        .order_by(BusinessAnalysis.id.desc())
        .first()
    )

    if not latest_analysis:
        return None

    result = _safe_json_loads(latest_analysis.result)

    if not result:
        return None

    result["_source_analysis_id"] = latest_analysis.id
    result["_source_file_name"] = latest_analysis.file_name
    result["_source_created_at"] = (
        latest_analysis.created_at.isoformat()
        if latest_analysis.created_at
        else None
    )

    return result


def build_weekly_report_prompt(
    latest_result: dict[str, Any],
    output_language: str = "en",
) -> str:
    language_name = get_language_name(output_language)

    compact_context = {
        "business_model": latest_result.get("business_model", "general"),
        "business_health_score": latest_result.get(
            "business_health_score",
        ),
        "kpis": latest_result.get("kpis", {}),
        "forecast": latest_result.get("forecast", {}),
        "business_memory": latest_result.get("business_memory", {}),
        "smart_insights": latest_result.get("smart_insights", {}),
        "risks": latest_result.get("risks", []),
        "opportunities": latest_result.get("opportunities", []),
        "recommendations": latest_result.get("recommendations", []),
        "file_metadata": latest_result.get("file_metadata", {}),
        "source_file_name": latest_result.get("_source_file_name"),
        "source_created_at": latest_result.get("_source_created_at"),
    }

    return f"""
Create an AI CEO Weekly Report from the latest business analysis.

LANGUAGE RULES:
- Return the entire JSON content in {language_name}.
- Keep all JSON keys exactly in English.
- Do not translate JSON keys.
- Translate all user-facing explanations into {language_name}.
- Keep numbers, dates, currencies, company names, product names, and file names unchanged when appropriate.
- Mixed-language explanatory output is forbidden.
- Do not write anything outside JSON.

FACTUALITY RULES:
- Use only the provided business analysis context.
- Do not invent revenue, expenses, profit, forecasts, risks, or opportunities.
- If something is unavailable, say it is not available.
- Be practical and concise.
- Avoid generic business advice.
- Recommendations must be tied to provided KPIs, risks, forecast, memory, or insights.
- Do not claim week-over-week performance unless business_memory supports comparison.
- This is decision-support only, not financial advice.

CEO REPORT STYLE:
- Write like a concise CEO/CFO executive brief.
- Prioritize what the business owner should focus on this week.
- Focus on money, cashflow, growth, risk, and operational decisions.
- Rank the most important actions first.
- Avoid long paragraphs.

Return EXACT JSON:

{{
  "title": "AI CEO Weekly Report",
  "generated_at": "{datetime.utcnow().isoformat()}Z",
  "business_model": "general",
  "source_file_name": "",
  "executive_brief": "short executive CEO-style brief",
  "weekly_summary": "summary of the latest business situation",
  "business_health_score": null,
  "kpi_snapshot": {{
    "revenue": 0,
    "expenses": 0,
    "profit": 0,
    "profit_margin_percent": 0,
    "growth_rate_percent": 0,
    "cashflow_status": "unknown"
  }},
  "forecast_snapshot": {{
    "available": false,
    "next_month_revenue": 0,
    "next_quarter_revenue": 0,
    "trend": "unknown",
    "cashflow_risk": "unknown",
    "volatility": "unknown"
  }},
  "memory_summary": "business memory summary or not available",
  "top_risks": [
    {{
      "title": "risk title",
      "severity": "medium",
      "why_it_matters": "practical explanation",
      "recommended_action": "specific action"
    }}
  ],
  "top_opportunities": [
    {{
      "title": "opportunity title",
      "impact": "medium",
      "why_it_matters": "practical explanation",
      "recommended_action": "specific action"
    }}
  ],
  "priority_actions": [
    {{
      "title": "action title",
      "priority": "high",
      "expected_impact": "expected impact",
      "owner_focus": "what the owner should do this week"
    }}
  ],
  "ceo_decision": {{
    "decision": "single most important decision",
    "why": "why this matters now",
    "timeframe": "this week"
  }},
  "data_limitations": ["limitation1"],
  "disclaimer": "This report is for business decision support only. Verify important decisions with a qualified professional."
}}

Latest business analysis context:
{json.dumps(compact_context, ensure_ascii=False)[:14000]}
"""


def generate_weekly_report_from_result(
    latest_result: dict[str, Any],
    output_language: str = "en",
) -> dict[str, Any]:
    """
    Generate a CEO weekly report from a saved business analysis result.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": (
                    "You are Runexa AI CEO Reporting Engine. "
                    "Return only valid JSON. Do not use markdown."
                ),
            },
            {
                "role": "user",
                "content": build_weekly_report_prompt(
                    latest_result=latest_result,
                    output_language=output_language,
                ),
            },
        ],
        temperature=0.2,
    )

    content = response.choices[0].message.content or "{}"

    try:
        report = json.loads(content)

        if not isinstance(report, dict):
            raise ValueError("Report is not a JSON object.")

        return report

    except Exception:
        return build_fallback_weekly_report(
            latest_result=latest_result,
            output_language=output_language,
            error="Invalid AI weekly report JSON output.",
        )


def build_fallback_weekly_report(
    latest_result: dict[str, Any],
    output_language: str = "en",
    error: str | None = None,
) -> dict[str, Any]:
    """
    Deterministic fallback report when AI output fails.
    """

    kpis = latest_result.get("kpis", {}) or {}
    forecast = latest_result.get("forecast", {}) or {}
    memory = latest_result.get("business_memory", {}) or {}
    smart_insights = latest_result.get("smart_insights", {}) or {}
    decision = smart_insights.get("most_important_decision", {}) or {}

    if output_language == "fr":
        executive_brief = (
            "Rapport généré à partir de la dernière analyse disponible."
        )
        weekly_summary = (
            "Les données disponibles ont été résumées sans génération avancée."
        )
        memory_summary = memory.get(
            "summary",
            "Aucune mémoire business précédente disponible.",
        )
        disclaimer = (
            "Ce rapport sert uniquement d’aide à la décision business. "
            "Vérifiez les décisions importantes avec un professionnel qualifié."
        )
    elif output_language == "ar":
        executive_brief = "تم إنشاء التقرير من آخر تحليل أعمال متاح."
        weekly_summary = "تم تلخيص البيانات المتاحة بدون توليد متقدم."
        memory_summary = memory.get(
            "summary",
            "لا توجد ذاكرة أعمال سابقة متاحة.",
        )
        disclaimer = (
            "هذا التقرير مخصص لدعم قرارات الأعمال فقط. "
            "تحقق من القرارات المهمة مع مختص مؤهل."
        )
    else:
        executive_brief = (
            "Report generated from the latest available business analysis."
        )
        weekly_summary = (
            "Available business data was summarized without advanced generation."
        )
        memory_summary = memory.get(
            "summary",
            "No previous business memory available.",
        )
        disclaimer = (
            "This report is for business decision support only. "
            "Verify important decisions with a qualified professional."
        )

    limitations = []

    if error:
        limitations.append(error)

    if not forecast.get("available"):
        limitations.append("Forecast data is unavailable or limited.")

    return {
        "title": "AI CEO Weekly Report",
        "generated_at": f"{datetime.utcnow().isoformat()}Z",
        "business_model": latest_result.get("business_model", "general"),
        "source_file_name": latest_result.get("_source_file_name", ""),
        "executive_brief": executive_brief,
        "weekly_summary": weekly_summary,
        "business_health_score": latest_result.get(
            "business_health_score",
        ),
        "kpi_snapshot": {
            "revenue": kpis.get("revenue", 0),
            "expenses": kpis.get("expenses", 0),
            "profit": kpis.get("profit", 0),
            "profit_margin_percent": kpis.get(
                "profit_margin_percent",
                0,
            ),
            "growth_rate_percent": kpis.get(
                "growth_rate_percent",
                0,
            ),
            "cashflow_status": kpis.get(
                "cashflow_status",
                "unknown",
            ),
        },
        "forecast_snapshot": {
            "available": forecast.get("available", False),
            "next_month_revenue": forecast.get(
                "next_month_revenue",
                0,
            ),
            "next_quarter_revenue": forecast.get(
                "next_quarter_revenue",
                0,
            ),
            "trend": forecast.get("trend", "unknown"),
            "cashflow_risk": forecast.get(
                "cashflow_risk",
                "unknown",
            ),
            "volatility": forecast.get("volatility", "unknown"),
        },
        "memory_summary": memory_summary,
        "top_risks": latest_result.get("risks", [])[:3],
        "top_opportunities": latest_result.get("opportunities", [])[:3],
        "priority_actions": latest_result.get("recommendations", [])[:3],
        "ceo_decision": {
            "decision": decision.get(
                "decision",
                "No specific CEO decision available.",
            ),
            "why": decision.get(
                "why",
                "No decision rationale available.",
            ),
            "timeframe": decision.get("timeframe", "this week"),
        },
        "data_limitations": limitations,
        "disclaimer": disclaimer,
    }


def generate_weekly_report_for_user(
    db: Session,
    user_id: int,
    output_language: str = "en",
) -> dict[str, Any]:
    """
    Main public service function.

    Use this from a route:
    report = generate_weekly_report_for_user(db, current_user.id, output_language)
    """

    latest_result = get_latest_business_result(
        db=db,
        user_id=user_id,
    )

    if not latest_result:
        return {
            "error": "No business analysis found.",
            "title": "AI CEO Weekly Report",
            "generated_at": f"{datetime.utcnow().isoformat()}Z",
            "business_model": "general",
            "source_file_name": "",
            "executive_brief": "No business analysis is available yet.",
            "weekly_summary": "Upload and analyze a business file first.",
            "business_health_score": None,
            "kpi_snapshot": {
                "revenue": 0,
                "expenses": 0,
                "profit": 0,
                "profit_margin_percent": 0,
                "growth_rate_percent": 0,
                "cashflow_status": "unknown",
            },
            "forecast_snapshot": {
                "available": False,
                "next_month_revenue": 0,
                "next_quarter_revenue": 0,
                "trend": "unknown",
                "cashflow_risk": "unknown",
                "volatility": "unknown",
            },
            "memory_summary": "No previous business memory available.",
            "top_risks": [],
            "top_opportunities": [],
            "priority_actions": [],
            "ceo_decision": {
                "decision": "Analyze a business file first.",
                "why": "A weekly report requires at least one saved business analysis.",
                "timeframe": "now",
            },
            "data_limitations": [
                "No saved business analysis found."
            ],
            "disclaimer": "This report is for business decision support only. Verify important decisions with a qualified professional.",
        }

    return generate_weekly_report_from_result(
        latest_result=latest_result,
        output_language=output_language,
    )
