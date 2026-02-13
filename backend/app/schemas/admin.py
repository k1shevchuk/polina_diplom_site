from pydantic import BaseModel


class StatsOut(BaseModel):
    users: int
    sellers: int
    products: int
    orders: int
    reviews: int


class TrendItem(BaseModel):
    day: str
    count: int


class AuditOut(BaseModel):
    id: int
    admin_user_id: int
    action: str
    target_type: str
    target_id: int | None
    details_json: dict
    created_at: str
