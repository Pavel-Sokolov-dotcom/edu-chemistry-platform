import pytest
import asyncio
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import NullPool
import sys
from pathlib import Path
from app.main import app
from app.core.config import settings
from app.models.base import Base
from app.db.session import get_db, AsyncSessionLocal


sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# URL тестовой БД
TEST_DATABASE_URL = (
    "postgresql+asyncpg://postgres:postgres@localhost:5433/chemistry_platform_test"
)


@pytest.fixture(scope="session")
def event_loop():
    """Создаёт event loop для асинхронных тестов"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def db_engine():
    """Создаёт движок БД для тестов"""
    engine = create_async_engine(
        TEST_DATABASE_URL,
        poolclass=NullPool,
        echo=False,
    )

    # Создаю все таблицы перед тестом
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    # Удаляю таблицы после теста (чистая БД для последующих тестов)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest.fixture(scope="function")
async def db_session(db_engine) -> AsyncGenerator[AsyncSession, None]:
    """Создаёт сессию БД для каждого теста"""
    async_session = async_sessionmaker(
        db_engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        yield session


@pytest.fixture(scope="function")
async def client(db_session) -> AsyncGenerator[AsyncClient, None]:
    """
    Тестовый HTTP-клиент с переопределённой зависимостью БД.
    """

    # Переопределяю зависимость get_db
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac

    # Снимаю переопределение после теста
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
async def auth_token(client: AsyncClient) -> str:
    """Получает JWT токен через API"""
    # Регистрация пользователя
    await client.post(
        "/api/v1/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword",
        },
    )

    # Логинюсь с ранее переданными данными
    response = await client.post(
        "/api/v1/auth/login", json={"username": "testuser", "password": "testpassword"}
    )

    if response.status_code == 200:
        return response.json()["access_token"]
    return ""


@pytest.fixture(scope="function")
def auth_headers(auth_token: str) -> dict:
    """Заголовки с авторизацией"""
    return {"Authorization": f"Bearer {auth_token}"}
