import numpy as np

class ReplenishmentOptimizer:
    def __init__(self):
        pass

    def optimize_inventory(self, forecast_mean, forecast_std, lead_time_days, service_level=0.95):
        """
        Calculate Reorder Point (ROP) and Order Quantity.
        ROP = (Avg Daily Demand * Lead Time) + Safety Stock
        Safety Stock = Z * StdDev * sqrt(Lead Time)
        """
        # Z-score for service level (approximate)
        z_score = 1.645 if service_level == 0.95 else 1.96 # 95% vs 97.5%
        
        avg_daily_demand = forecast_mean
        std_dev_demand = forecast_std
        
        safety_stock = z_score * std_dev_demand * np.sqrt(lead_time_days)
        reorder_point = (avg_daily_demand * lead_time_days) + safety_stock
        
        # Simple EOQ-like logic for order quantity (mocked for now)
        # In reality, we'd use holding costs and ordering costs
        economic_order_quantity = avg_daily_demand * 14 # 2 weeks of stock
        
        return {
            "reorder_point": int(np.ceil(reorder_point)),
            "safety_stock": int(np.ceil(safety_stock)),
            "suggested_order_quantity": int(np.ceil(economic_order_quantity))
        }
