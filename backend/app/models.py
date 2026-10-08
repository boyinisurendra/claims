from sqlalchemy import Column, String, Integer, DateTime, Text, Float, JSON, Enum
from sqlalchemy.sql import func
from datetime import datetime
import enum
from .database import Base


class ClaimStatus(str, enum.Enum):
    PENDING = "pending"
    EXTRACTED = "extracted"
    VALIDATED = "validated"
    RECOMMENDED = "recommended"
    APPROVED = "approved"
    DENIED = "denied"
    FLAGGED = "flagged"


class Claim(Base):
    __tablename__ = "claims"

    id = Column(String(36), primary_key=True)
    claim_number = Column(String(100), unique=True, index=True)
    file_name = Column(String(255))
    file_path = Column(String(500))
    status = Column(Enum(ClaimStatus), default=ClaimStatus.PENDING, index=True)

    # Extracted data from OCR
    extracted_data = Column(JSON)

    # Validation results
    validation_results = Column(JSON)
    missing_fields = Column(JSON)

    # Recommendation
    recommendation = Column(String(50))  # approved, denied, flagged
    recommendation_reason = Column(Text)
    recommendation_confidence = Column(Float)

    # Approval workflow
    approved_by = Column(String(255), nullable=True)
    approval_date = Column(DateTime, nullable=True)
    denial_reason = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ClaimReview(Base):
    __tablename__ = "claim_reviews"

    id = Column(String(36), primary_key=True)
    claim_id = Column(String(36), index=True)
    reviewer_id = Column(String(255))
    notes = Column(Text, nullable=True)
    decision = Column(String(50))  # approved, denied
    created_at = Column(DateTime, default=datetime.utcnow)


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(String(36), primary_key=True)
    claim_id = Column(String(36), index=True)
    action = Column(String(100))
    actor = Column(String(255), nullable=True)
    details = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
