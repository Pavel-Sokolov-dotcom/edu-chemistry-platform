import os
import pytest
import asyncio
import sys
from pathlib import Path
from typing import Generator

from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import NullPool

# Устанавливаем URL тестовой БД
TEST_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5433/chemistry_platform_test"
os.environ["DATABASE_URL"] = TEST_DATABASE_URL

# Добавляем путь к src
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src.app.main import app
from src.app.models.base import Base
from src.app.db.session import get_db


@pytest.fixture(scope="function")
def client() -> Generator:
    """
    Тестовый клиент с изолированной БД для каждого теста.
    Использует синхронную фикстуру, которая управляет асинхронным кодом.
    """
    # Создаём новый цикл событий для этого теста
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    # Асинхронная функция для настройки
    async def setup():
        # Создаём engine
        engine = create_async_engine(
            TEST_DATABASE_URL,
            echo=False,
            poolclass=NullPool,
        )
        
        # Создаём таблицы
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
        
        # Создаём сессию
        async_session = async_sessionmaker(
            engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )
        
        # Создаём сессию
        session = async_session()
        
        # Переопределяем зависимость
        async def override_get_db():
            yield session
        app.dependency_overrides[get_db] = override_get_db
        
        # Создаём клиент
        client = AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
        )
        await client.__aenter__()
        
        return client, engine, session
    
    # Запускаем настройку
    client, engine, session = loop.run_until_complete(setup())
    
    # Возвращаем клиент для теста
    yield client
    
    # Очистка после теста
    async def teardown():
        await client.__aexit__(None, None, None)
        app.dependency_overrides.clear()
        await session.close()
        await engine.dispose()
    
    loop.run_until_complete(teardown())
    loop.close()
    