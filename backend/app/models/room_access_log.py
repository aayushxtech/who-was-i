import uuid
from datetime import datetime

from sqlalchemy import (
    String,
    Boolean,
    DateTime,
    Text,
    ForeignKey,
    BigInteger,
    Index,
    func,
)
from sqlalchemy.dialects.postgresql import UUID, INET
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class RoomAccessLog(Base):
    __tablename__ = "room_access_logs"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    room_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("rooms.id"), nullable=False
    )

    session_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True))

    ip_address: Mapped[str] = mapped_column(INET, nullable=False)

    user_agent: Mapped[str | None] = mapped_column(Text)

    event_type: Mapped[str] = mapped_column(String(64), nullable=False)

    success: Mapped[bool] = mapped_column(Boolean, nullable=False)

    failure_reason: Mapped[str | None] = mapped_column(Text)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


Index("ix_room_access_logs_room_id", RoomAccessLog.room_id)
Index("ix_room_access_logs_created_at", RoomAccessLog.created_at)
