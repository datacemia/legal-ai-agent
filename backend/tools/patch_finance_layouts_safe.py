from pathlib import Path

p = Path("app/services/finance_agent/transaction_extractor.py")
s = p.read_text(encoding="utf-8")

MARK = "# === RUNEXA_SAFE_LAYOUT_PATCH_V10 ==="
if MARK in s:
    print("Patch already installed")
    raise SystemExit(0)

patch = r'''

# === RUNEXA_SAFE_LAYOUT_PATCH_V10 ===
# Additive fallback parsers only.
# Principle: SUMMARY -> CANDIDATE -> RECONCILIATION -> KPI coherent.
# Existing extractors remain authoritative when they already return transactions.

def _runexa_safe_tx(
    *,
    date,
    description,
    amount,
    currency="unknown",
    parser_family="safe_layout_patch_v10",
    balance=None,
):
    amount = round(float(amount or 0), 2)
    if amount == 0:
        return None

    typ = "income" if amount > 0 else "expense"

    tx = {
        "date": str(date),
        "description": str(description or "").strip()[:700],
        "amount": amount,
        "signed_amount": amount,
        "locked_amount": amount,
        "_locked_amount": amount,
        "locked_type": typ,
        "type": typ,
        "currency": currency,
        "parser_family": parser_family,
        "_balance_locked": True,
    }

    if balance is not None:
        try:
            tx["balance"] = round(float(balance), 2)
        except Exception:
            pass

    return tx


def _runexa_money_tokens(text):
    import re
    return re.findall(
        r"[-+]?\d{1,3}(?:[,\s]\d{3})*(?:[.,]\d{1,2})|[-+]?\d+(?:[.,]\d{1,2})?",
        str(text or ""),
    )


def _runexa_tx_totals(transactions):
    income = round(sum(float(t.get("amount") or 0) for t in transactions if t.get("type") == "income"), 2)
    expense = round(sum(abs(float(t.get("amount") or 0)) for t in transactions if t.get("type") == "expense"), 2)
    return income, expense


def _runexa_summary_is_strong(summary):
    if not isinstance(summary, dict) or not summary:
        return False

    has_movements = (
        float(summary.get("deposits") or 0) > 0
        or float(summary.get("withdrawals") or 0) > 0
    )
    has_balances = (
        summary.get("opening_balance") is not None
        or summary.get("ending_balance") is not None
    )

    return has_movements and has_balances


def _runexa_reconciled_candidate(transactions, summary=None, tolerance=0.05):
    transactions = [t for t in transactions or [] if isinstance(t, dict) and t.get("amount")]
    if not transactions:
        return []

    income, expense = _runexa_tx_totals(transactions)

    if _runexa_summary_is_strong(summary):
        expected_income = round(float(summary.get("deposits") or 0), 2)
        expected_expense = round(float(summary.get("withdrawals") or 0), 2)

        income_gap = round(abs(income - expected_income), 2)
        expense_gap = round(abs(expense - expected_expense), 2)

        if income_gap <= tolerance and expense_gap <= tolerance:
            print("RUNEXA_SAFE_LAYOUT_RECONCILED", {
                "transactions": len(transactions),
                "income_total": income,
                "expense_total": expense,
                "expected_income": expected_income,
                "expected_expenses": expected_expense,
                "income_gap": income_gap,
                "expense_gap": expense_gap,
            })
            return transactions

        print("RUNEXA_SAFE_LAYOUT_REJECTED_BY_RECONCILIATION", {
            "transactions": len(transactions),
            "income_total": income,
            "expense_total": expense,
            "expected_income": expected_income,
            "expected_expenses": expected_expense,
            "income_gap": income_gap,
            "expense_gap": expense_gap,
        })
        return []

    # Weak/no summary: accept only structurally locked candidates.
    if len(transactions) >= 2:
        print("RUNEXA_SAFE_LAYOUT_ACCEPTED_WITH_WEAK_SUMMARY", {
            "transactions": len(transactions),
            "income_total": income,
            "expense_total": expense,
        })
        return transactions

    return []


def extract_riyad_balance_credit_debit_v10(text):
    import re

    raw = normalize_arabic_digits(str(text or ""))
    if "Total Deposits" not in raw and "الإيداعات إجمالي" not in raw:
        return []

    lines = [" ".join(x.split()) for x in raw.splitlines() if " ".join(x.split())]
    txs = []
    pending = None
    desc = []

    triple_re = re.compile(
        r"(?P<balance>\d{1,3}(?:,\d{3})*(?:\.\d{2}))\s*SAR\s+"
        r"(?P<credit>\d{1,3}(?:,\d{3})*(?:\.\d{2}))\s*SAR\s+"
        r"(?P<debit>\d{1,3}(?:,\d{3})*(?:\.\d{2}))\s*SAR",
        re.I,
    )
    date_re = re.compile(r"\b(20\d{2})[/-](\d{2})[/-](\d{2})\b")

    for line in lines:
        m = triple_re.search(line)
        if m:
            pending = {
                "balance": parse_amount(m.group("balance")),
                "credit": parse_amount(m.group("credit")),
                "debit": parse_amount(m.group("debit")),
            }
            desc = []
            continue

        if pending:
            dm = date_re.search(line)
            if dm:
                amount = pending["credit"] if pending["credit"] > 0 else -pending["debit"]
                tx = _runexa_safe_tx(
                    date=f"{dm.group(1)}-{dm.group(2)}-{dm.group(3)}",
                    description=" ".join(desc) or line,
                    amount=amount,
                    currency="SAR",
                    parser_family="riyad_balance_credit_debit_v10",
                    balance=pending["balance"],
                )
                if tx:
                    txs.append(tx)
                pending = None
                desc = []
            else:
                desc.append(line)

    print("RIYAD_BALANCE_CREDIT_DEBIT_V10_EXTRACTED", {
        "transactions": len(txs),
        "income_total": _runexa_tx_totals(txs)[0],
        "expense_total": _runexa_tx_totals(txs)[1],
    })
    return txs


def extract_anb_signed_balance_v10(text):
    import re

    raw = normalize_arabic_digits(str(text or ""))
    if "البنك العربي الوطني" not in raw and "Arab National Bank" not in raw and "ANB" not in raw:
        return []

    flat = re.sub(r"\r", "\n", raw)
    date_pair = re.compile(r"(20\d{2}-\d{2}-\d{2})\s*\n\s*(20\d{2}-\d{2}-\d{2})")
    starts = list(date_pair.finditer(flat))
    txs = []

    for i, m in enumerate(starts):
        date = m.group(1)
        start = m.end()
        end = starts[i + 1].start() if i + 1 < len(starts) else len(flat)
        block = flat[start:end].strip()
        if not block:
            continue

        nums = _runexa_money_tokens(block)
        if len(nums) < 2:
            continue

        signed = []
        for tok in nums:
            st = str(tok).strip()
            if st.startswith("+") or st.startswith("-"):
                try:
                    signed.append(parse_amount(st))
                except Exception:
                    pass

        amount = None
        balance = None

        if signed:
            amount = signed[-1]
            # Balance is usually the last unsigned big number near the end.
            try:
                last_num = parse_amount(nums[-1])
                if round(last_num, 2) != round(amount, 2):
                    balance = last_num
            except Exception:
                balance = None
        else:
            try:
                # ANB OCR row usually ends as: balance amount
                balance = parse_amount(nums[-2])
                amount = parse_amount(nums[-1])
            except Exception:
                continue

        if amount is None or amount == 0:
            continue

        desc = re.sub(r"\s+", " ", block)
        tx = _runexa_safe_tx(
            date=date,
            description=desc,
            amount=amount,
            currency="SAR",
            parser_family="anb_signed_balance_v10",
            balance=balance,
        )
        if tx:
            txs.append(tx)

    print("ANB_SIGNED_BALANCE_V10_EXTRACTED", {
        "transactions": len(txs),
        "income_total": _runexa_tx_totals(txs)[0],
        "expense_total": _runexa_tx_totals(txs)[1],
    })
    return txs


def extract_bank_of_america_credit_card_v10(text):
    import re

    raw = str(text or "")
    if "Bank of America" not in raw or "Purchases and Adjustments" not in raw:
        return []

    year = detect_document_year(raw)
    txs = []
    section = None

    line_re = re.compile(
        r"^(?P<tdate>\d{2}/\d{2})\s+(?P<pdate>\d{2}/\d{2})\s+"
        r"(?P<desc>.+?)\s+(?P<amount>-?\d{1,3}(?:,\d{3})*(?:\.\d{2})|-?\d+\.\d{2})$"
    )

    for raw_line in raw.splitlines():
        line = " ".join(raw_line.split())
        low = line.lower()

        if "total payments and other credits" in low:
            section = None
            continue
        if "total purchases and adjustments" in low:
            section = None
            continue
        if "interest charged" in low:
            section = None
            continue
        if "payments and other credits" in low:
            section = "payment"
            continue
        if "purchases and adjustments" in low:
            section = "purchase"
            continue

        m = line_re.match(line)
        if not m or section not in {"payment", "purchase"}:
            continue

        amount_abs = abs(parse_amount(m.group("amount")))
        amount = amount_abs if section == "payment" else -amount_abs

        mm, dd = m.group("pdate").split("/")
        tx = _runexa_safe_tx(
            date=f"{year}-{mm}-{dd}",
            description=m.group("desc"),
            amount=amount,
            currency="USD",
            parser_family="bank_of_america_credit_card_v10",
        )
        if tx:
            txs.append(tx)

    print("BOA_CREDIT_CARD_V10_EXTRACTED", {
        "transactions": len(txs),
        "income_total": _runexa_tx_totals(txs)[0],
        "expense_total": _runexa_tx_totals(txs)[1],
    })
    return txs


def extract_banque_postale_multiline_v10(text):
    import re

    raw = str(text or "")
    if "LA BANQUE POSTALE" not in raw.upper() and "La Banque Postale" not in raw:
        return []

    year = None
    ym = re.search(r"Relevé édité le\s+\d{1,2}\s+\w+\s+(20\d{2})", raw, re.I)
    if ym:
        year = int(ym.group(1))
    else:
        year = detect_document_year(raw)

    lines = [" ".join(x.replace("¤", " ").split()) for x in raw.splitlines() if " ".join(x.split())]
    date_re = re.compile(r"^(?P<date>\d{2}/\d{2})\s+(?P<rest>.+)")
    money_line_re = re.compile(r"^\d{1,3}(?:[ .]\d{3})*,\d{2}$|^\d+,\d{2}$")

    blocks = []
    current = []

    for line in lines:
        if date_re.match(line) and not line.lower().startswith(("date opérations", "date operations")):
            if current:
                blocks.append(current)
            current = [line]
        elif current:
            current.append(line)

    if current:
        blocks.append(current)

    txs = []

    credit_markers = [
        "virement de",
        "remboursement",
        "versement",
        "crédit",
        "credit",
        "cpam",
        "caf de",
        "salaire",
    ]
    debit_markers = [
        "achat cb",
        "retrait",
        "prelevement",
        "prélèvement",
        "virement pour",
        "frais",
        "cotisation",
        "carte",
    ]

    for block in blocks:
        first = block[0]
        m = date_re.match(first)
        if not m:
            continue

        date_part = m.group("date")
        desc_text = " ".join(block)
        low = desc_text.lower()

        if "ancien solde" in low or "nouveau solde" in low or "solde au" in low:
            continue

        money_candidates = []
        for line in block:
            clean = line.strip()
            if money_line_re.fullmatch(clean):
                money_candidates.append(clean)

        if not money_candidates:
            # fallback: last comma money in block
            found = re.findall(r"\b\d{1,3}(?:[ .]\d{3})*,\d{2}\b|\b\d+,\d{2}\b", desc_text)
            money_candidates = found[-1:]

        if not money_candidates:
            continue

        amount_abs = abs(parse_amount(money_candidates[-1]))

        is_credit = any(k in low for k in credit_markers) and not any(k in low for k in ["virement pour"])
        is_debit = any(k in low for k in debit_markers)

        if is_credit and not is_debit:
            amount = amount_abs
        else:
            amount = -amount_abs

        dd, mm = date_part.split("/")
        tx = _runexa_safe_tx(
            date=f"{year}-{mm}-{dd}",
            description=desc_text,
            amount=amount,
            currency="EUR",
            parser_family="banque_postale_multiline_v10",
        )
        if tx:
            txs.append(tx)

    print("BANQUE_POSTALE_MULTILINE_V10_EXTRACTED", {
        "transactions": len(txs),
        "income_total": _runexa_tx_totals(txs)[0],
        "expense_total": _runexa_tx_totals(txs)[1],
    })
    return txs


_RUNEXA_ORIGINAL_EXTRACT_TRANSACTIONS = extract_transactions
_RUNEXA_ORIGINAL_EXTRACT_GLOBAL_STATEMENT_SUMMARY = extract_global_statement_summary


def extract_transactions(text):
    original = _RUNEXA_ORIGINAL_EXTRACT_TRANSACTIONS(text)

    if original:
        return original

    summary = _RUNEXA_ORIGINAL_EXTRACT_GLOBAL_STATEMENT_SUMMARY(text)

    candidates = [
        ("riyad_balance_credit_debit_v10", extract_riyad_balance_credit_debit_v10(text)),
        ("anb_signed_balance_v10", extract_anb_signed_balance_v10(text)),
        ("bank_of_america_credit_card_v10", extract_bank_of_america_credit_card_v10(text)),
        ("banque_postale_multiline_v10", extract_banque_postale_multiline_v10(text)),
    ]

    audit = []
    for name, txs in candidates:
        income, expense = _runexa_tx_totals(txs)
        audit.append({
            "parser": name,
            "count": len(txs or []),
            "income_total": income,
            "expense_total": expense,
        })

    print("RUNEXA_SAFE_LAYOUT_CANDIDATE_AUDIT", audit)

    best = []
    best_name = None

    for name, txs in candidates:
        selected = _runexa_reconciled_candidate(txs, summary)
        if len(selected) > len(best):
            best = selected
            best_name = name

    if best:
        print("STATEMENT_LAYOUT_DETECTED", best_name)
        print("FINANCE_CANDIDATE_SELECTED", {
            "parser": best_name,
            "transactions": len(best),
            "income_total": _runexa_tx_totals(best)[0],
            "expense_total": _runexa_tx_totals(best)[1],
            "score": 0.0,
        })
        return best

    return original


def extract_global_statement_summary(text):
    summary = _RUNEXA_ORIGINAL_EXTRACT_GLOBAL_STATEMENT_SUMMARY(text)

    # Banque Postale sometimes has no reliable official movement total in OCR.
    # If original summary is weak, derive movement totals from the trusted multiline candidate.
    raw = str(text or "")
    if ("LA BANQUE POSTALE" in raw.upper() or "La Banque Postale" in raw) and not _runexa_summary_is_strong(summary):
        txs = extract_banque_postale_multiline_v10(text)
        if txs:
            income, expense = _runexa_tx_totals(txs)
            derived = dict(summary or {})
            derived["deposits"] = income
            derived["withdrawals"] = expense
            if "opening_balance" not in derived:
                derived["opening_balance"] = 0.0
            if "ending_balance" not in derived:
                derived["ending_balance"] = round(income - expense, 2)

            print("BANQUE_POSTALE_DERIVED_MOVEMENT_SUMMARY", derived)
            print("STATEMENT_SUMMARY_EXTRACTED", derived)
            return derived

    return summary

# === END_RUNEXA_SAFE_LAYOUT_PATCH_V10 ===
'''

p.write_text(s + patch, encoding="utf-8")
print("Patch installed in", p)
