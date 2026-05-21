from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.sql import func

from app.database import Base


class BusinessAnalysis(Base):
    __tablename__ = "business_analyses"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    file_name = Column(
        String,
        nullable=False,
    )

    # Full backend + AI result JSON.
    # Important:
    # - Backend KPIs are the financial source of truth.
    # - AI is used only for narrative / explanation layers.
    result = Column(
        Text,
        nullable=False,
    )

    # Backend-detected business model.
    business_model = Column(
        String,
        default="general",
        index=True,
    )

    # Backend-calculated business health score.
    business_health_score = Column(
        Integer,
        default=0,
    )

    # Billing / access metadata.
    access_type = Column(
        String,
        default="trial",
    )

    credits_used = Column(
        Integer,
        default=0,
    )

    # Output language requested by the user.
    output_language = Column(
        String,
        default="en",
    )

    # Number of parsed rows in the uploaded business file.
    rows_count = Column(
        Integer,
        default=0,
    )

    # =========================
    # Executive report exports
    # =========================

    # Server-side generated PDF path or storage key.
    pdf_report_path = Column(
        String,
        nullable=True,
    )

    # Server-side generated PowerPoint path or storage key.
    pptx_report_path = Column(
        String,
        nullable=True,
    )

    # PDF generation timestamp for audit / enterprise reporting.
    pdf_generated_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    # PowerPoint generation timestamp for audit / enterprise reporting.
    pptx_generated_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    # =========================
    # Currency / internationalization
    # =========================

    # Main detected currency code, for example USD, EUR, MAD, AED.
    currency_code = Column(
        String,
        default="USD",
        index=True,
    )

    # Main detected currency symbol, for example $, €, د.م.
    currency_symbol = Column(
        String,
        default="$",
    )

    # =========================
    # Processing / worker metadata
    # =========================

    # completed, pending, processing, failed.
    # This is ready for future async workers.
    report_status = Column(
        String,
        default="completed",
        index=True,
    )

    # Analysis processing duration in milliseconds.
    processing_time_ms = Column(
        Integer,
        default=0,
    )

    # Backend analysis schema/version.
    # Useful when reports evolve and old analyses must remain readable.
    analysis_version = Column(
        String,
        default="v1",
    )

    # upload, api, scheduled, enterprise_connector, stripe, quickbooks, shopify, etc.
    source_type = Column(
        String,
        default="upload",
        index=True,
    )

    # =========================
    # Feature flags for dashboards / exports
    # =========================

    # Stored as integer for broad DB compatibility:
    # 1 = true, 0 = false.
    has_charts = Column(
        Integer,
        default=1,
    )

    has_forecast = Column(
        Integer,
        default=0,
    )

    has_ai_narrative = Column(
        Integer,
        default=1,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
