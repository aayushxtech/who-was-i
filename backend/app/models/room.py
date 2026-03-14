import uuid
from datetime import datetime

from sqlalchemy import String, Boolean, Integer, DateTime, Text, Index, func
from sqlalchemy.dialects.postgresql import UUID, INET
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Room(Base):
    __tablename__ = "rooms"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    room_code: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)

    password_hash: Mapped[str] = mapped_column(Text, nullable=False)

    title: Mapped[str | None] = mapped_column(String(255))

    created_by_ip: Mapped[str | None] = mapped_column(INET)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    last_activity_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    max_participants: Mapped[int | None] = mapped_column(Integer)


Index("ix_rooms_room_code", Room.room_code)
Index("ix_rooms_last_activity_at", Room.last_activity_at)
Index("ix_rooms_is_active", Room.is_active)
