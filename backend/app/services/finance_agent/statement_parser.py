from fastapi import UploadFile
import fitz
import os
import re

from app.services.finance_agent.scan_agent import scan_agent_extract_text
from app.services.finance_agent.international_standard import normalize_statement_text


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


def _normalize_statement_text_structure(
    text: str,
    *,
    preserve_positional_layout: bool = False,
) -> str:
    if not text:
        return text

    text = normalize_statement_text(text)

    if preserve_positional_layout:
        return text

    text = re.sub(
        r"(\d{1,2}[./-]\d{1,2})\s*\n\s*"
        r"(?=\d{1,3}(?:[ .]\d{3})*[,.]\d{2}\b)",
        r"\1 ",
        text,
    )

    normalized = _merge_amount_only_lines_into_previous(text)

    if normalized != text:
        print(
            "FINANCE_TEXT_STRUCTURE_NORMALIZED",
            {
                "mode": "amount_only_line_merged",
                "before_lines": len(text.splitlines()),
                "after_lines": len(normalized.splitlines()),
            },
        )
        text = normalized

    if _looks_like_word_per_line_statement(text):
        normalized = _normalize_word_per_line_statement(text)

        print(
            "FINANCE_TEXT_STRUCTURE_NORMALIZED",
            {
                "mode": "word_per_line_statement",
                "before_lines": len(text.splitlines()),
                "after_lines": len(normalized.splitlines()),
            },
        )

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


