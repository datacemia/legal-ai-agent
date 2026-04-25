ALLOWED_EXTENSIONS = ["pdf", "docx"]
MAX_FILE_SIZE_MB = 10


def validate_file(filename: str, file_size: int):
    extension = filename.split(".")[-1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError("Only PDF and DOCX files are allowed")

    max_size_bytes = MAX_FILE_SIZE_MB * 1024 * 1024

    if file_size > max_size_bytes:
        raise ValueError("File is too large")

    return extension