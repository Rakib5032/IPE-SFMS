from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


if TYPE_CHECKING:
    from app.models.layout import Layout


class LayoutMachine(Base):
    __tablename__ = "layout_machines"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    layout_id: Mapped[int] = mapped_column(
        ForeignKey("layouts.id"),
        nullable=False,
    )

    machine_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    machine_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="PENDING",
    )

    reason: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    started_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    layout: Mapped["Layout"] = relationship(
        "Layout",
        back_populates="machines",
    )