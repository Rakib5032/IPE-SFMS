from datetime import datetime

from pydantic import BaseModel, ConfigDict


# ============================================================
# CREATE
# ============================================================

class LineStatusCreate(BaseModel):
    line_id: int
    status: str
    reason: str | None = None


# ============================================================
# UPDATE
# ============================================================

class LineStatusUpdate(BaseModel):
    status: str | None = None
    reason: str | None = None
    ended_at: datetime | None = None


# ============================================================
# RESPONSE
# ============================================================

class LineStatusResponse(BaseModel):
    id: int
    line_id: int
    status: str
    reason: str | None = None
    started_at: datetime
    ended_at: datetime | None = None
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )