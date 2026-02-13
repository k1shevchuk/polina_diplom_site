from __future__ import annotations

from collections import defaultdict
from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.cart import Cart, CartItem
from app.models.notification import NotificationType
from app.models.order import Order, OrderItem, OrderStatus
from app.models.product import Product, ProductStatus
from app.services.notification_service import create_notification


def checkout_cart(db: Session, buyer_id: int, payload: dict) -> list[Order]:
    cart = db.scalar(select(Cart).where(Cart.user_id == buyer_id))
    if not cart:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cart is empty")

    cart_items = db.scalars(select(CartItem).where(CartItem.cart_id == cart.id)).all()
    if not cart_items:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cart is empty")

    product_ids = [item.product_id for item in cart_items]
    products = db.scalars(select(Product).where(Product.id.in_(product_ids), Product.status == ProductStatus.ACTIVE)).all()
    product_map = {product.id: product for product in products}

    grouped: dict[int, list[CartItem]] = defaultdict(list)
    for item in cart_items:
        product = product_map.get(item.product_id)
        if not product:
            continue
        grouped[product.seller_id].append(item)

    if not grouped:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No active products in cart")

    created_orders: list[Order] = []
    for seller_id, items in grouped.items():
        order = Order(
            buyer_id=buyer_id,
            seller_id=seller_id,
            status=OrderStatus.REQUESTED,
            full_name=payload["full_name"],
            phone=payload["phone"],
            address=payload["address"],
            comment=payload.get("comment"),
            total_amount=Decimal("0.00"),
        )
        db.add(order)
        db.flush()

        total = Decimal("0.00")
        for item in items:
            product = product_map[item.product_id]
            subtotal = Decimal(product.price) * item.qty
            total += subtotal
            db.add(
                OrderItem(
                    order_id=order.id,
                    product_id=product.id,
                    product_title_snapshot=product.title,
                    product_price_snapshot=product.price,
                    qty=item.qty,
                    subtotal=subtotal,
                )
            )

        order.total_amount = total
        db.add(order)
        create_notification(
            db,
            user_id=seller_id,
            notification_type=NotificationType.NEW_ORDER,
            payload={"order_id": order.id, "buyer_id": buyer_id},
        )
        created_orders.append(order)

    for item in cart_items:
        db.delete(item)

    db.commit()

    for order in created_orders:
        db.refresh(order)
    return created_orders


def list_user_orders(db: Session, user_id: int, as_seller: bool = False) -> list[Order]:
    if as_seller:
        stmt = select(Order).where(Order.seller_id == user_id)
    else:
        stmt = select(Order).where(Order.buyer_id == user_id)
    return db.scalars(stmt.order_by(Order.created_at.desc())).all()


def update_order_status(db: Session, order_id: int, actor_id: int, next_status: OrderStatus, is_seller: bool) -> Order:
    order = db.scalar(select(Order).where(Order.id == order_id))
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    if is_seller:
        if order.seller_id != actor_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your order")
        allowed = {
            OrderStatus.REQUESTED: {OrderStatus.ACCEPTED, OrderStatus.REJECTED},
            OrderStatus.ACCEPTED: {OrderStatus.COMPLETED},
        }
    else:
        if order.buyer_id != actor_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your order")
        allowed = {
            OrderStatus.REQUESTED: {OrderStatus.CANCELED},
        }

    if next_status not in allowed.get(order.status, set()):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid status transition")

    order.status = next_status
    db.add(order)
    db.commit()
    db.refresh(order)
    return order
