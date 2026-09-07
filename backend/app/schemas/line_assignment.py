from datetime import datetime

from pydantic import BaseModel, ConfigDict



# CREATE

class LineAssignmentCreate(BaseModel):
    employee_id: int
    line_id: int
    assignment_type: str = "PRIMARY"


# UPDATE

class LineAssignmentUpdate(BaseModel):
    assignment_type: str | None = None

# RESPONSE

class LineAssignmentResponse(BaseModel):
    id: int
    employee_id: int
    line_id: int
    assignment_type: str
    start_date: datetime
    end_date: datetime | None = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )