import json

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


@router.post("/analyze")
async def analyze_study(
    file: UploadFile = File(...),
    education_level: str = Form(...),
    output_language: str = Form("en"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # 🔥 FIX: support PDF + DOCX (rien d'autre changé)
    if not file.filename or not file.filename.lower().endswith((".pdf", ".docx")):
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are allowed.",
        )

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

    result = analyze_study_content(text, education_level, output_language)

    analysis = StudyAnalysis(
        user_id=current_user.id,
        file_name=file.filename,
        result=json.dumps(result, ensure_ascii=False),
    )

    db.add(analysis)
    db.commit()
    db.refresh(analysis)

    return result


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