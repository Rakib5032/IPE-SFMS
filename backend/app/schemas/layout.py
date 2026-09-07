from datetime import datetime

from pydantic import BaseModel, ConfigDict


class LayoutBase(BaseModel):
    line_id: int

    style: str | None = None
    job: str | None = None
    buyer: str
    smv: float

    required_machine_count: int | None = None
    total_machines: int
    machine_status: dict

    status: str = "RUNNING"

    started_at: datetime
    completed_at: datetime | None = None

    duration_minutes: int | None = None

    is_active: bool | None = None
    notes: str | None = None


class LayoutCreate(BaseModel):
    line_id: int

    style: str | None = None
    job: str | None = None
    buyer: str
    smv: float

    required_machine_count: int | None = None
    total_machines: int
    machine_status: dict

    status: str = "RUNNING"

    notes: str | None = None


class LayoutUpdate(BaseModel):
    style: str | None = None
    job: str | None = None
    buyer: str | None = None
    smv: float | None = None

    required_machine_count: int | None = None
    total_machines: int | None = None
    machine_status: dict | None = None

    status: str | None = None

    completed_at: datetime | None = None
    duration_minutes: int | None = None

    is_active: bool | None = None
    notes: str | None = None


class LayoutResponse(LayoutBase):
    id: int

    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = ConfigDict(
        from_attributes=True,
    )