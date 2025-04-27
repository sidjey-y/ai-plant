from flask import Blueprint, render_template, request, jsonify, session, flash, redirect, url_for
from flask_login import login_required
import os
import json
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import random

from app.models.planting_scheduler import PlantingScheduler

# Initialize planting scheduler
planting_scheduler = PlantingScheduler()

planting_bp = Blueprint('planting', __name__)

@planting_bp.route('/')
@login_required
def planting_dashboard():
    """Main planting schedule dashboard."""
    return render_template('planting/dashboard.html')

@planting_bp.route('/schedule')
@login_required
def planting_schedule():
    """View and manage planting schedules."""
    field_id = request.args.get('field_id', 1)
    
    # Get planting schedule data for the field
    schedule_data = get_planting_schedule(field_id)
    
    return render_template('planting/schedule.html', schedule_data=schedule_data, field_id=field_id)

@planting_bp.route('/recommendations')
@login_required
def planting_recommendations():
    """View planting recommendations."""
    field_id = request.args.get('field_id', 1)
    crop_type = request.args.get('crop', None)
    
    # Get planting recommendations
    recommendations = get_planting_recommendations(field_id, crop_type)
    
    return render_template('planting/recommendations.html', recommendations=recommendations, field_id=field_id)

@planting_bp.route('/history')
@login_required
def planting_history():
    """View planting history and results."""
    field_id = request.args.get('field_id', 1)
    
    # Get planting history data
    history_data = get_planting_history(field_id)
    
    return render_template('planting/history.html', history_data=history_data, field_id=field_id)

@planting_bp.route('/api/schedule')
@login_required
def api_planting_schedule():
    """API endpoint to get planting schedule data."""
    field_id = request.args.get('field_id', 1)
    
    # Get planting schedule data
    schedule_data = get_planting_schedule(field_id)
    
    return jsonify(schedule_data)

@planting_bp.route('/api/recommendations')
@login_required
def api_planting_recommendations():
    """API endpoint to get planting recommendations."""
    field_id = request.args.get('field_id', 1)
    crop_type = request.args.get('crop', None)
    
    # Get planting recommendations
    recommendations = get_planting_recommendations(field_id, crop_type)
    
    return jsonify(recommendations)

@planting_bp.route('/api/optimal-date', methods=['POST'])
@login_required
def api_optimal_planting_date():
    """API endpoint to calculate optimal planting date for a crop."""
    data = request.get_json()
    
    field_id = data.get('field_id', 1)
    crop_type = data.get('crop_type')
    
    if not crop_type:
        return jsonify({'error': 'Crop type is required'})
    
    # Get optimal planting date
    result = calculate_optimal_planting_date(field_id, crop_type)
    
    return jsonify(result)

# Helper functions

def get_planting_schedule(field_id):
    """
    Get planting schedule for a field.
    
    Args:
        field_id: ID of the field
        
    Returns:
        dict: Planting schedule data
    """
    # In a real app, this would query the database
    # For demo purposes, we'll generate simulated data
    
    # Define common crops
    crops = ['Corn', 'Wheat', 'Soybean', 'Cotton', 'Potato']
    
    # Generate current schedule
    current_schedule = []
    for crop in random.sample(crops, min(3, len(crops))):
        # Random planting window
        start_date = datetime.now() + timedelta(days=random.randint(-30, 60))
        optimal_date = start_date + timedelta(days=random.randint(5, 10))
        end_date = optimal_date + timedelta(days=random.randint(5, 10))
        
        current_schedule.append({
            'crop': crop,
            'field_id': field_id,
            'start_date': start_date.strftime('%Y-%m-%d'),
            'optimal_date': optimal_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
            'confidence': round(random.uniform(0.7, 0.95), 2)
        })
    
    # Sort by optimal date
    current_schedule.sort(key=lambda x: x['optimal_date'])
    
    return {
        'field_id': field_id,
        'current_schedule': current_schedule
    }

