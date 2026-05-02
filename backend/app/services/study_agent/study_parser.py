import fitz
from fastapi import UploadFile


def fix_arabic_text(text: str) -> str:
    fixed_lines = []

    for line in text.splitlines():
        stripped = line.strip()

        if not stripped:
            continue

        arabic_chars = sum(1 for c in stripped if "\u0600" <= c <= "\u06FF")

        # Si ligne arabe
        if arabic_chars > 3:
            # inversion simple
            reversed_line = stripped[::-1]

            # 🔥 correction minimale des mots inversés
            words = reversed_line.split()

            # inverser chaque mot seulement si nécessaire
            corrected_words = []
            for w in words:
                if len(w) > 2:
                    corrected_words.append(w[::-1])
                else:
                    corrected_words.append(w)

            fixed_line = " ".join(corrected_words)
            fixed_lines.append(fixed_line)

        else:
            fixed_lines.append(stripped)

    return "\n".join(fixed_lines)


async def extract_study_text(file: UploadFile) -> str:
    content = await file.read()

    text = ""

    try:
        pdf = fitz.open(stream=content, filetype="pdf")

        for page in pdf:
            text += page.get_text("text", sort=True) + "\n"

        pdf.close()

        text = text.strip()

        if not text:
            return ""

        text = fix_arabic_text(text)

        print("EXTRACTED TEXT:", text[:500])

        return text.strip()

    except Exception as e:
        print("PDF extraction error:", repr(e))
        return ""