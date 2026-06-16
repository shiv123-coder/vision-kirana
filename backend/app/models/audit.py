from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    action = Column(String, nullable=False) # e.g., "APPROVED_LOAN", "UPLOADED_EVIDENCE"
    target_resource = Column(String, nullable=False) # e.g., "Application"
    target_id = Column(Integer, nullable=True)
    ip_address = Column(String, nullable=True)

    user = relationship("User", back_populates="audit_logs")
