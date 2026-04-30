from fastapi import UploadFile
import fitz


async def extract_statement_text(file: UploadFile) -> str:
    content = await file.read()

    text = ""

    with fitz.open(stream=content, filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()

    return text