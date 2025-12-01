// Main JavaScript file for Ginger Price Prediction App

// Initialize tooltips
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize charts if they exist on the page
    initializeCharts();
});

// Function to initialize charts
function initializeCharts() {
    // Check if chart canvases exist on the page
    const priceChartCanvas = document.getElementById('priceChart');
    if (priceChartCanvas) {
        createPriceChart(priceChartCanvas);
    }
    
    const predictionChartCanvas = document.getElementById('predictionChart');
    if (predictionChartCanvas) {
        createPredictionChart(predictionChartCanvas);
    }
}

// Function to create price chart
function createPriceChart(canvas) {
    const ctx = canvas.getContext('2d');
    
    // Sample data - in a real app, this would come from the backend
    const data = {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        datasets: [{
            label: 'Ginger Price (Rp/kg)',
            data: [18000, 19500, 21000, 22500, 24000, 25500, 27000, 28500, 30000, 31500, 33000, 34500],
            borderColor: '#d2691e',
            backgroundColor: 'rgba(210, 105, 30, 0.1)',
            tension: 0.4,
            fill: true
        }]
    };
    
    const config = {
        type: 'line',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: 'Ginger Price Trend (Last 12 Months)'
                },
                legend: {
                    display: true,
                    position: 'top',
                }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    title: {
                        display: true,
                        text: 'Price (Rp/kg)'
                    }
                }
            }
        }
    };
    
    new Chart(ctx, config);
}

// Function to create prediction chart
function createPredictionChart(canvas) {
    const ctx = canvas.getContext('2d');
    
    // Sample prediction data
    const data = {
        labels: ['Today', 'Tomorrow', '+2 Days', '+3 Days', '+4 Days', '+5 Days'],
        datasets: [{
            label: 'Predicted Price (Rp/kg)',
            data: [34500, 35200, 35800, 36500, 37200, 37900],
            borderColor: '#cd853f',
            backgroundColor: 'rgba(205, 133, 63, 0.2)',
            tension: 0.4,
            fill: true
        }, {
            label: 'Actual Price (Rp/kg)',
            data: [34500, null, null, null, null, null],
            borderColor: '#d2691e',
            backgroundColor: 'rgba(210, 105, 30, 0.2)',
            tension: 0.4,
            fill: true
        }]
    };
    
    const config = {
        type: 'line',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: 'Price Prediction (Next 5 Days)'
                },
                legend: {
                    display: true,
                    position: 'top',
                }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    title: {
                        display: true,
                        text: 'Price (Rp/kg)'
                    }
                }
            }
        }
    };
    
    new Chart(ctx, config);
}

// Function to handle form submissions with loading state
function submitFormWithLoading(formId, submitBtnId) {
    const form = document.getElementById(formId);
    const submitBtn = document.getElementById(submitBtnId);
    
    if (form && submitBtn) {
        // Show loading state
        const originalText = submitBtn.innerHTML;
        submitBtn.innerHTML = '<span class="loading"></span> Processing...';
        submitBtn.disabled = true;
        
        // Submit form
        form.submit();
        
        // In a real app, you would handle the form submission with AJAX
        // and reset the button after receiving the response
    }
}

// Function to format currency
function formatCurrency(amount) {
    return new Intl.NumberFormat('id-ID', {
        style: 'currency',
        currency: 'IDR',
        minimumFractionDigits: 0
    }).format(amount);
}

// Function to show notification
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    // Add to body
    document.body.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.parentNode.removeChild(notification);
        }
    }, 5000);
}

// Function to validate form inputs
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return false;
    
    let isValid = true;
    const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.classList.add('is-invalid');
            isValid = false;
        } else {
            input.classList.remove('is-invalid');
        }
    });
    
    return isValid;
}

// Function to handle API calls
async function apiCall(url, options = {}) {
    try {
        const response = await fetch(url, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API call failed:', error);
        showNotification('An error occurred while processing your request.', 'danger');
        throw error;
    }
}

// Export functions for use in other modules (if using modules)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        initializeCharts,
        createPriceChart,
        createPredictionChart,
        submitFormWithLoading,
        formatCurrency,
        showNotification,
        validateForm,
        apiCall
    };
}