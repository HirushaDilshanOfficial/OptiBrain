import pandas as pd
from prophet import Prophet

class DemandForecaster:
    def __init__(self):
        self.model = None

    def train(self, data):
        """
        Train the Prophet model.
        data: List of dicts with 'ds' (date string) and 'y' (value)
        """
        df = pd.DataFrame(data)
        df['ds'] = pd.to_datetime(df['ds'])
        
        self.model = Prophet()
        self.model.fit(df)

    def predict(self, days=7):
        """
        Generate forecast.
        """
        if not self.model:
            raise ValueError("Model not trained")
            
        future = self.model.make_future_dataframe(periods=days)
        forecast = self.model.predict(future)
        
        # Return only future predictions
        future_forecast = forecast.tail(days)
        
        return future_forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].to_dict('records')
