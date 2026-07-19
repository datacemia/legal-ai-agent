import re
from app.services.finance_agent.statement_parser import extract_statement_text_from_path
from app.services.finance_agent.transaction_extractor import parse_amount

path = "ejjami/t38.pdf"
text = extract_statement_text_from_path(path)

lines = [" ".join(x.split()) for x in text.splitlines() if " ".join(x.split())]

date_re = re.compile(r"(\d{1,2})\s+([A-Za-z]+)\s+(20\d{2})")
pair_re = re.compile(r"(?P<amount>[+-]?\d+\.\d{2})\s+(?P<balance>[+-]?\d+\.\d{2})")

months = {
    "january": 1, "february": 2, "march": 3, "april": 4,
    "may": 5, "june": 6, "july": 7, "august": 8,
    "september": 9, "october": 10, "november": 11, "december": 12,
}

current_date = None
pending_desc = None
txs = []

for line in lines:
    dm = date_re.search(line)
    if dm:
        current_date = f"{int(dm.group(3)):04d}-{months[dm.group(2).lower()]:02d}-{int(dm.group(1)):02d}"
        pending_desc = line

    pm = pair_re.search(line)
    if pm and current_date:
        amount = parse_amount(pm.group("amount"))
        balance = parse_amount(pm.group("balance"))
        txs.append({
            "date": current_date,
            "description": pending_desc or line,
            "type": "income" if amount > 0 else "expense",
            "amount": round(amount, 2),
            "balance": round(balance, 2),
        })

print("T38_VISUALIZED_TRANSACTIONS")
for tx in txs:
    print(tx)

income = round(sum(tx["amount"] for tx in txs if tx["amount"] > 0), 2)
expenses = round(sum(abs(tx["amount"]) for tx in txs if tx["amount"] < 0), 2)
ending = txs[-1]["balance"] if txs else None

print("T38_VISUALIZED_TOTALS", {
    "transactions": len(txs),
    "income": income,
    "expenses": expenses,
    "net": round(income - expenses, 2),
    "ending_balance": ending,
})
