import json
import os
import re
from app.models.job import Job
from app.models.document import Document
from app.models.analysis import AnalysisResult

from app.services.contract_agent.contract_parser import extract_text
from app.services.cloud_storage_service import (
    download_api_file_from_cloud,
    delete_api_file_from_cloud,
)
from app.services.text_cleaner import clean_text
from app.services.contract_agent.clause_splitter import split_into_clauses
from app.services.language_service import detect_language
from app.services.contract_agent.contract_agent import analyze_contract_clauses
from app.services.contract_agent.pii_redactor import redact_sensitive_data
from app.services.contract_agent.unified_report_from_pipeline import (
    build_unified_report_from_pipeline,
    to_legacy_summary_data,
    to_legacy_simplified_string,
)

from app.services.contract_agent.summary_service import (
    calculate_global_risk,
    render_summary_text,
)

from app.services.contract_agent.jurisdiction_profiles import (
    detect_jurisdiction,
    format_jurisdiction_fields,
)
from app.services.contract_agent.party_role_detector import (
    get_display_roles,
    normalize_ai_role_words,
)

from app.services.contract_agent.validator import (
    validate_contract_result,
    is_probably_contract,
)

from app.workers.progress import update_job_progress


SUPPORTED_LANGUAGES = ("en", "fr", "ar")


def delete_local_file_safely(file_path):
    if not file_path:
        return

    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception:
        pass


def get_job_input(job: Job) -> dict:
    """
    Safely read job input data.

    Some code creates jobs using input_data.
    Older code uses input. This supports both.
    """

    data = getattr(job, "input_data", None)

    if data is None:
        data = getattr(job, "input", None)

    if isinstance(data, str):
        try:
            data = json.loads(data)
        except Exception:
            data = {}

    return data if isinstance(data, dict) else {}


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

    if language not in SUPPORTED_LANGUAGES:
        language = "en"

    return messages.get(key, {}).get(language, messages.get(key, {}).get("en", key))


def get_default_recommendations(language: str) -> list:
    """
    Trilingual fallback recommendations, matching every other user-facing
    string in this pipeline (which is produced in the requested language,
    never English-only regardless of output_language).
    """
    recommendations = {
        "en": [
            "Review all medium and high risk clauses.",
            "Ask a lawyer before signing important contracts.",
        ],
        "fr": [
            "Examiner toutes les clauses à risque moyen et élevé.",
            "Consulter un avocat avant de signer des contrats importants.",
        ],
        "ar": [
            "مراجعة جميع البنود ذات المخاطر المتوسطة والعالية.",
            "استشارة محامٍ قبل توقيع العقود المهمة.",
        ],
    }

    if language not in SUPPORTED_LANGUAGES:
        language = "en"

    return recommendations[language]


