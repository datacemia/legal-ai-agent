import fitz


def scan_agent_extract_text(
    file_path: str | None = None,
    content: bytes | None = None,
) -> str:
    """
    Safe OCR placeholder for scanned PDFs.

    For now, it does not perform real OCR.
    It prevents import errors and keeps finance worker stable.
    Later, plug real OCR here.
    """
    text = ""

    try:
        if content:
            with fitz.open(stream=content, filetype="pdf") as doc:
                for page in doc:
                    text += page.get_text() or ""
                    text += "\n"

        elif file_path:
            with fitz.open(file_path) as doc:
                for page in doc:
                    text += page.get_text() or ""
                    text += "\n"

    except Exception as e:
        print("SCAN_AGENT_EXTRACT_FAILED", str(e))
        return ""

    return text.strip()