def get_planting_recommendations(field_id, crop_type=None):
    """
    Get planting recommendations for a field.
    
    Args:
        field_id: ID of the field
        crop_type: Type of crop (optional)
        
    Returns:
        dict: Planting recommendations
    """
    # In a real app, this would use the ML model
    # For demo purposes, we'll generate simulated data
    
    # Define common crops
    all_crops = ['Corn', 'Wheat', 'Soybean', 'Cotton', 'Potato']
    
    # Filter by crop type if specified
    if crop_type and crop_type in all_crops:
        crops = [crop_type]
    else:
        # If no crop specified, provide recommendations for all suitable crops
        crops = all_crops
    
    # Generate recommendations
    recommendations = []
    for crop in crops:
        # Random planting window
        start_date = datetime.now() + timedelta(days=random.randint(7, 30))
        optimal_date = start_date + timedelta(days=random.randint(5, 10))
        end_date = optimal_date + timedelta(days=random.randint(5, 10))
        
        recommendations.append({
            'crop': crop,
            'field_id': field_id,
            'planting_window': {
                'start': start_date.strftime('%Y-%m-%d'),
                'optimal': optimal_date.strftime('%Y-%m-%d'),
                'end': end_date.strftime('%Y-%m-%d')
            },
            'confidence': round(random.uniform(0.7, 0.95), 2),
            'expected_yield': f"{random.randint(70, 95)}%",
            'factors': [
                'Soil temperature',
                'Weather forecast',
                'Soil moisture',
                'Historical yield data'
            ]
        })
    
    # Sort by confidence (highest first)
    recommendations.sort(key=lambda x: x['confidence'], reverse=True)
    
    return {
        'field_id': field_id,
        'crop_type': crop_type,
        'recommendations': recommendations
    }

def get_planting_history(field_id):
    """
    Get planting history for a field.
    
    Args:
        field_id: ID of the field
        
    Returns:
        dict: Planting history data
    """
    # In a real app, this would query the database
    # For demo purposes, we'll generate simulated data
    
    # Define common crops
    crops = ['Corn', 'Wheat', 'Soybean', 'Cotton', 'Potato']
    
    # Generate history records for past seasons
    history = []
    current_year = datetime.now().year
    
    for year in range(current_year - 3, current_year):
        # Random crop rotation
        season_crop = random.choice(crops)
        
        # Random planting and harvest dates
        planting_date = datetime(year, random.randint(3, 6), random.randint(1, 28))
        harvest_date = datetime(year, random.randint(8, 11), random.randint(1, 28))
        
        # Random yield data
        expected_yield = random.randint(70, 90)
        actual_yield = expected_yield + random.randint(-15, 10)
        
        history.append({
            'year': year,
            'season': f"{year} Growing Season",
            'crop': season_crop,
            'field_id': field_id,
            'planting_date': planting_date.strftime('%Y-%m-%d'),
            'harvest_date': harvest_date.strftime('%Y-%m-%d'),
            'expected_yield': f"{expected_yield}%",
            'actual_yield': f"{actual_yield}%",
            'success_factors' if actual_yield >= expected_yield else 'challenges': [
                random.choice([
                    'Optimal weather conditions',
                    'Effective pest management',
                    'Ideal soil conditions',
                    'Drought conditions',
                    'Unexpected pest outbreak',
                    'Heavy rainfall'
                ])
            ]
        })
    
    # Sort by year (most recent first)
    history.sort(key=lambda x: x['year'], reverse=True)
    
    return {
        'field_id': field_id,
        'history': history
    }

def calculate_optimal_planting_date(field_id, crop_type):
    """
    Calculate the optimal planting date for a specific crop.
    
    Args:
        field_id: ID of the field
        crop_type: Type of crop
        
    Returns:
        dict: Optimal planting information
    """
    # In a real app, this would use the ML model
    # For demo purposes, we'll generate simulated data
    
    # Random planting window
    start_date = datetime.now() + timedelta(days=random.randint(7, 30))
    optimal_date = start_date + timedelta(days=random.randint(5, 10))
    end_date = optimal_date + timedelta(days=random.randint(5, 10))
    
    # Random confidence score
    confidence = round(random.uniform(0.7, 0.95), 2)
    
    # Generate factors that influenced the recommendation
    factors = [
        {
            'name': 'Soil temperature',
            'value': f"{random.randint(15, 25)}°C",
            'impact': 'positive' if random.random() > 0.3 else 'negative'
        },
        {
            'name': 'Precipitation forecast',
            'value': f"{random.randint(10, 50)} mm expected",
            'impact': 'positive' if random.random() > 0.3 else 'negative'
        },
        {
            'name': 'Soil moisture',
            'value': f"{random.randint(30, 60)}%",
            'impact': 'positive' if random.random() > 0.3 else 'negative'
        },
        {
            'name': 'Historical data',
            'value': f"Based on {random.randint(3, 10)} seasons",
            'impact': 'positive' if random.random() > 0.3 else 'neutral'
        }
    ]
    
    return {
        'field_id': field_id,
        'crop_type': crop_type,
        'planting_window': {
            'start': start_date.strftime('%Y-%m-%d'),
            'optimal': optimal_date.strftime('%Y-%m-%d'),
            'end': end_date.strftime('%Y-%m-%d')
        },
        'confidence': confidence,
        'factors': factors,
        'days_until_optimal': (optimal_date - datetime.now()).days
    } 