from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn
from app.db import database
from app.models import Base
from views.auth_views import router as auth_router
from views.user_views import router as user_router

app = FastAPI()

# Подключаем маршруты


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with database.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield



app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(user_router, prefix="/users", tags=["users"])


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)