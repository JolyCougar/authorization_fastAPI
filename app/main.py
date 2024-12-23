from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.auth import authenticate_user, create_access_token
from app.routes.protected import router as protected_router
from app.config import TOKEN_EXPIRE_DELTA
import uvicorn

app = FastAPI()


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
