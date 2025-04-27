import os
import json
import requests
import logging
import time
from datetime import datetime, timedelta
import threading
import queue
import random  # For simulating sensor data
from dotenv import load_dotenv
import math

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IoTService:
    """
    Service to interact with IoT devices and sensors for retrieving
    real-time agricultural data. This is a stub implementation that
    returns simulated data.
    """
    
    def __init__(self):
        logger.info("IoT service initialized")
        self.sensors = self._initialize_demo_sensors()
    
    def _initialize_demo_sensors(self):
        """Initialize demo sensors for simulation."""
        # In a real implementation, this would connect to actual IoT sensors
        # For demo purposes, create simulated sensors
        
        sensors = {
            'soil': [
                {'id': 'soil-001', 'field_id': 1, 'name': 'North Field Sensor 1', 'location': {'lat': 51.5074, 'lon': -0.1278}},
                {'id': 'soil-002', 'field_id': 1, 'name': 'North Field Sensor 2', 'location': {'lat': 51.5080, 'lon': -0.1290}},
                {'id': 'soil-003', 'field_id': 2, 'name': 'South Field Sensor 1', 'location': {'lat': 51.4900, 'lon': -0.1400}},
                {'id': 'soil-004', 'field_id': 3, 'name': 'East Field Sensor 1', 'location': {'lat': 51.5100, 'lon': -0.1100}}
            ],
            'weather': [
                {'id': 'weather-001', 'name': 'Farm Weather Station', 'location': {'lat': 51.5074, 'lon': -0.1278}}
            ],
            'irrigation': [
                {'id': 'irrig-001', 'field_id': 1, 'name': 'North Field Irrigation Controller', 'zones': 4},
                {'id': 'irrig-002', 'field_id': 2, 'name': 'South Field Irrigation Controller', 'zones': 3}
            ]
        }
        
        return sensors
    
    def get_sensor_data(self, sensor_type='soil', field_id=None, sensor_id=None, timeframe='latest'):
        """
        Get data from IoT sensors.
        
        Args:
            sensor_type (str): Type of sensors to get data from ('soil', 'weather', 'irrigation')
            field_id (int, optional): ID of the field to get data for
            sensor_id (str, optional): ID of a specific sensor to get data for
            timeframe (str): 'latest', '24h', '7d', '30d'
            
        Returns:
            dict: Sensor data
        """
        # Validate sensor type
        if sensor_type not in self.sensors:
            return {'error': f'Unknown sensor type: {sensor_type}'}
        
        # Filter sensors by field_id if provided
        filtered_sensors = self.sensors[sensor_type]
        if field_id is not None:
            filtered_sensors = [s for s in filtered_sensors if s.get('field_id') == field_id]
        
        # Filter by sensor_id if provided
        if sensor_id is not None:
            filtered_sensors = [s for s in filtered_sensors if s['id'] == sensor_id]
        
        # Generate simulated data for each sensor
        sensor_data = []
        for sensor in filtered_sensors:
            if sensor_type == 'soil':
                data = self._generate_soil_sensor_data(sensor, timeframe)
            elif sensor_type == 'weather':
                data = self._generate_weather_sensor_data(sensor, timeframe)
            elif sensor_type == 'irrigation':
                data = self._generate_irrigation_sensor_data(sensor, timeframe)
            else:
                data = {'error': f'Unknown sensor type: {sensor_type}'}
            
            sensor_data.append({
                'sensor': sensor,
                'data': data
            })
        
        return {
            'sensor_type': sensor_type,
            'timestamp': datetime.now().isoformat(),
            'count': len(sensor_data),
            'sensors': sensor_data
        }
    
    def _generate_soil_sensor_data(self, sensor, timeframe):
        """Generate simulated soil sensor data."""
        if timeframe == 'latest':
            # Single data point for the latest reading
        return {
                'timestamp': datetime.now().isoformat(),
                'moisture': round(35 + 10 * random.random(), 1),
                'temperature': round(15 + 10 * random.random(), 1),
                'ph': round(6.0 + 1.5 * random.random(), 1),
                'electrical_conductivity': round(0.5 + 0.5 * random.random(), 2),
                'nitrogen': round(20 + 40 * random.random(), 1),
                'phosphorus': round(10 + 30 * random.random(), 1),
                'potassium': round(100 + 100 * random.random(), 1),
                'battery': round(70 + 30 * random.random(), 1)
            }
        else:
            # Multiple data points for time series
            data_points = []
            
            # Determine number of points based on timeframe
            if timeframe == '24h':
                num_points = 24
                interval = 1  # 1 hour intervals
            elif timeframe == '7d':
                num_points = 7 * 24
                interval = 1  # 1 hour intervals
            elif timeframe == '30d':
                num_points = 30
                interval = 24  # 1 day intervals
            else:
                num_points = 24
                interval = 1
            
            # Generate time series data
            for i in range(num_points):
                timestamp = (datetime.now() - timedelta(hours=i * interval)).isoformat()
                
                # Add some random variation but maintain trends
                noise_factor = random.random() * 0.4 + 0.8  # Between 0.8 and 1.2
                
                data_points.append({
                    'timestamp': timestamp,
                    'moisture': round((35 + 5 * math.sin(i/24)) * noise_factor, 1),
                    'temperature': round((15 + 5 * math.sin(i/12)) * noise_factor, 1),
                    'ph': round(6.5 + 0.5 * math.sin(i/48) * noise_factor, 1),
                    'electrical_conductivity': round((0.7 + 0.2 * math.sin(i/36)) * noise_factor, 2)
                })
            
            return data_points
    
    def _generate_weather_sensor_data(self, sensor, timeframe):
        """Generate simulated weather station data."""
        if timeframe == 'latest':
            # Single data point for the latest reading
            return {
                'timestamp': datetime.now().isoformat(),
                'temperature': round(15 + 10 * random.random(), 1),
                'humidity': round(60 + 20 * random.random(), 1),
                'pressure': round(1010 + 10 * random.random(), 1),
                'wind_speed': round(5 + 10 * random.random(), 1),
                'wind_direction': random.choice(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']),
                'rain_last_hour': round(random.random() * 2, 1) if random.random() > 0.7 else 0,
                'solar_radiation': round(400 + 600 * random.random(), 1),
                'battery': round(70 + 30 * random.random(), 1)
            }
        else:
            # Multiple data points for time series
            # Implementation similar to soil sensor but with weather-specific metrics
            return []
    
    def _generate_irrigation_sensor_data(self, sensor, timeframe):
        """Generate simulated irrigation controller data."""
        zones = sensor.get('zones', 1)
        
        if timeframe == 'latest':
            # Generate data for each zone
            zone_data = []
            for i in range(zones):
                # Random but realistic irrigation data
                is_active = random.random() > 0.8
                
                zone_data.append({
                    'zone': i + 1,
                    'name': f"Zone {i+1}",
                    'status': 'active' if is_active else 'inactive',
                    'flow_rate': round(10 + 5 * random.random(), 1) if is_active else 0,
                    'last_activation': (datetime.now() - timedelta(hours=random.randint(1, 72))).isoformat(),
                    'duration': random.randint(15, 60) if is_active else 0,
                    'scheduled_next': (datetime.now() + timedelta(hours=random.randint(1, 48))).isoformat() if random.random() > 0.3 else None
                })
            
            return {
                'timestamp': datetime.now().isoformat(),
                'controller_status': 'online',
                'battery': round(70 + 30 * random.random(), 1),
                'zones': zone_data
            }
        else:
            # Historical irrigation data
            # Implementation would return irrigation events over time
            return []
    
    def send_command(self, device_id, command, parameters=None):
        """
        Send a command to an IoT device.
        
        Args:
            device_id (str): ID of the device to send command to
            command (str): Command to send
            parameters (dict, optional): Command parameters
            
        Returns:
            dict: Command response
        """
        # In a real implementation, this would send commands to actual devices
        # For demo purposes, return a simulated response
        
        return {
            'device_id': device_id,
            'command': command,
            'parameters': parameters,
            'status': 'accepted',
            'timestamp': datetime.now().isoformat(),
            'message': f"Command {command} sent to device {device_id}"
        } 