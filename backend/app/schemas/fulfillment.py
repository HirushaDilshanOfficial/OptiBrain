from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class ChannelType(str, Enum):
    ONLINE = "online"
    RETAIL = "retail"
    MARKETPLACE = "marketplace"

class FulfillmentNodeBase(BaseModel):
    name: str
    location: Optional[str] = None
    is_active: bool = True
    priority: int = 1

class FulfillmentNodeCreate(FulfillmentNodeBase):
    pass

class FulfillmentNode(FulfillmentNodeBase):
    id: int

    class Config:
        from_attributes = True

class ChannelBase(BaseModel):
    name: str
    type: ChannelType = ChannelType.ONLINE

class ChannelCreate(ChannelBase):
    pass

class Channel(ChannelBase):
    id: int
    api_key: Optional[str] = None

    class Config:
        from_attributes = True

class OrderSourceBase(BaseModel):
    external_order_id: str
    channel_id: int
    sku_id: str
    quantity: int

class OrderSourceCreate(OrderSourceBase):
    pass

class OrderSource(OrderSourceBase):
    id: int
    status: str
    fulfillment_node_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True

class RoutingRequest(BaseModel):
    order_id: int
