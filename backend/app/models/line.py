from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


if TYPE_CHECKING:
    from app.models.organization import OrganizationUnit
    from app.models.line_assignment import LineAssignment
    from app.models.line_status import LineStatus
    from app.models.layout import Layout
    from app.models.production import Production


class Line(Base):
    __tablename__ = "lines"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    line_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        unique=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    organization_unit_id: Mapped[int] = mapped_column(
        ForeignKey("organization_units.id"),
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    organization_unit: Mapped["OrganizationUnit"] = relationship(
        "OrganizationUnit",
        back_populates="lines",
    )

    assignments: Mapped[list["LineAssignment"]] = relationship(
        "LineAssignment",
        back_populates="line",
        cascade="all, delete-orphan",
    )

    status_history: Mapped[list["LineStatus"]] = relationship(
        "LineStatus",
        back_populates="line",
        cascade="all, delete-orphan",
    )

    layouts: Mapped[list["Layout"]] = relationship(
        "Layout",
        back_populates="line",
        cascade="all, delete-orphan",
        order_by="Layout.started_at.desc()",
    )

    production_records: Mapped[list["Production"]] = relationship(
        "Production",
        back_populates="line",
        cascade="all, delete-orphan",
    )