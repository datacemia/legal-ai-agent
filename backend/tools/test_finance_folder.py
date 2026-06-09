from pathlib import Path
import io
import contextlib
import json
import traceback
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pypdf import PdfReader

from app.services.finance_agent.transaction_extractor import (
    extract_global_statement_summary,
    extract_transactions,
)

ROOT = Path("ejjami")
TOLERANCE = 0.01


def pdf_text(path: Path) -> str:
    reader = PdfReader(str(path))
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def money(v):
    try:
        return round(abs(float(v or 0)), 2)
    except Exception:
        return None


def analyze(path: Path) -> dict:
    text = pdf_text(path)

    captured = io.StringIO()
    with contextlib.redirect_stdout(captured):
        summary = extract_global_statement_summary(text) or {}
        txs = extract_transactions(text) or []

    income = round(
        sum(abs(float(t.get("amount") or 0)) for t in txs if t.get("type") == "income"),
        2,
    )
    expenses = round(
        sum(abs(float(t.get("amount") or 0)) for t in txs if t.get("type") == "expense"),
        2,
    )

    expected_income = money(summary.get("deposits"))
    expected_expenses = money(summary.get("withdrawals"))

    income_gap = None if expected_income is None else round(abs(expected_income - income), 2)
    expense_gap = None if expected_expenses is None else round(abs(expected_expenses - expenses), 2)

    reasons = []
    status = "OK"

    if not txs:
        status = "NO_TRANSACTIONS"
        reasons.append("aucune transaction candidate extraite")

    if expected_income is None and expected_expenses is None:
        if txs:
            status = "NEEDS_PARSER_FIX"
            reasons.append("SUMMARY absent ou incomplet")

    if income_gap is not None and income_gap > TOLERANCE:
        status = "NEEDS_PARSER_FIX"
        reasons.append(f"income_gap={income_gap}")

    if expense_gap is not None and expense_gap > TOLERANCE:
        status = "NEEDS_PARSER_FIX"
        reasons.append(f"expense_gap={expense_gap}")

    if status == "OK":
        reasons.append("SUMMARY → CANDIDATE → RECONCILIATION → KPI cohérents")

    return {
        "file": path.name,
        "status": status,
        "validated": status == "OK",
        "reason": "; ".join(reasons),
        "summary": summary,
        "transactions": len(txs),
        "income_count": sum(1 for t in txs if t.get("type") == "income"),
        "expense_count": sum(1 for t in txs if t.get("type") == "expense"),
        "income_total": income,
        "expense_total": expenses,
        "expected_income": expected_income,
        "expected_expenses": expected_expenses,
        "income_gap": income_gap,
        "expense_gap": expense_gap,
        "logs": [
            line for line in captured.getvalue().splitlines()
            if any(k in line for k in [
                "STATEMENT_SUMMARY_EXTRACTED",
                "FINANCE_CANDIDATE_AUDIT",
                "FINANCE_CANDIDATE_SELECTED",
                "STATEMENT_LAYOUT_DETECTED",
            ])
        ][-20:],
    }


def main():
    files = sorted(ROOT.glob("*.pdf"))
    if not files:
        raise SystemExit(f"No PDF files found in {ROOT.resolve()}")

    results = []

    for path in files:
        try:
            results.append(analyze(path))
        except Exception as e:
            results.append({
                "file": path.name,
                "status": "ERROR",
                "validated": False,
                "reason": str(e),
                "error": str(e),
                "traceback": traceback.format_exc(limit=8),
            })

    total = len(results)
    validated = sum(1 for r in results if r.get("validated") is True)
    not_validated = total - validated

    print(json.dumps(results, ensure_ascii=False, indent=2))

    print("\nSUMMARY")
    print(f"TOTAL={total}")
    print(f"VALIDATED={validated}")
    print(f"NOT_VALIDATED={not_validated}")

    print("\nVALIDATED FILES")
    for r in results:
        if r.get("validated"):
            print(f"OK {r['file']}")

    print("\nNOT VALIDATED FILES")
    for r in results:
        if not r.get("validated"):
            print(f"{r['status']} {r['file']} -> {r.get('reason')}")

    print("\nDETAIL")
    for r in results:
        print(
            f"{r['status']:18} {r['file']} | "
            f"validated={r.get('validated')} "
            f"tx={r.get('transactions')} "
            f"income={r.get('income_total')} "
            f"expenses={r.get('expense_total')} "
            f"expected_income={r.get('expected_income')} "
            f"expected_expenses={r.get('expected_expenses')} "
            f"gap_i={r.get('income_gap')} "
            f"gap_e={r.get('expense_gap')} "
            f"reason={r.get('reason')}"
        )


if __name__ == "__main__":
    main()