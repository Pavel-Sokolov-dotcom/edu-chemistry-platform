# tests/mocks/deps.py
"""Тестовая версия зависимостей."""

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession


# Эта функция будет переопределена в тестах
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Заглушка для тестов."""
    raise NotImplementedError("This should be overridden in tests")
