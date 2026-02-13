from decimal import Decimal

from sqlalchemy import select

from app.models.cart import Cart, CartItem
from app.models.notification import Notification
from app.models.product import Product, ProductStatus
from app.models.role import RoleName


def test_checkout_splits_orders_by_seller(client, db_session, create_user_factory):
    buyer = create_user_factory("buyer@example.com", "StrongPass123", [RoleName.BUYER])
    seller1 = create_user_factory("seller1@example.com", "StrongPass123", [RoleName.BUYER, RoleName.SELLER])
    seller2 = create_user_factory("seller2@example.com", "StrongPass123", [RoleName.BUYER, RoleName.SELLER])

    p1 = Product(
        seller_id=seller1.id,
        title="Bag",
        description="Handmade bag with leather handles",
        price=Decimal("50.00"),
        status=ProductStatus.ACTIVE,
        tags=["bag"],
        materials=["leather"],
    )
    p2 = Product(
        seller_id=seller2.id,
        title="Scarf",
        description="Warm knitted scarf",
        price=Decimal("20.00"),
        status=ProductStatus.ACTIVE,
        tags=["scarf"],
        materials=["wool"],
    )
    db_session.add_all([p1, p2])
    db_session.commit()

    login = client.post("/api/v1/auth/login", json={"email": buyer.email, "password": "StrongPass123"})
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    add_first = client.post("/api/v1/cart/items", json={"product_id": p1.id, "qty": 1}, headers=headers)
    assert add_first.status_code == 201
    add_second = client.post("/api/v1/cart/items", json={"product_id": p2.id, "qty": 2}, headers=headers)
    assert add_second.status_code == 201

    checkout = client.post(
        "/api/v1/orders/checkout",
        json={"full_name": "Buyer Test", "phone": "+7000000000", "address": "Moscow", "comment": "call me"},
        headers=headers,
    )
    assert checkout.status_code == 201
    payload = checkout.json()
    assert payload["total_orders"] == 2

    cart = db_session.scalar(select(Cart).where(Cart.user_id == buyer.id))
    assert cart is not None
    remaining_items = db_session.scalars(select(CartItem).where(CartItem.cart_id == cart.id)).all()
    assert remaining_items == []

    notifications = db_session.scalars(select(Notification)).all()
    assert len(notifications) == 2
