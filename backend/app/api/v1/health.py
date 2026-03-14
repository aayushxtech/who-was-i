from fastapi import APIRouter
from sqlalchemy import text
from app.state.redis_client import redis_client
from app.db.session import engine

router = APIRouter()


@router.get("/health")
def health_check():
    return {"status": "ok"}


@router.get("/health/redis")
def redis_test():
    redis_client.set("test_key", "redis_working")
    value = redis_client.get("test_key")
    return {"redis_value": value}


@router.get("/health/db")
def db_test():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        value = result.scalar()
    return {"db": value}
