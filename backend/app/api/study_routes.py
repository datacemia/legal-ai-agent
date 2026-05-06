import hashlib
import json
import time
from pathlib import Path
from typing import List, Dict, Any, Optional

from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.utils.security import get_current_user
from app.models.user import User
from app.models.study_analysis import StudyAnalysis, StudyAttempt
from app.schemas.study_schema import StudyHistoryItem

from app.services.study_agent.study_parser import extract_study_text
from app.services.study_agent.study_ai_agent import analyze_study_content
from app.services.study_agent.study_audio_service import generate_study_audio

router = APIRouter(prefix="/study", tags=["Study"])


# =========================
# 🔥 CACHE
# =========================
CACHE_DIR = Path("cache/study_results")
CACHE_DIR.mkdir(parents=True, exist_ok=True)

CACHE_TTL_SECONDS = 7 * 24 * 60 * 60  # 7 days


class StudyAttemptPayload(BaseModel):
    document_hash: Optional[str] = None
    language: str
    education_level: str
    score: int
    total_questions: int
    correct_answers: int
    answers: List[Dict[str, Any]]


class StudyAudioPayload(BaseModel):
    text: str
    language: str = "en"
    voice: Optional[str] = None


def make_study_cache_key(
    file_bytes: bytes,
    education_level: str,
    output_language: str,
    weak_points: list[str] | None = None,
) -> str:
    file_hash = hashlib.sha256(file_bytes).hexdigest()
    weak_key = "|".join(weak_points or [])

    raw_key = f"{file_hash}:{education_level}:{output_language}:{weak_key}"
    return hashlib.sha256(raw_key.encode("utf-8")).hexdigest()


