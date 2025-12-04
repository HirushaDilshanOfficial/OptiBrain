from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class PricingRuleBase(BaseModel):
    sku_id: str
    min_price: float
    max_price: float
    max_daily_increase_pct: Optional[float] = 0.1
    is_active: Optional[bool] = True

class PricingRuleCreate(PricingRuleBase):
    pass

class PricingRule(PricingRuleBase):
    id: int

    class Config:
        from_attributes = True

class PriceLogBase(BaseModel):
    sku_id: str
    old_price: float
    new_price: float
    reason: Optional[str] = None
    model_version: Optional[str] = None

class PriceLog(PriceLogBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True

class OptimizeRequest(BaseModel):
    sku_id: str
    current_price: float
    inventory_level: int