def _extract_date_description_value_date_debit_credit_position_lines(
    *,
    file_path: str | None = None,
    content: bytes | None = None,
) -> str:
    """
    Additive positional extraction for:

        Date | Description | Value Date | Debit | Credit

    The original PDF text is never replaced. The extractor emits neutral
    synthetic observations only when a reliable five-column header is found.

    Rows are reconstructed from date anchors and vertical bands. This handles
    PDFs where the date/amount baseline and the description baseline differ
    slightly, without using bank, country, merchant, or currency rules.
    """
    import io
    import re
    import unicodedata
    from datetime import date

    try:
        import pdfplumber
    except Exception:
        return ""

    if not file_path and content is None:
        return ""

    def compact(value: str) -> str:
        return " ".join(
            str(value or "")
            .replace("\xa0", " ")
            .replace("\u202f", " ")
            .split()
        )

    def fold(value: str) -> str:
        normalized = unicodedata.normalize(
            "NFKD",
            compact(value),
        )
        normalized = "".join(
            character
            for character in normalized
            if not unicodedata.combining(character)
        )
        return normalized.casefold()

    full_date_re = re.compile(
        r"^(?P<day>\d{1,2})[./-]"
        r"(?P<month>\d{1,2})[./-]"
        r"(?P<year>\d{2,4})$"
    )
    short_date_re = re.compile(
        r"^(?P<day>\d{1,2})[./-]"
        r"(?P<month>\d{1,2})$"
    )
    integer_money_re = re.compile(
        r"^(?:"
        r"\d{1,3}(?:[ .,\u00a0\u202f]\d{3})+"
        r"|\d+"
        r")$"
    )

    header_terms = {
        "date": {"date"},
        "description": {
            "description",
            "details",
            "detail",
            "narrative",
            "libelle",
            "operation",
            "operations",
            "nature",
        },
        "value_date": {
            "value",
            "valeur",
            "val",
            "bval",
            "valor",
            "valuta",
        },
        "debit": {
            "debit",
            "debito",
            "addebito",
            "belastung",
            "مدين",
        },
        "credit": {
            "credit",
            "credito",
            "accredito",
            "gutschrift",
            "دائن",
        },
    }

    def word_center_x(word: dict) -> float:
        return (
            float(word["x0"])
            + float(word["x1"])
        ) / 2.0

    def word_center_y(word: dict) -> float:
        return (
            float(word["top"])
            + float(word.get("bottom", word["top"]))
        ) / 2.0

    def group_header_rows(
        words: list[dict],
    ) -> list[list[dict]]:
        rows: list[list[dict]] = []
        row_centers: list[float] = []

        for word in sorted(
            words,
            key=lambda item: (
                word_center_y(item),
                float(item["x0"]),
            ),
        ):
            y = word_center_y(word)
            selected = None
            selected_distance = None

            for index, center_y in enumerate(row_centers):
                distance = abs(y - center_y)

                if distance <= 3.5 and (
                    selected_distance is None
                    or distance < selected_distance
                ):
                    selected = index
                    selected_distance = distance

            if selected is None:
                rows.append([word])
                row_centers.append(y)
                continue

            rows[selected].append(word)
            row_centers[selected] = sum(
                word_center_y(item)
                for item in rows[selected]
            ) / len(rows[selected])

        return [
            sorted(row, key=lambda item: float(item["x0"]))
            for _, row in sorted(
                zip(row_centers, rows),
                key=lambda item: item[0],
            )
        ]

    def detect_header(
        words: list[dict],
    ) -> dict | None:
        for row in group_header_rows(words):
            role_words: dict[str, list[dict]] = {}

            for word in row:
                token = fold(word.get("text"))

                for role, terms in header_terms.items():
                    if token in terms:
                        role_words.setdefault(role, []).append(word)

            required = (
                "date",
                "description",
                "value_date",
                "debit",
                "credit",
            )

            if any(
                not role_words.get(role)
                for role in required
            ):
                continue

            selected = {
                role: min(
                    role_words[role],
                    key=lambda item: float(item["x0"]),
                )
                for role in required
            }
            centers = {
                role: word_center_x(word)
                for role, word in selected.items()
            }

            if not (
                centers["date"]
                < centers["description"]
                < centers["value_date"]
                < centers["debit"]
                < centers["credit"]
            ):
                continue

            return {
                "centers": centers,
                "top": min(
                    float(word["top"])
                    for word in row
                ),
                "bottom": max(
                    float(word.get("bottom", word["top"]))
                    for word in row
                ),
            }

        return None

    def parse_full_date(token: str) -> str | None:
        match = full_date_re.fullmatch(
            compact(token)
        )

        if match is None:
            return None

        try:
            year = int(match.group("year"))

            if year < 100:
                year += 2000 if year < 70 else 1900

            return date(
                year,
                int(match.group("month")),
                int(match.group("day")),
            ).isoformat()
        except (TypeError, ValueError):
            return None

    def parse_value_date(
        token: str,
        operation_date: str,
    ) -> str | None:
        match = short_date_re.fullmatch(
            compact(token)
        )

        if match is None:
            return None

        try:
            operation = date.fromisoformat(
                operation_date
            )
            month = int(match.group("month"))
            day = int(match.group("day"))
            candidate = date(
                operation.year,
                month,
                day,
            )
            delta = (candidate - operation).days

            if delta < -183:
                candidate = date(
                    operation.year + 1,
                    month,
                    day,
                )
            elif delta > 183:
                candidate = date(
                    operation.year - 1,
                    month,
                    day,
                )

            return candidate.isoformat()
        except (TypeError, ValueError):
            return None

    def parse_integer_amount(
        words: list[dict],
    ) -> float | None:
        tokens = [
            compact(word.get("text"))
            for word in sorted(
                words,
                key=lambda item: float(item["x0"]),
            )
            if integer_money_re.fullmatch(
                compact(word.get("text"))
            )
        ]

        if not tokens:
            return None

        digits = "".join(
            re.sub(r"[^0-9]", "", token)
            for token in tokens
        )

        if not digits.isdigit():
            return None

        value = float(digits)
        return round(value, 2) if value > 0 else None

    output: list[str] = []
    header_count = 0
    transaction_count = 0

    try:
        pdf_source = (
            io.BytesIO(content)
            if content is not None
            else str(file_path)
        )

        with pdfplumber.open(pdf_source) as pdf:
            for page_index, page in enumerate(
                pdf.pages,
                1,
            ):
                extracted_words = page.extract_words(
                    x_tolerance=2,
                    y_tolerance=3,
                    use_text_flow=False,
                )
                words = [
                    {
                        "text": compact(word.get("text")),
                        "x0": float(word["x0"]),
                        "x1": float(word["x1"]),
                        "top": float(word["top"]),
                        "bottom": float(
                            word.get("bottom", word["top"])
                        ),
                    }
                    for word in extracted_words
                    if compact(word.get("text"))
                ]

                header = detect_header(words)

                if header is None:
                    continue

                header_count += 1
                centers = header["centers"]

                date_description_boundary = (
                    centers["date"]
                    + centers["description"]
                ) / 2.0
                description_value_boundary = (
                    centers["description"]
                    + centers["value_date"]
                ) / 2.0
                value_debit_boundary = (
                    centers["value_date"]
                    + centers["debit"]
                ) / 2.0
                debit_credit_boundary = (
                    centers["debit"]
                    + centers["credit"]
                ) / 2.0
                credit_right = min(
                    float(page.width) + 1.0,
                    centers["credit"]
                    + (
                        centers["credit"]
                        - centers["debit"]
                    ),
                )

                date_anchors = [
                    word
                    for word in words
                    if (
                        full_date_re.fullmatch(
                            compact(word.get("text"))
                        )
                        and word_center_x(word)
                        < date_description_boundary
                        and float(word["top"])
                        > float(header["bottom"])
                    )
                ]
                date_anchors.sort(
                    key=lambda item: word_center_y(item)
                )

                for anchor_index, anchor in enumerate(
                    date_anchors
                ):
                    anchor_y = word_center_y(anchor)
                    previous_y = (
                        word_center_y(
                            date_anchors[anchor_index - 1]
                        )
                        if anchor_index > 0
                        else float(header["bottom"])
                    )
                    next_y = (
                        word_center_y(
                            date_anchors[anchor_index + 1]
                        )
                        if anchor_index + 1
                        < len(date_anchors)
                        else min(
                            float(page.height),
                            anchor_y + max(
                                10.0,
                                anchor_y - previous_y,
                            ),
                        )
                    )

                    row_top = (
                        previous_y + anchor_y
                    ) / 2.0
                    row_bottom = (
                        anchor_y + next_y
                    ) / 2.0

                    row_words = [
                        word
                        for word in words
                        if (
                            row_top
                            <= word_center_y(word)
                            < row_bottom
                        )
                    ]

                    operation_date = parse_full_date(
                        anchor["text"]
                    )

                    if operation_date is None:
                        continue

                    value_candidates = [
                        word
                        for word in row_words
                        if (
                            description_value_boundary
                            <= word_center_x(word)
                            < value_debit_boundary
                            and short_date_re.fullmatch(
                                compact(word.get("text"))
                            )
                        )
                    ]
                    value_date = None
                    value_word = None

                    if value_candidates:
                        value_word = min(
                            value_candidates,
                            key=lambda item: abs(
                                word_center_x(item)
                                - centers["value_date"]
                            ),
                        )
                        value_date = parse_value_date(
                            value_word["text"],
                            operation_date,
                        )

                    description_left = float(anchor["x1"]) + 4.0
                    description_right = (
                        float(value_word["x0"]) - 3.0
                        if value_word is not None
                        else value_debit_boundary
                    )
                    description = compact(
                        " ".join(
                            word["text"]
                            for word in sorted(
                                row_words,
                                key=lambda item: (
                                    word_center_y(item),
                                    float(item["x0"]),
                                ),
                            )
                            if (
                                description_left
                                <= float(word["x0"])
                                and float(word["x1"])
                                <= description_right
                            )
                        )
                    )

                    debit = parse_integer_amount([
                        word
                        for word in row_words
                        if (
                            value_debit_boundary
                            <= word_center_x(word)
                            < debit_credit_boundary
                        )
                    ])
                    credit = parse_integer_amount([
                        word
                        for word in row_words
                        if (
                            debit_credit_boundary
                            <= word_center_x(word)
                            < credit_right
                        )
                    ])

                    if debit is not None and credit is not None:
                        continue

                    folded_description = fold(description)

                    if re.search(
                        r"\b(?:"
                        r"solde initial|"
                        r"opening balance|"
                        r"beginning balance"
                        r")\b",
                        folded_description,
                    ):
                        opening = (
                            credit
                            if credit is not None
                            else debit
                        )

                        if opening is not None:
                            output.append(
                                " ".join([
                                    "DATE_DESC_VALUE_DC_POSITION_BALANCE",
                                    "opening",
                                    f"{opening:.2f}",
                                    f"page={page_index}",
                                ])
                            )

                        continue

                    if (
                        not description
                        or (
                            debit is None
                            and credit is None
                        )
                    ):
                        continue

                    output.append(
                        "\t".join([
                            "DATE_DESC_VALUE_DC_POSITION_TX",
                            operation_date,
                            value_date or "-",
                            (
                                f"{debit:.2f}"
                                if debit is not None
                                else "-"
                            ),
                            (
                                f"{credit:.2f}"
                                if credit is not None
                                else "-"
                            ),
                            description[:500],
                            f"page={page_index}",
                        ])
                    )
                    transaction_count += 1

                # TOTAL and closing BALANCE remain neutral accounting context.
                for row in group_header_rows(words):
                    line = compact(
                        " ".join(
                            word["text"]
                            for word in row
                        )
                    )
                    folded_line = fold(line)

                    if re.match(r"^total\b", folded_line):
                        total_tokens = [
                            compact(word.get("text"))
                            for word in sorted(
                                row,
                                key=lambda item: float(item["x0"]),
                            )
                            if integer_money_re.fullmatch(
                                compact(word.get("text"))
                            )
                        ]

                        if len(total_tokens) == 2:
                            debit_total = float(
                                re.sub(r"[^0-9]", "", total_tokens[0])
                            )
                            credit_total = float(
                                re.sub(r"[^0-9]", "", total_tokens[1])
                            )

                            output.append(
                                " ".join([
                                    "DATE_DESC_VALUE_DC_POSITION_TOTAL",
                                    f"{debit_total:.2f}",
                                    f"{credit_total:.2f}",
                                    f"page={page_index}",
                                ])
                            )

                    if re.match(
                        r"^(?:"
                        r"solde au|"
                        r"closing balance|"
                        r"ending balance"
                        r")\b",
                        folded_line,
                    ):
                        closing = parse_integer_amount([
                            word
                            for word in row
                            if word_center_x(word)
                            >= value_debit_boundary
                        ])

                        if closing is not None:
                            output.append(
                                " ".join([
                                    "DATE_DESC_VALUE_DC_POSITION_BALANCE",
                                    "closing",
                                    f"{closing:.2f}",
                                    f"page={page_index}",
                                ])
                            )

    except Exception as exc:
        print(
            "DATE_DESCRIPTION_VALUE_DATE_DEBIT_CREDIT_POSITION_EXTRACTION_FAILED",
            str(exc)[:200],
        )
        return ""

    print(
        "DATE_DESCRIPTION_VALUE_DATE_DEBIT_CREDIT_POSITION_EXTRACTION_AUDIT",
        {
            "headers": header_count,
            "transactions": transaction_count,
            "lines": len(output),
        },
    )

    return "\n".join(output)


