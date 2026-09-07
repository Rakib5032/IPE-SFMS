from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.line_status import LineStatus


# ============================================================
# GET CURRENT STATUS
# ============================================================

def get_current_status(
    db: Session,
    line_id: int,
) -> LineStatus | None:
    return db.scalar(
        select(LineStatus)
        .where(
            LineStatus.line_id == line_id,
            LineStatus.ended_at.is_(None),
        )
        .order_by(
            LineStatus.started_at.desc()
        )
    )


# ============================================================
# GET STATUS HISTORY
# ============================================================

def get_status_history(
    db: Session,
    line_id: int,
) -> list[LineStatus]:
    return list(
        db.scalars(
            select(LineStatus)
            .where(
                LineStatus.line_id == line_id
            )
            .order_by(
                LineStatus.started_at.desc()
            )
        ).all()
    )


# ============================================================
# CREATE / CHANGE STATUS
# ============================================================

def create_status(
    db: Session,
    line_id: int,
    status: str,
    reason: str | None = None,
) -> LineStatus:

    now = datetime.utcnow()

    # --------------------------------------------------------
    # Close current status
    # --------------------------------------------------------

    current_status = get_current_status(
        db=db,
        line_id=line_id,
    )

    if current_status:
        current_status.ended_at = now

    # --------------------------------------------------------
    # Create new status
    # --------------------------------------------------------

    new_status = LineStatus(
        line_id=line_id,
        status=status,
        reason=reason,
        started_at=now,
    )

    db.add(new_status)

    db.commit()
    db.refresh(new_status)

    return new_status