from __future__ import annotations

from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy import asc, desc, func, or_, select
from sqlalchemy.orm import Session, selectinload

from app.models.product import Product, ProductStatus
from app.models.product_image import ProductImage


def list_public_products(
    db: Session,
    q: str | None,
    category_id: int | None,
    min_price: Decimal | None,
    max_price: Decimal | None,
    sort: str,
    page: int,
    page_size: int,
) -> tuple[list[Product], int]:
    stmt = select(Product).options(selectinload(Product.images)).where(Product.status == ProductStatus.ACTIVE)

    if q:
        pattern = f"%{q.lower()}%"
        stmt = stmt.where(or_(func.lower(Product.title).like(pattern), func.lower(Product.description).like(pattern)))
    if category_id:
        stmt = stmt.where(Product.category_id == category_id)
    if min_price is not None:
        stmt = stmt.where(Product.price >= min_price)
    if max_price is not None:
        stmt = stmt.where(Product.price <= max_price)

    if sort == "price_asc":
        stmt = stmt.order_by(asc(Product.price))
    elif sort == "price_desc":
        stmt = stmt.order_by(desc(Product.price))
    elif sort == "popular":
        stmt = stmt.order_by(desc(Product.created_at))
    else:
        stmt = stmt.order_by(desc(Product.created_at))

    total = db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
    items = db.scalars(stmt.offset((page - 1) * page_size).limit(page_size)).unique().all()
    return items, total


def create_product(db: Session, seller_id: int, payload: dict) -> Product:
    image_urls = payload.pop("image_urls", [])
    product = Product(seller_id=seller_id, **payload)
    db.add(product)
    db.flush()
    for idx, image_url in enumerate(image_urls):
        db.add(ProductImage(product_id=product.id, image_url=image_url, sort_order=idx))
    db.commit()
    db.refresh(product)
    return product


def get_seller_product(db: Session, seller_id: int, product_id: int) -> Product:
    stmt = select(Product).options(selectinload(Product.images)).where(Product.id == product_id, Product.seller_id == seller_id)
    product = db.scalar(stmt)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product


def update_product(db: Session, product: Product, payload: dict) -> Product:
    image_urls = payload.pop("image_urls", None)
    for key, value in payload.items():
        setattr(product, key, value)
    if image_urls is not None:
        product.images.clear()
        for idx, image_url in enumerate(image_urls):
            product.images.append(ProductImage(image_url=image_url, sort_order=idx))
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def submit_for_moderation(db: Session, product: Product) -> Product:
    if product.status not in {ProductStatus.DRAFT, ProductStatus.REJECTED}:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only draft/rejected can be submitted")
    product.status = ProductStatus.PENDING
    product.rejection_reason = None
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def moderate_product(db: Session, product_id: int, approve: bool, reason: str | None) -> Product:
    stmt = select(Product).options(selectinload(Product.images)).where(Product.id == product_id)
    product = db.scalar(stmt)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    if product.status != ProductStatus.PENDING:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product is not pending")

    if approve:
        product.status = ProductStatus.ACTIVE
        product.rejection_reason = None
    else:
        product.status = ProductStatus.REJECTED
        product.rejection_reason = reason or "Rejected by moderator"

    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def list_moderation_queue(db: Session, page: int, page_size: int) -> tuple[list[Product], int]:
    stmt = select(Product).options(selectinload(Product.images)).where(Product.status == ProductStatus.PENDING)
    total = db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
    items = db.scalars(stmt.order_by(Product.created_at.asc()).offset((page - 1) * page_size).limit(page_size)).all()
    return items, total


def delete_or_archive_product(db: Session, seller_id: int, product_id: int, hard_delete: bool = False) -> None:
    product = db.scalar(select(Product).where(Product.id == product_id, Product.seller_id == seller_id))
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    if hard_delete:
        db.delete(product)
    else:
        product.status = ProductStatus.ARCHIVED
        db.add(product)
    db.commit()


def admin_hide_or_delete_product(db: Session, product_id: int, hard_delete: bool = False) -> None:
    product = db.scalar(select(Product).where(Product.id == product_id))
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    if hard_delete:
        db.delete(product)
    else:
        product.status = ProductStatus.ARCHIVED
        db.add(product)
    db.commit()
