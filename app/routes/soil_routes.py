from flask import Blueprint, render_template, request, jsonify, session, flash, redirect, url_for
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import sqlite3

from app.services.agrimetrics_api import AgrimetricsAPI
from app.services.iot_service import IoTService
from app.models.soil_prediction_model import SoilQualityModel

# Initialize services
agrimetrics_api = AgrimetricsAPI()
iot_service = IoTService()
soil_model = SoilQualityModel()

soil_bp = Blueprint('soil', __name__)

@soil_bp.route('/')
def soil_dashboard():
    """Main soil analysis dashboard."""
    return render_template('soil/dashboard.html')

@soil_bp.route('/quality')
def soil_quality():
    """View soil quality data and analysis."""
    # Get field ID from request, default to first field if not specified
    field_id = request.args.get('field_id', 1)
    
    # Get soil data for the field
    soil_data = get_soil_data_for_field(field_id)
    
    return render_template('soil/quality.html', soil_data=soil_data, field_id=field_id)

@soil_bp.route('/moisture')
def soil_moisture():
    """View soil moisture data and analysis."""
    # Get field ID from request, default to first field if not specified
    field_id = request.args.get('field_id', 1)
    
    # Get soil moisture data for the field
    moisture_data = get_moisture_data_for_field(field_id)
    
    return render_template('soil/moisture.html', moisture_data=moisture_data, field_id=field_id)

@soil_bp.route('/nutrients')
def nutrients():
    """
    Render the soil nutrients page that is accessible without login
    """
    return render_template('soil/nutrients.html', title="Soil Nutrients")

@soil_bp.route('/ph')
def soil_ph():
    """View soil pH data and recommendations."""
    # Get field ID from request, default to first field if not specified
    field_id = request.args.get('field_id', 1)
    
    # Get soil pH data for the field
    ph_data = get_ph_data_for_field(field_id)
    
    return render_template('soil/ph.html', ph_data=ph_data, field_id=field_id)

@soil_bp.route('/recommendations')
def soil_recommendations():
    """Get recommendations for improving soil quality."""
    # Get field ID from request, default to first field if not specified
    field_id = request.args.get('field_id', 1)
    
    # Get soil data for the field
    soil_data = get_soil_data_for_field(field_id)
    
    # Generate recommendations
    recommendations = generate_soil_recommendations(soil_data)
    
    return render_template('soil/recommendations.html', recommendations=recommendations, field_id=field_id)

@soil_bp.route('/api/data')
def api_soil_data():
    """API endpoint to get soil data for charts and visualizations."""
    field_id = request.args.get('field_id', 1)
    data_type = request.args.get('type', 'all')  # all, moisture, ph, nutrients
    time_range = request.args.get('range', '7d')  # 1d, 7d, 30d, 90d
    
    # Get data based on parameters
    if data_type == 'all':
        data = get_soil_data_for_field(field_id, time_range)
    elif data_type == 'moisture':
        data = get_moisture_data_for_field(field_id, time_range)
    elif data_type == 'nutrients':
        data = get_nutrient_data_for_field(field_id, time_range)
    elif data_type == 'ph':
        data = get_ph_data_for_field(field_id, time_range)
    else:
        data = {'error': 'Invalid data type'}
    
    return jsonify(data)

@soil_bp.route('/api/predict')
def api_soil_predict():
    """API endpoint to predict future soil conditions."""
    field_id = request.args.get('field_id', 1)
    days_ahead = int(request.args.get('days', 7))
    
    # Get current soil data
    current_data = get_soil_data_for_field(field_id)
    
    # Prepare input for prediction model
    # In a real app, we would have a properly trained model
    # Here we'll just simulate predictions
    predictions = simulate_soil_predictions(current_data, days_ahead)
    
    return jsonify(predictions)

@soil_bp.route('/api/sensors')
def api_soil_sensors():
    """API endpoint to get data from soil sensors."""
    field_id = int(request.args.get('field_id', 1))
    
    # Get data from soil sensors in the field
    sensor_data = iot_service.get_sensor_data(sensor_type='soil', field_id=field_id)
    
    return jsonify(sensor_data)

