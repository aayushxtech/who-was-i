from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from app.schema.room import Room
from app.services.join_token_service import generate_join_token

from app.core.security import verify_password


class RoomNotFoundError(Exception):
    pass


class RoomExpiredError(Exception):
    pass


class RoomPasswordError(Exception):
    pass


async def join_room(
    *,
    db: AsyncSession,
    room_code: str,
    password: str,
) -> tuple[Room, str, datetime | None]:
    """
    Join a room by its code and password.

    This function performs the following steps:
    1. Fetch the room by its code.
    2. Check if the room exists, is not expired, and the password is correct.
    3. Generate and return a join token for the room.

    Raises:
        RoomNotFoundError: If no room with the given code exists.
        RoomExpiredError: If the room has expired.
        RoomPasswordError: If the provided password is incorrect.
    """

    result = await db.execute(select(Room).where(Room.room_code == room_code))
    room: Room | None = result.scalar_one_or_none()

    if not room:
        raise RoomNotFoundError("Room not found")

    if room.expires_at and room.expires_at < datetime.now(timezone.utc):
        raise RoomExpiredError("Room has expired")

    if not verify_password(room.password_hash, password):
        raise RoomPasswordError("Incorrect password")

    token, expires_at = generate_join_token(room.id)

    return room, token, expires_at
