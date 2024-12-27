from datetime import datetime, timedelta
from typing import Set

# Простая память для хранения "отозванных" токенов
revoked_tokens: Set[str] = set()


def add_token_to_blacklist(token: str):
    """Добавить токен в черный список."""
    revoked_tokens.add(token)


def is_token_revoked(token: str) -> bool:
    """Проверить, есть ли токен в черном списке."""
    return token in revoked_tokens
