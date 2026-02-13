from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.review import ReviewCreate, ReviewOut
from app.services.review_service import create_review, list_product_reviews

router = APIRouter()


@router.get("/product/{product_id}", response_model=list[ReviewOut])
def list_reviews(product_id: int, db: Session = Depends(get_db)):
    return [ReviewOut.model_validate(item) for item in list_product_reviews(db, product_id)]


@router.post("/product/{product_id}", response_model=ReviewOut)
def add_review(
    product_id: int,
    payload: ReviewCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    review = create_review(db, current_user.id, product_id, payload.rating, payload.text)
    return ReviewOut.model_validate(review)
