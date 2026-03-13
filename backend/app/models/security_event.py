from datetime import datetime

from sqlalchemy import String, DateTime, BigInteger, Index, func
from sqlalchemy.dialects.postgresql import JSONB, INET
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class SecurityEvent(Base):
    __tablename__ = "security_events"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    ip_address: Mapped[str | None] = mapped_column(
        INET
    )

    event_type: Mapped[str] = mapped_column(
        String(64),
        nullable=False
    )

    severity: Mapped[str] = mapped_column(
        String(32),
        nullable=False
    )

    event_metadata: Mapped[dict | None] = mapped_column(
        JSONB
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )


Index("ix_security_events_created_at", SecurityEvent.created_at)
Index("ix_security_events_severity", SecurityEvent.severity)
