from pathlib import Path
import re
import pdfplumber

pdf = Path("ejjami/cic.pdf")

money_re = re.compile(r"^\d{1,3}(?:[ .]\d{3})*,\d{2}$|^\d+,\d{2}$")
date_re = re.compile(r"^\d{2}/\d{2}/\d{4}$")


def parse_amount(s: str) -> float:
    return float(str(s).replace(".", "").replace(" ", "").replace(",", "."))


txs = []

with pdfplumber.open(pdf) as p:
    for page_i, page in enumerate(p.pages, 1):
        words = page.extract_words(
            x_tolerance=2,
            y_tolerance=3,
            use_text_flow=False,
        )

        rows = {}
        for w in words:
            top = round(w["top"] / 3) * 3
            rows.setdefault(top, []).append(w)

        for top in sorted(rows):
            row = sorted(rows[top], key=lambda w: w["x0"])
            texts = [w["text"] for w in row]

            dates = [t for t in texts if date_re.match(t)]
            if not dates:
                continue

            desc_words = [
                w["text"]
                for w in row
                if 145 <= w["x0"] <= 310
                and not date_re.match(w["text"])
            ]

            desc = " ".join(desc_words).strip()
            if not desc:
                continue

            if "SOLDE" in desc.upper() or "TOTAL" in desc.upper():
                continue

            debit_tokens = [
                w["text"]
                for w in row
                if 430 <= w["x0"] <= 475
                and re.match(r"^\d", w["text"])
            ]

            credit_tokens = [
                w["text"]
                for w in row
                if 505 <= w["x0"] <= 550
                and re.match(r"^\d", w["text"])
            ]

            debit_text = "".join(debit_tokens).replace(" ", "")
            credit_text = "".join(credit_tokens).replace(" ", "")

            debit = parse_amount(debit_text) if money_re.match(debit_text) else None
            credit = parse_amount(credit_text) if money_re.match(credit_text) else None

            if debit is None and credit is None:
                continue

            if debit is not None:
                amount = -debit
                typ = "expense"
            else:
                amount = credit
                typ = "income"

            txs.append({
                "date": dates[0],
                "description": desc,
                "amount": round(amount, 2),
                "type": typ,
                "page": page_i,
            })

print("tx", len(txs))
print("income", round(sum(abs(t["amount"]) for t in txs if t["type"] == "income"), 2))
print("expenses", round(sum(abs(t["amount"]) for t in txs if t["type"] == "expense"), 2))

for t in txs:
    print(t)