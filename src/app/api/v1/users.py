from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.schemas.user import UserResponse, UserCreate
from src.app.api.deps import get_db

router = APIRouter()


@router.post("/register", response_model=UserResponse)
async def register_user(
    user_data: UserCreate, 
    db: AsyncSession = Depends(get_db)
): 
    ...
