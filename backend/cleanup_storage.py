from supabase import create_client

SUPABASE_URL = "https://lygxysonyoyfsbyraxuw.supabase.co"
SERVICE_ROLE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imx5Z3h5c29ueW95ZnNieXJheHV3Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3NzEyMTU2OSwiZXhwIjoyMDkyNjk3NTY5fQ.nDxz4mDhMVSElhHWNVf8EfukvlCHN4n7A6BJBS99Xdo"

supabase = create_client(SUPABASE_URL, SERVICE_ROLE_KEY)

bucket = "runexa-files"
prefixes = ["business/", "finance/", "legal/", "study/", "upload/"]

for prefix in prefixes:
    offset = 0

    while True:
        files = supabase.storage.from_(bucket).list(
            path=prefix.rstrip("/"),
            options={"limit": 100, "offset": offset}
        )

        if not files:
            break

        paths = [f"{prefix}{item['name']}" for item in files]

        print(f"Deleting {len(paths)} files from {prefix}")
        supabase.storage.from_(bucket).remove(paths)

        if len(files) < 100:
            break