@soil_bp.route('/api/soil-data')
def soil_data_api():
    """
    API endpoint to get real-time soil data from IoT sensors
    """
    field_id = request.args.get('field_id', type=int)
    sensor_id = request.args.get('sensor_id')
    sensor_type = request.args.get('sensor_type', 'soil')
    timeframe = request.args.get('timeframe', 'latest')
    
    # Get soil data from IoT service
    data = iot_service.get_sensor_data(
        sensor_type=sensor_type,
        field_id=field_id,
        sensor_id=sensor_id,
        timeframe=timeframe
    )
    
    return jsonify(data)

@soil_bp.route('/api/agrimetrics-data')
def agrimetrics_data_api():
    """
    API endpoint to get soil and weather data from Agrimetrics API
    """
    data_type = request.args.get('type', 'soil')
    lat = request.args.get('lat', 51.5074, type=float)
    lon = request.args.get('lon', -0.1278, type=float)
    
    if data_type == 'soil':
        data = agrimetrics_api.get_soil_properties(lat, lon)
    elif data_type == 'weather':
        data = agrimetrics_api.get_weather_forecast(lat, lon)
    elif data_type == 'crop':
        crop_type = request.args.get('crop', 'wheat')
        data = agrimetrics_api.get_crop_calendar(lat, lon, crop_type)
    elif data_type == 'pest':
        crop_type = request.args.get('crop', 'wheat')
        data = agrimetrics_api.get_pest_risk(lat, lon, crop_type)
    else:
        data = {"error": "Invalid data type requested"}
    
    return jsonify(data)

@soil_bp.route('/api/recommendations')
def soil_recommendations_api():
    """
    API endpoint to get soil improvement recommendations
    """
    # Get soil data for analysis
    field_id = request.args.get('field_id', 1, type=int)
    soil_data = iot_service.get_sensor_data(
        sensor_type='soil',
        field_id=field_id,
        timeframe='latest'
    )
    
    # Extract soil properties from the first sensor
    soil_properties = {}
    if soil_data.get('sensors') and len(soil_data['sensors']) > 0:
        sensor_data = soil_data['sensors'][0]['data']
        soil_properties = {
            'nitrogen': sensor_data.get('nitrogen', 0),
            'phosphorus': sensor_data.get('phosphorus', 0),
            'potassium': sensor_data.get('potassium', 0),
            'ph': sensor_data.get('ph', 0),
            'moisture': sensor_data.get('moisture', 0),
            'electrical_conductivity': sensor_data.get('electrical_conductivity', 0)
        }
    
    # Generate recommendations based on soil properties
    recommendations = []
    
    # Nitrogen recommendations
    if soil_properties.get('nitrogen', 0) < 30:
        recommendations.append({
            'nutrient': 'Nitrogen',
            'status': 'Low',
            'action': 'Apply nitrogen-rich fertilizer or incorporate legumes into crop rotation',
            'priority': 'High',
            'benefit': 'Improved plant growth and yield'
        })
    
    # Phosphorus recommendations
    if soil_properties.get('phosphorus', 0) < 20:
        recommendations.append({
            'nutrient': 'Phosphorus',
            'status': 'Low',
            'action': 'Apply phosphate fertilizer or bone meal',
            'priority': 'Medium',
            'benefit': 'Enhanced root development and flowering'
        })
    
    # Potassium recommendations
    if soil_properties.get('potassium', 0) < 150:
        recommendations.append({
            'nutrient': 'Potassium',
            'status': 'Low',
            'action': 'Apply potash fertilizer or wood ash',
            'priority': 'Medium',
            'benefit': 'Improved drought resistance and disease tolerance'
        })
    
    # pH recommendations
    ph_level = soil_properties.get('ph', 7.0)
    if ph_level < 6.0:
        recommendations.append({
            'nutrient': 'pH',
            'status': 'Acidic',
            'action': 'Apply agricultural lime to raise pH',
            'priority': 'High',
            'benefit': 'Better nutrient availability and microbial activity'
        })
    elif ph_level > 7.5:
        recommendations.append({
            'nutrient': 'pH',
            'status': 'Alkaline',
            'action': 'Apply sulfur or acidifying amendments to lower pH',
            'priority': 'Medium',
            'benefit': 'Improved micronutrient availability'
        })
    
    # Moisture recommendations
    moisture = soil_properties.get('moisture', 30)
    if moisture < 25:
        recommendations.append({
            'nutrient': 'Moisture',
            'status': 'Low',
            'action': 'Increase irrigation frequency or apply mulch to retain moisture',
            'priority': 'High',
            'benefit': 'Prevent drought stress and nutrient uptake issues'
        })
    elif moisture > 45:
        recommendations.append({
            'nutrient': 'Moisture',
            'status': 'High',
            'action': 'Improve drainage or reduce irrigation',
            'priority': 'High',
            'benefit': 'Prevent root rot and oxygen depletion in soil'
        })
    
    # EC recommendations
    ec = soil_properties.get('electrical_conductivity', 0.5)
    if ec > 0.8:
        recommendations.append({
            'nutrient': 'Salinity',
            'status': 'High',
            'action': 'Leach soil with fresh water and reduce fertilizer application',
            'priority': 'Medium',
            'benefit': 'Reduce salt stress on plants'
        })
    
    # Add generic recommendation if no specific issues found
    if not recommendations:
        recommendations.append({
            'nutrient': 'Overall',
            'status': 'Good',
            'action': 'Maintain current soil management practices',
            'priority': 'Low',
            'benefit': 'Sustained soil health and productivity'
        })
    
    return jsonify({
        'timestamp': datetime.now().isoformat(),
        'field_id': field_id,
        'soil_properties': soil_properties,
        'recommendations': recommendations
    })

