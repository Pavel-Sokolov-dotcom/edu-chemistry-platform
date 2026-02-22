from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.app.schemas.token import Token
from src.app.api.deps import get_db
from src.app.core.security import verify_password
from src.app.models.user import User
from src.app.core.jwt import create_access_token


router = APIRouter()


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    """
    Аутентификация пользователя и выдача JWT токена.
    
    Использует стандартную форму OAuth2:
        username email пользователя
        password пароль
    """
    stmt = select(User).where(User.email == form_data.username)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный email или пароль", headers={"WWW-Authenticate": "Bearer"},)
    
    # Проверяю проль
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Создаю токен
    access_token = create_access_token(
        data={"sub": user.email} # sub = subject (идентификатор пользователя)
    )
    # Возвращаю токен
    return Token(access_token=access_token)