from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status, BackgroundTasks
from sqlalchemy.orm import Session
import httpx
from app.db.session import SessionLocal
from app.api.deps import get_db, get_current_active_user
from app.models.user import User, RoleEnum
from app.models.application import Application
from app.models.evidence_file import EvidenceFile, FileTypeEnum
from app.models.voice import VoiceTranscript
from app.services.storage.factory import get_storage_provider
from app.core.config import settings

router = APIRouter()

MAX_IMAGE_SIZE = 5 * 1024 * 1024 # 5 MB
MAX_DOC_SIZE = 10 * 1024 * 1024 # 10 MB
MAX_AUDIO_SIZE = 10 * 1024 * 1024 # 10 MB

ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png", "image/webp"]
ALLOWED_DOC_TYPES = ["application/pdf"]
ALLOWED_AUDIO_TYPES = ["audio/mpeg", "audio/wav", "audio/mp4", "audio/x-m4a"]

def call_ml_service_bg(file_bytes: bytes, filename: str, content_type: str, file_category: str, specific_type: str, db_file_id: int):
    url = f"{settings.ML_API_BASE_URL}"
    files = {'file': (filename, file_bytes, content_type)}
    try:
        with httpx.Client(timeout=60.0) as client:
            if file_category == "image":
                client.post(f"{url}/analyze/image", files=files)
            elif file_category == "document":
                client.post(f"{url}/analyze/ocr", params={"category": specific_type}, files=files)
            elif file_category == "audio":
                client.post(f"{url}/analyze/voice", files=files)
    except Exception as e:
        print(f"ML Service call failed: {e}")

@router.post("/", status_code=status.HTTP_201_CREATED)
async def upload_file(
    file: UploadFile = File(...),
    application_id: int = Form(...),
    file_category: str = Form(...), # "image", "document", "audio"
    specific_type: str = Form(...), # "shop_front", "invoice", "voice_note", etc.
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    """
    Securely upload a file to Cloudinary and create a DB record.
    """
    application = db.query(Application).filter(Application.id == application_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
        
    if application.shop.owner_id != current_user.id and current_user.role not in [RoleEnum.ADMIN, RoleEnum.LOAN_OFFICER]:
        raise HTTPException(status_code=403, detail="Not authorized to upload for this application")

    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.file.seek(0)
    
    content_type = file.content_type
    
    if file_category == "image":
        if content_type not in ALLOWED_IMAGE_TYPES:
            raise HTTPException(status_code=400, detail=f"Invalid image type. Allowed: {ALLOWED_IMAGE_TYPES}")
        if file_size > MAX_IMAGE_SIZE:
            raise HTTPException(status_code=400, detail="Image size exceeds 5MB limit")
    elif file_category == "document":
        if content_type not in ALLOWED_DOC_TYPES:
            raise HTTPException(status_code=400, detail=f"Invalid document type. Allowed: {ALLOWED_DOC_TYPES}")
        if file_size > MAX_DOC_SIZE:
            raise HTTPException(status_code=400, detail="Document size exceeds 10MB limit")
    elif file_category == "audio":
        if content_type not in ALLOWED_AUDIO_TYPES:
            raise HTTPException(status_code=400, detail=f"Invalid audio type. Allowed: {ALLOWED_AUDIO_TYPES}")
        if file_size > MAX_AUDIO_SIZE:
            raise HTTPException(status_code=400, detail="Audio size exceeds 10MB limit")
    else:
        raise HTTPException(status_code=400, detail="Invalid file category")

    folder_map = {
        "shop_front": "visionkirana/shop-images",
        "inventory": "visionkirana/inventory-images",
        "invoice": "visionkirana/invoices",
        "receipt": "visionkirana/receipts",
        "voice_note": "visionkirana/voice-notes",
    }
    folder = folder_map.get(specific_type, "visionkirana/reports")
    
    storage = get_storage_provider("cloudinary")
    try:
        file_bytes = file.file.read()
        file.file.seek(0)
        upload_res = storage.upload_file(file.file, file.filename, content_type, folder)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload file to storage: {str(e)}")
        
    if file_category in ["image", "document"]:
        try:
            enum_type = FileTypeEnum(specific_type)
        except ValueError:
            enum_type = FileTypeEnum.OTHER
            
        db_file = EvidenceFile(
            application_id=application_id,
            shop_id=application.shop_id,
            uploaded_by=current_user.id,
            file_name=file.filename,
            file_type=enum_type,
            storage_provider="cloudinary",
            storage_url=upload_res.get("url"),
            storage_public_id=upload_res.get("public_id"),
            mime_type=content_type,
            file_size=file_size,
            processing_status="pending"
        )
        db.add(db_file)
    elif file_category == "audio":
        db_file = VoiceTranscript(
            application_id=application_id,
            file_url=upload_res.get("url")
        )
        db.add(db_file)
        
    db.commit()
    db.refresh(db_file)
    
    background_tasks.add_task(call_ml_service_bg, file_bytes, file.filename, content_type, file_category, specific_type, db_file.id)
    
    return {"message": "File uploaded successfully", "id": db_file.id, "url": upload_res.get("url")}
