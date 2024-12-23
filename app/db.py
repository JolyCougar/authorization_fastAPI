from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# база данных
fake_users_db = {
    "admin": {
        "username": "admin",
        "hashed_password": pwd_context.hash("admin"),
    }
}


def get_user(username: str):
    """Получить пользователя из БД."""
    return fake_users_db.get(username)


def verify_password(plain_password, hashed_password):
    """Проверить, совпадает ли пароль с хешем."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    """Хешировать пароль."""
    return pwd_context.hash(password)
