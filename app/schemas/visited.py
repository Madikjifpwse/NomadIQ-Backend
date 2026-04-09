from pydantic import BaseModel, Field, validator
from typing import Optional
from uuid import UUID
from datetime import datetime

from app.schemas.place import PlaceResponse

class VisitedPlaceCreate(BaseModel):
    place_id: UUID = Field(..., description="ID of the place being visited")
    rating: Optional[int] = Field(None, ge=1, le=5, description="User rating (1-5 stars)")
    notes: Optional[str] = Field(None, max_length=1000, description="Optional user notes")

    @validator('notes')
    def clean_notes(cls, v):
        return v.strip() if v else None


class VisitedPlaceUpdate(BaseModel):
    rating: Optional[int] = Field(None, ge=1, le=5, description="Update rating")
    notes: Optional[str] = Field(None, max_length=1000, description="Update notes")

    class Config:
        from_attributes = True

class VisitedPlaceResponse(BaseModel):
    id: UUID
    user_id: UUID
    place_id: UUID
    visited_at: datetime
    rating: Optional[int]
    notes: Optional[str]

    class Config:
        from_attributes = True


class VisitedPlaceWithDetails(VisitedPlaceResponse):
    place: PlaceResponse

    class Config:
        from_attributes = True

class VisitedPlaceListResponse(BaseModel):
    visited_places: list[VisitedPlaceWithDetails]
    total: int
    limit: int
    offset: int
    has_more: bool


class VisitedPlaceStats(BaseModel):
    total_visited: int
    average_rating: Optional[float]
    most_common_category: Optional[str]
    most_common_tags: list[str] = []