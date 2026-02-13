from decimal import Decimal

from pydantic import BaseModel, Field


class CartItemCreate(BaseModel):
    product_id: int
    qty: int = Field(default=1, ge=1, le=99)


class CartItemUpdate(BaseModel):
    qty: int = Field(ge=1, le=99)


class CartItemOut(BaseModel):
    id: int
    product_id: int
    qty: int
    title: str
    price: Decimal
    seller_id: int


class CartOut(BaseModel):
    id: int
    user_id: int
    items: list[CartItemOut]
    total_amount: Decimal
