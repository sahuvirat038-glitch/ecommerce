from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.cart import Cart
from app.models.product import Product
from app.models.user import User
from app.schemas.order import OrderCreate, OrderResponse
from app.utils.auth import get_current_user
from typing import List

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

# GET all orders for current user
@router.get("/", response_model=List[OrderResponse])
def get_orders(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    orders = db.query(Order).filter(Order.user_id == current_user.id).all()
    return orders

# GET single order
@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == current_user.id
    ).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    return order

# CREATE order from cart
@router.post("/", response_model=OrderResponse)
def create_order(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    cart_items = db.query(Cart).filter(Cart.user_id == current_user.id).all()
    if not cart_items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cart is empty"
        )
    total_price = 0
    for item in cart_items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        total_price += product.price * item.quantity

    new_order = Order(
        user_id=current_user.id,
        total_price=total_price,
        status="pending"
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    for item in cart_items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        order_item = OrderItem(
            order_id=new_order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=product.price
        )
        db.add(order_item)

    for item in cart_items:
        db.delete(item)

    db.commit()
    return new_order

# UPDATE order status
@router.put("/{order_id}", response_model=OrderResponse)
def update_order_status(order_id: int, order_status: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == current_user.id
    ).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    order.status = order_status
    db.commit()
    db.refresh(order)
    return order

# DELETE order
@router.delete("/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == current_user.id
    ).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    db.delete(order)
    db.commit()
    return {"message": "Order deleted successfully"}