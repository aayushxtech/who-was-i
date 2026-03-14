from fastapi import APIRouter
from . import websocket, health, room

api_router = APIRouter()

api_router.include_router(websocket.router, prefix="/ws", tags=["websocket"])
api_router.include_router(health.router, tags=["health"])
api_router.include_router(room.router, tags=["rooms"])
