from uuid import UUID
from pydantic import BaseModel
from datetime import datetime
from typing import List
from app.schemas.order_item import OrderItemResponse

class OrderCreate(BaseModel):
    total_price: float

class OrderResponse(BaseModel):
    id: UUID
    user_id: UUID
    total_price: float
    status: str
    created_at: datetime
    items: List[OrderItemResponse] = []

    class Config:
        from_attributes = True
