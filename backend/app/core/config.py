from typing import List, Union, Any
from pydantic import AnyHttpUrl, validator
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "VisionKirana"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "super-secret-visionkirana-key-change-in-prod"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8 # 8 days
    GOOGLE_CLIENT_ID: str = ""
    CLOUDINARY_CLOUD_NAME: str = ""
    CLOUDINARY_API_KEY: str = ""
    CLOUDINARY_API_SECRET: str = ""
    ML_API_BASE_URL: str = "http://localhost:8001/api/v1"
    FRONTEND_URL: str = "http://localhost:5173"
    ADMIN_EMAIL: str = "admin@visionkirana.com"
    
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", "http://localhost:5173"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] | List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
    ]

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]], values: dict[str, Any]) -> Union[List[str], str]:
        origins = []
        if isinstance(v, str) and not v.startswith("["):
            origins = [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            origins = v
            
        frontend_url = values.get("FRONTEND_URL")
        if frontend_url and frontend_url not in origins:
            origins.append(frontend_url)
            
        return origins

    POSTGRES_SERVER: str = "db"
    POSTGRES_USER: str = "user"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_DB: str = "visionkirana"
    SQLALCHEMY_DATABASE_URI: str | None = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: str | None, values: dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return f"postgresql://{values.get('POSTGRES_USER')}:{values.get('POSTGRES_PASSWORD')}@{values.get('POSTGRES_SERVER')}/{values.get('POSTGRES_DB')}"

    class Config:
        case_sensitive = True

    # Cloud Storage
    STORAGE_PROVIDER: str = "aws" # aws, r2, supabase
    STORAGE_BUCKET: str = "visionkirana-bucket"
    STORAGE_ACCESS_KEY: str = "your-access-key"
    STORAGE_SECRET_KEY: str = "your-secret-key"
    STORAGE_REGION: str = "us-east-1"
    STORAGE_ENDPOINT: str | None = None

settings = Settings()
