from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, get_db
from app.models.line import Line
from app.models.line_assignment import LineAssignment
from app.models.organization import OrganizationUnit
from app.models.user import User
from app.schemas.organization import (
    LineCreate,
    LineResponse,
    LineUpdate,
    OrganizationUnitCreate,
    OrganizationUnitResponse,
    OrganizationUnitUpdate,
)


router = APIRouter(
    prefix="/organization",
    tags=["Organization Management"],
)


# ============================================================
# ROLE GROUPS
# ============================================================

MANAGEMENT_ROLES = {
    "ADMIN",
    "DGM",
    "CENTRAL_MANAGER",
}

UNIT_MANAGEMENT_ROLES = {
    "FLOOR_IE",
    "DPM",
    "APM",
    "IN_CHARGE",
}

GROUP_MANAGEMENT_ROLES = {
    "GROUP_MANAGER",
}


# ============================================================
# ADMIN CHECK
# ============================================================

def require_admin_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if current_user.role.code != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can manage organization structure",
        )

    return current_user


# ============================================================
# HELPERS
# ============================================================

def validate_unit_type(unit_type: str) -> str:
    value = unit_type.strip().upper()

    if value not in {"GROUP", "UNIT"}:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="unit_type must be GROUP or UNIT",
        )

    return value


def validate_parent_for_unit(
    db: Session,
    unit_type: str,
    parent_id: int | None,
) -> None:

    # --------------------------------------------------------
    # GROUP
    # --------------------------------------------------------

    if unit_type == "GROUP":

        if parent_id is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A GROUP cannot have a parent",
            )

        return

    # --------------------------------------------------------
    # UNIT
    # --------------------------------------------------------

    if parent_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A UNIT must belong to a GROUP",
        )

    parent = db.scalar(
        select(OrganizationUnit).where(
            OrganizationUnit.id == parent_id
        )
    )

    if not parent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Parent organization not found",
        )

    if parent.unit_type != "GROUP":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A UNIT can only belong to a GROUP",
        )


def validate_not_descendant(
    db: Session,
    unit_id: int,
    new_parent_id: int | None,
) -> None:

    if new_parent_id is None:
        return

    if unit_id == new_parent_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An organization unit cannot be its own parent",
        )

    current_id = new_parent_id
    visited: set[int] = set()

    while current_id is not None:

        if current_id in visited:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid organization hierarchy",
            )

        visited.add(current_id)

        if current_id == unit_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot move an organization under its own child",
            )

        parent = db.scalar(
            select(OrganizationUnit).where(
                OrganizationUnit.id == current_id
            )
        )

        if not parent:
            break

        current_id = parent.parent_id


def get_unit(
    db: Session,
    organization_unit_id: int,
) -> OrganizationUnit:

    organization_unit = db.scalar(
        select(OrganizationUnit).where(
            OrganizationUnit.id == organization_unit_id
        )
    )

    if not organization_unit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization unit not found",
        )

    return organization_unit


def get_line(
    db: Session,
    line_id: int,
) -> Line:

    line = db.scalar(
        select(Line).where(
            Line.id == line_id
        )
    )

    if not line:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Line not found",
        )

    return line


# ============================================================
# ORGANIZATION ACCESS HELPERS
# ============================================================

def can_access_organization(
    db: Session,
    current_user: User,
    organization_unit: OrganizationUnit,
) -> bool:

    role = current_user.role.code

    # --------------------------------------------------------
    # ADMIN / MANAGEMENT
    # --------------------------------------------------------

    if role in MANAGEMENT_ROLES:
        return True

    # --------------------------------------------------------
    # GROUP MANAGER
    # --------------------------------------------------------

    if role in GROUP_MANAGEMENT_ROLES:

        group_id = current_user.organization_unit_id

        if not group_id:
            return False

        # Can access their own group
        if organization_unit.id == group_id:
            return True

        # Can access units directly under their group
        return organization_unit.parent_id == group_id

    # --------------------------------------------------------
    # FLOOR IE / DPM / APM / IN_CHARGE
    # --------------------------------------------------------

    if role in UNIT_MANAGEMENT_ROLES:

        return (
            current_user.organization_unit_id
            == organization_unit.id
        )

    # --------------------------------------------------------
    # SUPERVISOR
    # --------------------------------------------------------

    if role == "SUPERVISOR":

        return (
            current_user.organization_unit_id
            == organization_unit.id
        )

    return False


