from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, get_db
from app.models.line import Line
from app.models.organization import OrganizationUnit
from app.models.user import User
from app.schemas.line import (
    LineCreate,
    LineResponse,
    LineUpdate,
)
from app.services import line_service


router = APIRouter(
    prefix="/lines",
    tags=["Lines"],
)


# ============================================================
# CREATE LINE
# ============================================================

@router.post(
    "/",
    response_model=LineResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_line(
    data: LineCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Only Admin can create lines.
    if current_user.role.code != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can create lines",
        )

    # Check organization unit.
    unit = db.scalar(
        select(OrganizationUnit).where(
            OrganizationUnit.id
            == data.organization_unit_id
        )
    )

    if not unit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization unit not found",
        )

    if unit.unit_type != "UNIT":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A line must belong to a UNIT",
        )

    # Check duplicate line number.
    existing = db.scalar(
        select(Line).where(
            Line.line_number == data.line_number
        )
    )

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Line number already exists",
        )

    return line_service.create_line(
        db=db,
        line_number=data.line_number,
        name=data.name,
        organization_unit_id=data.organization_unit_id,
        is_active=data.is_active,
    )


# ============================================================
# LIST LINES
# ============================================================

@router.get(
    "/",
    response_model=list[LineResponse],
)
def list_lines(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    role = current_user.role.code

    # --------------------------------------------------------
    # ADMIN / DGM / CENTRAL MANAGER
    # --------------------------------------------------------

    if role in {
        "ADMIN",
        "DGM",
        "CENTRAL_MANAGER",
    }:
        return line_service.get_all_lines(db)

    # --------------------------------------------------------
    # GROUP MANAGER / ASSISTANT MANAGER
    # --------------------------------------------------------

    if role in {
        "GROUP_MANAGER",
        "ASSISTANT_MANAGER",
    }:
        if current_user.organization_unit_id is None:
            return []

        organization_unit = db.scalar(
            select(OrganizationUnit).where(
                OrganizationUnit.id
                == current_user.organization_unit_id
            )
        )

        if not organization_unit:
            return []

        # Their assigned organization must be a GROUP.
        if organization_unit.unit_type != "GROUP":
            return []

        return line_service.get_lines_by_group(
            db,
            organization_unit.id,
        )

    # --------------------------------------------------------
    # FLOOR IE
    # --------------------------------------------------------

    if role == "FLOOR_IE":
        if current_user.organization_unit_id is None:
            return []

        return line_service.get_lines_by_unit(
            db,
            current_user.organization_unit_id,
        )

    # --------------------------------------------------------
    # SUPERVISOR
    # --------------------------------------------------------

    if role == "SUPERVISOR":
        from app.models.line_assignment import LineAssignment

        assignments = db.scalars(
            select(LineAssignment).where(
                LineAssignment.employee_id
                == current_user.employee_id,
                LineAssignment.is_active.is_(True),
            )
        ).all()

        line_ids = [
            assignment.line_id
            for assignment in assignments
        ]

        if not line_ids:
            return []

        return list(
            db.scalars(
                select(Line)
                .where(Line.id.in_(line_ids))
                .order_by(Line.line_number)
            ).all()
        )

    return []


# ============================================================
# GET ONE LINE
# ============================================================

@router.get(
    "/{line_id}",
    response_model=LineResponse,
)
def get_line(
    line_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    line = line_service.get_line(
        db,
        line_id,
    )

    if not line:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Line not found",
        )

    role = current_user.role.code

    # --------------------------------------------------------
    # ADMIN / DGM / CENTRAL MANAGER
    # --------------------------------------------------------

    if role in {
        "ADMIN",
        "DGM",
        "CENTRAL_MANAGER",
    }:
        return line

    # --------------------------------------------------------
    # GROUP MANAGER / ASSISTANT MANAGER
    # --------------------------------------------------------

    if role in {
        "GROUP_MANAGER",
        "ASSISTANT_MANAGER",
    }:
        organization_unit = db.scalar(
            select(OrganizationUnit).where(
                OrganizationUnit.id
                == line.organization_unit_id
            )
        )

        if not organization_unit:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Line organization unit not found",
            )

        if (
            organization_unit.parent_id
            != current_user.organization_unit_id
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have access to this line",
            )

        return line

    # --------------------------------------------------------
    # FLOOR IE
    # --------------------------------------------------------

    if role == "FLOOR_IE":
        if (
            line.organization_unit_id
            != current_user.organization_unit_id
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have access to this line",
            )

        return line

    # --------------------------------------------------------
    # SUPERVISOR
    # --------------------------------------------------------

    if role == "SUPERVISOR":
        from app.models.line_assignment import LineAssignment

        assignment = db.scalar(
            select(LineAssignment).where(
                LineAssignment.employee_id
                == current_user.employee_id,
                LineAssignment.line_id == line_id,
                LineAssignment.is_active.is_(True),
            )
        )

        if not assignment:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="This line is not assigned to you",
            )

        return line

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Line access denied",
    )


# ============================================================
# UPDATE LINE
# ============================================================

@router.put(
    "/{line_id}",
    response_model=LineResponse,
)
def update_line(
    line_id: int,
    data: LineUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Only Admin can change line configuration.
    if current_user.role.code != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can update line configuration",
        )

    line = line_service.get_line(
        db,
        line_id,
    )

    if not line:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Line not found",
        )

    update_data = data.model_dump(
        exclude_unset=True
    )

    # --------------------------------------------------------
    # Validate line number
    # --------------------------------------------------------

    if "line_number" in update_data:
        existing = db.scalar(
            select(Line).where(
                Line.line_number
                == update_data["line_number"],
                Line.id != line_id,
            )
        )

        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Line number already exists",
            )

    # --------------------------------------------------------
    # Validate organization unit
    # --------------------------------------------------------

    if "organization_unit_id" in update_data:
        unit = db.scalar(
            select(OrganizationUnit).where(
                OrganizationUnit.id
                == update_data["organization_unit_id"]
            )
        )

        if not unit:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Organization unit not found",
            )

        if unit.unit_type != "UNIT":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A line must belong to a UNIT",
            )

    return line_service.update_line(
        db=db,
        line=line,
        update_data=update_data,
    )