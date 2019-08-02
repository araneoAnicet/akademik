from application import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    surname = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=True)
    password = db.Column(db.String(40), nullable=False)

    def _repr_(self):
        return f'{self.name} {self.surname}'

class Day(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    candidates = db.relationship('User', backref='requested_by', lazy='joined')
    booked_by = db.relationship('User', backref='bookers', lazy='joined')

    def _repr_(self):
        return f'{self.day}.{self.month}.{self.year}'