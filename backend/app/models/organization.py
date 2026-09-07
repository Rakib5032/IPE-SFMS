from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


if TYPE_CHECKING:
    from app.models.user import User
    from app.models.line import Line


class OrganizationUnit(Base):
    __tablename__ = "organization_units"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    code: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )

    unit_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("organization_units.id"),
        nullable=True,
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

    # Parent organization unit
    parent: Mapped["OrganizationUnit | None"] = relationship(
        "OrganizationUnit",
        remote_side=[id],
        back_populates="children",
    )

    # Child organization units
    children: Mapped[list["OrganizationUnit"]] = relationship(
        "OrganizationUnit",
        back_populates="parent",
    )

    # Users assigned to this organization unit
    users: Mapped[list["User"]] = relationship(
        "User",
        back_populates="organization_unit",
    )

    # Lines belonging to this organization unit
    lines: Mapped[list["Line"]] = relationship(
        "Line",
        back_populates="organization_unit",
    )