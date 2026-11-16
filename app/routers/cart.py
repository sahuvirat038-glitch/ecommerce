from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.cart import Cart
from app.models.product import Product
from app.models.user import User
from app.schemas.cart import CartCreate, CartUpdate, CartResponse
from app.utils.auth import get_current_user

router = APIRouter(prefix="/cart", tags=["Cart"])

@router.get("/", response_model=List[CartResponse])
def get_cart(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Cart).filter(Cart.user_id == current_user.id).all()

@router.post("/", response_model=CartResponse)
def add_to_cart(cart: CartCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    product = db.query(Product).filter(Product.id == cart.product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    if product.stock < cart.quantity:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient stock")

    existing = db.query(Cart).filter(Cart.user_id == current_user.id, Cart.product_id == cart.product_id).first()
    if existing:
        if product.stock < (existing.quantity + cart.quantity):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient stock")
        existing.quantity += cart.quantity
        db.commit()
        db.refresh(existing)
        return existing

    new_cart = Cart(user_id=current_user.id, product_id=cart.product_id, quantity=cart.quantity)
    db.add(new_cart)
    db.commit()
    db.refresh(new_cart)
    return new_cart

@router.put("/{cart_id}", response_model=CartResponse)
def update_cart_quantity(cart_id: UUID, cart: CartUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_cart = db.query(Cart).filter(Cart.id == cart_id, Cart.user_id == current_user.id).first()
    if not db_cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found")
    if cart.quantity <= 0:
        db.delete(db_cart)
        db.commit()
        raise HTTPException(status_code=status.HTTP_200_OK, detail="Item removed from cart")
    if db_cart.product.stock < cart.quantity:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient stock")
    db_cart.quantity = cart.quantity
    db.commit()
    db.refresh(db_cart)
    return db_cart

@router.delete("/{cart_id}")
def delete_cart(cart_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_cart = db.query(Cart).filter(Cart.id == cart_id, Cart.user_id == current_user.id).first()
    if not db_cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found")
    db.delete(db_cart)
    db.commit()
    return {"message": "Item removed from cart successfully"}
