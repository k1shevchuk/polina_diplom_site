from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.common import BaseSchema


class ReviewCreate(BaseModel):
    rating: int = Field(ge=1, le=5)
    text: str = Field(min_length=3, max_length=2000)


class ReviewOut(BaseSchema):
    id: int
    user_id: int
    product_id: int
    order_item_id: int
    rating: int
    text: str
    is_hidden: bool
    created_at: datetime
