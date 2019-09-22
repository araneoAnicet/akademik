from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, BooleanField
from wtforms.validators import Email, Length, DataRequired, EqualTo, NumberRange

class RegistrationBoxForm(FlaskForm):
    name = StringField('name', validators=[
        Length(min=2, max=40, message='Your name is too short or too long!'),
        DataRequired(message='This field is required!')
        ])
    surname = StringField('surname', validators=[
        Length(min=2, max=60, message='Your surname is too short or too long!'),
        DataRequired(message='This field is required!')
        ])
    email = StringField('email', validators=[
        Email(message='Does not look like an e-mail!'),
        Length(min=4, max=30, message='Your e-mail is too short or too long!'),
        DataRequired(message='This field is required!')
        ])
    password = PasswordField('password', validators=[
        Length(min=8, max=30, message='Your password is too short or too long!'),
        DataRequired(message='This field is required!')
        ])
    confirm_password = PasswordField('confirm_password', validators=[
        EqualTo('password', message='fields should be equal'), DataRequired()
        ])
    room = IntegerField('room', validators=[
        DataRequired(message='This field is required!'),
        NumberRange(min=1, max=9999, message='Your room number is too big or too small!')])

class LoginBoxForm(FlaskForm):
    email = StringField('email', validators=[
        DataRequired(message='This field is required!'),
        Email(message='Does not look like an e-mail!'),
        Length(min=4, max=30, message='Your e-mail is too short or too long!')
        ])
    password = PasswordField('password', validators=[
        DataRequired(message='This field is required!'),
        Length(min=8, max=30, message='Your password is too short or too long!')
        ])

class ForgotPasswordForm(FlaskForm):
    email = StringField('email', validators=[
        DataRequired(message='This field is required!'),
        Email(),
        Length(min=4, max=30)
        ])

class ChangePasswordForm(FlaskForm):
    email = StringField('email', validators=[
        DataRequired(message='This field is required!'),
        Email()])
    old_password = PasswordField('password', validators=[
        DataRequired(message='This field is required!'),
        Length(min=8)])
    new_password = PasswordField('new_password', validators=[
        DataRequired(message='This field is required!'),
        Length(min=8)])
    confirm_new_password = PasswordField('confirm_password', validators=[
        DataRequired(message='This field is required!'),
        EqualTo('new_password'),
        Length(min=8)])

class AdminForm(FlaskForm):
    email = StringField('email', validators=[
    DataRequired(message='This field is required!'),
    Email(message='Does not look like an e-mail!'),
    Length(min=4, max=30, message='Your e-mail is too short or too long!')
    ])
    password = PasswordField('password', validators=[
        DataRequired(message='This field is required!'),
        Length(min=8, max=30, message='Your password is too short or too long!')
        ])

class ProfileSettingsForm(FlaskForm):
    name = StringField('name', validators=[Length(min=2, max=40)])
    surname = StringField('surname', validators=[Length(min=2, max=60)])
    room = IntegerField('room', validators=[NumberRange(min=1, max=9999)])

class SecretKeyForm(FlaskForm):
    email = StringField('email', validators=[
        DataRequired(message='This field is required!'),
        Email(message='Does not look like an e-mail!'),
        Length(min=4, max=30, message='This e-mail is too short or too long!')
    ])
    password = PasswordField('password', validators=[
        Length(min=8, max=30, message='Your password is too short or too long!')
    ])
    control_key = PasswordField('key', validators=[
        DataRequired(message="Don't you think you can not to fill this out?")
    ])
    isDeletingAdmin = BooleanField('isDeletingAdmin')