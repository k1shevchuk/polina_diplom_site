from __future__ import annotations

from datetime import date

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.admin_audit_log import AdminAuditLog
from app.models.order import Order
from app.models.product import Product
from app.models.review import Review
from app.models.user import User


def log_admin_action(
    db: Session,
    admin_user_id: int,
    action: str,
    target_type: str,
    target_id: int | None,
    details: dict | None = None,
) -> AdminAuditLog:
    row = AdminAuditLog(
        admin_user_id=admin_user_id,
        action=action,
        target_type=target_type,
        target_id=target_id,
        details_json=details or {},
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def get_stats(db: Session) -> dict:
    users = db.scalar(select(func.count(User.id))) or 0

    # MVP simplification: sellers are users who have at least one product.
    sellers = db.scalar(select(func.count(func.distinct(Product.seller_id)))) or 0

    products = db.scalar(select(func.count(Product.id))) or 0
    orders = db.scalar(select(func.count(Order.id))) or 0
    reviews = db.scalar(select(func.count(Review.id))) or 0
    return {
        "users": users,
        "sellers": sellers,
        "products": products,
        "orders": orders,
        "reviews": reviews,
    }


def orders_trend_by_day(db: Session, days: int = 14) -> list[dict]:
    rows = db.execute(
        select(func.date(Order.created_at), func.count(Order.id))
        .group_by(func.date(Order.created_at))
        .order_by(func.date(Order.created_at).desc())
        .limit(days)
    ).all()
    return [{"day": str(day), "count": count} for day, count in rows if isinstance(day, date)]


def list_audit_logs(db: Session, limit: int = 100) -> list[AdminAuditLog]:
    return db.scalars(select(AdminAuditLog).order_by(AdminAuditLog.created_at.desc()).limit(limit)).all()
