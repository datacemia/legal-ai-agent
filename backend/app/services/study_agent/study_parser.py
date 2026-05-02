import fitz
from fastapi import UploadFile
from docx import Document
from io import BytesIO
from PIL import Image
import pytesseract
import io

# 🔥 IMPORTANT (Windows seulement)
import os

if os.name == "nt":
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def fix_arabic_text(text: str) -> str:
    fixed_lines = []

    for line in text.splitlines():
        stripped = line.strip()

        if not stripped:
            continue

        arabic_chars = sum(1 for c in stripped if "\u0600" <= c <= "\u06FF")

        if arabic_chars > 3:
            reversed_line = stripped[::-1]
            words = reversed_line.split()

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


# ================= DOCX =================

def extract_docx_text(content: bytes) -> str:
    try:
        doc = Document(BytesIO(content))
        text_parts = []

        for para in doc.paragraphs:
            t = para.text.strip()
            if t:
                text_parts.append(t)

        for table in doc.tables:
            for row in table.rows:
                row_text = " | ".join(
                    cell.text.strip() for cell in row.cells if cell.text.strip()
                )
                if row_text:
                    text_parts.append(row_text)

        return "\n".join(text_parts).strip()

    except Exception as e:
        print("DOCX extraction error:", repr(e))
        return ""


# ================= OCR PDF =================

def extract_scanned_pdf_text(content: bytes) -> str:
    text = ""

    try:
        pdf = fitz.open(stream=content, filetype="pdf")

        for page in pdf:
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
            img_bytes = pix.tobytes("png")

            image = Image.open(io.BytesIO(img_bytes))

            page_text = pytesseract.image_to_string(
                image,
                lang="eng+fra+ara"
            )

            if page_text.strip():
                text += page_text + "\n"

        pdf.close()
        return text.strip()

    except Exception as e:
        print("OCR extraction error:", repr(e))
        return ""


# ================= MAIN =================

async def extract_study_text(file: UploadFile) -> str:
    content = await file.read()
    filename = (file.filename or "").lower()

    try:
        # ===== PDF =====
        if filename.endswith(".pdf"):
            text = ""

            pdf = fitz.open(stream=content, filetype="pdf")

            for page in pdf:
                text += page.get_text("text", sort=True) + "\n"

            pdf.close()

            text = text.strip()

            # 🔥 OCR fallback (clé du système)
            if not text or len(text) < 50:
                print("⚠️ SCANNED PDF DETECTED → USING OCR")
                text = extract_scanned_pdf_text(content)

            if not text:
                return ""

            text = fix_arabic_text(text)

            print("EXTRACTED PDF TEXT:", text[:500])
            return text.strip()

        # ===== DOCX =====
        elif filename.endswith(".docx"):
            text = extract_docx_text(content)

            if not text:
                return ""

            text = fix_arabic_text(text)

            print("EXTRACTED DOCX TEXT:", text[:500])
            return text.strip()

        # ===== OTHER =====
        else:
            print("Unsupported file type:", filename)
            return ""

    except Exception as e:
        print("File extraction error:", repr(e))
        return ""