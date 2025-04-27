import os
from pathlib import Path
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from app import create_app, db

load_dotenv()

BASEDIR = os.path.abspath(os.path.dirname(__file__))
instance_dir = os.path.join(BASEDIR, 'instance')
os.makedirs(instance_dir, exist_ok=True)

app = create_app()

db_path = os.path.join(instance_dir, 'agriculture_assistant.db')

if not os.path.exists(db_path):
    with open(db_path, 'w') as f:
        pass  
    
    try:
        os.chmod(db_path, 0o666) 
        print(f"Database file created at: {db_path}")
    except Exception as e:
        print(f"Warning: Could not set file permissions: {e}")

from app.routes.dashboard_routes import dashboard_bp
app.register_blueprint(dashboard_bp, url_prefix='/dashboard')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("Database tables created successfully.")
    app.run(debug=True, host='0.0.0.0') 