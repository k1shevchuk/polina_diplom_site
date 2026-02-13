from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.core.deps import require_roles
from app.db.session import get_db
from app.models.notification import NotificationType
from app.models.product import Product
from app.models.role import RoleName
from app.models.user import User
from app.schemas.common import MessageResponse, PaginationMeta
from app.schemas.product import ProductModerationRequest, ProductOut
from app.services.admin_service import log_admin_action
from app.services.notification_service import create_notification
from app.services.product_service import admin_hide_or_delete_product, list_moderation_queue, moderate_product

router = APIRouter()


@router.get("", response_model=dict)
def moderation_queue(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    pending_only: bool = Query(default=False),
    current_admin: User = Depends(require_roles(RoleName.ADMIN)),
    db: Session = Depends(get_db),
):
    if pending_only:
        items, total = list_moderation_queue(db, page, page_size)
    else:
        stmt = select(Product).options(selectinload(Product.images)).order_by(Product.created_at.desc())
        total = len(db.scalars(stmt).all())
        items = db.scalars(stmt.offset((page - 1) * page_size).limit(page_size)).all()
    return {
        "items": [ProductOut.model_validate(item).model_dump() for item in items],
        "meta": PaginationMeta(page=page, page_size=page_size, total=total).model_dump(),
    }


@router.post("/{product_id}/moderate", response_model=ProductOut)
def moderate(
    product_id: int,
    payload: ProductModerationRequest,
    current_admin: User = Depends(require_roles(RoleName.ADMIN)),
    db: Session = Depends(get_db),
):
    product = moderate_product(db, product_id, payload.approve, payload.reason)

    create_notification(
        db,
        user_id=product.seller_id,
        notification_type=(NotificationType.PRODUCT_APPROVED if payload.approve else NotificationType.PRODUCT_REJECTED),
        payload={"product_id": product.id, "reason": payload.reason},
    )
    db.commit()

    log_admin_action(
        db,
        admin_user_id=current_admin.id,
        action="moderate_product",
        target_type="product",
        target_id=product.id,
        details={"approve": payload.approve, "reason": payload.reason},
    )
    return ProductOut.model_validate(product)


@router.delete("/{product_id}", response_model=MessageResponse)
def delete_or_hide(
    product_id: int,
    hard_delete: bool = Query(default=False),
    current_admin: User = Depends(require_roles(RoleName.ADMIN)),
    db: Session = Depends(get_db),
):
    admin_hide_or_delete_product(db, product_id, hard_delete=hard_delete)
    log_admin_action(
        db,
        admin_user_id=current_admin.id,
        action="delete_product" if hard_delete else "hide_product",
        target_type="product",
        target_id=product_id,
        details={"hard_delete": hard_delete},
    )
    return MessageResponse(message="Product updated")