def can_access_line(
    db: Session,
    current_user: User,
    line: Line,
) -> bool:

    role = current_user.role.code

    # --------------------------------------------------------
    # ADMIN / MANAGEMENT
    # --------------------------------------------------------

    if role in MANAGEMENT_ROLES:
        return True

    # --------------------------------------------------------
    # GET LINE'S ORGANIZATION UNIT
    # --------------------------------------------------------

    unit = db.scalar(
        select(OrganizationUnit).where(
            OrganizationUnit.id == line.organization_unit_id
        )
    )

    if not unit:
        return False

    # --------------------------------------------------------
    # GROUP MANAGER
    # --------------------------------------------------------

    if role in GROUP_MANAGEMENT_ROLES:

        group_id = current_user.organization_unit_id

        if not group_id:
            return False

        return unit.parent_id == group_id

    # --------------------------------------------------------
    # FLOOR IE / DPM / APM / IN_CHARGE
    # --------------------------------------------------------

    if role in UNIT_MANAGEMENT_ROLES:

        return (
            current_user.organization_unit_id
            == line.organization_unit_id
        )

    # --------------------------------------------------------
    # SUPERVISOR
    # --------------------------------------------------------

    if role == "SUPERVISOR":

        assignment = db.scalar(
            select(LineAssignment).where(
                LineAssignment.employee_id
                == current_user.employee_id,
                LineAssignment.line_id == line.id,
                LineAssignment.is_active.is_(True),
            )
        )

        return assignment is not None

    return False


# ============================================================
# LIST ORGANIZATION
# ============================================================

@router.get(
    "/",
    response_model=list[OrganizationUnitResponse],
)
def list_organization_units(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    role = current_user.role.code

    # --------------------------------------------------------
    # ADMIN / MANAGEMENT ROLES
    # --------------------------------------------------------

    if role in MANAGEMENT_ROLES:

        return db.scalars(
            select(OrganizationUnit)
            .order_by(
                OrganizationUnit.unit_type,
                OrganizationUnit.code,
            )
        ).all()

    # --------------------------------------------------------
    # GROUP MANAGER
    # --------------------------------------------------------

    if role in GROUP_MANAGEMENT_ROLES:

        group_id = current_user.organization_unit_id

        if not group_id:
            return []

        return db.scalars(
            select(OrganizationUnit)
            .where(
                (OrganizationUnit.id == group_id)
                | (OrganizationUnit.parent_id == group_id)
            )
            .order_by(
                OrganizationUnit.code
            )
        ).all()

    # --------------------------------------------------------
    # FLOOR IE / DPM / APM / IN_CHARGE
    # --------------------------------------------------------

    if role in UNIT_MANAGEMENT_ROLES:

        if not current_user.organization_unit_id:
            return []

        unit = db.scalar(
            select(OrganizationUnit).where(
                OrganizationUnit.id
                == current_user.organization_unit_id
            )
        )

        return [unit] if unit else []

    # --------------------------------------------------------
    # SUPERVISOR
    # --------------------------------------------------------

    if role == "SUPERVISOR":

        if not current_user.organization_unit_id:
            return []

        unit = db.scalar(
            select(OrganizationUnit).where(
                OrganizationUnit.id
                == current_user.organization_unit_id
            )
        )

        return [unit] if unit else []

    return []


# ============================================================
# GET ONE ORGANIZATION UNIT
# ============================================================

@router.get(
    "/{organization_unit_id}",
    response_model=OrganizationUnitResponse,
)
def get_organization_unit(
    organization_unit_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    organization_unit = get_unit(
        db,
        organization_unit_id,
    )

    if not can_access_organization(
        db,
        current_user,
        organization_unit,
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this organization",
        )

    return organization_unit


# ============================================================
# CREATE ORGANIZATION UNIT
# ============================================================

@router.post(
    "/",
    response_model=OrganizationUnitResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_organization_unit(
    data: OrganizationUnitCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_user),
):

    name = data.name.strip()
    code = data.code.strip()
    unit_type = validate_unit_type(data.unit_type)

    # --------------------------------------------------------
    # VALIDATE NAME
    # --------------------------------------------------------

    if not name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Organization name is required",
        )

    # --------------------------------------------------------
    # VALIDATE CODE
    # --------------------------------------------------------

    if not code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Organization code is required",
        )

    # --------------------------------------------------------
    # CODE MUST BE UNIQUE
    # --------------------------------------------------------

    existing = db.scalar(
        select(OrganizationUnit).where(
            OrganizationUnit.code == code
        )
    )

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Organization code already exists",
        )

    # --------------------------------------------------------
    # VALIDATE PARENT
    # --------------------------------------------------------

    validate_parent_for_unit(
        db,
        unit_type,
        data.parent_id,
    )

    # --------------------------------------------------------
    # CREATE
    # --------------------------------------------------------

    organization_unit = OrganizationUnit(
        name=name,
        code=code,
        unit_type=unit_type,
        parent_id=data.parent_id,
        is_active=data.is_active,
    )

    db.add(organization_unit)
    db.commit()
    db.refresh(organization_unit)

    return organization_unit


