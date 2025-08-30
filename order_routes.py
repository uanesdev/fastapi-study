from fastapi import APIRouter

order_router = APIRouter(prefix="/order", tags=["order"])

@order_router.get("/")
async def get_orders():
    """
    This route is used to get all orders, but only if the user is authenticated
    """
    return {"message": "You are on the order route"}
