from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.config import settings

app = FastAPI(title="Who Was I", version="1.0.0")


@app.get("/")
async def root():
    return {"message": "Who Was I API running!"}


app.include_router(api_router, prefix=settings.API_V1_PREFIX)
