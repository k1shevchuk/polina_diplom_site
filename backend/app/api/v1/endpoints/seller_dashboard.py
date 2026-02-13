from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.deps import require_roles
from app.db.session import get_db
from app.models.order import Order
from app.models.product import Product
from app.models.role import RoleName
from app.models.user import User

router = APIRouter()


@router.get("")
def seller_dashboard(
    current_user: User = Depends(require_roles(RoleName.SELLER, RoleName.ADMIN)),
    db: Session = Depends(get_db),
):
    products = db.scalar(select(func.count(Product.id)).where(Product.seller_id == current_user.id)) or 0
    orders = db.scalar(select(func.count(Order.id)).where(Order.seller_id == current_user.id)) or 0
    return {"products": products, "orders": orders}
