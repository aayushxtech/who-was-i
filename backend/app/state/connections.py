from typing import Set
from fastapi import WebSocket


class ConnectionRegistry:
    """
    In-memory registry for active WebSocket connections.

    Phase 1 responsibilities:
    - track connect / disconnect
    - expose current connections
    - nothing else

    This state is intentionally ephemeral.
    """

    def __init__(self) -> None:
        self._connections: Set[WebSocket] = set()

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self._connections.add(websocket)

    def disconnect(self, websocket: WebSocket) -> None:
        self._connections.discard(websocket)

    @property
    def connections(self) -> Set[WebSocket]:
        """
        Read-only view of active connections.
        """
        return self._connections


# Singleton registry for the process
connections = ConnectionRegistry()
