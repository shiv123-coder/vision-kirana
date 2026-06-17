from sqlalchemy import Column, Integer, Float, ForeignKey, JSON, String
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class CreditScore(Base):
    __tablename__ = "credit_scores"
    
    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"), nullable=False)
    final_score = Column(Float, nullable=False)
    risk_category = Column(String, nullable=False) # e.g. LOW, MEDIUM, HIGH
    features_used = Column(JSON, nullable=True) # Record of what factors influenced the score

    application = relationship("Application", back_populates="credit_scores")
