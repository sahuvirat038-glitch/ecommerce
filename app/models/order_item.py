from sqlalchemy import Column, Integer, Float, ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, default = 1)
    price = Column(Float, nullable = False)

    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")
