from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from uuid import UUID
import secrets


JOIN_TOKEN_TTL_MINUTES: int = 10


@dataclass
class JoinTokenRecord:
    room_id: UUID
    issued_at: datetime
    used: bool = False
    expires_at: datetime | None = None


_join_token_storage: dict[str, JoinTokenRecord] = {}


def generate_join_token(room_id: UUID) -> tuple[str, datetime]:
    """
    Generate a secure join token for a given room ID.

    The token is valid for a limited time (JOIN_TOKEN_TTL_MINUTES) and can only be used once.
    """

    token = secrets.token_urlsafe(32)
    now = datetime.now(timezone.utc)

    expires_at = None
    if JOIN_TOKEN_TTL_MINUTES is not None:
        expires_at = now + timedelta(minutes=JOIN_TOKEN_TTL_MINUTES)

        _join_token_storage[token] = JoinTokenRecord(
            room_id=room_id,
            issued_at=now,
            expires_at=expires_at,
        )

    return token, expires_at


def validate_join_token(token: str) -> UUID | None:
    """
    Validate a join token and return the associated room ID if valid.

    A token is valid if:
    - It exists in the storage
    - It has not expired
    - It has not been used before

    If the token is valid, it is marked as used to prevent reuse.
    """

    record = _join_token_storage.get(token)

    if record is None:
        return None

    now = datetime.now(timezone.utc)

    if record.used:
        return None

    if record.expires_at is not None:
        if record.expires_at < datetime.now(tz=timezone.utc):
            _join_token_storage.pop(token, None)
            return None

    record.used = True
    return record.room_id


def cleanup_expired_tokens() -> None:
    """
    Cleanup expired tokens from the storage.

    This function can be called periodically (e.g., via a background task) to remove expired tokens.
    """

    now = datetime.now(timezone.utc)
    tokens_to_cleanup = []

    for token, record in _join_token_storage.items():
        if record.used:
            tokens_to_cleanup.append(token)
        elif record.expires_at is not None and record.expires_at < now:
            tokens_to_cleanup.append(token)

    for token in tokens_to_cleanup:
        _join_token_storage.pop(token, None)
