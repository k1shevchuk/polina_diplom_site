from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.core.deps import require_roles
from app.db.session import get_db
from app.models.role import RoleName
from app.models.user import User
from app.schemas.user import UserOut
from app.services.admin_service import log_admin_action
from app.services.auth_service import revoke_all_refresh_tokens_for_user

router = APIRouter()


@router.get("", response_model=list[UserOut])
def list_users(
    current_admin: User = Depends(require_roles(RoleName.ADMIN)),
    db: Session = Depends(get_db),
):
    rows = db.scalars(select(User).options(selectinload(User.roles)).order_by(User.created_at.desc())).all()
    return [UserOut.model_validate(row) for row in rows]


@router.post("/{user_id}/ban", response_model=UserOut)
def ban_user(
    user_id: int,
    is_banned: bool = True,
    current_admin: User = Depends(require_roles(RoleName.ADMIN)),
    db: Session = Depends(get_db),
):
    user = db.scalar(select(User).options(selectinload(User.roles)).where(User.id == user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user.is_banned = is_banned
    db.add(user)
    db.commit()
    db.refresh(user)
    if is_banned:
        revoke_all_refresh_tokens_for_user(db, user.id)
    log_admin_action(
        db,
        admin_user_id=current_admin.id,
        action="ban_user" if is_banned else "unban_user",
        target_type="user",
        target_id=user_id,
        details={"is_banned": is_banned},
    )
    return UserOut.model_validate(user)
