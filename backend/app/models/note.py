from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class OfficerNote(Base):
    __tablename__ = "officer_notes"
    
    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"), nullable=False)
    officer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    note_text = Column(String, nullable=False)

    application = relationship("Application", back_populates="officer_notes")
    officer = relationship("User", back_populates="notes")
