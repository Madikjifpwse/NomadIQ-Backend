from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.database import get_db
from app.dependencies import get_current_user
from app.services.visited_service import VisitedPlaceService
from app.schemas.visited import (
    VisitedPlaceCreate,
    VisitedPlaceUpdate,
    VisitedPlaceResponse
)
from app.models.user import User

router = APIRouter(prefix="/visited", tags=["Visited Places"])


@router.post("", response_model=VisitedPlaceResponse, status_code=status.HTTP_201_CREATED)
def mark_place_as_visited(
        visit_data: VisitedPlaceCreate,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    visited_service = VisitedPlaceService(db)
    return visited_service.mark_as_visited(current_user.id, visit_data)


@router.patch("/{place_id}", response_model=VisitedPlaceResponse)
def update_visited_place(
        place_id: UUID,
        update_data: VisitedPlaceUpdate,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    visited_service = VisitedPlaceService(db)
    return visited_service.update_visited(current_user.id, place_id, update_data)

@router.delete("/{place_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_from_visited(
        place_id: UUID,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    visited_service = VisitedPlaceService(db)
    visited_service.remove_visited(current_user.id, place_id)
    return None

@router.get("/check/{place_id}", response_model=dict)
def check_if_visited(
        place_id: UUID,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    visited_service = VisitedPlaceService(db)
    is_visited = visited_service.check_if_visited(current_user.id, place_id)
    return {
        "place_id": str(place_id),
        "is_visited": is_visited
    }