from __future__ import annotations

from fastapi import APIRouter, Depends, Request, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.deps import get_client_ip, get_current_user, get_user_agent
from app.db.session import get_db
from app.models.role import Role, RoleName
from app.models.user import User
from app.schemas.auth import LoginRequest, RefreshResponse, RegisterRequest, TokenResponse, UserMe
from app.schemas.common import MessageResponse
from app.services import auth_service

router = APIRouter()


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, response: Response, request: Request, db: Session = Depends(get_db)):
    user = auth_service.register_user(db, payload.email, payload.password)
    access_token = auth_service.issue_tokens(
        db,
        user,
        response=response,
        user_agent=get_user_agent(request),
        ip=get_client_ip(request),
    )
    return TokenResponse(access_token=access_token)


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, response: Response, request: Request, db: Session = Depends(get_db)):
    user = auth_service.authenticate_user(db, payload.email, payload.password)
    access_token = auth_service.issue_tokens(
        db,
        user,
        response=response,
        user_agent=get_user_agent(request),
        ip=get_client_ip(request),
    )
    return TokenResponse(access_token=access_token)


@router.post("/refresh", response_model=RefreshResponse)
def refresh(request: Request, response: Response, db: Session = Depends(get_db)):
    token = request.cookies.get("refresh_token")
    access_token = auth_service.refresh_access_token(db, token, response)
    return RefreshResponse(access_token=access_token)


@router.post("/logout", response_model=MessageResponse)
def logout(request: Request, response: Response, db: Session = Depends(get_db)):
    token = request.cookies.get("refresh_token")
    auth_service.revoke_refresh_token(db, token)
    response.delete_cookie("refresh_token", path="/api/v1/auth")
    return MessageResponse(message="Logged out")


@router.get("/me", response_model=UserMe)
def me(current_user: User = Depends(get_current_user)):
    return UserMe(
        id=current_user.id,
        email=current_user.email,
        roles=[role.name for role in current_user.roles],
        is_banned=current_user.is_banned,
        is_active=current_user.is_active,
    )


@router.post("/roles/seller", response_model=UserMe)
def toggle_seller_role(
    enabled: bool = True,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    auth_service.ensure_system_roles(db)
    seller_role = next((role for role in current_user.roles if role.name == RoleName.SELLER), None)
    if enabled and not seller_role:
        role_row = db.scalar(select(Role).where(Role.name == RoleName.SELLER))
        current_user.roles.append(role_row)
    elif not enabled and seller_role:
        current_user.roles = [role for role in current_user.roles if role.name != RoleName.SELLER]
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return UserMe(
        id=current_user.id,
        email=current_user.email,
        roles=[role.name for role in current_user.roles],
        is_banned=current_user.is_banned,
        is_active=current_user.is_active,
    )
