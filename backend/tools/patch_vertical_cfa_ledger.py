from pathlib import Path

p = Path("app/services/finance_agent/transaction_extractor.py")
s = p.read_text(encoding="utf-8")

if "parse_vertical_cfa_debit_credit_statement" in s:
    print("Vertical CFA parser already installed")
    raise SystemExit()

anchor = "def parse_month_name_ledger_transactions"
idx = s.find(anchor)
if idx == -1:
    raise RuntimeError("anchor not found")

parser = r'''

def parse_vertical_cfa_debit_credit_statement(text: str) -> list[dict]:
    """Afrique francophone / CFA vertical column dump parser.

    Handles PDFs where extraction returns all dates, then all descriptions,
    then all value dates, then debit/credit numeric columns.
    Layout: Date | Nature de l’opération | Val | Débit | Crédit.
    """
    import re

    raw = normalize_arabic_digits(str(text or ""))
    low = raw.lower()

    if not (
        ("francs cfa" in low or "fcfa" in low or "xaf" in low or "xof" in low)
        and ("nature de l" in low or "nature de l’opération" in low or "nature de l'operation" in low)
        and "débit" in low
        and "crédit" in low
        and "total" in low
    ):
        return []

    date_re = re.compile(r"^\d{2}/\d{2}/\d{4}$")
    val_re = re.compile(r"^\d{2}/\d{2}$")
    amount_re = re.compile(r"^[+-]?\d{1,3}(?:[.,]\d{3})*$|^[+-]?\d+$")

    lines = [" ".join(x.split()) for x in raw.splitlines() if " ".join(x.split())]

    # Find header zone.
    try:
        header_i = next(i for i, line in enumerate(lines) if "Nature de l" in line and "Débit" in line and "Crédit" in line)
    except StopIteration:
        return []

    body = lines[header_i + 1:]

    # Stop at Total, footer or RIB repeated block.
    stop = len(body)
    for i, line in enumerate(body):
        if line.lower().startswith("total ") or "solde au" in line.lower() or "n.b" in line.lower():
            stop = i
            break
    body = body[:stop]

    dates = []
    descriptions = []
    value_dates = []
    amounts = []

    phase = "dates"

    for line in body:
        if date_re.match(line):
            if phase in {"dates", "descriptions"}:
                dates.append(line)
                phase = "dates"
            else:
                # Ignore accidental full dates after value dates.
                pass
            continue

        if val_re.match(line):
            value_dates.append(line)
            phase = "value_dates"
            continue

        if amount_re.match(line):
            amounts.append(line)
            phase = "amounts"
            continue

        if phase in {"dates", "descriptions"}:
            if not re.search(r"solde initial|rib|iban|swift", line, re.I):
                descriptions.append(line)
                phase = "descriptions"

    # Remove non-transaction initial balance if present.
    if descriptions and re.search(r"solde initial", descriptions[0], re.I):
        descriptions = descriptions[1:]
    if dates and len(dates) > len(descriptions):
        dates = dates[-len(descriptions):]

    n = min(len(dates), len(descriptions))
    if n < 3:
        return []

    # The numeric dump contains debit column then credit column.
    # Use Total line to infer split if available.
    total_re = re.search(
        r"Total\s+(?P<debit>\d{1,3}(?:[.,]\d{3})*)\s+(?P<credit>\d{1,3}(?:[.,]\d{3})*)",
        raw,
        re.I,
    )

    debit_total = credit_total = None
    if total_re:
        debit_total = parse_amount_cfa(total_re.group("debit"))
        credit_total = parse_amount_cfa(total_re.group("credit"))

    parsed_amounts = [parse_amount_cfa(x) for x in amounts]

    best = None
    if debit_total is not None and credit_total is not None:
        for split in range(0, len(parsed_amounts) + 1):
            deb = parsed_amounts[:split]
            cre = parsed_amounts[split:]
            if abs(sum(deb) - debit_total) <= 1 and abs(sum(cre) - credit_total) <= 1:
                best = (deb, cre)
                break

    if best:
        debit_amounts, credit_amounts = best
    else:
        # Fallback: first half debit, second half credit.
        mid = len(parsed_amounts) // 2
        debit_amounts, credit_amounts = parsed_amounts[:mid], parsed_amounts[mid:]

    income_words = ("depot", "dépôt", "verst", "versement", "epargne", "épargne")
    expense_words = ("retrait", "frais", "taxe", "tva", "virement bancaire", "virement par cheque")

    txs = []
    seen = set()
    debit_i = credit_i = 0

    for i in range(n):
        desc = descriptions[i]
        low_desc = desc.lower()
        date = dates[i]
        d, m, y = date.split("/")
        iso = f"{y}-{m}-{d}"

        typ = None
        amount = None

        if any(w in low_desc for w in income_words) and not any(w in low_desc for w in expense_words):
            if credit_i < len(credit_amounts):
                amount = credit_amounts[credit_i]
                credit_i += 1
                typ = "income"
        else:
            if debit_i < len(debit_amounts):
                amount = debit_amounts[debit_i]
                debit_i += 1
                typ = "expense"

        if amount is None or amount <= 0:
            continue

        signed = amount if typ == "income" else -amount
        key = (iso, desc[:100], round(signed, 2))
        if key in seen:
            continue
        seen.add(key)

        txs.append({
            "date": iso,
            "description": clean_db_text(desc[:500]),
            "amount": round(signed, 2),
            "signed_amount": round(signed, 2),
            "type": typ,
            "currency": "XAF",
            "locked_amount": round(signed, 2),
            "_locked_amount": round(signed, 2),
            "locked_type": typ,
            "parser_family": "vertical_cfa_debit_credit",
        })

    if len(txs) < 3:
        return []

    print("VERTICAL_CFA_LEDGER_EXTRACTED", {
        "transactions": len(txs),
        "income_total": round(sum(abs(t["amount"]) for t in txs if t["type"] == "income"), 2),
        "expense_total": round(sum(abs(t["amount"]) for t in txs if t["type"] == "expense"), 2),
    })

    return txs

'''

s = s[:idx] + parser + "\n" + s[idx:]

old = '("credit_mutuel_fr", parse_credit_mutuel_fr_statement, 3),'
new = '("vertical_cfa_debit_credit", parse_vertical_cfa_debit_credit_statement, 3),\n        ("credit_mutuel_fr", parse_credit_mutuel_fr_statement, 3),'
if old in s:
    s = s.replace(old, new, 1)
else:
    print("WARNING: registry anchor not found")

p.write_text(s, encoding="utf-8")
print("Vertical CFA ledger parser installed")
