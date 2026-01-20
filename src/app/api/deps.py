from typing import AsyncGenerator
from src.app.db.session import AsyncSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession


async def get_db() -> (
    AsyncGenerator[AsyncSession, None]
):  # AsyncGenerator[Что_возвращаем, Что_принимаем]
    async with AsyncSessionLocal() as session:
        yield session
