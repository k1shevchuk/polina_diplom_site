from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from app.models.role import RoleName


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class RefreshResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserMe(BaseModel):
    id: int
    email: EmailStr
    roles: list[RoleName]
    is_banned: bool
    is_active: bool


class RefreshCookieData(BaseModel):
    token: str
    expires_at: datetime
