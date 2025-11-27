#!/bin/bash

echo "Mempersiapkan lingkungan untuk aplikasi Prediksi Harga Jahe..."

# Membuat virtual environment
echo "Membuat virtual environment..."
python -m venv venv

# Menginstal dependensi
echo "Menginstal dependensi..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    echo "File requirements.txt tidak ditemukan!"
    exit 1
fi

# Membuat direktori jika belum ada
echo "Membuat direktori yang diperlukan..."
mkdir -p data models static/css static/js templates

# Menghasilkan data sample
echo "Menghasilkan data sample..."
python data/generate_sample_data.py

echo "Instalasi selesai!"
echo ""
echo "Untuk menjalankan aplikasi, gunakan perintah:"
echo "  source venv/bin/activate  # di Linux/Mac"
echo "  OR"
echo "  venv\Scripts\activate     # di Windows"
echo "  python app.py"