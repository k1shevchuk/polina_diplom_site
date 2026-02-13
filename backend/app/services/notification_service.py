from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.notification import Notification, NotificationType


def create_notification(db: Session, user_id: int, notification_type: NotificationType, payload: dict) -> Notification:
    notification = Notification(user_id=user_id, type=notification_type, payload_json=payload)
    db.add(notification)
    return notification


def list_notifications(db: Session, user_id: int) -> list[Notification]:
    stmt = select(Notification).where(Notification.user_id == user_id).order_by(Notification.created_at.desc())
    return db.scalars(stmt).all()


def mark_notification_read(db: Session, user_id: int, notification_id: int, is_read: bool) -> Notification | None:
    notification = db.scalar(select(Notification).where(Notification.id == notification_id, Notification.user_id == user_id))
    if not notification:
        return None
    notification.is_read = is_read
    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification
