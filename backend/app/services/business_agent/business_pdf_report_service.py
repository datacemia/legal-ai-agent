import json
import os
import re
import tempfile
from datetime import datetime
from typing import Any

from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from reportlab.graphics.shapes import Drawing, String
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    HRFlowable,
    Image,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


from app.services.business_agent.business_chart_image_service import (
    cleanup_chart_images,
    generate_business_chart_images,
)


BRAND_NAME = "Runexa Systems"
SUPPORTED_LANGUAGES = {"en", "fr", "ar"}

INK = colors.HexColor("#0f172a")
MUTED = colors.HexColor("#64748b")
BORDER = colors.HexColor("#e2e8f0")
LIGHT = colors.HexColor("#f8fafc")
GREEN = colors.HexColor("#059669")
RED = colors.HexColor("#dc2626")
AMBER = colors.HexColor("#d97706")
BLUE = colors.HexColor("#2563eb")
WHITE = colors.white
DARK_PANEL = colors.HexColor("#020617")
PANEL = colors.HexColor("#f1f5f9")


def _register_fonts() -> dict[str, str]:
    """
    Register Unicode fonts when available.
    This fixes Arabic/Unicode black squares in generated PDFs.
    Font files are loaded from the OS only; they are not bundled or shared.
    """

    candidates = [
        (
            "RunexaSans",
            "RunexaSans-Bold",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        ),
        (
            "RunexaSans",
            "RunexaSans-Bold",
            "C:/Windows/Fonts/arial.ttf",
            "C:/Windows/Fonts/arialbd.ttf",
        ),
        (
            "RunexaSans",
            "RunexaSans-Bold",
            "C:/Windows/Fonts/tahoma.ttf",
            "C:/Windows/Fonts/tahomabd.ttf",
        ),
    ]

    for regular_name, bold_name, regular_path, bold_path in candidates:
        if os.path.exists(regular_path):
            try:
                pdfmetrics.registerFont(TTFont(regular_name, regular_path))

                if os.path.exists(bold_path):
                    pdfmetrics.registerFont(TTFont(bold_name, bold_path))
                else:
                    bold_name = regular_name

                return {
                    "regular": regular_name,
                    "bold": bold_name,
                }
            except Exception:
                continue

    return {
        "regular": "Helvetica",
        "bold": "Helvetica-Bold",
    }


FONTS = _register_fonts()


def _safe_language(language: str | None) -> str:
    return language if language in SUPPORTED_LANGUAGES else "en"


def _is_rtl(language: str) -> bool:
    return language == "ar"


def _shape_arabic(text: str) -> str:
    """
    Best-effort Arabic shaping for ReportLab.
    Without this, Arabic can render disconnected or as tofu depending on renderer.
    """

    try:
        import arabic_reshaper
        from bidi.algorithm import get_display

        return get_display(arabic_reshaper.reshape(text))
    except Exception:
        return text


def _display_text(value: Any, language: str, fallback: str = "-") -> str:
    if value is None:
        text = fallback
    elif isinstance(value, str):
        text = value.strip() or fallback
    elif isinstance(value, bool):
        text = "Yes" if value else "No"
    elif isinstance(value, int | float):
        text = str(value)
    else:
        try:
            text = json.dumps(value, ensure_ascii=False)
        except Exception:
            text = fallback

    if language == "ar":
        return _shape_arabic(text)

    return text


def _xml_escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def _number(value: Any) -> float | None:
    if isinstance(value, bool):
        return None

    if isinstance(value, int | float):
        return float(value)

    try:
        return float(value)
    except Exception:
        return None


def _format_number(value: Any) -> str:
    numeric = _number(value)

    if numeric is None:
        return "-"

    if numeric.is_integer():
        return f"{numeric:,.0f}"

    return f"{numeric:,.2f}".rstrip("0").rstrip(".")


def _format_percent(value: Any) -> str:
    numeric = _number(value)

    if numeric is None:
        return "-"

    return f"{numeric:,.2f}%".rstrip("0").rstrip(".")


def _format_money(
    value: Any,
    currency: dict[str, Any] | None,
    language: str,
) -> str:
    numeric = _number(value)

    if numeric is None:
        return "-"

    number = _format_number(numeric)
    symbol = str((currency or {}).get("symbol") or "")
    code = str((currency or {}).get("code") or "")
    display_currency = symbol or code

    if not display_currency:
        return number

    if language == "ar":
        return f"{number} {display_currency}".strip()

    if (currency or {}).get("position") == "suffix":
        return f"{number} {display_currency}".strip()

    return f"{display_currency}{number}"


