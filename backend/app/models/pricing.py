from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from app.db.base import Base
from datetime import datetime

class PricingRule(Base):
    __tablename__ = "pricing_rules"

    id = Column(Integer, primary_key=True, index=True)
    sku_id = Column(String, index=True, nullable=False)
    min_price = Column(Float, nullable=False)
    max_price = Column(Float, nullable=False)
    max_daily_increase_pct = Column(Float, default=0.1) # e.g., 10%
    is_active = Column(Boolean, default=True)

class PriceLog(Base):
    __tablename__ = "price_logs"

    id = Column(Integer, primary_key=True, index=True)
    sku_id = Column(String, index=True, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    old_price = Column(Float, nullable=False)
    new_price = Column(Float, nullable=False)
    reason = Column(String) # e.g., "Demand Surge", "Competitor Match"
    model_version = Column(String)
