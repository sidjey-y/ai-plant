# (A)I Plant - AI-Powered Agriculture Monitoring System 

![Dashboard](readme_images/Dashboard.png)

## Overview

(A)I Plant is an intelligent agriculture monitoring system that leverages artificial intelligence to provide real-time soil analysis, nutrient monitoring, and farming recommendations. The platform helps farmers optimize their agricultural practices by offering detailed insights into soil quality, moisture levels, pH balance, and nutrient content across multiple fields.

While (A)I Plant integrates machine learning models for soil quality prediction and recommendation generation, much of the current functionality operates as a simulation to demonstrate the intended AI capabilities. Full integration with live sensor data and real-time AI-driven analysis is planned for future development.

## Key Features

![Key Features](readme_images/Key-Features%20(2).png)

- Monitor soil quality metrics including texture, structure, drainage, and organic matter content
- Track essential nutrients like nitrogen, phosphorus, potassium, calcium, magnesium, and sulfur
- Real-time soil moisture data with alerts for optimal irrigation timing
- Monitor and track soil pH levels for optimal crop growth
- AI-generated recommendations for fertilizer application and soil improvement
- Manage multiple fields with individual monitoring and recommendations
- Weather forecasts and historical data to inform farming decisions
- Automated irrigation scheduling based on soil moisture and weather forecasts

## Screenshots

### Soil Analysis Dashboard
![Soil Analysis](readme_images/Soil.png)

### Nutrient Monitoring
![Nutrient Monitoring](readme_images/Soil-Nutrient.png)

### Field Management
![Field Management](readme_images/Plant-Fields.png)

### Irrigation Control
![Irrigation Control](readme_images/Irrigation.png)

### Weather Forecasting
![Weather Forecasting](readme_images/Weather.png)

### AI Recommendations
![AI Recommendations](readme_images/Recommendations.png)

## Technology Stack

### Frontend
- **HTML5/CSS3**: Modern, responsive layout with custom styling
- **Bootstrap 5.3**: UI framework for responsive design and components
- **JavaScript**: Client-side interactivity and data visualization
- **Chart.js**: Data visualization for soil metrics and trends
- **Font Awesome**: Icon library for UI elements
- **Custom CSS Animations**: Plant growth effects and interactive elements

### Backend
- **Python**: Core application logic
- **Flask**: Web framework for routing and request handling
- **SQLite**: Database for storing soil data, user information, and recommendations
- **SQLAlchemy**: ORM for database interactions

### APIs & Services
- **Agrimetrics API**: Agricultural data integration
- **IoT Service**: Integration with soil sensors and monitoring devices
- **Weather API**: Weather forecasting and historical data

### Data Analysis
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computations for soil predictions
- **Machine Learning Models**: Soil quality prediction and recommendation generation

### Development Tools
- **Git**: Version control
- **Flask-SQLAlchemy**: Database ORM
- **Flask-Login**: User authentication
- **Flask-WTF**: Form handling and validation

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/ai-plant.git
   cd ai-plant
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Initialize the database:
   ```
   python init_db.py
   python generate_sample_data.py
   ```

5. Run the application:
   ```
   python app.py
   ```

6. Access the application at `http://localhost:5000`

## Project Structure

```
ai-plant/
├── app/
│   ├── routes/           # Route handlers
│   ├── services/         # Business logic and API integrations
│   ├── static/           # Static assets (CSS, JS, images)
│   ├── templates/        # HTML templates
│   └── __init__.py       # Application factory
├── instance/             # Database and instance-specific files
├── readme_images/        # Images for documentation
├── app.py                # Application entry point
├── init_db.py            # Database initialization script
├── generate_sample_data.py # Sample data generation
└── requirements.txt      # Project dependencies
```

## Future Enhancements

- Mobile application for on-field monitoring
- Integration with drone imagery for crop health analysis
- Advanced predictive analytics for crop yield forecasting
- Blockchain integration for supply chain transparency
- Community features for knowledge sharing among farmers

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Soil science data provided by agricultural research institutions
- Weather data from meteorological services
- IoT sensor manufacturers for hardware integration 
