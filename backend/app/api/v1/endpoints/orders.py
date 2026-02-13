from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.core.deps import get_current_user, require_roles
from app.db.session import get_db
from app.models.order import Order
from app.models.role import RoleName
from app.models.user import User
from app.schemas.order import CheckoutRequest, CheckoutResponse, OrderOut, OrderStatusUpdate
from app.services.checkout_service import checkout_cart, list_user_orders, update_order_status

router = APIRouter()


@router.post("/checkout", response_model=CheckoutResponse, status_code=status.HTTP_201_CREATED)
def checkout(payload: CheckoutRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    orders = checkout_cart(db, current_user.id, payload.model_dump())
    hydrated: list[Order] = []
    for order in orders:
        row = db.scalar(select(Order).options(selectinload(Order.items)).where(Order.id == order.id))
        hydrated.append(row)
    return CheckoutResponse(orders=[OrderOut.model_validate(order) for order in hydrated], total_orders=len(hydrated))


@router.get("/my", response_model=list[OrderOut])
def buyer_orders(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    orders = list_user_orders(db, current_user.id, as_seller=False)
    result = []
    for order in orders:
        row = db.scalar(select(Order).options(selectinload(Order.items)).where(Order.id == order.id))
        result.append(OrderOut.model_validate(row))
    return result


@router.get("/seller", response_model=list[OrderOut])
def seller_orders(
    current_user: User = Depends(require_roles(RoleName.SELLER, RoleName.ADMIN)),
    db: Session = Depends(get_db),
):
    orders = list_user_orders(db, current_user.id, as_seller=True)
    result = []
    for order in orders:
        row = db.scalar(select(Order).options(selectinload(Order.items)).where(Order.id == order.id))
        result.append(OrderOut.model_validate(row))
    return result


@router.patch("/{order_id}/status", response_model=OrderOut)
def update_status(
    order_id: int,
    payload: OrderStatusUpdate,
    as_seller: bool = False,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    order = update_order_status(db, order_id, current_user.id, payload.status, is_seller=as_seller)
    row = db.scalar(select(Order).options(selectinload(Order.items)).where(Order.id == order.id))
    return OrderOut.model_validate(row)
