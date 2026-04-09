from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
from uuid import UUID

from app.models.user import User, ExperienceLevel


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, username: str, email: str, password_hash: str, experience_level: ExperienceLevel) -> User:
        user = User(
            username=username.lower(),
            email=email.lower(),
            password_hash=password_hash,
            experience_level=experience_level
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_by_id(self, user_id: UUID) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_username(self, username: str) -> Optional[User]:
        return self.db.query(User).filter(func.lower(User.username) == username.lower()).first()

    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(func.lower(User.email) == email.lower()).first()

    def get_by_username_or_email(self, identifier: str) -> Optional[User]:
        identifier_lower = identifier.lower()
        return self.db.query(User).filter(
            (func.lower(User.username) == identifier_lower) |
            (func.lower(User.email) == identifier_lower)
        ).first()

    def update(self, user: User, **kwargs) -> User:
        for key, value in kwargs.items():
            if hasattr(user, key) and value is not None:
                setattr(user, key, value)

        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user: User) -> None:
        self.db.delete(user)
        self.db.commit()

    def count_visited_places(self, user_id: UUID) -> int:
        user = self.get_by_id(user_id)
        if user:
            return len(user.visited_places)
        return 0