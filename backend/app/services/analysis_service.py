from sqlalchemy.orm import Session
from app.ml.vision_analyzer import VisionAnalyzer
from app.ml.ocr_processor import OCRProcessor
from app.models.analysis import ImageAnalysisResult, OcrResult
import logging

logger = logging.getLogger(__name__)

def analyze_uploaded_image(image_bytes: bytes, evidence_file_id: int, db: Session):
    """
    Background task to analyze an uploaded image using VisionAnalyzer 
    and store the results in the database.
    """
    try:
        analyzer = VisionAnalyzer()
        
        # Run analyses
        # We pass the raw bytes directly to the analyzer, which handles decoding
        image_quality = analyzer.calculateImageQuality(image_bytes)
        shelf_density = analyzer.calculateShelfDensity(image_bytes)
        store_organization = analyzer.estimateStoreOrganization(image_bytes)
        product_diversity = analyzer.estimateProductDiversity(image_bytes)
        inventory_visibility = analyzer.calculateInventoryVisibility(image_bytes)
        barcode_results = analyzer.verifyBarcode(image_bytes)
        
        # Structure the metadata
        analysis_metadata = {
            "image_quality_score": image_quality,
            "store_organization_score": store_organization,
            "inventory_visibility_score": inventory_visibility,
            "barcode_data": barcode_results
        }
        
        # Create DB record
        analysis_result = ImageAnalysisResult(
            evidence_file_id=evidence_file_id,
            shelf_density_score=shelf_density,
            brand_diversity_score=product_diversity,
            analysis_metadata=analysis_metadata
        )
        
        db.add(analysis_result)
        db.commit()
        
        logger.info(f"Successfully analyzed image for evidence_file_id {evidence_file_id}")
        
    except Exception as e:
        logger.error(f"Failed to analyze image for evidence_file_id {evidence_file_id}: {str(e)}")
        db.rollback()
    finally:
        # We should close the session since it's running in a background task
        # and we passed a new session instance to it
        db.close()

def analyze_uploaded_document(file_bytes: bytes, file_category: str, evidence_file_id: int, db: Session):
    """
    Background task to analyze an uploaded document (PDF or Image) using OCRProcessor
    and store the results in the database.
    """
    try:
        processor = OCRProcessor()
        
        # Run OCR
        results = processor.process(file_bytes, file_category)
        
        # Create DB record
        ocr_result = OcrResult(
            evidence_file_id=evidence_file_id,
            extracted_text=results["extracted_text"],
            total_amount_found=results["total_amount"],
            merchant_name_found=results["merchant_name"],
            confidence_score=results["confidence"],
            invoice_activity_score=results["invoice_activity_score"],
            transaction_consistency_score=results["transaction_consistency_score"]
        )
        
        db.add(ocr_result)
        db.commit()
        
        logger.info(f"Successfully processed OCR for evidence_file_id {evidence_file_id}")
        
    except Exception as e:
        logger.error(f"Failed to process OCR for evidence_file_id {evidence_file_id}: {str(e)}")
        db.rollback()
    finally:
        db.close()
