from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime, func
from sqlalchemy.orm import relationship
import enum
from app.db.base_class import Base

class FileTypeEnum(str, enum.Enum):
    SHOP_FRONT = "shop_front"
    INVENTORY = "inventory"
    INVOICE = "invoice"
    RECEIPT = "receipt"
    OTHER = "other"

class EvidenceFile(Base):
    __tablename__ = "evidence_files"
    
    id = Column(Integer, primary_key=True, index=True)
    shop_id = Column(Integer, ForeignKey("shops.id"), nullable=True) # Linked to shop directly or via app
    application_id = Column(Integer, ForeignKey("applications.id"), nullable=True)
    uploaded_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    file_name = Column(String, nullable=True)
    file_type = Column(Enum(FileTypeEnum), nullable=False)
    storage_provider = Column(String, default="cloudinary")
    storage_url = Column(String, nullable=False)
    storage_public_id = Column(String, nullable=True)
    mime_type = Column(String, nullable=True)
    file_size = Column(Integer, nullable=True)
    processing_status = Column(String, default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    application = relationship("Application", back_populates="evidence_files")
    image_analysis = relationship("ImageAnalysisResult", back_populates="evidence_file", uselist=False)
    ocr_result = relationship("OcrResult", back_populates="evidence_file", uselist=False)
