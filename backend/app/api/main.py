from fastapi import APIRouter
from app.api.routes import auth, shops, upload, analysis, report, system

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(shops.router, prefix="/shops", tags=["shops"])
api_router.include_router(upload.router, prefix="/upload", tags=["upload"])
api_router.include_router(analysis.router, prefix="/analysis", tags=["analysis"])
api_router.include_router(report.router, prefix="/report", tags=["report"])
api_router.include_router(system.router, prefix="/system", tags=["system"])
