from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from uuid import UUID

from app.database import get_db
from app.dependencies import get_current_user_optional
from app.services.place_service import PlaceService
from app.schemas.place import (
    PlaceSearchFilters,
    PlaceResponse,
    PlaceDetailResponse,
    PlaceListResponse
)
from app.models.user import User, ExperienceLevel

router = APIRouter(prefix="/places", tags=["Places"])


@router.get("", response_model=PlaceListResponse)
def search_places(
        experience_level: Optional[ExperienceLevel] = Query(
            None,
            description="Filter by experience level: 'first_timer' for popular places, 'advanced' for hidden gems"
        ),
        category: Optional[str] = Query(None,
                                        description="Filter by category (e.g., 'must_see', 'student_friendly', 'local_secret')"),
        tags: Optional[str] = Query(None, description="Comma-separated tags (e.g., 'food,historic')"),

        latitude: Optional[float] = Query(None, ge=-90, le=90, description="Latitude for nearby search"),
        longitude: Optional[float] = Query(None, ge=-180, le=180, description="Longitude for nearby search"),
        radius_km: Optional[float] = Query(None, ge=0.1, le=50, description="Search radius in kilometers"),

        exclude_visited: bool = Query(True, description="Exclude places already visited (requires authentication)"),

        limit: int = Query(20, ge=1, le=100, description="Number of results per page"),
        offset: int = Query(0, ge=0, description="Number of results to skip"),

        current_user: Optional[User] = Depends(get_current_user_optional),
        db: Session = Depends(get_db)
):
    tag_list = None
    if tags:
        tag_list = [tag.strip() for tag in tags.split(',') if tag.strip()]

    filters = PlaceSearchFilters(
        experience_level=experience_level,
        category=category,
        tags=tag_list,
        exclude_visited=exclude_visited,
        latitude=latitude,
        longitude=longitude,
        radius_km=radius_km,
        limit=limit,
        offset=offset
    )
    place_service = PlaceService(db)
    user_id = current_user.id if current_user else None
    return place_service.search_places(filters, user_id=user_id)


@router.get("/{place_id}", response_model=PlaceDetailResponse)
def get_place_details(
        place_id: UUID,
        current_user: Optional[User] = Depends(get_current_user_optional),
        db: Session = Depends(get_db)
):
    place_service = PlaceService(db)
    user_id = current_user.id if current_user else None
    return place_service.get_place_by_id(place_id, user_id=user_id)