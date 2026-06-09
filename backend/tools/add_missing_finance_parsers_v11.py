from pathlib import Path

p = Path("app/services/finance_agent/transaction_extractor.py")
s = p.read_text(encoding="utf-8")

MARK = "# === RUNEXA_MISSING_LAYOUTS_V11 ==="
if MARK in s:
    print("V11 already installed")
    raise SystemExit(0)

insert_before = "\ndef extract_transactions(text: str) -> list[dict]:\n"
idx = s.rfind(insert_before)
if idx == -1:
    raise RuntimeError("Final extract_transactions wrapper not found")

patch = r'''
# === RUNEXA_MISSING_LAYOUTS_V11 ===

def _v11_tx(date, desc, amount, currency="unknown", parser="v11"):
    amount = round(float(amount or 0), 2)
    if amount == 0:
        return None
    typ = "income" if amount > 0 else "expense"
    return {
        "date": str(date),
        "description": str(desc or "").strip()[:900],
        "amount": amount,
        "signed_amount": amount,
        "locked_amount": amount,
        "_locked_amount": amount,
        "type": typ,
        "locked_type": typ,
        "currency": currency,
        "parser_family": parser,
        "excluded_from_financial_kpis": False,
    }

def _v11_totals(txs):
    inc = round(sum(float(t.get("amount") or 0) for t in txs if t.get("type") == "income"), 2)
    exp = round(sum(abs(float(t.get("amount") or 0)) for t in txs if t.get("type") == "expense"), 2)
    return inc, exp

def parser_riyad_arabe1(text):
    import re
    raw = normalize_arabic_digits(str(text or ""))
    if "Total Deposits" not in raw or "Total Withdrawals" not in raw:
        return []
    lines = [" ".join(x.split()) for x in raw.splitlines() if " ".join(x.split())]
    triple = re.compile(r"(\d{1,3}(?:,\d{3})*\.\d{2})\s*SAR\s+(\d{1,3}(?:,\d{3})*\.\d{2})\s*SAR\s+(\d{1,3}(?:,\d{3})*\.\d{2})\s*SAR")
    date_re = re.compile(r"(20\d{2})[/-](\d{2})[/-](\d{2})")
    txs, pending, desc = [], None, []
    for line in lines:
        m = triple.search(line)
        if m:
            pending = (parse_amount(m.group(1)), parse_amount(m.group(2)), parse_amount(m.group(3)))
            desc = []
            continue
        if pending:
            d = date_re.search(line)
            if d:
                balance, credit, debit = pending
                amount = credit if credit > 0 else -debit
                tx = _v11_tx(f"{d.group(1)}-{d.group(2)}-{d.group(3)}", " ".join(desc), amount, "SAR", "parser_riyad_arabe1")
                if tx: tx["balance"] = balance; txs.append(tx)
                pending = None
            else:
                desc.append(line)
    return txs

def parser_anb_arabe3(text):
    import re
    raw = normalize_arabic_digits(str(text or ""))
    if "البنك العربي الوطني" not in raw and "Arab National Bank" not in raw:
        return []
    date_pair = re.compile(r"(20\d{2}-\d{2}-\d{2})\s*\n\s*(20\d{2}-\d{2}-\d{2})")
    starts = list(date_pair.finditer(raw))
    txs = []
    for i, m in enumerate(starts):
        date = m.group(1)
        block = raw[m.end():(starts[i+1].start() if i+1 < len(starts) else len(raw))]
        nums = re.findall(r"[-+]?\d{1,3}(?:,\d{3})*(?:\.\d+)?|[-+]?\d+(?:\.\d+)?", block)
        signed = [parse_amount(x) for x in nums if str(x).startswith(("-", "+"))]
        if signed:
            amount = signed[-1]
        elif len(nums) >= 2:
            amount = parse_amount(nums[-1])
        else:
            continue
        tx = _v11_tx(date, " ".join(block.split()), amount, "SAR", "parser_anb_arabe3")
        if tx: txs.append(tx)
    return txs

def parser_bank_of_america_credit_card(text):
    import re
    raw = str(text or "")
    if "Bank of America" not in raw or "Purchases and Adjustments" not in raw:
        return []
    year = detect_document_year(raw)
    txs, section = [], None
    line_re = re.compile(r"^(\d{2}/\d{2})\s+(\d{2}/\d{2})\s+(.+?)\s+(-?\d+(?:,\d{3})*\.\d{2})$")
    for line in [" ".join(x.split()) for x in raw.splitlines()]:
        low = line.lower()
        if "payments and other credits" in low: section = "credit"; continue
        if "purchases and adjustments" in low: section = "debit"; continue
        if "total " in low or "interest charged" in low or "fees charged" in low: section = None
        m = line_re.match(line)
        if m and section:
            mm, dd = m.group(2).split("/")
            amt = abs(parse_amount(m.group(4)))
            tx = _v11_tx(f"{year}-{mm}-{dd}", m.group(3), amt if section == "credit" else -amt, "USD", "parser_bank_of_america_credit_card")
            if tx: txs.append(tx)
    return txs

def parser_banque_postale_multiline(text):
    import re
    raw = str(text or "")
    if "BANQUE POSTALE" not in raw.upper():
        return []
    year = detect_document_year(raw)
    lines = [" ".join(x.replace("¤", " ").split()) for x in raw.splitlines() if " ".join(x.split())]
    date_re = re.compile(r"^(\d{2})/(\d{2})\s+(.+)")
    money_re = re.compile(r"\b\d{1,3}(?:[ .]\d{3})*,\d{2}\b|\b\d+,\d{2}\b")
    blocks, cur = [], []
    for line in lines:
        if date_re.match(line) and not line.lower().startswith("date opérations"):
            if cur: blocks.append(cur)
            cur = [line]
        elif cur:
            cur.append(line)
    if cur: blocks.append(cur)

    credit_words = ["virement de", "remboursement", "versement", "caf de", "cpam", "salaire"]
    debit_words = ["achat cb", "retrait", "prelevement", "prélèvement", "virement pour", "frais", "cotisation"]
    txs = []
    for b in blocks:
        m = date_re.match(b[0])
        if not m: continue
        textb = " ".join(b)
        low = textb.lower()
        if "ancien solde" in low or "nouveau solde" in low: continue
        vals = money_re.findall(textb)
        if not vals: continue
        amount = abs(parse_amount(vals[-1]))
        is_credit = any(w in low for w in credit_words) and "virement pour" not in low
        is_debit = any(w in low for w in debit_words)
        signed = amount if is_credit and not is_debit else -amount
        tx = _v11_tx(f"{year}-{m.group(2)}-{m.group(1)}", textb, signed, "EUR", "parser_banque_postale_multiline")
        if tx: txs.append(tx)
    return txs

def parser_bank_chaabi(text):
    # Safe generic Moroccan/French fallback: only transaction-like dated rows.
    import re
    raw = str(text or "")
    if "CHAABI" not in raw.upper() and "BANQUE POPULAIRE" not in raw.upper():
        return []
    year = detect_document_year(raw)
    txs = []
    line_re = re.compile(r"^(\d{2})[/-](\d{2})(?:[/-]\d{2,4})?\s+(.+?)\s+([-+]?\d+(?:[ .]\d{3})*[,.]\d{2})$")
    for line in [" ".join(x.split()) for x in raw.splitlines()]:
        m = line_re.match(line)
        if not m: continue
        desc = m.group(3)
        amount = parse_amount(m.group(4))
        low = desc.lower()
        if amount > 0 and any(w in low for w in ["achat", "retrait", "frais", "commission", "prelev", "prélèv"]):
            amount = -abs(amount)
        tx = _v11_tx(f"{year}-{m.group(2)}-{m.group(1)}", desc, amount, "MAD", "parser_bank_chaabi")
        if tx: txs.append(tx)
    return txs

def _v11_missing_layout_candidates(text):
    parsers = [
        parser_riyad_arabe1,
        parser_anb_arabe3,
        parser_bank_of_america_credit_card,
        parser_banque_postale_multiline,
        parser_bank_chaabi,
    ]
    best = []
    audit = []
    for fn in parsers:
        try:
            txs = _runexa_clean_txs(fn(text) or [])
        except Exception as e:
            print("V11_PARSER_ERROR", fn.__name__, str(e))
            txs = []
        inc, exp = _v11_totals(txs)
        audit.append({"parser": fn.__name__, "count": len(txs), "income_total": inc, "expense_total": exp})
        if len(txs) > len(best):
            best = txs
    print("V11_CANDIDATE_AUDIT", audit)
    return best

# === END_RUNEXA_MISSING_LAYOUTS_V11 ===

'''

