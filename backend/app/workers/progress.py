def update_job_progress(job, db, progress: int, message: str):
    job.progress = max(0, min(progress, 100))
    job.status_message = message
    db.commit()
    db.refresh(job)