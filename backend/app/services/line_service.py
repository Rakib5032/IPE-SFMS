from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.line import Line
from app.models.organization import OrganizationUnit


def get_line(
    db: Session,
    line_id: int,
) -> Line | None:
    return db.scalar(
        select(Line).where(
            Line.id == line_id
        )
    )


def get_all_lines(
    db: Session,
) -> list[Line]:
    return list(
        db.scalars(
            select(Line).order_by(
                Line.line_number
            )
        ).all()
    )


def get_lines_by_unit(
    db: Session,
    unit_id: int,
) -> list[Line]:
    return list(
        db.scalars(
            select(Line)
            .where(
                Line.organization_unit_id == unit_id
            )
            .order_by(Line.line_number)
        ).all()
    )


def get_lines_by_group(
    db: Session,
    group_id: int,
) -> list[Line]:
    """
    Get all lines belonging to units
    under the specified group.
    """

    units = db.scalars(
        select(OrganizationUnit).where(
            OrganizationUnit.parent_id == group_id
        )
    ).all()

    unit_ids = [unit.id for unit in units]

    if not unit_ids:
        return []

    return list(
        db.scalars(
            select(Line)
            .where(
                Line.organization_unit_id.in_(unit_ids)
            )
            .order_by(Line.line_number)
        ).all()
    )


def create_line(
    db: Session,
    line_number: int,
    name: str,
    organization_unit_id: int,
    is_active: bool = True,
) -> Line:
    line = Line(
        line_number=line_number,
        name=name,
        organization_unit_id=organization_unit_id,
        is_active=is_active,
    )

    db.add(line)
    db.commit()
    db.refresh(line)

    return line


def update_line(
    db: Session,
    line: Line,
    update_data: dict,
) -> Line:
    for field, value in update_data.items():
        setattr(
            line,
            field,
            value,
        )

    db.commit()
    db.refresh(line)

    return line