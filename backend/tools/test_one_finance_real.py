from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.test_finance_real_reconciliation import test_file

if len(sys.argv) < 2:
    raise SystemExit("Usage: python tools/test_one_finance_real.py <pdf_path>")

r = test_file(Path(sys.argv[1]))

print(
    f"{r.get('status')} {r['file']} | "
    f"tx={r.get('tx')} "
    f"income={r.get('income')} expenses={r.get('expenses')} "
    f"expected_income={r.get('expected_income')} "
    f"expected_expenses={r.get('expected_expenses')} "
    f"summary_ok={r.get('summary_ok')} "
    f"real_ok={r.get('real_ok')} "
    f"opening={r.get('opening_balance')} "
    f"ending={r.get('ending_balance')} "
    f"gap={r.get('real_gap')} "
    f"reason={r.get('reason')}"
)
