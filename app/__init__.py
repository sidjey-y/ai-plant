
import sys
import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_key_for_testing')
    
    db.init_app(app)
    
    from app.routes.main_routes import main_bp
    from app.routes.soil_routes import soil_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(soil_bp, url_prefix='/soil')
    
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template('errors/500.html'), 500
    
    return app 