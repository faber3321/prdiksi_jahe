from flask import Blueprint, render_template, request, jsonify
from models.train_model import predict_ginger_price
import pandas as pd

bp = Blueprint('prediction', __name__)

@bp.route('/predict', methods=['GET', 'POST'])
def predict_price():
    """Price prediction page"""
    if request.method == 'POST':
        try:
            # Get form data
            days_ahead = int(request.form.get('days_ahead', 1))
            model_type = request.form.get('model_type', 'lstm')
            
            # Make prediction using the model
            prediction = predict_with_model(days_ahead, model_type)
            
            return render_template('prediction/results.html', 
                                 prediction=prediction, 
                                 days_ahead=days_ahead,
                                 model_type=model_type)
        except Exception as e:
            error_message = f"Error making prediction: {str(e)}"
            return render_template('prediction/predict.html', error=error_message)
    
    # GET request - show prediction form
    return render_template('prediction/predict.html')

@bp.route('/prediction/history')
def history():
    """Show prediction history"""
    # This would load prediction history from database
    prediction_history = get_prediction_history()
    return render_template('prediction/history.html', history=prediction_history)

@bp.route('/api/predict', methods=['POST'])
def api_predict():
    """API endpoint for price prediction"""
    try:
        data = request.get_json()
        days_ahead = data.get('days_ahead', 1)
        model_type = data.get('model_type', 'lstm')
        
        prediction = predict_with_model(days_ahead, model_type)
        
        return jsonify({
            'success': True,
            'prediction': prediction,
            'days_ahead': days_ahead,
            'model_type': model_type
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

def predict_with_model(days_ahead=1, model_type='lstm'):
    """Make prediction using the selected model"""
    # This is a placeholder - in a real app, this would call your trained model
    # For now, return sample data
    from datetime import datetime, timedelta
    
    current_price = 34500  # Sample current price
    daily_change = 700     # Sample daily increase
    
    predictions = []
    for i in range(1, days_ahead + 1):
        future_date = datetime.now() + timedelta(days=i)
        predicted_price = current_price + (daily_change * i)
        
        predictions.append({
            'date': future_date.strftime('%Y-%m-%d'),
            'predicted_price': predicted_price,
            'model_used': model_type.upper()
        })
    
    return {
        'current_price': current_price,
        'predictions': predictions,
        'model_used': model_type.upper(),
        'accuracy': 98.5  # Sample accuracy
    }

def get_prediction_history():
    """Get prediction history from database"""
    # This would query the database for prediction history
    # For now, return sample data
    return [
        {
            'date': '2025-12-01',
            'model_used': 'LSTM',
            'predicted_price': 34200,
            'actual_price': 34500,
            'accuracy': 98.7,
            'status': 'Accurate'
        },
        {
            'date': '2025-11-30',
            'model_used': 'RNN',
            'predicted_price': 33800,
            'actual_price': 34100,
            'accuracy': 98.1,
            'status': 'Accurate'
        },
        {
            'date': '2025-11-29',
            'model_used': 'GRU',
            'predicted_price': 34600,
            'actual_price': 34300,
            'accuracy': 97.8,
            'status': 'Moderate'
        }
    ]