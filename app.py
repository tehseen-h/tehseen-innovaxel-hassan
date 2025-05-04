from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Setup database (SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