# Helper functions

def get_soil_data_for_field(field_id, time_range='7d'):
    """
    Get soil data for a specific field.
    
    Args:
        field_id: ID of the field
        time_range: Time range to get data for (1d, 7d, 30d, 90d)
        
    Returns:
        dict: Soil data
    """
    # In a real app, this would query the database or API
    # For demo purposes, we'll generate simulated data
    
    # Determine the date range
    end_date = datetime.now()
    if time_range == '1d':
        start_date = end_date - timedelta(days=1)
        points = 24  # Hourly data
    elif time_range == '7d':
        start_date = end_date - timedelta(days=7)
        points = 7 * 24  # Hourly data for a week
    elif time_range == '30d':
        start_date = end_date - timedelta(days=30)
        points = 30  # Daily data for a month
    elif time_range == '90d':
        start_date = end_date - timedelta(days=90)
        points = 90  # Daily data for 3 months
    else:
        start_date = end_date - timedelta(days=7)
        points = 7  # Default to daily data for a week
    
    # Generate timestamps
    delta = (end_date - start_date) / points
    timestamps = [(start_date + delta * i).isoformat() for i in range(points)]
    
    # Generate soil data
    data = {
        'field_id': field_id,
        'time_range': time_range,
        'timestamps': timestamps,
        'moisture': [round(40 + 10 * np.sin(i/10) + np.random.uniform(-5, 5), 1) for i in range(points)],
        'ph': [round(6.5 + 0.5 * np.sin(i/15) + np.random.uniform(-0.3, 0.3), 1) for i in range(points)],
        'temperature': [round(20 + 5 * np.sin(i/12) + np.random.uniform(-2, 2), 1) for i in range(points)],
        'nitrogen': [round(50 + 10 * np.sin(i/20) + np.random.uniform(-5, 5), 1) for i in range(points)],
        'phosphorus': [round(30 + 5 * np.sin(i/25) + np.random.uniform(-3, 3), 1) for i in range(points)],
        'potassium': [round(100 + 20 * np.sin(i/18) + np.random.uniform(-10, 10), 1) for i in range(points)],
        'electrical_conductivity': [round(0.8 + 0.3 * np.sin(i/22) + np.random.uniform(-0.1, 0.1), 2) for i in range(points)]
    }
    
    return data

