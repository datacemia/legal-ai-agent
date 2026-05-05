import hashlib
import json
import time
from pathlib import Path

from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.utils.security import get_current_user
from app.models.user import User
from app.models.study_analysis import StudyAnalysis
from app.schemas.study_schema import StudyHistoryItem

from app.services.study_agent.study_parser import extract_study_text
from app.services.study_agent.study_ai_agent import analyze_study_content

router = APIRouter(prefix="/study", tags=["Study"])


# =========================
# 🔥 CACHE
# =========================
CACHE_DIR = Path("cache/study_results")
CACHE_DIR.mkdir(parents=True, exist_ok=True)

CACHE_TTL_SECONDS = 7 * 24 * 60 * 60  # 7 days


def make_study_cache_key(file_bytes: bytes, education_level: str, output_language: str) -> str:
    file_hash = hashlib.sha256(file_bytes).hexdigest()
    raw_key = f"{file_hash}:{education_level}:{output_language}"
    return hashlib.sha256(raw_key.encode("utf-8")).hexdigest()


def get_cached_study_result(cache_key: str):
    cache_file = CACHE_DIR / f"{cache_key}.json"

    if not cache_file.exists():
        return None

    # 🔥 TTL check
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

    cache_key = make_study_cache_key(
        file_bytes=file_bytes,
        education_level=education_level,
        output_language=output_language,
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
    result = analyze_study_content(text, education_level, output_language)

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
        result=json.dumps(result, ensure_ascii=False),
    )

    db.add(analysis)
    db.commit()
    db.refresh(analysis)

    return result


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
            "result": json.loads(a.result),
            "created_at": a.created_at,
        }
        for a in analyses
    ]