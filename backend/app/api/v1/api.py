from fastapi import APIRouter

from app.api.v1.endpoints import login, users, sales, pricing, inventory, fulfillment, analytics, customers

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(sales.router, prefix="/sales", tags=["sales"])
api_router.include_router(pricing.router, prefix="/pricing", tags=["pricing"])
api_router.include_router(inventory.router, prefix="/inventory", tags=["inventory"])
api_router.include_router(fulfillment.router, prefix="/fulfillment", tags=["fulfillment"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
api_router.include_router(customers.router, prefix="/customers", tags=["customers"])
