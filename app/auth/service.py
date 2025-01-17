from datetime import timedelta, datetime
from typing import Optional, Set, Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, HTTPAuthorizationCredentials, HTTPBearer, HTTPBasic
from jose import jwt, JWTError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM
from db import database
from auth.models import User
from auth.utils import verify_password

oauth2_scheme = HTTPBearer()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def authenticate_user(db: AsyncSession, username: str, password: str):
    user = await db.get(User, username)
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user


async def get_current_user_from_db(db: AsyncSession, username: str):
    result = await db.execute(
        select(User).where(User.username == username)
    )
    user = result.scalars().first()
    return user


async def get_current_user_from_jwt(
        credentials: HTTPAuthorizationCredentials,
        db: AsyncSession,
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    result = await get_current_user_from_db(db, username)

    return result


revoked_tokens: Set[str] = set()


def add_token_to_blacklist(token: str):
    """Добавить токен в черный список."""
    revoked_tokens.add(token)


def is_token_revoked(token: str) -> bool:
    """Проверить, есть ли токен в черном списке."""
    return token in revoked_tokens
