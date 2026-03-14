from pydantic import BaseModel


class CreateRoomRequest(BaseModel):
    password: str


class CreateRoomResponse(BaseModel):
    room_id: str
    room_code: str


class JoinRoomRequest(BaseModel):
    room_code: str
    password: str
    display_name: str


class JoinRoomResponse(BaseModel):
    session_id: str
    room_id: str
    display_name: str
