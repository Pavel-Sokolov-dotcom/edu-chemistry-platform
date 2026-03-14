import pytest
import asyncpg

@pytest.mark.asyncio
async def test_db_connection():
    """Проверка подключения к БД."""
    conn = await asyncpg.connect(
        user='postgres',
        password='postgres',
        database='chemistry_platform_test',
        host='localhost',
        port=5433
    )
    result = await conn.fetchval('SELECT 1')
    await conn.close()
    assert result == 1