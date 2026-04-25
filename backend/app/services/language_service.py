from langdetect import detect, LangDetectException


SUPPORTED_LANGUAGES = ["en", "fr", "ar"]


def detect_language(text: str) -> str:
    if not text or len(text.strip()) < 20:
        return "en"

    try:
        language = detect(text)
    except LangDetectException:
        return "en"

    if language in SUPPORTED_LANGUAGES:
        return language

    return "en"