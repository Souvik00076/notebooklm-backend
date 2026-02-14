from pydantic import BaseModel, Field
from datetime import datetime


class UploadResponse(BaseModel):
    """Schema for file upload response"""
    filename: str = Field(..., description="Name of the uploaded file")
    original_filename: str = Field(..., description="Original filename provided by user")
    file_path: str = Field(..., description="Path where the file is stored")
    file_size: int = Field(..., description="Size of the file in bytes")
    content_type: str = Field(..., description="MIME type of the file")
    uploaded_at: datetime = Field(..., description="Timestamp of upload")
    message: str = Field(default="File uploaded successfully", description="Success message")
