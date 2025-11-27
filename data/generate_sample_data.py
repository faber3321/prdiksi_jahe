import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_sample_price_data():
    """
    Fungsi untuk menghasilkan data harga jahe historis sample
    """
    # Membuat data selama 2 tahun terakhir
    start_date = datetime.now() - timedelta(days=730)  # 2 tahun
    dates = pd.date_range(start=start_date, end=datetime.now(), freq='D')
    
    # Membuat tren harga dasar dengan fluktuasi
    base_price = 20000  # Harga dasar Rp 20,000
    trend = np.linspace(base_price, base_price * 1.2, len(dates))  # Tren naik sedikit
    
    # Menambahkan noise untuk membuatnya realistis
    daily_change = np.random.normal(0, 1000, size=len(dates))  # Perubahan harian acak
    seasonal_factor = 1 + 0.1 * np.sin(2 * np.pi * np.arange(len(dates)) / 365.25)  # Faktor musiman
    
    prices = trend * seasonal_factor + np.cumsum(daily_change)
    
    # Pastikan harga tidak negatif
    prices = np.maximum(prices, 10000)
    
    # Membuat DataFrame
    df = pd.DataFrame({
        'date': dates,
        'price': prices.astype(int)
    })
    
    # Membuat direktori jika belum ada
    os.makedirs('data', exist_ok=True)
    
    # Menyimpan ke file CSV
    df.to_csv('data/jahe_historical_prices.csv', index=False)
    print(f"Data harga jahe historis telah dibuat: {len(df)} baris data")
    print(f"Periode: {df['date'].min()} sampai {df['date'].max()}")
    print(f"Harga rata-rata: Rp {df['price'].mean():,.0f}")
    print(f"Harga tertinggi: Rp {df['price'].max():,.0f}")
    print(f"Harga terendah: Rp {df['price'].min():,.0f}")
    
    return df

def generate_sample_weather_data():
    """
    Fungsi untuk menghasilkan data cuaca sample yang relevan dengan harga jahe
    """
    start_date = datetime.now() - timedelta(days=730)  # 2 tahun
    dates = pd.date_range(start=start_date, end=datetime.now(), freq='D')
    
    # Data cuaca sederhana
    temperatures = np.random.normal(27, 3, size=len(dates))  # Suhu rata-rata 27°C
    rainfall = np.random.exponential(5, size=len(dates))     # Curah hujan
    humidity = np.random.normal(75, 10, size=len(dates))    # Kelembapan
    
    # Batasi nilai-nilai ke rentang realistis
    temperatures = np.clip(temperatures, 20, 35)
    rainfall = np.clip(rainfall, 0, 50)
    humidity = np.clip(humidity, 40, 95)
    
    df = pd.DataFrame({
        'date': dates,
        'temperature': np.round(temperatures, 2),
        'rainfall': np.round(rainfall, 2),
        'humidity': np.round(humidity, 2)
    })
    
    df.to_csv('data/weather_data.csv', index=False)
    print(f"Data cuaca sample telah dibuat: {len(df)} baris data")
    
    return df

if __name__ == "__main__":
    print("Menghasilkan data sample...")
    price_df = generate_sample_price_data()
    weather_df = generate_sample_weather_data()
    
    print("\nData berhasil dibuat di folder /data/")