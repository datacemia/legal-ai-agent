import os
import tempfile
from pathlib import Path

from fastapi import UploadFile
from supabase import create_client


SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
SUPABASE_STORAGE_BUCKET = os.getenv("SUPABASE_STORAGE_BUCKET", "runexa-files")


def get_supabase_client():
    if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
        raise RuntimeError("Supabase storage environment variables are missing.")

    return create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)


async def upload_api_file_to_cloud(
    file: UploadFile,
    folder: str,
) -> dict:
    client = get_supabase_client()

    ext = Path(file.filename or "").suffix.lower() or ".bin"
    object_path = f"{folder}/{os.urandom(16).hex()}{ext}"

    content = await file.read()

    client.storage.from_(SUPABASE_STORAGE_BUCKET).upload(
        object_path,
        content,
        {
            "content-type": file.content_type or "application/octet-stream",
            "x-upsert": "false",
        },
    )

    return {
        "storage_bucket": SUPABASE_STORAGE_BUCKET,
        "storage_path": object_path,
        "file_name": file.filename,
        "content_type": file.content_type,
        "ext": ext,
    }


def download_api_file_from_cloud(
    storage_path: str,
    suffix: str = ".bin",
) -> str:
    client = get_supabase_client()

    content = client.storage.from_(SUPABASE_STORAGE_BUCKET).download(storage_path)

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    tmp.write(content)
    tmp.close()

    return tmp.name