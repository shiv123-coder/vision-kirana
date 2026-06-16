from sqlalchemy import Column, Integer, String, ForeignKey, Enum
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
    application_id = Column(Integer, ForeignKey("applications.id"), nullable=False)
    file_url = Column(String, nullable=False)
    file_type = Column(Enum(FileTypeEnum), nullable=False)
    s3_key = Column(String, nullable=True)

    application = relationship("Application", back_populates="evidence_files")
    image_analysis = relationship("ImageAnalysisResult", back_populates="evidence_file", uselist=False)
    ocr_result = relationship("OcrResult", back_populates="evidence_file", uselist=False)
