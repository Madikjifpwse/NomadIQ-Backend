from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from uuid import UUID
from datetime import datetime

from app.models.user import ExperienceLevel



class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="Unique username")
    email: EmailStr = Field(..., description="Valid email address")
    password: str = Field(..., min_length=8, max_length=100, description="Password (min 8 characters)")
    experience_level: ExperienceLevel = Field(
        default=ExperienceLevel.FIRST_TIMER,
        description="User's travel experience level"
    )

    @validator('username')
    def username_alphanumeric(cls, v):
        if not v.replace('_', '').isalnum():
            raise ValueError('Username must be alphanumeric (underscores allowed)')
        return v.lower()


class UserLogin(BaseModel):
    username: str = Field(..., description="Username or email")
    password: str = Field(..., description="User password")


class UserUpdate(BaseModel):
    experience_level: Optional[ExperienceLevel] = Field(None, description="Update experience level")
    email: Optional[EmailStr] = Field(None, description="Update email")

    class Config:
        from_attributes = True



class UserResponse(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    experience_level: ExperienceLevel
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserProfileResponse(UserResponse):
    visited_places_count: int = 0

    class Config:
        from_attributes = True



class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: UUID
    username: str