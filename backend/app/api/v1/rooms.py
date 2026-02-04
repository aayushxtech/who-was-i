from app.services.rooms import create_room
from app.models.room import CreateRoomResponseSchema, CreateRoomSchema
from fastapi import APIRouter, Depends
from app.core.db import get_db_session

router = APIRouter(prefix="/rooms", tags=["rooms"])


@router.post("/create", response_model=CreateRoomResponseSchema)
async def create_room_endpoint(
    room_data: CreateRoomSchema,
    db=Depends(get_db_session),
):
    """
    Endpoint to create a new room.

    This endpoint expects:
    - name: Name of the room
    - password: Password for the room

    It returns:
    - room_code: Unique code for the created room
    """

    room = await create_room(
        db=db,
        name=room_data.name,
        password=room_data.password,
        expires_at=room_data.expires_at,
    )

    return CreateRoomResponseSchema(room_code=room.room_code)
