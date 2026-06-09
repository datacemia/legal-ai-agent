from pathlib import Path

p = Path("app/services/finance_agent/transaction_extractor.py")
s = p.read_text(encoding="utf-8")

MARK = "# === RUNEXA_ANB_ARABE3_V12 ==="
if MARK in s:
    print("ANB ARABE3 V12 already installed")
    raise SystemExit(0)

anchor = "def _v11_missing_layout_candidates(text):"
idx = s.find(anchor)
if idx == -1:
    raise RuntimeError("V11 candidates function not found")

patch = r'''
# === RUNEXA_ANB_ARABE3_V12 ===

def parser_anb_arabe3_v12(text):
    import re

    raw = normalize_arabic_digits(str(text or ""))

    if (
        "البنك العربي الوطني" not in raw
        and "Arab National Bank" not in raw
        and "ANB" not in raw
    ):
        return []

    lines = [" ".join(x.split()) for x in raw.splitlines() if " ".join(x.split())]

    date_re = re.compile(r"^20\d{2}-\d{2}-\d{2}$")
    row_re = re.compile(
        r"(?P<balance>-?\d{1,3}(?:,\d{3})*(?:\.\d{1,2})?)\s+"
        r"(?P<amount>-?\d{1,3}(?:,\d{3})*(?:\.\d{1,2})?)$"
    )

    txs = []
    current_date = None
    current_desc = []
    seen_date_once = False

    for line in lines:
        if line.startswith("Page ") or "تاريخ العملية" in line or "الوصف" in line:
            continue
        if "البنك العربي الوطني –" in line or "خاضع لإشراف" in line:
            continue

        if date_re.match(line):
            if seen_date_once:
                current_date = line
                current_desc = []
                seen_date_once = False
            else:
                current_date = line
                seen_date_once = True
            continue

        m = row_re.search(line)

        if m and current_date:
            balance = parse_amount(m.group("balance"))
            amount = parse_amount(m.group("amount"))

            desc = " ".join(current_desc).strip()
            if not desc:
                desc = line[: m.start()].strip()

            tx = _v11_tx(
                current_date,
                desc,
                amount,
                "SAR",
                "parser_anb_arabe3_v12",
            )

            if tx:
                tx["balance"] = balance
                txs.append(tx)

            current_desc = []
            seen_date_once = False
            continue

        if current_date:
            current_desc.append(line)

    print("ANB_ARABE3_V12_EXTRACTED", {
        "transactions": len(txs),
        "income_total": _v11_totals(txs)[0],
        "expense_total": _v11_totals(txs)[1],
    })

    return txs

# === END_RUNEXA_ANB_ARABE3_V12 ===

'''

s = s[:idx] + patch + "\n" + s[idx:]

old = """    parsers = [
        parser_riyad_arabe1,
        parser_anb_arabe3,
        parser_bank_of_america_credit_card,
        parser_banque_postale_multiline,
        parser_bank_chaabi,
    ]
"""

new = """    parsers = [
        parser_riyad_arabe1,
        parser_anb_arabe3_v12,
        parser_anb_arabe3,
        parser_bank_of_america_credit_card,
        parser_banque_postale_multiline,
        parser_bank_chaabi,
    ]
"""

if old not in s:
    raise RuntimeError("Parser list not found")
s = s.replace(old, new, 1)

p.write_text(s, encoding="utf-8")
print("ANB ARABE3 V12 installed.")
