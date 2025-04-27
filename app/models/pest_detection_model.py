import os
import numpy as np
import logging
import random

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PestDetectionModel:
    """
    Stub model for detecting pests in crop images.
    """
    
    def __init__(self, model_path=None):
        """
        Initialize the pest detection model.
        
        Args:
            model_path (str, optional): Path to load a pre-trained model
        """
        self.model_path = model_path
        self.pest_classes = [
            'Aphids', 'Armyworms', 'Corn Borers', 'Cutworms', 
            'Grasshoppers', 'Japanese Beetles', 'Spider Mites', 
            'Stink Bugs', 'Thrips', 'Whiteflies'
        ]
        logger.info("Initialized stub PestDetectionModel")
    
    def predict(self, image_path):
        """
        Make predictions using the stub model.
        
        Args:
            image_path (str): Path to the image file
            
        Returns:
            dict: Predicted pest information
        """
        if not os.path.exists(image_path):
            return {
                'success': False,
                'error': 'Image file not found'
            }
        
        return self._generate_mock_results(image_path)
    
    def _generate_mock_results(self, image_path):
        """
        Generate mock pest detection results for demonstration purposes.
        
        Args:
            image_path (str): Path to the image
            
        Returns:
            dict: Mock pest detection results
        """
        num_pests = random.randint(1, 3)
        detected_pests = random.sample(self.pest_classes, num_pests)
        
        results = []
        for pest in detected_pests:
            confidence = round(0.7 + 0.3 * random.random(), 2)  # Between 0.7 and 1.0
            severity = random.choice(['Low', 'Medium', 'High'])
            coverage = round(5 + 25 * random.random(), 1)  # Between 5% and 30%
            
            results.append({
                'pest': pest,
                'confidence': confidence,
                'severity': severity,
                'coverage_percent': coverage,
                'bounding_box': {
                    'x': random.randint(10, 100),
                    'y': random.randint(10, 100),
                    'width': random.randint(50, 200),
                    'height': random.randint(50, 200)
                }
            })
        
        results.sort(key=lambda x: x['confidence'], reverse=True)
        
        return {
            'success': True,
            'image_path': image_path,
            'analyzed_at': '2023-11-01T12:34:56',
            'detections': results,
            'recommendations': [
                'Monitor field for increased pest activity',
                'Consider targeted pesticide application if severity increases',
                'Check surrounding fields for similar infestations'
            ]
        } 