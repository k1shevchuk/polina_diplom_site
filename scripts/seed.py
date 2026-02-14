from __future__ import annotations

from collections import defaultdict
from datetime import UTC, datetime, timedelta
from decimal import Decimal
import random

from sqlalchemy import create_engine, delete, select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import hash_password
from app.models import (
    AdminAuditLog,
    Cart,
    CartItem,
    Category,
    Conversation,
    Favorite,
    Message,
    Notification,
    NotificationType,
    Order,
    OrderItem,
    OrderStatus,
    Product,
    ProductImage,
    ProductStatus,
    RefreshToken,
    Review,
    Role,
    RoleName,
    SellerProfile,
    User,
    UserRole,
)

TOTAL_USERS = 100
TOTAL_SELLERS = 12
RNG = random.Random(42)

CATEGORY_DEFINITIONS: list[tuple[str, str]] = [
    ("scarves", "Шарфы"),
    ("mittens", "Варежки"),
    ("socks", "Носки"),
    ("cardigans", "Кардиганы"),
    ("dresses", "Платья"),
    ("skirts", "Юбки"),
    ("bags", "Сумки"),
    ("sweaters", "Свитеры"),
]

PRODUCT_SERIES = {
    "scarf": {"category": "scarves", "label": "Шарф", "material": "мериносовая шерсть", "price": (2100, 4300), "count": 6},
    "mittens": {"category": "mittens", "label": "Варежки", "material": "кашемир", "price": (1500, 2800), "count": 3},
    "socks": {"category": "socks", "label": "Носки", "material": "шерсть альпаки", "price": (900, 1900), "count": 3},
    "cardigan": {"category": "cardigans", "label": "Кардиган", "material": "смесовая пряжа", "price": (4500, 8400), "count": 6},
    "dress": {"category": "dresses", "label": "Платье", "material": "хлопок с мериносом", "price": (5200, 9800), "count": 6},
    "skirt": {"category": "skirts", "label": "Юбка", "material": "тонкая шерсть", "price": (3200, 6200), "count": 6},
    "bag": {"category": "bags", "label": "Сумка", "material": "хлопковый шнур", "price": (2400, 5100), "count": 6},
    "sweater": {"category": "sweaters", "label": "Свитер", "material": "меринос и мохер", "price": (4700, 9200), "count": 6},
}

SELLER_NAMES = [
    "Мария Тёплая Нить",
    "Екатерина Уют",
    "Анна ВязАрт",
    "Ольга Wool Home",
    "Наталья Knit Mood",
    "Ирина Cozy Loop",
    "Татьяна Лавка Петелек",
    "Светлана Soft Yarn",
    "Юлия Тёплый Дом",
    "Дарья Knit Studio",
    "Елена Craft Knit",
    "Ксения Зимний Узор",
]

BUYER_FIRST_NAMES = [
    "Алексей",
    "Иван",
    "Алина",
    "Марина",
    "Виктория",
    "Денис",
    "София",
    "Полина",
    "Дмитрий",
    "Ольга",
]

BUYER_LAST_NAMES = [
    "Иванов",
    "Петров",
    "Сидорова",
    "Кузнецов",
    "Смирнова",
    "Орлова",
    "Фёдоров",
    "Волкова",
    "Белов",
    "Егорова",
]

ADJECTIVES = [
    "Уютный",
    "Нежный",
    "Тёплый",
    "Праздничный",
    "Базовый",
    "Элегантный",
    "Лёгкий",
    "Пушистый",
]


def clear_seed_domain(db: Session) -> None:
    db.execute(delete(AdminAuditLog))
    db.execute(delete(Notification))
    db.execute(delete(Message))
    db.execute(delete(Conversation))
    db.execute(delete(Review))
    db.execute(delete(Favorite))
    db.execute(delete(CartItem))
    db.execute(delete(Cart))
    db.execute(delete(OrderItem))
    db.execute(delete(Order))
    db.execute(delete(ProductImage))
    db.execute(delete(Product))
    db.execute(delete(Category))
    db.execute(delete(SellerProfile))
    db.execute(delete(RefreshToken))
    db.execute(delete(UserRole))
    db.execute(delete(User))
    db.commit()


def ensure_roles(db: Session) -> dict[RoleName, Role]:
    roles: dict[RoleName, Role] = {}
    existing = {role.name: role for role in db.scalars(select(Role)).all()}
    for role_name in RoleName:
        role = existing.get(role_name)
        if not role:
            role = Role(name=role_name)
            db.add(role)
            db.flush()
        roles[role_name] = role
    db.commit()
    return roles


