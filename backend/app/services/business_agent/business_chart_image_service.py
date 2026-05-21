import os
import tempfile
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib import font_manager


SUPPORTED_LANGUAGES = {"en", "fr", "ar"}

ENTERPRISE_COLORS = {
    "ink": "#0f172a",
    "muted": "#64748b",
    "grid": "#e2e8f0",
    "line": "#111827",
    "bar": "#111827",
    "green": "#059669",
    "red": "#dc2626",
    "blue": "#2563eb",
    "background": "#ffffff",
}


def _safe_language(language: str | None) -> str:
    if language in SUPPORTED_LANGUAGES:
        return language

    return "en"


def _is_rtl(language: str) -> bool:
    return language == "ar"


def _find_font_path() -> str | None:
    """
    Best-effort Unicode font discovery.

    Important:
    - We only use fonts already installed on the server/OS.
    - We do not ship or expose font files.
    """

    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/noto/NotoSansArabic-Regular.ttf",
        "/usr/share/fonts/truetype/noto/NotoNaskhArabic-Regular.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/tahoma.ttf",
        "C:/Windows/Fonts/segoeui.ttf",
    ]

    for path in candidates:
        if os.path.exists(path):
            return path

    try:
        return font_manager.findfont(
            "DejaVu Sans",
            fallback_to_default=True,
        )
    except Exception:
        return None


FONT_PATH = _find_font_path()


def _shape_arabic(text: str) -> str:
    """
    Shape Arabic for matplotlib text rendering.

    Works best when arabic-reshaper and python-bidi are installed:
        pip install arabic-reshaper python-bidi
    """

    try:
        import arabic_reshaper
        from bidi.algorithm import get_display

        return get_display(arabic_reshaper.reshape(text))
    except Exception:
        return text


def _display_text(
    value: Any,
    language: str,
) -> str:
    if value is None:
        text = "-"
    else:
        text = str(value)

    if language == "ar":
        return _shape_arabic(text)

    return text


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
    number = _number(value)

    if number is None:
        return "-"

    if number.is_integer():
        return f"{number:,.0f}"

    return f"{number:,.2f}".rstrip("0").rstrip(".")


def _format_percent(value: Any) -> str:
    number = _number(value)

    if number is None:
        return "-"

    return f"{number:,.2f}%".rstrip("0").rstrip(".")


def _format_money(
    value: Any,
    currency: dict[str, Any] | None,
    language: str,
) -> str:
    number = _number(value)

    if number is None:
        return "-"

    formatted = _format_number(number)
    symbol = str((currency or {}).get("symbol") or "")
    code = str((currency or {}).get("code") or "")
    display_currency = symbol or code

    if not display_currency:
        return formatted

    if language == "ar":
        return f"{formatted} {display_currency}".strip()

    if (currency or {}).get("position") == "suffix":
        return f"{formatted} {display_currency}".strip()

    return f"{display_currency}{formatted}"


def _translate_common_value(
    value: Any,
    language: str,
) -> str:
    text = str(value or "").strip()
    normalized = text.lower()

    translations = {
        "ar": {
            "revenue trend": "تطور الإيرادات",
            "expense trend": "تطور المصاريف",
            "profit evolution": "تطور الأرباح",
            "cashflow trend": "تطور التدفق النقدي",
            "expenses by category": "المصاريف حسب الفئة",
            "payroll": "الرواتب",
            "marketing": "التسويق",
            "software": "البرمجيات",
            "revenue": "الإيرادات",
            "expenses": "المصاريف",
            "profit": "الأرباح",
            "cashflow": "التدفق النقدي",
        },
        "fr": {
            "revenue trend": "Évolution des revenus",
            "expense trend": "Évolution des dépenses",
            "profit evolution": "Évolution du profit",
            "cashflow trend": "Évolution du cashflow",
            "expenses by category": "Dépenses par catégorie",
            "payroll": "Masse salariale",
            "marketing": "Marketing",
            "software": "Logiciels",
            "revenue": "Revenus",
            "expenses": "Dépenses",
            "profit": "Profit",
            "cashflow": "Cashflow",
        },
        "en": {},
    }

    return translations.get(language, {}).get(normalized, text)


