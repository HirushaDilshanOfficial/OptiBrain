from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

class SalesDataBase(BaseModel):
    sku_id: str
    timestamp: datetime
    quantity: float
    price: float
    outlet_id: Optional[str] = None

class SalesDataCreate(SalesDataBase):
    pass

class SalesData(SalesDataBase):
    id: int

    class Config:
        from_attributes = True

class ForecastBase(BaseModel):
    sku_id: str
    timestamp: datetime
    predicted_quantity: float
    confidence_lower: Optional[float] = None
    confidence_upper: Optional[float] = None

class Forecast(ForecastBase):
    id: int
    model_version: Optional[str] = None

    class Config:
        from_attributes = True

class ForecastRequest(BaseModel):
    sku_id: str
    days: int = 7
