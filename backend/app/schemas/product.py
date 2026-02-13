from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field

from app.models.product import ProductStatus
from app.schemas.common import BaseSchema


class ProductImageOut(BaseSchema):
    id: int
    image_url: str
    sort_order: int


class ProductBase(BaseModel):
    title: str = Field(min_length=2, max_length=255)
    description: str = Field(min_length=10, max_length=5000)
    price: Decimal = Field(gt=0)
    stock: int | None = Field(default=None, ge=0)
    category_id: int | None = None
    tags: list[str] = Field(default_factory=list)
    materials: list[str] = Field(default_factory=list)


class ProductCreate(ProductBase):
    image_urls: list[str] = Field(default_factory=list)


class ProductUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=2, max_length=255)
    description: str | None = Field(default=None, min_length=10, max_length=5000)
    price: Decimal | None = Field(default=None, gt=0)
    stock: int | None = Field(default=None, ge=0)
    category_id: int | None = None
    tags: list[str] | None = None
    materials: list[str] | None = None
    image_urls: list[str] | None = None
    status: ProductStatus | None = None


class ProductOut(BaseSchema):
    id: int
    seller_id: int
    title: str
    description: str
    price: Decimal
    stock: int | None
    category_id: int | None
    tags: list[str]
    materials: list[str]
    status: ProductStatus
    rejection_reason: str | None
    created_at: datetime
    images: list[ProductImageOut]


class ProductModerationRequest(BaseModel):
    approve: bool
    reason: str | None = None
