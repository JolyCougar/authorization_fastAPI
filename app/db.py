from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker, AsyncEngine,

)

DATABASE_URL = "sqlite+aiosqlite:///database.db"


class Database:
    def __init__(self):
        self.engine: AsyncEngine = create_async_engine(
            url=DATABASE_URL,
            echo=False,
        )
        self.session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False
        )


    async def session_getter(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_factory() as session:
            yield session
            await session.close()


database = Database()
