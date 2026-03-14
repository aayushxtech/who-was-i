from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from redis import Redis

from app.db.session import get_db
from app.state.redis_client import get_redis
from app.services.room.room_service import (
    create_room,
    RoomNotFoundError,
    RoomInactiveError,
    InvalidRoomPasswordError,
    RoomJoinError,
)

from app.services.room.join_service import join_room
from app.api.v1.schema.room import (
    CreateRoomRequest,
    CreateRoomResponse,
    JoinRoomRequest,
    JoinRoomResponse,
)

router = APIRouter(prefix="/rooms", tags=["rooms"])


@router.post("", response_model=CreateRoomResponse)
def create_room_endpoint(
    payload: CreateRoomRequest,
    db: Session = Depends(get_db),
):
    room_code, room_id = create_room(db, payload.password)

    return CreateRoomResponse(
        room_id=room_id,
        room_code=room_code,
    )


@router.post("/join", response_model=JoinRoomResponse)
def join_room_endpoint(
    payload: JoinRoomRequest,
    db: Session = Depends(get_db),
    redis: Redis = Depends(get_redis),
):
    try:
        return join_room(
            db=db,
            redis=redis,
            room_code=payload.room_code,
            password=payload.password,
            display_name=payload.display_name,
        )
    except RoomNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except (RoomInactiveError, InvalidRoomPasswordError) as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except RoomJoinError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
