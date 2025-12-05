from typing import Any, List
import httpx
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.api import deps
from app.core.config import settings

router = APIRouter()

@router.post("/rules", response_model=schemas.PricingRule)
def create_pricing_rule(
    *,
    db: Session = Depends(deps.get_db),
    rule_in: schemas.PricingRuleCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create a pricing rule.
    """
    db_obj = models.PricingRule(**rule_in.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

@router.post("/optimize", response_model=schemas.PriceLog)
async def optimize_price(
    *,
    db: Session = Depends(deps.get_db),
    request: schemas.OptimizeRequest,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Calculate optimal price for a SKU.
    """
    # 1. Get Pricing Rule
    rule = db.query(models.PricingRule).filter(
        models.PricingRule.sku_id == request.sku_id,
        models.PricingRule.is_active == True
    ).first()
    
    if not rule:
        raise HTTPException(status_code=404, detail="No active pricing rule found for this SKU")

    # 2. Get Forecast (Simplification: calling ML service directly or using cached forecast)
    # For this MVP, we'll assume we pass a dummy forecast value or fetch it.
    # Let's fetch the latest forecast from DB or assume a value.
    forecast_val = 150.0 # Mock forecast value

    # 3. Call ML Service for Optimization
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{settings.ML_SERVICE_URL}/optimize_price",
                json={
                    "current_price": request.current_price,
                    "forecast": forecast_val,
                    "inventory_level": request.inventory_level,
                    "min_price": rule.min_price,
                    "max_price": rule.max_price
                }
            )
            response.raise_for_status()
            result = response.json()
        except httpx.RequestError as exc:
            raise HTTPException(status_code=503, detail=f"ML Service unavailable: {exc}")

    # 4. Log the price change
    price_log = models.PriceLog(
        sku_id=request.sku_id,
        old_price=request.current_price,
        new_price=result["recommended_price"],
        reason=result["reason"],
        model_version="v1"
    )
    db.add(price_log)
    db.commit()
    db.refresh(price_log)
    
    return price_log
