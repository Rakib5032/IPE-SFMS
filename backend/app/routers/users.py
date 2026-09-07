from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, require_admin
from app.core.security import hash_password
from app.models.organization import OrganizationUnit
from app.models.role import Role
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserUpdate


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin),
):
    if user_data.employee_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Employee ID must be a positive integer",
        )

    if not user_data.full_name.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Full name is required",
        )

    if not user_data.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password is required",
        )

    if user_data.role_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Role ID must be a positive integer",
        )

    existing_employee = db.scalar(
        select(User).where(
            User.employee_id == user_data.employee_id
        )
    )

    if existing_employee:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Employee ID already exists",
        )

    if user_data.email:
        existing_email = db.scalar(
            select(User).where(
                User.email == user_data.email
            )
        )

        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already exists",
            )

    role = db.scalar(
        select(Role).where(
            Role.id == user_data.role_id
        )
    )

    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found",
        )

    if not role.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Role is inactive",
        )

    if user_data.organization_unit_id is not None:
        if user_data.organization_unit_id <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Organization unit ID must be a positive integer",
            )

        organization_unit = db.scalar(
            select(OrganizationUnit).where(
                OrganizationUnit.id
                == user_data.organization_unit_id
            )
        )

        if not organization_unit:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Organization unit not found",
            )

        if not organization_unit.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Organization unit is inactive",
            )

    user = User(
        employee_id=user_data.employee_id,
        username=str(user_data.employee_id),
        full_name=user_data.full_name.strip(),
        designation=(
            user_data.designation.strip()
            if user_data.designation
            else None
        ),
        email=user_data.email,
        password_hash=hash_password(
            user_data.password
        ),
        role_id=user_data.role_id,
        organization_unit_id=user_data.organization_unit_id,
        is_active=True,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@router.get(
    "/{employee_id}",
    response_model=UserResponse,
)
def get_user(
    employee_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin),
):
    if employee_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Employee ID must be a positive integer",
        )

    user = db.scalar(
        select(User).where(
            User.employee_id == employee_id
        )
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user


@router.patch(
    "/{employee_id}",
    response_model=UserResponse,
)
def update_user(
    employee_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin),
):
    if employee_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Employee ID must be a positive integer",
        )

    user = db.scalar(
        select(User).where(
            User.employee_id == employee_id
        )
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    if user_data.full_name is not None:
        if not user_data.full_name.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Full name cannot be empty",
            )

    if user_data.designation is not None:
        if not user_data.designation.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Designation cannot be empty",
            )

    if user_data.password is not None:
        if not user_data.password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password cannot be empty",
            )

    if user_data.email is not None:
        existing_email = db.scalar(
            select(User).where(
                User.email == user_data.email,
                User.employee_id != employee_id,
            )
        )

        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already exists",
            )

    if user_data.role_id is not None:
        role = db.scalar(
            select(Role).where(
                Role.id == user_data.role_id
            )
        )

        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role not found",
            )

        if not role.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Role is inactive",
            )

    if user_data.organization_unit_id is not None:
        organization_unit = db.scalar(
            select(OrganizationUnit).where(
                OrganizationUnit.id
                == user_data.organization_unit_id
            )
        )

        if not organization_unit:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Organization unit not found",
            )

        if not organization_unit.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Organization unit is inactive",
            )

    try:
        if user_data.full_name is not None:
            user.full_name = user_data.full_name.strip()

        if user_data.designation is not None:
            user.designation = (
                user_data.designation.strip()
            )

        if user_data.email is not None:
            user.email = user_data.email

        if user_data.password is not None:
            user.password_hash = hash_password(
                user_data.password
            )

        if user_data.role_id is not None:
            user.role_id = user_data.role_id

        if user_data.organization_unit_id is not None:
            user.organization_unit_id = (
                user_data.organization_unit_id
            )

        if user_data.is_active is not None:
            user.is_active = user_data.is_active

        db.commit()
        db.refresh(user)

    except Exception:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user",
        )

    return user