import json

from app.models.job import Job
from app.models.document import Document
from app.models.analysis import AnalysisResult

from app.services.contract_agent.contract_parser import extract_text
from app.services.text_cleaner import clean_text
from app.services.contract_agent.clause_splitter import split_into_clauses
from app.services.language_service import detect_language
from app.services.contract_agent.contract_agent import analyze_contract_clauses

from app.services.contract_agent.summary_service import (
    generate_summary_data,
    render_summary_text,
    calculate_global_risk,
    generate_simplified_version,
)

from app.services.contract_agent.validator import (
    validate_contract_result,
    is_probably_contract,
)

from app.workers.progress import update_job_progress


def legal_progress_message(key: str, language: str) -> str:
    messages = {
        "loading": {
            "en": "Loading legal document...",
            "fr": "Chargement du document juridique...",
            "ar": "جارٍ تحميل المستند القانوني...",
        },
        "extracting": {
            "en": "Extracting contract text...",
            "fr": "Extraction du texte du contrat...",
            "ar": "جارٍ استخراج نص العقد...",
        },
        "splitting": {
            "en": "Splitting contract clauses...",
            "fr": "Découpage des clauses du contrat...",
            "ar": "جارٍ تقسيم بنود العقد...",
        },
        "analyzing": {
            "en": "Analyzing risky clauses...",
            "fr": "Analyse des clauses à risque...",
            "ar": "جارٍ تحليل البنود الحساسة...",
        },
        "summary": {
            "en": "Generating legal summary...",
            "fr": "Génération du résumé juridique...",
            "ar": "جارٍ إنشاء الملخص القانوني...",
        },
        "simplified": {
            "en": "Generating simplified version...",
            "fr": "Génération de la version simplifiée...",
            "ar": "جارٍ إنشاء نسخة مبسطة...",
        },
        "saving": {
            "en": "Saving legal analysis...",
            "fr": "Enregistrement de l’analyse juridique...",
            "ar": "جارٍ حفظ التحليل القانوني...",
        },
        "finalizing": {
            "en": "Finalizing legal analysis...",
            "fr": "Finalisation de l’analyse juridique...",
            "ar": "جارٍ إنهاء التحليل القانوني...",
        },
    }

    if language not in ["en", "fr", "ar"]:
        language = "en"

    return messages.get(key, {}).get(language, messages.get(key, {}).get("en", key))


def handle_contract_ai(job: Job, db):
    document_id = job.input.get("document_id")
    output_language = job.input.get("output_language", "en")
    access_type = job.input.get("access_type")
    credits_used = job.input.get("credits_used", 0)

    if output_language not in ["en", "fr", "ar"]:
        output_language = "en"

    update_job_progress(
        job,
        db,
        10,
        legal_progress_message("loading", output_language),
    )

    document = db.query(Document).filter(Document.id == document_id).first()

    if not document:
        raise ValueError("Document not found")

    update_job_progress(
        job,
        db,
        20,
        legal_progress_message("extracting", output_language),
    )

    raw_text = extract_text(
        document.file_path,
        document.file_type,
    )

    cleaned_text = clean_text(raw_text)

    if not is_probably_contract(cleaned_text):
        document.status = "rejected"
        db.commit()

        return {
            "error": "unsupported_document",
            "message": {
                "en": "The file was uploaded successfully, but its content does not appear to be a contract or legal agreement. Please upload a contract document.",
                "fr": "Le fichier a bien été importé, mais son contenu ne semble pas être un contrat ou un accord juridique. Veuillez importer un document contractuel.",
                "ar": "تم رفع الملف بنجاح، لكن محتواه لا يبدو أنه عقد أو اتفاقية قانونية. يرجى رفع مستند تعاقدي.",
            }.get(output_language, "Unsupported document"),
        }

    detected_language = detect_language(cleaned_text)

    update_job_progress(
        job,
        db,
        35,
        legal_progress_message("splitting", output_language),
    )

    clauses = split_into_clauses(cleaned_text)

    update_job_progress(
        job,
        db,
        50,
        legal_progress_message("analyzing", output_language),
    )

    clause_results = analyze_contract_clauses(
        clauses,
        output_language,
    )

    global_risk = calculate_global_risk(clause_results)

    update_job_progress(
        job,
        db,
        70,
        legal_progress_message("summary", output_language),
    )

    summary_data = generate_summary_data(
        cleaned_text,
        output_language,
    )

    summary = render_summary_text(
        summary_data,
        output_language,
    )

    update_job_progress(
        job,
        db,
        82,
        legal_progress_message("simplified", output_language),
    )

    simplified = generate_simplified_version(
        cleaned_text,
        output_language,
    )

    recommendations = [
        "Review all medium and high risk clauses.",
        "Ask a lawyer before signing important contracts.",
    ]

    update_job_progress(
        job,
        db,
        90,
        legal_progress_message("saving", output_language),
    )

    analysis = AnalysisResult(
        document_id=document.id,
        summary=summary,
        clauses=json.dumps(clause_results, ensure_ascii=False),
        risk_level=global_risk["risk_level"],
        risk_score=global_risk["risk_score"],
        simplified_version=simplified,
        recommendations=json.dumps(recommendations, ensure_ascii=False),
        access_type=access_type,
        credits_used=credits_used,
    )

    document.language = detected_language
    document.status = "completed"

    db.add(analysis)
    db.commit()
    db.refresh(analysis)

    response = {
        "id": analysis.id,
        "document_id": analysis.document_id,
        "summary": analysis.summary,
        "clauses": clause_results,
        "risk_level": analysis.risk_level,
        "risk_score": analysis.risk_score,
        "simplified_version": analysis.simplified_version,
        "recommendations": recommendations,
        "created_at": analysis.created_at.isoformat() if analysis.created_at else None,
        "contract_quality_score": summary_data.get("contract_quality_score"),
        "overall_balance": summary_data.get("overall_balance"),
        "contract_complexity": summary_data.get("contract_complexity"),
        "jurisdiction_detected": summary_data.get("jurisdiction_detected"),
    }

    response["quality_check"] = validate_contract_result(response)

    update_job_progress(
        job,
        db,
        95,
        legal_progress_message("finalizing", output_language),
    )

    return response
