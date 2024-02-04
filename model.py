from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin

db = SQLAlchemy()
login_manager = LoginManager()


class Participant(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    coins = db.Column(db.Integer)
    password = db.Column(db.String(100))

class CentralBank(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    coins = db.Column(db.Integer)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    sender_id = db.Column(db.Integer, db.ForeignKey('participant.id'))
    receiver_id = db.Column(db.Integer, db.ForeignKey('participant.id'))
    subject = db.Column(db.String(200))

    sender = db.relationship('Participant', foreign_keys=[sender_id])
    receiver = db.relationship('Participant', foreign_keys=[receiver_id])



@login_manager.user_loader
def load_user(user_id):
    return Participant.query.get(int(user_id))