def create_user(db: Session, email: str, password: str, role_rows: list[Role]) -> User:
    user = User(email=email, password_hash=hash_password(password), roles=role_rows)
    db.add(user)
    db.flush()
    return user


def create_categories(db: Session) -> dict[str, Category]:
    categories: dict[str, Category] = {}
    for slug, name in CATEGORY_DEFINITIONS:
        row = Category(name=name, slug=slug)
        db.add(row)
        db.flush()
        categories[slug] = row
    return categories


def create_products(db: Session, sellers: list[User], categories: dict[str, Category]) -> list[Product]:
    products: list[Product] = []
    now = datetime.now(UTC)
    seller_cycle = 0

    for prefix, definition in PRODUCT_SERIES.items():
        for index in range(1, definition["count"] + 1):
            low, high = definition["price"]
            price = Decimal(str(RNG.randrange(low, high, 100)))
            adjective = ADJECTIVES[(index + seller_cycle) % len(ADJECTIVES)]
            title = f"{adjective} {definition['label'].lower()} #{index}"
            description = (
                f"{definition['label']} ручной вязки из материала \"{definition['material']}\". "
                "Создано мастерицей Craft With Love, мягкая посадка и аккуратная отделка петель."
            )

            status = ProductStatus.ACTIVE if len(products) < 34 else ProductStatus.PENDING
            seller = sellers[seller_cycle % len(sellers)]
            seller_cycle += 1

            product = Product(
                seller_id=seller.id,
                title=title,
                description=description,
                price=price,
                stock=RNG.randint(2, 18),
                category_id=categories[definition["category"]].id,
                tags=[definition["label"].lower(), "вязание", "уют"],
                materials=[definition["material"]],
                status=status,
                created_at=now - timedelta(hours=len(products) * 6),
                updated_at=now - timedelta(hours=len(products) * 6),
            )
            db.add(product)
            db.flush()

            image_name = f"{prefix}{index}.jpg"
            db.add(ProductImage(product_id=product.id, image_url=f"/brand/products/{image_name}", sort_order=0))
            products.append(product)

    return products


def create_orders_reviews_and_notifications(db: Session, buyers: list[User], products: list[Product]) -> None:
    active_products = [product for product in products if product.status == ProductStatus.ACTIVE]
    if not active_products:
        return

    created_orders: list[Order] = []
    created_order_items: list[OrderItem] = []

    for index in range(40):
        buyer = buyers[index % len(buyers)]
        product = active_products[index % len(active_products)]
        qty = 1 if index % 3 else 2
        subtotal = (product.price * qty).quantize(Decimal("0.01"))

        first_name = BUYER_FIRST_NAMES[index % len(BUYER_FIRST_NAMES)]
        last_name = BUYER_LAST_NAMES[(index * 3) % len(BUYER_LAST_NAMES)]

        order = Order(
            buyer_id=buyer.id,
            seller_id=product.seller_id,
            status=OrderStatus.COMPLETED if index % 4 == 0 else (OrderStatus.ACCEPTED if index % 2 == 0 else OrderStatus.REQUESTED),
            full_name=f"{first_name} {last_name}",
            phone=f"+7999{index:06d}",
            address=f"Москва, ул. Пряничная, д. {10 + index}",
            comment="Доставка после 18:00" if index % 5 == 0 else None,
            total_amount=subtotal,
            created_at=datetime.now(UTC) - timedelta(days=index % 14),
            updated_at=datetime.now(UTC) - timedelta(days=index % 14),
        )
        db.add(order)
        db.flush()

        order_item = OrderItem(
            order_id=order.id,
            product_id=product.id,
            product_title_snapshot=product.title,
            product_price_snapshot=product.price,
            qty=qty,
            subtotal=subtotal,
        )
        db.add(order_item)
        db.flush()

        db.add(
            Notification(
                user_id=product.seller_id,
                type=NotificationType.NEW_ORDER,
                payload_json={"order_id": order.id, "buyer_email": buyer.email},
                is_read=index % 3 == 0,
            )
        )

        created_orders.append(order)
        created_order_items.append(order_item)

    review_candidates = [item for item in created_order_items if item.order.status == OrderStatus.COMPLETED]
    for index, order_item in enumerate(review_candidates[:20]):
        rating = 5 if index % 3 else 4
        review = Review(
            user_id=created_orders[index].buyer_id,
            product_id=order_item.product_id,
            order_item_id=order_item.id,
            rating=rating,
            text="Очень тёплая и аккуратная вещь, полностью как на фото.",
        )
        db.add(review)
        db.flush()

        db.add(
            Notification(
                user_id=created_orders[index].seller_id,
                type=NotificationType.NEW_REVIEW,
                payload_json={"review_id": review.id, "product_id": order_item.product_id},
                is_read=False,
            )
        )

    conversation_keys: set[tuple[int, int, int | None]] = set()
    for order in created_orders[:18]:
        order_item = next((item for item in created_order_items if item.order_id == order.id), None)
        product_id = order_item.product_id if order_item else None
        key = (order.buyer_id, order.seller_id, product_id)
        if key in conversation_keys:
            continue

        conversation_keys.add(key)
        conversation = Conversation(buyer_id=order.buyer_id, seller_id=order.seller_id, product_id=product_id)
        db.add(conversation)
        db.flush()

        db.add_all(
            [
                Message(
                    conversation_id=conversation.id,
                    sender_id=order.buyer_id,
                    body="Здравствуйте! Подскажите, пожалуйста, сроки отправки?",
                    is_read=True,
                ),
                Message(
                    conversation_id=conversation.id,
                    sender_id=order.seller_id,
                    body="Добрый день! Отправим в течение 1-2 дней после подтверждения.",
                    is_read=False,
                ),
            ]
        )

        db.add(
            Notification(
                user_id=order.seller_id,
                type=NotificationType.NEW_MESSAGE,
                payload_json={"conversation_id": conversation.id},
                is_read=False,
            )
        )


