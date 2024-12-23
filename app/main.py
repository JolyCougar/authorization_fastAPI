from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.db import create_user, get_user
from app.auth import authenticate_user, create_access_token
from app.routes.protected import router as protected_router
from app.config import TOKEN_EXPIRE_DELTA
import uvicorn

app = FastAPI()


@app.post("/register")
async def register(username: str, password: str):
    existing_user = get_user(username)
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="User already exists"
        )
    user = create_user(username, password)
    if not user:
        raise HTTPException(
            status_code=500,
            detail="Could not create user"
        )
    return {"message": "User created successfully"}


@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user["username"]}, expires_delta=TOKEN_EXPIRE_DELTA)
    return {"access_token": access_token, "token_type": "bearer"}


# Подключение маршрутов
app.include_router(protected_router, prefix="/api", tags=["protected"])

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
