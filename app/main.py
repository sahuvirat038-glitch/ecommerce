from fastapi import FastAPI
from app.database import engine, Base
from app.models import User, Category, Product, Cart, Order, OrderItem
from app.routers import user, category, product, cart, order

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="E-commerce API",
    description="A fully functional e-commerce backend",
    version="1.0.0"
)

app.include_router(user.router)
app.include_router(category.router)
app.include_router(product.router)
app.include_router(cart.router)
app.include_router(order.router)

@app.get("/")
def root():
    return {"message": "Welcome to E-commerce API!"}