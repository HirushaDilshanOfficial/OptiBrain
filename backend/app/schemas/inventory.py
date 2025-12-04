from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class POStatus(str, Enum):
    DRAFT = "draft"
    SENT = "sent"
    RECEIVED = "received"
    CANCELLED = "cancelled"

class SupplierBase(BaseModel):
    name: str
    contact_email: Optional[str] = None
    lead_time_days: int = 3

class SupplierCreate(SupplierBase):
    pass

class Supplier(SupplierBase):
    id: int

    class Config:
        from_attributes = True

class InventoryBase(BaseModel):
    sku_id: str
    outlet_id: str
    quantity: int
    reorder_point: Optional[int] = 10

class InventoryCreate(InventoryBase):
    pass

class Inventory(InventoryBase):
    id: int
    last_updated: Optional[datetime] = None

    class Config:
        from_attributes = True

class PurchaseOrderBase(BaseModel):
    supplier_id: int
    sku_id: str
    quantity: int
    status: POStatus = POStatus.DRAFT

class PurchaseOrderCreate(PurchaseOrderBase):
    pass

class PurchaseOrder(PurchaseOrderBase):
    id: int
    created_at: Optional[datetime] = None
    supplier: Optional[Supplier] = None

    class Config:
        from_attributes = True

class ReplenishRequest(BaseModel):
    sku_id: str
    outlet_id: str
