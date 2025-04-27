from flask import Blueprint, render_template, jsonify, current_app, request
from datetime import datetime, timedelta
from app.services.iot_service import IoTService

iot_service = IoTService()

dashboard_bp = Blueprint('dashboard_bp', __name__)

@dashboard_bp.route('/')
def index():
    """
    Main dashboard page showing overview of farm data
    """
    return render_template('dashboard.html', title="(A)I Plant Dashboard")

@dashboard_bp.route('/api/dashboard-summary')
def dashboard_summary():
    """
    API endpoint to get summary data for the dashboard
    """
    soil_data = iot_service.get_sensor_data(
        sensor_type='soil',
        timeframe='latest'
    )
    
    weather_data = iot_service.get_sensor_data(
        sensor_type='weather',
        timeframe='latest'
    )
    
    irrigation_data = iot_service.get_sensor_data(
        sensor_type='irrigation',
        timeframe='latest'
    )
    
    avg_soil_moisture = 0
    avg_soil_temp = 0
    avg_soil_ph = 0
    soil_sensors_count = 0
    
    if soil_data.get('sensors'):
        for sensor in soil_data['sensors']:
            if 'data' in sensor:
                soil_sensors_count += 1
                avg_soil_moisture += sensor['data'].get('moisture', 0)
                avg_soil_temp += sensor['data'].get('temperature', 0)
                avg_soil_ph += sensor['data'].get('ph', 0)
    
    if soil_sensors_count > 0:
        avg_soil_moisture /= soil_sensors_count
        avg_soil_temp /= soil_sensors_count
        avg_soil_ph /= soil_sensors_count
    
    current_temperature = 0
    current_humidity = 0
    
    if weather_data.get('sensors') and len(weather_data['sensors']) > 0:
        weather_sensor = weather_data['sensors'][0]
        if 'data' in weather_sensor:
            current_temperature = weather_sensor['data'].get('temperature', 0)
            current_humidity = weather_sensor['data'].get('humidity', 0)
    
    irrigation_status = 'Off'
    water_usage_today = 0
    
    if irrigation_data.get('sensors'):
        for sensor in irrigation_data['sensors']:
            if 'data' in sensor:
                if sensor['data'].get('active', False):
                    irrigation_status = 'On'
                water_usage_today += sensor['data'].get('water_usage_daily', 0)
    
    battery_levels = []
    for sensor_type in ['soil', 'weather', 'irrigation']:
        sensor_data = iot_service.get_sensor_data(
            sensor_type=sensor_type,
            timeframe='latest'
        )
        if sensor_data.get('sensors'):
            for sensor in sensor_data['sensors']:
                if 'data' in sensor and 'battery_level' in sensor['data']:
                    battery_levels.append(sensor['data']['battery_level'])
    
    system_health = 100
    if battery_levels:
        system_health = sum(battery_levels) / len(battery_levels)
    
    now = datetime.now()
    formatted_date = now.strftime("%B %d, %Y")
    formatted_time = now.strftime("%H:%M:%S")
    
    return jsonify({
        'timestamp': now.isoformat(),
        'date': formatted_date,
        'time': formatted_time,
        'soil': {
            'moisture': round(avg_soil_moisture, 1),
            'temperature': round(avg_soil_temp, 1),
            'ph': round(avg_soil_ph, 1)
        },
        'weather': {
            'temperature': round(current_temperature, 1),
            'humidity': round(current_humidity, 1)
        },
        'irrigation': {
            'status': irrigation_status,
            'water_usage_today': round(water_usage_today, 1)
        },
        'system_health': round(system_health, 1)
    })

@dashboard_bp.route('/api/field-status')
def field_status():
    """
    API endpoint to get status of all fields
    """
    soil_data = iot_service.get_sensor_data(
        sensor_type='soil',
        timeframe='latest'
    )
    
    fields = {}
    
    if soil_data.get('sensors'):
        for sensor in soil_data['sensors']:
            field_id = sensor.get('field_id', 0)
            if field_id not in fields:
                fields[field_id] = {
                    'id': field_id,
                    'name': f"Field {field_id}",
                    'sensors': [],
                    'avg_moisture': 0,
                    'avg_temperature': 0,
                    'status': 'Good'
                }
            
            if 'data' in sensor:
                fields[field_id]['sensors'].append(sensor)
    
    field_list = []
    for field_id, field in fields.items():
        sensors = field['sensors']
        if sensors:
            moisture_sum = sum(s['data'].get('moisture', 0) for s in sensors)
            temp_sum = sum(s['data'].get('temperature', 0) for s in sensors)
            
            field['avg_moisture'] = round(moisture_sum / len(sensors), 1)
            field['avg_temperature'] = round(temp_sum / len(sensors), 1)
            
            if field['avg_moisture'] < 25:
                field['status'] = 'Dry'
            elif field['avg_moisture'] > 45:
                field['status'] = 'Wet'
            else:
                field['status'] = 'Good'
        
        field_list.append(field)
    
    return jsonify({
        'timestamp': datetime.now().isoformat(),
        'fields': field_list
    })

@dashboard_bp.route('/api/sensor-alerts')
def sensor_alerts():
    """
    API endpoint to get sensor alerts
    """
    alerts = []
    
    for sensor_type in ['soil', 'weather', 'irrigation']:
        sensor_data = iot_service.get_sensor_data(
            sensor_type=sensor_type,
            timeframe='latest'
        )
        
        if sensor_data.get('sensors'):
            for sensor in sensor_data['sensors']:
                if 'data' in sensor and sensor['data'].get('battery_level', 100) < 30:
                    alerts.append({
                        'type': 'Low Battery',
                        'sensor_id': sensor.get('id', 'unknown'),
                        'sensor_type': sensor_type,
                        'field_id': sensor.get('field_id', 0),
                        'value': f"{sensor['data'].get('battery_level')}%",
                        'timestamp': datetime.now().isoformat(),
                        'severity': 'Warning'
                    })
                
                if sensor_type == 'soil' and 'data' in sensor:
                    moisture = sensor['data'].get('moisture', 30)
                    if moisture < 20:
                        alerts.append({
                            'type': 'Low Moisture',
                            'sensor_id': sensor.get('id', 'unknown'),
                            'sensor_type': 'soil',
                            'field_id': sensor.get('field_id', 0),
                            'value': f"{moisture}%",
                            'timestamp': datetime.now().isoformat(),
                            'severity': 'Warning'
                        })
                    elif moisture > 50:
                        alerts.append({
                            'type': 'High Moisture',
                            'sensor_id': sensor.get('id', 'unknown'),
                            'sensor_type': 'soil',
                            'field_id': sensor.get('field_id', 0),
                            'value': f"{moisture}%",
                            'timestamp': datetime.now().isoformat(),
                            'severity': 'Warning'
                        })
    
    alerts.sort(key=lambda x: 0 if x['severity'] == 'Critical' else 1 if x['severity'] == 'Warning' else 2)
    
    return jsonify({
        'timestamp': datetime.now().isoformat(),
        'alerts': alerts
    }) 