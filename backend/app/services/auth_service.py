from __future__ import annotations

from datetime import UTC, datetime

from fastapi import HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.core.config import settings
from app.core.security import (
    create_access_token,
    hash_password,
    hash_refresh_token,
    new_refresh_token,
    refresh_token_expiry,
    verify_password,
)
from app.models.refresh_token import RefreshToken
from app.models.role import Role, RoleName
from app.models.user import User


def ensure_system_roles(db: Session) -> None:
    existing = {role.name for role in db.scalars(select(Role)).all()}
    for role_name in RoleName:
        if role_name not in existing:
            db.add(Role(name=role_name))
    db.commit()


def register_user(db: Session, email: str, password: str) -> User:
    ensure_system_roles(db)
    existing = db.scalar(select(User).where(User.email == email))
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    buyer_role = db.scalar(select(Role).where(Role.name == RoleName.BUYER))
    if not buyer_role:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Role setup failed")

    user = User(email=email, password_hash=hash_password(password), roles=[buyer_role])
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str) -> User:
    stmt = select(User).options(selectinload(User.roles)).where(User.email == email)
    user = db.scalar(stmt)
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    if user.is_banned:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is banned")
    return user


def issue_tokens(db: Session, user: User, response: Response, user_agent: str | None, ip: str | None) -> str:
    access_token = create_access_token(str(user.id))
    refresh_token = new_refresh_token()
    refresh_row = RefreshToken(
        user_id=user.id,
        token_hash=hash_refresh_token(refresh_token),
        expires_at=refresh_token_expiry(),
        user_agent=user_agent,
        ip_address=ip,
    )
    db.add(refresh_row)
    db.commit()

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=settings.app_env != "development",
        samesite="lax",
        max_age=settings.refresh_token_expire_days * 24 * 60 * 60,
        path="/api/v1/auth",
    )
    return access_token


def refresh_access_token(db: Session, refresh_token: str | None, response: Response) -> str:
    _ = response
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing refresh token")

    hashed = hash_refresh_token(refresh_token)
    token_row = db.scalar(select(RefreshToken).where(RefreshToken.token_hash == hashed))
    if not token_row or token_row.revoked_at is not None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    expires_at = token_row.expires_at
    now = datetime.now(UTC) if expires_at.tzinfo is not None else datetime.now()
    if expires_at < now:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token expired")

    user = db.scalar(select(User).where(User.id == token_row.user_id))
    if not user or user.is_banned:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User unavailable")

    return create_access_token(str(user.id))


def revoke_refresh_token(db: Session, refresh_token: str | None) -> None:
    if not refresh_token:
        return
    hashed = hash_refresh_token(refresh_token)
    token_row = db.scalar(select(RefreshToken).where(RefreshToken.token_hash == hashed))
    if token_row and token_row.revoked_at is None:
        token_row.revoked_at = datetime.now(UTC)
        db.add(token_row)
        db.commit()


def revoke_all_refresh_tokens_for_user(db: Session, user_id: int) -> None:
    rows = db.scalars(select(RefreshToken).where(RefreshToken.user_id == user_id, RefreshToken.revoked_at.is_(None))).all()
    now = datetime.now(UTC)
    for row in rows:
        row.revoked_at = now
    if rows:
        db.commit()
