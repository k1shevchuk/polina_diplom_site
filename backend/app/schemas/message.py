from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.common import BaseSchema


class ConversationCreate(BaseModel):
    seller_id: int
    product_id: int | None = None


class ConversationOut(BaseSchema):
    id: int
    buyer_id: int
    seller_id: int
    product_id: int | None
    created_at: datetime
    updated_at: datetime


class MessageCreate(BaseModel):
    body: str = Field(min_length=1, max_length=3000)


class MessageOut(BaseSchema):
    id: int
    conversation_id: int
    sender_id: int
    body: str
    is_read: bool
    created_at: datetime
