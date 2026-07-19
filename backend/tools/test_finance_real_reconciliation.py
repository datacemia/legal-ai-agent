from pathlib import Path
import json
import traceback
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.services.finance_agent.statement_parser import extract_statement_text_from_path
from app.services.finance_agent.transaction_extractor import (
    extract_global_statement_summary,
    extract_transactions,
)

ROOT = Path("ejjami")
TOLERANCE = 0.05
REAL_BALANCE_TOLERANCE = 1.0
SMALL_SUMMARY_GAP_TOLERANCE = 5.0

UNTRUSTED_SOURCES = {
    None,
    "",
    "candidate_inferred",
    "fallback",
    "reconciled_from_candidate",
    "statement_summary_reconciled_from_candidate",
}


def money(v):
    try:
        return round(abs(float(v)), 2)
    except Exception:
        return None


def test_file(path: Path):
    text = extract_statement_text_from_path(str(path))
    text_lower = text.lower()

    summary = extract_global_statement_summary(text) or {}
    txs = extract_transactions(text) or []

    income = round(sum(abs(float(t.get("amount") or 0)) for t in txs if t.get("type") == "income"), 2)
    expenses = round(sum(abs(float(t.get("amount") or 0)) for t in txs if t.get("type") == "expense"), 2)

    expected_income = money(summary.get("deposits"))
    expected_expenses = money(summary.get("withdrawals"))
    opening = money(summary.get("opening_balance"))
    ending = money(summary.get("ending_balance"))
    source = summary.get("source")

    has_txs = len(txs) > 0

    summary_gap_i = None if expected_income is None else round(abs(expected_income - income), 2)
    summary_gap_e = None if expected_expenses is None else round(abs(expected_expenses - expenses), 2)

    audit_tolerance = max(TOLERANCE, REAL_BALANCE_TOLERANCE)

    summary_available = expected_income is not None or expected_expenses is not None
    summary_ok = None
    if summary_available:
        summary_ok = (
            (summary_gap_i is None or summary_gap_i <= audit_tolerance)
            and (summary_gap_e is None or summary_gap_e <= audit_tolerance)
        )

        if summary_gap_i is not None and summary_gap_e is not None:
            if (
                summary_gap_i <= SMALL_SUMMARY_GAP_TOLERANCE
                and summary_gap_e <= SMALL_SUMMARY_GAP_TOLERANCE
            ):
                summary_ok = True

    real_balance_available = (
        opening is not None
        and ending is not None
        and source not in UNTRUSTED_SOURCES
        and not (opening == 0 and ending == 0)
    )

    real_gap = None
    real_ok = None
    if real_balance_available:
        computed_ending = round(opening + income - expenses, 2)
        real_gap = round(abs(computed_ending - ending), 2)
        real_ok = real_gap <= audit_tolerance

    tiny_candidate = (
        has_txs
        and len(txs) <= 10
        and income + expenses < 100
        and (
            "solde crediteur" in text_lower
            or "solde créditeur" in text_lower
            or "date valeur opération débit" in text_lower
            or "date valeur operation debit" in text_lower
        )
    )

    has_adjustments = any(t.get("is_reconciliation_adjustment") for t in txs)

    externally_validated = has_txs and (summary_ok is True or real_ok is True)

    suspicious = not externally_validated
    reasons = []

    if not has_txs:
        reasons.append("NO_TRANSACTIONS")

    if summary_available and summary_ok is False:
        reasons.append(f"SUMMARY_GAP income={summary_gap_i} expense={summary_gap_e}")

    if real_balance_available and real_ok is False:
        reasons.append(f"REAL_BALANCE_GAP={real_gap}")

    if not summary_available and not real_balance_available:
        reasons.append("NO_RELIABLE_REAL_VALUES_FROM_STATEMENT")

    if tiny_candidate:
        suspicious = True
        externally_validated = False
        reasons.append("UNDER_EXTRACTED_BANK_STATEMENT")

    if has_adjustments and not externally_validated:
        suspicious = True
        reasons.append("ADJUSTMENT_WITHOUT_REAL_VALIDATION")

    status = "OK_REAL" if externally_validated and not suspicious else "SUSPICIOUS"

    return {
        "file": path.name,
        "status": status,
        "externally_validated": externally_validated,
        "suspicious": suspicious,
        "tx": len(txs),
        "income": income,
        "expenses": expenses,
        "expected_income": expected_income,
        "expected_expenses": expected_expenses,
        "summary_available": summary_available,
        "summary_ok": summary_ok,
        "summary_gap_i": summary_gap_i,
        "summary_gap_e": summary_gap_e,
        "opening_balance": opening,
        "ending_balance": ending,
        "real_balance_available": real_balance_available,
        "real_ok": real_ok,
        "real_gap": real_gap,
        "tiny_candidate": tiny_candidate,
        "has_adjustments": has_adjustments,
        "summary_source": source,
        "reason": "; ".join(reasons) or "MATCHES_REAL_STATEMENT_VALUES",
    }


def main():
    files = sorted(p for p in ROOT.rglob("*") if p.is_file() and p.suffix.lower() == ".pdf")
    results = []

    for path in files:
        try:
            results.append(test_file(path))
        except Exception as e:
            results.append({
                "file": path.name,
                "status": "ERROR",
                "externally_validated": False,
                "suspicious": True,
                "reason": f"ERROR: {e}",
                "traceback": traceback.format_exc(limit=5),
            })

    ok = sum(1 for r in results if r.get("status") == "OK_REAL")
    suspicious = sum(1 for r in results if r.get("suspicious"))

    print(json.dumps(results, ensure_ascii=False, indent=2))

    print("\nREAL AUDIT SUMMARY")
    print("TOTAL=", len(results))
    print("OK_REAL=", ok)
    print("SUSPICIOUS=", suspicious)

    print("\nOK REAL FILES")
    for r in results:
        if r.get("status") == "OK_REAL":
            print(
                f"OK_REAL {r['file']} | tx={r.get('tx')} "
                f"income={r.get('income')} expenses={r.get('expenses')} "
                f"source={r.get('summary_source')}"
            )

    print("\nSUSPICIOUS FILES")
    for r in results:
        if r.get("suspicious"):
            print(
                f"{r.get('status')} {r['file']} | tx={r.get('tx')} "
                f"income={r.get('income')} expenses={r.get('expenses')} "
                f"expected_income={r.get('expected_income')} "
                f"expected_expenses={r.get('expected_expenses')} "
                f"summary_ok={r.get('summary_ok')} "
                f"real_ok={r.get('real_ok')} "
                f"real_available={r.get('real_balance_available')} "
                f"opening={r.get('opening_balance')} "
                f"ending={r.get('ending_balance')} "
                f"gap={r.get('real_gap')} "
                f"tiny={r.get('tiny_candidate')} "
                f"adjustments={r.get('has_adjustments')} "
                f"source={r.get('summary_source')} "
                f"reason={r.get('reason')}"
            )


if __name__ == "__main__":
    main()
