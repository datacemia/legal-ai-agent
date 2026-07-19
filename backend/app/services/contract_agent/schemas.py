from typing import Any, Dict, List

from pydantic import BaseModel, Field, field_validator


SUPPORTED_LANGUAGES = {"en", "fr", "ar"}
SUPPORTED_COMPLEXITY_LEVELS = {"low", "medium", "high"}
SUPPORTED_RISK_LEVELS = {"", "low", "medium", "high", "elevated", "critical"}


def normalize_language(value: str) -> str:
    value = str(value or "en").lower().strip()
    return value if value in SUPPORTED_LANGUAGES else "en"


def normalize_complexity(value: str) -> str:
    value = str(value or "medium").lower().strip()

    mapping = {
        "low": "low",
        "simple": "low",
        "faible": "low",
        "منخفض": "low",
        "منخفضة": "low",
        "بسيط": "low",

        "medium": "medium",
        "moderate": "medium",
        "moyen": "medium",
        "moyenne": "medium",
        "متوسط": "medium",
        "متوسطة": "medium",

        "high": "high",
        "complex": "high",
        "complexe": "high",
        "élevé": "high",
        "élevée": "high",
        "مرتفع": "high",
        "مرتفعة": "high",
        "معقد": "high",
    }

    return mapping.get(value, "medium")


def normalize_risk_level(value: str) -> str:
    value = str(value or "").lower().strip()

    mapping = {
        "low": "low",
        "medium": "medium",
        "moderate": "medium",
        "elevated": "elevated",
        "high": "high",
        "critical": "critical",

        "faible": "low",
        "moyen": "medium",
        "moyenne": "medium",
        "élevé": "high",
        "élevée": "high",
        "critique": "critical",

        "منخفض": "low",
        "متوسط": "medium",
        "مرتفع": "high",
        "حرج": "critical",
    }

    return mapping.get(value, value if value in SUPPORTED_RISK_LEVELS else "")


def clamp_score(value: int) -> int:
    try:
        value = int(value)
    except Exception:
        return 0

    return max(0, min(value, 100))


def clamp_coverage(value: float) -> float:
    try:
        value = float(value)
    except Exception:
        return 0.0

    return max(0.0, min(value, 1.0))


class ContractSummary(BaseModel):
    # Legacy fields kept for backward compatibility.
    contract_type: str = ""
    parties: List[str] = Field(default_factory=list)
    duration: str = ""
    payment_terms: str = ""

    main_obligations: List[str] = Field(default_factory=list)
    global_summary: str = ""
    important_points: List[str] = Field(default_factory=list)

    missing_clauses: List[str] = Field(default_factory=list)
    dangerous_patterns: List[str] = Field(default_factory=list)

    contract_score: int = 0
    overall_balance: str = ""

    negotiation_priorities: List[str] = Field(default_factory=list)
    key_risks: List[str] = Field(default_factory=list)
    practical_decision: str = ""
    recommended_actions: List[str] = Field(default_factory=list)

    jurisdiction_detected: str = ""
    jurisdiction_note: str = ""

    contract_complexity: str = "medium"

    # International / multi-domain extensions.
    party_roles: Dict[str, str] = Field(default_factory=dict)

    effective_date: str = ""
    renewal_terms: str = ""
    termination_terms: str = ""
    post_termination_obligations: List[str] = Field(default_factory=list)

    governing_law: str = ""
    dispute_resolution: str = ""
    arbitration_details: Dict[str, Any] = Field(default_factory=dict)

    risk_level: str = ""
    risk_breakdown: Dict[str, Any] = Field(default_factory=dict)

    commercial_terms: Dict[str, Any] = Field(default_factory=dict)
    data_protection_terms: Dict[str, Any] = Field(default_factory=dict)
    intellectual_property_terms: Dict[str, Any] = Field(default_factory=dict)
    liability_terms: Dict[str, Any] = Field(default_factory=dict)
    compliance_terms: Dict[str, Any] = Field(default_factory=dict)

    contract_family: str = ""
    sector_context: str = ""

    confidence_score: int = 0
    coverage: float = 0.0
    language: str = "en"

    source_notes: List[str] = Field(default_factory=list)
    confidence_notes: List[str] = Field(default_factory=list)

    @field_validator("contract_score", "confidence_score")
    @classmethod
    def validate_scores(cls, value: int) -> int:
        return clamp_score(value)

    @field_validator("coverage")
    @classmethod
    def validate_coverage(cls, value: float) -> float:
        return clamp_coverage(value)

    @field_validator("contract_complexity")
    @classmethod
    def validate_complexity(cls, value: str) -> str:
        return normalize_complexity(value)

    @field_validator("risk_level")
    @classmethod
    def validate_risk_level(cls, value: str) -> str:
        return normalize_risk_level(value)

    @field_validator("language")
    @classmethod
    def validate_language(cls, value: str) -> str:
        return normalize_language(value)


class SimplifiedContract(BaseModel):
    # Legacy fields kept for backward compatibility.
    simplified_version: str = ""
    key_points: List[str] = Field(default_factory=list)
    things_to_watch: List[str] = Field(default_factory=list)

    # International / multi-domain extensions.
    plain_language_risks: List[str] = Field(default_factory=list)
    plain_language_obligations: List[str] = Field(default_factory=list)
    plain_language_actions: List[str] = Field(default_factory=list)

    business_decision: str = ""
    negotiation_focus: List[str] = Field(default_factory=list)

    language: str = "en"
    confidence_notes: List[str] = Field(default_factory=list)

    @field_validator("language")
    @classmethod
    def validate_language(cls, value: str) -> str:
        return normalize_language(value)


class ArbitrationDetails(BaseModel):
    seat: str = ""
    institution: str = ""
    rules: str = ""
    language: str = ""
    number_of_arbitrators: str = ""
    confidentiality: str = ""
    emergency_arbitrator: str = ""
    interim_measures: str = ""
    cost_allocation: str = ""


class RiskBreakdown(BaseModel):
    high_count: int = 0
    medium_count: int = 0
    low_count: int = 0
    critical_clauses: List[str] = Field(default_factory=list)
    exposure: Dict[str, str] = Field(default_factory=dict)
    score_explanation: str = ""


class UnifiedReport(BaseModel):
    contract_family: str = ""
    contract_overview: Dict[str, Any] = Field(default_factory=dict)
    executive_summary: str = ""

    key_clauses: List[Dict[str, Any]] = Field(default_factory=list)
    risks_identified: List[Dict[str, Any]] = Field(default_factory=list)
    negotiation_priorities: List[Dict[str, Any]] = Field(default_factory=list)
    suggested_wording: List[Dict[str, Any]] = Field(default_factory=list)
    fallback_position: str = ""
    action_checklist: List[Dict[str, Any]] = Field(default_factory=list)

    risk_score: Dict[str, Any] = Field(default_factory=dict)
    missing_clauses: List[Dict[str, Any]] = Field(default_factory=list)
    confidence_notes: List[str] = Field(default_factory=list)

    contract_version: str = ""
    analysis_timestamp: str = ""
    analysis_engine: str = ""
    coverage: float = 0.0
    confidence_score: int = 0
    language: str = "en"

    @field_validator("coverage")
    @classmethod
    def validate_coverage(cls, value: float) -> float:
        return clamp_coverage(value)

    @field_validator("confidence_score")
    @classmethod
    def validate_confidence_score(cls, value: int) -> int:
        return clamp_score(value)

    @field_validator("language")
    @classmethod
    def validate_language(cls, value: str) -> str:
        return normalize_language(value)