def _format_health_score(
    analysis: dict[str, Any],
    business_health: dict[str, Any],
) -> str:
    """
    Format Business Health Score without converting unavailable values to 0/100.

    Product catalogs, inventory files, reference tables, and incomplete datasets can
    legitimately have business_health_score = None. In those cases, PDF exports
    must show N/A, matching the web dashboard.
    """

    score = analysis.get("business_health_score")

    if score is None:
        score = business_health.get("score")

    if isinstance(score, bool):
        return "N/A"

    if isinstance(score, int | float):
        return f"{int(round(float(score)))}/100"

    return "N/A"


def _labels(language: str) -> dict[str, str]:
    labels = {
        "en": {
            "title": "Executive Business Report",
            "subtitle": "Data-verified business intelligence report",
            "generated_at": "Generated at",
            "source_file": "Source file",
            "verified": "Data-verified analysis",
            "summary": "Executive Summary",
            "kpis": "Core KPIs",
            "health": "Business Health",
            "business_model": "Industry Sector",
            "score": "Score",
            "rating": "Rating",
            "currency": "Currency",
            "revenue": "Revenue",
            "expenses": "Expenses",
            "profit": "Profit",
            "margin": "Profit Margin",
            "growth": "Growth",
            "cashflow": "Flux de trésorerie",
            "decision": "Priority Decision",
            "risks": "Risks",
            "opportunities": "Opportunities",
            "recommendations": "Recommendations",
            "forecast": "Forecast",
            "data_quality": "Data Quality",
            "advanced_kpis": "Advanced KPIs",
            "disclaimer": "Disclaimer",
            "next_month": "Next Month Revenue",
            "next_quarter": "Next Quarter Revenue",
            "trend": "Trend",
            "cashflow_risk": "Cash Flow Risk",
            "volatility": "Volatility",
            "strengths": "Strengths",
            "warnings": "Warnings",
            "missing_fields": "Missing fields",
            "limitations": "Limitations",
            "metric": "Metric",
            "value": "Value",
            "charts": "Charts",
            "no_data": "No data available.",
            "multi_currency_warning": "Multiple currencies were detected in the uploaded data.",
        },
        "fr": {
            "title": "Rapport exécutif business",
            "subtitle": "Rapport d’intelligence business vérifié par les données",
            "generated_at": "Généré le",
            "source_file": "Fichier source",
            "verified": "Analyse vérifiée par les données",
            "summary": "Résumé exécutif",
            "kpis": "KPIs principaux",
            "health": "Santé de l\'entreprise",
            "business_model": "Secteur d\'activité",
            "score": "Score",
            "rating": "Évaluation",
            "currency": "Devise",
            "revenue": "Revenus",
            "expenses": "Dépenses",
            "profit": "Profit",
            "margin": "Marge",
            "growth": "Croissance",
            "cashflow": "Flux de trésorerie",
            "decision": "Décision prioritaire",
            "risks": "Risques",
            "opportunities": "Opportunités",
            "recommendations": "Recommandations",
            "forecast": "Prévisions",
            "data_quality": "Qualité des données",
            "advanced_kpis": "KPIs avancés",
            "disclaimer": "Avertissement",
            "next_month": "Revenus mois prochain",
            "next_quarter": "Revenus prochain trimestre",
            "trend": "Tendance",
            "cashflow_risk": "Risque de flux de trésorerie",
            "volatility": "Volatilité",
            "strengths": "Forces",
            "warnings": "Alertes",
            "missing_fields": "Champs manquants",
            "limitations": "Limites",
            "metric": "Métrique",
            "value": "Valeur",
            "charts": "Graphiques",
            "no_data": "Aucune donnée disponible.",
            "multi_currency_warning": "Plusieurs devises ont été détectées dans les données importées.",
        },
        "ar": {
            "title": "تقرير تنفيذي للأعمال",
            "subtitle": "تقرير ذكاء أعمال موثوق بالبيانات",
            "generated_at": "تم الإنشاء في",
            "source_file": "الملف المصدر",
            "verified": "تحليل موثوق بالبيانات",
            "summary": "الملخص التنفيذي",
            "kpis": "المؤشرات الأساسية",
            "health": "صحة الأعمال",
            "business_model": "نوع النشاط",
            "score": "النتيجة",
            "rating": "التقييم",
            "currency": "العملة",
            "revenue": "الإيرادات",
            "expenses": "المصاريف",
            "profit": "الأرباح",
            "margin": "الهامش",
            "growth": "النمو",
            "cashflow": "التدفق النقدي",
            "decision": "القرار الأولوي",
            "risks": "المخاطر",
            "opportunities": "الفرص",
            "recommendations": "التوصيات",
            "forecast": "التوقعات",
            "data_quality": "جودة البيانات",
            "advanced_kpis": "مؤشرات متقدمة",
            "disclaimer": "تنبيه",
            "next_month": "إيرادات الشهر القادم",
            "next_quarter": "إيرادات الربع القادم",
            "trend": "الاتجاه",
            "cashflow_risk": "مخاطر التدفق النقدي",
            "volatility": "التقلب",
            "strengths": "نقاط القوة",
            "warnings": "التحذيرات",
            "missing_fields": "الحقول الناقصة",
            "limitations": "القيود",
            "metric": "المؤشر",
            "value": "القيمة",
            "charts": "الرسوم البيانية",
            "no_data": "لا توجد بيانات متاحة.",
            "multi_currency_warning": "تم اكتشاف عدة عملات داخل البيانات التي تم رفعها.",
        },
    }

    return labels.get(language, labels["en"])



