import requests
import os
from config import Config
from datetime import datetime

def get_current_weather(city="Jakarta"):
    """
    Get current weather data from API
    """
    try:
        # Using OpenWeatherMap API as an example
        api_key = Config.WEATHER_API_KEY
        if not api_key:
            # Return sample data if no API key is provided
            return get_sample_weather_data(city)
        
        url = f"http://api.openweathermap.org/data/2.5/weather"
        params = {
            'q': city,
            'appid': api_key,
            'units': 'metric'
        }
        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            return {
                'city': data['name'],
                'temperature': data['main']['temp'],
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'description': data['weather'][0]['description'],
                'timestamp': datetime.now().isoformat()
            }
        else:
            # Return sample data in case of API error
            return get_sample_weather_data(city)
    
    except Exception as e:
        print(f"Error getting weather data: {str(e)}")
        return get_sample_weather_data(city)

def get_weather_forecast(city="Jakarta", days=5):
    """
    Get weather forecast data
    """
    try:
        # Using OpenWeatherMap API as an example
        api_key = Config.WEATHER_API_KEY
        if not api_key:
            # Return sample forecast data if no API key is provided
            return get_sample_forecast_data(city, days)
        
        url = f"http://api.openweathermap.org/data/2.5/forecast"
        params = {
            'q': city,
            'appid': api_key,
            'units': 'metric'
        }
        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            forecast = []
            for item in data['list'][:days]:
                forecast.append({
                    'date': item['dt_txt'],
                    'temperature': item['main']['temp'],
                    'humidity': item['main']['humidity'],
                    'description': item['weather'][0]['description']
                })
            return forecast
        else:
            # Return sample forecast data in case of API error
            return get_sample_forecast_data(city, days)
    
    except Exception as e:
        print(f"Error getting weather forecast: {str(e)}")
        return get_sample_forecast_data(city, days)

def get_sample_weather_data(city="Jakarta"):
    """
    Get sample weather data for demonstration
    """
    import random
    
    return {
        'city': city,
        'temperature': round(random.uniform(25, 35), 1),  # Random temp between 25-35°C
        'humidity': random.randint(60, 90),  # Random humidity between 60-90%
        'pressure': random.randint(1000, 1020),  # Random pressure
        'description': random.choice(['sunny', 'cloudy', 'rainy', 'partly cloudy']),
        'timestamp': datetime.now().isoformat()
    }

def get_sample_forecast_data(city="Jakarta", days=5):
    """
    Get sample weather forecast data for demonstration
    """
    import random
    from datetime import timedelta
    
    forecast = []
    for i in range(days):
        future_date = datetime.now() + timedelta(days=i)
        forecast.append({
            'date': future_date.strftime('%Y-%m-%d %H:%M:%S'),
            'temperature': round(random.uniform(25, 35), 1),
            'humidity': random.randint(60, 90),
            'description': random.choice(['sunny', 'cloudy', 'rainy', 'partly cloudy'])
        })
    
    return forecast

def get_historical_weather(start_date, end_date, city="Jakarta"):
    """
    Get historical weather data for a date range
    """
    try:
        # This would normally call a weather API that provides historical data
        # For demo purposes, we'll generate sample data
        from datetime import datetime, timedelta
        
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        
        weather_data = []
        current_date = start
        day_count = 0
        
        while current_date <= end:
            import random
            weather_data.append({
                'date': current_date.strftime('%Y-%m-%d'),
                'temperature': round(random.uniform(22, 38), 1),
                'humidity': random.randint(50, 95),
                'rainfall': round(random.uniform(0, 20), 1) if random.random() > 0.7 else 0
            })
            current_date += timedelta(days=1)
            day_count += 1
        
        return weather_data
    
    except Exception as e:
        print(f"Error getting historical weather: {str(e)}")
        return []