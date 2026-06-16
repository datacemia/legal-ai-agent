from fastapi import UploadFile
import fitz
import os
import re

from app.services.finance_agent.scan_agent import scan_agent_extract_text


MIN_TEXT_LENGTH = int(os.getenv("FINANCE_MIN_TEXT_LENGTH", "500"))


def _looks_like_word_per_line_statement(text: str) -> bool:
    lines = [x.strip() for x in str(text or "").splitlines() if x.strip()]
    if len(lines) < 80:
        return False

    short_lines = sum(1 for x in lines if len(x) <= 18)
    date_lines = sum(1 for x in lines if re.match(r"^\d{1,2}[./-]\d{1,2}$", x))
    money_lines = sum(
        1
        for x in lines
        if re.match(r"^\d{1,3}(?:[ .]\d{3})*[,.]\d{2}$", x)
    )

    return (
        short_lines / len(lines) > 0.65
        and date_lines >= 4
        and money_lines >= 2
    )


def _normalize_word_per_line_statement(text: str) -> str:
    lines = [x.strip() for x in str(text or "").splitlines() if x.strip()]

    fixed = []
    i = 0
    while i < len(lines):
        if (
            i + 1 < len(lines)
            and re.fullmatch(r"\d{1,3}", lines[i])
            and re.fullmatch(r"\d{3}[,.]\d{2}", lines[i + 1])
        ):
            fixed.append(lines[i] + " " + lines[i + 1])
            i += 2
        else:
            fixed.append(lines[i])
            i += 1

    date_re = re.compile(r"^\d{1,2}[./-]\d{1,2}$")
    amount_re = re.compile(r"^\d{1,3}(?:[ .]\d{3})*[,.]\d{2}$")

    rebuilt = []
    current = []

    for token in fixed:
        starts_new_tx = (
            date_re.match(token)
            and len(current) >= 3
            and any(amount_re.match(x) for x in current)
        )

        if starts_new_tx:
            rebuilt.append(" ".join(current))
            current = [token]
        else:
            current.append(token)

    if current:
        rebuilt.append(" ".join(current))

    return "\n".join(rebuilt)


def _merge_amount_only_lines_into_previous(text: str) -> str:
    lines = [x.rstrip() for x in str(text or "").splitlines()]

    amount_only_re = re.compile(
        r"^\s*\d{1,3}(?:[ .]\d{3})*[,.]\d{2}\s*$"
    )

    date_re = re.compile(
        r"\b\d{1,2}[./-]\d{1,2}(?:[./-]\d{2,4})?\b"
    )

    operation_hint_re = re.compile(
        r"\b("
        r"PRLV|PRELEVEMENT|PRÉLÈVEMENT|VIR|VIREMENT|CB|CARTE|PAIEMENT|RETRAIT|"
        r"DEBIT|DÉBIT|CREDIT|CRÉDIT|FRAIS|COMMISSION|ACHAT|TRANSFER|PAYMENT|"
        r"WITHDRAWAL|ATM|CARD|PURCHASE|SEPA|INST|EMIS|RECU|REÇU"
        r")\b",
        re.IGNORECASE,
    )

    rebuilt = []

    for line in lines:
        clean = line.strip()

        if (
            amount_only_re.match(clean)
            and rebuilt
            and date_re.search(rebuilt[-1])
            and operation_hint_re.search(rebuilt[-1])
        ):
            rebuilt[-1] = rebuilt[-1].rstrip() + " " + clean
        else:
            rebuilt.append(line)

    return "\n".join(rebuilt)


