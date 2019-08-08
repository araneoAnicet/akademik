from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Email, Length, DataRequired, EqualTo

class RegistrationBoxForm(FlaskForm):
    name = StringField('Name', validators=[Length(min=2, max=40), DataRequired()])
    surname = StringField('Surname', validators=[Length(min=2, max=60), DataRequired()])
    email = StringField('E-mail', validators=[Email(), Length(min=4, max=30), DataRequired()])
    password = PasswordField('password', validators=[Length(min=8, max=30), DataRequired()])
    confirm_password = PasswordField('confirm_password', validators=[Length(min=8, max=30), EqualTo('password', message='fields should be equal'), DataRequired()])
    submit = SubmitField()

class LoginBoxForm(FlaskForm):
    email = StringField(validators=[DataRequired(), Email(), Length(min=4, max=30)])
    password = PasswordField(validators=[DataRequired(), Length(min=8, max=30)])
    submit = SubmitField()

class ForgotPasswordForm(FlaskForm):
    email = StringField(validators=[DataRequired(), Email(), Length(min=4, max=30)])
    submit = SubmitField()

class ChangePasswordForm(FlaskForm):
    email = StringField(validators=[DataRequired(), Email()])
    old_password = PasswordField(validators=[DataRequired(), Length(min=8)])
    new_password = PasswordField(validators=[DataRequired(), Length(min=8)])
    confirm_new_password = PasswordField(validators=[DataRequired(), EqualTo('new_password'), Length(min=8)])