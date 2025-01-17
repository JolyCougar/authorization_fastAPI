from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn
from app.db import database
from auth.models import Base
from auth import auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with database.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield



app = FastAPI(lifespan=lifespan)
app.include_router(auth_router, prefix="/auth", tags=["auth"])



if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)