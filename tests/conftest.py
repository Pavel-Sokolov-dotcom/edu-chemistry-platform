import os
import pytest
import sys
from pathlib import Path
from typing import Generator

from fastapi.testclient import TestClient
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Устанавливаем URL тестовой БД (синхронный)
TEST_DATABASE_URL = (
    "postgresql://postgres:postgres@localhost:5433/chemistry_platform_test"
)
os.environ["DATABASE_URL"] = TEST_DATABASE_URL

# Добавляем путь к src
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# Импортируем модели
from src.app.models.base import Base
from src.app.models.user import User


@pytest.fixture(scope="function")
def client() -> Generator:
    """
    Тестовый клиент с изолированной БД.
    """
    # Создаём синхронный engine
    engine = create_engine(
        TEST_DATABASE_URL,
        echo=False,
        pool_size=1,
        max_overflow=0,
    )

    # Создаём таблицы
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    # Создаём сессию
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )

    session = TestingSessionLocal()

    # Создаём тестовое приложение
    app = FastAPI(title="Test API")

    # Функция для получения сессии
    def get_db_override():
        yield session

    # Переопределяем зависимость
    from src.app.api import deps

    app.dependency_overrides[deps.get_db] = get_db_override

    # Импортируем роутеры
    from src.app.api.v1 import auth, users

    # Подключаем роутеры
    app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
    app.include_router(users.router, prefix="/api/v1/users", tags=["users"])

    # Используем TestClient из FastAPI
    with TestClient(app) as client:
        yield client

    # Очистка
    app.dependency_overrides.clear()
    session.close()
    engine.dispose()
