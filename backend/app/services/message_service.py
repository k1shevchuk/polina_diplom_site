from __future__ import annotations

from datetime import UTC, datetime

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.conversation import Conversation
from app.models.message import Message
from app.models.notification import NotificationType
from app.services.notification_service import create_notification


def get_or_create_conversation(db: Session, buyer_id: int, seller_id: int, product_id: int | None) -> Conversation:
    conversation = db.scalar(
        select(Conversation).where(
            Conversation.buyer_id == buyer_id,
            Conversation.seller_id == seller_id,
            Conversation.product_id == product_id,
        )
    )
    if conversation:
        return conversation

    conversation = Conversation(buyer_id=buyer_id, seller_id=seller_id, product_id=product_id)
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return conversation


def ensure_participant(conversation: Conversation, user_id: int) -> None:
    if user_id not in {conversation.buyer_id, conversation.seller_id}:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not a participant")


def list_user_conversations(db: Session, user_id: int) -> list[Conversation]:
    stmt = select(Conversation).where((Conversation.buyer_id == user_id) | (Conversation.seller_id == user_id))
    return db.scalars(stmt.order_by(Conversation.updated_at.desc())).all()


def create_message(db: Session, conversation: Conversation, sender_id: int, body: str) -> Message:
    ensure_participant(conversation, sender_id)
    message = Message(conversation_id=conversation.id, sender_id=sender_id, body=body)
    db.add(message)
    conversation.updated_at = datetime.now(UTC)
    db.add(conversation)

    receiver_id = conversation.seller_id if sender_id == conversation.buyer_id else conversation.buyer_id
    create_notification(
        db,
        user_id=receiver_id,
        notification_type=NotificationType.NEW_MESSAGE,
        payload={"conversation_id": conversation.id, "sender_id": sender_id},
    )
    db.commit()
    db.refresh(message)
    return message


def list_messages(db: Session, conversation: Conversation, user_id: int, after: datetime | None) -> list[Message]:
    ensure_participant(conversation, user_id)
    stmt = select(Message).where(Message.conversation_id == conversation.id)
    if after:
        stmt = stmt.where(Message.created_at > after)
    return db.scalars(stmt.order_by(Message.created_at.asc())).all()


def mark_messages_read(db: Session, conversation: Conversation, user_id: int) -> int:
    ensure_participant(conversation, user_id)
    rows = db.scalars(
        select(Message).where(Message.conversation_id == conversation.id, Message.sender_id != user_id, Message.is_read.is_(False))
    ).all()
    for row in rows:
        row.is_read = True
        db.add(row)
    db.commit()
    return len(rows)
