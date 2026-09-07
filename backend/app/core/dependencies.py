from collections.abc import Generator

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.database.connection import SessionLocal
from app.models.user import User


security = HTTPBearer()


# ============================================================
# DATABASE
# ============================================================

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# ============================================================
# AUTHENTICATION
# ============================================================

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        if payload.get("type") != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
            )

        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
            )

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    user = db.scalar(
        select(User).where(
            User.employee_id == int(user_id)
        )
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )

    return user


# ============================================================
# ROLE CHECKS
# ============================================================

def require_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    if current_user.role.code != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )

    return current_user


def require_factory_access(
    current_user: User = Depends(get_current_user),
) -> User:
    allowed_roles = {
        "ADMIN",
        "DGM",
        "CENTRAL_MANAGER",
    }

    if current_user.role.code not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Factory-wide access required",
        )

    return current_user


def require_group_access(
    current_user: User = Depends(get_current_user),
) -> User:
    allowed_roles = {
        "ADMIN",
        "DGM",
        "CENTRAL_MANAGER",
        "GROUP_MANAGER",
        "ASSISTANT_MANAGER",
    }

    if current_user.role.code not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Group access required",
        )

    return current_user


def require_unit_access(
    current_user: User = Depends(get_current_user),
) -> User:
    allowed_roles = {
        "ADMIN",
        "DGM",
        "CENTRAL_MANAGER",
        "GROUP_MANAGER",
        "ASSISTANT_MANAGER",
        "FLOOR_IE",
    }

    if current_user.role.code not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unit access required",
        )

    return current_user


def require_line_access(
    current_user: User = Depends(get_current_user),
) -> User:
    allowed_roles = {
        "ADMIN",
        "DGM",
        "CENTRAL_MANAGER",
        "GROUP_MANAGER",
        "ASSISTANT_MANAGER",
        "FLOOR_IE",
        "SUPERVISOR",
    }

    if current_user.role.code not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Line access required",
        )

    return current_user


# ============================================================
# ORGANIZATION SCOPE
# ============================================================

def is_unit_in_user_group(
    unit_id: int,
    current_user: User,
    db: Session,
) -> bool:
    """
    Check whether a UNIT belongs to the GROUP
    assigned to the current user.
    """

    from app.models.organization import OrganizationUnit

    unit = db.scalar(
        select(OrganizationUnit).where(
            OrganizationUnit.id == unit_id
        )
    )

    if not unit:
        return False

    # Requested organization must be a UNIT.
    if unit.unit_type != "UNIT":
        return False

    # UNIT must have a parent.
    group = unit.parent

    if not group:
        return False

    # Parent must be a GROUP.
    if group.unit_type != "GROUP":
        return False

    return (
        current_user.organization_unit_id
        == group.id
    )


def is_line_in_user_group(
    line_id: int,
    current_user: User,
    db: Session,
) -> bool:
    """
    Check whether a LINE belongs to the GROUP
    assigned to the current user.
    """

    from app.models.line import Line

    line = db.scalar(
        select(Line).where(
            Line.id == line_id
        )
    )

    if not line:
        return False

    return is_unit_in_user_group(
        line.organization_unit_id,
        current_user,
        db,
    )


# ============================================================
# GROUP ACCESS
# ============================================================

def check_group_access(
    organization_unit_id: int,
    current_user: User,
    db: Session,
) -> None:
    """
    Check whether the current user can access
    the requested GROUP.
    """

    role = current_user.role.code

    # Admin, DGM and Central Manager
    # can access every group.
    if role in {
        "ADMIN",
        "DGM",
        "CENTRAL_MANAGER",
    }:
        return

    # Group Manager and Assistant Manager
    # can access only their assigned group.
    if role in {
        "GROUP_MANAGER",
        "ASSISTANT_MANAGER",
    }:
        from app.models.organization import OrganizationUnit

        group = db.scalar(
            select(OrganizationUnit).where(
                OrganizationUnit.id == organization_unit_id
            )
        )

        if not group:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Group not found",
            )

        if group.unit_type != "GROUP":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Requested organization is not a group",
            )

        if current_user.organization_unit_id != group.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have access to this group",
            )

        return

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Group access denied",
    )


# ============================================================
# UNIT ACCESS
# ============================================================

def check_unit_access(
    organization_unit_id: int,
    current_user: User,
    db: Session,
) -> None:
    """
    Check whether the current user can access
    the requested UNIT.
    """

    role = current_user.role.code

    # Admin, DGM and Central Manager
    # can access every unit.
    if role in {
        "ADMIN",
        "DGM",
        "CENTRAL_MANAGER",
    }:
        return

    # Group Manager and Assistant Manager
    # can access units inside their group.
    if role in {
        "GROUP_MANAGER",
        "ASSISTANT_MANAGER",
    }:
        if not is_unit_in_user_group(
            organization_unit_id,
            current_user,
            db,
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="This unit is outside your assigned group",
            )

        return

    # Floor IE can access only their assigned unit.
    if role == "FLOOR_IE":
        if current_user.organization_unit_id != organization_unit_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have access to this unit",
            )

        return

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Unit access denied",
    )


# ============================================================
# LINE ACCESS
# ============================================================

def check_line_access(
    line_id: int,
    current_user: User,
    db: Session,
) -> None:
    """
    Check whether the current user can access
    a particular production line.
    """

    role = current_user.role.code

    # --------------------------------------------------------
    # Admin / DGM / Central Manager
    # --------------------------------------------------------

    if role in {
        "ADMIN",
        "DGM",
        "CENTRAL_MANAGER",
    }:
        return

    # --------------------------------------------------------
    # Get line
    # --------------------------------------------------------

    from app.models.line import Line

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

    # --------------------------------------------------------
    # Group Manager / Assistant Manager
    # --------------------------------------------------------

    if role in {
        "GROUP_MANAGER",
        "ASSISTANT_MANAGER",
    }:
        if not is_line_in_user_group(
            line_id,
            current_user,
            db,
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="This line is outside your assigned group",
            )

        return

    # --------------------------------------------------------
    # Floor IE
    # --------------------------------------------------------

    if role == "FLOOR_IE":
        if line.organization_unit_id != current_user.organization_unit_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have access to this line",
            )

        return

    # --------------------------------------------------------
    # Supervisor
    # --------------------------------------------------------

    if role == "SUPERVISOR":
        from app.models.line_assignment import LineAssignment

        assignment = db.scalar(
            select(LineAssignment).where(
                LineAssignment.employee_id
                == current_user.employee_id,
                LineAssignment.line_id
                == line_id,
                LineAssignment.is_active.is_(True),
            )
        )

        if not assignment:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="This line is not assigned to you",
            )

        return

    # --------------------------------------------------------
    # Unknown / unsupported role
    # --------------------------------------------------------

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Line access denied",
    )