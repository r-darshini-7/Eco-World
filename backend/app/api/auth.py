from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import create_access_token, get_current_user, hash_password, verify_password
from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import TokenResponse, UserLogin, UserPublic, UserRegister

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/register', response_model=UserPublic, status_code=status.HTTP_201_CREATED)
def register_user(payload: UserRegister, db: Session = Depends(get_db)) -> dict[str, str]:
    existing = db.scalar(select(User).where(User.email == payload.email.lower()))
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Email already registered')

    user = User(
        email=payload.email.lower(),
        full_name=payload.full_name,
        password_hash=hash_password(payload.password),
        role='ADMIN',
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {'email': user.email, 'full_name': user.full_name, 'role': user.role}


@router.post('/login', response_model=TokenResponse)
def login_user(payload: UserLogin, db: Session = Depends(get_db)) -> dict[str, str]:
    user = db.scalar(select(User).where(User.email == payload.email.lower()))
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid email or password')

    token = create_access_token(user.email)
    return {'access_token': token, 'token_type': 'bearer'}


@router.get('/me', response_model=UserPublic)
def get_me(current_user: dict[str, str] = Depends(get_current_user), db: Session = Depends(get_db)) -> dict[str, str]:
    user = db.scalar(select(User).where(User.email == current_user['email']))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')
    return {'email': user.email, 'full_name': user.full_name, 'role': user.role}