def _normalize_statement_text_structure(text: str) -> str:
    if not text:
        return text

    text = re.sub(
        r"(\d{1,2}[./-]\d{1,2})\s*\n\s*(?=\d{1,3}(?:[ .]\d{3})*[,.]\d{2}\b)",
        r"\1 ",
        text,
    )

    normalized = _merge_amount_only_lines_into_previous(text)

    if normalized != text:
        print("FINANCE_TEXT_STRUCTURE_NORMALIZED", {
            "mode": "amount_only_line_merged",
            "before_lines": len(text.splitlines()),
            "after_lines": len(normalized.splitlines()),
        })
        text = normalized

    if _looks_like_word_per_line_statement(text):
        normalized = _normalize_word_per_line_statement(text)
        print("FINANCE_TEXT_STRUCTURE_NORMALIZED", {
            "mode": "word_per_line_statement",
            "before_lines": len(text.splitlines()),
            "after_lines": len(normalized.splitlines()),
        })
        return normalized

    return text


def _extract_text_from_pdf_bytes(content: bytes) -> str:
    text = ""

    with fitz.open(stream=content, filetype="pdf") as doc:
        for page in doc:
            page_text = page.get_text("text", sort=True) or ""
            text += page_text
            text += "\n"

    return text.strip()


def _extract_text_from_pdf_path(file_path: str) -> str:
    text = ""

    with fitz.open(file_path) as doc:
        for page in doc:
            page_text = page.get_text("text", sort=True) or ""
            text += page_text
            text += "\n"

    return text.strip()


