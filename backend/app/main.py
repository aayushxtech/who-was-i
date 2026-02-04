from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from app.core.config import get_settings
from app.core.db import check_database_connection
from app.api.health import router as health_router
from app.api.ready import router as ready_router
from app.api.v1.rooms import router as rooms_router

from app.state.connections import connections


# -------------------------------------------------------------------
# Lifespan (startup / shutdown)
# -------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load settings (forces config validation early)
    get_settings()

    # Infra-only startup check
    await check_database_connection()

    yield

    # No shutdown logic in Phase 1
    # (connections, rooms, workers come later)


# -------------------------------------------------------------------
# App factory
# -------------------------------------------------------------------
def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title=settings.app.name,
        debug=settings.app.debug,
        lifespan=lifespan,
    )

    # REST routers
    app.include_router(health_router)
    app.include_router(ready_router)

    # Versioned API router
    app.include_router(rooms_router, prefix="/api")
    return app


app = create_app()


# -------------------------------------------------------------------
# WebSocket (Phase 1: blind pipe)
# -------------------------------------------------------------------
@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()

    try:
        while True:
            data = await ws.receive_text()
            await ws.send_text(data)
    finally:
        connections.disconnect(ws)
