import uuid
import time
from redis import Redis

from app.services.room.room_service import validate_room_join, update_room_activity

SESSION_PREFIX = "wwi:session:"
ROOM_MEMBERS_PREFIX = "wwi:room:"


def join_room(redis: Redis, db, room_code: str, password: str, display_name: str):
    room = validate_room_join(db, room_code, password)

    session_id = str(uuid.uuid4())
    session_key = f"{SESSION_PREFIX}{session_id}"
    members_key = f"{ROOM_MEMBERS_PREFIX}{room.id}:members"

    joined_at = int(time.time())

    redis.hset(
        session_key,
        mapping={
            "room_id": str(room.id),
            "display_name": display_name,
            "joined_at": joined_at,
        },
    )

    redis.sadd(members_key, session_id)

    update_room_activity(db, room)

    return {
        "session_id": session_id,
        "room_id": str(room.id),
        "display_name": display_name,
    }
