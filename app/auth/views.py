from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from auth.models import User
from auth.schemas import UserResponse, UserCreate
from auth.service import authenticate_user, create_access_token, get_current_user
from auth.utils import get_password_hash
from db import database

router = APIRouter()



@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate, db: AsyncSession = Depends(database.session_getter)):
    hashed_password = get_password_hash(user.password)
    new_user = User(username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    await db.commit()
    return new_user


@router.post("/login")
async def login(username: str, password: str, db: AsyncSession = Depends(database.session_getter)):

    user = authenticate_user(db, username, password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    access_token = create_access_token(data={"sub": username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/protected")
async def protected_route(current_user: User = Depends(get_current_user)):
    return {"message": f"Hello, {current_user.username}!"}
