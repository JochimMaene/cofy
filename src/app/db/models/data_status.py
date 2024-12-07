from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from advanced_alchemy.base import BigIntBase
from sqlalchemy.orm import Mapped, mapped_column

if TYPE_CHECKING:
    from datetime import datetime


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
