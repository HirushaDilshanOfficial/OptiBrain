from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from models.forecasting import DemandForecaster

app = FastAPI(title="OptiBrain ML Service")

forecaster = DemandForecaster()

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