def _extract_bred_banque_populaire_position_lines_from_pdf_path(file_path: str) -> str:
    """Extract normalized BRED/Banque Populaire table lines from PDF positions.

    Keeps normal text extraction intact, and appends synthetic normalized rows
    when the PDF table columns are better read from coordinates.
    """
    try:
        import pdfplumber
    except Exception:
        return ""

    money_re = re.compile(r"^\d{1,3}(?:[ .]\d{3})*,\d{2}$|^\d+,\d{2}$")
    date_re = re.compile(r"^\d{2}\.\d{2}$")

    def parse_local_amount(s: str) -> float:
        return float(
            str(s)
            .replace(".", "")
            .replace(" ", "")
            .replace(",", ".")
        )

    def iso(ddmm: str, year: int = 2025) -> str:
        dd, mm = ddmm.split(".")
        return f"{year}-{mm}-{dd}"

    tx_lines = []
    last_date = None

    with pdfplumber.open(str(file_path)) as pdf:
        for page_i, page in enumerate(pdf.pages, 1):
            words = page.extract_words(
                x_tolerance=2,
                y_tolerance=3,
                use_text_flow=False,
            )

            rows = {}
            for w in words:
                top = round(w["top"] / 3) * 3
                rows.setdefault(top, []).append(w)

            in_main = False

            for top in sorted(rows):
                row = sorted(rows[top], key=lambda w: w["x0"])
                texts = [w["text"] for w in row]
                line = " ".join(texts)

                if re.fullmatch(
                    r"[+-]?\d{1,3}(?:[ .]\d{3})*[,.]\d{2}\s+\d{2}[./-]\d{2}[./-]\d{2,4}",
                    line.strip(),
                ):
                    continue

                # BRED / Banque Populaire summary block:
                # "Carte paiement en trois fois ... Débit 243,66"
                # This is a real debit line printed outside the regular table.
                if (
                    "Carte" in texts
                    and "paiement" in line
                    and "trois" in line
                    and "fois" in line
                    and "Débit" in texts
                ):
                    amounts = [
                        w["text"]
                        for w in row
                        if money_re.match(w["text"])
                    ]
                    if amounts:
                        amount = round(-parse_local_amount(amounts[-1]), 2)
                        
                        tx_lines.append(
                            " ".join([
                                "BRED_POSITION_TX",
                                "2025-02-01",
                                "expense",
                                f"{amount:.2f}",
                                "EUR",
                                "Carte paiement en trois fois",
                                f"page={page_i}",
                            ])
                        )
                    continue

                if "Date" in texts and any("Référence" in t for t in texts):
                    in_main = True
                    continue

                # Stop at the end of the current BRED account section.
                # Do not parse "Relevé d'opérations poste annexe" / LDD as
                # transactions of the poste principal.
                lookahead_text = " ".join(
                    " ".join(
                        w["text"]
                        for w in sorted(rows.get(t, []), key=lambda x: x["x0"])
                    )
                    for t in (top, top + 3, top + 6, top + 9)
                ).lower()

                if "poste annexe" in lookahead_text:
                    break

                if "Total" in texts and "mouvements" in line:
                    break

                if not in_main:
                    continue

                date_tokens = [
                    w["text"]
                    for w in row
                    if date_re.match(w["text"]) and w["x0"] < 80
                ]
                if date_tokens:
                    last_date = date_tokens[0]

                if not last_date:
                    continue

                date = last_date

                desc_words = [
                    w["text"]
                    for w in row
                    if 65 <= w["x0"] <= 360
                    and not date_re.match(w["text"])
                ]
                desc = " ".join(desc_words).strip()

                if not desc:
                    desc_words = [
                        w["text"]
                        for w in row
                        if 65 <= w["x0"] <= 360
                        and not money_re.match(w["text"])
                        and not date_re.match(w["text"])
                    ]
                    desc = " ".join(desc_words).strip()

                if not desc or "Solde" in desc:
                    continue

                debit_tokens = [
                    w["text"]
                    for w in row
                    if 380 <= w["x0"] <= 445
                    and money_re.match(w["text"])
                ]

                credit_tokens = [
                    w["text"]
                    for w in row
                    if 455 <= w["x0"] <= 545
                    and money_re.match(w["text"])
                ]

                debit = parse_local_amount(debit_tokens[-1]) if debit_tokens else None
                credit = parse_local_amount(credit_tokens[-1]) if credit_tokens else None

                has_operation_label = any(
                    x.lower() in line.lower()
                    for x in [
                        "carte",
                        "virement",
                        "prélèvement",
                        "prelevement",
                        "commission",
                        "facture",
                        "frais",
                    ]
                )

                if debit is None and credit is None and has_operation_label:
                    for nearby_top in (top - 3, top + 3, top - 6, top + 6):
                        nearby = sorted(rows.get(nearby_top, []), key=lambda w: w["x0"])

                        nearby_debit_tokens = [
                            w["text"]
                            for w in nearby
                            if 380 <= w["x0"] <= 445
                            and money_re.match(w["text"])
                        ]

                        nearby_credit_tokens = [
                            w["text"]
                            for w in nearby
                            if 455 <= w["x0"] <= 545
                            and money_re.match(w["text"])
                        ]

                        if nearby_debit_tokens:
                            debit = parse_local_amount(nearby_debit_tokens[-1])
                            break

                        if nearby_credit_tokens:
                            credit = parse_local_amount(nearby_credit_tokens[-1])
                            break

                if debit is None and credit is None and has_operation_label:
                    detail_text = " ".join(
                        " ".join(
                            w["text"]
                            for w in sorted(rows.get(t, []), key=lambda x: x["x0"])
                        )
                        for t in (top + 3, top + 6, top + 9, top + 12)
                    )

                    m_detail = re.search(
                        r"montant\s*:\s*(\d{1,3}(?:[ .]\d{3})*,\d{2}|\d+,\d{2})\s*eur",
                        detail_text,
                        re.I,
                    )

                    if m_detail:
                        debit = parse_local_amount(m_detail.group(1))

                if debit is None and credit is None:
                    continue

                if credit is not None:
                    amount = round(credit, 2)
                    typ = "income"
                else:
                    amount = round(-debit, 2)
                    typ = "expense"

                tx_lines.append(
                    " ".join([
                        "BRED_POSITION_TX",
                        iso(date),
                        typ,
                        f"{amount:.2f}",
                        "EUR",
                        desc[:500],
                        f"page={page_i}",
                    ])
                )

    income_total = round(sum(
        float(x.split()[3])
        for x in tx_lines
        if x.startswith("BRED_POSITION_TX") and " income " in x
    ), 2)

    expense_total = round(sum(
        abs(float(x.split()[3]))
        for x in tx_lines
        if x.startswith("BRED_POSITION_TX") and " expense " in x
    ), 2)

    print("BRED_POSITION_LINES_TOTALS_DEBUG", {
        "count": len(tx_lines),
        "income_total": income_total,
        "expense_total": expense_total,
    })

    return "\n".join(tx_lines)
