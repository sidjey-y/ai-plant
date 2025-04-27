/**
 * Main JavaScript for AI-Powered Precision Agriculture Assistant
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Auto-close alerts after 5 seconds
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Handle file input for pest detection
    const pestUploadInput = document.getElementById('pest-upload');
    if (pestUploadInput) {
        pestUploadInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(event) {
                    const imgPreview = document.getElementById('pest-image-preview');
                    imgPreview.src = event.target.result;
                    imgPreview.classList.remove('d-none');
                    
                    // Show the analyze button
                    document.getElementById('analyze-pest-btn').classList.remove('d-none');
                };
                reader.readAsDataURL(file);
            }
        });
    }

    // Handle pest detection submission
    const analyzePestBtn = document.getElementById('analyze-pest-btn');
    if (analyzePestBtn) {
        analyzePestBtn.addEventListener('click', function() {
            // Show loading state
            this.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Analyzing...';
            this.disabled = true;
            
            // Get the form and submit
            document.getElementById('pest-detection-form').submit();
        });
    }

    // Soil quality chart initialization (if present on page)
    initializeSoilQualityChart();

    // Field dropdown change handler
    const fieldDropdown = document.getElementById('field-selector');
    if (fieldDropdown) {
        fieldDropdown.addEventListener('change', function() {
            window.location.href = this.value;
        });
    }

    // Time range selector for data charts
    const timeRangeSelector = document.getElementById('time-range-selector');
    if (timeRangeSelector) {
        timeRangeSelector.addEventListener('change', function() {
            // Get current URL
            let url = new URL(window.location);
            
            // Update or add the range parameter
            url.searchParams.set('range', this.value);
            
            // Navigate to the new URL
            window.location.href = url.toString();
        });
    }

    // Handle planting date calculator
    initializePlantingCalculator();

    initPlantAnimations();
    initGrowthEffects();
    initSoilNavigationEffects();
    initLeafCursorEffects();
});

/**
 * Initialize soil quality chart if the element exists
 */
function initializeSoilQualityChart() {
    const soilChartElem = document.getElementById('soil-quality-chart');
    if (!soilChartElem) return;

    // Fetch soil data from API
    fetchSoilData().then(data => {
        if (!data) return;
        
        // Create chart
        const ctx = soilChartElem.getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.timestamps.map(t => {
                    // Format timestamp to show only date or time based on range
                    const date = new Date(t);
                    return date.toLocaleDateString();
                }),
                datasets: [
                    {
                        label: 'Moisture (%)',
                        data: data.moisture,
                        borderColor: 'rgba(54, 162, 235, 1)',
                        backgroundColor: 'rgba(54, 162, 235, 0.1)',
                        fill: true,
                        tension: 0.4
                    },
                    {
                        label: 'pH Level',
                        data: data.ph,
                        borderColor: 'rgba(75, 192, 192, 1)',
                        backgroundColor: 'rgba(75, 192, 192, 0.1)',
                        fill: true,
                        tension: 0.4
                    },
                    {
                        label: 'Nitrogen (ppm)',
                        data: data.nitrogen,
                        borderColor: 'rgba(153, 102, 255, 1)',
                        backgroundColor: 'rgba(153, 102, 255, 0.1)',
                        fill: true,
                        tension: 0.4
                    }
                ]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: false
                    }
                }
            }
        });
    });
}

/**
 * Fetch soil data from API
 */
async function fetchSoilData() {
    try {
        // Get field ID from URL or use default
        const urlParams = new URLSearchParams(window.location.search);
        const fieldId = urlParams.get('field_id') || 1;
        const timeRange = urlParams.get('range') || '7d';
        
        const response = await fetch(`/api/soil/data?field_id=${fieldId}&range=${timeRange}`);
        if (!response.ok) {
            throw new Error('Failed to fetch soil data');
        }
        
        return await response.json();
    } catch (error) {
        console.error('Error fetching soil data:', error);
        return null;
    }
}

/**
 * Initialize planting date calculator
 */
function initializePlantingCalculator() {
    const calculateBtn = document.getElementById('calculate-planting-date');
    if (!calculateBtn) return;
    
    calculateBtn.addEventListener('click', function() {
        // Get form values
        const cropType = document.getElementById('crop-type').value;
        const fieldId = document.getElementById('field-id').value;
        
        if (!cropType) {
            showAlert('Please select a crop type', 'danger');
            return;
        }
        
        // Show loading state
        this.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Calculating...';
        this.disabled = true;
        
        // Make API request
        fetch('/api/planting/optimal-date', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                crop_type: cropType,
                field_id: fieldId
            })
        })
        .then(response => response.json())
        .then(data => {
            // Reset button
            this.innerHTML = 'Calculate';
            this.disabled = false;
            
            // Display results
            const resultsContainer = document.getElementById('planting-results');
            resultsContainer.innerHTML = '';
            
            if (data.error) {
                showAlert(data.error, 'danger');
                return;
            }
            
            const resultHTML = `
                <div class="card mt-4">
                    <div class="card-header bg-success text-white">
                        <h5 class="mb-0">Optimal Planting Schedule for ${data.crop_type}</h5>
                    </div>
                    <div class="card-body">
                        <div class="row">
                            <div class="col-md-6">
                                <h6>Planting Window</h6>
                                <p><strong>Start:</strong> ${data.planting_window.start}</p>
                                <p><strong>Optimal Date:</strong> ${data.planting_window.optimal}</p>
                                <p><strong>End:</strong> ${data.planting_window.end}</p>
                                <p><strong>Confidence:</strong> ${(data.confidence * 100).toFixed(1)}%</p>
                                <p><strong>Days Until Optimal Date:</strong> ${data.days_until_optimal}</p>
                            </div>
                            <div class="col-md-6">
                                <h6>Influencing Factors</h6>
                                <ul class="list-group">
                                    ${data.factors.map(factor => `
                                        <li class="list-group-item d-flex justify-content-between align-items-center">
                                            ${factor.name}: ${factor.value}
                                            <span class="badge bg-${factor.impact === 'positive' ? 'success' : factor.impact === 'negative' ? 'danger' : 'secondary'} rounded-pill">
                                                ${factor.impact}
                                            </span>
                                        </li>
                                    `).join('')}
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            `;
            
            resultsContainer.innerHTML = resultHTML;
        })
        .catch(error => {
            console.error('Error calculating planting date:', error);
            this.innerHTML = 'Calculate';
            this.disabled = false;
            showAlert('Failed to calculate planting date. Please try again.', 'danger');
        });
    });
}