def get_cached_study_result(cache_key: str):
    cache_file = CACHE_DIR / f"{cache_key}.json"

    if not cache_file.exists():
        return None

    age = time.time() - cache_file.stat().st_mtime

    if age > CACHE_TTL_SECONDS:
        try:
            cache_file.unlink()
            print("STUDY CACHE EXPIRED:", cache_key)
        except Exception:
            pass
        return None

    try:
        with open(cache_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        data["_cached"] = True
        return data

    except Exception:
        return None


def get_user_weak_points(db: Session, user_id: int) -> list[str]:
    attempts = (
        db.query(StudyAttempt)
        .filter(StudyAttempt.user_id == user_id)
        .order_by(StudyAttempt.created_at.desc())
        .limit(10)
        .all()
    )

    weak_points = []

    for attempt in attempts:
        wp = attempt.weak_points

        try:
            if isinstance(wp, str):
                wp = json.loads(wp)

            if isinstance(wp, list):
                weak_points.extend(wp)
        except Exception:
            pass

    cleaned = []
    seen = set()

    for wp in weak_points:
        wp = str(wp).strip()

        if not wp or "???" in wp:
            continue

        key = wp.lower()

        if key not in seen:
            seen.add(key)
            cleaned.append(wp)

    return cleaned[:10]


def save_study_result_cache(cache_key: str, result: dict):
    cache_file = CACHE_DIR / f"{cache_key}.json"

    try:
        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

    except Exception as e:
        print("CACHE SAVE ERROR:", e)


# =========================
# 🚀 ANALYZE
# =========================
@router.post("/analyze")
async def analyze_study(
    file: UploadFile = File(...),
    education_level: str = Form(...),
    output_language: str = Form("en"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not file.filename or not file.filename.lower().endswith((".pdf", ".docx")):
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are allowed.",
        )

    # =========================
    # 🔥 CACHE CHECK
    # =========================
    file_bytes = await file.read()

    user_weak_points = get_user_weak_points(db, current_user.id)

    cache_key = make_study_cache_key(
        file_bytes=file_bytes,
        education_level=education_level,
        output_language=output_language,
        weak_points=user_weak_points,
    )

    cached_result = get_cached_study_result(cache_key)
    if cached_result:
        print("STUDY CACHE HIT:", cache_key)
        return cached_result

    print("STUDY CACHE MISS:", cache_key)

    # ⚠️ reset pointer
    await file.seek(0)

    # =========================
    # 📄 EXTRACTION
    # =========================
    text = await extract_study_text(file)

    print("\n=== FINAL TEXT SENT TO AGENT ===")
    print(text[:1000])
    print("TEXT LENGTH:", len(text))
    print("================================\n")

    if not text.strip():
        raise HTTPException(
            status_code=400,
            detail="Could not extract text from file.",
        )

    # =========================
    # 🧠 AI
    # =========================
    result = analyze_study_content(
        text=text,
        education_level=education_level,
        output_language=output_language,
        weak_points=user_weak_points,
    )

    # =========================
    # 💾 SAVE CACHE
    # =========================
    save_study_result_cache(cache_key, result)

    # =========================
    # 🗄️ DB SAVE
    # =========================
    analysis = StudyAnalysis(
        user_id=current_user.id,
        file_name=file.filename,
        result=result,
    )

    db.add(analysis)
    db.commit()
    db.refresh(analysis)

    return result


# =========================
# 💾 SAVE STUDY ATTEMPT
# =========================
@router.post("/attempt")
def save_study_attempt(
    payload: StudyAttemptPayload,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    weak_points = []

    for answer in payload.answers:
        if not answer.get("is_correct"):
            weak_points.append(
                answer.get("concept")
                or answer.get("question")
                or "Unknown concept"
            )

    attempt = StudyAttempt(
        user_id=current_user.id,
        document_hash=payload.document_hash,
        language=payload.language,
        education_level=payload.education_level,
        score=payload.score,
        total_questions=payload.total_questions,
        correct_answers=payload.correct_answers,
        answers=payload.answers,
        weak_points=weak_points,
    )

    db.add(attempt)
    db.commit()
    db.refresh(attempt)

    return {
        "saved": True,
        "weak_points": weak_points,
    }


# =========================
# 🎯 WEAK POINTS
# =========================
@router.get("/weak-points")
def get_study_weak_points(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    attempts = (
        db.query(StudyAttempt)
        .filter(StudyAttempt.user_id == current_user.id)
        .order_by(StudyAttempt.created_at.desc())
        .limit(10)
        .all()
    )

    weak_points = []

    for attempt in attempts:
        wp = attempt.weak_points

        if not wp:
            continue

        try:
            if isinstance(wp, str):
                wp = json.loads(wp)

            if isinstance(wp, list):
                weak_points.extend(wp)

        except Exception:
            pass

    cleaned = []

    for wp in weak_points:
        if wp and "???" not in wp:
            cleaned.append(str(wp).strip())

    cleaned = list(dict.fromkeys(cleaned))

    return {
        "weak_points": cleaned[:20]
    }


# =========================
# 🔊 GENERATE STUDY AUDIO
# =========================
@router.post("/audio")
def generate_audio(
    payload: StudyAudioPayload,
    current_user: User = Depends(get_current_user),
):
    try:
        audio_path = generate_study_audio(
            text=payload.text,
            language=payload.language,
            voice=payload.voice,
        )

        return FileResponse(
            audio_path,
            media_type="audio/mpeg",
            filename="study-audio.mp3",
        )

    except Exception as e:
        print("STUDY AUDIO ERROR:", e)

        raise HTTPException(
            status_code=500,
            detail="Could not generate audio.",
        )


# =========================
# 📜 HISTORY
# =========================
@router.get("/history", response_model=list[StudyHistoryItem])
def get_study_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    analyses = (
        db.query(StudyAnalysis)
        .filter(StudyAnalysis.user_id == current_user.id)
        .order_by(StudyAnalysis.id.desc())
        .all()
    )

    return [
        {
            "id": a.id,
            "file_name": a.file_name,
            "result": a.result,
            "created_at": a.created_at,
        }
        for a in analyses
    ]