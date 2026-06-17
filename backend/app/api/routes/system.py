from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.api.deps import get_db, get_current_active_admin
from app.models.user import User
import httpx
from app.core.config import settings
import cloudinary.api

router = APIRouter()

@router.get("/status")
def get_system_status(
    db: Session = Depends(get_db),
    # current_user: User = Depends(get_current_active_admin) # Protect the route if needed
):
    status = {
        "database": "unknown",
        "ml_service": "unknown",
        "cloudinary": "unknown"
    }

    # 1. Check Database
    try:
        db.execute(text("SELECT 1"))
        status["database"] = "healthy"
    except Exception:
        status["database"] = "unhealthy"

    # 2. Check ML Service
    try:
        response = httpx.get(f"{settings.ML_API_BASE_URL}/health", timeout=5.0)
        if response.status_code == 200:
            status["ml_service"] = "healthy"
        else:
            status["ml_service"] = "unhealthy"
    except Exception:
        status["ml_service"] = "unreachable"

    # 3. Check Cloudinary
    try:
        # Just pinging the API with a generic status check or using the config
        cloudinary.api.ping()
        status["cloudinary"] = "healthy"
    except Exception:
        status["cloudinary"] = "unhealthy"

    overall_health = "healthy" if all(v == "healthy" for v in status.values()) else "degraded"
    
    return {
        "status": overall_health,
        "services": status
    }
