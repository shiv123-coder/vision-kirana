from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status, BackgroundTasks
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.api.deps import get_db, get_current_active_user
from app.models.user import User
from app.models.application import Application
from app.models.evidence_file import EvidenceFile, FileTypeEnum
from app.models.voice import VoiceTranscript
from app.services.storage import get_storage_adapter
from app.services.analysis_service import analyze_uploaded_image, analyze_uploaded_document
from app.services.voice_service import process_uploaded_audio

router = APIRouter()

MAX_IMAGE_SIZE = 5 * 1024 * 1024 # 5 MB
MAX_DOC_SIZE = 10 * 1024 * 1024 # 10 MB
MAX_AUDIO_SIZE = 10 * 1024 * 1024 # 10 MB

ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png", "image/webp"]
ALLOWED_DOC_TYPES = ["application/pdf"]
ALLOWED_AUDIO_TYPES = ["audio/mpeg", "audio/wav", "audio/mp4", "audio/x-m4a"]

@router.post("/", status_code=status.HTTP_201_CREATED)
async def upload_file(
    file: UploadFile = File(...),
    application_id: int = Form(...),
    file_category: str = Form(...), # "image", "document", "audio"
    specific_type: str = Form(...), # "shop_front", "invoice", "voice_note", etc.
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    storage_adapter = Depends(get_storage_adapter),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    """
    Securely upload a file to cloud storage and create a DB record.
    """
    # Verify application belongs to user
    application = db.query(Application).filter(Application.id == application_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
        
    if application.shop.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to upload for this application")

    # Read file size (by seeking to end, then back to 0)
    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.file.seek(0)
    
    # Validation
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

    # Upload to Cloud Storage
    directory = f"applications/{application_id}/{file_category}"
    try:
        s3_key = storage_adapter.upload_file(file, directory)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to upload file to storage")
        
    # Read bytes for background analysis before closing the file
    file.file.seek(0)
    file_bytes = file.file.read()

    # DB Record Creation
    file_url = storage_adapter.get_file_url(s3_key)
    
    if file_category in ["image", "document"]:
        try:
            # Map specific type string to enum if possible
            enum_type = FileTypeEnum(specific_type)
        except ValueError:
            enum_type = FileTypeEnum.OTHER
            
        db_file = EvidenceFile(
            application_id=application_id,
            file_url=file_url,
            file_type=enum_type,
            s3_key=s3_key
        )
        db.add(db_file)
        
    elif file_category == "audio":
        db_file = VoiceTranscript(
            application_id=application_id,
            file_url=file_url
            # s3_key could be added if schema is updated, but let's stick to url for now
        )
        db.add(db_file)
        
        
    db.commit()
    db.refresh(db_file)
    
    # Enqueue background analysis for images
    if file_category == "image":
        # Create a new session for the background task to avoid thread issues
        bg_db = SessionLocal()
        background_tasks.add_task(analyze_uploaded_image, file_bytes, db_file.id, bg_db)
    elif file_category == "document":
        bg_db = SessionLocal()
        background_tasks.add_task(analyze_uploaded_document, file_bytes, file_category, db_file.id, bg_db)
    elif file_category == "audio":
        bg_db = SessionLocal()
        background_tasks.add_task(process_uploaded_audio, file_bytes, db_file.id, bg_db)
    
    return {"message": "File uploaded successfully", "id": db_file.id, "url": file_url}
