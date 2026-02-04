from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class CreateRoomSchema(BaseModel):
    name: str = Field(..., description="Name of the room")
    password: str = Field(..., description="Password for the room")
    expires_at: Optional[datetime] = Field(
        None, description="Optional expiration time for the room (UTC)"
    )


class CreateRoomResponseSchema(BaseModel):
    room_code: str
