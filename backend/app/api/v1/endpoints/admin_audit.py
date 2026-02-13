from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import require_roles
from app.db.session import get_db
from app.models.role import RoleName
from app.models.user import User
from app.schemas.admin import AuditOut
from app.services.admin_service import list_audit_logs

router = APIRouter()


@router.get("", response_model=list[AuditOut])
def audit_logs(current_admin: User = Depends(require_roles(RoleName.ADMIN)), db: Session = Depends(get_db)):
    rows = list_audit_logs(db)
    return [
        AuditOut(
            id=row.id,
            admin_user_id=row.admin_user_id,
            action=row.action,
            target_type=row.target_type,
            target_id=row.target_id,
            details_json=row.details_json,
            created_at=row.created_at.isoformat(),
        )
        for row in rows
    ]