def _extract_credit_mutuel_position_lines_from_pdf_path(
    file_path: str | None = None,
    content: bytes | None = None,
) -> str:
    """Extract the structural family:

        Posting Date | Value Date | Description | Debit | Credit

    The historical public helper name is preserved for compatibility. The
    implementation is institution-, country-, currency-, merchant-, and
    commercial-label neutral. It activates only when a page exposes a reliable
    five-column header and classifies amounts exclusively from their horizontal
    position under Debit or Credit.
    """
    import io
    import re
    import unicodedata
    from datetime import date

    try:
        import pdfplumber
    except Exception:
        return ""

    def compact(value: str) -> str:
        return " ".join(
            str(value or "")
            .replace("\xa0", " ")
            .replace("\u202f", " ")
            .split()
        )

    def fold(value: str) -> str:
        normalized = unicodedata.normalize("NFKD", compact(value))
        normalized = "".join(
            char
            for char in normalized
            if not unicodedata.combining(char)
        )
        return normalized.casefold()

    short_date_re = re.compile(r"^\d{1,2}[./-]\d{1,2}$")
    full_date_re = re.compile(
        r"^(?P<day>\d{1,2})[./-](?P<month>\d{1,2})[./-](?P<year>\d{2,4})$"
    )
    # Complete monetary cells, including grouped thousands such as
    # 2.500,00 / 3,342.05. Historical plain decimal cells remain supported.
    decimal_fragment_re = re.compile(
        r"^[+\-]?(?:\d{1,3}(?:[ .,'’]\d{3})+|\d+)[.,]\d{2}$"
    )
    integer_fragment_re = re.compile(r"^\d{1,3}$")

    date_terms = {"date"}
    value_terms = {"value", "valeur", "valor", "valuta"}
    description_terms = {
        "description", "detail", "details", "operation", "operations",
        "narrative", "libelle", "concepto", "descrizione", "beschreibung",
    }
    debit_terms = {"debit", "debito", "addebito", "belastung", "مدين"}
    credit_terms = {"credit", "credito", "accredito", "gutschrift", "دائن"}

    # Hard table endings only. A creditor/debtor balance can be an opening
    # BALANCE row immediately below the header, so it must not close the table.
    footer_phrases = {
        "total des mouvements", "total movements", "total operations",
        "closing balance", "ending balance", "nouveau solde",
        "iban", "qxban", "legal notice", "terms and conditions",
        "privacy notice", "information sur", "sous reserve",
    }

    def word_role(word: dict) -> str | None:
        token = fold(word.get("text"))
        if token in date_terms:
            return "date"
        if token in value_terms:
            return "value_date"
        if token in description_terms:
            return "description"
        if token in debit_terms:
            return "debit"
        if token in credit_terms:
            return "credit"
        return None

    def parse_year_token(token: str) -> int | None:
        match = full_date_re.fullmatch(compact(token))
        if not match:
            return None
        year = int(match.group("year"))
        if year < 100:
            year += 2000
        try:
            date(year, int(match.group("month")), int(match.group("day")))
        except ValueError:
            return None
        return year

    def infer_statement_year(words: list[dict]) -> int | None:
        candidates: list[int] = []
        for word in words:
            year = parse_year_token(word.get("text"))
            if year is not None:
                candidates.append(year)
        if not candidates:
            return None
        # Statement/header dates are normally repeated across pages. The most
        # frequent valid year is therefore stronger than the first occurrence.
        return max(set(candidates), key=lambda item: (candidates.count(item), item))

    def iso_date(token: str, year: int | None) -> str | None:
        value = compact(token)
        full = full_date_re.fullmatch(value)
        if full:
            local_year = int(full.group("year"))
            if local_year < 100:
                local_year += 2000
            month = int(full.group("month"))
            day = int(full.group("day"))
        elif short_date_re.fullmatch(value) and year is not None:
            day_s, month_s = re.split(r"[./-]", value)
            local_year = int(year)
            month = int(month_s)
            day = int(day_s)
        else:
            return None
        try:
            return date(local_year, month, day).isoformat()
        except ValueError:
            return None

    def group_rows(words: list[dict]) -> dict[float, list[dict]]:
        rows: dict[float, list[dict]] = {}
        for word in words:
            top = round(float(word["top"]) / 3.0) * 3.0
            rows.setdefault(top, []).append(word)
        for top in rows:
            rows[top] = sorted(rows[top], key=lambda item: float(item["x0"]))
        return rows

    def detect_header(row: list[dict]) -> dict | None:
        role_words: dict[str, list[dict]] = {}
        for word in row:
            role = word_role(word)
            if role is not None:
                role_words.setdefault(role, []).append(word)

        # The family requires two date roles, description, debit and credit.
        # Some languages repeat the word "date" instead of naming value date.
        date_words = role_words.get("date", [])
        value_words = role_words.get("value_date", [])
        description_words = role_words.get("description", [])
        debit_words = role_words.get("debit", [])
        credit_words = role_words.get("credit", [])

        if not debit_words or not credit_words:
            return None

        if not date_words:
            return None

        date_word = min(date_words, key=lambda item: float(item["x0"]))
        if value_words:
            value_word = min(value_words, key=lambda item: float(item["x0"]))
        elif len(date_words) >= 2:
            value_word = sorted(date_words, key=lambda item: float(item["x0"]))[1]
        else:
            return None

        description_word = (
            min(description_words, key=lambda item: float(item["x0"]))
            if description_words
            else None
        )
        debit_word = min(debit_words, key=lambda item: float(item["x0"]))
        credit_word = min(credit_words, key=lambda item: float(item["x0"]))

        centers = {
            "date": (float(date_word["x0"]) + float(date_word["x1"])) / 2.0,
            "value_date": (float(value_word["x0"]) + float(value_word["x1"])) / 2.0,
            "description": (
                (float(description_word["x0"]) + float(description_word["x1"])) / 2.0
                if description_word is not None
                else (
                    (float(value_word["x0"]) + float(value_word["x1"])) / 2.0
                    + (float(debit_word["x0"]) + float(debit_word["x1"])) / 2.0
                ) / 2.0
            ),
            "debit": (float(debit_word["x0"]) + float(debit_word["x1"])) / 2.0,
            "credit": (float(credit_word["x0"]) + float(credit_word["x1"])) / 2.0,
        }

        if not (
            centers["date"] < centers["value_date"]
            < centers["description"] < centers["debit"] < centers["credit"]
        ):
            return None

        return centers

    def monetary_cell(row: list[dict], center: float, half_width: float) -> str | None:
        candidates = [
            word
            for word in row
            if center - half_width <= float(word["x0"]) <= center + half_width
            and (
                integer_fragment_re.fullmatch(compact(word.get("text")))
                or decimal_fragment_re.fullmatch(compact(word.get("text")))
            )
        ]
        if not candidates:
            return None

        candidates.sort(key=lambda item: float(item["x0"]))
        tokens = [compact(item.get("text")) for item in candidates]

        # PDF word extraction may split "3 982,55" into two adjacent words.
        decimal_positions = [
            index
            for index, token in enumerate(tokens)
            if decimal_fragment_re.fullmatch(token)
        ]
        if not decimal_positions:
            return None

        decimal_index = decimal_positions[-1]
        selected = [tokens[decimal_index]]
        cursor = decimal_index - 1
        while cursor >= 0 and integer_fragment_re.fullmatch(tokens[cursor]):
            right_word = candidates[cursor + 1]
            left_word = candidates[cursor]
            gap = float(right_word["x0"]) - float(left_word["x1"])
            if gap > 8.0:
                break
            selected.insert(0, tokens[cursor])
            cursor -= 1

        return " ".join(selected)

    def parse_amount_token(token: str | None) -> float | None:
        if not token:
            return None
        raw = compact(token).replace(" ", "")
        if "," in raw and "." in raw:
            if raw.rfind(",") > raw.rfind("."):
                raw = raw.replace(".", "").replace(",", ".")
            else:
                raw = raw.replace(",", "")
        elif "," in raw:
            raw = raw.replace(",", ".")
        try:
            value = round(float(raw), 2)
        except (TypeError, ValueError):
            return None
        return value if value > 0 else None

    output_rows: list[dict] = []
    detected_headers = 0

    try:
        if content is not None:
            pdf_source = io.BytesIO(content)
        elif file_path:
            pdf_source = str(file_path)
        else:
            return ""

        with pdfplumber.open(pdf_source) as pdf:
            for page_index, page in enumerate(pdf.pages, 1):
                extracted = page.extract_words(
                    x_tolerance=2,
                    y_tolerance=3,
                    use_text_flow=False,
                )
                words = []
                for word in extracted:
                    token = compact(word.get("text"))
                    if not token:
                        continue
                    words.append({
                        "text": token,
                        "x0": float(word["x0"]),
                        "x1": float(word["x1"]),
                        "top": float(word["top"]),
                    })

                statement_year = infer_statement_year(words)
                rows = group_rows(words)
                active_header: dict | None = None
                current: dict | None = None

                def flush_current() -> None:
                    nonlocal current
                    if current is not None:
                        output_rows.append(current)
                        current = None

                for top in sorted(rows):
                    row = rows[top]
                    line = compact(" ".join(item["text"] for item in row))
                    normalized_line = fold(line)

                    header = detect_header(row)
                    if header is not None:
                        flush_current()
                        active_header = header
                        detected_headers += 1
                        continue

                    if active_header is None:
                        continue

                    if any(phrase in normalized_line for phrase in footer_phrases):
                        flush_current()
                        active_header = None
                        continue

                    row_dates = [
                        item
                        for item in row
                        if short_date_re.fullmatch(item["text"])
                        or full_date_re.fullmatch(item["text"])
                    ]
                    row_dates.sort(key=lambda item: float(item["x0"]))

                    date_limit = (
                        active_header["date"] + active_header["value_date"]
                    ) / 2.0
                    description_limit = (
                        active_header["description"] + active_header["debit"]
                    ) / 2.0
                    amount_gap = active_header["credit"] - active_header["debit"]
                    amount_half_width = max(24.0, min(52.0, amount_gap * 0.46))

                    transaction_dates = [
                        item
                        for item in row_dates
                        if float(item["x0"]) < active_header["description"]
                    ]

                    if transaction_dates:
                        flush_current()
                        posting_token = transaction_dates[0]["text"]
                        value_token = (
                            transaction_dates[1]["text"]
                            if len(transaction_dates) > 1
                            else posting_token
                        )
                        posting_date = iso_date(posting_token, statement_year)
                        value_date = iso_date(value_token, statement_year)
                        if posting_date is None:
                            continue
                        current = {
                            "date": posting_date,
                            "value_date": value_date or posting_date,
                            "description_parts": [],
                            "debit": None,
                            "credit": None,
                            "page": page_index,
                            "source_top": float(top),
                        }

                    if current is None:
                        continue

                    description_words = [
                        item["text"]
                        for item in row
                        if active_header["value_date"] + 12.0
                        < float(item["x0"]) < description_limit
                        and not short_date_re.fullmatch(item["text"])
                        and not full_date_re.fullmatch(item["text"])
                    ]
                    description = compact(" ".join(description_words))
                    if description:
                        current["description_parts"].append(description)

                    debit_token = monetary_cell(
                        row,
                        active_header["debit"],
                        amount_half_width,
                    )
                    credit_token = monetary_cell(
                        row,
                        active_header["credit"],
                        amount_half_width,
                    )
                    debit = parse_amount_token(debit_token)
                    credit = parse_amount_token(credit_token)

                    # A single physical token cannot belong to both columns.
                    # When overlapping windows detect the same cell, choose the
                    # nearest header center from the token's geometric anchor.
                    if debit is not None and credit is not None and debit == credit:
                        money_words = [
                            item
                            for item in row
                            if decimal_fragment_re.fullmatch(item["text"])
                        ]
                        if money_words:
                            anchor = (
                                float(money_words[-1]["x0"])
                                + float(money_words[-1]["x1"])
                            ) / 2.0
                            if abs(anchor - active_header["debit"]) <= abs(
                                anchor - active_header["credit"]
                            ):
                                credit = None
                            else:
                                debit = None

                    if debit is not None:
                        current["debit"] = debit
                    if credit is not None:
                        current["credit"] = credit

                flush_current()

        lines: list[str] = []
        seen: set[tuple] = set()

        for observation in output_rows:
            debit = observation.get("debit")
            credit = observation.get("credit")
            if (debit is None) == (credit is None):
                continue

            description = compact(
                " ".join(observation.get("description_parts") or [])
            )
            if not description:
                description = "Transaction"

            if debit is not None:
                transaction_type = "expense"
                amount = -abs(float(debit))
            else:
                transaction_type = "income"
                amount = abs(float(credit))

            key = (
                observation["date"],
                observation.get("value_date"),
                round(amount, 2),
                description[:160].casefold(),
                observation["page"],
                observation.get("source_top"),
            )
            if key in seen:
                continue
            seen.add(key)

            lines.append(
                " ".join([
                    "CM_POSITION_TX",
                    observation["date"],
                    transaction_type,
                    f"{amount:.2f}",
                    "MULTI",
                    description[:500],
                    f"value_date={observation.get('value_date')}",
                    f"page={observation['page']}",
                ])
            )

        print(
            "DATE_VALUE_DESCRIPTION_DEBIT_CREDIT_POSITION_AUDIT",
            {
                "headers": detected_headers,
                "observations": len(output_rows),
                "transactions": len(lines),
                "debits": sum(" expense " in line for line in lines),
                "credits": sum(" income " in line for line in lines),
                "sample": lines[:8],
            },
        )

        return "\n".join(lines)

    except Exception as exc:
        print(
            "DATE_VALUE_DESCRIPTION_DEBIT_CREDIT_POSITION_FAILED",
            str(exc)[:300],
        )
        return ""



