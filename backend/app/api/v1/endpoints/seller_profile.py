from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.deps import require_roles
from app.db.session import get_db
from app.models.role import RoleName
from app.models.seller_profile import SellerProfile
from app.models.user import User
from app.schemas.seller import SellerProfileOut, SellerProfileUpdate

router = APIRouter()


def _get_or_create_profile(db: Session, user: User) -> SellerProfile:
    profile = db.scalar(select(SellerProfile).where(SellerProfile.user_id == user.id))
    if profile:
        return profile

    profile = SellerProfile(
        user_id=user.id,
        display_name=user.email.split("@")[0],
        bio=None,
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


@router.get("", response_model=SellerProfileOut)
def get_seller_profile(
    current_user: User = Depends(require_roles(RoleName.SELLER, RoleName.ADMIN)),
    db: Session = Depends(get_db),
):
    profile = _get_or_create_profile(db, current_user)
    return SellerProfileOut(
        seller_id=current_user.id,
        display_name=profile.display_name,
        bio=profile.bio,
    )


@router.put("", response_model=SellerProfileOut)
def update_seller_profile(
    payload: SellerProfileUpdate,
    current_user: User = Depends(require_roles(RoleName.SELLER, RoleName.ADMIN)),
    db: Session = Depends(get_db),
):
    profile = _get_or_create_profile(db, current_user)
    profile.display_name = payload.display_name
    profile.bio = payload.bio
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return SellerProfileOut(
        seller_id=current_user.id,
        display_name=profile.display_name,
        bio=profile.bio,
    )
