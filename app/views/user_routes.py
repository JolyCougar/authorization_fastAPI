from fastapi import APIRouter, Depends
from app.auth import get_current_user
from models import User

router = APIRouter()


@router.get("/protected")
async def protected_route(current_user: User = Depends(get_current_user)):
    return {"message": f"Hello, {current_user.username}!"}