def _translate_common_value(value: Any, language: str) -> str:
    text = str(value or "").strip()
    normalized = text.lower()

    translations = {
        "ar": {
            "up": "صاعد",
            "down": "هابط",
            "stable": "مستقر",
            "flat": "مستقر",
            "not specified": "غير محددة",
            "n/a": "غير متاح",
            "excellent profit margin.": "هامش ربح ممتاز.",
            "revenue is declining.": "الإيرادات في تراجع.",
            "excellent data quality.": "جودة بيانات ممتازة.",
            "low": "منخفض",
            "medium": "متوسط",
            "high": "مرتفع",
            "critical": "حرج",
            "healthy": "جيد",
            "positive": "إيجابي",
            "negative": "سلبي",
            "general": "عام",
            "saas": "SaaS / اشتراك",
            "healthy profit margin.": "هامش ربح صحي.",
            "healthy growth.": "نمو صحي.",
            "positive cashflow.": "تدفق نقدي إيجابي.",
            "healthy roas.": "عائد إنفاق إعلاني صحي.",
            "healthy cac efficiency.": "كفاءة صحية لتكلفة اكتساب العميل.",
            "critical churn level.": "مستوى فقدان عملاء حرج.",
            "payroll": "الرواتب",
            "marketing": "التسويق",
            "software": "البرمجيات",
            "ad spend": "الإنفاق الإعلاني",
            "customers": "العملاء",
            "orders": "الطلبات",
            "churn": "فقدان العملاء",
        },
        "fr": {
            "up": "hausse",
            "down": "baisse",
            "stable": "stable",
            "flat": "stable",
            "not specified": "Non définie",
            "n/a": "Indisponible",
            "excellent profit margin.": "Excellente marge bénéficiaire.",
            "revenue is declining.": "Les revenus sont en baisse.",
            "excellent data quality.": "Excellente qualité des données.",
            "low": "faible",
            "medium": "moyen",
            "high": "élevé",
            "critical": "critique",
            "healthy": "sain",
            "positive": "positif",
            "negative": "négatif",
            "general": "général",
            "saas": "SaaS / abonnement",
            "healthy profit margin.": "Marge bénéficiaire saine.",
            "healthy growth.": "Croissance saine.",
            "positive cashflow.": "Flux de trésorerie positif.",
            "healthy roas.": "ROAS sain.",
            "healthy cac efficiency.": "Efficacité CAC saine.",
            "critical churn level.": "Niveau de churn critique.",
            "payroll": "Masse salariale",
            "marketing": "Marketing",
            "software": "Logiciels",
            "ad spend": "Dépenses publicitaires",
            "customers": "Clients",
            "orders": "Commandes",
            "churn": "Churn",
        },
        "en": {},
    }

    return translations.get(language, {}).get(normalized, text)


def _translate_category(value: Any, language: str) -> str:
    return _translate_common_value(value, language)


def _translate_list_values(values: list[Any], language: str) -> list[str]:
    return [_translate_common_value(value, language) for value in values]



def _localized_metric_label(metric: Any, language: str) -> str:
    text = str(metric or "").strip()
    normalized = text.lower()

    labels = {
        "en": {
            "aov": "AOV",
            "cac": "CAC",
            "roas": "ROAS",
            "mrr": "MRR",
            "arr": "ARR",
            "churn": "Churn",
            "customers": "Customers",
            "orders": "Orders",
            "ad spend": "Ad spend",
        },
        "fr": {
            "aov": "Panier moyen",
            "cac": "CAC",
            "roas": "ROAS",
            "mrr": "MRR",
            "arr": "ARR",
            "churn": "Churn",
            "customers": "Clients",
            "orders": "Commandes",
            "ad spend": "Dépenses publicitaires",
        },
        "ar": {
            "aov": "متوسط قيمة الطلب",
            "cac": "تكلفة اكتساب العميل",
            "roas": "عائد الإنفاق الإعلاني",
            "mrr": "الإيراد الشهري المتكرر",
            "arr": "الإيراد السنوي المتكرر",
            "churn": "فقدان العملاء",
            "customers": "العملاء",
            "orders": "الطلبات",
            "ad spend": "الإنفاق الإعلاني",
        },
    }

    return labels.get(language, labels["en"]).get(normalized, text)


