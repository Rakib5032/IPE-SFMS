from datetime import datetime

from pydantic import BaseModel, ConfigDict


class LayoutMachineBase(BaseModel):
    machine_number: int
    machine_name: str | None = None
    status: str = "PENDING"
    reason: str | None = None
    is_active: bool = True


class LayoutMachineCreate(BaseModel):
    layout_id: int
    machine_number: int
    machine_name: str | None = None
    status: str = "PENDING"
    reason: str | None = None


class LayoutMachineUpdate(BaseModel):
    machine_name: str | None = None
    status: str | None = None
    reason: str | None = None
    is_active: bool | None = None


class LayoutMachineResponse(LayoutMachineBase):
    id: int
    layout_id: int
    started_at: datetime | None = None
    completed_at: datetime | None = None

    model_config = ConfigDict(
        from_attributes=True,
    )