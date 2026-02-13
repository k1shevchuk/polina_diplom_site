from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.notification import NotificationType
from app.models.order import Order, OrderItem, OrderStatus
from app.models.review import Review
from app.services.notification_service import create_notification


def create_review(db: Session, user_id: int, product_id: int, rating: int, text: str) -> Review:
    order_item = db.scalar(
        select(OrderItem)
        .join(Order, Order.id == OrderItem.order_id)
        .where(
            Order.buyer_id == user_id,
            OrderItem.product_id == product_id,
            Order.status.in_([OrderStatus.ACCEPTED, OrderStatus.COMPLETED]),
        )
        .order_by(Order.id.desc())
    )
    if not order_item:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Purchase required for review")

    existing = db.scalar(select(Review).where(Review.order_item_id == order_item.id))
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Review already exists")

    review = Review(user_id=user_id, product_id=product_id, order_item_id=order_item.id, rating=rating, text=text)
    db.add(review)

    order = db.scalar(select(Order).where(Order.id == order_item.order_id))
    if order:
        create_notification(
            db,
            user_id=order.seller_id,
            notification_type=NotificationType.NEW_REVIEW,
            payload={"product_id": product_id, "review_user_id": user_id},
        )

    db.commit()
    db.refresh(review)
    return review


def list_product_reviews(db: Session, product_id: int) -> list[Review]:
    stmt = select(Review).where(Review.product_id == product_id, Review.is_hidden.is_(False)).order_by(Review.created_at.desc())
    return db.scalars(stmt).all()