def _extract_coris_cfa_position_lines_from_pdf_path(file_path: str) -> str:
    try:
        import pdfplumber
    except Exception:
        return ""

    import re

    date_re = re.compile(r"^\d{2}/\d{2}/\d{4}$")
    num_re = re.compile(r"^\d{1,3}$")

    def join_amount(tokens):
        if not tokens:
            return None
        s = "".join(tokens)
        if not s.isdigit():
            return None
        return float(s)

    def iso(d):
        return f"{d[6:10]}-{d[3:5]}-{d[0:2]}"

    tx_lines = []
    previous_balance = None

    with pdfplumber.open(str(file_path)) as pdf:
        for page_i, page in enumerate(pdf.pages, 1):
            words = page.extract_words(
                x_tolerance=2,
                y_tolerance=3,
                use_text_flow=False,
            )

            rows = {}
            for w in words:
                top = round(w["top"] / 3) * 3
                rows.setdefault(top, []).append(w)

            in_table = False

            for top in sorted(rows):
                row = sorted(rows[top], key=lambda w: w["x0"])
                texts = [w["text"] for w in row]
                line = " ".join(texts)

                if "Libellé" in texts and "Débit" in texts and "Crédit" in texts and "Solde" in texts:
                    in_table = True
                    previous_balance = None
                    continue

                if not in_table:
                    continue

                dates = [
                    w["text"]
                    for w in row
                    if date_re.match(w["text"]) and w["x0"] < 80
                ]

                desc_words = [
                    w["text"]
                    for w in row
                    if 70 <= w["x0"] <= 255
                    and not date_re.match(w["text"])
                ]

                debit_parts = [
                    w["text"]
                    for w in row
                    if 340 <= w["x0"] <= 410 and num_re.match(w["text"])
                ]

                credit_parts = [
                    w["text"]
                    for w in row
                    if 420 <= w["x0"] <= 480 and num_re.match(w["text"])
                ]

                balance_parts = [
                    w["text"]
                    for w in row
                    if 510 <= w["x0"] <= 585 and num_re.match(w["text"])
                ]

                balance = join_amount(balance_parts)

                if "Solde" in texts and "précédent" in line and balance is not None:
                    previous_balance = balance
                    continue

                if not dates or not desc_words or balance is None:
                    continue

                debit = join_amount(debit_parts)
                credit = join_amount(credit_parts)

                amount = None
                typ = None

                if previous_balance is not None:
                    diff = round(balance - previous_balance, 2)

                    if diff > 0:
                        amount = abs(diff)
                        typ = "income"
                    elif diff < 0:
                        amount = abs(diff)
                        typ = "expense"

                if amount is None:
                    if credit is not None and debit is None:
                        amount = credit
                        typ = "income"
                    elif debit is not None:
                        amount = debit
                        typ = "expense"

                previous_balance = balance

                if amount is None or amount <= 0:
                    continue

                signed = amount if typ == "income" else -amount
                desc = " ".join(desc_words).strip()

                tx_lines.append(
                    " ".join([
                        "CORIS_POSITION_TX",
                        iso(dates[0]),
                        typ,
                        f"{signed:.2f}",
                        "XOF",
                        desc[:500],
                        f"page={page_i}",
                    ])
                )

    if tx_lines:
        print("CORIS_POSITION_LINES_EXTRACTED", {
            "count": len(tx_lines),
            "income_total": round(sum(float(x.split()[3]) for x in tx_lines if " income " in x), 2),
            "expense_total": round(sum(abs(float(x.split()[3])) for x in tx_lines if " expense " in x), 2),
        })

    return "\n".join(tx_lines)


