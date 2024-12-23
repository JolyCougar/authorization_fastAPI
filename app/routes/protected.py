from fastapi import APIRouter, Depends
from app.auth import get_current_user

router = APIRouter()


@router.get("/protected")
async def protected_route(current_user: dict = Depends(get_current_user)):
    """Маршрут для авторизованных пользователей."""
    return {"message": f"Hello, {current_user['username']}"}
