from typing import Any, List
import httpx
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.api import deps
from app.core.config import settings

router = APIRouter()

@router.post("/", response_model=schemas.SalesData)
def create_sales_data(
    *,
    db: Session = Depends(deps.get_db),
    sales_in: schemas.SalesDataCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Ingest sales data.
    """
    db_obj = models.SalesData(**sales_in.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

@router.get("/forecast/{sku_id}", response_model=schemas.Forecast)
async def get_forecast(
    sku_id: str,
    days: int = 7,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get forecast for a SKU.
    """
    # 1. Fetch historical data from DB
    history = db.query(models.SalesData).filter(models.SalesData.sku_id == sku_id).all()
    
    # Format for ML service
    history_data = [
        {"ds": d.timestamp.isoformat(), "y": d.quantity} for d in history
    ]

    # 2. Call ML Service
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{settings.ML_SERVICE_URL}/predict",
                json={"history": history_data, "days": days}
            )
            response.raise_for_status()
            prediction = response.json()
        except httpx.RequestError as exc:
            raise HTTPException(status_code=503, detail=f"ML Service unavailable: {exc}")
        except httpx.HTTPStatusError as exc:
             raise HTTPException(status_code=exc.response.status_code, detail=f"ML Service error: {exc.response.text}")

    # 3. Save forecast to DB (optional, but good for caching/audit)
    # For now, just return the prediction
    
    # Mocking the return structure based on ML service response
    # Assuming ML service returns a list of forecasts, we take the last one or aggregate
    # This is a simplification.
    
    latest_forecast = prediction["forecast"][-1]
    
    return {
        "id": 0, # Placeholder
        "sku_id": sku_id,
        "timestamp": latest_forecast["ds"],
        "predicted_quantity": latest_forecast["yhat"],
        "confidence_lower": latest_forecast["yhat_lower"],
        "confidence_upper": latest_forecast["yhat_upper"],
        "model_version": "v1"
    }
