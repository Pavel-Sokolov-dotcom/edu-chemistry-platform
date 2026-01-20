from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.schemas.user import UserResponse, UserCreate
from src.app.api.deps import get_db
from src.app.core.security import get_password_hash, verify_password
from sqlalchemy import select
from src.app.models.user import User


router = APIRouter()


@router.post("/register", response_model=UserResponse)
async def register_user(
    user_data: UserCreate, 
    db: AsyncSession = Depends(get_db)
):
    # 1. Проверяю нет ли пользователя с таким email
    smtm = select(User).where(User.email == user_data.email) 
    result = await db.execute(smtm)
    exiting_user = result.scalar_one_or_none()
    if exiting_user:
        raise HTTPException(
            status_code = 400,
            detail = "Пользователь с такой почтой уже существует"
        )
    # 2. Хеширую переданный пароль
    hashed_password = get_password_hash(user_data.password)
    
    # 3. Создаю пользователя
    db_user = User(
        email = user_data.email,
        hashed_password = hashed_password,
        is_active = True
    )
    
    # 4. Сохраняю пользователя в БД
    db.add(db_user) # Добавляю пользователя в БД
    await db.commit() # Комичу изменения
    await db.refresh(db_user) # Обновляю данные пользователя из шага 3
    
    
    return UserResponse.model_validate(db_user)
