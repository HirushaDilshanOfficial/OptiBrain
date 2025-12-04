from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Enum
from sqlalchemy.orm import relationship
from app.db.base import Base
import enum
from datetime import datetime

class ChannelType(str, enum.Enum):
    ONLINE = "online"
    RETAIL = "retail"
    MARKETPLACE = "marketplace"

class FulfillmentNode(Base):
    __tablename__ = "fulfillment_nodes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    location = Column(String) # e.g., "New York, NY"
    is_active = Column(Boolean, default=True)
    priority = Column(Integer, default=1) # Lower number = higher priority

class Channel(Base):
    __tablename__ = "channels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    type = Column(String, default=ChannelType.ONLINE)
    api_key = Column(String, unique=True) # For external integrations

class OrderSource(Base):
    __tablename__ = "order_sources"

    id = Column(Integer, primary_key=True, index=True)
    external_order_id = Column(String, index=True, nullable=False)
    channel_id = Column(Integer, ForeignKey("channels.id"))
    sku_id = Column(String, index=True, nullable=False)
    quantity = Column(Integer, nullable=False)
    status = Column(String, default="pending")
    fulfillment_node_id = Column(Integer, ForeignKey("fulfillment_nodes.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    channel = relationship("Channel")
    fulfillment_node = relationship("FulfillmentNode")