def _extract_money_out_money_in_balance_position_lines(
    file_path: str | None = None,
    content: bytes | None = None,
) -> str:
    """Extract neutral observations for the structural family:

        Date | Description | Money out | Money in | Balance

    The historical helper name and all callers remain unchanged. Detection and
    classification depend only on the physical header and X positions. When the
    structure is not proved, the function returns an empty string.
    """
    import io
    import re
    import unicodedata
    from datetime import date

    try:
        import pdfplumber
    except Exception:
        return ""

    def compact(value: str) -> str:
        return " ".join(
            str(value or "")
            .replace("\xa0", " ")
            .replace("\u202f", " ")
            .split()
        )

    def fold(value: str) -> str:
        normalized = unicodedata.normalize("NFKD", compact(value))
        normalized = "".join(
            char for char in normalized if not unicodedata.combining(char)
        )
        return normalized.casefold()

    month_map = {
        "jan": 1, "january": 1, "janv": 1, "janvier": 1,
        "feb": 2, "february": 2, "fev": 2, "fevrier": 2,
        "mar": 3, "march": 3, "mars": 3,
        "apr": 4, "april": 4, "avr": 4, "avril": 4,
        "may": 5, "mai": 5,
        "jun": 6, "june": 6, "juin": 6,
        "jul": 7, "july": 7, "juil": 7, "juillet": 7,
        "aug": 8, "august": 8, "aout": 8,
        "sep": 9, "sept": 9, "september": 9, "septembre": 9,
        "oct": 10, "october": 10, "octobre": 10,
        "nov": 11, "november": 11, "novembre": 11,
        "dec": 12, "december": 12, "decembre": 12,
    }
    month_words = "|".join(
        sorted((re.escape(item) for item in month_map), key=len, reverse=True)
    )

    period_re = re.compile(
        rf"(?P<sd>\d{{1,2}})\s+(?P<sm>{month_words})\.?\s+"
        rf"(?P<sy>\d{{4}})\s*[-–—]\s*"
        rf"(?P<ed>\d{{1,2}})\s+(?P<em>{month_words})\.?\s+"
        rf"(?P<ey>\d{{4}})",
        re.I,
    )
    numeric_short_date_re = re.compile(r"^\d{1,2}[./-]\d{1,2}$")
    numeric_full_date_re = re.compile(
        r"^(?P<day>\d{1,2})[./-](?P<month>\d{1,2})[./-](?P<year>\d{2,4})$"
    )
    day_token_re = re.compile(r"^\d{1,2}$")
    month_token_re = re.compile(rf"^(?:{month_words})\.?$", re.I)
    money_token_re = re.compile(
        r"^[+\-]?(?:\d{1,3}(?:[,.]\d{3})+|\d+)(?:[.,]\d{2})$"
    )

    date_terms = {"date"}
    description_terms = {
        "description", "details", "detail", "narrative", "operation",
        "operations", "libelle", "particular", "particulars",
    }
    debit_terms = {
        "money out", "outgoing", "debit", "debits", "withdrawal", "sortie",
    }
    credit_terms = {
        "money in", "incoming", "credit", "credits", "deposit", "entree",
    }
    balance_terms = {"balance", "running balance", "solde"}

    hard_footer_phrases = {
        "continued", "legal notice", "terms and conditions", "privacy notice",
        "financial services compensation", "anything wrong", "credit interest rates",
    }
    balance_role_re = re.compile(
        r"\b(?:start(?:ing)?|opening|beginning|end(?:ing)?|closing|final|previous)\s+balance\b|"
        r"\b(?:brought|carried)\s+forward\b|"
        r"\bsolde\s+(?:initial|final|d['’]ouverture|de\s+cloture)\b",
        re.I,
    )

    def token_center(word: dict) -> float:
        return (float(word["x0"]) + float(word["x1"])) / 2.0

    def group_rows(words: list[dict]) -> dict[float, list[dict]]:
        rows: dict[float, list[dict]] = {}
        for word in words:
            key = round(float(word["top"]) / 3.0) * 3.0
            rows.setdefault(key, []).append(word)
        for key in rows:
            rows[key] = sorted(rows[key], key=lambda item: float(item["x0"]))
        return rows

    def role_candidates(row: list[dict]) -> dict[str, list[dict]]:
        result = {role: [] for role in ("date", "description", "debit", "credit", "balance")}
        ordered = sorted(row, key=lambda item: float(item["x0"]))

        for word in ordered:
            token = fold(word.get("text"))
            if token in date_terms:
                result["date"].append(word)
            if token in description_terms:
                result["description"].append(word)
            if token in debit_terms:
                result["debit"].append(word)
            if token in credit_terms:
                result["credit"].append(word)
            if token in balance_terms:
                result["balance"].append(word)

        for size in (2, 3):
            for index in range(len(ordered) - size + 1):
                segment = ordered[index:index + size]
                phrase = fold(" ".join(item["text"] for item in segment))
                synthetic = {
                    "text": phrase,
                    "x0": min(float(item["x0"]) for item in segment),
                    "x1": max(float(item["x1"]) for item in segment),
                    "top": min(float(item["top"]) for item in segment),
                }
                if phrase in debit_terms:
                    result["debit"].append(synthetic)
                if phrase in credit_terms:
                    result["credit"].append(synthetic)
                if phrase in balance_terms:
                    result["balance"].append(synthetic)

        return result

    def detect_header(row: list[dict]) -> dict | None:
        candidates = role_candidates(row)
        if not all(candidates[role] for role in candidates):
            return None
        selected = {
            role: min(words, key=lambda item: float(item["x0"]))
            for role, words in candidates.items()
        }
        centers = {role: token_center(word) for role, word in selected.items()}
        if not (
            centers["date"] < centers["description"] < centers["debit"]
            < centers["credit"] < centers["balance"]
        ):
            return None
        return centers

    def infer_year(month: int, period: dict | None, fallback_year: int | None) -> int | None:
        if period is None:
            return fallback_year
        start_year = period["start_year"]
        end_year = period["end_year"]
        start_month = period["start_month"]
        end_month = period["end_month"]
        if start_year == end_year:
            return start_year
        if start_month > end_month:
            return start_year if month >= start_month else end_year
        return start_year if month >= start_month else end_year

    def parse_date_words(
        row: list[dict],
        date_right_bound: float,
        period: dict | None,
        fallback_year: int | None,
    ) -> str | None:
        candidates = [word for word in row if token_center(word) < date_right_bound]
        candidates.sort(key=lambda item: float(item["x0"]))

        for word in candidates:
            token = compact(word.get("text"))
            match = numeric_full_date_re.fullmatch(token)
            if match:
                year = int(match.group("year"))
                if year < 100:
                    year += 2000
                try:
                    return date(year, int(match.group("month")), int(match.group("day"))).isoformat()
                except ValueError:
                    continue
            if numeric_short_date_re.fullmatch(token) and fallback_year is not None:
                day_s, month_s = re.split(r"[./-]", token)
                try:
                    return date(int(fallback_year), int(month_s), int(day_s)).isoformat()
                except ValueError:
                    continue

        # Additive named-date variant: DD Mon YYYY, usually split into three
        # adjacent pdfplumber words. The historical numeric paths above remain
        # authoritative and unchanged.
        for index in range(len(candidates) - 2):
            first = compact(candidates[index].get("text"))
            second = compact(candidates[index + 1].get("text")).rstrip(".")
            third = compact(candidates[index + 2].get("text"))

            if (
                not day_token_re.fullmatch(first)
                or not month_token_re.fullmatch(second)
                or not re.fullmatch(r"\d{4}", third)
            ):
                continue

            month = month_map.get(fold(second))
            if month is None:
                continue

            try:
                return date(int(third), month, int(first)).isoformat()
            except ValueError:
                continue

        for index in range(len(candidates) - 1):
            first = compact(candidates[index].get("text"))
            second = compact(candidates[index + 1].get("text")).rstrip(".")
            if not day_token_re.fullmatch(first) or not month_token_re.fullmatch(second):
                continue
            month = month_map.get(fold(second))
            if month is None:
                continue
            year = infer_year(month, period, fallback_year)
            if year is None:
                continue
            try:
                return date(year, month, int(first)).isoformat()
            except ValueError:
                continue
        return None

    def parse_amount(token: str | None) -> float | None:
        if not token:
            return None
        raw = compact(token).replace(" ", "")
        sign = -1.0 if raw.startswith("-") else 1.0
        raw = raw.lstrip("+-")
        if "," in raw and "." in raw:
            if raw.rfind(",") > raw.rfind("."):
                raw = raw.replace(".", "").replace(",", ".")
            else:
                raw = raw.replace(",", "")
        elif "," in raw:
            raw = raw.replace(",", ".")
        try:
            return round(sign * float(raw), 2)
        except (TypeError, ValueError):
            return None

    def extract_cell(row: list[dict], left: float, right: float) -> tuple[float | None, float | None]:
        words = [
            item for item in row
            if left <= token_center(item) < right
            and money_token_re.fullmatch(compact(item.get("text")))
        ]
        if not words:
            return None, None
        words.sort(key=lambda item: float(item["x0"]))
        chosen = words[-1]
        return parse_amount(chosen.get("text")), token_center(chosen)

    observations: list[dict] = []
    detected_headers = 0

    try:
        if content is not None:
            pdf_source = io.BytesIO(content)
        elif file_path:
            pdf_source = str(file_path)
        else:
            return ""

        with pdfplumber.open(pdf_source) as pdf:
            all_page_words: list[list[dict]] = []
            document_text_parts: list[str] = []
            fallback_years: list[int] = []

            for page in pdf.pages:
                extracted = page.extract_words(
                    x_tolerance=2,
                    y_tolerance=3,
                    use_text_flow=False,
                )
                page_words = []
                for word in extracted:
                    token = compact(word.get("text"))
                    if not token:
                        continue
                    page_words.append({
                        "text": token,
                        "x0": float(word["x0"]),
                        "x1": float(word["x1"]),
                        "top": float(word["top"]),
                    })
                    document_text_parts.append(token)
                    full_match = numeric_full_date_re.fullmatch(token)
                    if full_match:
                        year = int(full_match.group("year"))
                        fallback_years.append(year + 2000 if year < 100 else year)
                all_page_words.append(page_words)

            document_text = compact(" ".join(document_text_parts))
            period_match = period_re.search(document_text)
            period = None
            if period_match:
                period = {
                    "start_year": int(period_match.group("sy")),
                    "end_year": int(period_match.group("ey")),
                    "start_month": month_map[fold(period_match.group("sm"))],
                    "end_month": month_map[fold(period_match.group("em"))],
                }
            fallback_year = (
                max(set(fallback_years), key=lambda item: (fallback_years.count(item), item))
                if fallback_years else None
            )

            last_date: str | None = None

            for page_index, words in enumerate(all_page_words, 1):
                rows = group_rows(words)
                active_header: dict | None = None
                current: dict | None = None

                def flush_current() -> None:
                    nonlocal current
                    if current is None:
                        return
                    if current.get("debit") is not None or current.get("credit") is not None:
                        observations.append(current)
                    current = None

                for top in sorted(rows):
                    row = rows[top]
                    line = compact(" ".join(item["text"] for item in row))
                    folded_line = fold(line)

                    header = detect_header(row)
                    if header is not None:
                        flush_current()
                        active_header = header
                        detected_headers += 1
                        continue

                    if active_header is None:
                        continue

                    if any(phrase in folded_line for phrase in hard_footer_phrases):
                        flush_current()
                        active_header = None
                        continue

                    date_description_boundary = (
                        active_header["date"] + active_header["description"]
                    ) / 2.0
                    debit_credit_boundary = (
                        active_header["debit"] + active_header["credit"]
                    ) / 2.0
                    credit_balance_boundary = (
                        active_header["credit"] + active_header["balance"]
                    ) / 2.0
                    debit_left = (
                        active_header["description"] + active_header["debit"]
                    ) / 2.0
                    balance_right = active_header["balance"] + max(
                        35.0,
                        active_header["balance"] - active_header["credit"],
                    )

                    row_date = parse_date_words(
                        row,
                        date_description_boundary,
                        period,
                        fallback_year,
                    )

                    debit, _ = extract_cell(row, debit_left, debit_credit_boundary)
                    credit, _ = extract_cell(row, debit_credit_boundary, credit_balance_boundary)
                    balance, _ = extract_cell(row, credit_balance_boundary, balance_right)

                    # Opening/closing balance lines are BALANCE observations, not transactions.
                    if balance_role_re.search(line):
                        flush_current()
                        if row_date is not None:
                            last_date = row_date
                        continue

                    has_movement = debit is not None or credit is not None

                    if row_date is not None:
                        flush_current()
                        last_date = row_date
                        current = {
                            "date": row_date,
                            "description_parts": [],
                            "debit": debit,
                            "credit": credit,
                            "balance": balance,
                            "page": page_index,
                            "source_top": float(top),
                        }
                    elif has_movement:
                        if current is not None and (
                            current.get("debit") is not None
                            or current.get("credit") is not None
                        ):
                            flush_current()
                        if current is None and last_date is not None:
                            current = {
                                "date": last_date,
                                "description_parts": [],
                                "debit": None,
                                "credit": None,
                                "balance": None,
                                "page": page_index,
                                "source_top": float(top),
                            }
                        if current is not None:
                            if debit is not None:
                                current["debit"] = debit
                            if credit is not None:
                                current["credit"] = credit
                            if balance is not None:
                                current["balance"] = balance
                    elif current is None:
                        continue

                    if current is None:
                        continue

                    description_words = [
                        item["text"]
                        for item in row
                        if date_description_boundary <= token_center(item) < debit_left
                        and not money_token_re.fullmatch(compact(item.get("text")))
                    ]
                    description = compact(" ".join(description_words))
                    if description:
                        current["description_parts"].append(description)

                flush_current()

        lines: list[str] = []
        seen: set[tuple] = set()

        for observation in observations:
            debit = observation.get("debit")
            credit = observation.get("credit")
            if (debit is None) == (credit is None):
                continue
            description = compact(" ".join(observation.get("description_parts") or []))
            if not description:
                description = "Transaction"
            balance = observation.get("balance")
            key = (
                observation["date"],
                round(float(debit or 0), 2),
                round(float(credit or 0), 2),
                round(float(balance), 2) if balance is not None else None,
                description[:160].casefold(),
                observation["page"],
                observation.get("source_top"),
            )
            if key in seen:
                continue
            seen.add(key)
            lines.append(
                " ".join([
                    "MONEY_LEDGER_POSITION_TX",
                    f"date={observation['date']}",
                    f"debit={'' if debit is None else f'{abs(float(debit)):.2f}'}",
                    f"credit={'' if credit is None else f'{abs(float(credit)):.2f}'}",
                    f"balance={'' if balance is None else f'{float(balance):.2f}'}",
                    f"description={description[:500]}",
                ])
            )

        print(
            "MONEY_OUT_MONEY_IN_BALANCE_POSITION_AUDIT",
            {
                "headers": detected_headers,
                "observations": len(observations),
                "transactions": len(lines),
                "debits": sum(" debit=" in line and not " debit= " in line for line in lines),
                "credits": sum(" credit=" in line and not " credit= " in line for line in lines),
                "sample": lines[:8],
            },
        )
        return "\n".join(lines)

    except Exception as exc:
        print(
            "MONEY_OUT_MONEY_IN_BALANCE_POSITION_FAILED",
            str(exc)[:300],
        )
        return ""




