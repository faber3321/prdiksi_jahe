# Dokumentasi Teknis - Prediksi Harga Jahe

## Arsitektur Sistem

Aplikasi ini terdiri dari beberapa komponen utama:

### Backend (Python Flask)
- **Framework**: Flask untuk menangani permintaan HTTP
- **Machine Learning**: TensorFlow/Keras untuk model RNN (LSTM)
- **Preprocessing**: Scikit-learn untuk normalisasi data
- **Data**: Pandas untuk manipulasi data

### Frontend (HTML/CSS/JavaScript)
- **Template**: Jinja2 templates untuk rendering HTML
- **Visualisasi**: Chart.js untuk grafik interaktif
- **UI**: HTML5, CSS3, dan JavaScript ES6

## Struktur Proyek

```
/workspace/
├── app.py                 # Aplikasi Flask utama
├── requirements.txt       # Dependensi Python
├── setup.sh              # Script setup otomatis
├── README.md             # Dokumentasi pengguna
├── TECHNICAL_DOCS.md     # Dokumentasi teknis ini
├── templates/
│   └── index.html        # Template halaman utama
├── static/
│   ├── css/
│   │   └── style.css     # Styling halaman
│   └── js/
│       └── script.js     # Logika frontend
├── models/               # Model ML (akan dibuat saat pelatihan)
├── data/
│   ├── jahe_historical_prices.csv  # Data harga historis
│   ├── weather_data.csv            # Data cuaca (akan digunakan nanti)
│   └── generate_sample_data.py     # Script pembuatan data sample
```

## Algoritma Prediksi

### Model RNN (LSTM)
Model menggunakan arsitektur LSTM (Long Short-Term Memory) yang merupakan jenis RNN yang efektif untuk prediksi deret waktu:

1. **Lapisan Input**: Menerima urutan data harga harian
2. **LSTM pertama**: 50 unit dengan dropout 0.2
3. **LSTM kedua**: 50 unit dengan dropout 0.2  
4. **LSTM ketiga**: 50 unit dengan dropout 0.2 (tidak mengembalikan urutan)
5. **Dense layers**: 25 unit dan 1 unit output

### Proses Pelatihan
1. Data harga dinormalisasi menggunakan MinMaxScaler
2. Dibuat urutan input dengan panjang 60 hari
3. Model dilatih selama 1 epoch (dalam implementasi sebenarnya bisa lebih)
4. Prediksi dilakukan secara iteratif untuk hari-hari mendatang

## API Endpoints

### `GET /`
- Mengembalikan halaman utama aplikasi

### `POST /predict`
- Menerima jumlah hari untuk prediksi
- Mengembalikan array prediksi harga dan tanggal

**Contoh permintaan:**
```json
{
  "days": 7
}
```

**Contoh respons:**
```json
{
  "predictions": [25000, 25200, 25100, ...],
  "dates": ["2025-11-28", "2025-11-29", ...],
  "historical_dates": [...],
  "historical_prices": [...]
}
```

### `GET /analytics`
- Mengembalikan statistik harga dan tren pasar

## Integrasi Cuaca

Aplikasi ini dirancang untuk mengintegrasikan data cuaca melalui OpenWeatherMap API:

- Endpoint cuaca: `http://api.openweathermap.org/data/2.5/weather`
- Parameter: kota dan API key
- Data yang diambil: suhu, kelembapan, curah hujan (akan digunakan dalam model)

## Dashboard Analitik

Dashboard menyediakan:

1. **Statistik Harga**:
   - Rata-rata, tertinggi, dan terendah
   - Tren harga (naik/turun/stabil)

2. **Visualisasi**:
   - Grafik harga historis dan prediksi
   - Perbandingan harga sebenarnya dan prediksi

3. **Data Cuaca**:
   - Suhu, kelembapan, deskripsi cuaca
   - Kecepatan angin

## Penggunaan

### Instalasi
1. Jalankan `bash setup.sh` untuk instalasi otomatis
2. Atau instal manual:
   ```bash
   python -m venv venv
   pip install -r requirements.txt
   python data/generate_sample_data.py
   ```

### Menjalankan Aplikasi
```bash
python app.py
```

Aplikasi akan berjalan di `http://localhost:5000`

## Pengembangan Lebih Lanjut

Fitur yang dapat ditambahkan:
- Integrasi data cuaca nyata ke model prediksi
- Model ensemble untuk akurasi lebih tinggi
- Database permanen (PostgreSQL/MySQL)
- Autentikasi pengguna
- Penjadwalan pelatihan otomatis
- Ekspor laporan dalam berbagai format