import pandas as pd
import os
from config import Config

def load_historical_data():
    """
    Load historical ginger price data from CSV file
    """
    try:
        # Path to the raw data file
        data_path = os.path.join(Config.DATA_PATH, 'raw', 'harga_jahe_2020_2024.csv')
        
        # Check if file exists
        if not os.path.exists(data_path):
            # Return sample data if file doesn't exist
            return create_sample_data()
        
        # Load the data
        df = pd.read_csv(data_path)
        
        # Basic data validation
        if df.empty:
            return create_sample_data()
        
        # Ensure required columns exist
        required_columns = ['date', 'price']
        for col in required_columns:
            if col not in df.columns:
                return create_sample_data()
        
        # Convert date column to datetime
        df['date'] = pd.to_datetime(df['date'])
        
        # Sort by date
        df = df.sort_values('date')
        
        return df
    
    except Exception as e:
        print(f"Error loading historical data: {str(e)}")
        return create_sample_data()

def create_sample_data():
    """
    Create sample data for demonstration purposes
    """
    import pandas as pd
    from datetime import datetime, timedelta
    import numpy as np
    
    # Generate sample dates for the last 12 months
    dates = []
    prices = []
    
    start_date = datetime.now() - timedelta(days=365)
    for i in range(365):
        current_date = start_date + timedelta(days=i)
        dates.append(current_date)
        
        # Generate somewhat realistic price data with trend and seasonality
        base_price = 25000
        trend = i * 10  # Slight upward trend
        seasonal = 3000 * np.sin(2 * np.pi * i / 365.25 * 2)  # Seasonal variation
        noise = np.random.normal(0, 1000)  # Random noise
        
        price = base_price + trend + seasonal + noise
        prices.append(max(price, 10000))  # Ensure minimum price
    
    df = pd.DataFrame({
        'date': dates,
        'price': prices
    })
    
    return df

def load_weather_data():
    """
    Load weather data that affects ginger prices
    """
    try:
        # Path to the weather data file
        data_path = os.path.join(Config.DATA_PATH, 'raw', 'data_cuaca_2020_2024.csv')
        
        # Check if file exists
        if not os.path.exists(data_path):
            # Return sample weather data if file doesn't exist
            return create_sample_weather_data()
        
        # Load the data
        df = pd.read_csv(data_path)
        
        # Basic data validation
        if df.empty:
            return create_sample_weather_data()
        
        # Ensure required columns exist
        required_columns = ['date', 'temperature', 'rainfall', 'humidity']
        for col in required_columns:
            if col not in df.columns:
                return create_sample_weather_data()
        
        # Convert date column to datetime
        df['date'] = pd.to_datetime(df['date'])
        
        # Sort by date
        df = df.sort_values('date')
        
        return df
    
    except Exception as e:
        print(f"Error loading weather data: {str(e)}")
        return create_sample_weather_data()

def create_sample_weather_data():
    """
    Create sample weather data for demonstration purposes
    """
    import pandas as pd
    from datetime import datetime, timedelta
    import numpy as np
    
    # Generate sample dates for the last 12 months
    dates = []
    temperatures = []
    rainfalls = []
    humidities = []
    
    start_date = datetime.now() - timedelta(days=365)
    for i in range(365):
        current_date = start_date + timedelta(days=i)
        dates.append(current_date)
        
        # Generate somewhat realistic weather data
        base_temp = 28  # Base temperature in Celsius
        temp_seasonal = 5 * np.sin(2 * np.pi * i / 365.25)  # Seasonal temperature variation
        temp_noise = np.random.normal(0, 2)  # Random temperature noise
        temp = base_temp + temp_seasonal + temp_noise
        temperatures.append(max(temp, 15))  # Ensure minimum temperature
        
        # Rainfall with seasonal pattern
        base_rain = 20  # Base rainfall in mm
        rain_seasonal = 30 * np.sin(2 * np.pi * i / 365.25 * 2 + np.pi)  # Rainy season pattern
        rain_noise = np.random.exponential(5)  # Random rainfall noise (exponential for occasional heavy rain)
        rain = max(base_rain + rain_seasonal + rain_noise, 0)
        rainfalls.append(rain)
        
        # Humidity based on temperature and rainfall
        humidity = 60 + (28 - temp) * 1.5 + (rain - 20) * 0.5 + np.random.normal(0, 5)
        humidities.append(max(min(humidity, 100), 30))  # Keep between 30% and 100%
    
    df = pd.DataFrame({
        'date': dates,
        'temperature': temperatures,
        'rainfall': rainfalls,
        'humidity': humidities
    })
    
    return df