def create_favorites_and_carts(db: Session, buyers: list[User], active_products: list[Product]) -> None:
    for buyer in buyers[:45]:
        picks = RNG.sample(active_products, k=min(4, len(active_products)))
        for product in picks:
            db.add(Favorite(user_id=buyer.id, product_id=product.id))

    for index, buyer in enumerate(buyers[:20]):
        cart = Cart(user_id=buyer.id)
        db.add(cart)
        db.flush()

        picks = RNG.sample(active_products, k=min(3, len(active_products)))
        for product in picks:
            db.add(CartItem(cart_id=cart.id, product_id=product.id, qty=1 + ((index + product.id) % 2)))


def run_seed() -> None:
    engine = create_engine(settings.database_url, future=True)

    with Session(engine) as db:
        clear_seed_domain(db)
        roles = ensure_roles(db)

        users: list[User] = []
        sellers: list[User] = []
        buyers: list[User] = []

        admin = create_user(db, "admin@example.com", "Admin12345", [roles[RoleName.ADMIN], roles[RoleName.BUYER]])
        main_seller = create_user(db, "seller@example.com", "Seller12345", [roles[RoleName.SELLER], roles[RoleName.BUYER]])
        main_buyer = create_user(db, "buyer@example.com", "Buyer12345", [roles[RoleName.BUYER]])

        users.extend([admin, main_seller, main_buyer])
        sellers.append(main_seller)
        buyers.extend([admin, main_seller, main_buyer])

        extra_sellers_needed = TOTAL_SELLERS - len(sellers)
        for index in range(1, extra_sellers_needed + 1):
            seller_user = create_user(
                db,
                f"seller{index:02d}@craftwithlove.ru",
                "Seller12345",
                [roles[RoleName.SELLER], roles[RoleName.BUYER]],
            )
            users.append(seller_user)
            sellers.append(seller_user)
            buyers.append(seller_user)

        buyers_needed = TOTAL_USERS - len(users)
        for index in range(1, buyers_needed + 1):
            buyer_user = create_user(db, f"buyer{index:03d}@craftwithlove.ru", "Buyer12345", [roles[RoleName.BUYER]])
            users.append(buyer_user)
            buyers.append(buyer_user)

        for index, seller in enumerate(sellers):
            display_name = SELLER_NAMES[index % len(SELLER_NAMES)]
            db.add(
                SellerProfile(
                    user_id=seller.id,
                    display_name=display_name,
                    bio="Мастерская Craft With Love: вязаные изделия ручной работы, связанные с любовью.",
                )
            )

        categories = create_categories(db)
        products = create_products(db, sellers, categories)
        active_products = [product for product in products if product.status == ProductStatus.ACTIVE]

        create_orders_reviews_and_notifications(db, buyers, products)
        create_favorites_and_carts(db, buyers, active_products)

        db.commit()

        products_per_category: dict[str, int] = defaultdict(int)
        for product in products:
            category_slug = next((slug for slug, row in categories.items() if row.id == product.category_id), "unknown")
            products_per_category[category_slug] += 1

        print(
            "Seed completed:",
            {
                "users": len(users),
                "sellers": len(sellers),
                "buyers": len(buyers),
                "products": len(products),
                "active_products": len(active_products),
                "categories": len(categories),
                "products_per_category": dict(sorted(products_per_category.items())),
            },
        )


if __name__ == "__main__":
    run_seed()
