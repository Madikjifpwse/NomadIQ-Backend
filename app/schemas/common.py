from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID


class ResponseBase(BaseModel):
    message: Optional[str] = None
    success: bool = True


class PaginationParams(BaseModel):
    limit: int = Field(default=20, ge=1, le=100, description="Number of items per page")
    offset: int = Field(default=0, ge=0, description="Number of items to skip")


class PaginatedResponse(BaseModel):
    total: int
    limit: int
    offset: int
    has_more: bool


class LocationParams(BaseModel):
    latitude: float = Field(..., ge=-90, le=90, description="Latitude coordinate")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude coordinate")
    radius_km: float = Field(default=5.0, ge=0.1, le=50, description="Search radius in kilometers")


class TimestampMixin(BaseModel):
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True