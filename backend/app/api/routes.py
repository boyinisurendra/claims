from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import uuid4
from datetime import datetime
import json

from .. import models, schemas
from ..database import get_db
from ..utils.pdf_handler import save_upload
from ..agents.ocr_agent import OCRAgent
from ..agents.validation_agent import ValidationAgent
from ..agents.recommendation_agent import RecommendationAgent

router = APIRouter(prefix="/api", tags=["claims"])

ocr_agent = OCRAgent()
validation_agent = ValidationAgent()
recommendation_agent = RecommendationAgent()


@router.post("/claims/upload", response_model=schemas.ClaimResponse)
async def upload_claim(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload and process a claim PDF."""

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files allowed")

    claim_id = str(uuid4())
    file_path = save_upload(file)

    claim = models.Claim(
        id=claim_id,
        claim_number=f"CLM-{claim_id[:8]}",
        file_name=file.filename,
        file_path=file_path,
        status=models.ClaimStatus.PENDING
    )
    db.add(claim)
    db.commit()

    try:
        ocr_result = ocr_agent.process_claim(file_path)
        claim.extracted_data = ocr_result["structured_data"]
        claim.status = models.ClaimStatus.EXTRACTED
        db.commit()

        validation_result = validation_agent.validate_claim(
            ocr_result["structured_data"]
        )
        claim.validation_results = validation_result
        claim.missing_fields = validation_result.get("missing_fields", [])
        claim.status = models.ClaimStatus.VALIDATED
        db.commit()

        recommendation = recommendation_agent.generate_recommendation(
            ocr_result["structured_data"],
            validation_result
        )
        claim.recommendation = recommendation["recommendation"]
        claim.recommendation_reason = recommendation["reason"]
        claim.recommendation_confidence = recommendation["confidence"]
        claim.status = models.ClaimStatus.RECOMMENDED
        db.commit()

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")

    return claim


@router.get("/claims/pending")
def get_pending_claims(db: Session = Depends(get_db)):
    """Get all claims pending human review."""
    claims = db.query(models.Claim).filter(
        models.Claim.status.in_([
            models.ClaimStatus.PENDING,
            models.ClaimStatus.EXTRACTED,
            models.ClaimStatus.VALIDATED,
            models.ClaimStatus.RECOMMENDED,
            models.ClaimStatus.FLAGGED
        ])
    ).order_by(models.Claim.created_at.desc()).all()

    return claims


@router.get("/claims/{claim_id}", response_model=schemas.ClaimResponse)
def get_claim(claim_id: str, db: Session = Depends(get_db)):
    """Retrieve claim details."""
    claim = db.query(models.Claim).filter(models.Claim.id == claim_id).first()

    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")

    return claim


@router.post("/claims/{claim_id}/approve")
def approve_claim(
    claim_id: str,
    request: schemas.ApprovalRequest,
    db: Session = Depends(get_db)
):
    """Approve a claim."""
    claim = db.query(models.Claim).filter(models.Claim.id == claim_id).first()

    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")

    claim.status = models.ClaimStatus.APPROVED
    claim.approved_by = "system"
    claim.approval_date = datetime.utcnow()

    audit_log = models.AuditLog(
        id=str(uuid4()),
        claim_id=claim_id,
        action="APPROVED",
        actor="system",
        details={"notes": request.notes}
    )

    db.add(audit_log)
    db.commit()

    return {"status": "approved", "claim_id": claim_id}


@router.post("/claims/{claim_id}/deny")
def deny_claim(
    claim_id: str,
    request: schemas.ApprovalRequest,
    db: Session = Depends(get_db)
):
    """Deny a claim."""
    claim = db.query(models.Claim).filter(models.Claim.id == claim_id).first()

    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")

    claim.status = models.ClaimStatus.DENIED
    claim.denial_reason = request.denial_reason or ""

    audit_log = models.AuditLog(
        id=str(uuid4()),
        claim_id=claim_id,
        action="DENIED",
        actor="system",
        details={"reason": request.denial_reason}
    )

    db.add(audit_log)
    db.commit()

    return {"status": "denied", "claim_id": claim_id}


@router.delete("/claims/{claim_id}")
def delete_claim(claim_id: str, db: Session = Depends(get_db)):
    """Delete a claim."""
    claim = db.query(models.Claim).filter(models.Claim.id == claim_id).first()

    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")

    audit_log = models.AuditLog(
        id=str(uuid4()),
        claim_id=claim_id,
        action="DELETED",
        actor="system",
        details={"claim_number": claim.claim_number}
    )

    db.add(audit_log)
    db.delete(claim)
    db.commit()

    return {"status": "deleted", "claim_id": claim_id}


@router.get("/audit-logs")
def get_audit_logs(db: Session = Depends(get_db)):
    """Get all audit logs."""
    logs = db.query(models.AuditLog).order_by(
        models.AuditLog.created_at.desc()
    ).all()

    return [
        {
            "id": log.id,
            "claim_id": log.claim_id,
            "action": log.action,
            "actor": log.actor,
            "details": log.details,
            "created_at": log.created_at,
        }
        for log in logs
    ]


@router.get("/claims")
def list_claims(db: Session = Depends(get_db)):
    """List all claims."""
    claims = db.query(models.Claim).order_by(
        models.Claim.created_at.desc()
    ).all()
    return claims
