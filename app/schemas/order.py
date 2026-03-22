from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class OrderCreate(BaseModel):
    total_price : float

class OrderResponse(BaseModel):
    id : int
    user_id : int
    total_price : float
    status : str
    created_at : datetime


    class Config:
        from_attributes = True