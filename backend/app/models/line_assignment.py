from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


if TYPE_CHECKING:
    from app.models.user import User
    from app.models.line import Line


class LineAssignment(Base):
    __tablename__ = "line_assignments"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    employee_id: Mapped[int] = mapped_column(
        ForeignKey("users.employee_id"),
        nullable=False,
    )

    line_id: Mapped[int] = mapped_column(
        ForeignKey("lines.id"),
        nullable=False,
    )

    assignment_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="PRIMARY",
    )

    start_date: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    end_date: Mapped[datetime | None] = mapped_column(
        DateTime,
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

    user: Mapped["User"] = relationship(
        "User",
        back_populates="line_assignments",
    )

    line: Mapped["Line"] = relationship(
        "Line",
        back_populates="assignments",
    )