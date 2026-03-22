from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int
    price: float

class OrderItemResponse(BaseModel):
    id : int
    order_id : int
    product_id : int
    quantity : int
    price : float

    class Config:
        from_attributes = True