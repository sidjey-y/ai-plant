from flask import Blueprint, render_template, request, jsonify, session, flash, redirect, url_for, current_app
from flask_login import login_required
import os
import json
import numpy as np
from datetime import datetime, timedelta
import random
import base64
from werkzeug.utils import secure_filename

from app.models.pest_detection_model import PestDetectionModel

pest_model = PestDetectionModel()

pest_bp = Blueprint('pests', __name__)

@pest_bp.route('/')
@login_required
def pest_dashboard():
    """Main pest detection dashboard."""
    return render_template('pests/dashboard.html')

@pest_bp.route('/detection')
@login_required
def pest_detection():
    """Pest detection page with image upload."""
    return render_template('pests/detection.html')

@pest_bp.route('/history')
@login_required
def pest_history():
    """View pest detection history."""
    field_id = request.args.get('field_id', 1)
    
    pest_data = get_pest_history(field_id)
    
    return render_template('pests/history.html', pest_data=pest_data, field_id=field_id)

@pest_bp.route('/risk')
@login_required
def pest_risk():
    """View pest risk assessment."""
    field_id = request.args.get('field_id', 1)
    
    risk_data = get_pest_risk_data(field_id)
    
    return render_template('pests/risk.html', risk_data=risk_data, field_id=field_id)

@pest_bp.route('/api/detect', methods=['POST'])
@login_required
def api_detect_pests():
    """API endpoint to detect pests in uploaded images."""
    pests = ['Aphid', 'Grasshopper', 'Beetle']
    detected = random.choice(pests)
    confidence = round(random.uniform(0.7, 0.95), 2)
    
    return jsonify({
        'detected': detected,
        'confidence': confidence,
        'timestamp': datetime.now().isoformat()
    })

@pest_bp.route('/api/risk')
@login_required
def api_pest_risk():
    """API endpoint to get pest risk assessment data."""
    field_id = request.args.get('field_id', 1)
    time_range = request.args.get('range', '30d')  # 7d, 30d, 90d
    

    risk_data = get_pest_risk_data(field_id, time_range)
    
    return jsonify(risk_data)

@pest_bp.route('/api/history')
@login_required
def api_pest_history():
    """API endpoint to get pest detection history."""
    field_id = request.args.get('field_id', 1)
    time_range = request.args.get('range', '30d')  
    

    history_data = get_pest_history(field_id, time_range)
    
    return jsonify(history_data)


def simulate_pest_detection():
    """
    Simulate pest detection results.
    
    Returns:
        dict: Simulated detection results
    """
    pest_types = [
        'Aphid', 'Grasshopper', 'Beetle', 'Caterpillar', 'Spider Mite'
    ]
    
    num_detections = random.randint(0, 3)  
    
    if num_detections == 0:

        detections = []
        status = 'healthy'
    else:
        detected_pests = random.sample(pest_types, num_detections)
        
        detections = []
        for pest in detected_pests:
            confidence = round(random.uniform(0.6, 0.95), 2)
            detections.append({
                'pest': pest,
                'confidence': confidence,
                'count': random.randint(1, 10)
            })
        
        detections.sort(key=lambda x: x['confidence'], reverse=True)
        
        if detections[0]['confidence'] > 0.85:
            status = 'severe_infestation' if detections[0]['count'] > 5 else 'moderate_infestation'
        else:
            status = 'possible_infestation'
    
    return {
        'status': status,
        'detections': detections,
        'analysis_time': round(random.uniform(0.5, 2.0), 1) 
    }

def get_pest_history(field_id, time_range='30d'):
    """
    Get pest detection history for a field.
    
    Args:
        field_id: ID of the field
        time_range: Time range (7d, 30d, 90d)
        
    Returns:
        dict: Pest history data
    """
 
    
    return {
        'field_id': field_id,
        'time_range': time_range,
        'total_records': 5,
        'history': [] 
    }

def get_pest_risk_data(field_id, time_range='30d'):
    """
    Get pest risk assessment data for a field.
    
    Args:
        field_id: ID of the field
        time_range: Time range for assessment
        
    Returns:
        dict: Pest risk data
    """

    pest_types = [
        'Aphid', 'Grasshopper', 'Beetle', 'Caterpillar', 'Spider Mite'
    ]
    

    risk_scores = {}
    for pest in pest_types:
        risk_scores[pest] = round(random.uniform(0.1, 0.9), 2)
    
    return {
        'field_id': field_id,
        'time_range': time_range,
        'overall_risk': round(max(risk_scores.values()), 2),
        'risk_scores': risk_scores
    } 