def _chart_title(
    title: str | None,
    language: str,
) -> str:
    return _translate_common_value(title or "Business Chart", language)


def _axis_value_formatter(
    value: float,
    y_key: str,
    currency: dict[str, Any] | None,
    language: str,
) -> str:
    key = str(y_key or "").lower()

    if (
        "revenue" in key
        or "expense" in key
        or "profit" in key
        or "cashflow" in key
        or "spend" in key
        or "cost" in key
    ):
        return _format_money(value, currency, language)

    if "percent" in key or "margin" in key or "growth" in key:
        return _format_percent(value)

    return _format_number(value)


def _prepare_matplotlib(language: str):
    plt.rcParams.update(
        {
            "figure.facecolor": ENTERPRISE_COLORS["background"],
            "axes.facecolor": ENTERPRISE_COLORS["background"],
            "axes.edgecolor": ENTERPRISE_COLORS["grid"],
            "axes.labelcolor": ENTERPRISE_COLORS["muted"],
            "xtick.color": ENTERPRISE_COLORS["muted"],
            "ytick.color": ENTERPRISE_COLORS["muted"],
            "grid.color": ENTERPRISE_COLORS["grid"],
            "grid.linewidth": 0.55,
            "axes.titleweight": "bold",
            "axes.titlesize": 13.5,
            "axes.labelsize": 9,
            "xtick.labelsize": 7,
            "ytick.labelsize": 7.2,
            "savefig.facecolor": ENTERPRISE_COLORS["background"],
            "savefig.edgecolor": ENTERPRISE_COLORS["background"],
            "path.simplify": True,
            "path.simplify_threshold": 0.1,
        }
    )

    if FONT_PATH:
        font_manager.fontManager.addfont(FONT_PATH)
        font_name = font_manager.FontProperties(fname=FONT_PATH).get_name()
        plt.rcParams["font.family"] = font_name


def _extract_chart_data(
    chart: dict[str, Any],
) -> tuple[list[str], list[float], str, str]:
    data = chart.get("data") or []
    x_key = chart.get("x_key") or "period"
    y_key = chart.get("y_key") or "value"

    labels: list[str] = []
    values: list[float] = []

    for row in data:
        if not isinstance(row, dict):
            continue

        number = _number(row.get(y_key))

        if number is None:
            continue

        labels.append(str(row.get(x_key, "")))
        values.append(number)

    return labels, values, str(x_key), str(y_key)