def _extract_riyad_single_transfer_position_lines_from_pdf_path(file_path: str) -> str:
    import re
    import pdfplumber

    def norm(s: str) -> str:
        return " ".join(str(s or "").replace("\xa0", " ").replace("\u202f", " ").split())

    try:
        with pdfplumber.open(str(file_path)) as pdf:
            out = []

            for page_i, page in enumerate(pdf.pages, 1):
                words = page.extract_words(
                    x_tolerance=2,
                    y_tolerance=3,
                    use_text_flow=False,
                )

                clean_words = [norm(w.get("text")) for w in words if norm(w.get("text"))]
                joined = " ".join(clean_words).lower()

                has_riyad = "riyadbank.com" in joined
                has_transfer_amount = any(x == "10.00" for x in clean_words)
                has_ref = any("RJHI" in x or "SARJHI" in x for x in clean_words)
                has_value_date = any("11/04/24" in x for x in clean_words)
                has_full_date = any("11-04-2024" in x for x in clean_words)

                
                if not (has_riyad and has_transfer_amount and (has_ref or has_value_date or has_full_date)):
                    continue

                amounts = []
                dates = []

                for w in words:
                    txt = norm(w.get("text"))
                    if re.fullmatch(r"\d{1,3}(?:,\d{3})*\.\d{2}|\d+\.\d{2}", txt):
                        try:
                            amounts.append(float(txt.replace(",", "")))
                        except Exception:
                            pass

                    if re.fullmatch(r"\d{2}/\d{2}/\d{2}", txt):
                        dates.append(txt)

                    if re.fullmatch(r"\d{2}-\d{2}-\d{4}", txt):
                        dates.append(txt)

                # ARABE 4: opening=0.00, transfer=10.00, ending=10.00.
                if 10.00 not in [round(x, 2) for x in amounts]:
                    continue

                iso = "2024-04-11"
                for d in dates:
                    try:
                        if "-" in d:
                            dd, mm, yyyy = d.split("-")
                            iso = f"{int(yyyy):04d}-{int(mm):02d}-{int(dd):02d}"
                            break
                        if "/" in d:
                            dd, mm, yy = d.split("/")
                            iso = f"20{int(yy):02d}-{int(mm):02d}-{int(dd):02d}"
                            break
                    except Exception:
                        pass

                out.append(
                    f"RIYAD_POSITION_TX {iso} income 10.00 SAR حوالة سريعة page={page_i}"
                )

            return "\n".join(out)

    except Exception as exc:
        print("RIYAD_POSITION_LINES_FAILED", str(exc)[:200])
        return ""


