import os
import uuid
from fastapi import UploadFile

UPLOAD_DIR = "uploads"
MAX_FILE_SIZE = 10 * 1024 * 1024

ALLOWED_EXTENSIONS = {"pdf", "docx", "txt"}
ALLOWED_CONTENT_TYPES = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "text/plain",
}


def save_upload_file(file: UploadFile) -> str:
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    if not file.filename or "." not in file.filename:
        raise ValueError("Invalid file name")

    extension = file.filename.rsplit(".", 1)[-1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError("File type not allowed")

    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise ValueError("Invalid file content type")

    content = file.file.read()

    if len(content) > MAX_FILE_SIZE:
        raise ValueError("File too large")

    unique_name = f"{uuid.uuid4()}.{extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_name)

    with open(file_path, "wb") as buffer:
        buffer.write(content)

    file.file.seek(0)

    return file_path