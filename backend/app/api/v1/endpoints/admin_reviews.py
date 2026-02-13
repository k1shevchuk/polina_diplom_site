from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.deps import require_roles
from app.db.session import get_db
from app.models.review import Review
from app.models.role import RoleName
from app.models.user import User
from app.schemas.review import ReviewOut
from app.services.admin_service import log_admin_action

router = APIRouter()


@router.get("", response_model=list[ReviewOut])
def list_reviews(
    current_admin: User = Depends(require_roles(RoleName.ADMIN)),
    db: Session = Depends(get_db),
):
    rows = db.scalars(select(Review).order_by(Review.created_at.desc())).all()
    return [ReviewOut.model_validate(row) for row in rows]


@router.post("/{review_id}/hide", response_model=ReviewOut)
def hide_review(
    review_id: int,
    hidden: bool = True,
    current_admin: User = Depends(require_roles(RoleName.ADMIN)),
    db: Session = Depends(get_db),
):
    row = db.scalar(select(Review).where(Review.id == review_id))
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
    row.is_hidden = hidden
    db.add(row)
    db.commit()
    db.refresh(row)
    log_admin_action(
        db,
        admin_user_id=current_admin.id,
        action="hide_review" if hidden else "unhide_review",
        target_type="review",
        target_id=review_id,
        details={"hidden": hidden},
    )
    return ReviewOut.model_validate(row)


@router.delete("/{review_id}")
def delete_review(
    review_id: int,
    current_admin: User = Depends(require_roles(RoleName.ADMIN)),
    db: Session = Depends(get_db),
):
    row = db.scalar(select(Review).where(Review.id == review_id))
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
    db.delete(row)
    db.commit()
    log_admin_action(
        db,
        admin_user_id=current_admin.id,
        action="delete_review",
        target_type="review",
        target_id=review_id,
        details={},
    )
    return {"message": "Review deleted"}
