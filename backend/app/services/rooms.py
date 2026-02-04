import secrets
import string
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.schema.room import Room
from app.core.security import hash_password


ROOM_CODE_LENGTH = 6
ROOM_CODE_ALPHABET = string.ascii_uppercase + string.digits


def _generate_room_code(length: int = ROOM_CODE_LENGTH) -> str:
    return "".join(secrets.choice(ROOM_CODE_ALPHABET) for _ in range(length))


async def create_room(
    *,
    db: AsyncSession,
    name: str,
    password: str,
    expires_at: Optional[datetime] = None,
) -> Room:
    """
    Create a new room and persist it.

    This function assumes:
    - input validation is already done
    - db session lifecycle is managed by the caller
    """

    room_code = _generate_room_code()
    password_hash = hash_password(password)

    room = Room(
        room_code=room_code,
        name=name,
        password_hash=password_hash,
        created_at=datetime.now(timezone.utc),
        expires_at=expires_at,
    )

    db.add(room)
    await db.commit()
    await db.refresh(room)

    return room
