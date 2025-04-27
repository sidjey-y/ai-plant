from flask import Blueprint, render_template, request, redirect, url_for, flash, session

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Landing page of the application."""
    return render_template('index.html')

@main_bp.route('/dashboard')
def dashboard():
    """Redirect to soil nutrients page instead of requiring login."""
    return redirect(url_for('soil.nutrients'))

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Redirect to soil nutrients page instead of actual login."""
    if request.method == 'POST':
        flash('Login feature is currently disabled in demo mode. Redirecting to soil analysis.', 'info')
        return redirect(url_for('soil.nutrients'))
    return redirect(url_for('soil.nutrients'))

@main_bp.route('/logout')
def logout():
    """User logout."""
    session.clear()
    return redirect(url_for('main.index'))

@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Redirect to soil nutrients page instead of actual registration."""
    if request.method == 'POST':
        flash('Registration feature is currently disabled in demo mode. Redirecting to soil analysis.', 'info')
        return redirect(url_for('soil.nutrients'))
    return redirect(url_for('soil.nutrients'))

@main_bp.route('/fields')
def fields():
    """Fields management page."""
    return render_template('fields.html')

@main_bp.route('/irrigation')
def irrigation():
    """Irrigation management page."""
    return render_template('irrigation.html')

@main_bp.route('/weather')
def weather():
    """Weather forecasts and data page."""
    return render_template('weather.html')

@main_bp.route('/soil')
def soil():
    """Redirect to soil analysis dashboard."""
    return redirect(url_for('main.soil_analysis'))

@main_bp.route('/soil_analysis')
def soil_analysis():
    """Soil analysis dashboard."""
    return render_template('soil_analysis.html')

@main_bp.route('/about')
def about():
    """About page with information about the application."""
    return render_template('index.html', _anchor='about')

@main_bp.route('/contact')
def contact():
    """Contact page with form to contact support."""
    return redirect(url_for('main.index'))

@main_bp.route('/help')
def help_page():
    """Help page with documentation and guides."""
    return redirect(url_for('main.index'))

@main_bp.route('/terms')
def terms():
    """Terms of Service page."""
    return redirect(url_for('main.index'))

@main_bp.route('/privacy')
def privacy():
    """Privacy Policy page."""
    return redirect(url_for('main.index')) 