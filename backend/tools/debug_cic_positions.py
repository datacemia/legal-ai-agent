from pathlib import Path
import pdfplumber

pdf = Path("ejjami/cic.pdf")

with pdfplumber.open(pdf) as p:
    for page_i, page in enumerate(p.pages, 1):
        print("\n===== PAGE", page_i, "=====")
        words = page.extract_words(
            x_tolerance=2,
            y_tolerance=3,
            keep_blank_chars=False,
            use_text_flow=False,
        )

        for w in words:
            txt = w["text"]
            if any(k in txt.upper() for k in [
                "VIR", "PRLV", "PAIEMENT", "METRO", "BELISOFT",
                "TOTAL", "SOLDE", "3.342", "2.187", "5.529", "5.776",
                "92,10", "32,10", "1", "500,00"
            ]):
                print(
                    f'p{page_i} x0={w["x0"]:.1f} x1={w["x1"]:.1f} '
                    f'top={w["top"]:.1f} bottom={w["bottom"]:.1f} text={txt!r}'
                )
