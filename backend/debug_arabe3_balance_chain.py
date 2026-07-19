
from pathlib import Path
import io
import contextlib
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

from tools.test_finance_folder import pdf_text
from app.services.finance_agent.transaction_extractor import extract_transactions

text = pdf_text(Path("ejjami/ARABE3.pdf"))

buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    txs = extract_transactions(text)

txs = [t for t in txs if t.get("balance") is not None]

print("tx_with_balance =", len(txs))

for i in range(len(txs) - 1):
    a = txs[i]
    b = txs[i + 1]

    bal_a = round(float(a["balance"]), 2)
    bal_b = round(float(b["balance"]), 2)
    amt_b = round(float(b["amount"]), 2)

    expected_b = round(bal_a + amt_b, 2)
    delta = round(bal_b - expected_b, 2)

    if abs(delta) > 0.01:
        print()
        print("BREAK", i, "delta", delta)
        print("A", a.get("date"), a.get("amount"), a.get("balance"), (a.get("description") or "")[:150])
        print("B", b.get("date"), b.get("amount"), b.get("balance"), (b.get("description") or "")[:150])
