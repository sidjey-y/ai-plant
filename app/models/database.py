from datetime import datetime
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    farms = db.relationship('Farm', backref='owner', lazy='dynamic')
    
    def __repr__(self):
        return f'<User {self.username}>'

class Farm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    size_hectares = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    fields = db.relationship('Field', backref='farm', lazy='dynamic')
    
    def __repr__(self):
        return f'<Farm {self.name}>'

class Field(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    area_hectares = db.Column(db.Float, nullable=False)
    crop_type = db.Column(db.String(50))
    planting_date = db.Column(db.Date)
    harvest_date = db.Column(db.Date)
    farm_id = db.Column(db.Integer, db.ForeignKey('farm.id'), nullable=False)
    soil_records = db.relationship('SoilRecord', backref='field', lazy='dynamic')
    pest_records = db.relationship('PestRecord', backref='field', lazy='dynamic')
    
    def __repr__(self):
        return f'<Field {self.name}>'

class SoilRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    ph_level = db.Column(db.Float)
    moisture_percentage = db.Column(db.Float)
    nitrogen_level = db.Column(db.Float)
    phosphorus_level = db.Column(db.Float)
    potassium_level = db.Column(db.Float)
    temperature = db.Column(db.Float)
    field_id = db.Column(db.Integer, db.ForeignKey('field.id'), nullable=False)
    
    def __repr__(self):
        return f'<SoilRecord {self.id} for Field {self.field_id}>'

class PestRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    pest_type = db.Column(db.String(100))
    severity = db.Column(db.Integer)  
    detection_method = db.Column(db.String(50))  # 'manual', 'image', 'sensor'
    image_path = db.Column(db.String(200))
    notes = db.Column(db.Text)
    field_id = db.Column(db.Integer, db.ForeignKey('field.id'), nullable=False)
    
    def __repr__(self):
        return f'<PestRecord {self.id} for Field {self.field_id}>'

class WeatherRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    temperature = db.Column(db.Float)
    humidity = db.Column(db.Float)
    precipitation = db.Column(db.Float)
    wind_speed = db.Column(db.Float)
    wind_direction = db.Column(db.String(10))
    farm_id = db.Column(db.Integer, db.ForeignKey('farm.id'), nullable=False)
    
    def __repr__(self):
        return f'<WeatherRecord {self.id} for Farm {self.farm_id}>'

class PlantingRecommendation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    crop_type = db.Column(db.String(50), nullable=False)
    recommended_date = db.Column(db.Date, nullable=False)
    confidence_score = db.Column(db.Float)  # 0-1 scale
    reasoning = db.Column(db.Text)
    field_id = db.Column(db.Integer, db.ForeignKey('field.id'), nullable=False)
    
    def __repr__(self):
        return f'<PlantingRecommendation {self.id} for Field {self.field_id}>'

class IoTDevice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100))
    device_type = db.Column(db.String(50))  # 'soil', 'weather', 'pest', etc.
    installation_date = db.Column(db.Date, default=datetime.utcnow)
    battery_level = db.Column(db.Float)  # Percentage
    last_communication = db.Column(db.DateTime)
    firmware_version = db.Column(db.String(20))
    field_id = db.Column(db.Integer, db.ForeignKey('field.id'), nullable=False)
    
    def __repr__(self):
        return f'<IoTDevice {self.device_id}>' 