# tools/test_finance_missing_only.py
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.test_finance_real_reconciliation import test_file

FILES = [
    "ejjami/16.pdf",
    "ejjami/ARABE 4.pdf",
    "ejjami/ARABE1.pdf",
    "ejjami/Relevés compte 3.pdf",
    "ejjami/t12.pdf",
    "ejjami/t13.pdf",
    "ejjami/t38.pdf",
    "ejjami/t44.pdf",
    "ejjami/t51.pdf",
]

for f in FILES:
    r = test_file(Path(f))
    print(
        f"{r.get('status')} {r['file']} | tx={r.get('tx')} "
        f"income={r.get('income')} expenses={r.get('expenses')} "
        f"expected_income={r.get('expected_income')} "
        f"expected_expenses={r.get('expected_expenses')} "
        f"opening={r.get('opening_balance')} ending={r.get('ending_balance')} "
        f"reason={r.get('reason')}"
    )