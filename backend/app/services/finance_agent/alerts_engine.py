def generate_financial_alerts(
    transactions: list[dict],
    subscriptions: list[dict],
    forecast: dict,
    scores: dict,
) -> list[dict]:

    alerts = []

    expenses = sum(
        abs(t["amount"])
        for t in transactions
        if t.get("type") == "expense"
    )

    if expenses > 5000:
        alerts.append({
            "type": "warning",
            "severity": "medium",
            "code": "HIGH_EXPENSES",
            "title": "High monthly expenses",
            "message": (
                "Your monthly expenses are relatively high. "
                "Review discretionary spending."
            ),
        })

    overall_score = scores.get(
        "overall_financial_habits_score",
        0,
    )

    if overall_score < 50:
        alerts.append({
            "type": "risk",
            "severity": "high",
            "code": "LOW_FINANCIAL_SCORE",
            "title": "Low financial habits score",
            "message": (
                "Your financial behavior may expose "
                "you to future cashflow issues."
            ),
        })

    cash_risk_days = forecast.get(
        "days_until_cash_risk"
    )

    observed_net_cashflow = float(
        forecast.get("observed_net_cashflow", 0) or 0
    )

    if (
        observed_net_cashflow < 0
        and cash_risk_days is not None
        and cash_risk_days < 30
    ):
        alerts.append({
            "type": "risk",
            "severity": "high",
            "code": "NEGATIVE_CASHFLOW",
            "title": "Cashflow risk detected",
            "message": (
                "Your current spending trend could "
                "lead to cashflow pressure soon."
            ),
        })

    if len(subscriptions) >= 5:
        alerts.append({
            "type": "warning",
            "severity": "medium",
            "code": "TOO_MANY_SUBSCRIPTIONS",
            "title": "Too many subscriptions",
            "message": (
                "You have multiple recurring services. "
                "Consider reducing unused subscriptions."
            ),
        })

    return alerts
