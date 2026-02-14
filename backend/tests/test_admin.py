from decimal import Decimal

from sqlalchemy import select

from app.models.admin_audit_log import AdminAuditLog
from app.models.order import Order, OrderItem, OrderStatus
from app.models.product import Product, ProductStatus
from app.models.review import Review
from app.models.role import RoleName


def auth_headers(client, email: str, password: str) -> dict[str, str]:
    response = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    assert response.status_code == 200
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_admin_users_list_and_ban_unban(client, db_session, create_user_factory):
    admin = create_user_factory("admin@example.com", "StrongPass123", [RoleName.ADMIN, RoleName.BUYER])
    target = create_user_factory("buyer@example.com", "StrongPass123", [RoleName.BUYER])
    headers = auth_headers(client, admin.email, "StrongPass123")

    list_response = client.get("/api/v1/admin/users", headers=headers)
    assert list_response.status_code == 200
    payload = list_response.json()
    found = next(item for item in payload if item["id"] == target.id)
    assert found["email"] == target.email
    assert found["roles"][0]["name"] == "BUYER"

    ban_response = client.post(f"/api/v1/admin/users/{target.id}/ban?is_banned=true", headers=headers)
    assert ban_response.status_code == 200
    assert ban_response.json()["is_banned"] is True

    unban_response = client.post(f"/api/v1/admin/users/{target.id}/ban?is_banned=false", headers=headers)
    assert unban_response.status_code == 200
    assert unban_response.json()["is_banned"] is False

    audit_rows = db_session.scalars(select(AdminAuditLog).where(AdminAuditLog.target_type == "user")).all()
    assert len(audit_rows) >= 2


def test_admin_can_moderate_edit_and_archive_product(client, db_session, create_user_factory):
    admin = create_user_factory("admin@example.com", "StrongPass123", [RoleName.ADMIN, RoleName.BUYER])
    seller = create_user_factory("seller@example.com", "StrongPass123", [RoleName.SELLER, RoleName.BUYER])
    headers = auth_headers(client, admin.email, "StrongPass123")

    pending_product = Product(
        seller_id=seller.id,
        title="Pending Cardigan",
        description="Warm knitted cardigan awaiting moderation",
        price=Decimal("5000.00"),
        stock=3,
        tags=["cardigan"],
        materials=["wool"],
        status=ProductStatus.PENDING,
    )
    active_product = Product(
        seller_id=seller.id,
        title="Active Scarf",
        description="Soft scarf ready for update and archive checks",
        price=Decimal("1900.00"),
        stock=5,
        tags=["scarf"],
        materials=["cotton"],
        status=ProductStatus.ACTIVE,
    )
    db_session.add_all([pending_product, active_product])
    db_session.commit()

    moderate_response = client.post(
        f"/api/v1/admin/products/{pending_product.id}/moderate",
        json={"approve": True, "reason": None},
        headers=headers,
    )
    assert moderate_response.status_code == 200
    assert moderate_response.json()["status"] == "ACTIVE"

    update_response = client.put(
        f"/api/v1/admin/products/{active_product.id}",
        json={"stock": 9, "title": "Updated Active Scarf"},
        headers=headers,
    )
    assert update_response.status_code == 200
    assert update_response.json()["stock"] == 9
    assert update_response.json()["title"] == "Updated Active Scarf"

    archive_response = client.delete(f"/api/v1/admin/products/{active_product.id}", headers=headers)
    assert archive_response.status_code == 200

    db_session.expire_all()
    refreshed = db_session.scalar(select(Product).where(Product.id == active_product.id))
    assert refreshed is not None
    assert refreshed.status == ProductStatus.ARCHIVED


def test_admin_can_hide_and_delete_reviews(client, db_session, create_user_factory):
    admin = create_user_factory("admin@example.com", "StrongPass123", [RoleName.ADMIN, RoleName.BUYER])
    buyer = create_user_factory("buyer@example.com", "StrongPass123", [RoleName.BUYER])
    seller = create_user_factory("seller@example.com", "StrongPass123", [RoleName.SELLER, RoleName.BUYER])
    headers = auth_headers(client, admin.email, "StrongPass123")

    product = Product(
        seller_id=seller.id,
        title="Review Product",
        description="Product to test review moderation endpoints",
        price=Decimal("1200.00"),
        stock=2,
        tags=["review"],
        materials=["wool"],
        status=ProductStatus.ACTIVE,
    )
    db_session.add(product)
    db_session.flush()

    order = Order(
        buyer_id=buyer.id,
        seller_id=seller.id,
        status=OrderStatus.COMPLETED,
        full_name="Buyer Test",
        phone="+7999000000",
        address="Moscow",
        comment=None,
        total_amount=Decimal("1200.00"),
    )
    db_session.add(order)
    db_session.flush()

    order_item = OrderItem(
        order_id=order.id,
        product_id=product.id,
        product_title_snapshot=product.title,
        product_price_snapshot=product.price,
        qty=1,
        subtotal=Decimal("1200.00"),
    )
    db_session.add(order_item)
    db_session.flush()

    review = Review(
        user_id=buyer.id,
        product_id=product.id,
        order_item_id=order_item.id,
        rating=5,
        text="Excellent quality and warm texture.",
    )
    db_session.add(review)
    db_session.commit()

    list_response = client.get("/api/v1/admin/reviews", headers=headers)
    assert list_response.status_code == 200
    assert any(item["id"] == review.id for item in list_response.json())

    hide_response = client.post(f"/api/v1/admin/reviews/{review.id}/hide?hidden=true", headers=headers)
    assert hide_response.status_code == 200
    assert hide_response.json()["is_hidden"] is True

    delete_response = client.delete(f"/api/v1/admin/reviews/{review.id}", headers=headers)
    assert delete_response.status_code == 200
    assert db_session.scalar(select(Review).where(Review.id == review.id)) is None


def test_non_admin_cannot_access_admin_endpoints(client, create_user_factory):
    buyer = create_user_factory("buyer@example.com", "StrongPass123", [RoleName.BUYER])
    headers = auth_headers(client, buyer.email, "StrongPass123")

    response = client.get("/api/v1/admin/users", headers=headers)
    assert response.status_code == 403
