import json
from pathlib import Path

from app.models.job import Job
from app.models.study_analysis import StudyAnalysis

from app.services.study_agent.study_ai_agent import analyze_study_content
from app.services.study_agent.study_audio_service import generate_study_audio


CACHE_DIR = Path("cache/study_results")
CACHE_DIR.mkdir(parents=True, exist_ok=True)


def save_study_result_cache(cache_key: str, result: dict):
    if not cache_key:
        return

    cache_file = CACHE_DIR / f"{cache_key}.json"

    try:
        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print("STUDY CACHE SAVE ERROR:", e)


def handle_study_audio(job: Job, db):
    return generate_study_audio(
        text=job.input.get("text", ""),
        language=job.input.get("language", "en"),
        voice=job.input.get("voice"),
    )


def handle_study_ai(job: Job, db):
    result = analyze_study_content(
        text=job.input.get("text", ""),
        education_level=job.input.get("education_level", "university"),
        output_language=job.input.get("output_language", "en"),
        weak_points=job.input.get("weak_points", []),
    )

    cache_key = job.input.get("cache_key")
    file_name = job.input.get("file_name", "study_document")

    save_study_result_cache(cache_key, result)

    analysis = StudyAnalysis(
        user_id=job.user_id,
        file_name=file_name,
        result=result,
    )

    db.add(analysis)
    db.commit()
    db.refresh(analysis)

    return result