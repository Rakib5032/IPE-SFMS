from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    employee_id: int
    full_name: str
    designation: str | None = None
    email: EmailStr | None = None
    password: str
    role_id: int
    organization_unit_id: int | None = None


class UserUpdate(BaseModel):
    full_name: str
    designation: str | None = None
    email: EmailStr | None = None
    role_id: int
    organization_unit_id: int | None = None
    is_active: bool


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