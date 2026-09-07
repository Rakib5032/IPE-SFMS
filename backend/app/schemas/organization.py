from datetime import datetime

from pydantic import BaseModel, ConfigDict


# ORGANIZATION UNIT


class OrganizationUnitBase(BaseModel):
    name: str
    code: str
    unit_type: str
    parent_id: int | None = None
    is_active: bool = True


class OrganizationUnitCreate(OrganizationUnitBase):
    pass


class OrganizationUnitUpdate(BaseModel):
    name: str | None = None
    code: str | None = None
    unit_type: str | None = None
    parent_id: int | None = None
    is_active: bool | None = None


class OrganizationUnitResponse(OrganizationUnitBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


# LINE


class LineCreate(BaseModel):
    line_number: int
    name: str
    organization_unit_id: int
    is_active: bool = True


class LineUpdate(BaseModel):
    line_number: int | None = None
    name: str | None = None
    organization_unit_id: int | None = None
    is_active: bool | None = None


class LineResponse(BaseModel):
    id: int
    line_number: int
    name: str
    organization_unit_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )