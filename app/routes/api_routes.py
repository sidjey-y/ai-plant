from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required
import os
import json
from datetime import datetime, timedelta
import random

from app.services.agrimetrics_api import AgrimetricsAPI
from app.services.iot_service import IoTService
from app.models.soil_prediction_model import SoilQualityModel
from app.models.pest_detection_model import PestDetectionModel
from app.models.planting_scheduler import PlantingScheduler

agrimetrics_api = AgrimetricsAPI()
iot_service = IoTService()
soil_model = SoilQualityModel()
pest_model = PestDetectionModel()
planting_scheduler = PlantingScheduler()

api_bp = Blueprint('api', __name__)

@api_bp.route('/health')
def health_check():
    """API health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

@api_bp.route('/farms')
@login_required
def get_farms():
    """Get all farms for the current user."""

    
    farms = [
        {
            'id': 1,
            'name': 'North Field Farm',
            'location': 'Midwest Region',
            'size': 240,
            'size_unit': 'hectares',
            'fields': 4
        },
        {
            'id': 2,
            'name': 'Riverside Crops',
            'location': 'Western Region',
            'size': 185,
            'size_unit': 'hectares',
            'fields': 3
        }
    ]
    
    return jsonify(farms)

@api_bp.route('/farms/<int:farm_id>/fields')
@login_required
def get_fields(farm_id):
    """Get all fields for a specific farm."""

    
    fields = [
        {
            'id': 1,
            'name': f'Field {i}',
            'farm_id': farm_id,
            'area': random.randint(40, 80),
            'area_unit': 'hectares',
            'crop': random.choice(['Corn', 'Wheat', 'Soybean', 'Cotton', 'Potato']),
            'soil_type': random.choice(['Loam', 'Clay Loam', 'Sandy Loam', 'Silt Loam']),
            'status': random.choice(['active', 'fallow', 'preparing', 'harvested'])
        } for i in range(1, 5)
    ]
    
    return jsonify(fields)

@api_bp.route('/sensors')
@login_required
def get_sensors():
    """Get all IoT sensors data."""
    sensor_data = iot_service.get_sensor_data()
    
    return jsonify(sensor_data)

@api_bp.route('/fields/<int:field_id>/soil')
@login_required
def get_field_soil_data(field_id):
    """Get soil data for a specific field."""
    time_range = request.args.get('range', '7d')  
    end_date = datetime.now()
    if time_range == '1d':
        start_date = end_date - timedelta(days=1)
        points = 24  
    elif time_range == '7d':
        start_date = end_date - timedelta(days=7)
        points = 7  
    elif time_range == '30d':
        start_date = end_date - timedelta(days=30)
        points = 30  
    elif time_range == '90d':
        start_date = end_date - timedelta(days=90)
        points = 90  
    else:
        start_date = end_date - timedelta(days=7)
        points = 7  
    
    timestamps = []
    for i in range(points):
        if time_range == '1d':
            timestamp = start_date + timedelta(hours=i)
        else:
            timestamp = start_date + timedelta(days=i)
        timestamps.append(timestamp.isoformat())
    
    data = {
        'field_id': field_id,
        'time_range': time_range,
        'timestamps': timestamps,
        'moisture': [round(40 + 10 * random.random(), 1) for _ in range(points)],
        'temperature': [round(20 + 5 * random.random(), 1) for _ in range(points)],
        'ph': [round(6.5 + 0.5 * random.random(), 1) for _ in range(points)],
        'nitrogen': [round(50 + 10 * random.random(), 1) for _ in range(points)],
        'phosphorus': [round(30 + 5 * random.random(), 1) for _ in range(points)],
        'potassium': [round(100 + 20 * random.random(), 1) for _ in range(points)]
    }
    
    return jsonify(data)

@api_bp.route('/fields/<int:field_id>/weather')
@login_required
def get_field_weather_data(field_id):
    """Get weather data for a specific field."""
    time_range = request.args.get('range', '7d')  
    
    end_date = datetime.now()
    if time_range == '1d':
        start_date = end_date - timedelta(days=1)
        points = 24  
    elif time_range == '7d':
        start_date = end_date - timedelta(days=7)
        points = 7  
    elif time_range == '30d':
        start_date = end_date - timedelta(days=30)
        points = 30  
    elif time_range == '90d':
        start_date = end_date - timedelta(days=90)
        points = 90 
    else:
        start_date = end_date - timedelta(days=7)
        points = 7  
    
    timestamps = []
    for i in range(points):
        if time_range == '1d':
            timestamp = start_date + timedelta(hours=i)
        else:
            timestamp = start_date + timedelta(days=i)
        timestamps.append(timestamp.isoformat())
    
    data = {
        'field_id': field_id,
        'time_range': time_range,
        'timestamps': timestamps,
        'temperature': [round(20 + 10 * random.random(), 1) for _ in range(points)],
        'humidity': [round(60 + 20 * random.random(), 1) for _ in range(points)],
        'precipitation': [round(5 * random.random(), 1) for _ in range(points)],
        'wind_speed': [round(15 * random.random(), 1) for _ in range(points)],
        'wind_direction': [random.choice(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']) for _ in range(points)]
    }
    
    return jsonify(data)

@api_bp.route('/agrimetrics/soil', methods=['GET'])
@login_required
def get_agrimetrics_soil_data():
    """Get soil data from Agrimetrics API."""
    latitude = float(request.args.get('lat', 51.5074))  
    longitude = float(request.args.get('lon', -0.1278))
    date = request.args.get('date')
    

    
    response = {
        'request': {
            'latitude': latitude,
            'longitude': longitude,
            'date': date or datetime.now().strftime('%Y-%m-%d')
        },
        'soil_data': {
            'texture': random.choice(['Loam', 'Clay Loam', 'Sandy Loam', 'Silt Loam']),
            'ph': round(6.5 + 0.5 * random.random(), 1),
            'organic_matter': round(3 + 2 * random.random(), 1),
            'moisture': round(40 + 10 * random.random(), 1),
            'temperature': round(15 + 5 * random.random(), 1),
            'nutrients': {
                'nitrogen': round(50 + 10 * random.random(), 1),
                'phosphorus': round(30 + 5 * random.random(), 1),
                'potassium': round(100 + 20 * random.random(), 1),
                'calcium': round(2000 + 500 * random.random(), 1),
                'magnesium': round(200 + 50 * random.random(), 1)
            }
        }
    }
    
    return jsonify(response)

@api_bp.route('/agrimetrics/weather', methods=['GET'])
@login_required
def get_agrimetrics_weather_data():
    """Get weather data from Agrimetrics API."""
    latitude = float(request.args.get('lat', 51.5074)) 
    longitude = float(request.args.get('lon', -0.1278))
    days = int(request.args.get('days', 7))
    

    forecast = []
    for i in range(days):
        date = (datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d')
        forecast.append({
            'date': date,
            'temperature': {
                'min': round(15 + 5 * random.random(), 1),
                'max': round(25 + 5 * random.random(), 1)
            },
            'humidity': round(60 + 20 * random.random(), 1),
            'precipitation': {
                'probability': round(100 * random.random(), 1),
                'amount': round(10 * random.random(), 1) if random.random() > 0.5 else 0
            },
            'wind': {
                'speed': round(15 * random.random(), 1),
                'direction': random.choice(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'])
            }
        })
    
    response = {
        'request': {
            'latitude': latitude,
            'longitude': longitude,
            'days': days
        },
        'forecast': forecast
    }
    
    return jsonify(response)

@api_bp.route('/dashboard/summary')
@login_required
def get_dashboard_summary():
    """Get summary data for the main dashboard."""

    
    response = {
        'farms': 2,
        'fields': 8,
        'active_crops': 5,
        'sensors': {
            'total': 24,
            'online': 22,
            'offline': 2,
            'alerts': 3
        },
        'soil_health': {
            'excellent': 3,
            'good': 4,
            'fair': 1,
            'poor': 0
        },
        'pest_alerts': {
            'high': 1,
            'medium': 2,
            'low': 5
        },
        'upcoming_plantings': 3,
        'weather_alerts': 2
    }
    
    return jsonify(response) 