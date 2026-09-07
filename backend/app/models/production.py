from datetime import date, datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    Date,
    DateTime,
    ForeignKey,
    Integer,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


if TYPE_CHECKING:
    from app.models.line import Line


class Production(Base):
    __tablename__ = "productions"

    __table_args__ = (
        UniqueConstraint(
            "line_id",
            "production_date",
            name="uq_production_line_date",
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    line_id: Mapped[int] = mapped_column(
        ForeignKey("lines.id"),
        nullable=False,
    )

    production_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    target: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
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

    line: Mapped["Line"] = relationship(
        "Line",
        back_populates="production_records",
    )