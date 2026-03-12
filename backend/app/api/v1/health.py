from fastapi import APIRouter
from sqlalchemy import text
from app.state.redis_client import redis_client
from app.db.session import engine

router = APIRouter()


@router.get("/health")
async def health_check():
    return {"status": "ok"}


@router.get("/health/redis")
async def redis_test():
    await redis_client.set("test_key", "redis_working")
    value = await redis_client.get("test_key")

    return {"redis_value": value}


@router.get("/health/db")
async def db_test():
    async with engine.connect() as conn:
        result = await conn.execute(text("SELECT 1"))
        value = result.scalar()

    return {"db": value}
