from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CartCreate(BaseModel):
    product_id: int
    quantity: int

class CartResponse(BaseModel):
    id : int
    user_id : int
    product_id : int
    quantity : int
    created_at : datetime

    class Config:
        from_attributes = True