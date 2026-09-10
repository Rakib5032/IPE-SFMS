from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    employee_id: int
    full_name: str
    designation: str | None = None
    email: EmailStr | None = None
    password: str
    role_id: int
    organization_unit_id: int | None = None


class UserUpdate(BaseModel):
    full_name: str | None = None
    designation: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    role_id: int | None = Field(
        default=None,
        gt=0,
    )
    organization_unit_id: int | None = Field(
        default=None,
        gt=0,
    )
    is_active: bool | None = None


class UserResponse(BaseModel):
    employee_id: int
    username: str
    full_name: str
    designation: str | None
    email: str | None
    role_id: int
    organization_unit_id: int | None
    is_active: bool

    class Config:
        from_attributes = True