import hashlib
from pathlib import Path
from openai import OpenAI

client = OpenAI()

AUDIO_CACHE_DIR = Path("cache/study_audio")
AUDIO_CACHE_DIR.mkdir(parents=True, exist_ok=True)

SUPPORTED_TTS_LANGS = {"en", "fr", "ar"}


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

    if language == "fr":
        return "marin"

    return "marin"


def clean_tts_text(text: str, max_chars: int = 6000) -> str:
    if not isinstance(text, str):
        return ""

    text = " ".join(text.split())
    return text[:max_chars].strip()


def make_audio_cache_key(text: str, language: str, voice: str) -> str:
    raw = f"{language}:{voice}:{text}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def generate_study_audio(
    text: str,
    language: str = "en",
    voice: str | None = None,
) -> str:
    language = normalize_audio_language(language)
    text = clean_tts_text(text)

    if not text:
        raise ValueError("Text is empty")

    voice = voice or get_voice_for_language(language)
    cache_key = make_audio_cache_key(text, language, voice)
    output_path = AUDIO_CACHE_DIR / f"{cache_key}.mp3"

    if output_path.exists():
        return str(output_path)

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
        response.stream_to_file(output_path)

    return str(output_path)