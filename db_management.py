from application import app
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import sha256_crypt
from functools import wraps

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
    room = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    requested_days = db.relationship('Day', secondary=books, lazy='subquery',
        backref=db.backref('requested_by', lazy=True))

    accepted_days = db.relationship('Day', secondary=accepted, lazy='subquery', backref=db.backref('accepted_candidates', lazy=True))

    def __repr__(self):
        return f'{self.name} {self.surname}'


class Day(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'{self.day}.{self.month}.{self.year}'



class DatabaseManager():
    def __init__(self, app, db, user_obj, day_obj):
        self.app = app
        self.db = db
        self.User = user_obj
        self.Day = day_obj

    class UserAlreadyExistsError(BaseException):
        def __init__(self, message):
            super().__init__(message)

    class UserDoesNotExistError(BaseException):
        def __init__(self, message):
            super().__init__(message)
    
    def _user_exists(self, email):
        searched_user = self.User.query.filter_by(email=email).first()
        if not searched_user:
            raise self.UserDoesNotExistError('User with this email does not exist')
        return searched_user

    def _not_user_exists(self, email):
        searched_user = self.User.query.filter_by(email=email).first()
        if searched_user:
            raise self.UserAlreadyExistsError(f'User with this email already exists: {searched_user}')

    def _password_encrypt(self, password):
        return sha256_crypt.encrypt(password)

    def _password_verify(self, user, password):
        return sha256_crypt.verify(password, user.password)

    def user_registration(self, name, surname, email, password, room):
        self._not_user_exists(email)
        encrypted_password = self._password_encrypt(password)
        new_user = self.User(name=name, surname=surname, email=email, password=encrypted_password, room=room)
        self.db.session.add(new_user)
        self.db.session.commit()

    def user_sign_in(self, email, password):
        searched_user = self._user_exists(email)
        return self._password_verify(searched_user, password)

    def get_user(self, email):
        return self._user_exists(email)

    def get_day(self, date, create_if_none=False):
        parsed_date = [int(date_element) for date_element in date.split('.')]
        searched_day = self.Day.query.filter_by(day=parsed_date[0], month=parsed_date[1], year=parsed_date[2]).first()
        if create_if_none and not searched_day:
            self.db.session.add(Day(day=parsed_date[0], month=parsed_date[1], year=parsed_date[2]))
            self.db.session.commit()
        return searched_day
    