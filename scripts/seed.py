from __future__ import annotations

from decimal import Decimal

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import hash_password
from app.models import (
    Category,
    Conversation,
    Message,
    Notification,
    NotificationType,
    Order,
    OrderItem,
    OrderStatus,
    Product,
    ProductImage,
    ProductStatus,
    Review,
    Role,
    RoleName,
    SellerProfile,
    User,
)


def run_seed() -> None:
    engine = create_engine(settings.database_url, future=True)
    with Session(engine) as db:
        existing_admin = db.scalar(select(User).where(User.email == "admin@example.com"))
        if existing_admin:
            print("Seed already exists")
            return

        roles = {}
        for role_name in RoleName:
            role = db.scalar(select(Role).where(Role.name == role_name))
            if not role:
                role = Role(name=role_name)
                db.add(role)
                db.flush()
            roles[role_name] = role

        admin = User(email="admin@example.com", password_hash=hash_password("Admin12345"), roles=[roles[RoleName.ADMIN], roles[RoleName.BUYER]])
        seller = User(email="seller@example.com", password_hash=hash_password("Seller12345"), roles=[roles[RoleName.SELLER], roles[RoleName.BUYER]])
        buyer = User(email="buyer@example.com", password_hash=hash_password("Buyer12345"), roles=[roles[RoleName.BUYER]])
        db.add_all([admin, seller, buyer])
        db.flush()

        db.add(SellerProfile(user_id=seller.id, display_name="Мастер Лиза", bio="Делаю керамику и текстиль"))

        cat_ceramic = Category(name="Керамика", slug="ceramic")
        cat_textile = Category(name="Текстиль", slug="textile")
        db.add_all([cat_ceramic, cat_textile])
        db.flush()

        p_active = Product(
            seller_id=seller.id,
            title="Керамическая ваза",
            description="Ручная работа, матовая глазурь.",
            price=Decimal("2500.00"),
            stock=5,
            category_id=cat_ceramic.id,
            tags=["ваза", "керамика"],
            materials=["глина"],
            status=ProductStatus.ACTIVE,
        )
        p_pending = Product(
            seller_id=seller.id,
            title="Плед из шерсти",
            description="Теплый плед ручной вязки.",
            price=Decimal("3400.00"),
            stock=3,
            category_id=cat_textile.id,
            tags=["плед"],
            materials=["шерсть"],
            status=ProductStatus.PENDING,
        )
        db.add_all([p_active, p_pending])
        db.flush()

        db.add_all(
            [
                ProductImage(product_id=p_active.id, image_url="https://placehold.co/800x600?text=Vase", sort_order=0),
                ProductImage(product_id=p_pending.id, image_url="https://placehold.co/800x600?text=Plaid", sort_order=0),
            ]
        )

        order = Order(
            buyer_id=buyer.id,
            seller_id=seller.id,
            status=OrderStatus.ACCEPTED,
            full_name="Иван Иванов",
            phone="+79990000000",
            address="Москва, ул. Пример, 1",
            comment="Позвоните за час",
            total_amount=Decimal("2500.00"),
        )
        db.add(order)
        db.flush()

        order_item = OrderItem(
            order_id=order.id,
            product_id=p_active.id,
            product_title_snapshot=p_active.title,
            product_price_snapshot=p_active.price,
            qty=1,
            subtotal=Decimal("2500.00"),
        )
        db.add(order_item)
        db.flush()

        db.add(Review(user_id=buyer.id, product_id=p_active.id, order_item_id=order_item.id, rating=5, text="Очень красиво!"))

        conv = Conversation(buyer_id=buyer.id, seller_id=seller.id, product_id=p_active.id)
        db.add(conv)
        db.flush()

        db.add_all(
            [
                Message(conversation_id=conv.id, sender_id=buyer.id, body="Здравствуйте, когда отправка?", is_read=False),
                Message(conversation_id=conv.id, sender_id=seller.id, body="Добрый день, завтра утром.", is_read=True),
            ]
        )

        db.add_all(
            [
                Notification(user_id=seller.id, type=NotificationType.NEW_ORDER, payload_json={"order_id": order.id}, is_read=False),
                Notification(user_id=seller.id, type=NotificationType.NEW_REVIEW, payload_json={"product_id": p_active.id}, is_read=False),
            ]
        )

        db.commit()
        print("Seed completed")


if __name__ == "__main__":
    run_seed()
