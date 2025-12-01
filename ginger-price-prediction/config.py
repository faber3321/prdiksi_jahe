import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # Secret key for session management
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard-to-guess-string-for-ginger-prediction'
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///ginger_prediction.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # API Keys (to be set in .env file)
    WEATHER_API_KEY = os.environ.get('WEATHER_API_KEY')
    
    # Upload folder for CSV files
    UPLOAD_FOLDER = 'data/raw'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Model configuration
    MODEL_PATH = 'models/saved_models/'
    DATA_PATH = 'data/'
    PREDICTION_PATH = 'data/predictions/'
    
    # Application settings
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    TESTING = False