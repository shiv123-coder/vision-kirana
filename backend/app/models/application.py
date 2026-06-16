from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum
from app.db.base_class import Base

class ApplicationStatus(str, enum.Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    IN_REVIEW = "in_review"
    APPROVED = "approved"
    REJECTED = "rejected"

class Application(Base):
    __tablename__ = "applications"
    
    id = Column(Integer, primary_key=True, index=True)
    shop_id = Column(Integer, ForeignKey("shops.id"), nullable=False)
    status = Column(Enum(ApplicationStatus), default=ApplicationStatus.DRAFT, nullable=False)
    requested_amount = Column(Float, nullable=False)
    purpose = Column(String, nullable=True)

    shop = relationship("Shop", back_populates="applications")
    evidence_files = relationship("EvidenceFile", back_populates="application")
    voice_transcripts = relationship("VoiceTranscript", back_populates="application")
    credit_scores = relationship("CreditScore", back_populates="application")
    officer_notes = relationship("OfficerNote", back_populates="application")
