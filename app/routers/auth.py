from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user, get_current_user_id
from app.services.auth_service import AuthService
from app.schemas.user import (
    UserRegister,
    UserLogin,
    Token,
    UserResponse,
    UserProfileResponse
)
from app.models.user import User
from uuid import UUID

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(
        user_data: UserRegister,
        db: Session = Depends(get_db)
):
    auth_service = AuthService(db)
    return auth_service.register(user_data)


@router.post("/login", response_model=Token)
def login(
        credentials: UserLogin,
        db: Session = Depends(get_db)
):
    auth_service = AuthService(db)
    return auth_service.login(credentials)


@router.get("/me", response_model=UserProfileResponse)
def get_current_user_profile(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    auth_service = AuthService(db)
    return auth_service.get_user_profile(current_user.id)