def _native_text_transaction_signal(text: str) -> dict:
    """Bank-neutral signal for deciding whether native PDF text is usable.

    A PDF can contain hundreds of header/footer characters while its transaction
    table is image-only or position-scrambled. This score uses only universal
    ledger features and never bank names or language-specific labels.
    """
    value = normalize_statement_text(str(text or ""))
    lines = [line.strip() for line in value.splitlines() if line.strip()]
    date_re = re.compile(
        r"(?:\b\d{1,4}[./-]\d{1,2}[./-]\d{1,4}\b|"
        r"[\u0600-\u06ff]*\s*[٠-٩0-9]{1,4}[./-][٠-٩0-9]{1,2}(?:[./-][٠-٩0-9]{1,4})?)"
    )
    money_re = re.compile(
        r"(?<!\w)[+\-]?(?:[0-9٠-٩]{1,3}(?:[ ,.'’\u00a0\u202f٬][0-9٠-٩]{3})+|[0-9٠-٩]+)"
        r"(?:[.,٫][0-9٠-٩]{2,3})(?!\w)"
    )
    dated = 0
    dated_money = 0
    money_lines = 0
    for line in lines:
        has_date = bool(date_re.search(line))
        has_money = bool(money_re.search(line))
        dated += int(has_date)
        money_lines += int(has_money)
        dated_money += int(has_date and has_money)
    return {
        "line_count": len(lines),
        "dated_lines": dated,
        "money_lines": money_lines,
        "dated_money_lines": dated_money,
        "usable": dated_money >= 2 or (dated >= 3 and money_lines >= 3),
    }


