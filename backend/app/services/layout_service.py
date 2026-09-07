from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.layout import Layout


def get_layout(
    db: Session,
    layout_id: int,
) -> Layout | None:
    return db.scalar(
        select(Layout).where(
            Layout.id == layout_id
        )
    )


def get_active_layout(
    db: Session,
    line_id: int,
) -> Layout | None:
    return db.scalar(
        select(Layout)
        .where(
            Layout.line_id == line_id,
            Layout.is_active.is_(True),
        )
        .order_by(
            Layout.started_at.desc()
        )
    )


def get_line_layouts(
    db: Session,
    line_id: int,
) -> list[Layout]:
    return list(
        db.scalars(
            select(Layout)
            .where(
                Layout.line_id == line_id
            )
            .order_by(
                Layout.started_at.desc()
            )
        ).all()
    )


def create_layout(
    db: Session,
    line_id: int,
    style: str | None,
    job: str | None,
    buyer: str,
    smv: float,
    required_machine_count: int | None,
    total_machines: int,
    machine_status: dict,
    status: str,
    notes: str | None,
) -> Layout:

    now = datetime.utcnow()

    current_layout = get_active_layout(
        db=db,
        line_id=line_id,
    )

    if current_layout:
        current_layout.is_active = False
        current_layout.completed_at = now
        current_layout.status = "COMPLETED"

        if current_layout.started_at:
            current_layout.duration_minutes = int(
                (
                    now - current_layout.started_at
                ).total_seconds()
                / 60
            )

        current_layout.updated_at = now

    layout = Layout(
        line_id=line_id,
        style=style,
        job=job,
        buyer=buyer,
        smv=smv,
        required_machine_count=required_machine_count,
        total_machines=total_machines,
        machine_status=machine_status,
        status=status,
        started_at=now,
        completed_at=None,
        duration_minutes=None,
        is_active=True,
        notes=notes,
        created_at=now,
        updated_at=now,
    )

    db.add(layout)

    db.commit()
    db.refresh(layout)

    return layout


def update_layout(
    db: Session,
    layout: Layout,
    style: str | None = None,
    job: str | None = None,
    buyer: str | None = None,
    smv: float | None = None,
    required_machine_count: int | None = None,
    total_machines: int | None = None,
    machine_status: dict | None = None,
    status: str | None = None,
    completed_at: datetime | None = None,
    duration_minutes: int | None = None,
    is_active: bool | None = None,
    notes: str | None = None,
) -> Layout:

    if style is not None:
        layout.style = style

    if job is not None:
        layout.job = job

    if buyer is not None:
        layout.buyer = buyer

    if smv is not None:
        layout.smv = smv

    if required_machine_count is not None:
        layout.required_machine_count = required_machine_count

    if total_machines is not None:
        layout.total_machines = total_machines

    if machine_status is not None:
        layout.machine_status = machine_status

    if status is not None:
        layout.status = status

    if completed_at is not None:
        layout.completed_at = completed_at

    if duration_minutes is not None:
        layout.duration_minutes = duration_minutes

    if is_active is not None:
        layout.is_active = is_active

    if notes is not None:
        layout.notes = notes

    layout.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(layout)

    return layout


def complete_layout(
    db: Session,
    layout: Layout,
) -> Layout:

    if not layout.is_active:
        return layout

    now = datetime.utcnow()

    layout.completed_at = now
    layout.is_active = False
    layout.status = "COMPLETED"

    if layout.started_at:
        layout.duration_minutes = int(
            (
                now - layout.started_at
            ).total_seconds()
            / 60
        )

    layout.updated_at = now

    db.commit()
    db.refresh(layout)

    return layout