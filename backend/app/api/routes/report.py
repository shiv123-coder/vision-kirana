from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_active_user
from app.models.user import User, RoleEnum
from app.models.application import Application
from app.ml.location_engine import LocationIntelligenceEngine
from app.ml.risk_engine import RiskEngine

router = APIRouter()

@router.get("/{application_id}")
def generate_application_report(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Aggregates all AI intelligence modules and generates a complete report.
    """
    application = db.query(Application).filter(Application.id == application_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
        
    if application.shop.owner_id != current_user.id and current_user.role not in [RoleEnum.ADMIN, RoleEnum.LOAN_OFFICER]:
        raise HTTPException(status_code=403, detail="Not authorized to view this report")

    # 1. Gather Raw Data
    shop = application.shop
    image_analyses = []
    ocr_results = []
    for evidence in application.evidence_files:
        if evidence.image_analysis:
            image_analyses.append(evidence.image_analysis)
        if evidence.ocr_result:
            ocr_results.append(evidence.ocr_result)
            
    voice_transcripts = application.voice_transcripts

    # Extrapolate best scores for Risk Engine if there are multiple
    shelf_density_score = max([ia.shelf_density_score for ia in image_analyses if ia.shelf_density_score] + [0.0])
    product_diversity_score = max([ia.brand_diversity_score for ia in image_analyses if ia.brand_diversity_score] + [0.0])
    invoice_activity_score = max([ocr.invoice_activity_score for ocr in ocr_results if ocr.invoice_activity_score] + [0.0])

    # 2. Location Intelligence
    loc_engine = LocationIntelligenceEngine()
    # Mocking coordinates for demonstration
    loc_scores = loc_engine.generate_full_report(12.9716, 77.5946)
    
    # 3. Risk Assessment
    risk_engine = RiskEngine()
    raw_data = {
        "shelf_density_score": shelf_density_score,
        "product_diversity_score": product_diversity_score,
        "invoice_activity_score": invoice_activity_score,
        "years_in_business": shop.years_in_business,
        "location_score": loc_scores.get("market_area_score", 0.0),
        "sales_consistency_score": 80.0, # Defaulted for now
        "uploaded_documents_count": len(application.evidence_files),
        "required_documents_count": 5
    }
    
    risk_report = risk_engine.generate_risk_report(raw_data)
    
    # 4. Generate AI Insights (Factors)
    positive_factors = []
    risk_factors = []
    
    if risk_report["business_health_score"] >= 80:
        positive_factors.append("Exceptionally high overall business health.")
    if shop.years_in_business >= 5:
        positive_factors.append("Established business with 5+ years history.")
    if loc_scores.get("market_area_score", 0) > 75:
        positive_factors.append("Highly favorable market area demographics.")
        
    if shelf_density_score < 40:
        risk_factors.append("Low shelf density detected in images.")
    if len(application.evidence_files) < 3:
        risk_factors.append("Incomplete documentation provided.")
    if loc_scores.get("competition_density_score", 100) < 30:
        risk_factors.append("High competition density in the immediate radius.")

    # Format the comprehensive response
    return {
        "application_id": application.id,
        "shop_profile": {
            "name": shop.shop_name,
            "owner": shop.owner_name,
            "address": f"{shop.address}, {shop.city}, {shop.state}",
            "years_in_business": shop.years_in_business,
            "monthly_sales": shop.monthly_sales,
            "requested_loan": application.requested_amount,
            "purpose": application.purpose
        },
        "cv_analysis": {
            "shelf_density": shelf_density_score,
            "product_diversity": product_diversity_score
        },
        "ocr_analysis": {
            "invoice_activity": invoice_activity_score,
            "documents_analyzed": len(ocr_results)
        },
        "voice_analysis": [
            {
                "summary": vt.business_summary,
                "sentiment": vt.sentiment_score
            } for vt in voice_transcripts
        ],
        "location_intelligence": loc_scores,
        "risk_assessment": {
            "health_score": risk_report["business_health_score"],
            "category": risk_report["risk_category"],
            "positive_factors": positive_factors,
            "risk_factors": risk_factors,
            "recommendation": "APPROVE" if risk_report["business_health_score"] >= 60 else "MANUAL REVIEW"
        }
    }
