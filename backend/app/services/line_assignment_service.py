from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.line_assignment import LineAssignment


def get_assignment(
    db: Session,
    assignment_id: int,
) -> LineAssignment | None:
    return db.scalar(
        select(LineAssignment).where(
            LineAssignment.id == assignment_id
        )
    )


def get_active_assignments(
    db: Session,
) -> list[LineAssignment]:
    return list(
        db.scalars(
            select(LineAssignment)
            .where(
                LineAssignment.is_active.is_(True)
            )
            .order_by(
                LineAssignment.start_date.desc()
            )
        ).all()
    )


def get_line_assignments(
    db: Session,
    line_id: int,
) -> list[LineAssignment]:
    return list(
        db.scalars(
            select(LineAssignment)
            .where(
                LineAssignment.line_id == line_id
            )
            .order_by(
                LineAssignment.start_date.desc()
            )
        ).all()
    )


def get_user_assignments(
    db: Session,
    employee_id: int,
) -> list[LineAssignment]:
    return list(
        db.scalars(
            select(LineAssignment)
            .where(
                LineAssignment.employee_id == employee_id
            )
            .order_by(
                LineAssignment.start_date.desc()
            )
        ).all()
    )


def get_active_user_line_assignment(
    db: Session,
    employee_id: int,
    line_id: int,
) -> LineAssignment | None:
    return db.scalar(
        select(LineAssignment).where(
            LineAssignment.employee_id == employee_id,
            LineAssignment.line_id == line_id,
            LineAssignment.is_active.is_(True),
        )
    )


def create_assignment(
    db: Session,
    employee_id: int,
    line_id: int,
    assignment_type: str = "PRIMARY",
) -> LineAssignment:

    now = datetime.utcnow()

    assignment = LineAssignment(
        employee_id=employee_id,
        line_id=line_id,
        assignment_type=assignment_type,
        start_date=now,
        end_date=None,
        is_active=True,
    )

    db.add(assignment)
    db.commit()
    db.refresh(assignment)

    return assignment


def end_assignment(
    db: Session,
    assignment: LineAssignment,
) -> LineAssignment:

    now = datetime.utcnow()

    assignment.end_date = now
    assignment.is_active = False

    db.commit()
    db.refresh(assignment)

    return assignment


def update_assignment(
    db: Session,
    assignment: LineAssignment,
    update_data: dict,
) -> LineAssignment:

    for field, value in update_data.items():
        setattr(
            assignment,
            field,
            value,
        )

    db.commit()
    db.refresh(assignment)

    return assignment