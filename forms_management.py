from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Email, Length, DataRequired, EqualTo

class LoginBoxForm(FlaskForm):
    name = StringField(validators=[DataRequired(), Length(min=2, max=40)])
    surname = StringField(validators=[DataRequired(), Length(min=2, max=60)])
    email = StringField(validators=[DataRequired(), Email(), Length(min=4, max=30)])
    password = PasswordField(validators=[DataRequired(), Length(min=8, max=30)])
    confirm_password = PasswordField(validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField()

class ForgotPasswordForm(FlaskForm):
    email = StringField(validators=[DataRequired(), Email(), Length(min=4, max=30)])
    submit = SubmitField()

class ChangePasswordForm(FlaskForm):
    email = StringField(validators=[DataRequired(), Email()])
    old_password = PasswordField(validators=[DataRequired(), Length(min=8)])
    new_password = PasswordField(validators=[DataRequired(), Length(min=8)])
    confirm_new_password = PasswordField(validators=[DataRequired(), EqualTo('new_password'), Length(min=8)])