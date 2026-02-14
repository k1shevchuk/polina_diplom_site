from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, Query, UploadFile, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.core.config import settings
from app.core.deps import require_roles
from app.db.session import get_db
from app.models.product import Product
from app.models.role import RoleName
from app.models.user import User
from app.schemas.common import MessageResponse, PaginationMeta
from app.schemas.product import ProductCreate, ProductOut, ProductUpdate
from app.services.product_service import (
    create_product,
    delete_or_archive_product,
    get_seller_product,
    submit_for_moderation,
    update_product,
)

router = APIRouter()


@router.get("", response_model=dict)
def seller_products(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    current_user: User = Depends(require_roles(RoleName.SELLER, RoleName.ADMIN)),
    db: Session = Depends(get_db),
):
    stmt = (
        select(Product)
        .options(selectinload(Product.images))
        .where(Product.seller_id == current_user.id)
        .order_by(Product.created_at.desc())
    )
    total = len(db.scalars(stmt).all())
    items = db.scalars(stmt.offset((page - 1) * page_size).limit(page_size)).all()
    return {
        "items": [ProductOut.model_validate(item).model_dump() for item in items],
        "meta": PaginationMeta(page=page, page_size=page_size, total=total).model_dump(),
    }


@router.post("", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def create_product_handler(
    payload: ProductCreate,
    current_user: User = Depends(require_roles(RoleName.SELLER, RoleName.ADMIN)),
    db: Session = Depends(get_db),
):
    product = create_product(db, current_user.id, payload.model_dump())
    return ProductOut.model_validate(product)


@router.put("/{product_id}", response_model=ProductOut)
def update_product_handler(
    product_id: int,
    payload: ProductUpdate,
    current_user: User = Depends(require_roles(RoleName.SELLER, RoleName.ADMIN)),
    db: Session = Depends(get_db),
):
    product = get_seller_product(db, current_user.id, product_id)
    updated = update_product(db, product, payload.model_dump(exclude_unset=True))
    return ProductOut.model_validate(updated)


@router.get("/{product_id}", response_model=ProductOut)
def seller_product_detail(
    product_id: int,
    current_user: User = Depends(require_roles(RoleName.SELLER, RoleName.ADMIN)),
    db: Session = Depends(get_db),
):
    product = get_seller_product(db, current_user.id, product_id)
    return ProductOut.model_validate(product)


@router.post("/{product_id}/submit", response_model=ProductOut)
def submit_product(
    product_id: int,
    current_user: User = Depends(require_roles(RoleName.SELLER, RoleName.ADMIN)),
    db: Session = Depends(get_db),
):
    product = get_seller_product(db, current_user.id, product_id)
    submitted = submit_for_moderation(db, product)
    return ProductOut.model_validate(submitted)


@router.delete("/{product_id}", response_model=MessageResponse)
def delete_product(
    product_id: int,
    hard_delete: bool = Query(default=False),
    current_user: User = Depends(require_roles(RoleName.SELLER, RoleName.ADMIN)),
    db: Session = Depends(get_db),
):
    delete_or_archive_product(db, current_user.id, product_id, hard_delete=hard_delete)
    return MessageResponse(message="Product removed")


@router.post("/upload-image", response_model=dict, status_code=status.HTTP_201_CREATED)
async def upload_product_image(
    file: UploadFile = File(...),
    current_user: User = Depends(require_roles(RoleName.SELLER, RoleName.ADMIN)),
):
    _ = current_user
    suffix = Path(file.filename).suffix.lower() if file.filename else ".jpg"
    filename = f"{uuid4().hex}{suffix}"
    target = settings.media_root / "products"
    target.mkdir(parents=True, exist_ok=True)
    out_path = target / filename

    content = await file.read()
    out_path.write_bytes(content)
    return {"url": f"{settings.media_url}/products/{filename}"}
