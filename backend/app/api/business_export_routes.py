import json
import os
from datetime import datetime
from pathlib import Path
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.business_analysis import BusinessAnalysis
from app.models.user import User
from app.services.business_agent.business_pdf_report_service import (
    build_business_pdf_report,
)
from app.services.business_agent.business_pptx_report_service import (
    build_business_pptx_report,
)
from app.utils.security import get_current_user


router = APIRouter(
    prefix="/business/export",
    tags=["Business Export"],
)


REPORTS_DIR = Path("generated_reports/business")


def _ensure_reports_dir() -> Path:
    REPORTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    return REPORTS_DIR


def _load_analysis_or_404(
    analysis_id: int,
    db: Session,
    current_user: User,
) -> BusinessAnalysis:
    analysis = (
        db.query(BusinessAnalysis)
        .filter(
            BusinessAnalysis.id == analysis_id,
            BusinessAnalysis.user_id == current_user.id,
        )
        .first()
    )

    if not analysis:
        raise HTTPException(
            status_code=404,
            detail="Business analysis not found.",
        )

    return analysis


def _parse_analysis_result(
    analysis: BusinessAnalysis,
) -> dict:
    try:
        payload = json.loads(analysis.result)

        if not isinstance(payload, dict):
            raise ValueError("Stored result is not a JSON object.")

        return payload

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Stored business analysis result is invalid.",
        )


def _safe_report_file_name(
    analysis_id: int,
    extension: Literal["pdf", "pptx"],
) -> str:
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")

    return f"business_analysis_{analysis_id}_{timestamp}.{extension}"


def _download_response(
    file_path: str | None,
    media_type: str,
    filename: str,
) -> FileResponse:
    if not file_path or not os.path.exists(file_path):
        raise HTTPException(
            status_code=404,
            detail="Generated report file not found.",
        )

    return FileResponse(
        path=file_path,
        media_type=media_type,
        filename=filename,
    )


@router.post("/pdf/{analysis_id}")
def export_business_pdf_report(
    analysis_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Generate and download a PDF executive business report.

    This endpoint is synchronous for now.
    Later it can be moved to Celery/RQ without changing the service contract.
    """

    analysis = _load_analysis_or_404(
        analysis_id=analysis_id,
        db=db,
        current_user=current_user,
    )

    payload = _parse_analysis_result(analysis)

    reports_dir = _ensure_reports_dir()
    file_name = _safe_report_file_name(
        analysis_id=analysis.id,
        extension="pdf",
    )
    output_path = reports_dir / file_name

    pdf_path = build_business_pdf_report(
        analysis=payload,
        output_path=str(output_path),
        language=analysis.output_language
        or payload.get("file_metadata", {}).get("output_language", "en"),
        source_file_name=analysis.file_name,
    )

    analysis.pdf_report_path = pdf_path
    analysis.pdf_generated_at = datetime.utcnow()
    analysis.report_status = "completed"

    db.add(analysis)
    db.commit()
    db.refresh(analysis)

    return _download_response(
        file_path=pdf_path,
        media_type="application/pdf",
        filename=file_name,
    )


@router.post("/pptx/{analysis_id}")
def export_business_pptx_report(
    analysis_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Generate and download a board-ready PowerPoint business report.

    This endpoint is synchronous for now.
    Later it can be moved to Celery/RQ without changing the service contract.
    """

    analysis = _load_analysis_or_404(
        analysis_id=analysis_id,
        db=db,
        current_user=current_user,
    )

    payload = _parse_analysis_result(analysis)

    reports_dir = _ensure_reports_dir()
    file_name = _safe_report_file_name(
        analysis_id=analysis.id,
        extension="pptx",
    )
    output_path = reports_dir / file_name

    pptx_path = build_business_pptx_report(
        analysis=payload,
        output_path=str(output_path),
        language=analysis.output_language
        or payload.get("file_metadata", {}).get("output_language", "en"),
        source_file_name=analysis.file_name,
    )

    analysis.pptx_report_path = pptx_path
    analysis.pptx_generated_at = datetime.utcnow()
    analysis.report_status = "completed"

    db.add(analysis)
    db.commit()
    db.refresh(analysis)

    return _download_response(
        file_path=pptx_path,
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        filename=file_name,
    )


@router.get("/download/{analysis_id}/{kind}")
def download_business_report(
    analysis_id: int,
    kind: Literal["pdf", "pptx"],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Download the latest generated PDF or PPTX report for one analysis.
    """

    analysis = _load_analysis_or_404(
        analysis_id=analysis_id,
        db=db,
        current_user=current_user,
    )

    if kind == "pdf":
        file_path = analysis.pdf_report_path
        media_type = "application/pdf"
        filename = f"business_analysis_{analysis.id}.pdf"

    else:
        file_path = analysis.pptx_report_path
        media_type = "application/vnd.openxmlformats-officedocument.presentationml.presentation"
        filename = f"business_analysis_{analysis.id}.pptx"

    return _download_response(
        file_path=file_path,
        media_type=media_type,
        filename=filename,
    )


@router.get("/status/{analysis_id}")
def get_business_report_export_status(
    analysis_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Return export metadata for dashboard buttons.
    """

    analysis = _load_analysis_or_404(
        analysis_id=analysis_id,
        db=db,
        current_user=current_user,
    )

    return {
        "analysis_id": analysis.id,
        "report_status": analysis.report_status,
        "pdf_available": bool(
            analysis.pdf_report_path
            and os.path.exists(analysis.pdf_report_path)
        ),
        "pptx_available": bool(
            analysis.pptx_report_path
            and os.path.exists(analysis.pptx_report_path)
        ),
        "pdf_generated_at": analysis.pdf_generated_at,
        "pptx_generated_at": analysis.pptx_generated_at,
    }
