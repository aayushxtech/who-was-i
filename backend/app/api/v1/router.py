from fastapi import APIRouter
from . import websocket, health

api_router = APIRouter()

api_router.include_router(websocket.router, prefix="/ws", tags=["websocket"])
api_router.include_router(health.router, tags=["health"])
