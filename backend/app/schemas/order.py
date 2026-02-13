from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field

from app.models.order import OrderStatus
from app.schemas.common import BaseSchema


class CheckoutRequest(BaseModel):
    full_name: str = Field(min_length=2, max_length=255)
    phone: str = Field(min_length=5, max_length=50)
    address: str = Field(min_length=5, max_length=1000)
    comment: str | None = Field(default=None, max_length=1000)


class OrderItemOut(BaseSchema):
    id: int
    product_id: int | None
    product_title_snapshot: str
    product_price_snapshot: Decimal
    qty: int
    subtotal: Decimal


class OrderOut(BaseSchema):
    id: int
    buyer_id: int
    seller_id: int
    status: OrderStatus
    full_name: str
    phone: str
    address: str
    comment: str | None
    total_amount: Decimal
    created_at: datetime
    items: list[OrderItemOut]


class CheckoutResponse(BaseModel):
    orders: list[OrderOut]
    total_orders: int


class OrderStatusUpdate(BaseModel):
    status: OrderStatus
