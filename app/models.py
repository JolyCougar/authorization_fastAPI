from pydantic import BaseModel

class UserCreate(BaseModel):
    """Модель для регистрации нового пользователя."""
    username: str
    password: str

class UserResponse(BaseModel):
    """Модель для ответа при запросе пользователя."""
    id: int
    username: str

    class Config:
        orm_mode = True  # Для работы с ORM-моделями