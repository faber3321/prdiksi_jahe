from flask import Flask, render_template, jsonify, request
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout
from tensorflow.keras.optimizers import Adam
import json
import requests
import os
from datetime import datetime, timedelta
import math

app = Flask(__name__)

# Konfigurasi API cuaca (gunakan API key Anda sendiri)
WEATHER_API_KEY = os.environ.get('OPENWEATHER_API_KEY', 'default_api_key')
WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"

# Fungsi untuk mendapatkan data cuaca
def get_weather_data(city="Jakarta"):
    """Mengambil data cuaca dari OpenWeatherMap API"""
    try:
        params = {
            'q': city,
            'appid': WEATHER_API_KEY,
            'units': 'metric'
        }
        response = requests.get(WEATHER_API_URL, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        print(f"Error getting weather data: {e}")
        return None

# Fungsi untuk membuat model RNN
def create_rnn_model(input_shape):
    """Membuat model RNN untuk prediksi harga jahe"""
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=input_shape))
    model.add(Dropout(0.2))
    
    model.add(LSTM(units=50, return_sequences=True))
    model.add(Dropout(0.2))
    
    model.add(LSTM(units=50, return_sequences=False))
    model.add(Dropout(0.2))
    
    model.add(Dense(units=25))
    model.add(Dense(units=1))
    
    model.compile(optimizer=Adam(learning_rate=0.001), loss='mean_squared_error')
    return model

# Fungsi untuk melatih model
def train_model(data):
    """Melatih model RNN dengan data historis"""
    # Persiapan data
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data.reshape(-1, 1))
    
    # Membuat dataset untuk training
    x_train = []
    y_train = []
    time_step = 60  # Menggunakan 60 hari sebelumnya untuk memprediksi
    
    for i in range(time_step, len(scaled_data)):
        x_train.append(scaled_data[i-time_step:i, 0])
        y_train.append(scaled_data[i, 0])
        
    x_train, y_train = np.array(x_train), np.array(y_train)
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
    
    # Membuat dan melatih model
    model = create_rnn_model((x_train.shape[1], 1))
    model.fit(x_train, y_train, batch_size=1, epochs=1, verbose=0)
    
    return model, scaler

# Route untuk halaman utama
@app.route('/')
def index():
    return render_template('index.html')

# Fungsi untuk memuat data harga jahe historis
def load_historical_data():
    """Memuat data harga jahe historis dari file CSV"""
    try:
        df = pd.read_csv('data/jahe_historical_prices.csv')
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')
        return df
    except FileNotFoundError:
        # Jika file tidak ditemukan, buat data dummy
        dates = pd.date_range(start=datetime.now() - timedelta(days=365), end=datetime.now(), freq='D')
        prices = np.random.uniform(15000, 25000, size=len(dates))
        df = pd.DataFrame({'date': dates, 'price': prices})
        return df

# Route untuk mendapatkan data prediksi
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Mendapatkan data dari request
        data = request.get_json()
        days = data.get('days', 7)  # Default prediksi 7 hari ke depan
        
        # Memuat data historis
        df = load_historical_data()
        historical_prices = df['price'].values
        
        # Melatih model
        model, scaler = train_model(historical_prices)
        
        # Memprediksi harga untuk beberapa hari ke depan
        last_60_days = historical_prices[-60:]
        last_60_days_scaled = scaler.transform(last_60_days.reshape(-1, 1))
        
        predictions = []
        current_input = last_60_days_scaled.reshape(1, -1, 1)
        
        for _ in range(days):
            pred = model.predict(current_input, verbose=0)
            predictions.append(float(scaler.inverse_transform(pred)[0][0]))
            
            # Update input untuk prediksi berikutnya
            pred_reshaped = pred.reshape(1, 1, 1)
            current_input = np.append(current_input[:, 1:, :], pred_reshaped, axis=1)
        
        # Mendapatkan data cuaca terkini
        weather_data = get_weather_data()
        
        result = {
            'predictions': predictions,
            'dates': [(datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(1, days+1)],
            'current_weather': weather_data,
            'historical_dates': df['date'].dt.strftime('%Y-%m-%d').tolist()[-60:],  # 60 hari terakhir
            'historical_prices': df['price'].tolist()[-60:]  # 60 harga terakhir
        }
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route untuk mendapatkan data analitik
@app.route('/analytics')
def analytics():
    try:
        # Memuat data historis
        df = load_historical_data()
        
        # Menghitung statistik
        avg_price = float(df['price'].mean())
        min_price = float(df['price'].min())
        max_price = float(df['price'].max())
        current_price = float(df['price'].iloc[-1])
        
        # Menentukan tren harga (berdasarkan perbandingan 30 hari terakhir dengan 60 hari sebelumnya)
        recent_30 = df['price'].tail(30).mean()
        prev_30 = df['price'].tail(60).head(30).mean()
        
        if recent_30 > prev_30:
            price_trend = 'up'
            trend_text = 'Naik'
        elif recent_30 < prev_30:
            price_trend = 'down'
            trend_text = 'Turun'
        else:
            price_trend = 'stable'
            trend_text = 'Stabil'
        
        # Mendapatkan data cuaca terkini
        weather_data = get_weather_data()
        
        data = {
            'price_trend': price_trend,
            'trend_text': trend_text,
            'avg_price': avg_price,
            'min_price': min_price,
            'max_price': max_price,
            'current_price': current_price,
            'total_data_points': len(df),
            'date_range': {
                'start': df['date'].min().strftime('%Y-%m-%d'),
                'end': df['date'].max().strftime('%Y-%m-%d')
            },
            'current_weather': weather_data
        }
        
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)