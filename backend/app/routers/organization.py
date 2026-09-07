from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, get_db
from app.models.line import Line
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


# ADMIN CHECK

def require_admin_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if current_user.role.code != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can manage organization structure",
        )

    return current_user


# HELPERS

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

    if unit_type == "GROUP":

        if parent_id is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A GROUP cannot have a parent",
            )

        return

    # UNIT
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


# LIST ORGANIZATION

@router.get(
    "/",
    response_model=list[OrganizationUnitResponse],
)
def list_organization_units(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    role = current_user.role.code

    # ADMIN / MANAGEMENT ROLES CAN VIEW EVERYTHING
    if role in {
        "ADMIN",
        "DGM",
        "CENTRAL_MANAGER",
    }:
        return db.scalars(
            select(OrganizationUnit)
            .order_by(
                OrganizationUnit.unit_type,
                OrganizationUnit.code,
            )
        ).all()

    # GROUP MANAGER
    if role in {
        "GROUP_MANAGER",
        "ASSISTANT_MANAGER",
    }:

        group_id = current_user.organization_unit_id

        if not group_id:
            return []

        return db.scalars(
            select(OrganizationUnit)
            .where(
                (OrganizationUnit.id == group_id)
                | (OrganizationUnit.parent_id == group_id)
            )
            .order_by(OrganizationUnit.code)
        ).all()

    # FLOOR IE
    if role == "FLOOR_IE":

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


# GET ONE ORGANIZATION UNIT

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

    role = current_user.role.code

    if role in {
        "ADMIN",
        "DGM",
        "CENTRAL_MANAGER",
    }:
        return organization_unit

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You do not have access to this organization",
    )


# CREATE ORGANIZATION UNIT

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

    if not name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Organization name is required",
        )

    if not code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Organization code is required",
        )

    # CODE MUST BE UNIQUE
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

    validate_parent_for_unit(
        db,
        unit_type,
        data.parent_id,
    )

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


# UPDATE ORGANIZATION UNIT

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

    new_name = (
        data.name.strip()
        if data.name is not None
        else organization_unit.name
    )

    new_code = (
        data.code.strip()
        if data.code is not None
        else organization_unit.code
    )

    new_type = (
        validate_unit_type(data.unit_type)
        if data.unit_type is not None
        else organization_unit.unit_type
    )

    new_parent_id = (
        data.parent_id
        if data.parent_id is not None
        else organization_unit.parent_id
    )

    if not new_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Organization name is required",
        )

    if not new_code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Organization code is required",
        )

    # CHECK DUPLICATE CODE
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

    # VALIDATE PARENT
    validate_parent_for_unit(
        db,
        new_type,
        new_parent_id,
    )

    validate_not_descendant(
        db,
        organization_unit_id,
        new_parent_id,
    )

    organization_unit.name = new_name
    organization_unit.code = new_code
    organization_unit.unit_type = new_type
    organization_unit.parent_id = new_parent_id

    if data.is_active is not None:
        organization_unit.is_active = data.is_active

    db.commit()
    db.refresh(organization_unit)

    return organization_unit


# LIST LINES

@router.get(
    "/{organization_unit_id}/lines",
    response_model=list[LineResponse],
)
def list_unit_lines(
    organization_unit_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    get_unit(
        db,
        organization_unit_id,
    )

    return db.scalars(
        select(Line)
        .where(
            Line.organization_unit_id
            == organization_unit_id
        )
        .order_by(Line.line_number)
    ).all()


# CREATE LINE

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

    unit = get_unit(
        db,
        organization_unit_id,
    )

    if unit.unit_type != "UNIT":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Lines can only belong to a UNIT",
        )

    if data.line_number <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Line number must be positive",
        )

    if not data.name.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Line name is required",
        )

    # LINE NUMBER MUST BE UNIQUE
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


# UPDATE LINE

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

    line = get_line(
        db,
        line_id,
    )

    new_line_number = (
        data.line_number
        if data.line_number is not None
        else line.line_number
    )

    new_name = (
        data.name.strip()
        if data.name is not None
        else line.name
    )

    new_unit_id = (
        data.organization_unit_id
        if data.organization_unit_id is not None
        else line.organization_unit_id
    )

    if new_line_number <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Line number must be positive",
        )

    if not new_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Line name is required",
        )

    # VALIDATE UNIT
    unit = get_unit(
        db,
        new_unit_id,
    )

    if unit.unit_type != "UNIT":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A line can only belong to a UNIT",
        )

    # CHECK DUPLICATE LINE NUMBER
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

    line.line_number = new_line_number
    line.name = new_name
    line.organization_unit_id = new_unit_id

    if data.is_active is not None:
        line.is_active = data.is_active

    db.commit()
    db.refresh(line)

    return line


# GET LINE

@router.get(
    "/lines/{line_id}",
    response_model=LineResponse,
)
def get_line_endpoint(
    line_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return get_line(
        db,
        line_id,
    )