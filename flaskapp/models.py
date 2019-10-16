from flask_sqlalchemy import SQLAlchemy
from passlib.hash import sha256_crypt
from flaskapp import db

books = db.Table('books',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('day_id', db.Integer, db.ForeignKey('day.id'), primary_key=True)
)


accepted = db.Table('accepted',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('day_id', db.Integer, db.ForeignKey('day.id'), primary_key=True)
)

change_requests = db.Table('change_requests',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('profilechange_id', db.Integer, db.ForeignKey('profilechange.id'), primary_key=True)
)

class Profilechange(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    surname = db.Column(db.String(60), nullable=False)
    room = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'{self.name} {self.surname}: {self.room} ({self.email})'

class User(db.Model):
    is_admin = db.Column(db.Boolean, default=False, nullable=True)
    is_registered = db.Column(db.Boolean, default=False, nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    surname = db.Column(db.String(60), nullable=False)
    room = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    requested_changes = db.relationship('Profilechange', secondary=change_requests, lazy='subquery',
        backref=db.backref('requested_by', lazy=True))

    requested_days = db.relationship('Day', secondary=books, lazy='subquery',
        backref=db.backref('requested_by', lazy=True))

    accepted_days = db.relationship('Day', secondary=accepted, lazy='subquery',
        backref=db.backref('accepted_candidates', lazy=True))

    def __repr__(self):
        return f'{self.name} {self.surname}'


class Day(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'{self.day}.{self.month}.{self.year}'


# custom errors

class UserAlreadyExistsError(BaseException):
    def __init__(self, message):
        super().__init__(message)

class UserDoesNotExistError(BaseException):
    def __init__(self, message):
        super().__init__(message)

class UserAcceptedRegistrationError(BaseException):
    def __init__(self, message):
        super().__init__(message)

class UserRejectedRegistrationError(BaseException):
    def __init__(self, message):
        super().__init__(message)

class ProfilechangeDoesNotExistError(BaseException):
    def __init__(self, message):
        super().__init__(message)

db_errors = {
    'USER_ALREADY_EXISTS': UserAlreadyExistsError,
    'USER_DOES_NOT_EXIST': UserDoesNotExistError,
    'USER_REGISTRATION_REJECTED': UserAcceptedRegistrationError,
    'USER_REGISTRATION_ACCEPTED': UserRejectedRegistrationError,
    'PROFILECHANGE_DOES_NOT_EXIST': ProfilechangeDoesNotExistError
}

# =================

class DatabaseManager():
    def __init__(self, db, user_obj, day_obj, profilechange_obj):
        self.db = db
        self.User = user_obj
        self.Day = day_obj
        self.Profilechange = profilechange_obj
    
    # validator
    def _user_exists(self, email):
        # raises an error if does not exist
        searched_user = self.User.query.filter_by(email=email).first()
        if not searched_user:
            raise UserDoesNotExistError('User with this email does not exist')
        return searched_user

    # validator
    def _not_user_exists(self, email):
        # raises an error if user exists
        searched_user = self.User.query.filter_by(email=email).first()
        if searched_user:
            raise UserAlreadyExistsError(f'User with this email already exists: {searched_user}')

    # validator
    def _user_registration_request_accepted(self, email):
        # raises an error if user registration request has been accepted
        user = self._user_exists(email)
        if user.is_registered:
            raise UserRejectedRegistrationError('User with this e-mail has been accepted')
        return user

    # validator
    def _not_user_registration_request_accepted(self, email):
        # raises an error if user registration request has been rejected
        user = self._user_exists(email)
        if not user.is_registered:
            raise UserAcceptedRegistrationError('User with this e-mail is not accepted')
        return user

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
    
    def admin_registration(self, email, password):
        self._not_user_exists(email)
        encrypted_password = self._password_encrypt(password)
        new_user = self.User(name='None', surname='None', email=email, password=encrypted_password, room=0)
        new_user.is_admin = True
        self.db.session.add(new_user)
        self.db.session.commit()

    def get_admins(self):
        return self.User.query.filter_by(is_admin=True).all()

    def user_sign_in(self, email, password):
        searched_user = self._not_user_registration_request_accepted(email)
        return self._password_verify(searched_user, password)

    def get_user(self, email):
        return self._user_exists(email)
    
    def remove_user(self, email):
        if self._user_exists(email):
            self.db.session.delete(self.User.query.filter_by(email=email).first())
            self.db.session.commit()
        return True

    def make_admin(self, email):
        user = self._not_user_registration_request_accepted(email)
        user.is_admin = True
        self.db.session.commit()

    def get_unregistered_users(self):
        return self.User.query.filter_by(is_registered=False).all()
    
    def get_profilechanges(self):
        return self.Profilechange.query.all()

    def add_profilechange(self, user_email, change_obj):
        change_copy = change_obj.copy()
        self.db.session.add(change_copy)
        self.get_user(user_email).requested_changes.append(change_copy)
        self.db.session.commit()

    def get_day(self, date, create_if_none=False):
        parsed_date = [int(date_element) for date_element in date.split('.')]
        searched_day = self.Day.query.filter_by(day=parsed_date[0], month=parsed_date[1], year=parsed_date[2]).first()
        if create_if_none and not searched_day:
            self.db.session.add(Day(day=parsed_date[0], month=parsed_date[1], year=parsed_date[2]))
            self.db.session.commit()
        return searched_day
