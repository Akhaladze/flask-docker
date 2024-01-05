from flask_sqlalchemy import SQLAlchemy
from flask import Flask, current_app

app = current_app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Devices(db.Model):
    __tablename__ = 'devices'
    device_id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    type = db.Column(db.String)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)


class IoTEvents(db.Model):
    __tablename__ = 'iot_events'
    event_id = db.Column(db.String, primary_key=True)
    device_id = db.Column(db.String)
    status = db.Column(db.String)
    created_at = db.Column(db.DateTime)

class DeviceStatuses(db.Model):
    __tablename__ = 'device_statuses'
    device_id = db.Column(db.String, primary_key=True)
    status = db.Column(db.String)
    data = db.Column(db.String)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    
class Command(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device = db.Column(db.String())
    type = db.Column(db.String())
    timestamp = db.Column(db.DateTime)
    data = db.Column(db.String())
    status = db.Column(db.String())
    
with app.app_context():
    db.create_all()