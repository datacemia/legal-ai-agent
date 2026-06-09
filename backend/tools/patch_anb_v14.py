from pathlib import Path

p = Path("app/services/finance_agent/transaction_extractor.py")
s = p.read_text(encoding="utf-8")

start = s.find("def parser_anb_arabe3_v13(text):")
end = s.find("def _v11_missing_layout_candidates(text):", start)
if start == -1 or end == -1:
    raise RuntimeError("Cannot locate V13 block")

v14 = r'''
def parser_anb_arabe3_v13(text):
    import re

    raw = normalize_arabic_digits(str(text or ""))

    if (
        "البنك العربي الوطني" not in raw
        and "ANB" not in raw
        and "Arab National Bank" not in raw
        and "anb.com.sa" not in raw
    ):
        return []

    lines = [" ".join(x.split()) for x in raw.splitlines() if " ".join(x.split())]

    date_re = re.compile(r"20\d{2}-\d{2}-\d{2}")
    money_pair_re = re.compile(
        r"(?P<balance>-?\d{1,3}(?:,\d{3})*(?:\.\d{1,2})?)\s+"
        r"(?P<amount>-?\d{1,3}(?:,\d{3})*(?:\.\d{1,2})?)(?:\s|$)"
    )

    txs = []
    seen = set()

    for i, line in enumerate(lines):
        m = money_pair_re.search(line)
        if not m:
            continue

        try:
            balance = parse_amount(m.group("balance"))
            amount = parse_amount(m.group("amount"))
        except Exception:
            continue

        if amount == 0:
            continue

        # Exclude summary/header noise.
        if abs(balance) < 100 and abs(amount) < 100:
            continue

        # Find nearest transaction date around this money line.
        date = None
        search_window = lines[max(0, i - 4): min(len(lines), i + 5)]
        joined = " ".join(search_window)
        dates = date_re.findall(joined)
        if dates:
            date = dates[0]
        else:
            continue

        desc_window = lines[max(0, i - 3): i + 1]
        desc = " ".join(desc_window)
        desc = money_pair_re.sub("", desc)
        desc = " ".join(desc.split())[-700:]

        key = (date, round(balance, 2), round(amount, 2))
        if key in seen:
            continue
        seen.add(key)

        tx = _v11_tx(
            date,
            desc,
            amount,
            "SAR",
            "parser_anb_arabe3_v14",
        )

        if tx:
            tx["balance"] = balance
            txs.append(tx)

    print("ANB_ARABE3_V14_EXTRACTED", {
        "transactions": len(txs),
        "income_total": _v11_totals(txs)[0],
        "expense_total": _v11_totals(txs)[1],
    })

    return txs

'''

s = s[:start] + v14 + "\n" + s[end:]
p.write_text(s, encoding="utf-8")
print("ANB V14 installed over V13")
