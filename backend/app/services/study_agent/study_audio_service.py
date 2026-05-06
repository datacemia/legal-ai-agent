import hashlib
import os
from pathlib import Path

import requests
from openai import OpenAI

client = OpenAI()

AUDIO_CACHE_DIR = Path("cache/study_audio")
AUDIO_CACHE_DIR.mkdir(parents=True, exist_ok=True)

SUPPORTED_TTS_LANGS = {"en", "fr", "ar"}


def get_supabase_credentials():
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

    if not supabase_url or not supabase_key:
        raise ValueError("Missing Supabase storage environment variables")

    return supabase_url, supabase_key


def get_storage_bucket() -> str:
    return os.getenv("SUPABASE_STORAGE_BUCKET", "study-audio")


def normalize_audio_language(language: str) -> str:
    if not isinstance(language, str):
        return "en"

    value = language.strip().lower()

    aliases = {
        "english": "en",
        "anglais": "en",
        "french": "fr",
        "français": "fr",
        "francais": "fr",
        "arabic": "ar",
        "arabe": "ar",
        "العربية": "ar",
    }

    value = aliases.get(value, value)
    return value if value in SUPPORTED_TTS_LANGS else "en"


def get_voice_for_language(language: str) -> str:
    language = normalize_audio_language(language)

    if language == "ar":
        return "cedar"

    return "marin"


def clean_tts_text(text: str, max_chars: int = 6000) -> str:
    if not isinstance(text, str):
        return ""

    text = " ".join(text.split())
    return text[:max_chars].strip()


def make_audio_cache_key(text: str, language: str, voice: str) -> str:
    raw = f"{language}:{voice}:{text}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def upload_audio_to_supabase(local_path: Path, storage_path: str) -> str:
    supabase_url, supabase_key = get_supabase_credentials()
    bucket = get_storage_bucket()

    upload_url = (
        f"{supabase_url}/storage/v1/object/{bucket}/{storage_path}"
    )

    with open(local_path, "rb") as f:
        audio_bytes = f.read()

    response = requests.post(
        upload_url,
        headers={
            "Authorization": f"Bearer {supabase_key}",
            "apikey": supabase_key,
            "Content-Type": "audio/mpeg",
            "x-upsert": "true",
        },
        data=audio_bytes,
        timeout=60,
    )

    if response.status_code not in [200, 201]:
        raise ValueError(
            f"Supabase upload failed: "
            f"{response.status_code} - {response.text}"
        )

    public_url = (
        f"{supabase_url}/storage/v1/object/public/"
        f"{bucket}/{storage_path}"
    )

    return public_url


def generate_study_audio(
    text: str,
    language: str = "en",
    voice: str | None = None,
) -> dict:
    language = normalize_audio_language(language)

    print("SUPABASE_URL exists =", bool(os.getenv("SUPABASE_URL")))
    print(
        "SUPABASE_KEY starts =",
        os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")[:12],
    )
    print(
        "OPENAI_KEY starts =",
        os.getenv("OPENAI_API_KEY", "")[:8],
    )

    text = clean_tts_text(text)

    if not text:
        raise ValueError("Text is empty")

    voice = voice or get_voice_for_language(language)
    cache_key = make_audio_cache_key(text, language, voice)

    local_path = AUDIO_CACHE_DIR / f"{cache_key}.mp3"
    storage_path = f"{language}/{cache_key}.mp3"

    if not local_path.exists():
        instructions = {
            "en": "Speak clearly in a calm educational tone.",
            "fr": "Parle clairement avec un ton pédagogique et calme.",
            "ar": "تحدث بوضوح وبنبرة تعليمية هادئة.",
        }.get(language, "Speak clearly in a calm educational tone.")

        with client.audio.speech.with_streaming_response.create(
            model="gpt-4o-mini-tts",
            voice=voice,
            input=text,
            instructions=instructions,
            response_format="mp3",
        ) as response:
            response.stream_to_file(local_path)

    audio_url = upload_audio_to_supabase(local_path, storage_path)

    return {
        "audio_url": audio_url,
        "storage_path": storage_path,
        "mime_type": "audio/mpeg",
        "filename": "study-audio.mp3",
    }