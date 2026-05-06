from sqlalchemy.orm import Session
from app.models.job import Job


def create_job(
    db: Session,
    user_id: int,
    job_type: str,
    input_data: dict,
) -> Job:
    job = Job(
        user_id=user_id,
        job_type=job_type,
        status="pending",
        input=input_data,
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    return job