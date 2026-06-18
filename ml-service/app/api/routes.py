from fastapi import APIRouter, File, HTTPException, UploadFile
from typing import Any
import traceback
from app.services.vision_analyzer import VisionAnalyzer
from app.services.ocr_processor import OCRProcessor
from app.services.voice_processor import VoiceProcessor
from app.services.location_engine import LocationIntelligenceEngine
from app.services.risk_engine import RiskEngine

router = APIRouter()

vision_analyzer = VisionAnalyzer()
ocr_processor = OCRProcessor()
voice_processor = VoiceProcessor()
risk_engine = RiskEngine()
loc_engine = LocationIntelligenceEngine()

@router.get("/health")
def api_health():
    return {"status": "healthy"}

@router.post("/analyze/image")
async def analyze_image(file: UploadFile = File(...)) -> Any:
    try:
        contents = await file.read()
        image_quality = vision_analyzer.calculateImageQuality(contents)
        shelf_density = vision_analyzer.calculateShelfDensity(contents)
        store_org = vision_analyzer.estimateStoreOrganization(contents)
        diversity = vision_analyzer.estimateProductDiversity(contents)
        visibility = vision_analyzer.calculateInventoryVisibility(contents)
        barcode = vision_analyzer.verifyBarcode(contents)
        
        return {
            "image_quality_score": image_quality,
            "shelf_density_score": shelf_density,
            "store_organization_score": store_org,
            "brand_diversity_score": diversity,
            "inventory_visibility_score": visibility,
            "barcode_data": barcode
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze/ocr")
async def analyze_ocr(category: str, file: UploadFile = File(...)) -> Any:
    try:
        contents = await file.read()
        results = ocr_processor.process(contents, category)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze/voice")
async def analyze_voice(file: UploadFile = File(...)) -> Any:
    try:
        contents = await file.read()
        transcript, sentiment = voice_processor.process_audio(contents)
        return {
            "transcript": transcript,
            "sentiment_score": sentiment
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/extract/risk-features")
async def extract_risk_features(data: dict) -> Any:
    try:
        report = risk_engine.generate_risk_report(data)
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/analyze/location")
async def analyze_location(lat: float, lng: float) -> Any:
    try:
        return loc_engine.generate_full_report(lat, lng)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
