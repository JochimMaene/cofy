from __future__ import annotations

from datetime import datetime
from enum import Enum

from advanced_alchemy.base import BigIntBase
from sqlalchemy.orm import Mapped, mapped_column


class StatusType(str, Enum):
    updated = "updated"
    out_of_date = "out_of_date"


class DataStatus(BigIntBase):
    __tablename__ = "data_status"
    name: Mapped[str]
    last_update: Mapped[datetime]
    next_update: Mapped[datetime] = mapped_column(nullable=True)
    status: Mapped[StatusType]
    URL: Mapped[str]
    cron: Mapped[str | None] = mapped_column(nullable=True)
