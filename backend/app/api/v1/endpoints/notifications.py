from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.notification import NotificationOut
from app.services.notification_service import list_notifications, mark_notification_read

router = APIRouter()


@router.get("", response_model=list[NotificationOut])
def list_my_notifications(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    rows = list_notifications(db, current_user.id)
    return [NotificationOut.model_validate(row) for row in rows]


@router.post("/{notification_id}/read", response_model=NotificationOut)
def mark_read(notification_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    row = mark_notification_read(db, current_user.id, notification_id, True)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")
    return NotificationOut.model_validate(row)
