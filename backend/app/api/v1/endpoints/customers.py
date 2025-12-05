from typing import Any, List
import httpx
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta

from app import models, schemas
from app.api import deps
from app.core.config import settings

router = APIRouter()

@router.post("/", response_model=schemas.Customer)
def create_customer(
    *,
    db: Session = Depends(deps.get_db),
    customer_in: schemas.CustomerCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create a new customer.
    """
    db_obj = models.Customer(**customer_in.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

@router.get("/", response_model=List[schemas.Customer])
def read_customers(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve customers.
    """
    customers = db.query(models.Customer).offset(skip).limit(limit).all()
    return customers

@router.post("/segment")
async def segment_customers(
    *,
    db: Session = Depends(deps.get_db),
    request: schemas.SegmentationRequest,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Trigger customer segmentation using ML.
    """
    # 1. Get customers to segment
    if request.customer_ids:
        customers = db.query(models.Customer).filter(
            models.Customer.id.in_(request.customer_ids)
        ).all()
    else:
        customers = db.query(models.Customer).all()
    
    if not customers:
        raise HTTPException(status_code=404, detail="No customers found")
    
    # 2. Calculate RFM metrics from sales data
    customer_data = []
    for customer in customers:
        # Mock RFM calculation (in real system, join with sales data)
        # For demo, we'll use random-ish values based on customer ID
        recency = (customer.id % 30) + 1  # Days since last purchase
        frequency = (customer.id % 10) + 1  # Number of purchases
        monetary = (customer.id % 100) * 10.0 + 100.0  # Total spend
        
        customer_data.append({
            "customer_id": customer.id,
            "recency": recency,
            "frequency": frequency,
            "monetary": monetary
        })
    
    # 3. Call ML Service
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{settings.ML_SERVICE_URL}/segment_customers",
                json={"customers": customer_data}
            )
            response.raise_for_status()
            result = response.json()
        except httpx.RequestError as exc:
            raise HTTPException(status_code=503, detail=f"ML Service unavailable: {exc}")
    
    # 4. Ensure segments exist in DB
    segment_names = ["Low Value", "Medium Value", "High Value"]
    for i, name in enumerate(segment_names):
        segment = db.query(models.CustomerSegment).filter(
            models.CustomerSegment.name == name
        ).first()
        if not segment:
            segment = models.CustomerSegment(id=i, name=name, description=f"{name} customers")
            db.add(segment)
    db.commit()
    
    # 5. Update customer segments
    segments_map = result["segments"]
    for customer in customers:
        if str(customer.id) in segments_map:
            customer.segment_id = segments_map[str(customer.id)]
        elif customer.id in segments_map:
            customer.segment_id = segments_map[customer.id]
        db.add(customer)
    
    db.commit()
    
    return {"message": f"Segmented {len(customers)} customers", "segments": segments_map}

@router.get("/segments", response_model=List[schemas.CustomerSegment])
def read_segments(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve customer segments.
    """
    segments = db.query(models.CustomerSegment).all()
    return segments
