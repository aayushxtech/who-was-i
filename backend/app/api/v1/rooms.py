from app.services.room_create_service import create_room
from app.models.room import CreateRoomResponseSchema, CreateRoomSchema
from fastapi import APIRouter, Depends, status, HTTPException, Query
from app.core.db import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.room import (
    RoomJoinResponseSchema,
    RoomInfoSchema,
    RoomJoinTokenSchema,
    JoinRoomSchema,
)
from app.services.room_join_service import join_room as join_room_service
from app.services.room_join_service import (
    RoomNotFoundError,
    RoomExpiredError,
    RoomPasswordError,
)

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


@router.post(
    "/join",
    response_model=RoomJoinResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def join_room(
    room_code: str = Query(..., min_length=4, max_length=16,
                           description="Human-shareable room code"),
    password: str = Query(..., min_length=1,
                          description="Plaintext room password (verified server-side)"),
    db: AsyncSession = Depends(get_db_session),
):
    try:
        room, token, token_expires_at = await join_room_service(
            db=db,
            room_code=room_code,
            password=password,
        )

    except RoomNotFoundError:
        # Intentionally indistinguishable from invalid code
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room does not exist.",
        )

    except RoomExpiredError:
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail="This room is no longer available.",
        )

    except RoomPasswordError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Incorrect password.",
        )

    return RoomJoinResponseSchema(
        room=RoomInfoSchema(
            id=room.id,
            room_code=room.room_code,
            name=room.name,
            expires_at=room.expires_at,
        ),
        join_token=RoomJoinTokenSchema(
            token=token,
            expires_at=token_expires_at,
        ),
    )
