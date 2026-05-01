import json

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.utils.security import get_current_user
from app.models.user import User
from app.models.business_analysis import BusinessAnalysis
from app.schemas.business_schema import BusinessHistoryItem

from app.services.business_agent.business_parser import extract_business_data
from app.services.business_agent.business_ai_agent import analyze_business_data

router = APIRouter(prefix="/business", tags=["Business"])


@router.post("/analyze")
async def analyze_business(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not file.filename or not (
        file.filename.lower().endswith(".csv")
        or file.filename.lower().endswith(".xlsx")
    ):
        raise HTTPException(
            status_code=400,
            detail="Only CSV or Excel (.xlsx) files are supported for Business Agent.",
        )

    try:
        business_data = await extract_business_data(file)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    if not business_data.strip():
        raise HTTPException(
            status_code=400,
            detail="Could not extract business data from file.",
        )

    result = analyze_business_data(business_data)

    analysis = BusinessAnalysis(
        user_id=current_user.id,
        file_name=file.filename,
        result=json.dumps(result, ensure_ascii=False),
    )

    db.add(analysis)
    db.commit()
    db.refresh(analysis)

    return result


@router.get("/history", response_model=list[BusinessHistoryItem])
def get_business_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    analyses = (
        db.query(BusinessAnalysis)
        .filter(BusinessAnalysis.user_id == current_user.id)
        .order_by(BusinessAnalysis.id.desc())
        .all()
    )

    return [
        {
            "id": analysis.id,
            "file_name": analysis.file_name,
            "result": json.loads(analysis.result),
            "created_at": analysis.created_at,
        }
        for analysis in analyses
    ]