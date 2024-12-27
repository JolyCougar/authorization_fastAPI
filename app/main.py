from fastapi import FastAPI
from routes.auth_routes import router as auth_router
from routes.user_routes import router as user_router

app = FastAPI()

# Подключаем маршруты
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(user_router, prefix="/users", tags=["users"])
