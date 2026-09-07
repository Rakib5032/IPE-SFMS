from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import (
    check_line_access,
    get_current_user,
    get_db,
)
from app.models.layout import Layout
from app.models.line import Line
from app.models.user import User
from app.schemas.layout import (
    LayoutCreate,
    LayoutResponse,
    LayoutUpdate,
)
from app.services import layout_service


router = APIRouter(
    prefix="/layouts",
    tags=["Layouts"],
)


@router.post(
    "/",
    response_model=LayoutResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_layout(
    data: LayoutCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    line = db.get(Line, data.line_id)

    if not line:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Line not found",
        )

    check_line_access(
        line_id=data.line_id,
        current_user=current_user,
        db=db,
    )

    return layout_service.create_layout(
        db=db,
        line_id=data.line_id,
        style=data.style,
        job=data.job,
        buyer=data.buyer,
        smv=data.smv,
        required_machine_count=data.required_machine_count,
        total_machines=data.total_machines,
        machine_status=data.machine_status,
        status=data.status,
        notes=data.notes,
    )


@router.get(
    "/line/{line_id}",
    response_model=list[LayoutResponse],
)
def get_line_layouts(
    line_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    line = db.get(Line, line_id)

    if not line:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Line not found",
        )

    check_line_access(
        line_id=line_id,
        current_user=current_user,
        db=db,
    )

    return layout_service.get_line_layouts(
        db=db,
        line_id=line_id,
    )


@router.get(
    "/line/{line_id}/active",
    response_model=LayoutResponse | None,
)
def get_active_layout(
    line_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    line = db.get(Line, line_id)

    if not line:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Line not found",
        )

    check_line_access(
        line_id=line_id,
        current_user=current_user,
        db=db,
    )

    return layout_service.get_active_layout(
        db=db,
        line_id=line_id,
    )


@router.get(
    "/{layout_id}",
    response_model=LayoutResponse,
)
def get_layout(
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

    return layout


@router.put(
    "/{layout_id}",
    response_model=LayoutResponse,
)
def update_layout(
    layout_id: int,
    data: LayoutUpdate,
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

    return layout_service.update_layout(
        db=db,
        layout=layout,
        style=data.style,
        job=data.job,
        buyer=data.buyer,
        smv=data.smv,
        required_machine_count=data.required_machine_count,
        total_machines=data.total_machines,
        machine_status=data.machine_status,
        status=data.status,
        completed_at=data.completed_at,
        duration_minutes=data.duration_minutes,
        is_active=data.is_active,
        notes=data.notes,
    )


@router.post(
    "/{layout_id}/complete",
    response_model=LayoutResponse,
)
def complete_layout(
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

    return layout_service.complete_layout(
        db=db,
        layout=layout,
    )