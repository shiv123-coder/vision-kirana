from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class VoiceTranscript(Base):
    __tablename__ = "voice_transcripts"
    
    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"), nullable=False)
    file_url = Column(String, nullable=False)
    transcript_text = Column(String, nullable=True)
    sentiment_score = Column(String, nullable=True)
    business_summary = Column(String, nullable=True)
    loan_purpose = Column(String, nullable=True)
    challenges = Column(String, nullable=True)
    future_plans = Column(String, nullable=True)

    application = relationship("Application", back_populates="voice_transcripts")
