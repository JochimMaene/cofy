from __future__ import annotations

from datetime import datetime
from enum import Enum

from advanced_alchemy.base import BigIntBase
from advanced_alchemy.types import DateTimeUTC
from sqlalchemy.orm import Mapped, mapped_column


class StatusType(str, Enum):
    updated = "updated"
    out_of_date = "out_of_date"


class DataStatus(BigIntBase):
    __tablename__ = "data_status"
    name: Mapped[str]

    last_update: Mapped[datetime] = mapped_column(
        DateTimeUTC(timezone=True),
    )
    next_update: Mapped[DateTimeUTC] = mapped_column(
        DateTimeUTC(timezone=True),
        nullable=True,
    )
    status: Mapped[StatusType]
    URL: Mapped[str]
    cron: Mapped[str | None] = mapped_column(nullable=True)
