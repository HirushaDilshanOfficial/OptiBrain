from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class CustomerSegmentBase(BaseModel):
    name: str
    description: Optional[str] = None

class CustomerSegmentCreate(CustomerSegmentBase):
    pass

class CustomerSegment(CustomerSegmentBase):
    id: int

    class Config:
        from_attributes = True

class CustomerBase(BaseModel):
    full_name: Optional[str] = None
    email: str
    phone_number: Optional[str] = None

class CustomerCreate(CustomerBase):
    pass

class Customer(CustomerBase):
    id: int
    created_at: datetime
    segment_id: Optional[int] = None
    segment: Optional[CustomerSegment] = None

    class Config:
        from_attributes = True

class SegmentationRequest(BaseModel):
    customer_ids: Optional[list[int]] = None # If None, segment all
