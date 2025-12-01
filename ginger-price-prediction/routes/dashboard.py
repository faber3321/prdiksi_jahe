from flask import Blueprint, render_template, jsonify
from utils.data_loader import load_historical_data
from utils.weather_api import get_current_weather
import pandas as pd

bp = Blueprint('dashboard', __name__)

@bp.route('/dashboard')
def index():
    """Main dashboard page"""
    # Load sample data for the dashboard
    try:
        # This would typically load from your database or data files
        current_price = 34500  # Sample current price
        predicted_price = 36200  # Sample predicted price
        avg_temperature = 28
        rainfall = 45
        
        # Load historical data for charts
        historical_data = load_sample_data()
        
        return render_template('dashboard/index.html', 
                             current_price=current_price,
                             predicted_price=predicted_price,
                             avg_temperature=avg_temperature,
                             rainfall=rainfall,
                             historical_data=historical_data)
    except Exception as e:
        # In case of error, render with default values
        return render_template('dashboard/index.html')

def load_sample_data():
    """Load sample data for dashboard charts"""
    # This is sample data - in a real app, this would come from your data source
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    prices = [18000, 19500, 21000, 22500, 24000, 25500, 
              27000, 28500, 30000, 31500, 33000, 34500]
    
    return {
        'months': months,
        'prices': prices
    }