from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.dependencies import (
    check_line_access,
    get_current_user,
    get_db,
)
from app.models.layout import Layout
from app.models.layout_machine import LayoutMachine
from app.models.user import User
from app.schemas.layout_machine import (
    LayoutMachineCreate,
    LayoutMachineResponse,
    LayoutMachineUpdate,
)
from app.services import layout_machine_service


router = APIRouter(
    prefix="/layout-machines",
    tags=["Layout Machines"],
)


@router.post(
    "/",
    response_model=LayoutMachineResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_machine(
    data: LayoutMachineCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    layout = db.get(Layout, data.layout_id)

    if not layout:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Layout not found",
        )

    check_line_access(
        line_id=layout.line_id,
        current_user=current_user,
        db=db,
    )

    if data.status not in layout_machine_service.ALLOWED_STATUSES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Invalid status. Allowed values: "
                "PENDING, RUNNING, COMPLETED, OFF"
            ),
        )

    existing_machine = db.scalar(
    select(LayoutMachine)
    .where(
        LayoutMachine.layout_id == data.layout_id,
        LayoutMachine.machine_number == data.machine_number,
        )
    )

    if existing_machine:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Machine number already exists in this layout",
        )

    return layout_machine_service.create_machine(
        db=db,
        layout_id=data.layout_id,
        machine_number=data.machine_number,
        machine_name=data.machine_name,
        status=data.status,
        reason=data.reason,
    )


@router.get(
    "/layout/{layout_id}",
    response_model=list[LayoutMachineResponse],
)
def get_layout_machines(
    layout_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    layout = db.get(Layout, layout_id)

    if not layout:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Layout not found",
        )

    check_line_access(
        line_id=layout.line_id,
        current_user=current_user,
        db=db,
    )

    return layout_machine_service.get_layout_machines(
        db=db,
        layout_id=layout_id,
    )


@router.get(
    "/{machine_id}",
    response_model=LayoutMachineResponse,
)
def get_machine(
    machine_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    machine = db.get(LayoutMachine, machine_id)

    if not machine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Layout machine not found",
        )

    layout = db.get(Layout, machine.layout_id)

    if not layout:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Layout not found",
        )

    check_line_access(
        line_id=layout.line_id,
        current_user=current_user,
        db=db,
    )

    return machine


@router.put(
    "/{machine_id}",
    response_model=LayoutMachineResponse,
)
def update_machine(
    machine_id: int,
    data: LayoutMachineUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    machine = db.get(LayoutMachine, machine_id)

    if not machine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Layout machine not found",
        )

    layout = db.get(Layout, machine.layout_id)

    if not layout:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Layout not found",
        )

    check_line_access(
        line_id=layout.line_id,
        current_user=current_user,
        db=db,
    )

    if (
        data.status is not None
        and data.status not in layout_machine_service.ALLOWED_STATUSES
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Invalid status. Allowed values: "
                "PENDING, RUNNING, COMPLETED, OFF"
            ),
        )

    return layout_machine_service.update_machine(
        db=db,
        machine=machine,
        machine_name=data.machine_name,
        status=data.status,
        reason=data.reason,
        is_active=data.is_active,
    )