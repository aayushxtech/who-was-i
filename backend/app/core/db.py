from typing import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import get_settings

# -------------------------------------------------------------------
# Engine & sessionmaker (lazy singletons)
# -------------------------------------------------------------------

_engine: AsyncEngine | None = None
_sessionmaker: async_sessionmaker[AsyncSession] | None = None


def get_engine() -> AsyncEngine:
    """
    Create and return the async SQLAlchemy engine.
    Created lazily and reused for the lifetime of the process.
    """
    global _engine

    if _engine is None:
        settings = get_settings()

        _engine = create_async_engine(
            settings.database.url,
            echo=settings.database.echo,
            pool_size=settings.database.pool_size,
            pool_pre_ping=True,
        )

    return _engine


def get_sessionmaker() -> async_sessionmaker[AsyncSession]:
    """
    Create and return an async sessionmaker.
    """
    global _sessionmaker

    if _sessionmaker is None:
        engine = get_engine()

        _sessionmaker = async_sessionmaker(
            bind=engine,
            expire_on_commit=False,
        )

    return _sessionmaker


# -------------------------------------------------------------------
# FastAPI dependency (unused in Phase 1, wired early)
# -------------------------------------------------------------------

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Yield a database session.
    Intended for use as a FastAPI dependency.
    """
    sessionmaker = get_sessionmaker()

    async with sessionmaker() as session:
        yield session


# -------------------------------------------------------------------
# Connectivity check (used in lifespan / readiness)
# -------------------------------------------------------------------

async def check_database_connection() -> None:
    """
    Verify that the database is reachable.
    Fails fast if configuration or connectivity is broken.
    """
    engine = get_engine()

    async with engine.connect() as conn:
        await conn.execute(text("SELECT 1"))
    