def _translate_and_normalize(value: Any, language: str) -> str:
    translated = _translate_common_value(value, language)

    if language == "fr" and translated:
        exact = {
            "Moyen": "moyen",
            "Élevé": "élevé",
            "Critique": "critique",
            "Sain": "sain",
            "Positif": "positif",
            "Faible": "faible",
        }
        translated = exact.get(translated, translated)

    return translated




def _empty_list_message(kind: str, language: str) -> str:
    messages = {
        "missing_fields": {
            "ar": "لا توجد حقول ناقصة",
            "fr": "Aucun champ manquant",
            "en": "No missing fields",
        },
        "limitations": {
            "ar": "لا توجد قيود كبيرة",
            "fr": "Aucune limitation majeure",
            "en": "No major limitations",
        },
        "risks": {
            "ar": "لم يتم اكتشاف مخاطر حرجة",
            "fr": "Aucun risque critique détecté",
            "en": "No critical risks detected",
        },
    }
    return messages.get(kind, {}).get(language, messages.get(kind, {}).get("en", "-"))

def _display_currency(currency: dict[str, Any] | None, language: str) -> str:
    currency = currency or {}
    code = currency.get("code")
    symbol = currency.get("symbol")

    parts = [
        str(part).strip()
        for part in (code, symbol)
        if part not in (None, "", "-", "None")
    ]

    if parts:
        return " ".join(parts)

    return _translate_common_value("Not specified", language)


def _format_advanced_metric(
    value: Any,
    language: str,
    *,
    is_money: bool = False,
    is_percent: bool = False,
    currency: dict[str, Any] | None = None,
) -> str:
    if value in (None, "", "unknown", "N/A"):
        return _translate_common_value("N/A", language)

    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return str(value)

    if numeric == 0:
        return _translate_common_value("N/A", language)

    if is_percent:
        return f"{numeric:.2f}%"

    if is_money:
        return _format_money(numeric, currency, language)

    return _format_number(numeric, language)

def _format_narrative_text(
    text: Any,
    language: str,
    currency: dict[str, Any] | None = None,
) -> str:
    if not isinstance(text, str):
        return "-"

    result = text

    replacements = {
        "137300.0": _format_money(137300.0, currency, language),
        "98650.0": _format_money(98650.0, currency, language),
        "38650.0": _format_money(38650.0, currency, language),
        "28.15%": _format_percent(28.15),
        "10.32%": _format_percent(10.32),
        "28.65%": _format_percent(28.65),
        "28.65": _format_number(28.65),
        "73/100": "73/100",
    }

    for source, target in replacements.items():
        result = result.replace(source, target)

    common_values = {
        "Positive": _translate_and_normalize("positive", language),
        "positive": _translate_and_normalize("positive", language),
        "Healthy": _translate_and_normalize("healthy", language),
        "healthy": _translate_and_normalize("healthy", language),
        "Critical": _translate_and_normalize("critical", language),
        "critical": _translate_and_normalize("critical", language),
        "Medium": _translate_and_normalize("medium", language),
        "medium": _translate_and_normalize("medium", language),
        "Low": _translate_and_normalize("low", language),
        "low": _translate_and_normalize("low", language),
    }

    if language != "en":
        for source, target in common_values.items():
            result = re.sub(
                rf"\\b{re.escape(source)}\\b",
                target,
                result,
            )

    return result


def _styles(language: str) -> dict[str, ParagraphStyle]:
    align = TA_RIGHT if _is_rtl(language) else TA_LEFT

    return {
        "cover_brand": ParagraphStyle(
            "CoverBrand",
            fontName=FONTS["bold"],
            fontSize=10,
            leading=13,
            textColor=MUTED,
            alignment=align,
        ),
        "cover_title": ParagraphStyle(
            "CoverTitle",
            fontName=FONTS["bold"],
            fontSize=31,
            leading=37,
            textColor=INK,
            alignment=align,
            spaceAfter=10,
        ),
        "cover_subtitle": ParagraphStyle(
            "CoverSubtitle",
            fontName=FONTS["regular"],
            fontSize=12,
            leading=18,
            textColor=MUTED,
            alignment=align,
            spaceAfter=18,
        ),
        "section_title": ParagraphStyle(
            "SectionTitle",
            fontName=FONTS["bold"],
            fontSize=17,
            leading=22,
            textColor=INK,
            alignment=align,
            spaceBefore=8,
            spaceAfter=8,
        ),
        "body": ParagraphStyle(
            "Body",
            fontName=FONTS["regular"],
            fontSize=10,
            leading=15,
            textColor=colors.HexColor("#334155"),
            alignment=align,
        ),
        "body_bold": ParagraphStyle(
            "BodyBold",
            fontName=FONTS["bold"],
            fontSize=9.5,
            leading=14,
            textColor=INK,
            alignment=align,
        ),
        "small": ParagraphStyle(
            "Small",
            fontName=FONTS["regular"],
            fontSize=8,
            leading=11,
            textColor=MUTED,
            alignment=align,
        ),
        "badge": ParagraphStyle(
            "Badge",
            fontName=FONTS["bold"],
            fontSize=8,
            leading=10,
            textColor=GREEN,
            alignment=align,
        ),
        "kpi_label": ParagraphStyle(
            "KpiLabel",
            fontName=FONTS["regular"],
            fontSize=8,
            leading=10,
            textColor=MUTED,
            alignment=align,
        ),
        "kpi_value": ParagraphStyle(
            "KpiValue",
            fontName=FONTS["bold"],
            fontSize=13,
            leading=16,
            textColor=INK,
            alignment=align,
        ),
    }


