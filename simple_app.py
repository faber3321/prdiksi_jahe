from flask import Flask, render_template, jsonify, request
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import os

app = Flask(__name__)

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

# Fungsi untuk membuat prediksi sederhana tanpa ML
def simple_prediction_model(historical_prices, days=7):
    """
    Fungsi prediksi sederhana tanpa menggunakan ML
    Menggunakan pendekatan berbasis tren dan rata-rata bergerak
    """
    if len(historical_prices) < 30:
        # Jika data terlalu sedikit, kembalikan nilai acak di sekitar rata-rata
        avg_price = np.mean(historical_prices)
        predictions = []
        for i in range(days):
            # Tambahkan sedikit variasi acak
            variation = np.random.normal(0, avg_price * 0.02)  # 2% variasi
            pred_price = max(avg_price + variation, 10000)  # Harga minimum 10,000
            predictions.append(pred_price)
        return predictions
    
    # Ambil 30 hari terakhir untuk menghitung tren
    recent_prices = historical_prices[-30:]
    recent_avg = np.mean(recent_prices)
    
    # Hitung tren (naik/turun) dari 15 hari terakhir vs 15 hari sebelumnya
    first_half = recent_prices[:15]
    second_half = recent_prices[15:]
    first_avg = np.mean(first_half)
    second_avg = np.mean(second_half)
    
    trend_factor = (second_avg - first_avg) / len(recent_prices)  # Tren harian
    
    # Buat prediksi
    predictions = []
    last_price = historical_prices[-1]
    
    for i in range(days):
        # Prediksi berdasarkan tren + sedikit variasi acak
        trend_pred = last_price + (trend_factor * (i + 1))
        variation = np.random.normal(0, recent_avg * 0.015)  # 1.5% variasi
        pred_price = max(trend_pred + variation, 10000)
        predictions.append(pred_price)
    
    return predictions

# Route untuk halaman utama
@app.route('/')
def index():
    return render_template('index.html')

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
        
        # Membuat prediksi menggunakan fungsi sederhana
        predictions = simple_prediction_model(historical_prices, days)
        
        # Format hasil prediksi
        result = {
            'predictions': [float(p) for p in predictions],
            'dates': [(datetime.now() + timedelta(days=i+1)).strftime('%Y-%m-%d') for i in range(days)],
            'historical_dates': df['date'].dt.strftime('%Y-%m-%d').tolist()[-60:],  # 60 hari terakhir
            'historical_prices': [float(p) for p in df['price'].tolist()[-60:]]  # 60 harga terakhir
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
        if len(df) >= 60:
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
        else:
            price_trend = 'stable'
            trend_text = 'Stabil'
        
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
            }
        }
        
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)