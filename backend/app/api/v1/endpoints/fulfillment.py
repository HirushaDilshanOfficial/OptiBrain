from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid

from app import models, schemas
from app.api import deps
from datetime import datetime

router = APIRouter()

@router.post("/channels", response_model=schemas.Channel)
def create_channel(
    *,
    db: Session = Depends(deps.get_db),
    channel_in: schemas.ChannelCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create a sales channel.
    """
    db_obj = models.Channel(**channel_in.dict(), api_key=str(uuid.uuid4()))
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

@router.get("/channels", response_model=List[schemas.Channel])
def read_channels(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve channels.
    """
    channels = db.query(models.Channel).offset(skip).limit(limit).all()
    return channels

@router.post("/nodes", response_model=schemas.FulfillmentNode)
def create_fulfillment_node(
    *,
    db: Session = Depends(deps.get_db),
    node_in: schemas.FulfillmentNodeCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create a fulfillment node (store/warehouse).
    """
    db_obj = models.FulfillmentNode(**node_in.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

@router.post("/orders", response_model=schemas.OrderSource)
def ingest_order(
    *,
    db: Session = Depends(deps.get_db),
    order_in: schemas.OrderSourceCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Ingest an order from an external channel.
    """
    db_obj = models.OrderSource(
        **order_in.dict(),
        status="pending",
        created_at=datetime.utcnow()
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

@router.post("/route", response_model=schemas.OrderSource)
def route_order(
    *,
    db: Session = Depends(deps.get_db),
    request: schemas.RoutingRequest,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Route an order to the optimal fulfillment node.
    """
    order = db.query(models.OrderSource).filter(models.OrderSource.id == request.order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Simple Routing Logic:
    # 1. Find active nodes
    # 2. Check inventory (Mocked: assume priority 1 node has stock)
    # 3. Assign to highest priority node
    
    nodes = db.query(models.FulfillmentNode).filter(
        models.FulfillmentNode.is_active == True
    ).order_by(models.FulfillmentNode.priority).all()
    
    if not nodes:
        raise HTTPException(status_code=400, detail="No active fulfillment nodes available")
        
    # Assign to the first available node (highest priority)
    # In a real system, we would check `models.Inventory` for this node + SKU
    best_node = nodes[0]
    
    order.fulfillment_node_id = best_node.id
    order.status = "routed"
    db.add(order)
    db.commit()
    db.refresh(order)
    
    return order

@router.get("/orders", response_model=List[schemas.OrderSource])
def read_orders(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve orders.
    """
    orders = db.query(models.OrderSource).offset(skip).limit(limit).all()
    return orders