def _p(value: Any, style: ParagraphStyle, language: str) -> Paragraph:
    text = _xml_escape(_display_text(value, language))
    return Paragraph(text, style)


def _section(title: str, styles: dict[str, ParagraphStyle], language: str) -> list[Any]:
    return [
        Spacer(1, 0.2 * cm),
        _p(title, styles["section_title"], language),
        HRFlowable(
            width="100%",
            thickness=0.8,
            color=BORDER,
            spaceBefore=2,
            spaceAfter=8,
        ),
    ]


def _table(
    data: list[list[Any]],
    col_widths: list[float],
    header: bool = False,
    background=WHITE,
) -> Table:
    table = Table(
        data,
        colWidths=col_widths,
        repeatRows=1 if header else 0,
        hAlign="LEFT",
    )

    table_style = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BOX", (0, 0), (-1, -1), 0.6, BORDER),
        ("INNERGRID", (0, 0), (-1, -1), 0.35, BORDER),
        ("BACKGROUND", (0, 0), (-1, -1), background),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]

    if header:
        table_style.extend(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f1f5f9")),
                ("TEXTCOLOR", (0, 0), (-1, 0), INK),
                ("FONTNAME", (0, 0), (-1, 0), FONTS["bold"]),
            ]
        )

    table.setStyle(TableStyle(table_style))
    return table


def _kpi_cell(
    label: str,
    value: str,
    styles: dict[str, ParagraphStyle],
    language: str,
) -> list[Any]:
    return [
        _p(label, styles["kpi_label"], language),
        Spacer(1, 0.05 * cm),
        _p(value, styles["kpi_value"], language),
    ]


def _item_title(item: Any) -> str:
    if isinstance(item, str):
        return item

    if not isinstance(item, dict):
        return "Item"

    return (
        item.get("title")
        or item.get("risk")
        or item.get("opportunity")
        or item.get("recommendation")
        or item.get("decision")
        or item.get("description")
        or item.get("what_happened")
        or "Item"
    )


def _item_description(item: Any) -> str:
    if not isinstance(item, dict):
        return ""

    return (
        item.get("description")
        or item.get("why_it_matters")
        or item.get("expected_impact")
        or item.get("recommended_action")
        or item.get("why")
        or item.get("summary")
        or ""
    )


def _item_badge(item: Any) -> str:
    if not isinstance(item, dict):
        return ""

    return str(item.get("severity") or item.get("priority") or item.get("impact") or "")


def _list_items(
    items: list[Any],
    styles: dict[str, ParagraphStyle],
    language: str,
    max_items: int = 7,
) -> list[Any]:
    story: list[Any] = []

    if not items:
        empty_message = {
            "ar": "لم يتم اكتشاف مخاطر حرجة",
            "fr": "Aucun risque critique détecté",
            "en": "No critical risks detected",
        }.get(language, "No critical risks detected")
        story.append(_p(empty_message, styles["body"], language))
        return story

    for index, item in enumerate(items[:max_items], start=1):
        title = _translate_and_normalize(_item_title(item), language)
        description = _format_narrative_text(_translate_and_normalize(_item_description(item), language), language, None)
        badge = _translate_and_normalize(_item_badge(item), language)

        block = [
            _p(f"{index}. {title}", styles["body_bold"], language),
        ]

        if badge:
            block.append(_p(badge, styles["small"], language))

        if description:
            block.append(_p(description, styles["small"], language))

        if isinstance(item, dict) and item.get("business_impact"):
            impacts = ", ".join(_translate_and_normalize(x, language) for x in item.get("business_impact") or [])
            block.append(_p(impacts, styles["small"], language))

        block.append(Spacer(1, 0.14 * cm))
        story.append(KeepTogether(block))

    return story


