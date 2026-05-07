import time
from datetime import datetime

from app.database import SessionLocal
from app.models.job import Job
from app.models.user import User

from app.workers.handlers.study_handler import (
    handle_study_ai,
    handle_study_audio,
)


def process_job(job: Job, db):
    handlers = {
        "study_audio": handle_study_audio,
        "study_ai": handle_study_ai,
    }

    handler = handlers.get(job.job_type)

    if not handler:
        raise ValueError(f"Unknown job type: {job.job_type}")

    return handler(job, db)


def run_worker():
    print("Worker started", flush=True)

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

            print(f"Processing job {job.id} type={job.job_type}", flush=True)

            job.status = "running"
            job.started_at = datetime.utcnow()
            job.attempts += 1
            db.commit()
            db.refresh(job)

            try:
                result = process_job(job, db)

                job.status = "completed"
                job.result = result
                job.error = None
                job.completed_at = datetime.utcnow()
                db.commit()

                print(f"Completed job {job.id} type={job.job_type}", flush=True)

            except Exception as e:
                job.status = "failed"
                job.error = str(e)
                job.completed_at = datetime.utcnow()
                db.commit()

                print(f"Failed job {job.id} type={job.job_type}: {e}", flush=True)

        finally:
            db.close()


if __name__ == "__main__":
    run_worker()