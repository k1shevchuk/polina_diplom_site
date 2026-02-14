from decimal import Decimal

from pydantic import BaseModel, Field

from app.schemas.common import BaseSchema


class SellerProfileOut(BaseSchema):
    seller_id: int
    display_name: str
    bio: str | None


class SellerProfileUpdate(BaseModel):
    display_name: str = Field(min_length=2, max_length=255)
    bio: str | None = Field(default=None, max_length=2000)


class SellerPublicProductOut(BaseSchema):
    id: int
    title: str
    description: str
    price: Decimal
    stock: int | None
    image_url: str | None


class SellerPublicOut(BaseSchema):
    seller_id: int
    display_name: str
    bio: str | None
    products: list[SellerPublicProductOut]
