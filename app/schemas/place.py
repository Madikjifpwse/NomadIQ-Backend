from pydantic import BaseModel, Field, validator
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from decimal import Decimal

from app.models.place import PlaceCategory
from app.models.user import ExperienceLevel



class PlaceCreate(BaseModel):
    google_place_id: Optional[str] = None
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    category: Optional[str] = None
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    address: Optional[str] = None
    popularity_score: int = Field(default=50, ge=0, le=100, description="0=hidden gem, 100=very popular")
    image_url: Optional[str] = None
    tags: Optional[List[str]] = Field(default=[], description="List of tags (e.g., ['food', 'historic'])")

    @validator('tags')
    def validate_tags(cls, v):
        if v:
            return list(set(tag.lower().strip() for tag in v if tag.strip()))
        return []


class PlaceUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    category: Optional[str] = None
    popularity_score: Optional[int] = Field(None, ge=0, le=100)
    image_url: Optional[str] = None
    tags: Optional[List[str]] = None

    class Config:
        from_attributes = True


class PlaceSearchFilters(BaseModel):
    experience_level: Optional[ExperienceLevel] = Field(
        None,
        description="Filter by experience level (first_timer shows popular, advanced shows hidden gems)"
    )
    category: Optional[str] = Field(None, description="Filter by category")
    tags: Optional[List[str]] = Field(None, description="Filter by tags (OR logic)")
    exclude_visited: bool = Field(default=True, description="Exclude places already visited by user")

    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    radius_km: Optional[float] = Field(None, ge=0.1, le=50, description="Search radius in km")

    limit: int = Field(default=20, ge=1, le=100)
    offset: int = Field(default=0, ge=0)

class PlaceTagResponse(BaseModel):
    tag: str

    class Config:
        from_attributes = True

class PlaceResponse(BaseModel):
    id: UUID
    google_place_id: Optional[str]
    name: str
    description: Optional[str]
    category: Optional[str]
    latitude: Decimal
    longitude: Decimal
    address: Optional[str]
    popularity_score: int
    image_url: Optional[str]
    tags: List[str] = []
    created_at: datetime
    updated_at: datetime

    is_visited: bool = False
    distance_km: Optional[float] = None

    class Config:
        from_attributes = True

    @validator('tags', pre=True)
    def extract_tags(cls, v):
        if v and isinstance(v, list):
            if len(v) > 0 and hasattr(v[0], 'tag'):
                return [tag.tag for tag in v]
        return v or []

class PlaceDetailResponse(PlaceResponse):
    visit_count: int = 0
    average_rating: Optional[float] = None
    class Config:
        from_attributes = True

class PlaceListResponse(BaseModel):
    places: List[PlaceResponse]
    total: int
    limit: int
    offset: int
    has_more: bool