from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.cart import Cart, CartItem
from app.models.product import Product, ProductStatus


def get_or_create_cart(db: Session, user_id: int) -> Cart:
    cart = db.scalar(select(Cart).options(selectinload(Cart.items)).where(Cart.user_id == user_id))
    if not cart:
        cart = Cart(user_id=user_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    return cart


def add_to_cart(db: Session, user_id: int, product_id: int, qty: int) -> Cart:
    product = db.scalar(select(Product).where(Product.id == product_id, Product.status == ProductStatus.ACTIVE))
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    cart = get_or_create_cart(db, user_id)
    item = db.scalar(select(CartItem).where(CartItem.cart_id == cart.id, CartItem.product_id == product_id))
    if item:
        item.qty = qty
        db.add(item)
    else:
        db.add(CartItem(cart_id=cart.id, product_id=product_id, qty=qty))
    db.commit()
    return get_or_create_cart(db, user_id)


def update_cart_item(db: Session, user_id: int, item_id: int, qty: int) -> Cart:
    cart = get_or_create_cart(db, user_id)
    item = db.scalar(select(CartItem).where(CartItem.id == item_id, CartItem.cart_id == cart.id))
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found")
    item.qty = qty
    db.add(item)
    db.commit()
    return get_or_create_cart(db, user_id)


def remove_cart_item(db: Session, user_id: int, item_id: int) -> Cart:
    cart = get_or_create_cart(db, user_id)
    item = db.scalar(select(CartItem).where(CartItem.id == item_id, CartItem.cart_id == cart.id))
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found")
    db.delete(item)
    db.commit()
    return get_or_create_cart(db, user_id)
