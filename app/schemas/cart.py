from uuid import UUID
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.schemas.product import ProductResponse

class CartCreate(BaseModel):
    product_id: UUID
    quantity: int = 1

class CartUpdate(BaseModel):
    quantity: int

class CartResponse(BaseModel):
    id: UUID
    user_id: UUID
    product_id: UUID
    quantity: int
    created_at: datetime
    product: Optional[ProductResponse] = None

    class Config:
        from_attributes = True
