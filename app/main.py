from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models import UserCreate, UserResponse
from app.db import SessionLocal, init_db, User
from app.db import pwd_context
import uvicorn

# Инициализация базы данных
init_db()

app = FastAPI()

# Зависимость для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/register", response_model=UserResponse)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    """
    Регистрация нового пользователя.
    """
    # Проверяем, существует ли пользователь
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    # Создаем нового пользователя
    hashed_password = pwd_context.hash(user.password)
    new_user = User(username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
