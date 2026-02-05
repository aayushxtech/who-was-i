from uuid import UUID
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
    room_code: str = Field(..., min_length=4, max_length=16,
                           description="Unique code for the created room")


class JoinRoomSchema(BaseModel):
    room_code: str = Field(..., min_length=4, max_length=16,
                           description="Human-shareable room code")
    password: str = Field(..., min_length=1,
                          description="Plaintext room password (verified server-side)")


class RoomJoinTokenSchema(BaseModel):
    token: str = Field(..., description="Token to authorize joining the room")
    expires_at: datetime | None = Field(...,
                                        description="Expiration time of the token (UTC)")


class RoomInfoSchema(BaseModel):
    id: UUID = Field(..., description="Unique identifier of the room")
    room_code: str = Field(..., description="Unique code of the room")
    name: str = Field(..., description="Name of the room")
    expires_at: Optional[datetime] = Field(
        None, description="Expiration time of the room (UTC), if set"
    )


class RoomJoinResponseSchema(BaseModel):
    room: RoomInfoSchema = Field(...,
                                 description="Information about the joined room")
    join_token: RoomJoinTokenSchema = Field(
        ..., description="Token to authorize joining the room")
