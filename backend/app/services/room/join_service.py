import uuid
import time

from app.services.room.room_service import validate_room_join, update_room_activity
from app.services.name_service import generate_display_name
from typing import cast
from redis.client import Redis

SESSION_PREFIX = "wwi:session:"
ROOM_MEMBERS_PREFIX = "wwi:room:"


def join_room(redis: Redis, db, room_code: str, password: str, display_name: str | None) -> dict:
    room = validate_room_join(db, room_code, password)

    members_key = f"{ROOM_MEMBERS_PREFIX}{room.id}:members"

    existing_sessions = cast(set[str], redis.smembers(members_key))

    existing_names = set()

    for sid in existing_sessions:
        sid_str = sid.decode() if isinstance(sid, bytes) else sid

        session_key = f"{SESSION_PREFIX}{sid_str}"

        name = redis.hget(session_key, "display_name")

        if name:
            name_str = name.decode() if isinstance(name, bytes) else name
            existing_names.add(name_str)
    max_attempts = 20
    if not display_name:
        display_name = generate_display_name()
    attempts = 0
    while display_name in existing_names and attempts < max_attempts:
        display_name = generate_display_name()
        attempts += 1

    if attempts == max_attempts and display_name in existing_names:
        raise ValueError(
            "Could not generate a unique display name. Please try again.")

    session_id = str(uuid.uuid4())
    session_key = f"{SESSION_PREFIX}{session_id}"

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
