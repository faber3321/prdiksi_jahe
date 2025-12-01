from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    predictions = db.relationship('Prediction', backref='user', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Prediction(db.Model):
    __tablename__ = 'predictions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    model_type = db.Column(db.String(20), nullable=False)  # 'lstm', 'rnn', 'gru'
    current_price = db.Column(db.Float, nullable=False)
    predicted_price = db.Column(db.Float, nullable=False)
    prediction_date = db.Column(db.Date, nullable=False)
    actual_price = db.Column(db.Float)  # Actual price when known
    accuracy = db.Column(db.Float)  # Accuracy percentage
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Prediction {self.id} - {self.model_type}>'

class GingerPrice(db.Model):
    __tablename__ = 'ginger_prices'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    price = db.Column(db.Float, nullable=False)  # Price per kg in local currency
    source = db.Column(db.String(100))  # Source of the data
    location = db.Column(db.String(100))  # Market location
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<GingerPrice {self.date} - {self.price}>'

class WeatherData(db.Model):
    __tablename__ = 'weather_data'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    temperature = db.Column(db.Float)  # Average temperature
    humidity = db.Column(db.Float)  # Humidity percentage
    rainfall = db.Column(db.Float)  # Rainfall in mm
    location = db.Column(db.String(100))  # Location
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<WeatherData {self.date} - Temp: {self.temperature}>'

def init_db(app):
    """
    Initialize the database with the app context
    """
    with app.app_context():
        db.init_app(app)
        db.create_all()