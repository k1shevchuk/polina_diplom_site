from datetime import datetime

from pydantic import BaseModel

from app.models.notification import NotificationType
from app.schemas.common import BaseSchema


class NotificationOut(BaseSchema):
    id: int
    user_id: int
    type: NotificationType
    payload_json: dict
    is_read: bool
    created_at: datetime


class NotificationReadRequest(BaseModel):
    is_read: bool = True
