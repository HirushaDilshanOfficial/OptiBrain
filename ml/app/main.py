from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from models.forecasting import DemandForecaster
from models.pricing import DynamicPricingEngine
from models.inventory import ReplenishmentOptimizer

app = FastAPI(title="OptiBrain ML Service")

forecaster = DemandForecaster()
pricing_engine = DynamicPricingEngine()
inventory_optimizer = ReplenishmentOptimizer()

class HistoryPoint(BaseModel):
    ds: str
    y: float

class PredictRequest(BaseModel):
    history: List[HistoryPoint]
    days: int = 7

@app.get("/")
def root():
    return {"message": "OptiBrain ML Service"}

@app.post("/predict")
def predict(request: PredictRequest):
    try:
        # Convert request to DataFrame-like structure
        data = [{"ds": h.ds, "y": h.y} for h in request.history]
        
        # Train and Predict (In a real scenario, we would load a pre-trained model)
        forecaster.train(data)
        forecast = forecaster.predict(request.days)
        
        return {"forecast": forecast}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class PricingRequest(BaseModel):
    current_price: float
    forecast: float
    inventory_level: int
    min_price: float
    max_price: float

@app.post("/optimize_price")
def optimize_price(request: PricingRequest):
    try:
        result = pricing_engine.optimize_price(
            request.current_price,
            request.forecast,
            request.inventory_level,
            request.min_price,
            request.max_price
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class InventoryRequest(BaseModel):
    forecast_mean: float
    forecast_std: float
    lead_time_days: int
    service_level: float = 0.95

@app.post("/optimize_inventory")
def optimize_inventory(request: InventoryRequest):
    try:
        result = inventory_optimizer.optimize_inventory(
            request.forecast_mean,
            request.forecast_std,
            request.lead_time_days,
            request.service_level
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
