import os
import sys
import random
import datetime
import sqlite3
from pathlib import Path

BASEDIR = os.path.abspath(os.path.dirname(__file__))
instance_dir = os.path.join(BASEDIR, 'instance')
os.makedirs(instance_dir, exist_ok=True)
db_path = os.path.join(instance_dir, 'agriculture_assistant.db')

print(f"Using database at: {db_path}")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS soil_analysis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME NOT NULL,
    field_name TEXT NOT NULL,
    pH FLOAT,
    organic_matter FLOAT,
    nitrogen FLOAT,
    phosphorus FLOAT,
    potassium FLOAT,
    calcium FLOAT,
    magnesium FLOAT,
    sulfur FLOAT,
    iron FLOAT,
    manganese FLOAT,
    zinc FLOAT,
    copper FLOAT,
    boron FLOAT,
    molybdenum FLOAT,
    notes TEXT
)
''')

field_names = ['North Field', 'South Field', 'West Field', 'East Field', 'Center Field']
today = datetime.datetime.now()

soil_records = []
for month_offset in range(7):  
    date = today - datetime.timedelta(days=30 * month_offset)
    
    for field in field_names:
        soil_records.append({
            'timestamp': date.strftime('%Y-%m-%d %H:%M:%S'),
            'field_name': field,
            'pH': round(random.uniform(6.0, 7.5), 1),
            'organic_matter': round(random.uniform(2.5, 5.0), 1),
            'nitrogen': round(random.uniform(20, 30) - month_offset * random.uniform(0, 2), 1),
            'phosphorus': round(random.uniform(40, 50) - month_offset * random.uniform(0, 1), 1),
            'potassium': round(random.uniform(170, 190) - month_offset * random.uniform(0, 3), 1),
            'calcium': round(random.uniform(140, 160), 1),
            'magnesium': round(random.uniform(140, 160), 1),
            'sulfur': round(random.uniform(10, 15), 1),
            'iron': round(random.uniform(110, 130), 1),
            'manganese': round(random.uniform(30, 40), 1),
            'zinc': round(random.uniform(1.8, 2.3), 1),
            'copper': round(random.uniform(1.6, 2.0), 1),
            'boron': round(random.uniform(0.7, 0.9), 1),
            'molybdenum': round(random.uniform(0.04, 0.06), 3),
            'notes': f"Sample data for {field} - {date.strftime('%B %Y')}"
        })

for record in soil_records:
    cursor.execute('''
    INSERT INTO soil_analysis (
        timestamp, field_name, pH, organic_matter, 
        nitrogen, phosphorus, potassium, calcium, magnesium, 
        sulfur, iron, manganese, zinc, copper, boron, 
        molybdenum, notes
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        record['timestamp'], record['field_name'], record['pH'], record['organic_matter'],
        record['nitrogen'], record['phosphorus'], record['potassium'], record['calcium'], record['magnesium'],
        record['sulfur'], record['iron'], record['manganese'], record['zinc'], record['copper'], record['boron'],
        record['molybdenum'], record['notes']
    ))

cursor.execute('''
CREATE TABLE IF NOT EXISTS fertilizer_recommendations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    soil_analysis_id INTEGER,
    nutrient TEXT NOT NULL,
    recommendation TEXT NOT NULL,
    amount TEXT NOT NULL,
    FOREIGN KEY (soil_analysis_id) REFERENCES soil_analysis(id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS recommended_products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    soil_analysis_id INTEGER,
    name TEXT NOT NULL,
    dose TEXT NOT NULL,
    note TEXT,
    FOREIGN KEY (soil_analysis_id) REFERENCES soil_analysis(id)
)
''')

latest_records = [rec for rec in soil_records if rec['timestamp'] == soil_records[0]['timestamp']]

for record in latest_records:
    cursor.execute('SELECT id FROM soil_analysis WHERE field_name = ? ORDER BY timestamp DESC LIMIT 1', 
                   (record['field_name'],))
    soil_id = cursor.fetchone()[0]
    
    recommendations = []
    
    if record['nitrogen'] < 30:
        recommendations.append(('Nitrogen (N)', 'Apply nitrogen fertilizer', f"{round(30 - record['nitrogen'])} kg/ha"))
    else:
        recommendations.append(('Nitrogen (N)', 'No additional needed', '0 kg/ha'))
    
    if record['phosphorus'] < 30:
        recommendations.append(('Phosphorus (P)', 'Apply phosphorus fertilizer', f"{round(30 - record['phosphorus'])} kg/ha"))
    else:
        recommendations.append(('Phosphorus (P)', 'No additional needed', '0 kg/ha'))
    
    if record['potassium'] < 200:
        recommendations.append(('Potassium (K)', 'Apply potassium fertilizer', f"{round(200 - record['potassium'])} kg/ha"))
    else:
        recommendations.append(('Potassium (K)', 'No additional needed', '0 kg/ha'))
    
    if record['zinc'] < 3:
        recommendations.append(('Zinc (Zn)', 'Apply zinc sulfate', f"{round((3 - record['zinc']) * 5)} kg/ha"))
    
    if record['manganese'] < 50:
        recommendations.append(('Manganese (Mn)', 'Apply manganese sulfate', f"{round((50 - record['manganese']) / 5)} kg/ha"))
    
    for nutrient, recommendation, amount in recommendations:
        cursor.execute('''
        INSERT INTO fertilizer_recommendations (soil_analysis_id, nutrient, recommendation, amount) 
        VALUES (?, ?, ?, ?)
        ''', (soil_id, nutrient, recommendation, amount))
    
    products = [
        ('Balanced NPK 10-10-10', '300 kg/ha', 'For overall balance'),
        ('Urea (46-0-0)', '65 kg/ha', 'For nitrogen deficiency'),
        ('Zinc Sulfate', '5 kg/ha', 'For zinc deficiency')
    ]
    
    for name, dose, note in products:
        cursor.execute('''
        INSERT INTO recommended_products (soil_analysis_id, name, dose, note)
        VALUES (?, ?, ?, ?)
        ''', (soil_id, name, dose, note))

conn.commit()
conn.close()

print("Sample data has been generated successfully.")
print(f"Created {len(soil_records)} soil analysis records for {len(field_names)} fields over 7 months.")
print(f"Generated fertilizer recommendations and product suggestions for {len(latest_records)} recent records.") 