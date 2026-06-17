from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

db_url = settings.SQLALCHEMY_DATABASE_URI

# Neon PostgreSQL requires sslmode=require
if db_url and "neon.tech" in db_url and "sslmode=require" not in db_url:
    join_char = "&" if "?" in db_url else "?"
    db_url += f"{join_char}sslmode=require"

# Added connection pooling for production readiness
engine = create_engine(
    db_url, 
    pool_pre_ping=True, 
    pool_size=5, 
    max_overflow=10
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
