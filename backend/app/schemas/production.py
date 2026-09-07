from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


# ============================================================
# BASE
# ============================================================

class ProductionBase(BaseModel):
    line_id: int
    production_date: date
    quantity: int = 0
    target: int | None = None


# ============================================================
# CREATE
# ============================================================

class ProductionCreate(ProductionBase):
    pass


# ============================================================
# UPDATE
# ============================================================

class ProductionUpdate(BaseModel):
    quantity: int | None = None
    target: int | None = None


# ============================================================
# RESPONSE
# ============================================================

class ProductionResponse(ProductionBase):
    id: int

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )