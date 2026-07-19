from pathlib import Path
import re
import pdfplumber

pdf = Path("ejjami/banque populare 1 france.pdf")

money_re = re.compile(r"^\d{1,3}(?:[ .]\d{3})*,\d{2}$|^\d+,\d{2}$")
date_re = re.compile(r"^\d{2}\.\d{2}$")


def parse_amount(s):
    return float(s.replace(".", "").replace(" ", "").replace(",", "."))


def iso(ddmm, year=2025):
    dd, mm = ddmm.split(".")
    return f"{year}-{mm}-{dd}"


txs = []
last_date = None

with pdfplumber.open(str(pdf)) as p:
    for page_i, page in enumerate(p.pages, 1):
        words = page.extract_words(x_tolerance=2, y_tolerance=3, use_text_flow=False)

        rows = {}
        for w in words:
            top = round(w["top"] / 3) * 3
            rows.setdefault(top, []).append(w)

        in_main = False

        for top in sorted(rows):
            row = sorted(rows[top], key=lambda w: w["x0"])
            texts = [w["text"] for w in row]
            line = " ".join(texts)

            # Ignore rows that are amount + value-date only.
            # Example: "2.500,00 30.01.25"
            if re.fullmatch(
                r"[+-]?\d{1,3}(?:[ .]\d{3})*[,.]\d{2}\s+\d{2}[./-]\d{2}[./-]\d{2,4}",
                line.strip(),
            ):
                continue

            if "Date" in texts and any("Référence" in t for t in texts):
                in_main = True
                continue

            if "Total" in texts and "mouvements" in line:
                break

            if "Relevé" in line and "poste annexe" in line:
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

            debit = parse_amount(debit_tokens[-1]) if debit_tokens else None
            credit = parse_amount(credit_tokens[-1]) if credit_tokens else None

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
                        debit = parse_amount(nearby_debit_tokens[-1])
                        break

                    if nearby_credit_tokens:
                        credit = parse_amount(nearby_credit_tokens[-1])
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
                    debit = parse_amount(m_detail.group(1))

            if debit is None and credit is None:
                continue

            if credit is not None:
                amount = credit
                typ = "income"
            else:
                amount = -debit
                typ = "expense"

            txs.append({
                "date": iso(date),
                "description": desc,
                "amount": round(amount, 2),
                "type": typ,
                "page": page_i,
            })

print("tx", len(txs))
print("income", round(sum(t["amount"] for t in txs if t["amount"] > 0), 2))
print("expenses", round(sum(abs(t["amount"]) for t in txs if t["amount"] < 0), 2))

for t in txs:
    print(t)