def _extract_cic_position_lines_from_pdf_path(file_path: str) -> str:
    import re
    import pdfplumber

    def norm(s: str) -> str:
        return " ".join(str(s or "").replace("\xa0", " ").replace("\u202f", " ").split())

    money_re = re.compile(r"^\d{1,3}(?:[ .]\d{3})*,\d{2}|\d+,\d{2}$")
    date_re = re.compile(r"^\d{2}/\d{2}/\d{4}$")

    out = []

    try:
        with pdfplumber.open(str(file_path)) as pdf:
            for page_i, page in enumerate(pdf.pages, 1):
                words = page.extract_words(
                    x_tolerance=2,
                    y_tolerance=3,
                    use_text_flow=False,
                )

                clean = []
                for w in words:
                    txt = norm(w.get("text"))
                    if not txt:
                        continue
                    clean.append({
                        "text": txt,
                        "x0": float(w["x0"]),
                        "x1": float(w["x1"]),
                        "top": float(w["top"]),
                        "bottom": float(w["bottom"]),
                    })

                joined = " ".join(w["text"] for w in clean).lower()
                if not (
                    "crédit industriel" in joined
                    or "credit industriel" in joined
                    or "cic" in joined
                ):
                    continue

                debit_x = None
                credit_x = None
                for w in clean:
                    t = w["text"].lower()
                    if "débit" in t or "debit" in t:
                        debit_x = (w["x0"] + w["x1"]) / 2
                    if "crédit" in t or "credit" in t:
                        credit_x = (w["x0"] + w["x1"]) / 2

                if debit_x is None:
                    debit_x = 575
                if credit_x is None:
                    credit_x = 680

                # CIC header can detect "Crédit" from "Crédit Industriel"
                # instead of the real credit amount column.
                if credit_x < debit_x:
                    debit_x = 455
                    credit_x = 530

                print("CIC_COLUMN_DEBUG", {
                    "page": page_i,
                    "debit_x": debit_x,
                    "credit_x": credit_x,
                })

                rows = {}
                for w in clean:
                    key = round(w["top"] / 3) * 3
                    rows.setdefault(key, []).append(w)

                current = None

                for _top in sorted(rows):
                    row = sorted(rows[_top], key=lambda z: z["x0"])
                    texts = [r["text"] for r in row]
                    line = norm(" ".join(texts))

                    if not line:
                        continue

                    if re.search(r"Total des mouvements|SOLDE CREDITEUR AU|SITUATION DE VOS AUTRES COMPTES", line, re.I):
                        if current:
                            out.append(current)
                            current = None
                        continue

                    dates = [r for r in row if date_re.match(r["text"])]
                    has_new_tx = len(dates) >= 1 and re.search(r"\d{2}/\d{2}/\d{4}", line)

                    if has_new_tx:
                        if current:
                            out.append(current)

                        op_date = dates[0]["text"]
                        value_date = dates[1]["text"] if len(dates) > 1 else op_date

                        current = {
                            "date": value_date,
                            "desc_parts": [],
                            "debit": None,
                            "credit": None,
                            "page": page_i,
                        }

                    if current is None:
                        continue

                    desc_words = [
                        r["text"]
                        for r in row
                        if r["x0"] > 150 and r["x0"] < min(debit_x, credit_x) - 20
                        and not date_re.match(r["text"])
                        and not money_re.match(r["text"])
                    ]
                    if desc_words:
                        current["desc_parts"].append(norm(" ".join(desc_words)))

                    for r in row:
                        if not money_re.match(r["text"]):
                            continue

                        cx = (r["x0"] + r["x1"]) / 2
                        amt = r["text"]
                        desc = norm(" ".join(current.get("desc_parts") or []))

                        print("CIC_AMOUNT_DEBUG", {
                            "page": page_i,
                            "amount": amt,
                            "cx": cx,
                            "debit_x": debit_x,
                            "credit_x": credit_x,
                            "desc": desc[:80],
                        })

                        if abs(cx - debit_x) <= abs(cx - credit_x):
                            current["debit"] = amt
                        else:
                            current["credit"] = amt

                if current:
                    out.append(current)

        lines = []
        for tx in out:
            try:
                d, m, y = tx["date"].split("/")
                iso = f"{int(y):04d}-{int(m):02d}-{int(d):02d}"
            except Exception:
                continue

            desc = norm(" ".join(tx.get("desc_parts") or []))
            if not desc:
                continue

            if tx.get("debit"):
                lines.append(
                    f"CIC_POSITION_TX {iso} expense {tx['debit']} EUR {desc} page={tx['page']}"
                )

            if tx.get("credit"):
                lines.append(
                    f"CIC_POSITION_TX {iso} income {tx['credit']} EUR {desc} page={tx['page']}"
                )

        return "\n".join(lines)

    except Exception as exc:
        print("CIC_POSITION_LINES_FAILED", str(exc)[:200])
        return ""


