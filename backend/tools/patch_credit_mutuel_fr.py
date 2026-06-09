from pathlib import Path

p = Path("app/services/finance_agent/transaction_extractor.py")
s = p.read_text(encoding="utf-8")

if "parse_credit_mutuel_fr_statement" in s:
    print("Credit Mutuel parser already installed")
    raise SystemExit()

anchor = "def parse_banque_populaire_fr_ar_statement(text: str) -> list[dict]:"
idx = s.find(anchor)
if idx == -1:
    raise RuntimeError("anchor not found")

parser = r'''

def parse_credit_mutuel_fr_statement(text: str) -> list[dict]:
    """Crédit Mutuel / Arkéa FR compact parser: Date | Date valeur | Libellé | Débit/Crédit."""
    import re

    raw = normalize_arabic_digits(str(text or ""))
    low = raw.lower()

    if not (
        ("crédit mutuel" in low or "credit mutuel" in low or "cmb.fr" in low or "cmbrfr" in low)
        and ("relevé de compte" in low or "releve de compte" in low)
        and ("débit" in low or "debit" in low)
        and ("crédit" in low or "credit" in low)
    ):
        return []

    currency = "EUR"

    # Summary is useful for KPI.
    msum = re.search(
        r"TOTAL\s+DES\s+OP[ÉE]RATIONS\s+DU\s+RELEV[ÉE]\s+"
        r"(?P<debit>\d[\d\s.,]*[,.]\d{2})\s+"
        r"(?P<credit>\d[\d\s.,]*[,.]\d{2})",
        raw,
        re.I | re.S,
    )
    if msum:
        print("CREDIT_MUTUEL_FR_SUMMARY_EXTRACTED", {
            "withdrawals": parse_amount(msum.group("debit")),
            "deposits": parse_amount(msum.group("credit")),
        })

    txs = []
    seen = set()

    # Current section decides sign when table columns are lost by pypdf.
    section = None
    section_re = re.compile(
        r"(VIREMENTS\s+RECUS|VIREMENTS\s+EMIS\s+ET\s+PRELEVEMENTS|PAIEMENTS\s+PAR\s+CARTE|RETRAITS|SERVICES\s+ET\s+FRAIS\s+BANCAIRES)",
        re.I,
    )

    # Split compact pypdf text by every operation date pair.
    # Example: 10/0310/03/2023VIR SIACI SAINT HONORE 7,50
    pattern = re.compile(
        r"(?P<opd>\d{2})/(?P<opm>\d{2})\s*(?P<vald>\d{2})/(?P<valm>\d{2})/(?P<valy>\d{4})"
        r"(?P<body>.*?)(?=(?:\d{2}/\d{2}\s*\d{2}/\d{2}/\d{4})|TOTAL\s+DES\s+OP|NOUVEAU\s+SOLDE|$)",
        re.I | re.S,
    )

    money_re = re.compile(r"(?<!\d)(\d{1,3}(?:\s\d{3})*(?:[,.]\d{2})|\d+[,.]\d{2})(?!\d)")

    # Update section positions by scanning raw before each match.
    for m in pattern.finditer(raw):
        prefix = raw[max(0, m.start() - 500):m.start()]
        found_sections = section_re.findall(prefix)
        if found_sections:
            section = found_sections[-1].upper()

        body = " ".join(m.group("body").split())
        if not body:
            continue

        nums = money_re.findall(body)
        if not nums:
            continue

        amount_abs = abs(parse_amount(nums[-1]))
        if amount_abs <= 0 or amount_abs > 1000000:
            continue

        # Exclude summary/subtotal lines accidentally captured.
        if re.search(r"sous-total|ancien solde|nouveau solde|total des op", body, re.I):
            continue

        is_income = False
        if section and "RECUS" in section:
            is_income = True
        if re.search(r"\bVIR\b.*\b(RECU|RECUS)\b|CAF|SALAIRE|SAINT HONORE", body, re.I):
            is_income = True

        signed = amount_abs if is_income else -amount_abs
        typ = "income" if signed > 0 else "expense"

        iso = f"{int(m.group('valy')):04d}-{int(m.group('opm')):02d}-{int(m.group('opd')):02d}"
        key = (iso, round(signed, 2), body[:120])
        if key in seen:
            continue
        seen.add(key)

        txs.append({
            "date": iso,
            "description": clean_db_text(body[:500]),
            "amount": round(signed, 2),
            "signed_amount": round(signed, 2),
            "type": typ,
            "currency": currency,
            "locked_amount": round(signed, 2),
            "_locked_amount": round(signed, 2),
            "locked_type": typ,
            "parser_family": "credit_mutuel_fr",
        })

    if txs:
        print("CREDIT_MUTUEL_FR_EXTRACTED", {
            "transactions": len(txs),
            "income_total": round(sum(abs(t["amount"]) for t in txs if t["type"] == "income"), 2),
            "expense_total": round(sum(abs(t["amount"]) for t in txs if t["type"] == "expense"), 2),
        })

    return txs

'''

s = s[:idx] + parser + "\n" + s[idx:]

# register candidate before Banque Populaire parser if candidate list exists
old = '("banque_populaire_fr_ar", parse_banque_populaire_fr_ar_statement, 3),'
new = '("credit_mutuel_fr", parse_credit_mutuel_fr_statement, 3),\n        ("banque_populaire_fr_ar", parse_banque_populaire_fr_ar_statement, 3),'
if old in s:
    s = s.replace(old, new, 1)
else:
    print("WARNING: candidate registry anchor not found")

p.write_text(s, encoding="utf-8")
print("Credit Mutuel FR parser installed")
