from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Shop(Base):
    __tablename__ = "shops"
    
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    name = Column(String, index=True, nullable=False)
    owner_name = Column(String, nullable=False)
    mobile = Column(String, index=True, nullable=False)
    address = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    category = Column(String, nullable=False)
    years_in_business = Column(Integer, nullable=False)
    monthly_sales = Column(Float, nullable=False)
    
    gst_number = Column(String, unique=True, index=True, nullable=True)

    owner = relationship("User", back_populates="shops")
    applications = relationship("Application", back_populates="shop")
