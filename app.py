from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Setup database (SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from datetime import datetime

# Create URL model
class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(500), nullable=False)
    short_code = db.Column(db.String(10), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    access_count = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"<URL {self.short_code}>"

@app.route('/')
def home():
    return 'Database is set up and running!'

import string, random

# Function to create a random short code
def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits  # a-zA-Z0-9
    return ''.join(random.choices(characters, k=length))


from flask import request, jsonify

# API to shorten a long URL
@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()  # Get the JSON body
    original_url = data.get('original_url')  # Get "original_url" from JSON

    if not original_url:
        return jsonify({'error': 'original_url is required'}), 400

    short_code = generate_short_code()
    
    # Check if short_code already exists. If it does, generate again.
    while URL.query.filter_by(short_code=short_code).first() is not None:
        short_code = generate_short_code()

    # Save to database
    new_url = URL(original_url=original_url, short_code=short_code)
    db.session.add(new_url)
    db.session.commit()

    return jsonify({
        'original_url': original_url,
        'short_code': short_code
    }), 201

