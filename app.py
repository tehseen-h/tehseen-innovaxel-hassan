from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Setup database (SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

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

from flask import request, jsonify
import string, random

# Function to create a random short code
def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits  # a-zA-Z0-9
    return ''.join(random.choices(characters, k=length))

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

from flask import redirect

@app.route('/<string:short_code>', methods=['GET'])
def redirect_to_original(short_code):
    # Search for short code in the database
    url_entry = URL.query.filter_by(short_code=short_code).first()

    if url_entry:
        # Increase access count
        url_entry.access_count += 1
        db.session.commit()
        return redirect(url_entry.original_url)
    else:
        return jsonify({'error': 'Short URL not found'}), 404

@app.route('/info/<string:short_code>', methods=['GET'])
def get_url_info(short_code):
    url_entry = URL.query.filter_by(short_code=short_code).first()

    if url_entry:
        return jsonify({
            'original_url': url_entry.original_url,
            'short_code': url_entry.short_code,
            'created_at': url_entry.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': url_entry.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            'access_count': url_entry.access_count
        }), 200
    else:
        return jsonify({'error': 'Short URL not found'}), 404
@app.route('/update/<string:short_code>', methods=['PUT'])
def update_url(short_code):
    url_entry = URL.query.filter_by(short_code=short_code).first()

    if url_entry:
        data = request.get_json()
        new_url = data.get('original_url')

        if not new_url:
            return jsonify({'error': 'New URL is required'}), 400

        url_entry.original_url = new_url
        url_entry.updated_at = datetime.utcnow()
        db.session.commit()

        return jsonify({'message': 'URL updated successfully'}), 200
    else:
        return jsonify({'error': 'Short URL not found'}), 404
    
@app.route('/delete/<string:short_code>', methods=['DELETE'])
def delete_url(short_code):
    url_entry = URL.query.filter_by(short_code=short_code).first()

    if url_entry:
        db.session.delete(url_entry)
        db.session.commit()
        return jsonify({'message': 'Short URL deleted successfully'}), 200
    else:
        return jsonify({'error': 'Short URL not found'}), 404


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Creates the table(s)
    app.run(debug=True)


