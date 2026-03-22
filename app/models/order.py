from sqlalchemy import Column, String, Integer, Float,  DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base
from sqlalchemy.orm import relationship

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, index=True, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable = False)
    total_price = Column(Float, nullable = False)
    status = Column(String, nullable = False, default = "pending" )
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Add this at the bottom of the class
    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")