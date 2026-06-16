from sqlalchemy import Column, Integer, String, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class ImageAnalysisResult(Base):
    __tablename__ = "image_analysis_results"
    
    id = Column(Integer, primary_key=True, index=True)
    evidence_file_id = Column(Integer, ForeignKey("evidence_files.id"), nullable=False, unique=True)
    shelf_density_score = Column(Float, nullable=True)
    brand_diversity_score = Column(Float, nullable=True)
    analysis_metadata = Column(JSON, nullable=True) # Contains raw CV outputs

    evidence_file = relationship("EvidenceFile", back_populates="image_analysis")

class OcrResult(Base):
    __tablename__ = "ocr_results"
    
    id = Column(Integer, primary_key=True, index=True)
    evidence_file_id = Column(Integer, ForeignKey("evidence_files.id"), nullable=False, unique=True)
    extracted_text = Column(String, nullable=True)
    total_amount_found = Column(Float, nullable=True)
    merchant_name_found = Column(String, nullable=True)
    confidence_score = Column(Float, nullable=True)
    invoice_activity_score = Column(Float, nullable=True)
    transaction_consistency_score = Column(Float, nullable=True)

    evidence_file = relationship("EvidenceFile", back_populates="ocr_result")
