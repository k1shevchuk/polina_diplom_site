from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.favorite import Favorite
from app.models.product import Product, ProductStatus
from app.models.user import User
from app.schemas.common import MessageResponse

router = APIRouter()


@router.get("", response_model=list[int])
def list_favorites(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    rows = db.scalars(select(Favorite).where(Favorite.user_id == current_user.id)).all()
    return [row.product_id for row in rows]


@router.post("/{product_id}", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def add_favorite(product_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    product = db.scalar(select(Product).where(Product.id == product_id, Product.status == ProductStatus.ACTIVE))
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    exists = db.scalar(select(Favorite).where(Favorite.user_id == current_user.id, Favorite.product_id == product_id))
    if not exists:
        db.add(Favorite(user_id=current_user.id, product_id=product_id))
        db.commit()
    return MessageResponse(message="Added to favorites")


@router.delete("/{product_id}", response_model=MessageResponse)
def remove_favorite(product_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    row = db.scalar(select(Favorite).where(Favorite.user_id == current_user.id, Favorite.product_id == product_id))
    if row:
        db.delete(row)
        db.commit()
    return MessageResponse(message="Removed from favorites")
