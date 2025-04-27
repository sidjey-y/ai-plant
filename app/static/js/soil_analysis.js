document.addEventListener('DOMContentLoaded', function() {
    // Initialize gauge charts
    initializeGauges();
    
    // Initialize nutrient levels chart
    initializeNutrientChart();
    
    // Initialize historical data chart
    initializeHistoricalChart();
    
    // Initialize soil health map
    initializeSoilMap();
    
    // Setup event listeners
    setupEventListeners();
});

/**
 * Initialize gauge charts for soil health metrics
 */
function initializeGauges() {
    // This function would typically use a gauge library like Gauge.js
    // For now, we'll simulate the gauges with placeholder functions
    
    // Example implementation with a mock gauge library:
    if (typeof Gauge !== 'undefined') {
        // Overall health gauge
        const overallHealthGauge = new Gauge(document.getElementById('overallHealthGauge'));
        overallHealthGauge.setOptions({
            angle: 0.15,
            lineWidth: 0.44,
            radiusScale: 1,
            pointer: {
                length: 0.6,
                strokeWidth: 0.035,
                color: '#000000'
            },
            staticLabels: {
                font: "10px sans-serif",
                labels: [0, 20, 40, 60, 80, 100],
                color: "#000000",
                fractionDigits: 0
            },
            staticZones: [
                {strokeStyle: "#F03E3E", min: 0, max: 30},
                {strokeStyle: "#FFDD00", min: 30, max: 70},
                {strokeStyle: "#30B32D", min: 70, max: 100}
            ],
            renderTicks: {
                divisions: 5,
                divWidth: 1.1,
                divLength: 0.7,
                divColor: '#333333',
                subDivisions: 3,
                subLength: 0.5,
                subWidth: 0.6,
                subColor: '#666666'
            }
        });
        overallHealthGauge.setValue(78);
        
        // pH gauge
        const pHGauge = new Gauge(document.getElementById('pHGauge'));
        pHGauge.setOptions({
            angle: 0.15,
            lineWidth: 0.44,
            radiusScale: 0.8,
            pointer: {
                length: 0.6,
                strokeWidth: 0.035,
                color: '#000000'
            },
            staticLabels: {
                font: "10px sans-serif",
                labels: [0, 2, 4, 6, 8, 10, 14],
                color: "#000000",
                fractionDigits: 1
            },
            staticZones: [
                {strokeStyle: "#F03E3E", min: 0, max: 5.5},
                {strokeStyle: "#FFDD00", min: 5.5, max: 6.0},
                {strokeStyle: "#30B32D", min: 6.0, max: 7.0},
                {strokeStyle: "#FFDD00", min: 7.0, max: 7.5},
                {strokeStyle: "#F03E3E", min: 7.5, max: 14}
            ],
            renderTicks: {
                divisions: 7,
                divWidth: 1.1,
                divLength: 0.7,
                divColor: '#333333',
                subDivisions: 3,
                subLength: 0.5,
                subWidth: 0.6,
                subColor: '#666666'
            }
        });
        pHGauge.setValue(6.5);
        
        // Moisture gauge
        const moistureGauge = new Gauge(document.getElementById('moistureGauge'));
        moistureGauge.setOptions({
            angle: 0.15,
            lineWidth: 0.44,
            radiusScale: 0.8,
            pointer: {
                length: 0.6,
                strokeWidth: 0.035,
                color: '#000000'
            },
            staticLabels: {
                font: "10px sans-serif",
                labels: [0, 20, 40, 60, 80, 100],
                color: "#000000",
                fractionDigits: 0
            },
            staticZones: [
                {strokeStyle: "#F03E3E", min: 0, max: 20},
                {strokeStyle: "#FFDD00", min: 20, max: 40},
                {strokeStyle: "#30B32D", min: 40, max: 60},
                {strokeStyle: "#FFDD00", min: 60, max: 80},
                {strokeStyle: "#F03E3E", min: 80, max: 100}
            ],
            renderTicks: {
                divisions: 5,
                divWidth: 1.1,
                divLength: 0.7,
                divColor: '#333333',
                subDivisions: 4,
                subLength: 0.5,
                subWidth: 0.6,
                subColor: '#666666'
            }
        });
        moistureGauge.setValue(42);
        
        // Organic matter gauge
        const organicMatterGauge = new Gauge(document.getElementById('organicMatterGauge'));
        organicMatterGauge.setOptions({
            angle: 0.15,
            lineWidth: 0.44,
            radiusScale: 0.8,
            pointer: {
                length: 0.6,
                strokeWidth: 0.035,
                color: '#000000'
            },
            staticLabels: {
                font: "10px sans-serif",
                labels: [0, 1, 2, 3, 4, 5],
                color: "#000000",
                fractionDigits: 1
            },
            staticZones: [
                {strokeStyle: "#F03E3E", min: 0, max: 1.5},
                {strokeStyle: "#FFDD00", min: 1.5, max: 3},
                {strokeStyle: "#30B32D", min: 3, max: 5}
            ],
            renderTicks: {
                divisions: 5,
                divWidth: 1.1,
                divLength: 0.7,
                divColor: '#333333',
                subDivisions: 5,
                subLength: 0.5,
                subWidth: 0.6,
                subColor: '#666666'
            }
        });
        organicMatterGauge.setValue(3.2);
    } else {
        console.warn("Gauge library not loaded. Using fallback display.");
        // Fallback: simple representation using color blocks
        document.querySelectorAll('.soil-gauge, .soil-health-gauge').forEach(gauge => {
            gauge.style.width = '60px';
            gauge.style.height = '60px';
            gauge.style.borderRadius = '50%';
            gauge.style.backgroundColor = '#4CAF50';
            gauge.style.display = 'flex';
            gauge.style.alignItems = 'center';
            gauge.style.justifyContent = 'center';
            gauge.style.color = 'white';
            gauge.style.fontWeight = 'bold';
            
            // Different colors based on ID
            if (gauge.id === 'pHGauge') {
                gauge.style.backgroundColor = '#4CAF50';
                gauge.innerText = '6.5';
            } else if (gauge.id === 'moistureGauge') {
                gauge.style.backgroundColor = '#FFC107';
                gauge.innerText = '42%';
            } else if (gauge.id === 'organicMatterGauge') {
                gauge.style.backgroundColor = '#4CAF50';
                gauge.innerText = '3.2%';
            } else if (gauge.id === 'overallHealthGauge') {
                gauge.style.backgroundColor = '#4CAF50';
                gauge.innerText = '78';
            }
        });
    }
}

