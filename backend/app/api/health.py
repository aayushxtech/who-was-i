from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["health"])

@router.get("/")
def health_check():
    """
    Health probe.
    Answers: is the app running at all?
    """
    return {"status": "ok"}