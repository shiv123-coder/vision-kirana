import logging
from sqlalchemy.orm import Session
from app.db.session import SessionLocal, engine
from app.db.base_class import Base
from app.models.user import User, RoleEnum
from app.core.security import get_password_hash

# Ensure all models are imported before creating tables
from app.db import base  # noqa

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db(db: Session) -> None:
    # Normally Alembic handles this, but for seeding we can ensure tables exist
    # Base.metadata.create_all(bind=engine)
    
    admin = db.query(User).filter(User.email == "admin@visionkirana.com").first()
    if not admin:
        admin_user = User(
            email="admin@visionkirana.com",
            hashed_password=get_password_hash("admin123"),
            full_name="System Admin",
            role=RoleEnum.ADMIN,
            is_active=True,
        )
        db.add(admin_user)
        
    officer = db.query(User).filter(User.email == "officer@visionkirana.com").first()
    if not officer:
        officer_user = User(
            email="officer@visionkirana.com",
            hashed_password=get_password_hash("officer123"),
            full_name="Loan Officer 1",
            role=RoleEnum.LOAN_OFFICER,
            is_active=True,
        )
        db.add(officer_user)

    merchant = db.query(User).filter(User.email == "merchant@visionkirana.com").first()
    if not merchant:
        merchant_user = User(
            email="merchant@visionkirana.com",
            hashed_password=get_password_hash("merchant123"),
            full_name="Kirana Merchant 1",
            role=RoleEnum.SHOP_OWNER,
            is_active=True,
        )
        db.add(merchant_user)
        
    db.commit()

if __name__ == "__main__":
    logger.info("Creating initial data")
    db = SessionLocal()
    init_db(db)
    logger.info("Initial data created")
