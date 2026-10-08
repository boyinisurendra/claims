from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Dict, Any


class ClaimBase(BaseModel):
    claim_number: str


class ClaimCreate(ClaimBase):
    pass


class ClaimResponse(ClaimBase):
    id: str
    status: str
    file_name: str
    extracted_data: Optional[Dict[str, Any]]
    missing_fields: Optional[List[str]]
    recommendation: Optional[str]
    recommendation_reason: Optional[str]
    recommendation_confidence: Optional[float]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ValidationResult(BaseModel):
    is_valid: bool
    missing_fields: List[str]
    field_validation: Dict[str, Any]
    policy_matches: List[str]


class RecommendationResult(BaseModel):
    decision: str  # approved, denied, flagged
    confidence: float
    reason: str
    required_fields_missing: List[str]
    policy_violations: List[str]


class ApprovalRequest(BaseModel):
    decision: str  # approved or denied
    notes: Optional[str] = None
    denial_reason: Optional[str] = None


class ClaimReviewResponse(BaseModel):
    claim_id: str
    status: str
    recommendation: Optional[str]
    extracted_data: Optional[Dict[str, Any]]
    validation_results: Optional[Dict[str, Any]]
    pending_approval: bool

    class Config:
        from_attributes = True


class ProcessingStatus(BaseModel):
    claim_id: str
    status: str
    step: str
    progress: int
    message: str