def handle_contract_ai(job: Job, db):
    input_data = get_job_input(job)

    document_id = input_data.get("document_id")
    output_language = input_data.get("output_language", "en")
    access_type = input_data.get("access_type")
    credits_used = input_data.get("credits_used", 0)
    storage_path = input_data.get("storage_path")

    if output_language not in SUPPORTED_LANGUAGES:
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

    downloaded_temp_file_path = None

    # Everything that touches the downloaded/temp file or the cloud
    # storage object is wrapped in try/finally so cleanup always runs
    # exactly once -- on success, on early rejection (unsupported
    # document), and on any unexpected exception. Previously, cleanup
    # only happened on the success path, leaking the temp file and the
    # cloud storage object whenever the document was rejected or any
    # step raised.
    try:
        update_job_progress(
            job,
            db,
            20,
            legal_progress_message("extracting", output_language),
        )

        file_path = document.file_path

        if storage_path:
            downloaded_temp_file_path = download_api_file_from_cloud(
                storage_path=str(storage_path),
                suffix=f".{document.file_type}",
            )
            file_path = downloaded_temp_file_path

        raw_text = extract_text(
            file_path,
            document.file_type,
        )

        # Non-redacted source for deterministic legal extraction.
        legal_source_text = clean_text(raw_text)

        # Redacted source for AI-facing processing.
        cleaned_text = redact_sensitive_data(legal_source_text)

        with open("debug_cleaned_text.txt", "w", encoding="utf-8") as f:
            f.write(cleaned_text)

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

        if not clauses:
            clauses = [cleaned_text]

        update_job_progress(
            job,
            db,
            50,
            legal_progress_message("analyzing", output_language),
        )

        # Detect party roles ONCE for the entire document, from the raw
        # contract text, and reuse it across all 3 pipelines below (clause
        # analysis, summary, simplified version). Without this, each
        # pipeline independently redetects roles from its own
        # already-processed text -- the root cause of "Client"/"Service
        # Provider" vs "Employer"/"Employee" inconsistency across sections
        # of the same report.
        party_roles = get_display_roles(
            contract_type="",
            text=cleaned_text[:2000],
            language=output_language,
            anonymized=True,
        )

        clause_results = analyze_contract_clauses(
            clauses,
            output_language,
            party_roles=party_roles,
        )

        # Document-level clause-coverage transparency, computed inside
        # analyze_contract_clauses() but previously never copied out of
        # the nested clause_results dict -- so a caller inspecting the
        # top-level response had no way to know whether every detected
        # clause was actually analyzed, or some were silently dropped
        # past the internal max_clauses cap.
        total_clauses_detected = clause_results.get("total_clauses_detected")
        clauses_analyzed = clause_results.get("clauses_analyzed")
        clauses_truncated = clause_results.get("clauses_truncated", False)

        clauses_obj = clause_results.get("clauses")

        if isinstance(clauses_obj, dict):
            clauses_list = (
                clauses_obj.get("results")
                or clauses_obj.get("items")
                or clauses_obj.get("clauses")
                or []
            )
        else:
            clauses_list = clauses_obj or []

        clause_results = normalize_ai_role_words(
            clause_results,
            party_roles,
            output_language,
        )

        unified_report = build_unified_report_from_pipeline(
            clause_results,
            cleaned_text,
            output_language,
            party_roles=party_roles,
        )

        risk_score = unified_report.get("risk_score", {})

        if isinstance(risk_score, dict):
            explanation = risk_score.get("explanation", "")

            if (
                "risk_node_" in explanation
                or "Score reflects" in explanation
                or "The score is mainly influenced" in explanation
            ):
                safe_clauses_list = (
                    clauses_list
                    if isinstance(clauses_list, list)
                    else []
                )

                high_titles_all = [
                    c.get("display_title")
                    or c.get("localized_title")
                    or c.get("clause_title")
                    or c.get("title")
                    or c.get("clause_type")
                    for c in safe_clauses_list
                    if isinstance(c, dict)
                    and str(c.get("risk_level", "")).lower() == "high"
                ]

                high_titles_all = [t for t in high_titles_all if t]

                # The narrative only NAMES the top 3 for readability, but
                # the COUNT stated in the sentence must reflect the true
                # total -- previously len() was computed on the
                # already-truncated list, so a contract with 4+ high-risk
                # clauses had its explanation silently understate the
                # real count (and drop any clause beyond the first 3
                # entirely, with no indication more existed).
                high_titles_total = len(high_titles_all)
                high_titles = high_titles_all[:3]
                high_titles_omitted = high_titles_total - len(high_titles)

                medium_count = sum(
                    1
                    for c in safe_clauses_list
                    if isinstance(c, dict)
                    and str(c.get("risk_level", "")).lower() == "medium"
                )

                if output_language == "fr":
                    if high_titles:
                        omitted_note = (
                            f", et {high_titles_omitted} autre(s)"
                            if high_titles_omitted
                            else ""
                        )
                        risk_score["explanation"] = (
                            f"Le score est principalement influencé par "
                            f"{high_titles_total} clause(s) à risque élevé : "
                            f"{', '.join(high_titles)}{omitted_note}. "
                            f"{medium_count} clause(s) à risque moyen contribuent également au score."
                        )
                    elif medium_count:
                        risk_score["explanation"] = (
                            f"Le score est principalement basé sur "
                            f"{medium_count} clause(s) à risque moyen, "
                            f"aucune clause à risque élevé n'ayant été identifiée."
                        )
                    else:
                        risk_score["explanation"] = (
                            "Le contrat ne contient que des clauses à faible risque."
                        )

                elif output_language == "ar":
                    if high_titles:
                        omitted_note = (
                            f"، و{high_titles_omitted} بند إضافي"
                            if high_titles_omitted
                            else ""
                        )
                        risk_score["explanation"] = (
                            f"تعتمد النتيجة بشكل أساسي على "
                            f"{high_titles_total} بند عالي المخاطر: "
                            f"{'، '.join(high_titles)}{omitted_note}. "
                            f"كما ساهم {medium_count} بند متوسط المخاطر في احتساب النتيجة."
                        )
                    elif medium_count:
                        risk_score["explanation"] = (
                            f"تعتمد النتيجة بشكل أساسي على "
                            f"{medium_count} بند متوسط المخاطر، "
                            f"دون وجود أي بند عالي المخاطر."
                        )
                    else:
                        risk_score["explanation"] = (
                            "لا يحتوي العقد إلا على بنود منخفضة المخاطر."
                        )

                else:
                    if high_titles:
                        omitted_note = (
                            f", and {high_titles_omitted} more"
                            if high_titles_omitted
                            else ""
                        )
                        risk_score["explanation"] = (
                            f"The score is mainly influenced by "
                            f"{high_titles_total} high-risk clause(s): "
                            f"{', '.join(high_titles)}{omitted_note}. "
                            f"{medium_count} medium-risk clause(s) also contributed."
                        )
                    elif medium_count:
                        risk_score["explanation"] = (
                            f"The score is based primarily on "
                            f"{medium_count} medium-risk clause(s), "
                            f"as no high-risk clauses were identified."
                        )
                    else:
                        risk_score["explanation"] = (
                            "The contract contains only low-risk clauses."
                        )

                unified_report["risk_score"] = risk_score

        unified_report = normalize_ai_role_words(
            unified_report,
            party_roles,
            output_language,
        )

        global_risk = calculate_global_risk(clause_results)

        update_job_progress(
            job,
            db,
            70,
            legal_progress_message("summary", output_language),
        )
        jurisdiction_detection = detect_jurisdiction(
            legal_source_text,
            output_language,
        )

        jurisdiction_fields = format_jurisdiction_fields(
            jurisdiction_detection,
            output_language,
        )


        # Single analysis truth: enrich the unified report once, then render
        # all legacy/user-facing views from the same structured overview.
        overview = unified_report.get("contract_overview", {}) or {}

        resolved_jurisdiction = str(
            overview.get("jurisdiction_detected") or ""
        ).strip()

        detector_jurisdiction = str(
            jurisdiction_fields.get("jurisdiction") or ""
        ).strip()

        localized_unknowns = {
            "",
            "Not specified",
            "Non spécifié",
            "غير محدد",
            "Unknown",
            "Inconnu",
            "غير معروف",
            "None",
            "null",
        }

        def _contains_redaction_placeholder(value: str) -> bool:
            """
            Return True when a value is empty, unknown, or contains an anonymization
            placeholder such as [LOCATION], [ADDRESS], [PERSON], [PARTY_1], etc.
            """
            normalized = str(value or "").strip()

            if not normalized:
                return True

            if normalized in localized_unknowns:
                return True

            return bool(
                re.search(
                    r"\[[A-Z][A-Z0-9_]*\]",
                    normalized,
                )
            )

        detector_is_valid = not _contains_redaction_placeholder(
            detector_jurisdiction
        )

        resolved_is_unknown = _contains_redaction_placeholder(
            resolved_jurisdiction
        )

        # Deterministic extraction has priority only when it contains a real value.
        if detector_is_valid:
            overview["jurisdiction_detected"] = detector_jurisdiction

        # If neither the AI nor the deterministic detector produced a usable value,
        # use the localized fallback.
        elif resolved_is_unknown:
            overview["jurisdiction_detected"] = {
                "en": "Not specified",
                "fr": "Non spécifié",
                "ar": "غير محدد",
            }.get(output_language, "Not specified")

        if jurisdiction_detection.get("confidence") == "low" and not any([
            jurisdiction_detection.get("governing_law"),
            jurisdiction_detection.get("dispute_forum"),
            jurisdiction_detection.get("arbitration_seat"),
            jurisdiction_detection.get("arbitration_institution"),
        ]):
            overview["jurisdiction_note"] = ""
        else:
            overview["jurisdiction_note"] = jurisdiction_fields[
                "jurisdiction_note"
            ]

        unified_report["contract_overview"] = overview

        legacy_summary_data = to_legacy_summary_data(
            unified_report,
            output_language,
        )

        # Preserve the exact values resolved by the unified pipeline.
        overview = unified_report.get("contract_overview", {}) or {}

        for source_key, legacy_key in [
            ("duration", "duration"),
            ("payment_terms", "payment_terms"),
            ("jurisdiction_detected", "jurisdiction_detected"),
            ("jurisdiction_note", "jurisdiction_note"),
        ]:
            if source_key in overview:
                legacy_summary_data[legacy_key] = overview[source_key]

        summary = render_summary_text(
            legacy_summary_data,
            output_language,
            party_roles=party_roles,
        )

        update_job_progress(
            job,
            db,
            82,
            legal_progress_message("simplified", output_language),
        )

        simplified = to_legacy_simplified_string(
            unified_report,
            output_language,
        )

        recommendations = get_default_recommendations(output_language)

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

        overview = unified_report.get("contract_overview", {})

        response = {
            "id": analysis.id,
            "document_id": analysis.document_id,
            "summary": analysis.summary,
            "clauses": clause_results,
            "risk_level": analysis.risk_level,
            "risk_score": unified_report.get("risk_score", analysis.risk_score),
            "simplified_version": analysis.simplified_version,
            "recommendations": recommendations,
            "unified_report": unified_report,
            "created_at": analysis.created_at.isoformat() if analysis.created_at else None,
            "contract_quality_score": unified_report.get("confidence_score"),
            "overall_balance": overview.get("overall_balance"),
            "contract_complexity": overview.get("contract_complexity"),
            "jurisdiction_detected": overview.get("jurisdiction_detected"),
            "total_clauses_detected": total_clauses_detected,
            "clauses_analyzed": clauses_analyzed,
            "clauses_truncated": clauses_truncated,
        }

        response = normalize_ai_role_words(
            response,
            party_roles,
            output_language,
        )

        response["quality_check"] = validate_contract_result(response)

        update_job_progress(
            job,
            db,
            95,
            legal_progress_message("finalizing", output_language),
        )

        with open("last_analysis.json", "w", encoding="utf-8") as f:
            json.dump(response, f, ensure_ascii=False, indent=2)

        return response

    finally:
        delete_api_file_from_cloud(storage_path)
        delete_local_file_safely(downloaded_temp_file_path)
        delete_local_file_safely(document.file_path)
