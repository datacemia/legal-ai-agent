import fitz
from fastapi import UploadFile


async def extract_study_text(file: UploadFile) -> str:
    content = await file.read()

    text = ""

    try:
        pdf = fitz.open(stream=content, filetype="pdf")

        for page in pdf:
            text += page.get_text() + "\n"

        pdf.close()

        return text.strip()

    except Exception:
        return ""