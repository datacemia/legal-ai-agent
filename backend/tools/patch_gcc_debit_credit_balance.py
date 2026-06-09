from pathlib import Path

p = Path("app/services/finance_agent/transaction_extractor.py")
s = p.read_text(encoding="utf-8")

if "parse_gcc_debit_credit_balance_statement" in s:
    print("GCC debit-credit-balance parser already installed")
    raise SystemExit()

anchor = "def parse_vertical_cfa_debit_credit_statement"
idx = s.find(anchor)
if idx == -1:
    raise RuntimeError("anchor not found")

parser = r'''

def parse_gcc_debit_credit_balance_statement(text: str) -> list[dict]:
    """GCC/UAE bilingual debit-credit-balance ledger parser.

    Layout: Date | Description | Debits | Credits | Balance.
    Handles AED/GCC statements with balances like 24,75 Cr / 0.00Cr.
    """
    import re

    raw = normalize_arabic_digits(str(text or ""))
    low = raw.lower()

    if not (
        ("debits" in low or "débits" in low or "debit" in low or "débit" in low)
        and ("credits" in low or "crédits" in low or "credit" in low or "crédit" in low)
        and ("balance" in low or "équilibre" in low or "equilibre" in low)
        and ("dirham" in low or "aed" in low or "emirates nbd" in low or "uae" in low)
    ):
        return []

    month = {
        "JAN": "01", "FEB": "02", "FÉV": "02", "FEV": "02", "MAR": "03",
        "APR": "04", "AVR": "04", "MAY": "05", "MAI": "05",
        "JUN": "06", "JUIN": "06", "JUL": "07", "AUG": "08", "AOÛ": "08", "AOU": "08",
        "SEP": "09", "OCT": "10", "NOV": "11", "DEC": "12", "DÉC": "12",
    }

    def parse_gcc_date(tok):
        t = normalize_arabic_digits(tok.upper())
        t = t.replace("É", "E").replace("È", "E").replace("Û", "U").replace("Î", "I")
        m = re.match(r"^(\d{2})([A-Z]{3,4})(\d{2})$", t)
        if not m:
            return None
        dd, mon, yy = m.groups()
        mon = month.get(mon[:3])
        if not mon:
            return None
        return f"20{yy}-{mon}-{dd}"

    money_re = re.compile(r"(?<!\d)(\d{1,3}(?:[ ,]\d{3})*(?:[.,]\d{2})|\d+[.,]\d{2})(?:\s*Cr)?(?!\d)", re.I)
    date_re = re.compile(r"^\d{2}[A-Za-zÉÈÊÛÙÎÏÔ]{3,4}\d{2}$", re.I)

    lines = [" ".join(x.split()) for x in raw.splitlines() if " ".join(x.split())]

    txs = []
    current = None
    seen = set()

    def money_amount(tok):
        tok = tok.replace("Cr", "").replace("cr", "").strip()
        return parse_amount(tok)

    def flush():
        nonlocal current
        if not current:
            return

        desc = " ".join(current["parts"]).strip()
        if not desc or re.search(r"report[ée]|brought|statement date|page|détails|details", desc, re.I):
            current = None
            return

        nums = money_re.findall(desc)
        if not nums:
            current = None
            return

        vals = []
        for n in nums:
            try:
                vals.append(money_amount(n))
            except Exception:
                pass

        vals = [v for v in vals if abs(v) > 0]
        if not vals:
            current = None
            return

        # Running-balance layout: usually [... amount, balance].
        # If multiple values, transaction amount is normally penultimate when final is balance.
        amount = vals[-2] if len(vals) >= 2 else vals[-1]

        dlow = desc.lower()
        is_credit = any(x in dlow for x in [
            "de -", "from", "salary", "salaire", "salaires", "transfert bancaire",
            "transfert banknet", "transmission bancaire"
        ]) and not any(x in dlow for x in [
            "à -", "a -", "netflix", "purchase", "achat", "wdl", "dab", "frais", "dr",
            "payment", "paiement"
        ])

        is_expense = any(x in dlow for x in [
            "à -", "a -", "netflix", "purchase", "achat", "wdl", "dab", "frais",
            "payment", "paiement", "dr", "shake n save"
        ])

        if is_credit and not is_expense:
            signed = abs(amount)
            typ = "income"
        elif is_expense:
            signed = -abs(amount)
            typ = "expense"
        else:
            current = None
            return

        key = (current["date"], round(signed, 2), desc[:120])
        if key not in seen:
            seen.add(key)
            txs.append({
                "date": current["date"],
                "description": clean_db_text(desc[:500]),
                "amount": round(signed, 2),
                "signed_amount": round(signed, 2),
                "type": typ,
                "currency": "AED",
                "locked_amount": round(signed, 2),
                "_locked_amount": round(signed, 2),
                "locked_type": typ,
                "parser_family": "gcc_debit_credit_balance",
            })

        current = None

    for line in lines:
        if date_re.match(line):
            flush()
            iso = parse_gcc_date(line)
            if iso:
                current = {"date": iso, "parts": []}
            continue

        if current:
            current["parts"].append(line)

    flush()

    if len(txs) < 2:
        return []

    print("GCC_DEBIT_CREDIT_BALANCE_EXTRACTED", {
        "transactions": len(txs),
        "income_total": round(sum(abs(t["amount"]) for t in txs if t["type"] == "income"), 2),
        "expense_total": round(sum(abs(t["amount"]) for t in txs if t["type"] == "expense"), 2),
    })

    return txs

'''

s = s[:idx] + parser + "\n" + s[idx:]

old = '("vertical_cfa_debit_credit", parse_vertical_cfa_debit_credit_statement, 3),'
new = '("gcc_debit_credit_balance", parse_gcc_debit_credit_balance_statement, 3),\n        ("vertical_cfa_debit_credit", parse_vertical_cfa_debit_credit_statement, 3),'
if old in s:
    s = s.replace(old, new, 1)
else:
    print("WARNING: registry anchor not found")

p.write_text(s, encoding="utf-8")
print("GCC debit-credit-balance parser installed")
