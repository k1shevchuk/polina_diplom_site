from decimal import Decimal

from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.product import Product
from app.models.user import User
from app.schemas.cart import CartItemCreate, CartItemOut, CartItemUpdate, CartOut
from app.services.cart_service import add_to_cart, get_or_create_cart, remove_cart_item, update_cart_item

router = APIRouter()


def serialize_cart(cart) -> CartOut:
    items: list[CartItemOut] = []
    total = Decimal("0.00")
    for item in cart.items:
        product = item.product
        if not product:
            continue
        subtotal = Decimal(product.price) * item.qty
        total += subtotal
        items.append(
            CartItemOut(
                id=item.id,
                product_id=item.product_id,
                qty=item.qty,
                title=product.title,
                price=product.price,
                seller_id=product.seller_id,
            )
        )
    return CartOut(id=cart.id, user_id=cart.user_id, items=items, total_amount=total)


@router.get("", response_model=CartOut)
def get_cart(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    cart = get_or_create_cart(db, current_user.id)
    db.refresh(cart)
    for item in cart.items:
        db.refresh(item)
        item.product = db.scalar(select(Product).where(Product.id == item.product_id))
    return serialize_cart(cart)


@router.post("/items", response_model=CartOut, status_code=status.HTTP_201_CREATED)
def add_item(
    payload: CartItemCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    cart = add_to_cart(db, current_user.id, payload.product_id, payload.qty)
    db.refresh(cart)
    for item in cart.items:
        item.product = db.scalar(select(Product).where(Product.id == item.product_id))
    return serialize_cart(cart)


@router.put("/items/{item_id}", response_model=CartOut)
def update_item(
    item_id: int,
    payload: CartItemUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    cart = update_cart_item(db, current_user.id, item_id, payload.qty)
    db.refresh(cart)
    for item in cart.items:
        item.product = db.scalar(select(Product).where(Product.id == item.product_id))
    return serialize_cart(cart)


@router.delete("/items/{item_id}", response_model=CartOut)
def delete_item(item_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    cart = remove_cart_item(db, current_user.id, item_id)
    db.refresh(cart)
    for item in cart.items:
        item.product = db.scalar(select(Product).where(Product.id == item.product_id))
    return serialize_cart(cart)
