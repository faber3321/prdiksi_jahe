from flask import Blueprint, render_template
from utils.data_loader import load_historical_data
import pandas as pd

bp = Blueprint('analysis', __name__)

@bp.route('/analysis')
def correlation():
    """Price correlation and analysis"""
    # Load historical data
    data = load_historical_data()
    
    # Perform basic analysis
    analysis_data = {
        'total_records': len(data),
        'date_range': {
            'start': data['date'].min().strftime('%Y-%m-%d'),
            'end': data['date'].max().strftime('%Y-%m-%d')
        },
        'price_stats': {
            'min': data['price'].min(),
            'max': data['price'].max(),
            'avg': data['price'].mean(),
            'std': data['price'].std()
        }
    }
    
    return render_template('analysis/correlation.html', analysis=analysis_data)

@bp.route('/analysis/trends')
def trends():
    """Price trends analysis"""
    # Load historical data
    data = load_historical_data()
    
    # Calculate trends
    data['price_change'] = data['price'].pct_change() * 100
    data['moving_avg'] = data['price'].rolling(window=7).mean()
    
    # Get recent trends
    recent_trends = data.tail(30).to_dict('records')
    
    return render_template('analysis/trends.html', trends=recent_trends)

@bp.route('/analysis/comparison')
def comparison():
    """Model comparison"""
    # This would normally compare different model performances
    comparison_data = {
        'models': [
            {'name': 'LSTM', 'accuracy': 95.2, 'mape': 4.8},
            {'name': 'RNN', 'accuracy': 92.1, 'mape': 7.9},
            {'name': 'GRU', 'accuracy': 94.5, 'mape': 5.5}
        ]
    }
    
    return render_template('analysis/comparison.html', comparison=comparison_data)