def _style_axis(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#eef2f7")
    ax.spines["bottom"].set_color("#eef2f7")
    ax.grid(
        axis="y",
        linestyle="-",
        alpha=0.55,
    )
    ax.set_axisbelow(True)


def _annotate_last_point(
    ax,
    x_index: int,
    value: float,
    text: str,
    language: str,
):
    ax.annotate(
        _display_text(text, language),
        xy=(x_index, value),
        xytext=(8, 8),
        textcoords="offset points",
        fontsize=6.7,
        color=ENTERPRISE_COLORS["ink"],
        bbox={
            "boxstyle": "round,pad=0.35",
            "facecolor": "#ffffff",
            "edgecolor": "#e2e8f0",
            "linewidth": 0.8,
        },
    )


def generate_business_chart_image(
    chart: dict[str, Any],
    output_path: str | None = None,
    language: str = "en",
    currency: dict[str, Any] | None = None,
    width: float = 11.8,
    height: float = 4.8,
    dpi: int = 320,
) -> str | None:
    """
    Generate one premium business chart PNG from backend chart data.

    Supports:
    - line charts
    - bar charts
    - EN / FR / AR labels
    - currency-aware y-axis labels
    - high-resolution PNG output

    Returns:
        Absolute PNG path, or None if chart has no usable data.
    """

    language = _safe_language(language)
    _prepare_matplotlib(language)

    labels, values, _x_key, y_key = _extract_chart_data(chart)

    if not labels or not values:
        return None

    if output_path is None:
        fd, output_path = tempfile.mkstemp(
            suffix=".png",
            prefix="runexa_business_chart_",
        )
        os.close(fd)

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

    translated_labels = [
        _display_text(_translate_common_value(label, language), language)
        for label in labels
    ]

    title = _display_text(_chart_title(chart.get("title"), language), language)

    fig, ax = plt.subplots(
        figsize=(width, height),
        dpi=dpi,
        constrained_layout=False,
    )

    chart_type = str(chart.get("type") or "line").lower()

    if chart_type == "bar":
        bars = ax.bar(
            range(len(values)),
            values,
            color=ENTERPRISE_COLORS["bar"],
            width=0.48,
            zorder=3,
        )

        for bar, value in zip(bars, values):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height(),
                _display_text(
                    _axis_value_formatter(value, y_key, currency, language),
                    language,
                ),
                ha="center",
                va="bottom",
                fontsize=6.8,
                color=ENTERPRISE_COLORS["muted"],
                alpha=0.92,
            )
    else:
        ax.plot(
            range(len(values)),
            values,
            color=ENTERPRISE_COLORS["line"],
            linewidth=2.2,
            marker="o",
            markersize=4,
            markerfacecolor=ENTERPRISE_COLORS["background"],
            markeredgecolor=ENTERPRISE_COLORS["line"],
            markeredgewidth=1.45,
            zorder=3,
        )

        _annotate_last_point(
            ax=ax,
            x_index=len(values) - 1,
            value=values[-1],
            text=_axis_value_formatter(values[-1], y_key, currency, language),
            language=language,
        )

    ax.set_title(
        title,
        loc="right" if _is_rtl(language) else "left",
        color=ENTERPRISE_COLORS["ink"],
        pad=10,
    )

    ax.set_xticks(range(len(values)))
    ax.set_xticklabels(
        translated_labels,
        rotation=0 if len(values) <= 6 else 30,
        ha="right" if len(values) > 6 else "center",
    )

    min_value = min(values)
    max_value = max(values)
    top_padding = abs(max_value) * 0.18 if max_value else 1
    bottom_padding = abs(min_value) * 0.08 if min_value < 0 else 0

    ax.set_ylim(
        min(0, min_value - bottom_padding),
        max_value + top_padding,
    )

    ax.yaxis.set_major_formatter(
        lambda value, _pos: _axis_value_formatter(
            float(value),
            y_key,
            currency,
            language,
        )
    )

    _style_axis(ax)

    fig.savefig(
        output_path,
        format="png",
        dpi=dpi,
        bbox_inches="tight",
        pad_inches=0.18,
    )
    plt.close(fig)

    return os.path.abspath(output_path)


def generate_business_chart_images(
    charts: list[dict[str, Any]] | None,
    output_dir: str | None = None,
    language: str = "en",
    currency: dict[str, Any] | None = None,
) -> list[str]:
    """
    Generate all chart images for one analysis.

    This does not change the analysis payload.
    It only creates temporary PNGs for PDF/PPTX rendering.
    """

    if not charts:
        return []

    if output_dir is None:
        output_dir = tempfile.mkdtemp(
            prefix="runexa_business_charts_",
        )

    Path(output_dir).mkdir(
        parents=True,
        exist_ok=True,
    )

    image_paths: list[str] = []

    for index, chart in enumerate(charts):
        if not isinstance(chart, dict):
            continue

        output_path = os.path.join(
            output_dir,
            f"business_chart_{index + 1}.png",
        )

        image_path = generate_business_chart_image(
            chart=chart,
            output_path=output_path,
            language=language,
            currency=currency,
        )

        if image_path:
            image_paths.append(image_path)

    return image_paths


def cleanup_chart_images(
    image_paths: list[str],
) -> None:
    """
    Best-effort cleanup for temporary chart images.
    Safe to call even when files are already deleted.
    """

    for image_path in image_paths:
        try:
            if os.path.exists(image_path):
                os.remove(image_path)
        except Exception:
            continue