/**
 * Initialize nutrient levels chart
 */
function initializeNutrientChart() {
    const nutrientCtx = document.getElementById('nutrientLevelsChart').getContext('2d');
    
    // Sample data - in a real application, this would come from an API
    const nutrientData = {
        labels: ['Nitrogen', 'Phosphorus', 'Potassium', 'Calcium', 'Magnesium', 'Sulfur'],
        datasets: [{
            label: 'Current Level',
            data: [25, 45, 180, 1500, 150, 12],
            backgroundColor: '#4CAF50',
            borderColor: '#388E3C',
            borderWidth: 1
        }, {
            label: 'Ideal Minimum',
            data: [40, 30, 200, 1000, 100, 10],
            type: 'line',
            borderColor: '#FF9800',
            borderDash: [5, 5],
            borderWidth: 2,
            fill: false,
            pointRadius: 0
        }, {
            label: 'Ideal Maximum',
            data: [80, 50, 300, 2000, 250, 20],
            type: 'line',
            borderColor: '#F44336',
            borderDash: [5, 5],
            borderWidth: 2,
            fill: false,
            pointRadius: 0
        }]
    };
    
    const nutrientChart = new Chart(nutrientCtx, {
        type: 'bar',
        data: nutrientData,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Value (ppm)'
                    }
                }
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const label = context.dataset.label || '';
                            let value = context.parsed.y || 0;
                            
                            // Add unit based on nutrient
                            let unit = 'ppm';
                            if (context.dataset.label === 'Organic Matter') {
                                unit = '%';
                            }
                            
                            return `${label}: ${value} ${unit}`;
                        }
                    }
                }
            }
        }
    });
}

/**
 * Initialize historical soil data chart
 */
