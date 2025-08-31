from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies import get_session
from models import Order
from schemas import OrderSchema

order_router = APIRouter(prefix="/order", tags=["order"])

@order_router.get("/")
async def get_orders():
    """
    This route is used to get all orders, but only if the user is authenticated
    """
    return {"message": "You are on the order route"}

@order_router.post("/create")
async def create_order(order_schema: OrderSchema, session: Session = Depends(get_session)):
    new_order = Order(user= order_schema.user_id)
    session.add(new_order)
    session.commit()
    return {"message": f"Order add with sucess. Order id: {new_order.id}"}