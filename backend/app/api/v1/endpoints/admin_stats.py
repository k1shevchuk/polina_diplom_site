from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import require_roles
from app.db.session import get_db
from app.models.role import RoleName
from app.models.user import User
from app.schemas.admin import StatsOut, TrendItem
from app.services.admin_service import get_stats, orders_trend_by_day

router = APIRouter()


@router.get("", response_model=StatsOut)
def stats(current_admin: User = Depends(require_roles(RoleName.ADMIN)), db: Session = Depends(get_db)):
    return StatsOut(**get_stats(db))


@router.get("/trend", response_model=list[TrendItem])
def trend(current_admin: User = Depends(require_roles(RoleName.ADMIN)), db: Session = Depends(get_db)):
    return [TrendItem(**row) for row in orders_trend_by_day(db)]