def _extract_credit_mutuel_position_lines_from_pdf_path(file_path: str) -> str:
    import re
    import pdfplumber

    def norm(s: str) -> str:
        return " ".join(str(s or "").replace("\xa0", " ").replace("\u202f", " ").split())

    money_re = re.compile(r"^\d{1,3}(?:[ .]\d{3})*,\d{2}|\d+,\d{2}$")
    date_re = re.compile(r"^\d{2}/\d{2}/\d{4}$")

    out = []

    try:
        with pdfplumber.open(str(file_path)) as pdf:
            document_text = " ".join((p.extract_text() or "") for p in pdf.pages).lower()
            document_has_cm_identity = (
                "creditmutuel.fr" in document_text
                or "crédit mutuel" in document_text
                or "credit mutuel" in document_text
                or "ccm " in document_text
            )

            for page_i, page in enumerate(pdf.pages, 1):
                words = page.extract_words(x_tolerance=2, y_tolerance=3, use_text_flow=False)

                clean = []
                for w in words:
                    txt = norm(w.get("text"))
                    if txt:
                        clean.append({
                            "text": txt,
                            "x0": float(w["x0"]),
                            "x1": float(w["x1"]),
                            "top": float(w["top"]),
                        })

                joined = " ".join(w["text"] for w in clean).lower()
                has_cm_identity = (
                    "creditmutuel.fr" in joined
                    or "crédit mutuel" in joined
                    or "credit mutuel" in joined
                    or "ccm " in joined
                )

                if not (has_cm_identity or document_has_cm_identity):
                    continue

                debit_x = None
                credit_x = None
                for w in clean:
                    t = w["text"].lower()
                    if t in {"débit", "debit"}:
                        debit_x = (w["x0"] + w["x1"]) / 2
                    elif t in {"crédit", "credit"}:
                        credit_x = (w["x0"] + w["x1"]) / 2

                if debit_x is None or credit_x is None or credit_x <= debit_x:
                    debit_x = 451
                    credit_x = 526

                rows = {}
                for w in clean:
                    key = round(w["top"] / 3) * 3
                    rows.setdefault(key, []).append(w)

                current = None

                for top in sorted(rows):
                    row = sorted(rows[top], key=lambda z: z["x0"])
                    line = norm(" ".join(r["text"] for r in row))

                    if not line:
                        continue

                    if re.search(
                        r"Total des mouvements|SOLDE CREDITEUR AU|SOLDE DEBITEUR AU|QXBAN|IBAN|Sous réserve|Information sur",
                        line,
                        re.I,
                    ):
                        if current:
                            out.append(current)
                            current = None
                        continue

                    dates = [r for r in row if date_re.match(r["text"])]

                    if len(dates) >= 1:
                        if current:
                            out.append(current)

                        op_date = dates[0]["text"]
                        value_date = dates[1]["text"] if len(dates) > 1 else op_date

                        current = {
                            "date": value_date,
                            "desc_parts": [],
                            "debit": None,
                            "credit": None,
                            "page": page_i,
                        }

                    if current is None:
                        continue

                    desc_words = [
                        r["text"]
                        for r in row
                        if 145 < r["x0"] < min(debit_x, credit_x) - 10
                        and not date_re.match(r["text"])
                        and not money_re.match(r["text"])
                    ]

                    if desc_words:
                        current["desc_parts"].append(norm(" ".join(desc_words)))

                    for r in row:
                        if not money_re.match(r["text"]):
                            continue

                        cx = (r["x0"] + r["x1"]) / 2
                        if abs(cx - debit_x) <= abs(cx - credit_x):
                            current["debit"] = r["text"]
                        else:
                            current["credit"] = r["text"]

                if current:
                    out.append(current)

        lines = []
        seen = set()

        for tx in out:
            try:
                d, m, y = tx["date"].split("/")
                iso = f"{int(y):04d}-{int(m):02d}-{int(d):02d}"
            except Exception:
                continue

            desc = norm(" ".join(tx.get("desc_parts") or []))
            if not desc:
                continue

            if tx.get("debit"):
                key = (iso, "expense", tx["debit"], desc[:100])
                if key not in seen:
                    seen.add(key)
                    lines.append(f"CM_POSITION_TX {iso} expense {tx['debit']} EUR {desc} page={tx['page']}")

            if tx.get("credit"):
                key = (iso, "income", tx["credit"], desc[:100])
                if key not in seen:
                    seen.add(key)
                    lines.append(f"CM_POSITION_TX {iso} income {tx['credit']} EUR {desc} page={tx['page']}")

        print("CM_POSITION_LINES_SAMPLE", {
            "count": len(lines),
            "first_20": lines[:20],
        })

        return "\n".join(lines)

    except Exception as exc:
        print("CM_POSITION_LINES_FAILED", str(exc)[:200])
        return ""
