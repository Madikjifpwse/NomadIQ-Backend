from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.services.auth_service import AuthService
from app.services.visited_service import VisitedPlaceService
from app.schemas.user import UserUpdate, UserResponse
from app.schemas.visited import VisitedPlaceListResponse, VisitedPlaceStats
from app.models.user import User

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserResponse)
def get_my_profile(
        current_user: User = Depends(get_current_user)
):
    return UserResponse.model_validate(current_user)


@router.patch("/me", response_model=UserResponse)
def update_my_profile(
        update_data: UserUpdate,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    auth_service = AuthService(db)
    return auth_service.update_user_profile(
        user_id=current_user.id,
        email=update_data.email,
        experience_level=update_data.experience_level
    )


@router.get("/me/visited", response_model=VisitedPlaceListResponse)
def get_my_visited_places(
        limit: int = 50,
        offset: int = 0,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    visited_service = VisitedPlaceService(db)
    return visited_service.get_user_visited_places(
        user_id=current_user.id,
        limit=min(limit, 100),
        offset=offset
    )


@router.get("/me/stats", response_model=VisitedPlaceStats)
def get_my_visit_statistics(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    visited_service = VisitedPlaceService(db)
    return visited_service.get_user_statistics(current_user.id)