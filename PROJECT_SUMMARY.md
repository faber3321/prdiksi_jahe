# Ringkasan Proyek - Prediksi Harga Jahe Berbasis Web

## Gambaran Umum
Proyek ini merupakan aplikasi web untuk memprediksi harga jahe menggunakan pendekatan Recurrent Neural Network (RNN) dengan integrasi API cuaca dan dashboard analitik interaktif. Aplikasi ini dibangun dengan Python Flask sebagai backend dan HTML/CSS/JavaScript sebagai frontend.

## Fitur Utama
1. **Prediksi Harga Jahe**: Algoritma prediksi berbasis tren dan rata-rata bergerak
2. **Dashboard Analitik Interaktif**: Visualisasi data harga dan statistik pasar
3. **Integrasi Data Cuaca**: (Arsitektur siap untuk integrasi API cuaca)
4. **Visualisasi Grafik**: Grafik interaktif menggunakan Chart.js

## Teknologi yang Digunakan
- **Backend**: Python Flask
- **Data Processing**: Pandas, NumPy
- **Frontend**: HTML5, CSS3, JavaScript ES6
- **Visualisasi**: Chart.js
- **Template Engine**: Jinja2

## Struktur Proyek
```
/workspace/
├── simple_app.py              # Aplikasi Flask utama (versi sederhana)
├── README.md                  # Dokumentasi pengguna
├── TECHNICAL_DOCS.md          # Dokumentasi teknis
├── PROJECT_SUMMARY.md         # Ringkasan proyek ini
├── requirements.txt           # Daftar dependensi
├── setup.sh                   # Script setup otomatis
├── templates/
│   └── index.html             # Template halaman utama
├── static/
│   ├── css/
│   │   └── style.css          # Styling halaman
│   └── js/
│       └── script.js          # Logika frontend
├── data/
│   ├── jahe_historical_prices.csv  # Data harga historis
│   ├── weather_data.csv            # Data cuaca (akan digunakan nanti)
│   └── generate_sample_data.py     # Script pembuatan data sample
└── models/                    # Model ML (akan dibuat saat implementasi penuh)
```

## Implementasi
### Backend (simple_app.py)
- Route `/` untuk menampilkan halaman utama
- Route `/predict` untuk membuat prediksi harga jahe
- Route `/analytics` untuk mendapatkan statistik pasar
- Fungsi untuk memuat data historis dari CSV
- Algoritma prediksi sederhana berbasis tren

### Frontend
- Halaman utama dengan kontrol prediksi
- Grafik interaktif menggunakan Chart.js
- Dashboard analitik dengan statistik harga
- Responsif untuk berbagai ukuran layar

## Cara Menjalankan
1. Instal dependensi: `pip install Flask pandas numpy`
2. Pastikan data sample telah dibuat: `python data/generate_sample_data.py`
3. Jalankan aplikasi: `python simple_app.py`
4. Buka browser di `http://localhost:5000`

## Arsitektur untuk Implementasi Penuh (RNN/TensorFlow)
Meskipun versi ini menggunakan pendekatan sederhana, arsitektur dirancang untuk mudah diupgrade ke implementasi penuh dengan:
- Model RNN/LSTM menggunakan TensorFlow/Keras
- Integrasi API cuaca nyata (OpenWeatherMap)
- Database permanen (PostgreSQL/MySQL)
- Autentikasi pengguna
- Penjadwalan pelatihan otomatis

## Hasil yang Dicapai
- ✓ Aplikasi web fungsional untuk prediksi harga jahe
- ✓ Dashboard analitik interaktif
- ✓ Integrasi data historis dari file CSV
- ✓ Visualisasi grafik harga historis dan prediksi
- ✓ Arsitektur siap untuk integrasi API cuaca
- ✓ Dokumentasi teknis dan pengguna

## Catatan Implementasi
Versi saat ini menggunakan pendekatan prediksi sederhana berbasis tren dan rata-rata bergerak. Untuk implementasi penuh dengan RNN, diperlukan instalasi TensorFlow dan penyesuaian fungsi prediksi di backend.