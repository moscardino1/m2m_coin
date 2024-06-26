#model.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
import uuid
from sqlalchemy import func
from datetime import datetime
 


db = SQLAlchemy()
login_manager = LoginManager()




class CentralBank(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    coins = db.Column(db.Float)


class Participant(UserMixin, db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(50))
    coins = db.Column(db.Float)
    password = db.Column(db.String(255))
    profile_picture_url = db.Column(db.String(1000))
    is_active = db.Column(db.Boolean, default=True)
    insert_timestamp = db.Column(db.DateTime, default=datetime.utcnow)  # Insert timestamp
    update_timestamp = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Update timestamp

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    sender_id = db.Column(db.String(36), db.ForeignKey('participant.id'))
    receiver_id = db.Column(db.String(36), db.ForeignKey('participant.id'))
    amount = db.Column(db.Float)  # Add this line to define the amount attribute
    subject = db.Column(db.String(200))

    sender = db.relationship('Participant', foreign_keys=[sender_id], backref='sent_transactions')
    receiver = db.relationship('Participant', foreign_keys=[receiver_id], backref='received_transactions')

@login_manager.user_loader
def load_user(user_id):
    return Participant.query.get((user_id))

