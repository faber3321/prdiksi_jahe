from flask import Blueprint, render_template
from utils.weather_api import get_current_weather, get_weather_forecast

bp = Blueprint('weather', __name__)

@bp.route('/weather')
def current_weather():
    """Current weather information"""
    weather_data = get_current_weather()
    return render_template('weather/current.html', weather=weather_data)

@bp.route('/weather/forecast')
def forecast():
    """Weather forecast"""
    forecast_data = get_weather_forecast()
    return render_template('weather/forecast.html', forecast=forecast_data)