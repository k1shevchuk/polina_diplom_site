from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.db.session import get_db
from app.models.product import Product
from app.schemas.common import PaginationMeta
from app.schemas.product import ProductOut
from app.services.product_service import list_public_products

router = APIRouter()


@router.get("", response_model=dict)
def catalog_list(
    q: str | None = Query(default=None),
    category_id: int | None = Query(default=None),
    min_price: Decimal | None = Query(default=None),
    max_price: Decimal | None = Query(default=None),
    sort: str = Query(default="new"),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    items, total = list_public_products(db, q, category_id, min_price, max_price, sort, page, page_size)
    return {
        "items": [ProductOut.model_validate(item).model_dump() for item in items],
        "meta": PaginationMeta(page=page, page_size=page_size, total=total).model_dump(),
    }


@router.get("/{product_id}", response_model=ProductOut)
def product_detail(product_id: int, db: Session = Depends(get_db)):
    stmt = select(Product).options(selectinload(Product.images)).where(Product.id == product_id)
    product = db.scalar(stmt)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return ProductOut.model_validate(product)