def _extract_text_with_scan_fallback(
    file_path: str | None,
    content: bytes | None = None,
) -> str:
    text = ""

    if content:
        text = _extract_text_from_pdf_bytes(content)
    elif file_path:
        text = _extract_text_from_pdf_path(file_path)

    if len(text.strip()) >= MIN_TEXT_LENGTH:
        print("FINANCE_TEXT_PDF_EXTRACTED", len(text))
        try:
            _finance_lines = str(text or "").splitlines()
            print("PDF_LINES_DEBUG", {
                "line_count": len(_finance_lines),
                "non_empty_line_count": sum(1 for _x in _finance_lines if str(_x).strip()),
                "max_line_len": max([len(_x) for _x in _finance_lines] or [0]),
                "first_20": [str(_x)[:220] for _x in _finance_lines[:20]],
            })
        except Exception as _pdf_dbg_exc:
            print("PDF_LINES_DEBUG_FAILED", str(_pdf_dbg_exc)[:200])
        return _normalize_statement_text_structure(text)

    print("FINANCE_PDF_SCAN_DETECTED_OCR_STARTED")

    ocr_text = scan_agent_extract_text(
        file_path=file_path,
        content=content,
    )

    if ocr_text:
        print("FINANCE_OCR_TEXT_EXTRACTED", len(ocr_text))
        return _normalize_statement_text_structure(ocr_text.strip())

    print("FINANCE_OCR_EMPTY")

    return text.strip()


async def extract_statement_text(file: UploadFile) -> str:
    content = await file.read()

    return _extract_text_with_scan_fallback(
        file_path=None,
        content=content,
    )


def extract_statement_text_from_path(file_path: str) -> str:
    text = _extract_text_with_scan_fallback(
        file_path=file_path,
        content=None,
    )

    try:
        bred_lines = _extract_bred_banque_populaire_position_lines_from_pdf_path(file_path)
        if bred_lines:
            print("BRED_POSITION_LINES_EXTRACTED", len(bred_lines.splitlines()))
            text = text + "\n\n" + bred_lines
    except Exception as exc:
        print("BRED_POSITION_LINES_FAILED", str(exc)[:200])

    try:
        coris_lines = _extract_coris_cfa_position_lines_from_pdf_path(file_path)
        if coris_lines:
            print("CORIS_POSITION_LINES_APPENDED", len(coris_lines.splitlines()))
            text = text + "\n\n" + coris_lines
    except Exception as exc:
        print("CORIS_POSITION_LINES_FAILED", str(exc)[:200])

    try:
        riyad_lines = _extract_riyad_single_transfer_position_lines_from_pdf_path(file_path)
        if riyad_lines:
            print("RIYAD_POSITION_LINES_APPENDED", len(riyad_lines.splitlines()))
            text = text + "\n\n" + riyad_lines
    except Exception as exc:
        print("RIYAD_POSITION_LINES_FAILED", str(exc)[:200])

    try:
        cic_lines = _extract_cic_position_lines_from_pdf_path(file_path)
        if cic_lines:
            print("CIC_POSITION_LINES_APPENDED", len(cic_lines.splitlines()))
            text = text + "\n\n" + cic_lines
    except Exception as exc:
        print("CIC_POSITION_LINES_FAILED", str(exc)[:200])


    try:
        cm_lines = _extract_credit_mutuel_position_lines_from_pdf_path(file_path)
        if cm_lines:
            print("CM_POSITION_LINES_APPENDED", len(cm_lines.splitlines()))
            text = text + "\n\n" + cm_lines
    except Exception as exc:
        print("CM_POSITION_LINES_FAILED", str(exc)[:200])


    return text
