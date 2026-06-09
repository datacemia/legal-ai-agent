#!/usr/bin/env python3
import argparse, contextlib, io, json, sys
from pathlib import Path

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT))

from app.services.finance_agent.transaction_extractor import (
    extract_transactions,
    extract_global_statement_summary,
)

AUDIT_KEYS = [
    "STATEMENT_SUMMARY_EXTRACTED",
    "FINANCE_CANDIDATE_AUDIT",
    "FINANCE_CANDIDATE_SELECTED",
    "RECONCILIATION_CHECK",
    "KPI_AUDIT",
]

def money(v):
    try:
        return round(float(v or 0), 2)
    except Exception:
        return 0.0

def compute(statement_text):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        summary = extract_global_statement_summary(statement_text)
        txs = extract_transactions(statement_text)

    log = buf.getvalue()

    kpi = [
        t for t in txs
        if not t.get("excluded_from_financial_kpis")
        and t.get("type") in {"income", "expense"}
    ]

    income = sum(abs(money(t.get("amount"))) for t in kpi if t.get("type") == "income")
    expense = sum(abs(money(t.get("amount"))) for t in kpi if t.get("type") == "expense")

    return {
        "transaction_count": len(txs),
        "kpi_transaction_count": len(kpi),
        "income_total": round(income, 2),
        "expense_total": round(expense, 2),
        "net_cashflow": round(income - expense, 2),
        "statement_summary": summary or {},
        "audits_present": {k: k in log for k in AUDIT_KEYS},
    }

def compare(actual, expected, tolerance):
    errors = []

    for k in ["transaction_count", "kpi_transaction_count"]:
        if k in expected and actual.get(k) != expected.get(k):
            errors.append(f"{k}: expected {expected.get(k)} got {actual.get(k)}")

    for k in ["income_total", "expense_total", "net_cashflow"]:
        if k in expected and abs(money(actual.get(k)) - money(expected.get(k))) > tolerance:
            errors.append(f"{k}: expected {expected.get(k)} got {actual.get(k)}")

    return errors

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--statement")
    ap.add_argument("--expected")
    ap.add_argument("--update", action="store_true")
    ap.add_argument("--all")
    ap.add_argument("--tolerance", type=float, default=1.0)
    args = ap.parse_args()

    if args.all:
        ok = True
        for expected in sorted(Path(args.all).glob("*.expected.json")):
            statement = expected.with_suffix("").with_suffix(".txt")
            if not statement.exists():
                print("SKIP", statement)
                continue

            actual = compute(statement.read_text(encoding="utf-8", errors="ignore"))
            exp = json.loads(expected.read_text(encoding="utf-8"))
            errors = compare(actual, exp, args.tolerance)

            if errors:
                ok = False
                print("GOLDEN_FAIL", statement)
                for e in errors:
                    print(" -", e)
            else:
                print("GOLDEN_OK", statement)

        raise SystemExit(0 if ok else 1)

    if not args.statement:
        raise SystemExit("Missing --statement")

    statement = Path(args.statement)
    expected = Path(args.expected) if args.expected else statement.with_suffix(".expected.json")

    actual = compute(statement.read_text(encoding="utf-8", errors="ignore"))

    if args.update or not expected.exists():
        expected.write_text(json.dumps(actual, ensure_ascii=False, indent=2), encoding="utf-8")
        print("GOLDEN_WRITTEN", expected)
        return

    exp = json.loads(expected.read_text(encoding="utf-8"))
    errors = compare(actual, exp, args.tolerance)

    print(json.dumps(actual, ensure_ascii=False, indent=2))

    if errors:
        print("GOLDEN_FAIL")
        for e in errors:
            print(" -", e)
        raise SystemExit(1)

    print("GOLDEN_OK")

if __name__ == "__main__":
    main()
