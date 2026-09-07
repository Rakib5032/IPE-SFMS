from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, get_db
from app.models.line import Line
from app.models.line_assignment import LineAssignment
from app.models.organization import OrganizationUnit
from app.models.user import User
from app.schemas.line_assignment import (
    LineAssignmentCreate,
    LineAssignmentResponse,
    LineAssignmentUpdate,
)
from app.services import line_assignment_service


router = APIRouter(
    prefix="/line-assignments",
    tags=["Line Assignments"],
)


# ============================================================
# CREATE ASSIGNMENT
# ============================================================

@router.post(
    "/",
    response_model=LineAssignmentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_line_assignment(
    data: LineAssignmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    role = current_user.role.code

    # Permission

    allowed_roles = {
        "ADMIN",
        "DGM",
        "CENTRAL_MANAGER",
        "GROUP_MANAGER",
        "ASSISTANT_MANAGER",
        "FLOOR_IE",
    }

    if role not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot assign employees to lines",
        )

    # Get employee

    employee = db.scalar(
        select(User).where(
            User.employee_id == data.employee_id
        )
    )

    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found",
        )

    if not employee.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Employee is inactive",
        )

    # Only supervisors should receive line assignments.
    if employee.role.code != "SUPERVISOR":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only supervisors can be assigned to lines",
        )

    # Get line
    
    line = db.scalar(
        select(Line).where(
            Line.id == data.line_id
        )
    )

    if not line:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Line not found",
        )

    if not line.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Line is inactive",
        )

    # Check assigner's scope


    if role in {
        "GROUP_MANAGER",
        "ASSISTANT_MANAGER",
    }:
        if current_user.organization_unit_id is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No group assigned to current user",
            )

        unit = db.scalar(
            select(OrganizationUnit).where(
                OrganizationUnit.id
                == line.organization_unit_id
            )
        )

        if not unit:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Line organization unit not found",
            )

        if (
            unit.unit_type != "UNIT"
            or unit.parent_id
            != current_user.organization_unit_id
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="This line is outside your assigned group",
            )

    elif role == "FLOOR_IE":
        if (
            current_user.organization_unit_id
            != line.organization_unit_id
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="This line is outside your assigned unit",
            )

    # Check supervisor's existing active assignment

    existing = (
        line_assignment_service
        .get_active_user_line_assignment(
            db=db,
            employee_id=data.employee_id,
            line_id=data.line_id,
        )
    )

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This supervisor is already assigned to this line",
        )

    # Create

    return line_assignment_service.create_assignment(
        db=db,
        employee_id=data.employee_id,
        line_id=data.line_id,
        assignment_type=data.assignment_type,
    )



# GET ALL ACTIVE ASSIGNMENTS

@router.get(
    "/",
    response_model=list[LineAssignmentResponse],
)
def get_line_assignments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    role = current_user.role.code

    allowed_roles = {
        "ADMIN",
        "DGM",
        "CENTRAL_MANAGER",
        "GROUP_MANAGER",
        "ASSISTANT_MANAGER",
        "FLOOR_IE",
    }

    if role not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot view line assignments",
        )

    assignments = (
        line_assignment_service
        .get_active_assignments(db)
    )

    # Factory-wide users.
    if role in {
        "ADMIN",
        "DGM",
        "CENTRAL_MANAGER",
    }:
        return assignments


    # Group Manager / Assistant Manager

    if role in {
        "GROUP_MANAGER",
        "ASSISTANT_MANAGER",
    }:
        if current_user.organization_unit_id is None:
            return []

        result = []

        for assignment in assignments:
            line = db.get(
                Line,
                assignment.line_id,
            )

            if not line:
                continue

            unit = db.get(
                OrganizationUnit,
                line.organization_unit_id,
            )

            if not unit:
                continue

            if (
                unit.unit_type == "UNIT"
                and unit.parent_id
                == current_user.organization_unit_id
            ):
                result.append(assignment)

        return result

    # Floor IE

    if role == "FLOOR_IE":
        return [
            assignment
            for assignment in assignments
            if (
                db.get(
                    Line,
                    assignment.line_id,
                )
                and db.get(
                    Line,
                    assignment.line_id,
                ).organization_unit_id
                == current_user.organization_unit_id
            )
        ]

    return []


# ============================================================
# GET ONE ASSIGNMENT
# ============================================================

@router.get(
    "/{assignment_id}",
    response_model=LineAssignmentResponse,
)
def get_line_assignment(
    assignment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    assignment = line_assignment_service.get_assignment(
        db,
        assignment_id,
    )

    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Line assignment not found",
        )

    line = db.get(
        Line,
        assignment.line_id,
    )

    if not line:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assigned line not found",
        )

    role = current_user.role.code

    # Factory-wide
    if role in {
        "ADMIN",
        "DGM",
        "CENTRAL_MANAGER",
    }:
        return assignment

    # Group level
    if role in {
        "GROUP_MANAGER",
        "ASSISTANT_MANAGER",
    }:
        unit = db.get(
            OrganizationUnit,
            line.organization_unit_id,
        )

        if (
            not unit
            or unit.parent_id
            != current_user.organization_unit_id
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have access to this assignment",
            )

        return assignment

    # Floor IE
    if role == "FLOOR_IE":
        if (
            line.organization_unit_id
            != current_user.organization_unit_id
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have access to this assignment",
            )

        return assignment

    # Supervisor can view their own assignment.
    if role == "SUPERVISOR":
        if (
            assignment.employee_id
            != current_user.employee_id
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have access to this assignment",
            )

        return assignment

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Assignment access denied",
    )


# ============================================================
# MY ASSIGNMENTS
# ============================================================

@router.get(
    "/my/active",
    response_model=list[LineAssignmentResponse],
)
def get_my_active_assignments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return [
        assignment
        for assignment in (
            line_assignment_service
            .get_user_assignments(
                db,
                current_user.employee_id,
            )
        )
        if assignment.is_active
    ]


# ============================================================
# END ASSIGNMENT
# ============================================================

@router.post(
    "/{assignment_id}/end",
    response_model=LineAssignmentResponse,
)
def end_line_assignment(
    assignment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    assignment = line_assignment_service.get_assignment(
        db,
        assignment_id,
    )

    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Line assignment not found",
        )

    role = current_user.role.code

    allowed_roles = {
        "ADMIN",
        "DGM",
        "CENTRAL_MANAGER",
        "GROUP_MANAGER",
        "ASSISTANT_MANAGER",
        "FLOOR_IE",
    }

    if role not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot end line assignments",
        )

    line = db.get(
        Line,
        assignment.line_id,
    )

    if not line:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assigned line not found",
        )

    # Group scope
    if role in {
        "GROUP_MANAGER",
        "ASSISTANT_MANAGER",
    }:
        unit = db.get(
            OrganizationUnit,
            line.organization_unit_id,
        )

        if (
            not unit
            or unit.parent_id
            != current_user.organization_unit_id
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="This assignment is outside your group",
            )

    # Unit scope
    if role == "FLOOR_IE":
        if (
            line.organization_unit_id
            != current_user.organization_unit_id
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="This assignment is outside your unit",
            )

    if not assignment.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Assignment is already inactive",
        )

    return line_assignment_service.end_assignment(
        db,
        assignment,
    )