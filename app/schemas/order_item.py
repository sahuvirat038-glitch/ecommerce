from uuid import UUID
from pydantic import BaseModel
from typing import Optional
from app.schemas.product import ProductResponse

class OrderItemCreate(BaseModel):
    product_id: UUID
    quantity: int
    price: float

class OrderItemResponse(BaseModel):
    id: UUID
    order_id: UUID
    product_id: UUID
    quantity: int
    price: float
    product: Optional[ProductResponse] = None

    class Config:
        from_attributes = True
