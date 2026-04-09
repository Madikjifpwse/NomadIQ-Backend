from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from typing import Optional
from uuid import UUID

from app.models.user import User, ExperienceLevel
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserRegister, UserLogin, Token, UserResponse, UserProfileResponse
from app.utils.security import hash_password, verify_password, create_access_token


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)

    def register(self, user_data: UserRegister) -> UserResponse:
        existing_user = self.user_repo.get_by_username(user_data.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )

        existing_email = self.user_repo.get_by_email(user_data.email)
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        password_hash = hash_password(user_data.password)

        try:
            user = self.user_repo.create(
                username=user_data.username,
                email=user_data.email,
                password_hash=password_hash,
                experience_level=user_data.experience_level
            )
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User registration failed due to database constraint"
            )

        return UserResponse.model_validate(user)

    def login(self, credentials: UserLogin) -> Token:
        user = self.user_repo.get_by_username_or_email(credentials.username)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not verify_password(credentials.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token = create_access_token(
            data={"user_id": str(user.id), "username": user.username}
        )

        return Token(access_token=access_token, token_type="bearer")

    def get_current_user(self, user_id: UUID) -> User:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user

    def get_user_profile(self, user_id: UUID) -> UserProfileResponse:
        user = self.get_current_user(user_id)
        visited_count = self.user_repo.count_visited_places(user_id)
        profile = UserProfileResponse.model_validate(user)
        profile.visited_places_count = visited_count

        return profile

    def update_user_profile(self, user_id: UUID, email: Optional[str] = None,
                            experience_level: Optional[ExperienceLevel] = None) -> UserResponse:
        user = self.get_current_user(user_id)
        if email and email.lower() != user.email.lower():
            existing_email = self.user_repo.get_by_email(email)
            if existing_email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )

        updated_user = self.user_repo.update(
            user,
            email=email,
            experience_level=experience_level
        )
        return UserResponse.model_validate(updated_user)