import os
import requests
import json
import logging
import random
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AgrimetricsAPI:
    """
    Service class to interact with the Agrimetrics API for retrieving
    agricultural data related to soil quality, weather, and crop information.
    
    This is a demo version that returns simulated data.
    """
    
    def __init__(self):
        self.api_key = os.getenv('AGRIMETRICS_API_KEY')
        self.base_url = 'https://api.agrimetrics.co.uk/v1'
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        if not self.api_key:
            logger.warning("Agrimetrics API key not found. API calls will fail.")
    
    def _make_request(self, endpoint, method='GET', params=None, data=None):
        """
        Simulate a request to the Agrimetrics API.
        
        Args:
            endpoint (str): API endpoint to call
            method (str): HTTP method (GET, POST, etc.)
            params (dict): Query parameters
            data (dict): Request body for POST/PUT requests
            
        Returns:
            dict: Simulated response data
        """
        #this would make an actual API call - simulation only

        
        if endpoint == 'soil-properties':
            return self._simulate_soil_properties(params)
        elif endpoint == 'weather/forecast':
            return self._simulate_weather_forecast(params)
        elif endpoint == 'crop-calendar':
            return self._simulate_crop_calendar(params)
        elif endpoint == 'pest-risk':
            return self._simulate_pest_risk(params)
        elif endpoint == 'soil-moisture':
            return self._simulate_soil_moisture(params)
        else:
            return {'error': f'Unknown endpoint: {endpoint}'}
    
    def get_soil_data(self, latitude, longitude, date=None):
        """
        Get soil data for a specific location.
        
        Args:
            latitude (float): Latitude coordinate
            longitude (float): Longitude coordinate
            date (str, optional): Date in ISO format (YYYY-MM-DD)
            
        Returns:
            dict: Soil data including pH, nutrients, moisture, etc.
        """
        endpoint = 'soil-properties'
        params = {
            'lat': latitude,
            'lon': longitude
        }
        
        if date:
            params['date'] = date
            
        return self._make_request(endpoint, params=params)
    
    def get_weather_forecast(self, latitude, longitude, days=7):
        """
        Get weather forecast for a specific location.
        
        Args:
            latitude (float): Latitude coordinate
            longitude (float): Longitude coordinate
            days (int): Number of days to forecast (default: 7)
            
        Returns:
            dict: Weather forecast data
        """
        endpoint = 'weather/forecast'
        params = {
            'lat': latitude,
            'lon': longitude,
            'days': days
        }
        
        return self._make_request(endpoint, params=params)
    
    def get_crop_calendar(self, crop_type, latitude, longitude):
        """
        Get recommended planting and harvesting dates for a specific crop.
        
        Args:
            crop_type (str): Type of crop
            latitude (float): Latitude coordinate
            longitude (float): Longitude coordinate
            
        Returns:
            dict: Crop calendar information
        """
        endpoint = 'crop-calendar'
        params = {
            'crop': crop_type,
            'lat': latitude,
            'lon': longitude
        }
        
        return self._make_request(endpoint, params=params)
    
    def get_pest_risk(self, crop_type, latitude, longitude, date=None):
        """
        Get pest risk assessment for a specific crop and location.
        
        Args:
            crop_type (str): Type of crop
            latitude (float): Latitude coordinate
            longitude (float): Longitude coordinate
            date (str, optional): Date in ISO format (YYYY-MM-DD)
            
        Returns:
            dict: Pest risk information
        """
        endpoint = 'pest-risk'
        params = {
            'crop': crop_type,
            'lat': latitude,
            'lon': longitude
        }
        
        if date:
            params['date'] = date
            
        return self._make_request(endpoint, params=params)
    
    def get_soil_moisture(self, latitude, longitude, date=None):
        """
        Get soil moisture data for a specific location.
        
        Args:
            latitude (float): Latitude coordinate
            longitude (float): Longitude coordinate
            date (str, optional): Date in ISO format (YYYY-MM-DD)
            
        Returns:
            dict: Soil moisture data
        """
        endpoint = 'soil-moisture'
        params = {
            'lat': latitude,
            'lon': longitude
        }
        
        if date:
            params['date'] = date
            
        return self._make_request(endpoint, params=params)
    
    
    def _simulate_soil_properties(self, params):
        """Simulate soil properties data."""
        latitude = params.get('lat', 51.5074)
        longitude = params.get('lon', -0.1278)
        date = params.get('date', datetime.now().strftime('%Y-%m-%d'))
        
        seed = int(float(latitude) * 100 + float(longitude) * 100)
        random.seed(seed)
        
        return {
            'request': {
                'latitude': latitude,
                'longitude': longitude,
                'date': date
            },
            'source': 'Agrimetrics API (Demo)',
            'soil_data': {
                'texture': random.choice(['Loam', 'Clay Loam', 'Sandy Loam', 'Silt Loam', 'Clay', 'Sandy Clay']),
                'ph': round(6.0 + 2.0 * random.random(), 1),
                'organic_matter': round(2.0 + 4.0 * random.random(), 1),
                'moisture': round(30 + 20 * random.random(), 1),
                'temperature': round(12 + 8 * random.random(), 1),
                'nutrients': {
                    'nitrogen': round(35 + 25 * random.random(), 1),
                    'phosphorus': round(15 + 25 * random.random(), 1),
                    'potassium': round(150 + 100 * random.random(), 1),
                    'calcium': round(1000 + 1000 * random.random(), 1),
                    'magnesium': round(100 + 150 * random.random(), 1),
                    'sulfur': round(5 + 15 * random.random(), 1),
                    'iron': round(80 + 50 * random.random(), 1),
                    'manganese': round(30 + 20 * random.random(), 1),
                    'zinc': round(2 + 4 * random.random(), 1),
                    'copper': round(1 + 2 * random.random(), 1),
                    'boron': round(0.5 + 1.5 * random.random(), 1)
                },
                'cation_exchange_capacity': round(10 + 10 * random.random(), 1),
                'electrical_conductivity': round(0.5 + 0.5 * random.random(), 2)
            },
            'recommendations': {
                'ideal_crops': random.sample(['Wheat', 'Corn', 'Soybeans', 'Barley', 'Potatoes', 'Carrots', 'Lettuce'], 3),
                'fertilization': [
                    {'nutrient': 'Nitrogen', 'amount': f"{round(10 + 40 * random.random())} kg/ha"},
                    {'nutrient': 'Phosphorus', 'amount': f"{round(5 + 15 * random.random())} kg/ha"},
                    {'nutrient': 'Potassium', 'amount': f"{round(20 + 30 * random.random())} kg/ha"}
                ],
                'soil_management': random.choice([
                    'Consider adding organic matter to improve soil structure',
                    'Apply lime to adjust pH if growing acid-sensitive crops',
                    'Incorporate cover crops to enhance soil health',
                    'Implement crop rotation to maintain soil fertility'
                ])
            }
        }
    
    def _simulate_weather_forecast(self, params):
        """Simulate weather forecast data."""
        latitude = params.get('lat', 51.5074)
        longitude = params.get('lon', -0.1278)
        days = int(params.get('days', 7))
        
        forecast = []
        for i in range(days):
            date = (datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + 
                    datetime.timedelta(days=i)).strftime('%Y-%m-%d')
            
            min_temp = round(10 + 5 * random.random(), 1)
            max_temp = min_temp + round(5 + 5 * random.random(), 1)
            
            forecast.append({
                'date': date,
                'temperature': {
                    'min': min_temp,
                    'max': max_temp,
                    'unit': 'C'
                },
                'humidity': round(60 + 30 * random.random(), 1),
                'precipitation': {
                    'probability': round(100 * random.random(), 1),
                    'amount': round(10 * random.random(), 1) if random.random() > 0.5 else 0,
                    'unit': 'mm'
                },
                'wind': {
                    'speed': round(15 * random.random(), 1),
                    'direction': random.choice(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']),
                    'unit': 'km/h'
                },
                'uv_index': round(1 + 9 * random.random(), 1)
            })
        
        return {
            'request': {
                'latitude': latitude,
                'longitude': longitude,
                'days': days
            },
            'source': 'Agrimetrics API (Demo)',
            'forecast': forecast
        }
    
    def _simulate_crop_calendar(self, params):
        """Simulate crop calendar data."""
        crop = params.get('crop', 'wheat')
        latitude = params.get('lat', 51.5074)
        longitude = params.get('lon', -0.1278)
        
        crop_data = {
            'wheat': {
                'planting_start': 'September 15',
                'planting_end': 'November 15',
                'harvest_start': 'July 15',
                'harvest_end': 'August 31'
            },
            'corn': {
                'planting_start': 'April 20',
                'planting_end': 'May 31',
                'harvest_start': 'September 15',
                'harvest_end': 'November 15'
            },
            'soybeans': {
                'planting_start': 'May 10',
                'planting_end': 'June 20',
                'harvest_start': 'September 25',
                'harvest_end': 'October 31'
            },
            'potatoes': {
                'planting_start': 'March 15',
                'planting_end': 'May 1',
                'harvest_start': 'August 1',
                'harvest_end': 'October 15'
            }
        }
        
        crop_info = crop_data.get(crop.lower(), crop_data['wheat'])
        
        return {
            'request': {
                'crop': crop,
                'latitude': latitude,
                'longitude': longitude
            },
            'source': 'Agrimetrics API (Demo)',
            'calendar': {
                'planting_window': {
                    'start': crop_info['planting_start'],
                    'end': crop_info['planting_end'],
                    'optimal': self._get_middle_date(crop_info['planting_start'], crop_info['planting_end'])
                },
                'harvest_window': {
                    'start': crop_info['harvest_start'],
                    'end': crop_info['harvest_end'],
                    'optimal': self._get_middle_date(crop_info['harvest_start'], crop_info['harvest_end'])
                },
                'growing_days': random.randint(90, 180),
                'growing_degree_days': random.randint(1500, 3000),
                'notes': f"Best results are achieved when planting around {crop_info['planting_start']}."
            }
        }
    
    def _simulate_pest_risk(self, params):
        """Simulate pest risk data."""
        crop = params.get('crop', 'wheat')
        latitude = params.get('lat', 51.5074)
        longitude = params.get('lon', -0.1278)
        date = params.get('date', datetime.now().strftime('%Y-%m-%d'))
        
        crop_pests = {
            'wheat': ['Aphids', 'Rust', 'Septoria', 'Mildew', 'Fusarium'],
            'corn': ['Corn Rootworm', 'European Corn Borer', 'Armyworm', 'Corn Leaf Aphid'],
            'soybeans': ['Soybean Aphid', 'Bean Leaf Beetle', 'Spider Mites', 'Stink Bugs'],
            'potatoes': ['Colorado Potato Beetle', 'Potato Leafhopper', 'Wireworms', 'Late Blight']
        }
        
        pests = crop_pests.get(crop.lower(), crop_pests['wheat'])
        
        pest_risks = []
        for pest in pests:
            risk_level = random.choice(['Low', 'Moderate', 'High'])
            risk_score = random.randint(1, 10) if risk_level == 'Low' else \
                         random.randint(11, 70) if risk_level == 'Moderate' else \
                         random.randint(71, 100)
            
            pest_risks.append({
                'pest': pest,
                'risk_level': risk_level,
                'risk_score': risk_score,
                'factors': ['Temperature', 'Humidity', 'Previous Infestations'],
                'recommendation': self._get_pest_recommendation(pest, risk_level)
            })
        
        return {
            'request': {
                'crop': crop,
                'latitude': latitude,
                'longitude': longitude,
                'date': date
            },
            'source': 'Agrimetrics API (Demo)',
            'overall_risk': random.choice(['Low', 'Moderate', 'High']),
            'pest_risks': pest_risks
        }
    
    def _simulate_soil_moisture(self, params):
        """Simulate soil moisture data."""
        latitude = params.get('lat', 51.5074)
        longitude = params.get('lon', -0.1278)
        date = params.get('date', datetime.now().strftime('%Y-%m-%d'))
        
        seed = int(float(latitude) * 100 + float(longitude) * 100)
        random.seed(seed)
        
        return {
            'request': {
                'latitude': latitude,
                'longitude': longitude,
                'date': date
            },
            'source': 'Agrimetrics API (Demo)',
            'moisture_data': {
                'surface': round(30 + 20 * random.random(), 1),
                'root_zone': round(35 + 15 * random.random(), 1),
                'deep_soil': round(40 + 10 * random.random(), 1),
                'soil_capacity': {
                    'field_capacity': round(40 + 10 * random.random(), 1),
                    'permanent_wilting_point': round(15 + 5 * random.random(), 1),
                    'available_water': round(20 + 10 * random.random(), 1)
                },
                'trends': {
                    'daily_change': round(-2 + 4 * random.random(), 1),
                    '7_day_change': round(-5 + 10 * random.random(), 1)
                }
            },
            'irrigation_recommendation': {
                'status': random.choice(['Not Needed', 'Recommended', 'Urgent']),
                'amount': round(5 + 15 * random.random(), 1) if random.random() > 0.3 else 0,
                'next_check': (datetime.now() + datetime.timedelta(days=random.randint(1, 7))).strftime('%Y-%m-%d')
            }
        }
    
    def _get_middle_date(self, start_date, end_date):
        """Helper function to get an approximate middle date between two dates."""
        return f"{start_date} to {end_date}"
    
    def _get_pest_recommendation(self, pest, risk_level):
        """Generate a recommendation based on the pest and risk level."""
        if risk_level == 'Low':
            return f"Monitor {pest} populations but no immediate action required."
        elif risk_level == 'Moderate':
            return f"Consider preventative treatments for {pest} in the next 7-14 days."
        else:  # High
            return f"Immediate treatment recommended for {pest}. Consult with an agronomist for specific options."
        
    def get_field_boundaries(self, field_id=None, user_id=None):
        """
        Get field boundary information.
        
        Args:
            field_id (str, optional): Specific field ID
            user_id (str, optional): User ID to get all fields
            
        Returns:
            dict: Field boundary data in GeoJSON format
        """
        endpoint = 'field-boundaries'
        params = {}
        
        if field_id:
            params['field_id'] = field_id
        elif user_id:
            params['user_id'] = user_id
            
        return self._make_request(endpoint, params=params) 