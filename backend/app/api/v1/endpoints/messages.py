from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.conversation import Conversation
from app.models.user import User
from app.schemas.common import MessageResponse
from app.schemas.message import ConversationCreate, ConversationOut, MessageCreate, MessageOut
from app.services.message_service import (
    create_message,
    get_or_create_conversation,
    list_messages,
    list_user_conversations,
    mark_messages_read,
)

router = APIRouter()


@router.get("/conversations", response_model=list[ConversationOut])
def get_conversations(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    rows = list_user_conversations(db, current_user.id)
    return [ConversationOut.model_validate(row) for row in rows]


@router.post("/conversations", response_model=ConversationOut)
def start_conversation(
    payload: ConversationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    conversation = get_or_create_conversation(db, current_user.id, payload.seller_id, payload.product_id)
    return ConversationOut.model_validate(conversation)


@router.get("/conversations/{conversation_id}", response_model=list[MessageOut])
def get_messages(
    conversation_id: int,
    after: datetime | None = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    conversation = db.scalar(select(Conversation).where(Conversation.id == conversation_id))
    if not conversation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")
    rows = list_messages(db, conversation, current_user.id, after)
    return [MessageOut.model_validate(row) for row in rows]


@router.post("/conversations/{conversation_id}", response_model=MessageOut)
def send_message(
    conversation_id: int,
    payload: MessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    conversation = db.scalar(select(Conversation).where(Conversation.id == conversation_id))
    if not conversation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")
    message = create_message(db, conversation, current_user.id, payload.body)
    return MessageOut.model_validate(message)


@router.post("/conversations/{conversation_id}/read", response_model=MessageResponse)
def mark_read(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    conversation = db.scalar(select(Conversation).where(Conversation.id == conversation_id))
    if not conversation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")
    count = mark_messages_read(db, conversation, current_user.id)
    return MessageResponse(message=f"Marked {count} messages as read")
