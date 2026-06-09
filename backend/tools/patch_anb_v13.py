from pathlib import Path

p = Path("app/services/finance_agent/transaction_extractor.py")
s = p.read_text(encoding="utf-8")

if "parser_anb_arabe3_v13" in s:
    print("V13 already installed")
    raise SystemExit()

anchor = "def _v11_missing_layout_candidates(text):"
idx = s.find(anchor)

patch = r'''

def parser_anb_arabe3_v13(text):
    import re

    raw = normalize_arabic_digits(str(text or ""))

    if (
        "البنك العربي الوطني" not in raw
        and "ANB" not in raw
        and "Arab National Bank" not in raw
    ):
        return []

    pattern = re.compile(
        r'(?P<date>20\d{2}-\d{2}-\d{2})\s+'
        r'(?P<balance>-?\d{1,3}(?:,\d{3})*(?:\.\d+)?)\s+'
        r'(?P<amount>-?\d{1,3}(?:,\d{3})*(?:\.\d+)?)',
        re.S
    )

    txs = []

    for m in pattern.finditer(raw):

        try:
            balance = parse_amount(m.group("balance"))
            amount = parse_amount(m.group("amount"))
        except Exception:
            continue

        start = max(0, m.start() - 300)
        desc = raw[start:m.start()]
        desc = " ".join(desc.split())[-400:]

        tx = _v11_tx(
            m.group("date"),
            desc,
            amount,
            "SAR",
            "parser_anb_arabe3_v13"
        )

        if tx:
            tx["balance"] = balance
            txs.append(tx)

    print("ANB_ARABE3_V13_EXTRACTED", {
        "transactions": len(txs),
        "income_total": _v11_totals(txs)[0],
        "expense_total": _v11_totals(txs)[1],
    })

    return txs

'''

s = s[:idx] + patch + s[idx:]

old = "parser_anb_arabe3_v12,"
new = "parser_anb_arabe3_v13,\n        parser_anb_arabe3_v12,"

s = s.replace(old, new)

p.write_text(s, encoding="utf-8")

print("ANB V13 installed")