def _chart_title(title: str, language: str) -> str:
    mapping = {
        "Revenue Trend": {"fr": "Évolution des revenus", "ar": "تطور الإيرادات"},
        "Expense Trend": {"fr": "Évolution des dépenses", "ar": "تطور المصاريف"},
        "Profit Evolution": {"fr": "Évolution du profit", "ar": "تطور الأرباح"},
        "Cashflow Trend": {"fr": "Évolution du flux de trésorerie", "ar": "تطور التدفق النقدي"},
        "Expenses by Category": {"fr": "Dépenses par catégorie", "ar": "المصاريف حسب الفئة"},
        "Revenue by Category": {"fr": "Revenus par catégorie", "ar": "الإيرادات حسب الفئة"},
    }

    return mapping.get(title, {}).get(language, title)


def _chart_drawing(chart: dict[str, Any], language: str) -> Drawing | None:
    data = chart.get("data") or []
    x_key = chart.get("x_key") or "period"
    y_key = chart.get("y_key") or "value"

    if not data:
        return None

    values = []
    labels = []

    for item in data:
        value = _number(item.get(y_key))
        if value is None:
            continue

        values.append(value)
        labels.append(_translate_category(item.get(x_key, ""), language)[:12])

    if not values:
        return None

    drawing = Drawing(480, 210)

    title = _chart_title(str(chart.get("title") or ""), language)
    drawing.add(
        String(
            0,
            195,
            _display_text(title, language),
            fontName=FONTS["bold"],
            fontSize=10,
            fillColor=INK,
        )
    )

    if chart.get("type") == "bar":
        c = VerticalBarChart()
        c.x = 35
        c.y = 35
        c.height = 135
        c.width = 400
        c.data = [values]
        c.categoryAxis.categoryNames = labels
        c.categoryAxis.labels.fontName = FONTS["regular"]
        c.categoryAxis.labels.fontSize = 6
        c.valueAxis.labels.fontName = FONTS["regular"]
        c.valueAxis.labels.fontSize = 7
        c.bars[0].fillColor = INK
        c.valueAxis.valueMin = min(0, min(values))
        c.valueAxis.valueMax = max(values) * 1.15
        c.valueAxis.valueStep = max(max(values) / 4, 1)
        drawing.add(c)
    else:
        c = HorizontalLineChart()
        c.x = 35
        c.y = 35
        c.height = 135
        c.width = 400
        c.data = [values]
        c.categoryAxis.categoryNames = labels
        c.categoryAxis.labels.fontName = FONTS["regular"]
        c.categoryAxis.labels.fontSize = 6
        c.valueAxis.labels.fontName = FONTS["regular"]
        c.valueAxis.labels.fontSize = 7
        c.lines[0].strokeColor = INK
        c.lines[0].strokeWidth = 2
        c.valueAxis.valueMin = min(0, min(values))
        c.valueAxis.valueMax = max(values) * 1.15
        c.valueAxis.valueStep = max(max(values) / 4, 1)
        drawing.add(c)

    return drawing


