document.addEventListener('DOMContentLoaded', function() {
    // Inisialisasi chart
    let predictionChart = null;
    
    // Ambil elemen-elemen DOM
    const predictBtn = document.getElementById('predict-btn');
    const daysInput = document.getElementById('days');
    const predictionList = document.getElementById('prediction-list');
    const avgPriceEl = document.getElementById('avg-price');
    const maxPriceEl = document.getElementById('max-price');
    const minPriceEl = document.getElementById('min-price');
    const priceTrendEl = document.getElementById('price-trend');
    const weatherDataEl = document.getElementById('weather-data');
    
    // Event listener untuk tombol prediksi
    predictBtn.addEventListener('click', makePrediction);
    
    // Fungsi untuk membuat prediksi
    async function makePrediction() {
        const days = parseInt(daysInput.value);
        
        if (days < 1 || days > 30) {
            alert('Mohon masukkan jumlah hari antara 1-30');
            return;
        }
        
        try {
            // Tampilkan loading
            predictionList.innerHTML = '<div class="loading">Memproses prediksi...</div>';
            
            // Kirim permintaan ke backend
            const response = await fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ days: days })
            });
            
            if (!response.ok) {
                throw new Error('Gagal mendapatkan prediksi');
            }
            
            const data = await response.json();
            
            // Tampilkan hasil prediksi
            displayPredictions(data);
            
            // Dapatkan data analitik
            getAnalytics();
        } catch (error) {
            console.error('Error:', error);
            predictionList.innerHTML = `<div class="error">Error: ${error.message}</div>`;
        }
    }
    
    // Fungsi untuk menampilkan hasil prediksi
    function displayPredictions(data) {
        // Hapus konten sebelumnya
        predictionList.innerHTML = '';
        
        // Tampilkan data prediksi dalam bentuk daftar
        data.dates.forEach((date, index) => {
            const price = data.predictions[index];
            const predictionItem = document.createElement('div');
            predictionItem.className = 'prediction-item';
            predictionItem.innerHTML = `
                <span class="prediction-date">${date}</span> 
                <span class="prediction-price">Rp ${price.toLocaleString('id-ID')}</span>
            `;
            predictionList.appendChild(predictionItem);
        });
        
        // Update chart dengan data historis dan prediksi
        updateChart(data.dates, data.predictions, data.historical_dates, data.historical_prices);
    }
    
    // Fungsi untuk update chart
    function updateChart(dates, prices, historical_dates = [], historical_prices = []) {
        const ctx = document.getElementById('predictionChart').getContext('2d');
        
        // Hapus chart sebelumnya jika ada
        if (predictionChart) {
            predictionChart.destroy();
        }
        
        // Siapkan data untuk chart
        const chartData = {
            labels: [...historical_dates, ...dates],
            datasets: []
        };
        
        // Tambahkan data historis jika tersedia
        if (historical_dates.length > 0 && historical_prices.length > 0) {
            chartData.datasets.push({
                label: 'Harga Historis (Rp)',
                data: [...historical_prices, ...Array(dates.length).fill(NaN)],
                borderColor: '#a7c957',
                backgroundColor: 'rgba(167, 201, 87, 0.1)',
                borderWidth: 2,
                borderDash: [5, 5], // Garis putus-putus untuk historis
                fill: false,
                tension: 0.3
            });
        }
        
        // Tambahkan data prediksi
        chartData.datasets.push({
            label: 'Prediksi Harga Jahe (Rp)',
            data: [...Array(historical_dates.length).fill(NaN), ...prices],
            borderColor: '#6a994e',
            backgroundColor: 'rgba(106, 153, 78, 0.1)',
            borderWidth: 3,
            fill: true,
            tension: 0.3
        });
        
        // Buat chart baru
        predictionChart = new Chart(ctx, {
            type: 'line',
            data: chartData,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: 'Grafik Harga Historis dan Prediksi Harga Jahe'
                    },
                    legend: {
                        position: 'top',
                    }
                },
                scales: {
                    y: {
                        beginAtZero: false,
                        title: {
                            display: true,
                            text: 'Harga (Rp)'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Tanggal'
                        }
                    }
                }
            }
        });
    }
    
    // Fungsi untuk mendapatkan data analitik
    async function getAnalytics() {
        try {
            const response = await fetch('/analytics');
            if (!response.ok) {
                throw new Error('Gagal mendapatkan data analitik');
            }
            
            const data = await response.json();
            
            // Update elemen-elemen analitik
            avgPriceEl.textContent = `Rp ${data.avg_price.toLocaleString('id-ID')}`;
            maxPriceEl.textContent = `Rp ${data.max_price.toLocaleString('id-ID')}`;
            minPriceEl.textContent = `Rp ${data.min_price.toLocaleString('id-ID')}`;
            
            // Update tren harga dengan indikator visual
            let trendText = '';
            let trendClass = '';
            if (data.price_trend === 'up') {
                trendText = 'Naik';
                trendClass = 'trend-up';
            } else if (data.price_trend === 'down') {
                trendText = 'Turun';
                trendClass = 'trend-down';
            } else {
                trendText = 'Stabil';
                trendClass = 'trend-neutral';
            }
            
            priceTrendEl.innerHTML = `<span class="${trendClass}">${trendText}</span>`;
            
            // Update data cuaca jika tersedia
            if (data.current_weather) {
                displayWeatherData(data.current_weather);
            }
        } catch (error) {
            console.error('Error getting analytics:', error);
            weatherDataEl.innerHTML = `<div class="error">Error: ${error.message}</div>`;
        }
    }
    
    // Fungsi untuk menampilkan data cuaca
    function displayWeatherData(weather) {
        if (!weather || weather.cod !== 200) {
            weatherDataEl.innerHTML = '<p>Data cuaca tidak tersedia</p>';
            return;
        }
        
        const weatherHTML = `
            <div class="weather-data-item">
                <strong>Kota:</strong> ${weather.name}, ${weather.sys.country}
            </div>
            <div class="weather-data-item">
                <strong>Suhu:</strong> ${weather.main.temp}°C (Min: ${weather.main.temp_min}°C, Max: ${weather.main.temp_max}°C)
            </div>
            <div class="weather-data-item">
                <strong>Kelembapan:</strong> ${weather.main.humidity}%
            </div>
            <div class="weather-data-item">
                <strong>Deskripsi:</strong> ${weather.weather[0].description}
            </div>
            <div class="weather-data-item">
                <strong>Kecepatan Angin:</strong> ${weather.wind.speed} m/s
            </div>
        `;
        
        weatherDataEl.innerHTML = weatherHTML;
    }
    
    // Load data analitik saat halaman dimuat
    getAnalytics();
});

// Fungsi untuk format angka ke format Rupiah
function formatRupiah(angka) {
    return 'Rp ' + angka.toFixed(0).replace(/(\d)(?=(\d{3})+(?!\d))/g, '$1.');
}