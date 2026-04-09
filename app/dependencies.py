from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID

from app.database import get_db
from app.models.user import User
from app.services.auth_service import AuthService
from app.utils.security import extract_user_id_from_token

security = HTTPBearer()


def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: Session = Depends(get_db)
) -> User:
    token = credentials.credentials
    user_id = extract_user_id_from_token(token)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    auth_service = AuthService(db)
    user = auth_service.get_current_user(user_id)

    return user

def get_current_user_optional(
        credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False)),
        db: Session = Depends(get_db)
) -> Optional[User]:
    if credentials is None:
        return None
    try:
        token = credentials.credentials
        user_id = extract_user_id_from_token(token)

        if user_id is None:
            return None

        auth_service = AuthService(db)
        user = auth_service.get_current_user(user_id)
        return user
    except HTTPException:
        return None
    except Exception:
        return None

def get_current_user_id(current_user: User = Depends(get_current_user)) -> UUID:
    return current_user.id