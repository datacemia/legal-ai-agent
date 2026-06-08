import time
from datetime import UTC, datetime

from app.database import SessionLocal
from app.models.user import User
from app.models.job import Job

from app.workers.handlers.study_handler import (
    handle_study_ai,
    handle_study_audio,
)

from app.workers.handlers.contract_handler import (
    handle_contract_ai,
)

from app.workers.handlers.business_handler import (
    handle_business_ai,
)

from app.workers.handlers.finance_handler import (
    handle_finance_ai,
)


def utc_now():
    return datetime.now(UTC)


def process_job(job: Job, db):
    handlers = {
        "study_audio": handle_study_audio,
        "study_ai": handle_study_ai,
        "contract_ai": handle_contract_ai,
        "business_ai": handle_business_ai,
        "finance_ai": handle_finance_ai,
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
                .with_for_update(skip_locked=True)
                .first()
            )

            if not job:
                time.sleep(2)
                continue

            print(f"Processing job {job.id} type={job.job_type}", flush=True)

            job.status = "running"
            job.started_at = utc_now()
            job.attempts += 1
            db.commit()
            db.refresh(job)

            try:
                result = process_job(job, db)

                job.status = "completed"
                job.result = result
                job.error = None
                job.progress = 100
                job.status_message = "Completed"
                job.completed_at = utc_now()
                db.commit()

                print(f"Completed job {job.id} type={job.job_type}", flush=True)

            except Exception as e:
                job.status = "failed"
                job.error = "Business analysis failed."
                job.status_message = "Failed"
                job.completed_at = utc_now()
                db.commit()

                import traceback
                print(traceback.format_exc(), flush=True)
                print(f"Failed job {job.id} type={job.job_type}: {e}", flush=True)

        finally:
            db.close()


if __name__ == "__main__":
    run_worker()