s = s[:idx] + "\n" + patch + s[idx:]

old = '''def extract_transactions(text: str) -> list[dict]:
    txs = _RUNEXA_ORIGINAL_EXTRACT_TRANSACTIONS(text) or []
    return _runexa_clean_txs(txs)
'''

new = '''def extract_transactions(text: str) -> list[dict]:
    txs = _runexa_clean_txs(_RUNEXA_ORIGINAL_EXTRACT_TRANSACTIONS(text) or [])
    if txs:
        return txs
    fallback = _v11_missing_layout_candidates(text)
    if fallback:
        inc, exp = _v11_totals(fallback)
        print("STATEMENT_LAYOUT_DETECTED", fallback[0].get("parser_family"))
        print("FINANCE_CANDIDATE_SELECTED", {
            "parser": fallback[0].get("parser_family"),
            "transactions": len(fallback),
            "income_total": inc,
            "expense_total": exp,
            "score": 0.0,
        })
        return fallback
    return []
'''

if old not in s:
    raise RuntimeError("Expected final extract_transactions body not found")
s = s.replace(old, new, 1)

old2 = "txs = _runexa_clean_txs(_RUNEXA_ORIGINAL_EXTRACT_TRANSACTIONS(text) or [])"
new2 = "txs = _runexa_clean_txs(_RUNEXA_ORIGINAL_EXTRACT_TRANSACTIONS(text) or []) or _v11_missing_layout_candidates(text)"
s = s.replace(old2, new2, 1)

p.write_text(s, encoding="utf-8")
print("V11 missing parsers installed.")