def get_moisture_data_for_field(field_id, time_range='7d'):
    """Get moisture-specific data for a field."""
    soil_data = get_soil_data_for_field(field_id, time_range)
    
    moisture_data = {
        'field_id': field_id,
        'time_range': time_range,
        'timestamps': soil_data['timestamps'],
        'moisture': soil_data['moisture'],
        'ideal_range': {
            'min': 30,
            'max': 50,
            'optimal': 40
        },
        'status': 'normal'  # normal, low, high, critical
    }
    
    # Determine status based on latest moisture reading
    latest_moisture = moisture_data['moisture'][-1]
    if latest_moisture < 20:
        moisture_data['status'] = 'critical_low'
    elif latest_moisture < 30:
        moisture_data['status'] = 'low'
    elif latest_moisture > 60:
        moisture_data['status'] = 'critical_high'
    elif latest_moisture > 50:
        moisture_data['status'] = 'high'
    
    return moisture_data

def get_nutrient_data_for_field(field_id, time_range='7d'):
    """Get nutrient-specific data for a field."""
    # Remove the db import which is causing issues
    import sqlite3
    import os
    
    try:
        # Get absolute path for the database
        BASEDIR = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        db_path = os.path.join(BASEDIR, 'instance', 'agriculture_assistant.db')
        
        # Connect to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Determine field name based on field_id
        field_names = ['North Field', 'South Field', 'West Field', 'East Field', 'Center Field']
        field_name = field_names[int(field_id) - 1] if int(field_id) <= len(field_names) else field_names[0]
        
        # Get the latest soil analysis data for this field
        cursor.execute('''
            SELECT id, nitrogen, phosphorus, potassium, calcium, magnesium, sulfur, 
                   iron, manganese, zinc, copper, boron, molybdenum
            FROM soil_analysis 
            WHERE field_name = ?
            ORDER BY timestamp DESC
            LIMIT 1
        ''', (field_name,))
        
        latest_data = cursor.fetchone()
        soil_id = latest_data[0]
        
        # Get historical data for trends (last 6 months)
        cursor.execute('''
            SELECT timestamp, nitrogen, phosphorus, potassium
            FROM soil_analysis 
            WHERE field_name = ?
            ORDER BY timestamp DESC
            LIMIT 7
        ''', (field_name,))
        
        trend_data = cursor.fetchall()
        trend_data.reverse()  # Oldest to newest for chart
        
        # Get fertilizer recommendations
        cursor.execute('''
            SELECT nutrient, recommendation, amount
            FROM fertilizer_recommendations
            WHERE soil_analysis_id = ?
        ''', (soil_id,))
        
        fertilizer_recommendations = [
            {
                'nutrient': nutrient, 
                'recommendation': recommendation, 
                'amount': amount
            } for nutrient, recommendation, amount in cursor.fetchall()
        ]
        
        # Get recommended products
        cursor.execute('''
            SELECT name, dose, note
            FROM recommended_products
            WHERE soil_analysis_id = ?
        ''', (soil_id,))
        
        fertilizer_products = [
            {
                'name': name, 
                'dose': dose, 
                'note': note
            } for name, dose, note in cursor.fetchall()
        ]
        
        conn.close()
        
        # Create nutrient data structure
        nutrient_data = {
            'field_id': field_id,
            'field_name': field_name,
            'macronutrient_summary': [
                {'name': 'Nitrogen (N)', 'status': 'Low' if latest_data[1] < 30 else 'Optimal', 
                 'class': 'danger' if latest_data[1] < 30 else 'success'},
                {'name': 'Phosphorus (P)', 'status': 'Optimal', 'class': 'success'},
                {'name': 'Potassium (K)', 'status': 'Slightly Low' if latest_data[3] < 200 else 'Optimal', 
                 'class': 'warning' if latest_data[3] < 200 else 'success'},
                {'name': 'Calcium (Ca)', 'status': 'Optimal', 'class': 'success'},
                {'name': 'Magnesium (Mg)', 'status': 'Optimal', 'class': 'success'},
                {'name': 'Sulfur (S)', 'status': 'Optimal', 'class': 'success'}
            ],
            'micronutrient_summary': [
                {'name': 'Iron (Fe)', 'status': 'Optimal', 'class': 'success'},
                {'name': 'Manganese (Mn)', 'status': 'Slightly Low' if latest_data[7] < 50 else 'Optimal', 
                 'class': 'warning' if latest_data[7] < 50 else 'success'},
                {'name': 'Zinc (Zn)', 'status': 'Low' if latest_data[8] < 3 else 'Optimal', 
                 'class': 'danger' if latest_data[8] < 3 else 'success'},
                {'name': 'Copper (Cu)', 'status': 'Optimal', 'class': 'success'},
                {'name': 'Boron (B)', 'status': 'Optimal', 'class': 'success'},
                {'name': 'Molybdenum (Mo)', 'status': 'Optimal', 'class': 'success'}
            ],
            'ratio': {
                'n': round(latest_data[1] / (latest_data[1] + latest_data[2] + latest_data[3]) * 100),
                'p': round(latest_data[2] / (latest_data[1] + latest_data[2] + latest_data[3]) * 100),
                'k': round(latest_data[3] / (latest_data[1] + latest_data[2] + latest_data[3]) * 100),
                'current': f"{round(latest_data[1]/10)}:{round(latest_data[2]/10)}:{round(latest_data[3]/10)}",
                'ideal': '1:1:1'
            },
            'trend_data': {
                'timestamps': [item[0] for item in trend_data],
                'nitrogen': [item[1] for item in trend_data],
                'phosphorus': [item[2] for item in trend_data],
                'potassium': [item[3] for item in trend_data]
            }
        }
        
        return nutrient_data, fertilizer_recommendations, fertilizer_products
    
    except Exception as e:
        print(f"Error getting nutrient data: {e}")
        # Fall back to simulated data if there's an error
        soil_data = get_soil_data_for_field(field_id, time_range)
        
        nutrient_data = {
            'field_id': field_id,
            'time_range': time_range,
            'timestamps': soil_data['timestamps'],
            'nitrogen': soil_data['nitrogen'],
            'phosphorus': soil_data['phosphorus'],
            'potassium': soil_data['potassium'],
            'ideal_ranges': {
                'nitrogen': {'min': 40, 'max': 60, 'optimal': 50},
                'phosphorus': {'min': 25, 'max': 35, 'optimal': 30},
                'potassium': {'min': 80, 'max': 120, 'optimal': 100}
            },
            'status': {
                'nitrogen': 'normal',
                'phosphorus': 'normal',
                'potassium': 'normal'
            },
            'ratio': {
                'n': 25,
                'p': 25,
                'k': 50,
                'current': '1:1:2',
                'ideal': '1:1:1'
            }
        }
        
        # Determine status for each nutrient
        latest_n = nutrient_data['nitrogen'][-1]
        if latest_n < 30:
            nutrient_data['status']['nitrogen'] = 'deficient'
        elif latest_n > 70:
            nutrient_data['status']['nitrogen'] = 'excessive'
        
        latest_p = nutrient_data['phosphorus'][-1]
        if latest_p < 20:
            nutrient_data['status']['phosphorus'] = 'deficient'
        elif latest_p > 40:
            nutrient_data['status']['phosphorus'] = 'excessive'
        
        latest_k = nutrient_data['potassium'][-1]
        if latest_k < 70:
            nutrient_data['status']['potassium'] = 'deficient'
        elif latest_k > 130:
            nutrient_data['status']['potassium'] = 'excessive'
        
        # Default recommendations
        fertilizer_recommendations = [
            {'nutrient': 'Nitrogen (N)', 'recommendation': 'Apply nitrogen fertilizer', 'amount': '30 kg/ha'},
            {'nutrient': 'Phosphorus (P)', 'recommendation': 'No additional needed', 'amount': '0 kg/ha'},
            {'nutrient': 'Potassium (K)', 'recommendation': 'Apply potassium fertilizer', 'amount': '15 kg/ha'},
            {'nutrient': 'Zinc (Zn)', 'recommendation': 'Apply zinc sulfate', 'amount': '5 kg/ha'},
            {'nutrient': 'Manganese (Mn)', 'recommendation': 'Apply manganese sulfate', 'amount': '3 kg/ha'}
        ]
        
        # Default products
        fertilizer_products = [
            {'name': 'Balanced NPK 10-10-10', 'dose': '300 kg/ha', 'note': 'For overall balance'},
            {'name': 'Urea (46-0-0)', 'dose': '65 kg/ha', 'note': 'For nitrogen deficiency'},
            {'name': 'Zinc Sulfate', 'dose': '5 kg/ha', 'note': 'For zinc deficiency'}
        ]
        
        return nutrient_data, fertilizer_recommendations, fertilizer_products

