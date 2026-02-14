from decimal import Decimal

from app.core.config import settings
from app.models.product import Product, ProductStatus
from app.models.role import RoleName
from app.models.seller_profile import SellerProfile


def test_catalog_lists_only_active_and_supports_filters(client, db_session):
    db_session.add_all(
        [
            Product(
                seller_id=1,
                title="Wooden Bowl",
                description="Handmade wooden bowl for kitchen and decor",
                price=Decimal("25.00"),
                status=ProductStatus.ACTIVE,
                tags=["wood"],
                materials=["oak"],
            ),
            Product(
                seller_id=1,
                title="Draft Item",
                description="Hidden draft",
                price=Decimal("30.00"),
                status=ProductStatus.DRAFT,
                tags=["test"],
                materials=["test"],
            ),
        ]
    )
    db_session.commit()

    response = client.get("/api/v1/catalog")
    assert response.status_code == 200
    data = response.json()
    assert data["meta"]["total"] == 1
    assert data["items"][0]["title"] == "Wooden Bowl"

    search = client.get("/api/v1/catalog?q=wooden")
    assert search.status_code == 200
    assert search.json()["meta"]["total"] == 1

    empty = client.get("/api/v1/catalog?min_price=100")
    assert empty.status_code == 200
    assert empty.json()["meta"]["total"] == 0


def test_seller_can_read_update_and_upload_product_images(client, db_session, create_user_factory):
    seller = create_user_factory("seller@example.com", "StrongPass123", [RoleName.SELLER, RoleName.BUYER])
    db_session.add(
        SellerProfile(
            user_id=seller.id,
            display_name="Seller Name",
            bio="Seller bio",
        )
    )
    product = Product(
        seller_id=seller.id,
        title="Draft Scarf",
        description="Draft scarf description for update test",
        price=Decimal("1900.00"),
        stock=4,
        status=ProductStatus.DRAFT,
        tags=["scarf"],
        materials=["wool"],
    )
    db_session.add(product)
    db_session.commit()

    login = client.post("/api/v1/auth/login", json={"email": seller.email, "password": "StrongPass123"})
    headers = {"Authorization": f"Bearer {login.json()['access_token']}"}

    detail = client.get(f"/api/v1/seller/products/{product.id}", headers=headers)
    assert detail.status_code == 200
    assert detail.json()["title"] == "Draft Scarf"

    update = client.put(
        f"/api/v1/seller/products/{product.id}",
        json={
            "title": "Updated Scarf",
            "description": "Updated scarf description with enough length",
            "price": "2100.00",
            "stock": 0,
            "tags": ["updated", "scarf"],
            "materials": ["cotton"],
        },
        headers=headers,
    )
    assert update.status_code == 200
    assert update.json()["stock"] == 0
    assert update.json()["title"] == "Updated Scarf"

    upload = client.post(
        "/api/v1/seller/products/upload-image",
        headers=headers,
        files={"file": ("scarf.jpg", b"fake-image", "image/jpeg")},
    )
    assert upload.status_code == 201
    image_url = upload.json()["url"]
    assert image_url.startswith("/media/products/")

    filename = image_url.split("/")[-1]
    saved_path = settings.media_root / "products" / filename
    assert saved_path.exists()
    saved_path.unlink(missing_ok=True)


def test_public_seller_profile_returns_active_products(client, db_session, create_user_factory):
    seller = create_user_factory("seller@example.com", "StrongPass123", [RoleName.SELLER, RoleName.BUYER])
    db_session.add(
        SellerProfile(
            user_id=seller.id,
            display_name="Seller Public",
            bio="Public bio",
        )
    )
    db_session.add_all(
        [
            Product(
                seller_id=seller.id,
                title="Public Product",
                description="Visible product in public seller profile",
                price=Decimal("1000.00"),
                stock=2,
                status=ProductStatus.ACTIVE,
                tags=["public"],
                materials=["wool"],
            ),
            Product(
                seller_id=seller.id,
                title="Hidden Product",
                description="Hidden draft product in public profile",
                price=Decimal("1000.00"),
                stock=2,
                status=ProductStatus.DRAFT,
                tags=["hidden"],
                materials=["wool"],
            ),
        ]
    )
    db_session.commit()

    response = client.get(f"/api/v1/sellers/{seller.id}")
    assert response.status_code == 200
    payload = response.json()
    assert payload["display_name"] == "Seller Public"
    assert len(payload["products"]) == 1
    assert payload["products"][0]["title"] == "Public Product"
