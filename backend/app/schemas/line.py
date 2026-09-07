from datetime import datetime

from pydantic import BaseModel, ConfigDict


# ============================================================
# BASE
# ============================================================

class LineBase(BaseModel):
    line_number: int
    name: str
    organization_unit_id: int
    is_active: bool = True


# ============================================================
# CREATE
# ============================================================

class LineCreate(LineBase):
    pass


# ============================================================
# UPDATE
# ============================================================

class LineUpdate(BaseModel):
    line_number: int | None = None
    name: str | None = None
    organization_unit_id: int | None = None
    is_active: bool | None = None


# ============================================================
# RESPONSE
# ============================================================

class LineResponse(LineBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )