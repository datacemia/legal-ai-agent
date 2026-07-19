from pathlib import Path
import pdfplumber

pdf = Path("ejjami/banque populare 1 france.pdf")

with pdfplumber.open(str(pdf)) as p:
    for page_i, page in enumerate(p.pages, 1):
        print("\n===== PAGE", page_i, "=====")
        words = page.extract_words(x_tolerance=2, y_tolerance=3, use_text_flow=False)

        rows = {}
        for w in words:
            top = round(w["top"] / 3) * 3
            rows.setdefault(top, []).append(w)

        for top in sorted(rows):
            row = sorted(rows[top], key=lambda w: w["x0"])
            txt = " | ".join(f'{w["text"]}@{w["x0"]:.0f}-{w["x1"]:.0f}' for w in row)

            if any(k in txt.lower() for k in [
                "date", "solde", "carte", "virement", "prelevement", "prélèvement",
                "total", "nouveau", "commission", "facture"
            ]):
                print(f"top={top}: {txt}")
