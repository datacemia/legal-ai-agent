from pydantic import BaseModel, Field
from typing import List


class ContractSummary(BaseModel):
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
    jurisdiction_detected: str = ""
    jurisdiction_note: str = ""
    recommended_actions: List[str] = Field(default_factory=list)
    contract_complexity: str = "medium"


class SimplifiedContract(BaseModel):
    simplified_version: str = ""
    key_points: List[str] = Field(default_factory=list)
    things_to_watch: List[str] = Field(default_factory=list)