function initializeHistoricalChart() {
    const historyCtx = document.getElementById('historicalSoilDataChart').getContext('2d');
    
    // Sample data - in a real application, this would come from an API
    const historicalData = {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        datasets: [{
            label: 'pH Level',
            data: [6.2, 6.3, 6.4, 6.5, 6.5, 6.5],
            borderColor: '#2196F3',
            backgroundColor: 'rgba(33, 150, 243, 0.1)',
            borderWidth: 2,
            fill: true
        }, {
            label: 'Organic Matter (%)',
            data: [2.8, 2.9, 3.0, 3.1, 3.2, 3.2],
            borderColor: '#4CAF50',
            backgroundColor: 'rgba(76, 175, 80, 0.1)',
            borderWidth: 2,
            fill: true
        }]
    };
    
    const historyChart = new Chart(historyCtx, {
        type: 'line',
        data: historicalData,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: false
                }
            },
            interaction: {
                mode: 'index',
                intersect: false
            }
        }
    });
    
    // Make chart accessible to event handlers
    window.historyChart = historyChart;
}

/**
 * Initialize soil health map
 */
function initializeSoilMap() {
    // This would typically use a mapping library like Leaflet.js
    // For now, we'll just create a placeholder
    
    const mapElement = document.getElementById('soilHealthMap');
    
    if (typeof L !== 'undefined') {
        // If Leaflet.js is available
        const map = L.map(mapElement).setView([51.505, -0.09], 13);
        
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(map);
        
        // Add a sample heatmap overlay
        // This is just an example - in a real app you'd use real data
        const points = [
            [51.505, -0.09, 0.8],
            [51.51, -0.1, 0.5],
            [51.51, -0.08, 0.3],
            [51.5, -0.08, 0.9]
        ];
        
        if (L.heatLayer) {
            L.heatLayer(points, {
                radius: 25,
                blur: 15,
                maxZoom: 17,
                gradient: {0.4: 'blue', 0.6: 'yellow', 0.8: 'orange', 1.0: 'red'}
            }).addTo(map);
        }
    } else {
        // Create a simple placeholder with CSS grid
        mapElement.innerHTML = '';
        mapElement.style.display = 'grid';
        mapElement.style.gridTemplateColumns = 'repeat(10, 1fr)';
        mapElement.style.gridTemplateRows = 'repeat(10, 1fr)';
        
        // Create a grid of colored cells to simulate a soil health map
        for (let i = 0; i < 100; i++) {
            const cell = document.createElement('div');
            
            // Random health level
            const healthLevel = Math.random();
            if (healthLevel < 0.2) {
                cell.style.backgroundColor = '#F44336'; // Red - poor
            } else if (healthLevel < 0.5) {
                cell.style.backgroundColor = '#FFC107'; // Yellow - moderate
            } else {
                cell.style.backgroundColor = '#4CAF50'; // Green - good
            }
            
            cell.style.opacity = 0.7 + (Math.random() * 0.3);
            mapElement.appendChild(cell);
        }
    }
}

/**
 * Setup all event listeners for interactive elements
 */
function setupEventListeners() {
    // Field selector change handler
    const fieldSelector = document.getElementById('fieldSelector');
    if (fieldSelector) {
        fieldSelector.addEventListener('change', function() {
            const fieldId = this.value;
            fetchSoilDataForField(fieldId);
        });
    }
    
    // Time range buttons for historical chart
    document.querySelectorAll('[data-timerange]').forEach(button => {
        button.addEventListener('click', function() {
            document.querySelectorAll('[data-timerange]').forEach(btn => {
                btn.classList.remove('active');
            });
            this.classList.add('active');
            
            const timeRange = this.getAttribute('data-timerange');
            fetchHistoricalData(timeRange);
        });
    });
    
    // Submit analysis request
    const submitButton = document.getElementById('submitAnalysisRequest');
    if (submitButton) {
        submitButton.addEventListener('click', function() {
            const form = document.getElementById('requestAnalysisForm');
            const fieldSelect = document.getElementById('fieldSelect');
            const analysisType = document.getElementById('analysisType');
            
            if (fieldSelect.value && analysisType.value) {
                submitAnalysisRequest({
                    fieldId: fieldSelect.value,
                    analysisType: analysisType.value,
                    notes: document.getElementById('requestNotes').value,
                    urgent: document.getElementById('urgentCheck').checked
                });
                
                // Reset form and close modal
                const modal = bootstrap.Modal.getInstance(document.getElementById('requestAnalysisModal'));
                if (modal) {
                    modal.hide();
                }
                form.reset();
            } else {
                showAlert('Please fill in all required fields', 'danger');
            }
        });
    }
}

/**
 * Fetch soil data for a specific field
 * @param {string} fieldId - The ID of the field to fetch data for
 */
