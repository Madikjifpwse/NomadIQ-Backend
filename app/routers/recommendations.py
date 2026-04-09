from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional, List

from app.database import get_db
from app.dependencies import get_current_user
from app.services.recommendation_service import RecommendationService
from app.schemas.place import PlaceListResponse
from app.models.user import User, ExperienceLevel

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])


@router.get("", response_model=PlaceListResponse)
def get_personalized_recommendations(
        experience_level: Optional[ExperienceLevel] = Query(
            None,
            description="Override user's experience level for this search"
        ),
        category: Optional[str] = Query(None, description="Filter by category"),
        tags: Optional[str] = Query(None, description="Comma-separated tags (overrides learned preferences)"),
        latitude: Optional[float] = Query(None, ge=-90, le=90, description="Current latitude"),
        longitude: Optional[float] = Query(None, ge=-180, le=180, description="Current longitude"),
        radius_km: Optional[float] = Query(5.0, ge=0.1, le=50, description="Search radius in km (default 5)"),
        limit: int = Query(10, ge=1, le=50, description="Number of recommendations"),
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    tag_list = None
    if tags:
        tag_list = [tag.strip() for tag in tags.split(',') if tag.strip()]
    recommendation_service = RecommendationService(db)
    return recommendation_service.get_recommendations(
        user=current_user,
        experience_level=experience_level,
        category=category,
        tags=tag_list,
        latitude=latitude,
        longitude=longitude,
        radius_km=radius_km if latitude and longitude else None,
        limit=limit
    )

@router.get("/nearby", response_model=PlaceListResponse)
def get_nearby_recommendations(
        latitude: float = Query(..., ge=-90, le=90, description="Current latitude"),
        longitude: float = Query(..., ge=-180, le=180, description="Current longitude"),
        radius_km: float = Query(5.0, ge=0.1, le=50, description="Search radius in km"),
        limit: int = Query(10, ge=1, le=50, description="Number of recommendations"),

        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    recommendation_service = RecommendationService(db)
    return recommendation_service.get_nearby_recommendations(
        user=current_user,
        latitude=latitude,
        longitude=longitude,
        radius_km=radius_km,
        limit=limit
    )