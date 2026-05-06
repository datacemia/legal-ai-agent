import time
from datetime import datetime

from app.database import SessionLocal
from app.models.job import Job

from app.services.study_agent.study_ai_agent import analyze_study_content
from app.services.study_agent.study_audio_service import generate_study_audio


def process_job(job: Job, db):
    if job.job_type == "study_audio":
        audio_path = generate_study_audio(
            text=job.input.get("text", ""),
            language=job.input.get("language", "en"),
            voice=job.input.get("voice"),
        )

        return {"audio_path": audio_path}

    if job.job_type == "study_ai":
        result = analyze_study_content(
            text=job.input.get("text", ""),
            education_level=job.input.get("education_level", "university"),
            output_language=job.input.get("output_language", "en"),
            weak_points=job.input.get("weak_points", []),
        )

        return result

    raise ValueError(f"Unknown job type: {job.job_type}")


def run_worker():
    print("Worker started")

    while True:
        db = SessionLocal()

        try:
            job = (
                db.query(Job)
                .filter(Job.status == "pending")
                .order_by(Job.created_at.asc())
                .first()
            )

            if not job:
                time.sleep(2)
                continue

            job.status = "running"
            job.started_at = datetime.utcnow()
            job.attempts += 1
            db.commit()
            db.refresh(job)

            try:
                result = process_job(job, db)

                job.status = "completed"
                job.result = result
                job.completed_at = datetime.utcnow()
                db.commit()

            except Exception as e:
                job.status = "failed"
                job.error = str(e)
                job.completed_at = datetime.utcnow()
                db.commit()

        finally:
            db.close()


if __name__ == "__main__":
    run_worker()