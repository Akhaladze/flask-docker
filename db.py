from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    type = db.Column(db.String(255), unique=False, nullable=False)
    status = db.Column(db.String(255), unique=False, nullable=False)
    last_seen = db.Column(db.DateTime, unique=False, nullable=False)
    last_updated = db.Column(db.DateTime, unique=False, nullable=False)
    last_command = db.Column(db.String(255), unique=False, nullable=False)
    last_command_status = db.Column(db.String(255), unique=False, nullable=False)
    last_command_timestamp = db.Column(db.DateTime, unique=False, nullable=False)

    def __repr__(self):
        return '<Device %r>' % self.name
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device = db.Column(db.String(255), unique=False, nullable=False)
    type = db.Column(db.String(255), unique=False, nullable=False)
    timestamp = db.Column(db.DateTime, unique=False, nullable=False)
    data = db.Column(db.String(255), unique=False, nullable=False)
   

    def __repr__(self):
        return '<Event %r>' % self.device
    
class Command(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device = db.Column(db.String(255), unique=False, nullable=False)
    type = db.Column(db.String(255), unique=False, nullable=False)
    timestamp = db.Column(db.DateTime, unique=False, nullable=False)
    data = db.Column(db.String(255), unique=False, nullable=False)
   

    def __repr__(self):
        return '<Command %r>' % self.device
    
with app.app_context():
    db.create_all()