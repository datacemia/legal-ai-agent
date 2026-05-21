"""
Runexa Business Agent Backend Test Script

What it tests:
1. POST /business/analyze with a realistic CSV file
2. GET /business/history
3. POST /business/weekly-report

Usage:
    python test_business_backend.py --token YOUR_JWT_TOKEN

Optional:
    python test_business_backend.py --base-url http://127.0.0.1:8000 --file runexa_business_test_ecommerce_saas.csv --language en --token YOUR_JWT_TOKEN

Requirements:
    pip install requests
"""

import argparse
import json
import sys
from pathlib import Path

import requests


def print_section(title: str) -> None:
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def pretty(data) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2))


def assert_key(data: dict, key: str, errors: list[str]) -> None:
    if key not in data:
        errors.append(f"Missing key: {key}")


def quality_check_analysis(result: dict) -> list[str]:
    errors: list[str] = []

    required_keys = [
        "business_model",
        "confidence_level",
        "executive_summary",
        "business_health_score",
        "kpis",
        "smart_insights",
        "risks",
        "opportunities",
        "recommendations",
        "charts",
        "forecast",
        "data_quality",
        "disclaimer",
    ]

    for key in required_keys:
        assert_key(result, key, errors)

    if not isinstance(result.get("business_health_score"), int):
        errors.append("business_health_score must be an integer.")

    score = result.get("business_health_score", 0)
    if isinstance(score, int) and not (0 <= score <= 100):
        errors.append("business_health_score must be between 0 and 100.")

    kpis = result.get("kpis", {})
    if not isinstance(kpis, dict):
        errors.append("kpis must be an object.")
    else:
        for key in ["revenue", "expenses", "profit", "profit_margin_percent"]:
            if key not in kpis:
                errors.append(f"Missing KPI: {key}")

    charts = result.get("charts", [])
    if not isinstance(charts, list):
        errors.append("charts must be a list.")
    elif len(charts) == 0:
        errors.append("charts is empty. Check parser column_mapping + business_charts integration.")
    else:
        for chart in charts:
            for key in ["type", "title", "x_key", "y_key", "data"]:
                if key not in chart:
                    errors.append(f"Chart missing key: {key}")

    forecast = result.get("forecast", {})
    if not isinstance(forecast, dict):
        errors.append("forecast must be an object.")
    else:
        for key in ["available", "next_month_revenue", "next_quarter_revenue", "trend"]:
            if key not in forecast:
                errors.append(f"Forecast missing key: {key}")

    memory = result.get("business_memory")
    if memory is None:
        errors.append("business_memory missing. Check attach_business_memory integration.")

    decision = (
        result.get("smart_insights", {})
        .get("most_important_decision", {})
    )

    if not decision:
        errors.append("most_important_decision missing.")
    else:
        for key in ["title", "decision", "why", "impact", "timeframe"]:
            if key not in decision:
                errors.append(f"Decision missing key: {key}")

    return errors


def quality_check_report(report: dict) -> list[str]:
    errors: list[str] = []

    required_keys = [
        "title",
        "generated_at",
        "business_model",
        "executive_brief",
        "weekly_summary",
        "business_health_score",
        "kpi_snapshot",
        "forecast_snapshot",
        "memory_summary",
        "top_risks",
        "top_opportunities",
        "priority_actions",
        "ceo_decision",
        "data_limitations",
        "disclaimer",
    ]

    for key in required_keys:
        assert_key(report, key, errors)

    if not isinstance(report.get("kpi_snapshot", {}), dict):
        errors.append("kpi_snapshot must be an object.")

    if not isinstance(report.get("forecast_snapshot", {}), dict):
        errors.append("forecast_snapshot must be an object.")

    if not isinstance(report.get("priority_actions", []), list):
        errors.append("priority_actions must be a list.")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://127.0.0.1:8000")
    parser.add_argument("--file", default="runexa_business_test_ecommerce_saas.csv")
    parser.add_argument("--language", default="en", choices=["en", "fr", "ar"])
    parser.add_argument("--token", required=True)
    args = parser.parse_args()

    base_url = args.base_url.rstrip("/")
    file_path = Path(args.file)

    if not file_path.exists():
        print(f"ERROR: File not found: {file_path}")
        return 1

    headers = {
        "Authorization": f"Bearer {args.token}",
    }

    print_section("1) Health check")
    health = requests.get(f"{base_url}/health", timeout=30)
    print(f"Status: {health.status_code}")
    print(health.text)

    if health.status_code != 200:
        print("Backend is not healthy.")
        return 1

    print_section("2) POST /business/analyze")
    with file_path.open("rb") as f:
        files = {
            "file": (file_path.name, f, "text/csv"),
        }
        data = {
            "output_language": args.language,
        }

        res = requests.post(
            f"{base_url}/business/analyze",
            headers=headers,
            files=files,
            data=data,
            timeout=180,
        )

    print(f"Status: {res.status_code}")

    try:
        analysis = res.json()
    except Exception:
        print(res.text)
        return 1

    pretty(analysis)

    if res.status_code != 200:
        print("Business analysis failed.")
        return 1

    print_section("3) Quality check: analysis")
    analysis_errors = quality_check_analysis(analysis)

    if analysis_errors:
        print("FAILED:")
        for error in analysis_errors:
            print(f"- {error}")
        return 1

    print("PASSED: analysis structure looks good.")

    print_section("4) GET /business/history")
    history_res = requests.get(
        f"{base_url}/business/history",
        headers=headers,
        timeout=60,
    )

    print(f"Status: {history_res.status_code}")

    try:
        history = history_res.json()
    except Exception:
        print(history_res.text)
        return 1

    pretty(history[:2] if isinstance(history, list) else history)

    if history_res.status_code != 200:
        print("History failed.")
        return 1

    if not isinstance(history, list) or len(history) == 0:
        print("History is empty after analysis.")
        return 1

    print_section("5) POST /business/weekly-report")
    report_res = requests.post(
        f"{base_url}/business/weekly-report",
        headers={
            **headers,
            "Content-Type": "application/json",
        },
        json={
            "output_language": args.language,
        },
        timeout=180,
    )

    print(f"Status: {report_res.status_code}")

    try:
        report = report_res.json()
    except Exception:
        print(report_res.text)
        return 1

    pretty(report)

    if report_res.status_code != 200:
        print("Weekly report failed.")
        return 1

    print_section("6) Quality check: weekly report")
    report_errors = quality_check_report(report)

    if report_errors:
        print("FAILED:")
        for error in report_errors:
            print(f"- {error}")
        return 1

    print("PASSED: weekly report structure looks good.")

    print_section("FINAL RESULT")
    print("✅ Backend test completed successfully.")
    print("✅ Business analysis, history, charts, forecast, memory, and weekly report are working.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
