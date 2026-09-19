from datetime import datetime, timedelta
from typing import Any

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
from app.models.user import User

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
security = HTTPBearer()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(subject: str, expires_delta: timedelta | None = None) -> str:
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.access_token_expire_minutes))
    to_encode: dict[str, Any] = {'sub': subject, 'exp': expire}
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return encoded_jwt


def decode_access_token(token: str) -> str:
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        return payload['sub']
    except JWTError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token') from exc


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict[str, str]:
    token = credentials.credentials
    email = decode_access_token(token)
    return {'email': email}


def require_roles(*allowed_roles: str):
    def role_dependency(
        current_user: dict[str, str] = Depends(get_current_user),
        db: Session = Depends(get_db),
    ) -> dict[str, str]:
        user = db.scalar(select(User).where(User.email == current_user['email']))
        if not user or user.role.upper() not in {role.upper() for role in allowed_roles}:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Insufficient permissions')
        return {'email': user.email, 'role': user.role}

    return role_dependency