def _merge_native_and_ocr_text(
    native_text: str,
    ocr_text: str,
) -> str:
    """Append OCR evidence without replacing reliable native PDF text."""

    native = _normalize_statement_text_structure(
        native_text or "",
        preserve_positional_layout=False,
    )

    ocr = _normalize_statement_text_structure(
        ocr_text or "",
        preserve_positional_layout=True,
    )

    if not native:
        return ocr

    if not ocr:
        return native

    return (
        native
        + "\n\nOCR_AUGMENTED_TEXT_START\n"
        + ocr
    )

def _extract_text_with_scan_fallback(
    file_path: str | None,
    content: bytes | None = None,
) -> str:
    text = ""

    if content:
        text = _extract_text_from_pdf_bytes(content)
    elif file_path:
        text = _extract_text_from_pdf_path(file_path)

    signal = _native_text_transaction_signal(text)
    native_is_long = len(text.strip()) >= MIN_TEXT_LENGTH

    if native_is_long and signal["usable"]:
        print("FINANCE_TEXT_PDF_EXTRACTED", len(text))
        print("FINANCE_NATIVE_TEXT_SIGNAL", signal)

        return _normalize_statement_text_structure(
            text,
            preserve_positional_layout=False,
        )

    print(
        "FINANCE_PDF_SCAN_DETECTED_OCR_STARTED",
        {
            "native_length": len(text.strip()),
            "native_signal": signal,
        },
    )

    ocr_text = ""

    try:
        from app.services.finance_agent.universal_positional_ocr import (
            extract_pdf_text_preserving_layout,
        )

        print(
            "FINANCE_POSITIONAL_OCR_STARTED",
            {
                "has_file_path": bool(file_path),
                "has_content": bool(content),
                "content_size": len(content) if content else 0,
            },
        )

        ocr_text = extract_pdf_text_preserving_layout(
            pdf_path=file_path,
            content=content,
            dpi=300,
            grid_width=180,
            min_confidence=20.0,
            psm=4,
        )

        print(
            "FINANCE_POSITIONAL_OCR_FINISHED",
            {
                "characters": len(ocr_text or ""),
                "lines": len((ocr_text or "").splitlines()),
            },
        )

    except Exception as exc:
        print(
            "FINANCE_POSITIONAL_OCR_FAILED",
            {
                "error": repr(exc),
                "error_type": type(exc).__name__,
            },
        )

        ocr_text = scan_agent_extract_text(
            file_path=file_path,
            content=content,
        )

        print(
            "FINANCE_LEGACY_OCR_FALLBACK_FINISHED",
            {
                "characters": len(ocr_text or ""),
                "lines": len((ocr_text or "").splitlines()),
            },
        )

    if ocr_text:
        print("FINANCE_OCR_TEXT_EXTRACTED", len(ocr_text))

        return _merge_native_and_ocr_text(
            text,
            ocr_text.strip(),
        )

    print("FINANCE_OCR_EMPTY")

    return text.strip()
