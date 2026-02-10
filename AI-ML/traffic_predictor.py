"""
Benameur Python Lab - Professional Series
Smart City: Urban Traffic Predictor (ML)
--------------------------------------
Author: Benameur Mohamed
Entity: Benameur Soft
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import logging

# Configure Logging / إعداد سجل العمليات
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TrafficML")

def generate_synthetic_data(samples=1000):
    """Generates synthetic city traffic data / توليد بيانات مرورية اصطناعية للمدينة"""
    logger.info("📊 Generating training data...")
    time_of_day = np.random.randint(0, 24, samples)
    is_weekend = np.random.randint(0, 2, samples)
    weather_factor = np.random.uniform(0.5, 1.5, samples) # 1.0 is clear, higher is worse weather
    
    # Target: Traffic volume (Vehicles per hour)
    # Base traffic + Rush hour surges + Weekend effect
    rush_hour = np.where((time_of_day >= 7) & (time_of_day <= 9) | (time_of_day >= 16) & (time_of_day <= 18), 500, 100)
    traffic_volume = (rush_hour + (time_of_day * 10) - (is_weekend * 200)) * weather_factor
    
    df = pd.DataFrame({
        'hour': time_of_day,
        'weekend': is_weekend,
        'weather_index': weather_factor,
        'volume': traffic_volume
    })
    return df

class TrafficPredictor:
    """
    ML model to forecast urban congestion levels.
    نموذج تعلم آلي للتنبؤ بمستويات الازدحام الحضري.
    """
    def __init__(self):
        self.model = LinearRegression()
    
    def train(self, data):
        X = data[['hour', 'weekend', 'weather_index']]
        y = data['volume']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        logger.info("🧠 Training model...")
        self.model.fit(X_train, y_train)
        score = self.model.score(X_test, y_test)
        logger.info(f"✅ Training complete. Accuracy Score: {score:.4f}")
        
    def predict_status(self, hour, weekend, weather):
        """Predicts congestion based on parameters / التنبؤ بالازدحام بناءً على المعطيات"""
        prediction = self.model.predict([[hour, weekend, weather]])[0]
        status = "🔴 High Congestion" if prediction > 450 else "🟢 Low Congestion"
        return prediction, status

if __name__ == "__main__":
    # Simulate the ML pipeline
    data = generate_synthetic_data()
    predictor = TrafficPredictor()
    predictor.train(data)
    
    # Test a prediction (Monday at 8 AM, bad weather)
    # تجربة تنبؤ (يوم الإثنين، الساعة 8 صباحاً، طقس سيء)
    h, wkd, wth = 8, 0, 1.4
    pred, status = predictor.predict_status(h, wkd, wth)
    
    print(f"\n--- Benameur-Soft ML Report ---")
    print(f"🕒 Time: {h}:00 | Weekend: {'Yes' if wkd else 'No'}")
    print(f"☁️ Weather Index: {wth}")
    print(f"📈 Predicted Volume: {pred:.2f} vehicles/hour")
    print(f"🚦 Traffic Status: {status}")
