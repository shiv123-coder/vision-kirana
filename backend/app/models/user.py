from sqlalchemy import Column, Integer, String, Boolean, Enum
from sqlalchemy.orm import relationship
import enum
from app.db.base_class import Base

class RoleEnum(str, enum.Enum):
    ADMIN = "admin"
    LOAN_OFFICER = "loan_officer"
    SHOP_OWNER = "shop_owner"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, index=True)
    role = Column(Enum(RoleEnum), default=RoleEnum.SHOP_OWNER, nullable=False)
    is_active = Column(Boolean, default=True)

    shops = relationship("Shop", back_populates="owner")
    audit_logs = relationship("AuditLog", back_populates="user")
    notes = relationship("OfficerNote", back_populates="officer")
