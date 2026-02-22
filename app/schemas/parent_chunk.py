from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict, Any
from datetime import datetime
from uuid import UUID


class ParentChunkBase(BaseModel):
    """Base schema with common fields for parent chunks"""
    content: str = Field(...,
                         description="The actual parent chunk text content")
    chunk_index: int = Field(..., ge=0,
                             description="Position/order of this chunk in sequence")
    token_count: Optional[int] = Field(
        None, ge=0, description="Number of tokens in this chunk")
    char_count: Optional[int] = Field(
        None, ge=0, description="Character count of this chunk")
    metadata: Optional[Dict[str, Any]] = Field(
        default_factory=dict, description="Flexible metadata storage")


class ParentChunkCreate(ParentChunkBase):
    """Schema for creating a new parent chunk"""
    content_hash: str = Field(..., min_length=64, max_length=64,
                              description="SHA-256 hash of content")


class ParentChunkUpdate(BaseModel):
    """Schema for updating a parent chunk (all fields optional)"""
    content: Optional[str] = None
    content_hash: Optional[str] = Field(None, min_length=64, max_length=64)
    chunk_index: Optional[int] = Field(None, ge=0)
    token_count: Optional[int] = Field(None, ge=0)
    char_count: Optional[int] = Field(None, ge=0)
    metadata: Optional[Dict[str, Any]] = None


class ParentChunkResponse(ParentChunkBase):
    """Schema for parent chunk response"""
    id: UUID
    content_hash: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    # Pydantic v2 config
    model_config = ConfigDict(from_attributes=True)


class ParentChunkInDB(ParentChunkResponse):
    """Schema representing parent chunk as stored in database"""
    pass