function fetchSoilDataForField(fieldId) {
    showAlert('Loading data for field ' + fieldId, 'info');
    
    // In a real application, this would make an API call
    // For now, we'll just simulate it with a timeout
    setTimeout(() => {
        // Update charts and displays with new data
        // This is just simulated data for demonstration
        if (fieldId === 'all') {
            // Default data already shown
            showAlert('Showing data for all fields', 'success');
        } else {
            // Sample data for a specific field - in reality this would come from an API
            const fieldData = {
                ph: 6.8,
                moisture: 38,
                organicMatter: 2.9,
                nutrients: {
                    nitrogen: 35,
                    phosphorus: 40,
                    potassium: 210,
                    calcium: 1400,
                    magnesium: 130,
                    sulfur: 15
                }
            };
            
            // Update nutrient chart
            const nutrientChart = Chart.getChart('nutrientLevelsChart');
            if (nutrientChart) {
                nutrientChart.data.datasets[0].data = [
                    fieldData.nutrients.nitrogen,
                    fieldData.nutrients.phosphorus,
                    fieldData.nutrients.potassium,
                    fieldData.nutrients.calcium,
                    fieldData.nutrients.magnesium,
                    fieldData.nutrients.sulfur
                ];
                nutrientChart.update();
            }
            
            // Update gauges if available
            if (typeof Gauge !== 'undefined') {
                // This would update the gauges with the field-specific values
            } else {
                // Update our simple fallback displays
                document.getElementById('pHGauge').innerText = fieldData.ph.toFixed(1);
                document.getElementById('moistureGauge').innerText = fieldData.moisture + '%';
                document.getElementById('organicMatterGauge').innerText = fieldData.organicMatter.toFixed(1) + '%';
            }
            
            showAlert('Data updated for selected field', 'success');
        }
    }, 1000);
}

/**
 * Fetch historical data for a specific time range
 * @param {string} timeRange - The time range to fetch data for (month, quarter, year)
 */
function fetchHistoricalData(timeRange) {
    // In a real application, this would make an API call
    // For now, we'll just simulate it with predefined data
    
    let labels, phData, organicData;
    
    if (timeRange === 'month') {
        labels = ['1', '5', '10', '15', '20', '25', '30'];
        phData = [6.3, 6.4, 6.4, 6.5, 6.5, 6.5, 6.5];
        organicData = [3.0, 3.0, 3.1, 3.1, 3.2, 3.2, 3.2];
    } else if (timeRange === 'quarter') {
        labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'];
        phData = [6.2, 6.3, 6.4, 6.5, 6.5, 6.5];
        organicData = [2.8, 2.9, 3.0, 3.1, 3.2, 3.2];
    } else {
        labels = ['Jan', 'Mar', 'May', 'Jul', 'Sep', 'Nov'];
        phData = [6.0, 6.1, 6.3, 6.4, 6.5, 6.5];
        organicData = [2.5, 2.7, 2.9, 3.0, 3.1, 3.2];
    }
    
    if (window.historyChart) {
        window.historyChart.data.labels = labels;
        window.historyChart.data.datasets[0].data = phData;
        window.historyChart.data.datasets[1].data = organicData;
        window.historyChart.update();
    }
}

/**
 * Submit an analysis request
 * @param {Object} requestData - The analysis request data
 */
function submitAnalysisRequest(requestData) {
    // In a real application, this would make an API call
    // For now, we'll just log it and show a success message
    console.log('Analysis request submitted:', requestData);
    
    // Simulate API call
    setTimeout(() => {
        showAlert('Analysis request submitted successfully!', 'success');
    }, 500);
}

/**
 * Show an alert message
 * @param {string} message - The message to display
 * @param {string} type - The alert type (success, info, warning, danger)
 */
function showAlert(message, type) {
    const alertHTML = `
        <div class="alert alert-${type} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `;
    
    const alertContainer = document.createElement('div');
    alertContainer.className = 'position-fixed top-0 end-0 p-3';
    alertContainer.style.zIndex = '1050';
    alertContainer.innerHTML = alertHTML;
    
    document.body.appendChild(alertContainer);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        const alert = alertContainer.querySelector('.alert');
        if (alert) {
            alert.classList.remove('show');
            setTimeout(() => alertContainer.remove(), 150);
        }
    }, 5000);
} 