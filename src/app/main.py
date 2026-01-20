from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from src.app.api.v1 import test_db
from src.app.api.v1 import users


app = FastAPI(
    title="EGE Chemistry Platform",
    description="Платформа для подготовки к ЕГЭ по химии",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ! В продакшене заменить на домен
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(test_db.router, prefix="/api/v1", tags=["test"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])


@app.get("/")
async def root():
    return {
        "message": "Добро пожаловать в EGE Chemistry Platform API",
        "docs": "/docs",
        "redoc": "/redoc",
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.get("/test-db-url")
async def test_db_url():
    return {
        # "database_url": os.getenv("DATABASE_URL"),
        "postgres_user": os.getenv("POSTGRES_USER"),
        "postgres_db": os.getenv("POSTGRES_DB"),
        "postgres_host": os.getenv("POSTGRES_HOST", "localhost"),
        "postgres_port": os.getenv("POSTGRES_PORT", "5432"),
    }
