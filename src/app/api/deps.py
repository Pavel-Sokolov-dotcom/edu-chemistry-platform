# src/app/api/deps.py
from typing import AsyncGenerator, Generator
from src.app.db.session import get_db as get_db_session

# Для обратной совместимости
try:
    from src.app.db.session import AsyncSessionLocal
except ImportError:
    AsyncSessionLocal = None

# Экспортируем get_db под тем же именем
get_db = get_db_session
