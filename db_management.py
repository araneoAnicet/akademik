from application import app
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import sha256_crypt

db = SQLAlchemy(app)

books = db.Table('books',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('day_id', db.Integer, db.ForeignKey('day.id'), primary_key=True)
)


accepted = db.Table('accepted',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('day_id', db.Integer, db.ForeignKey('day.id'), primary_key=True)
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    surname = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    requested_days = db.relationship('Day', secondary=books, lazy='subquery',
        backref=db.backref('requested_by', lazy=True))

    accepted_days = db.relationship('Day', secondary=accepted, lazy='subquery', backref=db.backref('accepted_candidates', lazy=True))

    def __repr__(self):
        return f'{self.name} {self.surname}'

class Day(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    week_day = db.Column(db.String(3), nullable=False)
    day = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'{self.day}.{self.month}.{self.year}'


def user_check(email):
    searched_user = User.query.filter_by(email=email).first()
    return True if searched_user else False

def password_encrypt(password):
    return sha256_crypt.encrypt(password)

def password_verify(user, password):
    return sha256_crypt.verify(password, user.password)
