from datetime import datetime

from pydantic import BaseModel, EmailStr

from app.models.role import RoleName
from app.schemas.common import BaseSchema


class RoleOut(BaseSchema):
    id: int
    name: RoleName


class UserOut(BaseSchema):
    id: int
    email: EmailStr
    is_active: bool
    is_banned: bool
    roles: list[RoleOut]
    created_at: datetime


class BanRequest(BaseModel):
    is_banned: bool


class ToggleSellerRequest(BaseModel):
    enabled: bool = True
