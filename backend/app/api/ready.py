from fastapi import APIRouter, status
from fastapi.responses import JSONResponse


from app.core.db import check_database_connection
from app.state.connections import connections

router = APIRouter(prefix="/ready", tags=["ready"])


@router.get("/")
async def ready():
    """
    Readiness probe.
    Answers: can the app actually serve traffic?
    """
    checks = {
        "database": False,
        "websocket": False,
    }

    # ---- DB check ----
    try:
        await check_database_connection()
        checks["database"] = True
    except Exception:
        pass

    # ---- WebSocket runtime check ----
    # If the registry exists and is usable, WS stack is alive
    try:
        _ = connections.connections
        checks["websocket"] = True
    except Exception:
        pass

    all_ok = all(checks.values())

    return JSONResponse(
        status_code=status.HTTP_200_OK if all_ok else status.HTTP_503_SERVICE_UNAVAILABLE,
        content={
            "status": "ready" if all_ok else "not_ready",
            "checks": checks,
        },
    )