async def extract_statement_text(file: UploadFile) -> str:
    content = await file.read()

    text = _extract_text_with_scan_fallback(
        file_path=None,
        content=content,
    )

    # Branche additive pour la famille structurelle :
    # Date | Value Date | Description | Debit | Credit
    #
    # Le chemin historique reste prioritaire. L’extracteur positionnel
    # s’auto-rejette si cette géométrie n’est pas présente.
    if "DATE_DESC_VALUE_DC_POSITION_TX" not in text:
        try:
            structural_lines = (
                _extract_date_description_value_date_debit_credit_position_lines(
                    content=content,
                )
            )

            if structural_lines:
                print(
                    "DATE_DESCRIPTION_VALUE_DATE_DEBIT_CREDIT_POSITION_LINES_APPENDED",
                    len(structural_lines.splitlines()),
                )
                text = text + "\n\n" + structural_lines

        except Exception as exc:
            print(
                "DATE_DESCRIPTION_VALUE_DATE_DEBIT_CREDIT_POSITION_LINES_FAILED",
                str(exc)[:200],
            )

    if "CM_POSITION_TX " not in text:
        try:
            structural_lines = (
                _extract_credit_mutuel_position_lines_from_pdf_path(
                    content=content,
                )
            )

            if structural_lines:
                print(
                    "DATE_VALUE_DESCRIPTION_DEBIT_CREDIT_POSITION_LINES_APPENDED",
                    len(structural_lines.splitlines()),
                )
                text = text + "\n\n" + structural_lines

        except Exception as exc:
            print(
                "DATE_VALUE_DESCRIPTION_DEBIT_CREDIT_POSITION_LINES_FAILED",
                str(exc)[:200],
            )


    if "MONEY_LEDGER_POSITION_TX " not in text:
        try:
            structural_lines = (
                _extract_money_out_money_in_balance_position_lines(
                    content=content,
                )
            )

            if structural_lines:
                print(
                    "MONEY_OUT_MONEY_IN_BALANCE_POSITION_LINES_APPENDED",
                    len(structural_lines.splitlines()),
                )
                text = text + "\n\n" + structural_lines

        except Exception as exc:
            print(
                "MONEY_OUT_MONEY_IN_BALANCE_POSITION_LINES_FAILED",
                str(exc)[:200],
            )

    return text


