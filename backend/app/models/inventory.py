from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.db.base import Base
import enum

class POStatus(str, enum.Enum):
    DRAFT = "draft"
    SENT = "sent"
    RECEIVED = "received"
    CANCELLED = "cancelled"

class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    contact_email = Column(String)
    lead_time_days = Column(Integer, default=3)

class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    sku_id = Column(String, index=True, nullable=False)
    outlet_id = Column(String, index=True, nullable=False)
    quantity = Column(Integer, default=0)
    reorder_point = Column(Integer, default=10)
    last_updated = Column(DateTime)

class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"

    id = Column(Integer, primary_key=True, index=True)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"))
    sku_id = Column(String, index=True, nullable=False)
    quantity = Column(Integer, nullable=False)
    status = Column(String, default=POStatus.DRAFT)
    created_at = Column(DateTime)
    
    supplier = relationship("Supplier")
