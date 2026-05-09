import json
from pathlib import Path

from app.models.job import Job
from app.models.study_analysis import StudyAnalysis

from app.services.study_agent.study_ai_agent import analyze_study_content
from app.services.study_agent.study_audio_service import generate_study_audio
from app.workers.progress import update_job_progress


CACHE_DIR = Path("cache/study_results")
CACHE_DIR.mkdir(parents=True, exist_ok=True)


def get_job_input(job: Job) -> dict:
    """
    Safely read job input data.

    Some parts of the app create jobs using the field `input_data`.
    Older code may still use `input`. This helper supports both without
    breaking existing jobs.
    """
    data = getattr(job, "input_data", None)

    if data is None:
        data = getattr(job, "input", None)

    if isinstance(data, str):
        try:
            data = json.loads(data)
        except Exception:
            data = {}

    return data if isinstance(data, dict) else {}


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
    update_job_progress(job, db, 20, "Generating study audio...")

    input_data = get_job_input(job)

    result = generate_study_audio(
        text=input_data.get("text", ""),
        language=input_data.get("language", "en"),
        voice=input_data.get("voice"),
    )

    update_job_progress(job, db, 95, "Audio ready.")

    return result


def handle_study_ai(job: Job, db):
    update_job_progress(job, db, 20, "Analyzing study content...")

    input_data = get_job_input(job)

    result = analyze_study_content(
        text=input_data.get("text", ""),
        education_level=input_data.get("education_level", "university"),
        output_language=input_data.get("output_language", "en"),
        weak_points=input_data.get("weak_points", []),
    )

    update_job_progress(job, db, 75, "Saving study result...")

    cache_key = input_data.get("cache_key")
    file_name = input_data.get("file_name", "study_document")

    save_study_result_cache(cache_key, result)

    update_job_progress(job, db, 85, "Saving study history...")

    analysis = StudyAnalysis(
        user_id=job.user_id,
        file_name=file_name,
        result=result,
    )

    db.add(analysis)
    db.commit()
    db.refresh(analysis)

    update_job_progress(job, db, 95, "Finalizing...")

    return result
