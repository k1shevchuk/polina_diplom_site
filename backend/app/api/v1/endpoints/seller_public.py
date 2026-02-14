from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.db.session import get_db
from app.models.product import Product, ProductStatus
from app.models.role import RoleName
from app.models.user import User
from app.schemas.seller import SellerPublicOut, SellerPublicProductOut

router = APIRouter()


@router.get("/{seller_id}", response_model=SellerPublicOut)
def seller_public_profile(
    seller_id: int,
    limit: int = Query(default=24, ge=1, le=100),
    db: Session = Depends(get_db),
):
    seller = db.scalar(
        select(User)
        .options(selectinload(User.roles), selectinload(User.seller_profile))
        .where(User.id == seller_id)
    )
    if not seller:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Seller not found")

    products = db.scalars(
        select(Product)
        .options(selectinload(Product.images))
        .where(Product.seller_id == seller.id, Product.status == ProductStatus.ACTIVE)
        .order_by(Product.created_at.desc())
        .limit(limit)
    ).all()

    has_seller_role = any(role.name == RoleName.SELLER for role in seller.roles)
    if not has_seller_role and not seller.seller_profile and not products:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Seller not found")

    display_name = seller.seller_profile.display_name if seller.seller_profile else seller.email.split("@")[0]
    bio = seller.seller_profile.bio if seller.seller_profile else None

    product_rows = []
    for product in products:
        first_image = sorted(product.images, key=lambda image: image.sort_order)[0].image_url if product.images else None
        product_rows.append(
            SellerPublicProductOut(
                id=product.id,
                title=product.title,
                description=product.description,
                price=product.price,
                stock=product.stock,
                image_url=first_image,
            )
        )

    return SellerPublicOut(
        seller_id=seller.id,
        display_name=display_name,
        bio=bio,
        products=product_rows,
    )
