from fastapi import FastAPI
import os
from src.app.api.v1 import test_db


app = FastAPI(title="EGE Chemistry Platform")

app.include_router(test_db.router, prefix="/api/v1", tags=["test"])


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.get("/test-db-url")
async def test_db_url():
    return {
        # "database_url": os.getenv("DATABASE_URL"),
        "postgres_user": os.getenv("POSTGRES_USER"),
        "postgres_db": os.getenv("POSTGRES_DB")
    }


