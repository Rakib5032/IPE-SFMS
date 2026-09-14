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
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


if TYPE_CHECKING:
    from app.models.line import Line
    from app.models.layout_machine import LayoutMachine


class Layout(Base):
    __tablename__ = "layouts"

    __table_args__ = (
        UniqueConstraint(
            "line_id",
            "layout_year",
            "layout_month",
            "layout_number",
            name="uq_layout_line_month_number",
        ),
    )

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
    # MONTHLY LAYOUT NUMBERING
    # ========================================================

    # Example:
    # Line 5 - September 2026:
    #   layout_number = 1
    #   layout_number = 2
    #   layout_number = 3
    #
    # Line 5 - October 2026:
    #   layout_number = 1

    layout_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    layout_year: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    layout_month: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    # ========================================================
    # MACHINE INFORMATION
    # ========================================================

    required_machine_count: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    total_machines: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

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

    duration_minutes: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    # ========================================================
    # GENERAL INFORMATION
    # ========================================================

    is_active: Mapped[bool | None] = mapped_column(
        Boolean,
        nullable=True,
    )

    notes: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    created_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

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