from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class ExampleBase(BaseModel):
    """Base schema with common fields"""
    title: str = Field(..., min_length=1, max_length=255, description="Title of the example")
    description: Optional[str] = Field(None, description="Description of the example")
    status: str = Field(default="active", description="Status of the example")


class ExampleCreate(ExampleBase):
    """Schema for creating a new example"""
    pass


class ExampleUpdate(BaseModel):
    """Schema for updating an example (all fields optional)"""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    status: Optional[str] = None


class ExampleResponse(ExampleBase):
    """Schema for example response"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    # Pydantic v2 config
    model_config = ConfigDict(from_attributes=True)
