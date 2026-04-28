import pdfplumber
from docx import Document

MAX_PAGES = 20
MAX_CHARS = 200_000


def extract_text_from_pdf(file_path: str) -> str:
    text = ""

    try:
        with pdfplumber.open(file_path) as pdf:
            total_pages = min(len(pdf.pages), MAX_PAGES)

            for i in range(total_pages):
                page = pdf.pages[i]

                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

                if len(text) > MAX_CHARS:
                    break

    except Exception:
        raise ValueError("Failed to process PDF")

    if not text.strip():
        raise ValueError("Empty or unreadable PDF")

    return text.strip()


def extract_text_from_docx(file_path: str) -> str:
    try:
        doc = Document(file_path)
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        text = "\n".join(paragraphs)

    except Exception:
        raise ValueError("Failed to process DOCX")

    if not text.strip():
        raise ValueError("Empty or unreadable DOCX")

    return text.strip()


def extract_text(file_path: str, file_type: str) -> str:
    if file_type == "pdf":
        return extract_text_from_pdf(file_path)

    if file_type == "docx":
        return extract_text_from_docx(file_path)

    raise ValueError("Unsupported file type")