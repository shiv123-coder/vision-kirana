import boto3
from abc import ABC, abstractmethod
from typing import BinaryIO
from fastapi import UploadFile
import uuid
import os
from app.core.config import settings
from botocore.exceptions import ClientError
import logging

logger = logging.getLogger(__name__)

class StorageAdapter(ABC):
    @abstractmethod
    def upload_file(self, file: UploadFile, directory: str) -> str:
        """Uploads a file and returns the storage key or URL."""
        pass
        
    @abstractmethod
    def get_file_url(self, key: str) -> str:
        """Returns the public or presigned URL for a file key."""
        pass

    @abstractmethod
    def delete_file(self, key: str) -> bool:
        """Deletes a file by its key."""
        pass

class BaseS3Adapter(StorageAdapter):
    def __init__(self, endpoint_url: str = None):
        self.bucket = settings.STORAGE_BUCKET
        
        # Initialize boto3 client
        client_kwargs = {
            'aws_access_key_id': settings.STORAGE_ACCESS_KEY,
            'aws_secret_access_key': settings.STORAGE_SECRET_KEY,
            'region_name': settings.STORAGE_REGION,
        }
        
        if endpoint_url:
            client_kwargs['endpoint_url'] = endpoint_url
            
        self.s3_client = boto3.client('s3', **client_kwargs)

    def _generate_key(self, file: UploadFile, directory: str) -> str:
        _, ext = os.path.splitext(file.filename)
        return f"{directory}/{uuid.uuid4()}{ext}"

    def upload_file(self, file: UploadFile, directory: str) -> str:
        key = self._generate_key(file, directory)
        try:
            self.s3_client.upload_fileobj(
                file.file,
                self.bucket,
                key,
                ExtraArgs={'ContentType': file.content_type}
            )
            return key
        except ClientError as e:
            logger.error(f"Failed to upload file to S3: {e}")
            raise Exception("Failed to upload file")

    def get_file_url(self, key: str) -> str:
        # Generate presigned URL for secure access (expires in 1 hour)
        try:
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket, 'Key': key},
                ExpiresIn=3600
            )
            return url
        except ClientError as e:
            logger.error(f"Failed to generate presigned URL: {e}")
            return ""

    def delete_file(self, key: str) -> bool:
        try:
            self.s3_client.delete_object(Bucket=self.bucket, Key=key)
            return True
        except ClientError as e:
            logger.error(f"Failed to delete file from S3: {e}")
            return False

class AWSS3Adapter(BaseS3Adapter):
    def __init__(self):
        super().__init__(endpoint_url=settings.STORAGE_ENDPOINT)

class CloudflareR2Adapter(BaseS3Adapter):
    def __init__(self):
        # R2 requires an endpoint URL
        endpoint = settings.STORAGE_ENDPOINT
        if not endpoint:
            raise ValueError("STORAGE_ENDPOINT is required for Cloudflare R2")
        super().__init__(endpoint_url=endpoint)

class SupabaseStorageAdapter(BaseS3Adapter):
    def __init__(self):
        # Supabase S3 API requires endpoint URL and force path style
        endpoint = settings.STORAGE_ENDPOINT
        if not endpoint:
            raise ValueError("STORAGE_ENDPOINT is required for Supabase Storage")
        super().__init__(endpoint_url=endpoint)
        
        # Override client to use force_path_style required by Supabase S3 compatibility
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.STORAGE_ACCESS_KEY,
            aws_secret_access_key=settings.STORAGE_SECRET_KEY,
            region_name=settings.STORAGE_REGION,
            endpoint_url=endpoint,
            config=boto3.session.Config(signature_version='s3v4')
        )

def get_storage_adapter() -> StorageAdapter:
    provider = settings.STORAGE_PROVIDER.lower()
    
    if provider == 'r2':
        return CloudflareR2Adapter()
    elif provider == 'supabase':
        return SupabaseStorageAdapter()
    elif provider == 'aws':
        return AWSS3Adapter()
    else:
        # Default to AWS S3 if unknown
        logger.warning(f"Unknown storage provider {provider}, defaulting to AWS S3")
        return AWSS3Adapter()
