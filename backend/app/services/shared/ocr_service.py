import io
import os
import re

import fitz
import pytesseract
from PIL import Image
from langdetect import detect
from openai import OpenAI


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


TESSERACT_CMD = os.getenv("TESSERACT_CMD")
OCR_LANGS = os.getenv("OCR_LANGS", "ara+fra+eng")
OCR_CONFIG = os.getenv(
    "OCR_CONFIG",
    "--oem 3 --psm 4 -c preserve_interword_spaces=1",
)

if TESSERACT_CMD:
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD
elif os.name == "nt":
    pytesseract.pytesseract.tesseract_cmd = (
        r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    )


def fix_arabic_word_spacing(text: str) -> str:
    text = re.sub(r"\bال\s+([اأإآء-ي])", r"ال\1", text)
    text = re.sub(r"\b([لبكفو])\s+([اأإآ])", r"\1\2", text)
    return text


def fix_latin_spacing(text: str) -> str:
    text = re.sub(r"([a-zà-ÿ])([A-Z])", r"\1 \2", text)
    text = re.sub(r"([A-Z]+)([A-Z][a-zà-ÿ])", r"\1 \2", text)
    return text


def remove_ocr_noise(text: str) -> str:
    arabic_chars = len(re.findall(r"[\u0600-\u06FF]", text))
    latin_chars = len(re.findall(r"[A-Za-z]", text))

    if arabic_chars > latin_chars:
        text = re.sub(r"\b[A-Za-z]{2,}\b", " ", text)

    return text


def normalize_ocr_text(text: str) -> str:
    replacements = {
        "\x00": " ",
        "\u200f": "",
        "\u200e": "",
        "\ufeff": "",
        "ﻻ": "لا",
        "ﻷ": "لأ",
        "ﻹ": "لإ",
        "ﻵ": "لآ",
        "ﻼ": "لا",
        "ـ": "",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    text = fix_latin_spacing(text)
    text = fix_arabic_word_spacing(text)
    text = remove_ocr_noise(text)
    text = re.sub(r"[ \t]+", " ", text)

    return text.strip()


def clean_extracted_text(text: str) -> str:
    text = normalize_ocr_text(text)

    lines = []

    for line in text.splitlines():
        line = line.strip()

        if line:
            lines.append(" ".join(line.split()))

    return "\n".join(lines)


def detect_language(text: str) -> str:
    try:
        return detect(text)
    except Exception:
        return "unknown"


def ai_clean_text(text: str, lang: str) -> str:
    if len(text) < 200:
        return text

    prompt = f"""
Clean this OCR text in {lang}.

Rules:
- Fix spacing issues
- Fix broken words
- Remove noise
- Keep original meaning
- DO NOT summarize
- DO NOT translate

Text:
{text[:4000]}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=0.1,
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print("AI cleaning error:", e)
        return text


def extract_scanned_pdf_text(content: bytes) -> str:
    pdf = fitz.open(stream=content, filetype="pdf")
    pages_text = []

    print("OCR pages count:", len(pdf))

    for index, page in enumerate(pdf, start=1):
        print(f"OCR page {index}...")

        pix = page.get_pixmap(matrix=fitz.Matrix(3, 3))
        img = Image.open(io.BytesIO(pix.tobytes("png")))

        text = pytesseract.image_to_string(
            img,
            lang=OCR_LANGS,
            config=OCR_CONFIG,
        )

        print(f"OCR raw length page {index}:", len(text or ""))

        text = clean_extracted_text(text)

        print(f"OCR cleaned length page {index}:", len(text or ""))

        if text:
            pages_text.append(text)

    pdf.close()

    return "\n\n".join(pages_text)


def extract_pdf_text(content: bytes) -> str:
    pdf = fitz.open(stream=content, filetype="pdf")
    pages_text = []

    print("PDF pages count:", len(pdf))

    for index, page in enumerate(pdf, start=1):
        text = page.get_text("text", sort=True)

        print(f"Normal raw length page {index}:", len(text or ""))

        text = clean_extracted_text(text)

        print(f"Normal cleaned length page {index}:", len(text or ""))

        if text:
            pages_text.append(text)

    pdf.close()

    return "\n\n".join(pages_text)