def get_ph_data_for_field(field_id, time_range='7d'):
    """Get pH-specific data for a field."""
    soil_data = get_soil_data_for_field(field_id, time_range)
    
    ph_data = {
        'field_id': field_id,
        'time_range': time_range,
        'timestamps': soil_data['timestamps'],
        'ph': soil_data['ph'],
        'ideal_range': {
            'min': 6.0,
            'max': 7.0,
            'optimal': 6.5
        },
        'status': 'normal'  # normal, acidic, alkaline, very_acidic, very_alkaline
    }
    
    # Determine status based on latest pH reading
    latest_ph = ph_data['ph'][-1]
    if latest_ph < 5.0:
        ph_data['status'] = 'very_acidic'
    elif latest_ph < 6.0:
        ph_data['status'] = 'acidic'
    elif latest_ph > 8.0:
        ph_data['status'] = 'very_alkaline'
    elif latest_ph > 7.0:
        ph_data['status'] = 'alkaline'
    
    return ph_data

def generate_soil_recommendations(soil_data):
    """
    Generate recommendations for improving soil quality.
    
    Args:
        soil_data: Current soil data
        
    Returns:
        list: Recommendations
    """
    recommendations = []
    
    # Get latest values
    latest_moisture = soil_data['moisture'][-1]
    latest_ph = soil_data['ph'][-1]
    latest_n = soil_data['nitrogen'][-1]
    latest_p = soil_data['phosphorus'][-1]
    latest_k = soil_data['potassium'][-1]
    
    # Moisture recommendations
    if latest_moisture < 25:
        recommendations.append({
            'type': 'moisture',
            'severity': 'high',
            'problem': 'Soil moisture is critically low.',
            'solution': 'Increase irrigation immediately. Consider installing drip irrigation for more efficient water delivery.',
            'benefits': 'Preventing crop stress and yield loss due to drought conditions.'
        })
    elif latest_moisture < 35:
        recommendations.append({
            'type': 'moisture',
            'severity': 'medium',
            'problem': 'Soil moisture is below optimal levels.',
            'solution': 'Increase irrigation frequency or duration. Monitor soil moisture daily.',
            'benefits': 'Maintaining adequate water content for plant growth and nutrient uptake.'
        })
    elif latest_moisture > 55:
        recommendations.append({
            'type': 'moisture',
            'severity': 'medium',
            'problem': 'Soil moisture is above optimal levels.',
            'solution': 'Reduce irrigation frequency. Ensure proper drainage in the field.',
            'benefits': 'Preventing root diseases and improving soil aeration.'
        })
    
    # pH recommendations
    if latest_ph < 5.5:
        recommendations.append({
            'type': 'ph',
            'severity': 'high',
            'problem': 'Soil is too acidic for most crops.',
            'solution': 'Apply agricultural lime (calcium carbonate) to raise pH. Typical application rate: 2-3 tons per acre.',
            'benefits': 'Improving nutrient availability and reducing toxicity of aluminum and manganese.'
        })
    elif latest_ph > 7.5:
        recommendations.append({
            'type': 'ph',
            'severity': 'high',
            'problem': 'Soil is too alkaline for most crops.',
            'solution': 'Apply agricultural sulfur or gypsum to lower pH. Typical application rate: 500-1000 lbs per acre.',
            'benefits': 'Improving availability of micronutrients and preventing nutrient lockout.'
        })
    
    # Nutrient recommendations
    if latest_n < 35:
        recommendations.append({
            'type': 'nutrient',
            'severity': 'high',
            'problem': 'Nitrogen deficiency detected.',
            'solution': 'Apply nitrogen fertilizer such as ammonium nitrate or urea. Consider foliar application for quick response.',
            'benefits': 'Improving leaf development, protein synthesis, and overall plant growth.'
        })
    elif latest_n > 65:
        recommendations.append({
            'type': 'nutrient',
            'severity': 'medium',
            'problem': 'Excess nitrogen detected.',
            'solution': 'Reduce nitrogen applications. Consider planting cover crops that use nitrogen efficiently.',
            'benefits': 'Preventing leaching of nitrogen into groundwater and reducing environmental impact.'
        })
    
    if latest_p < 20:
        recommendations.append({
            'type': 'nutrient',
            'severity': 'high',
            'problem': 'Phosphorus deficiency detected.',
            'solution': 'Apply phosphate fertilizers. Ensure soil pH is in the 6.0-7.0 range for optimal phosphorus availability.',
            'benefits': 'Enhancing root development, flowering, and seed formation.'
        })
    
    if latest_k < 70:
        recommendations.append({
            'type': 'nutrient',
            'severity': 'medium',
            'problem': 'Potassium deficiency detected.',
            'solution': 'Apply potassium fertilizers such as potassium chloride or potassium sulfate.',
            'benefits': 'Improving disease resistance, water regulation, and overall plant hardiness.'
        })
    
    return recommendations

