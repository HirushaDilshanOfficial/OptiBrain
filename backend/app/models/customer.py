from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    phone_number = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Segmentation fields (updated by ML)
    segment_id = Column(Integer, ForeignKey("customer_segments.id"), nullable=True)
    
    segment = relationship("CustomerSegment", back_populates="customers")

class CustomerSegment(Base):
    __tablename__ = "customer_segments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True) # e.g., "VIP", "At Risk"
    description = Column(String)
    
    customers = relationship("Customer", back_populates="segment")