/**
 * Show a Bootstrap alert
 */
function showAlert(message, type = 'info') {
    const alertContainer = document.getElementById('alert-container');
    if (!alertContainer) return;
    
    const alertHTML = `
        <div class="alert alert-${type} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `;
    
    alertContainer.innerHTML = alertHTML;
}

function initPlantAnimations() {
    const plantElements = document.querySelectorAll('.icon-plant, .icon-soil, .icon-water, .icon-nutrient, .icon-ph');
    
    plantElements.forEach(element => {
        element.classList.add('animate-grow');
    });
}

function initGrowthEffects() {
    const cards = document.querySelectorAll('.card');
    
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px)';
            this.style.boxShadow = '0 15px 30px rgba(0, 0, 0, 0.1)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(-5px)';
            this.style.boxShadow = '0 10px 25px rgba(0, 0, 0, 0.1)';
        });
    });

    const buttons = document.querySelectorAll('.btn');
    
    buttons.forEach(button => {
        button.addEventListener('mousedown', function() {
            this.style.transform = 'translateY(0px)';
        });
        
        button.addEventListener('mouseup', function() {
            this.style.transform = 'translateY(-2px)';
        });
    });
}

function initSoilNavigationEffects() {
    const navLinks = document.querySelectorAll('.soil-nav .nav-link');
    
    navLinks.forEach(link => {
        link.addEventListener('mouseenter', function() {
            if (!this.classList.contains('active')) {
                this.style.transform = 'translateX(5px)';
            }
        });
        
        link.addEventListener('mouseleave', function() {
            if (!this.classList.contains('active')) {
                this.style.transform = 'translateX(0)';
            }
        });
    });
}

function initLeafCursorEffects() {
    const elements = document.querySelectorAll('a, button, .clickable');
    
    elements.forEach(element => {
        element.addEventListener('mouseover', function() {
            const leafTrail = document.createElement('div');
            leafTrail.className = 'leaf-trail';
            leafTrail.style.position = 'absolute';
            leafTrail.style.zIndex = '9999';
            leafTrail.style.pointerEvents = 'none';
            leafTrail.style.opacity = '0.7';
            leafTrail.style.transition = 'all 0.5s ease';
            leafTrail.innerHTML = '🌿';
            leafTrail.style.fontSize = '12px';
            
            document.body.appendChild(leafTrail);
            
            setTimeout(() => {
                leafTrail.style.opacity = '0';
                leafTrail.style.transform = 'translateY(-20px) rotate(45deg)';
                
                setTimeout(() => {
                    document.body.removeChild(leafTrail);
                }, 500);
            }, 100);
            
            const rect = this.getBoundingClientRect();
            leafTrail.style.left = (rect.left + rect.width / 2) + 'px';
            leafTrail.style.top = (rect.top + rect.height) + 'px';
        });
    });
}

function randomInRange(min, max) {
    return Math.random() * (max - min) + min;
}

window.updateSoilMoistureVisuals = function(elementId, value) {
    const element = document.getElementById(elementId);
    if (element) {
        let colorClass = 'bg-success';
        
        if (value < 30) {
            colorClass = 'bg-danger';
        } else if (value < 50) {
            colorClass = 'bg-warning';
        }
        
        const progressBar = element.querySelector('.progress-bar');
        if (progressBar) {
            progressBar.className = 'progress-bar ' + colorClass;
            progressBar.style.width = value + '%';
            progressBar.setAttribute('aria-valuenow', value);
        }
        
        const badge = element.querySelector('.badge');
        if (badge) {
            badge.className = 'badge ' + colorClass;
            badge.textContent = value + '%';
        }
    }
};

document.addEventListener('scroll', function() {
    const vineElements = document.querySelectorAll('.vine-border');
    
    vineElements.forEach(element => {
        const rect = element.getBoundingClientRect();
        const isInViewport = rect.top < window.innerHeight && rect.bottom >= 0;
        
        if (isInViewport && !element.classList.contains('animated')) {
            element.classList.add('animated');
            element.style.transition = 'all 1.5s ease';
            setTimeout(() => {
                element.style.opacity = '1';
            }, 300);
        }
    });
}); 