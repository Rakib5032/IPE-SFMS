from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.dependencies import (
    check_line_access,
    get_current_user,
    get_db,
)
from app.models.line import Line
from app.models.user import User
from app.schemas.line_status import (
    LineStatusCreate,
    LineStatusResponse,
)
from app.services import line_status_service


router = APIRouter(
    prefix="/line-status",
    tags=["Line Status"],
)


# ============================================================
# GET CURRENT STATUS
# ============================================================

@router.get(
    "/{line_id}",
    response_model=LineStatusResponse | None,
)
def get_current_line_status(
    line_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # --------------------------------------------------------
    # Check line access
    # --------------------------------------------------------

    check_line_access(
        line_id=line_id,
        current_user=current_user,
        db=db,
    )

    # --------------------------------------------------------
    # Check line exists
    # --------------------------------------------------------

    line = db.get(
        Line,
        line_id,
    )

    if not line:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Line not found",
        )

    # --------------------------------------------------------
    # Return current status
    # --------------------------------------------------------

    return line_status_service.get_current_status(
        db=db,
        line_id=line_id,
    )


# ============================================================
# GET STATUS HISTORY
# ============================================================

@router.get(
    "/{line_id}/history",
    response_model=list[LineStatusResponse],
)
def get_line_status_history(
    line_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # --------------------------------------------------------
    # Check line access
    # --------------------------------------------------------

    check_line_access(
        line_id=line_id,
        current_user=current_user,
        db=db,
    )

    # --------------------------------------------------------
    # Check line exists
    # --------------------------------------------------------

    line = db.get(
        Line,
        line_id,
    )

    if not line:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Line not found",
        )

    # --------------------------------------------------------
    # Return history
    # --------------------------------------------------------

    return line_status_service.get_status_history(
        db=db,
        line_id=line_id,
    )


# ============================================================
# CHANGE LINE STATUS
# ============================================================

@router.post(
    "/{line_id}",
    response_model=LineStatusResponse,
    status_code=status.HTTP_201_CREATED,
)
def change_line_status(
    line_id: int,
    data: LineStatusCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # --------------------------------------------------------
    # Check line access
    # --------------------------------------------------------

    check_line_access(
        line_id=line_id,
        current_user=current_user,
        db=db,
    )

    # --------------------------------------------------------
    # Check line exists
    # --------------------------------------------------------

    line = db.get(
        Line,
        line_id,
    )

    if not line:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Line not found",
        )

    # --------------------------------------------------------
    # Verify body line_id
    # --------------------------------------------------------

    if data.line_id != line_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Line ID does not match the requested line",
        )

    # --------------------------------------------------------
    # Validate status
    # --------------------------------------------------------

    allowed_statuses = {
        "RUNNING",
        "LAYOUT",
        "OFF",
    }

    if data.status not in allowed_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Invalid status. "
                "Allowed values: RUNNING, LAYOUT, OFF"
            ),
        )

    # --------------------------------------------------------
    # Create new status
    # --------------------------------------------------------

    return line_status_service.create_status(
        db=db,
        line_id=line_id,
        status=data.status,
        reason=data.reason,
    )