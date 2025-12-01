# Ginger Price Prediction Web Application

A web application that predicts ginger prices using machine learning models (RNN, LSTM, GRU) with real-time weather data integration. The application provides an intuitive dashboard for farmers and traders to make informed decisions about ginger prices.

## Features

- **Price Prediction**: Uses advanced ML models (RNN, LSTM, GRU) to predict ginger prices
- **Real-time Weather Integration**: Incorporates weather data that affects ginger prices
- **Interactive Dashboard**: User-friendly interface with charts and analytics
- **Historical Data Analysis**: Trend analysis and price history visualization
- **User Authentication**: Secure login and registration system

## Tech Stack

- **Backend**: Python Flask
- **Data Processing**: Pandas, NumPy
- **Frontend**: HTML5, CSS3, JavaScript ES6
- **Visualization**: Chart.js
- **Template Engine**: Jinja2
- **Database**: SQLite (with SQLAlchemy)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ginger-price-prediction
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
```
Edit the `.env` file with your configuration.

5. Run the application:
```bash
python app.py
```

## Project Structure

```
ginger-price-prediction/
├── app.py                          # Main Flask application
├── config.py                       # Application configuration
├── requirements.txt                # Python dependencies
├── .env                           # Environment variables
├── .gitignore                     # Git ignore file
├── README.md                      # Project documentation
│
├── data/                          # Data directory
│   ├── raw/                       # Raw data files
│   ├── processed/                 # Processed data
│   └── predictions/               # Prediction results
│
├── models/                        # ML models
│   ├── saved_models/              # Trained models
│   └── training scripts           # Model training code
│
├── utils/                         # Utility functions
├── routes/                        # Flask routes
├── static/                        # Static files (CSS, JS, Images)
├── templates/                     # HTML templates
├── database/                      # Database models
├── tests/                         # Unit tests
├── notebooks/                     # Jupyter notebooks
├── logs/                          # Application logs
└── docs/                          # Documentation
```

## API Endpoints

- `GET /` - Main dashboard
- `POST /predict` - Price prediction endpoint
- `GET /api/prices` - Historical prices API
- `GET /api/weather` - Weather data API

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.