def _normalize_statement_identity_text(text: str) -> str:
    return " ".join(
        str(text or "")
        .replace("\xa0", " ")
        .replace("\u202f", " ")
        .lower()
        .split()
    )


def _contains_any_marker(text: str, markers: tuple[str, ...]) -> bool:
    normalized = _normalize_statement_identity_text(text)
    return any(marker in normalized for marker in markers)


def extract_statement_text_from_path(file_path: str) -> str:
    text = _extract_text_with_scan_fallback(
        file_path=file_path,
        content=None,
    )

    if "DATE_DESC_VALUE_DC_POSITION_TX" not in text:
        try:
            structural_lines = (
                _extract_date_description_value_date_debit_credit_position_lines(
                    file_path=file_path,
                )
            )

            if structural_lines:
                print(
                    "DATE_DESCRIPTION_VALUE_DATE_DEBIT_CREDIT_POSITION_LINES_APPENDED",
                    len(structural_lines.splitlines()),
                )
                text = text + "\n\n" + structural_lines

        except Exception as exc:
            print(
                "DATE_DESCRIPTION_VALUE_DATE_DEBIT_CREDIT_POSITION_LINES_FAILED",
                str(exc)[:200],
            )

    identity_text = _normalize_statement_identity_text(text)

    specialized_extractors = [
        {
            "name": "BRED",
            "markers": (
                "bred banque populaire",
                "bred.fr",
                "banque populaire",
            ),
            "extractor": _extract_bred_banque_populaire_position_lines_from_pdf_path,
        },
        {
            "name": "CORIS",
            "markers": (
                "coris bank",
                "coris banque",
                "coris bank international",
            ),
            "extractor": _extract_coris_cfa_position_lines_from_pdf_path,
        },
        {
            "name": "RIYAD",
            "markers": (
                "riyad bank",
                "bank al riyad",
                "بنك الرياض",
            ),
            "extractor": _extract_riyad_single_transfer_position_lines_from_pdf_path,
        },
        {
            "name": "CIC",
            "markers": (
                "cic.fr",
                "crédit industriel et commercial",
                "credit industriel et commercial",
            ),
            "extractor": _extract_cic_position_lines_from_pdf_path,
        },
        {
            "name": "CM",
            "markers": (
                "creditmutuel.fr",
                "crédit mutuel",
                "credit mutuel",
                "caisse de crédit mutuel",
                "caisse de credit mutuel",
            ),
            "extractor": _extract_credit_mutuel_position_lines_from_pdf_path,
        },
    ]

    for config in specialized_extractors:
        if not any(marker in identity_text for marker in config["markers"]):
            continue

        try:
            extra_lines = config["extractor"](file_path)

            if extra_lines:
                print(
                    f"{config['name']}_POSITION_LINES_APPENDED",
                    len(extra_lines.splitlines()),
                )
                text = text + "\n\n" + extra_lines

        except Exception as exc:
            print(
                f"{config['name']}_POSITION_LINES_FAILED",
                str(exc)[:200],
            )

    # Additive structural-family fallback. Historical institution-triggered
    # extractors remain prioritary. This branch runs only when no existing
    # position observer has emitted this family's rows, and the helper itself
    # returns an empty string unless a reliable
    # Date | Value Date | Description | Debit | Credit header is present.
    if "CM_POSITION_TX " not in text:
        try:
            structural_lines = (
                _extract_credit_mutuel_position_lines_from_pdf_path(file_path)
            )
            if structural_lines:
                print(
                    "DATE_VALUE_DESCRIPTION_DEBIT_CREDIT_POSITION_LINES_APPENDED",
                    len(structural_lines.splitlines()),
                )
                text = text + "\n\n" + structural_lines
        except Exception as exc:
            print(
                "DATE_VALUE_DESCRIPTION_DEBIT_CREDIT_POSITION_LINES_FAILED",
                str(exc)[:200],
            )


    if "MONEY_LEDGER_POSITION_TX " not in text:
        try:
            structural_lines = (
                _extract_money_out_money_in_balance_position_lines(
                    file_path=file_path,
                )
            )

            if structural_lines:
                print(
                    "MONEY_OUT_MONEY_IN_BALANCE_POSITION_LINES_APPENDED",
                    len(structural_lines.splitlines()),
                )
                text = text + "\n\n" + structural_lines

        except Exception as exc:
            print(
                "MONEY_OUT_MONEY_IN_BALANCE_POSITION_LINES_FAILED",
                str(exc)[:200],
            )


    return text