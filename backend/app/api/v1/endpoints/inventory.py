from typing import Any, List
import httpx
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.api import deps
from app.core.config import settings
from datetime import datetime

router = APIRouter()

@router.post("/suppliers", response_model=schemas.Supplier)
def create_supplier(
    *,
    db: Session = Depends(deps.get_db),
    supplier_in: schemas.SupplierCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create a supplier.
    """
    db_obj = models.Supplier(**supplier_in.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

@router.get("/suppliers", response_model=List[schemas.Supplier])
def read_suppliers(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve suppliers.
    """
    suppliers = db.query(models.Supplier).offset(skip).limit(limit).all()
    return suppliers

@router.post("/replenish", response_model=schemas.PurchaseOrder)
async def trigger_replenishment(
    *,
    db: Session = Depends(deps.get_db),
    request: schemas.ReplenishRequest,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Trigger replenishment logic for a SKU.
    """
    # 1. Get Inventory and Supplier info
    inventory = db.query(models.Inventory).filter(
        models.Inventory.sku_id == request.sku_id,
        models.Inventory.outlet_id == request.outlet_id
    ).first()
    
    if not inventory:
        # Create initial inventory record if not exists
        inventory = models.Inventory(sku_id=request.sku_id, outlet_id=request.outlet_id, quantity=0)
        db.add(inventory)
        db.commit()
        db.refresh(inventory)

    # Mocking getting the preferred supplier
    supplier = db.query(models.Supplier).first()
    if not supplier:
         raise HTTPException(status_code=404, detail="No suppliers found")

    # 2. Get Forecast (Mocked for now, ideally fetch from Sales Forecast API)
    forecast_mean = 50.0 
    forecast_std = 10.0

    # 3. Call ML Service
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{settings.ML_SERVICE_URL}/optimize_inventory",
                json={
                    "forecast_mean": forecast_mean,
                    "forecast_std": forecast_std,
                    "lead_time_days": supplier.lead_time_days
                }
            )
            response.raise_for_status()
            result = response.json()
        except httpx.RequestError as exc:
            raise HTTPException(status_code=503, detail=f"ML Service unavailable: {exc}")

    # 4. Update Reorder Point
    inventory.reorder_point = result["reorder_point"]
    db.add(inventory)
    
    # 5. Create PO if needed
    if inventory.quantity < inventory.reorder_point:
        po = models.PurchaseOrder(
            supplier_id=supplier.id,
            sku_id=request.sku_id,
            quantity=result["suggested_order_quantity"],
            created_at=datetime.utcnow()
        )
        db.add(po)
        db.commit()
        db.refresh(po)
        return po
    else:
        # Return a dummy PO or handle this case better in a real app
        # For now, we raise an exception or return empty
        raise HTTPException(status_code=200, detail="Inventory levels sufficient, no PO generated")

@router.get("/orders", response_model=List[schemas.PurchaseOrder])
def read_orders(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve purchase orders.
    """
    orders = db.query(models.PurchaseOrder).offset(skip).limit(limit).all()
    return orders
