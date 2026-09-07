from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.layout_machine import LayoutMachine


ALLOWED_STATUSES = {
    "PENDING",
    "RUNNING",
    "COMPLETED",
    "OFF",
}


def get_machine(
    db: Session,
    machine_id: int,
) -> LayoutMachine | None:
    return db.scalar(
        select(LayoutMachine).where(
            LayoutMachine.id == machine_id
        )
    )


def get_layout_machines(
    db: Session,
    layout_id: int,
) -> list[LayoutMachine]:
    return list(
        db.scalars(
            select(LayoutMachine)
            .where(
                LayoutMachine.layout_id == layout_id
            )
            .order_by(
                LayoutMachine.machine_number
            )
        ).all()
    )


def create_machine(
    db: Session,
    layout_id: int,
    machine_number: int,
    machine_name: str | None,
    status: str,
    reason: str | None,
) -> LayoutMachine:

    machine = LayoutMachine(
        layout_id=layout_id,
        machine_number=machine_number,
        machine_name=machine_name,
        status=status,
        reason=reason,
        started_at=None,
        completed_at=None,
        is_active=True,
    )

    db.add(machine)
    db.commit()
    db.refresh(machine)

    return machine


def update_machine_status(
    db: Session,
    machine: LayoutMachine,
    new_status: str,
    reason: str | None = None,
) -> LayoutMachine:

    now = datetime.utcnow()

    if new_status == "RUNNING":
        if machine.started_at is None:
            machine.started_at = now

        machine.completed_at = None
        machine.is_active = True

    elif new_status == "COMPLETED":
        if machine.started_at is None:
            machine.started_at = now

        machine.completed_at = now
        machine.is_active = False

    elif new_status == "OFF":
        machine.is_active = False

    elif new_status == "PENDING":
        machine.is_active = True
        machine.completed_at = None

    machine.status = new_status
    machine.reason = reason

    db.commit()
    db.refresh(machine)

    return machine


def update_machine(
    db: Session,
    machine: LayoutMachine,
    machine_name: str | None = None,
    status: str | None = None,
    reason: str | None = None,
    is_active: bool | None = None,
) -> LayoutMachine:

    if machine_name is not None:
        machine.machine_name = machine_name

    if status is not None:
        machine = update_machine_status(
            db=db,
            machine=machine,
            new_status=status,
            reason=reason,
        )
        return machine

    if reason is not None:
        machine.reason = reason

    if is_active is not None:
        machine.is_active = is_active

    db.commit()
    db.refresh(machine)

    return machine