# ============================================================
# UPDATE ORGANIZATION UNIT
# ============================================================

@router.put(
    "/{organization_unit_id}",
    response_model=OrganizationUnitResponse,
)
def update_organization_unit(
    organization_unit_id: int,
    data: OrganizationUnitUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_user),
):

    organization_unit = get_unit(
        db,
        organization_unit_id,
    )

    # --------------------------------------------------------
    # NEW NAME
    # --------------------------------------------------------

    new_name = (
        data.name.strip()
        if data.name is not None
        else organization_unit.name
    )

    # --------------------------------------------------------
    # NEW CODE
    # --------------------------------------------------------

    new_code = (
        data.code.strip()
        if data.code is not None
        else organization_unit.code
    )

    # --------------------------------------------------------
    # NEW TYPE
    # --------------------------------------------------------

    new_type = (
        validate_unit_type(data.unit_type)
        if data.unit_type is not None
        else organization_unit.unit_type
    )

    # --------------------------------------------------------
    # NEW PARENT
    # --------------------------------------------------------

    new_parent_id = (
        data.parent_id
        if data.parent_id is not None
        else organization_unit.parent_id
    )

    # --------------------------------------------------------
    # VALIDATE NAME
    # --------------------------------------------------------

    if not new_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Organization name is required",
        )

    # --------------------------------------------------------
    # VALIDATE CODE
    # --------------------------------------------------------

    if not new_code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Organization code is required",
        )

    # --------------------------------------------------------
    # CHECK DUPLICATE CODE
    # --------------------------------------------------------

    duplicate = db.scalar(
        select(OrganizationUnit).where(
            OrganizationUnit.code == new_code,
            OrganizationUnit.id != organization_unit_id,
        )
    )

    if duplicate:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Organization code already exists",
        )

    # --------------------------------------------------------
    # VALIDATE PARENT
    # --------------------------------------------------------

    validate_parent_for_unit(
        db,
        new_type,
        new_parent_id,
    )

    # --------------------------------------------------------
    # PREVENT CIRCULAR HIERARCHY
    # --------------------------------------------------------

    validate_not_descendant(
        db,
        organization_unit_id,
        new_parent_id,
    )

    # --------------------------------------------------------
    # UPDATE
    # --------------------------------------------------------

    organization_unit.name = new_name
    organization_unit.code = new_code
    organization_unit.unit_type = new_type
    organization_unit.parent_id = new_parent_id

    if data.is_active is not None:
        organization_unit.is_active = data.is_active

    db.commit()
    db.refresh(organization_unit)

    return organization_unit


# ============================================================
# LIST LINES FOR ORGANIZATION UNIT
# ============================================================

@router.get(
    "/{organization_unit_id}/lines",
    response_model=list[LineResponse],
)
def list_unit_lines(
    organization_unit_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    # --------------------------------------------------------
    # GET UNIT
    # --------------------------------------------------------

    unit = get_unit(
        db,
        organization_unit_id,
    )

    # --------------------------------------------------------
    # LINES CAN ONLY BELONG TO UNIT
    # --------------------------------------------------------

    if unit.unit_type != "UNIT":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Lines can only be requested for a UNIT",
        )

    role = current_user.role.code

    # --------------------------------------------------------
    # ADMIN / MANAGEMENT
    # --------------------------------------------------------

    if role in MANAGEMENT_ROLES:

        return db.scalars(
            select(Line)
            .where(
                Line.organization_unit_id
                == organization_unit_id
            )
            .order_by(
                Line.line_number
            )
        ).all()

    # --------------------------------------------------------
    # GROUP MANAGER
    # --------------------------------------------------------

    if role in GROUP_MANAGEMENT_ROLES:

        group_id = current_user.organization_unit_id

        if not group_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not assigned to an organization group",
            )

        if unit.parent_id != group_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have access to this unit",
            )

        return db.scalars(
            select(Line)
            .where(
                Line.organization_unit_id
                == organization_unit_id
            )
            .order_by(
                Line.line_number
            )
        ).all()

    # --------------------------------------------------------
    # FLOOR IE / DPM / APM / IN_CHARGE
    # --------------------------------------------------------

    if role in UNIT_MANAGEMENT_ROLES:

        if (
            current_user.organization_unit_id
            != organization_unit_id
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have access to this unit",
            )

        return db.scalars(
            select(Line)
            .where(
                Line.organization_unit_id
                == organization_unit_id
            )
            .order_by(
                Line.line_number
            )
        ).all()

    # --------------------------------------------------------
    # SUPERVISOR
    # --------------------------------------------------------

    if role == "SUPERVISOR":

        if (
            current_user.organization_unit_id
            != organization_unit_id
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have access to this unit",
            )

        return db.scalars(
            select(Line)
            .join(
                LineAssignment,
                LineAssignment.line_id == Line.id,
            )
            .where(
                Line.organization_unit_id
                == organization_unit_id,
                LineAssignment.employee_id
                == current_user.employee_id,
                LineAssignment.is_active.is_(True),
            )
            .order_by(
                Line.line_number
            )
        ).all()

    # --------------------------------------------------------
    # OTHER ROLES
    # --------------------------------------------------------

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You do not have access to lines",
    )


