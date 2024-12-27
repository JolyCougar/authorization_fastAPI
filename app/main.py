from fastapi import FastAPI
import uvicorn
from routes.auth_routes import router as auth_router
from routes.user_routes import router as user_router

app = FastAPI()

# Подключаем маршруты
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(user_router, prefix="/users", tags=["users"])


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)