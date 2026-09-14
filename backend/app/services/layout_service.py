from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.layout import Layout
from app.models.line import Line


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

    # ============================================================
    # LOCK THE LINE
    # ============================================================
    #
    # Lock the line row so that two users cannot create a layout
    # for the same line at the same time.
    #
    # Example:
    #
    # User A -> locks Line 5 -> gets Layout 4
    # User B -> waits        -> gets Layout 5
    #

    line = db.scalar(
        select(Line)
        .where(
            Line.id == line_id
        )
        .with_for_update()
    )

    if line is None:
        raise ValueError("Line not found")

    # ============================================================
    # MONTHLY LAYOUT NUMBER
    # ============================================================
    #
    # Numbering is independent for every:
    #
    #     line + year + month
    #
    # Example:
    #
    # Line 5 / September 2026:
    #     1, 2, 3
    #
    # Line 5 / October 2026:
    #     1
    #
    # Line 1 / September 2026:
    #     1
    #

    layout_year = now.year
    layout_month = now.month

    last_layout_number = db.scalar(
        select(
            func.max(Layout.layout_number)
        ).where(
            Layout.line_id == line_id,
            Layout.layout_year == layout_year,
            Layout.layout_month == layout_month,
        )
    )

    layout_number = (
        last_layout_number + 1
        if last_layout_number is not None
        else 1
    )

    # ============================================================
    # COMPLETE CURRENT ACTIVE LAYOUT
    # ============================================================

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

    # ============================================================
    # CREATE NEW LAYOUT
    # ============================================================

    layout = Layout(
        line_id=line_id,

        # --------------------------------------------------------
        # BASIC INFORMATION
        # --------------------------------------------------------

        style=style,
        job=job,
        buyer=buyer,
        smv=smv,

        # --------------------------------------------------------
        # MONTHLY LAYOUT NUMBERING
        # --------------------------------------------------------

        layout_number=layout_number,
        layout_year=layout_year,
        layout_month=layout_month,

        # --------------------------------------------------------
        # MACHINE INFORMATION
        # --------------------------------------------------------

        required_machine_count=required_machine_count,
        total_machines=total_machines,
        machine_status=machine_status,

        # --------------------------------------------------------
        # STATUS
        # --------------------------------------------------------

        status=status,

        # --------------------------------------------------------
        # TIME INFORMATION
        # --------------------------------------------------------

        started_at=now,
        completed_at=None,
        duration_minutes=None,

        # --------------------------------------------------------
        # CURRENT / ACTIVE LAYOUT
        # --------------------------------------------------------

        is_active=True,

        # --------------------------------------------------------
        # GENERAL INFORMATION
        # --------------------------------------------------------

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

    # ============================================================
    # BASIC INFORMATION
    # ============================================================

    if style is not None:
        layout.style = style

    if job is not None:
        layout.job = job

    if buyer is not None:
        layout.buyer = buyer

    if smv is not None:
        layout.smv = smv

    # ============================================================
    # MACHINE INFORMATION
    # ============================================================

    if required_machine_count is not None:
        layout.required_machine_count = required_machine_count

    if total_machines is not None:
        layout.total_machines = total_machines

    if machine_status is not None:
        layout.machine_status = machine_status

    # ============================================================
    # STATUS
    # ============================================================

    if status is not None:
        layout.status = status

    # ============================================================
    # TIME INFORMATION
    # ============================================================

    if completed_at is not None:
        layout.completed_at = completed_at

    if duration_minutes is not None:
        layout.duration_minutes = duration_minutes

    # ============================================================
    # ACTIVE STATUS
    # ============================================================

    if is_active is not None:
        layout.is_active = is_active

    # ============================================================
    # GENERAL INFORMATION
    # ============================================================

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

    # Already completed.
    if not layout.is_active:
        return layout

    now = datetime.utcnow()

    # ============================================================
    # COMPLETE LAYOUT
    # ============================================================

    layout.completed_at = now
    layout.is_active = False
    layout.status = "COMPLETED"

    # ============================================================
    # CALCULATE DURATION
    # ============================================================

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