# ============================================================
# CREATE LINE
# ============================================================

@router.post(
    "/{organization_unit_id}/lines",
    response_model=LineResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_line(
    organization_unit_id: int,
    data: LineCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_user),
):

    # --------------------------------------------------------
    # GET UNIT
    # --------------------------------------------------------

    unit = get_unit(
        db,
        organization_unit_id,
    )

    # --------------------------------------------------------
    # ONLY UNIT CAN HAVE LINES
    # --------------------------------------------------------

    if unit.unit_type != "UNIT":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Lines can only belong to a UNIT",
        )

    # --------------------------------------------------------
    # VALIDATE LINE NUMBER
    # --------------------------------------------------------

    if data.line_number <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Line number must be positive",
        )

    # --------------------------------------------------------
    # VALIDATE NAME
    # --------------------------------------------------------

    if not data.name.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Line name is required",
        )

    # --------------------------------------------------------
    # LINE NUMBER MUST BE UNIQUE
    # --------------------------------------------------------

    existing = db.scalar(
        select(Line).where(
            Line.line_number == data.line_number
        )
    )

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Line number already exists",
        )

    # --------------------------------------------------------
    # CREATE LINE
    # --------------------------------------------------------

    line = Line(
        line_number=data.line_number,
        name=data.name.strip(),
        organization_unit_id=organization_unit_id,
        is_active=data.is_active,
    )

    db.add(line)
    db.commit()
    db.refresh(line)

    return line


# ============================================================
# UPDATE LINE
# ============================================================

@router.put(
    "/lines/{line_id}",
    response_model=LineResponse,
)
def update_line(
    line_id: int,
    data: LineUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_user),
):

    # --------------------------------------------------------
    # GET LINE
    # --------------------------------------------------------

    line = get_line(
        db,
        line_id,
    )

    # --------------------------------------------------------
    # NEW LINE NUMBER
    # --------------------------------------------------------

    new_line_number = (
        data.line_number
        if data.line_number is not None
        else line.line_number
    )

    # --------------------------------------------------------
    # NEW NAME
    # --------------------------------------------------------

    new_name = (
        data.name.strip()
        if data.name is not None
        else line.name
    )

    # --------------------------------------------------------
    # NEW UNIT
    # --------------------------------------------------------

    new_unit_id = (
        data.organization_unit_id
        if data.organization_unit_id is not None
        else line.organization_unit_id
    )

    # --------------------------------------------------------
    # VALIDATE LINE NUMBER
    # --------------------------------------------------------

    if new_line_number <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Line number must be positive",
        )

    # --------------------------------------------------------
    # VALIDATE NAME
    # --------------------------------------------------------

    if not new_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Line name is required",
        )

    # --------------------------------------------------------
    # VALIDATE UNIT
    # --------------------------------------------------------

    unit = get_unit(
        db,
        new_unit_id,
    )

    if unit.unit_type != "UNIT":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A line can only belong to a UNIT",
        )

    # --------------------------------------------------------
    # CHECK DUPLICATE LINE NUMBER
    # --------------------------------------------------------

    duplicate = db.scalar(
        select(Line).where(
            Line.line_number == new_line_number,
            Line.id != line_id,
        )
    )

    if duplicate:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Line number already exists",
        )

    # --------------------------------------------------------
    # UPDATE
    # --------------------------------------------------------

    line.line_number = new_line_number
    line.name = new_name
    line.organization_unit_id = new_unit_id

    if data.is_active is not None:
        line.is_active = data.is_active

    db.commit()
    db.refresh(line)

    return line


# ============================================================
# GET SINGLE LINE
# ============================================================

@router.get(
    "/lines/{line_id}",
    response_model=LineResponse,
)
def get_line_endpoint(
    line_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    # --------------------------------------------------------
    # GET LINE
    # --------------------------------------------------------

    line = get_line(
        db,
        line_id,
    )

    # --------------------------------------------------------
    # CHECK ROLE / SCOPE
    # --------------------------------------------------------

    if not can_access_line(
        db,
        current_user,
        line,
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this line",
        )

    return line