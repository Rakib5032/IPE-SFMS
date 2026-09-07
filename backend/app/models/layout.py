from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    JSON,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


if TYPE_CHECKING:
    from app.models.line import Line
    from app.models.layout_machine import LayoutMachine


class Layout(Base):
    __tablename__ = "layouts"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    line_id: Mapped[int] = mapped_column(
        ForeignKey("lines.id"),
        nullable=False,
    )

    # ========================================================
    # BASIC LAYOUT INFORMATION
    # ========================================================

    style: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    job: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    buyer: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    smv: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    # ========================================================
    # MACHINE INFORMATION
    # ========================================================

    # New field.
    # Existing database allows NULL.
    required_machine_count: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    # Existing field.
    total_machines: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    # Existing field.
    # Database stores this as JSON.
    machine_status: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
    )

    # ========================================================
    # LAYOUT STATUS
    # ========================================================

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="RUNNING",
    )

    # ========================================================
    # TIME INFORMATION
    # ========================================================

    started_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    # Existing field.
    duration_minutes: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    # ========================================================
    # GENERAL INFORMATION
    # ========================================================

    # New field.
    # Existing database allows NULL.
    is_active: Mapped[bool | None] = mapped_column(
        Boolean,
        nullable=True,
    )

    notes: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    # New field.
    # Existing database allows NULL.
    created_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    # New field.
    # Existing database allows NULL.
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    # ========================================================
    # RELATIONSHIPS
    # ========================================================

    line: Mapped["Line"] = relationship(
        "Line",
        back_populates="layouts",
    )

    machines: Mapped[list["LayoutMachine"]] = relationship(
        "LayoutMachine",
        back_populates="layout",
        cascade="all, delete-orphan",
        order_by="LayoutMachine.machine_number",
    )