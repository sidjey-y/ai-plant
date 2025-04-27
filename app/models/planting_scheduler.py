import os
import logging
import random
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PlantingScheduler:
    """
    Stub implementation for the planting scheduler.
    """
    
    def __init__(self):
        """
        Initialize the planting scheduler.
        """
        self.crops = [
            "Corn", "Soybeans", "Wheat", "Potatoes", "Tomatoes", 
            "Lettuce", "Carrots", "Beans", "Peppers", "Cucumbers"
        ]
        logger.info("Initialized stub PlantingScheduler")
    
    def get_optimal_planting_date(self, crop_name, location, planting_year=None):
        """
        Calculate optimal planting date for a crop at a specific location.
        
        Args:
            crop_name (str): Name of the crop
            location (dict): Location information including latitude, longitude
            planting_year (int, optional): Year for planting, defaults to current year
            
        Returns:
            dict: Optimal planting date information
        """
        if not planting_year:
            planting_year = datetime.now().year
        
        return self._generate_mock_planting_dates(crop_name, location, planting_year)
    
    def _generate_mock_planting_dates(self, crop_name, location, year):
        """
        Generate mock planting date information.
        
        Args:
            crop_name (str): Name of the crop
            location (dict): Location information
            year (int): Planting year
            
        Returns:
            dict: Mock planting date information
        """
        if crop_name not in self.crops:
            return {
                'success': False,
                'error': f"Crop '{crop_name}' not found in database"
            }
        
        seed_map = {
            "Corn": {"month": 4, "day": 15, "window": 21},
            "Soybeans": {"month": 5, "day": 5, "window": 21},
            "Wheat": {"month": 9, "day": 20, "window": 30},
            "Potatoes": {"month": 4, "day": 1, "window": 15},
            "Tomatoes": {"month": 5, "day": 10, "window": 14},
            "Lettuce": {"month": 3, "day": 15, "window": 14},
            "Carrots": {"month": 4, "day": 1, "window": 21},
            "Beans": {"month": 5, "day": 1, "window": 14},
            "Peppers": {"month": 5, "day": 15, "window": 14},
            "Cucumbers": {"month": 5, "day": 10, "window": 14}
        }
        
        crop_data = seed_map.get(crop_name)
        
        base_date = datetime(year, crop_data["month"], crop_data["day"])
        random_days = random.randint(-3, 3)  # Add some randomness
        optimal_date = base_date + timedelta(days=random_days)
        
        start_date = optimal_date - timedelta(days=crop_data["window"]//2)
        end_date = optimal_date + timedelta(days=crop_data["window"]//2)
        
        factors = [
            {
                "factor": "Soil Temperature",
                "status": random.choice(["Optimal", "Below Optimal", "Above Optimal"]),
                "value": f"{45 + random.randint(0, 20)}°F",
                "ideal": "50-55°F"
            },
            {
                "factor": "Soil Moisture",
                "status": random.choice(["Optimal", "Too Dry", "Too Wet"]),
                "value": f"{25 + random.randint(0, 15)}%",
                "ideal": "30-35%"
            },
            {
                "factor": "Frost Risk",
                "status": random.choice(["Low", "Medium", "High"]),
                "value": f"{random.randint(5, 20)}%",
                "ideal": "<10%"
            },
            {
                "factor": "Growing Degree Days",
                "status": random.choice(["Sufficient", "Insufficient"]),
                "value": str(random.randint(80, 150)),
                "ideal": ">120"
            }
        ]
        
        return {
            'success': True,
            'crop': crop_name,
            'location': f"{location.get('city', 'Unknown')}, {location.get('state', 'Unknown')}",
            'coordinates': {
                'latitude': location.get('latitude', 0),
                'longitude': location.get('longitude', 0)
            },
            'optimal_date': optimal_date.strftime("%Y-%m-%d"),
            'planting_window': {
                'start_date': start_date.strftime("%Y-%m-%d"),
                'end_date': end_date.strftime("%Y-%m-%d"),
                'duration_days': crop_data["window"]
            },
            'confidence': random.randint(70, 95),
            'influencing_factors': factors,
            'special_considerations': [
                f"Adjust planting depth according to soil moisture.",
                f"Consider using a starter fertilizer for {crop_name}."
            ]
        } 