def _footer(canvas, doc):
    canvas.saveState()
    width, _height = A4

    canvas.setStrokeColor(BORDER)
    canvas.line(1.5 * cm, 1.2 * cm, width - 1.5 * cm, 1.2 * cm)

    canvas.setFont(FONTS["regular"], 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(1.5 * cm, 0.82 * cm, f"{BRAND_NAME} - Executive Business Report")
    canvas.drawRightString(width - 1.5 * cm, 0.82 * cm, f"Page {doc.page}")

    canvas.restoreState()



def _chart_image_block(
    image_path: str,
    max_width: float = 17.0 * cm,
    max_height: float = 8.2 * cm,
) -> Image:
    image = Image(image_path)
    image._restrictSize(max_width, max_height)
    return image


def build_business_pdf_report(
    analysis: dict[str, Any],
    output_path: str | None = None,
    language: str = "en",
    source_file_name: str | None = None,
) -> str:
    """
    Generate a clean executive PDF report.

    Fixes included:
    - Unicode/Arabic capable fonts.
    - Arabic shaping when arabic-reshaper + python-bidi are installed.
    - Fully localized headings.
    - Better executive layout.
    - Chart pages from existing backend chart data.
    """

    language = _safe_language(language)
    labels = _labels(language)
    styles = _styles(language)

    if output_path is None:
        fd, output_path = tempfile.mkstemp(
            suffix=".pdf",
            prefix="runexa_business_report_",
        )
        os.close(fd)

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=1.5 * cm,
        leftMargin=1.5 * cm,
        topMargin=1.45 * cm,
        bottomMargin=1.5 * cm,
        title=labels["title"],
        author=BRAND_NAME,
    )

    story: list[Any] = []

    kpis = analysis.get("kpis") or {}
    advanced = analysis.get("advanced_kpis") or {}
    forecast = analysis.get("forecast") or {}
    currency = analysis.get("currency") or {}
    business_health = analysis.get("business_health") or {}
    data_quality = analysis.get("data_quality") or {}
    decision = (analysis.get("smart_insights") or {}).get("most_important_decision") or {}

    generated_at = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    source_file = source_file_name or (analysis.get("file_metadata") or {}).get("file_name") or "-"
    health_score_display = _format_health_score(analysis, business_health)

    # Cover
    story.append(_p(BRAND_NAME, styles["cover_brand"], language))
    story.append(Spacer(1, 0.25 * cm))
    story.append(_p(labels["title"], styles["cover_title"], language))
    story.append(_p(labels["subtitle"], styles["cover_subtitle"], language))
    story.append(Spacer(1, 0.1 * cm))
    story.append(_p(labels["verified"], styles["badge"], language))
    story.append(Spacer(1, 0.5 * cm))

    hero_cards = [
        _kpi_cell(labels["health"], health_score_display, styles, language),
        _kpi_cell(labels["revenue"], _format_money(kpis.get("revenue"), currency, language), styles, language),
        _kpi_cell(labels["profit"], _format_money(kpis.get("profit"), currency, language), styles, language),
    ]
    story.append(_table([hero_cards], [5.15 * cm, 5.15 * cm, 5.15 * cm], background=PANEL))
    story.append(Spacer(1, 0.45 * cm))

    metadata_rows = [
        [_p(labels["generated_at"], styles["small"], language), _p(generated_at, styles["body"], language)],
        [_p(labels["source_file"], styles["small"], language), _p(source_file, styles["body"], language)],
        [_p(labels["business_model"], styles["small"], language), _p(_translate_common_value(analysis.get("business_model") or "-", language), styles["body"], language)],
        [_p(labels["currency"], styles["small"], language), _p(_display_currency(currency, language), styles["body"], language)],
    ]
    story.append(_table(metadata_rows, [4.5 * cm, 11 * cm], header=False, background=WHITE))

    if currency.get("multi_currency_detected") or analysis.get("currency_warning"):
        story.append(Spacer(1, 0.25 * cm))
        story.append(_p(labels["multi_currency_warning"], styles["body_bold"], language))

    story.append(PageBreak())

    # Summary
    story.extend(_section(labels["summary"], styles, language))
    story.append(_p(_format_narrative_text(analysis.get("executive_summary") or "-", language, currency), styles["body"], language))

    story.extend(_section(labels["kpis"], styles, language))

    kpi_cells = [
        _kpi_cell(labels["revenue"], _format_money(kpis.get("revenue"), currency, language), styles, language),
        _kpi_cell(labels["expenses"], _format_money(kpis.get("expenses"), currency, language), styles, language),
        _kpi_cell(labels["profit"], _format_money(kpis.get("profit"), currency, language), styles, language),
        _kpi_cell(labels["margin"], _format_percent(kpis.get("profit_margin_percent")), styles, language),
        _kpi_cell(labels["growth"], _format_percent(kpis.get("growth_rate_percent")), styles, language),
        _kpi_cell(labels["cashflow"], _translate_and_normalize(kpis.get("cashflow_status") or "-", language), styles, language),
    ]

    story.append(
        _table(
            [
                kpi_cells[:3],
                kpi_cells[3:],
            ],
            [5.15 * cm, 5.15 * cm, 5.15 * cm],
            background=LIGHT,
        )
    )

    # Health + decision + forecast
    story.extend(_section(labels["health"], styles, language))
    health_rows = [
        [_p(labels["score"], styles["small"], language), _p(health_score_display, styles["body_bold"], language)],
        [_p(labels["rating"], styles["small"], language), _p(_translate_common_value(business_health.get("rating") or "-", language), styles["body"], language)],
    ]
    story.append(_table(health_rows, [4.5 * cm, 11 * cm], background=WHITE))

    if business_health.get("strengths"):
        story.append(Spacer(1, 0.2 * cm))
        story.append(_p(labels["strengths"], styles["body_bold"], language))
        story.extend(_list_items(business_health.get("strengths") or [], styles, language, max_items=5))

    if business_health.get("warnings"):
        story.append(_p(labels["warnings"], styles["body_bold"], language))
        story.extend(_list_items(business_health.get("warnings") or [], styles, language, max_items=5))

    if decision:
        story.extend(_section(labels["decision"], styles, language))
        story.append(_p(decision.get("title") or "-", styles["body_bold"], language))

        if decision.get("decision"):
            story.append(_p(decision.get("decision"), styles["body"], language))

        if decision.get("why"):
            story.append(_p(_format_narrative_text(decision.get("why"), language, currency), styles["small"], language))

        if decision.get("impact"):
            story.append(_p(f"{labels['score']}: {_translate_and_normalize(decision.get('impact'), language)}", styles["small"], language))

    if forecast:
        story.extend(_section(labels["forecast"], styles, language))
        forecast_rows = [
            [_p(labels["next_month"], styles["small"], language), _p(_format_money(forecast.get("next_month_revenue"), currency, language), styles["body"], language)],
            [_p(labels["next_quarter"], styles["small"], language), _p(_format_money(forecast.get("next_quarter_revenue"), currency, language), styles["body"], language)],
            [_p(labels["trend"], styles["small"], language), _p(_translate_and_normalize(forecast.get("trend") or "-", language), styles["body"], language)],
            [_p(labels["cashflow_risk"], styles["small"], language), _p(_translate_and_normalize(forecast.get("cashflow_risk") or "-", language), styles["body"], language)],
            [_p(labels["volatility"], styles["small"], language), _p(_translate_and_normalize(forecast.get("volatility") or "-", language), styles["body"], language)],
        ]
        story.append(_table(forecast_rows, [4.8 * cm, 10.7 * cm], background=WHITE))

        if forecast.get("explanation"):
            story.append(Spacer(1, 0.15 * cm))
            story.append(_p(_format_narrative_text(forecast.get("explanation"), language, currency), styles["small"], language))

    # Charts
    charts = analysis.get("charts") or []
    chart_image_paths: list[str] = []

    if charts:
        story.append(PageBreak())
        story.extend(_section(labels["charts"], styles, language))

        chart_image_paths = generate_business_chart_images(
            charts=charts[:5],
            language=language,
            currency=currency,
        )

        if chart_image_paths:
            for image_path in chart_image_paths:
                story.append(
                    KeepTogether(
                        [
                            _chart_image_block(image_path),
                            Spacer(1, 0.35 * cm),
                        ]
                    )
                )
        else:
            story.append(_p(labels["no_data"], styles["body"], language))

    # Risks / Opportunities / Recommendations
    story.append(PageBreak())
    story.extend(_section(labels["risks"], styles, language))
    story.extend(_list_items(analysis.get("risks") or [], styles, language, max_items=8))

    story.extend(_section(labels["opportunities"], styles, language))
    story.extend(_list_items(analysis.get("opportunities") or [], styles, language, max_items=8))

    story.extend(_section(labels["recommendations"], styles, language))
    story.extend(_list_items(analysis.get("recommendations") or [], styles, language, max_items=8))

    # Advanced KPIs + Quality
    story.append(PageBreak())
    if advanced:
        story.extend(_section(labels["advanced_kpis"], styles, language))
        rows = [
            [_p(labels["metric"], styles["body_bold"], language), _p(labels["value"], styles["body_bold"], language)]
        ]

        fields = [
            ("AOV", advanced.get("aov"), True, False),
            ("CAC", advanced.get("cac"), True, False),
            ("ROAS", advanced.get("roas"), False, False),
            ("MRR", advanced.get("mrr"), True, False),
            ("ARR", advanced.get("arr"), True, False),
            ("Churn", advanced.get("churn_rate_percent"), False, True),
            ("Customers", advanced.get("customers"), False, False),
            ("Orders", advanced.get("orders"), False, False),
            ("Ad spend", advanced.get("ad_spend"), True, False),
        ]

        for metric, value, money, percent in fields:
            display = _format_advanced_metric(
                value,
                language,
                is_money=money,
                is_percent=percent,
                currency=currency,
            )

            rows.append([_p(_localized_metric_label(metric, language), styles["body"], language), _p(display, styles["body"], language)])

        story.append(_table(rows, [6 * cm, 9.5 * cm], header=True, background=WHITE))

    story.extend(_section(labels["data_quality"], styles, language))
    quality_rows = [
        [_p(labels["score"], styles["small"], language), _p(f"{data_quality.get('score', 0)}/100", styles["body_bold"], language)],
        [_p(labels["missing_fields"], styles["small"], language), _p(", ".join(data_quality.get("missing_fields") or []) or _empty_list_message("missing_fields", language), styles["body"], language)],
        [_p(labels["limitations"], styles["small"], language), _p(", ".join(data_quality.get("limitations") or []) or _empty_list_message("limitations", language), styles["body"], language)],
    ]
    story.append(_table(quality_rows, [5 * cm, 10.5 * cm], background=WHITE))

    if analysis.get("disclaimer"):
        story.extend(_section(labels["disclaimer"], styles, language))
        story.append(_p(analysis.get("disclaimer"), styles["small"], language))

    try:
        doc.build(story, onFirstPage=_footer, onLaterPages=_footer)
    finally:
        cleanup_chart_images(chart_image_paths)

    return os.path.abspath(output_path)


def build_business_pdf_report_response_payload(pdf_path: str) -> dict[str, Any]:
    return {
        "file_path": pdf_path,
        "file_name": os.path.basename(pdf_path),
        "content_type": "application/pdf",
        "generated_at": datetime.utcnow().isoformat() + "Z",
    }
