import os

from supabase import create_client


SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
SUPABASE_STORAGE_BUCKET = os.getenv(
    "SUPABASE_STORAGE_BUCKET",
    "uploaded_files",
)


def get_supabase_client():
    if not SUPABASE_URL:
        raise RuntimeError("SUPABASE_URL is not configured.")

    if not SUPABASE_SERVICE_ROLE_KEY:
        raise RuntimeError("SUPABASE_SERVICE_ROLE_KEY is not configured.")

    return create_client(
        SUPABASE_URL,
        SUPABASE_SERVICE_ROLE_KEY,
    )


def get_supabase_public_url(
    *,
    storage_path: str,
) -> str:
    supabase = get_supabase_client()

    return supabase.storage.from_(
        SUPABASE_STORAGE_BUCKET
    ).get_public_url(
        storage_path
    )


def upload_file_to_supabase_storage(
    *,
    local_file_path: str,
    storage_path: str,
    content_type: str | None = None,
) -> dict:
    supabase = get_supabase_client()

    with open(local_file_path, "rb") as file:
        supabase.storage.from_(SUPABASE_STORAGE_BUCKET).upload(
            path=storage_path,
            file=file,
            file_options={
                "content-type": content_type or "application/octet-stream",
                "upsert": "true",
            },
        )

    public_url = get_supabase_public_url(
        storage_path=storage_path,
    )

    return {
        "storage_path": storage_path,
        "public_url": public_url,
    }