def simulate_soil_predictions(current_data, days_ahead):
    """
    Simulate predictions for future soil conditions.
    
    Args:
        current_data: Current soil data
        days_ahead: Number of days to predict ahead
        
    Returns:
        dict: Predicted soil conditions
    """
    # Get the most recent values
    latest_moisture = current_data['moisture'][-1]
    latest_ph = current_data['ph'][-1]
    latest_temperature = current_data['temperature'][-1]
    latest_n = current_data['nitrogen'][-1]
    latest_p = current_data['phosphorus'][-1]
    latest_k = current_data['potassium'][-1]
    latest_ec = current_data['electrical_conductivity'][-1]
    
    # Generate timestamps for prediction period
    start_date = datetime.now()
    timestamps = [(start_date + timedelta(days=i)).isoformat() for i in range(1, days_ahead + 1)]
    
    # In a real app, we would use the trained ML model to make predictions
    # Here, we'll simulate predictions with some decay and randomness
    
    # Simulate moisture decrease over time (assuming no rain)
    moisture_decay = 0.95  # 5% decrease per day
    predicted_moisture = [round(latest_moisture * (moisture_decay ** i) + np.random.uniform(-2, 2), 1) for i in range(1, days_ahead + 1)]
    
    # Other values change less dramatically
    predicted_ph = [round(latest_ph + np.random.uniform(-0.1, 0.1), 1) for _ in range(days_ahead)]
    predicted_temperature = [round(latest_temperature + np.random.uniform(-1, 1), 1) for _ in range(days_ahead)]
    
    # Nutrients slowly decrease
    nutrient_decay = 0.98  # 2% decrease per day
    predicted_n = [round(latest_n * (nutrient_decay ** i) + np.random.uniform(-1, 1), 1) for i in range(1, days_ahead + 1)]
    predicted_p = [round(latest_p * (nutrient_decay ** i) + np.random.uniform(-0.5, 0.5), 1) for i in range(1, days_ahead + 1)]
    predicted_k = [round(latest_k * (nutrient_decay ** i) + np.random.uniform(-2, 2), 1) for i in range(1, days_ahead + 1)]
    
    # EC stays relatively stable
    predicted_ec = [round(latest_ec + np.random.uniform(-0.05, 0.05), 2) for _ in range(days_ahead)]
    
    predictions = {
        'timestamps': timestamps,
        'moisture': predicted_moisture,
        'ph': predicted_ph,
        'temperature': predicted_temperature,
        'nitrogen': predicted_n,
        'phosphorus': predicted_p,
        'potassium': predicted_k,
        'electrical_conductivity': predicted_ec,
        'confidence': 0.85  # Fixed confidence for demo
    }
    
    return predictions 