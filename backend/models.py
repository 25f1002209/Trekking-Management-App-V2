from flask_sqlalchemy import SQLAlchemy
db=SQLAlchemy()
from sqlalchemy.orm import relationship, joinedload
from sqlalchemy import text
from datetime import date

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email=db.Column(db.String(100), nullable=False)

class Trek(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.String(50), nullable=False)
    difficulty_level = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
    photo = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(20), nullable=False, default='active')  # active or closed
    available_slots = db.Column(db.Integer, nullable=False)
    
class Staff(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    experience = db.Column(db.String(200), nullable=True)
    specialization = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(20), nullable=False, default='active')  # active or blacklisted
    assigned_trek = db.Column(db.Integer, db.ForeignKey(Trek.id), nullable=True)

class Trekker(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    trekker_id = db.Column(db.Integer, db.ForeignKey(Trekker.id), nullable=False)
    trek_id = db.Column(db.Integer, db.ForeignKey(Trek.id), nullable=False)
    booking_date = db.Column(db.Date, nullable=False, default=date.today)
    payment_status = db.Column(db.String(20), nullable=False, default='pending')  # pending, completed, failed
    status = db.Column(db.String(20), nullable=False, default='pending')  # pending, confirmed, cancelled