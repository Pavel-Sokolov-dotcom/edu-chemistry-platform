from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from src.app.api.deps import get_db


router = APIRouter()


@router.get("/test-db")
async def test_db(db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("SELECT version()"))
    version = result.scalar()  # Получаю значение

    return {"status": "success", "database": "PostgreSQL", "version": version}


@router.get("/test")
async def test():
    return {"message": "test"}


# 1. Запрос приходит на /api/v1/test-db
# 2. FastAPI вызывает test_db()
# 3. FastAPI выполняет Depends(get_db) → получает сессию БД
# 4. Выполняется код внутри test_db
# 5. Возвращается JSON ответ
