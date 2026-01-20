from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime


class Base(DeclarativeBase):
    """Базовый класс для всех моделей SQLAlchemy."""
    pass    


class TimestampMixin:
    """Миксин для добавления created_at и updated_at полей."""
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )  # Mapped работает с типами Python, mapped_column с типами SQL


