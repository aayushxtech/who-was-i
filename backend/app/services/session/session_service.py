from typing import cast
from redis.client import Redis

SESSION_PREFIX = "wwi:session:"
ROOM_MEMBERS_PREFIX = "wwi:room:"


def leave_room(redis: Redis, session_id: str) -> None:
    session_key = f"{SESSION_PREFIX}{session_id}"

    session = cast(dict[str, str], redis.hgetall(session_key))
    if not session:
        return

    room_id = session.get("room_id")
    if not room_id:
        redis.delete(session_key)
        return

    members_key = f"{ROOM_MEMBERS_PREFIX}{room_id}:members"
    redis.srem(members_key, session_id)
    redis.delete(session_key)
