from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.api.deps import get_db, get_current_active_user
from app.models.user import User, RoleEnum
from app.models.application import Application
from app.models.evidence_file import EvidenceFile
from app.schemas.analysis import ApplicationAnalysisResponse, ImageAnalysisResponse, OcrResultResponse

router = APIRouter()

@router.get("/{application_id}", response_model=ApplicationAnalysisResponse)
def get_application_analysis(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get all analysis results (CV and OCR) for a specific application.
    """
    application = db.query(Application).filter(Application.id == application_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
        
    if application.shop.owner_id != current_user.id and current_user.role not in [RoleEnum.ADMIN, RoleEnum.LOAN_OFFICER]:
        raise HTTPException(status_code=403, detail="Not authorized to view analysis for this application")

    image_analyses = []
    ocr_results = []
    
    for evidence in application.evidence_files:
        if evidence.image_analysis:
            image_analyses.append(evidence.image_analysis)
        if evidence.ocr_result:
            ocr_results.append(evidence.ocr_result)
            
    return ApplicationAnalysisResponse(
        application_id=application_id,
        image_analyses=image_analyses,
        ocr_results=ocr_results,
        voice_transcripts=application.voice_transcripts
    )
