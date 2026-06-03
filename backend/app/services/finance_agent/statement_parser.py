from fastapi import UploadFile
import fitz
import os


MIN_TEXT_LENGTH = int(os.getenv("FINANCE_MIN_TEXT_LENGTH", "500"))


def _extract_text_from_pdf_bytes(content: bytes) -> str:
    text = ""

    with fitz.open(stream=content, filetype="pdf") as doc:
        for page in doc:
            text += page.get_text() or ""
            text += "\n"

    return text.strip()


def _extract_text_from_pdf_path(file_path: str) -> str:
    text = ""

    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text() or ""
            text += "\n"

    return text.strip()


def _extract_text_with_scan_fallback(file_path: str | None, content: bytes | None = None) -> str:
    text = ""

    if content:
        text = _extract_text_from_pdf_bytes(content)
    elif file_path:
        text = _extract_text_from_pdf_path(file_path)

    if len(text.strip()) >= MIN_TEXT_LENGTH:
        return text

    print("FINANCE_PDF_SCAN_DETECTED_NEEDS_OCR")

    # TODO: brancher ici ton agent scan/OCR réel.
    # Exemple futur:
    # text = your_scan_agent_extract_text(file_path=file_path, content=content)

    return text.strip()


async def extract_statement_text(file: UploadFile) -> str:
    content = await file.read()
    return _extract_text_with_scan_fallback(
        file_path=None,
        content=content,
    )


def extract_statement_text_from_path(file_path: str) -> str:
    return _extract_text_with_scan_fallback(
        file_path=file_path,
        content=None,
    )