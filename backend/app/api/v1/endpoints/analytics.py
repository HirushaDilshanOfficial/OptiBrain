from typing import Any, Dict
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
import json

from app import models
from app.api import deps
from app.core.redis import get_redis_pool

router = APIRouter()

@router.get("/sales")
async def get_sales_analytics(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get sales analytics (Total Revenue, Total Units Sold).
    Cached for 60 seconds.
    """
    redis = await get_redis_pool()
    cache_key = "analytics:sales"
    cached_data = await redis.get(cache_key)
    
    if cached_data:
        return json.loads(cached_data)

    # Calculate Total Revenue (Mock: assuming price is constant or we sum up sales * price)
    # For MVP, we'll just sum the 'quantity' from SalesData and multiply by a mock avg price
    total_units = db.query(func.sum(models.SalesData.quantity)).scalar() or 0
    total_revenue = total_units * 25.0 # Mock average price
    
    data = {
        "total_revenue": total_revenue,
        "total_units_sold": total_units,
        "revenue_growth": 12.5, # Mock growth percentage
    }
    
    await redis.set(cache_key, json.dumps(data), ex=60)
    return data

@router.get("/inventory")
async def get_inventory_analytics(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get inventory analytics (Low Stock Items, Total Value).
    """
    # Count items below reorder point
    low_stock_count = 0
    inventory_items = db.query(models.Inventory).all()
    for item in inventory_items:
        if item.quantity < item.reorder_point:
            low_stock_count += 1
            
    return {
        "low_stock_items": low_stock_count,
        "total_sku_count": len(inventory_items),
        "inventory_turnover_rate": 4.2 # Mock
    }

@router.get("/fulfillment")
async def get_fulfillment_analytics(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get fulfillment analytics (Orders by Channel, Status).
    """
    # Orders by Channel
    channel_stats = db.query(
        models.Channel.name, func.count(models.OrderSource.id)
    ).join(models.OrderSource).group_by(models.Channel.name).all()
    
    return {
        "orders_by_channel": [{"name": name, "count": count} for name, count in channel_stats],
        "avg_fulfillment_time_hours": 24.5 # Mock
    }
