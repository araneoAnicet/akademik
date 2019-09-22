from flask import render_template, redirect, flash, url_for, request, Blueprint, session, g, current_app
from flaskapp import db
from flaskapp.config import flash_categories
from flaskapp.models import DatabaseManager, User, Day, Profilechange, db_errors
from flaskapp.site.forms import (
    RegistrationBoxForm,
    LoginBoxForm,
    ForgotPasswordForm,
    ChangePasswordForm,
    AdminForm,
    ProfileSettingsForm,
    SecretKeyForm
    )
from functools import wraps


mod = Blueprint('site', __name__)


dm = DatabaseManager(db, User, Day, Profilechange)

def requires_session(func):
    @wraps(func)
    def wrapper(*args, **kwds):
        if not g.email or not g.password:
            return render_template('not_signed_in.html')
        return func(*args, **kwds)
    return wrapper


@mod.before_request
def before_request():
    g.email = None
    g.password = None
    if 'email' in session:
        g.email = session['email']
    if 'password' in session:
        g.password = session['password']


@mod.route('/debug/drop', methods=['GET'])
# testing route!
def debug():
    # drops the data
    if 'email' in session:
        session.pop('email', None)
    if 'password' in session:
        session.pop('password', None)
    db.drop_all()
    db.create_all()
    return render_template('debug.html', message='The database has been cleaned successfully!')

@mod.route('/admins_control', methods=['GET', 'POST'])
def admins_control():
    form = SecretKeyForm()

    if form.validate_on_submit():
        if form.data['key'] == current_app.config['ADMINS_CONTROL_KEY']:
            if form.data['isDeletingAdmin']:
                flash(f"Admin {form.data['email']} has been removed!", flash_categories['success'])
                return redirect(url_for('admins_control'))
            flash(f"New admin {form.data['email']} has been created", flash_categories['success'])
            return redirect(url_for('admins_control'))
    return render_template('admins_control.html', form=form)


@mod.route('/', methods=['GET'])
@requires_session
def index():
    return render_template('index.html')


@mod.route('/oups')
def not_signed_in():
    return render_template('not_signed_in.html')


@mod.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationBoxForm()

    if form.validate_on_submit():
        try:
            dm.user_registration(
                form.data['name'],
                form.data['surname'],
                form.data['email'],
                form.data['password'],
                form.data['room']
                )
            flash('Your registration request has been sent successfully!' +
                'Please wait until administrator accepts your form...', flash_categories['success'])
            return redirect(url_for('site.registration'))
        except db_errors['USER_ALREADY_EXISTS']:
            flash('Sorry, user with such an e-mail already exists. Please, try again', flash_categories['error'])
            return redirect(url_for('site.registration'))
    return render_template('registration.html', form=form)


@mod.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    form = LoginBoxForm()

    if form.validate_on_submit():
        try:
            if dm.user_sign_in(form.data['email'], form.data['password']):
                session['email'] = form.data['email']
                session['password'] = form.data['password']
                return redirect(url_for('site.index'))
            flash('Incorrect e-mail or password', flash_categories['error'])
            return redirect(url_for('site.sign_in'))
        except (db_errors['USER_REGISTRATION_REJECTED'], db_errors['USER_DOES_NOT_EXIST']):
            flash('Incorrect e-mail or password', flash_categories['error'])
            return redirect(url_for('site.sign_in'))
    return render_template('sign_in.html', form=form)


@mod.route('/change_password')
def change_password():
    form = ForgotPasswordForm()

    if form.validate_on_submit():
        print('Gocha!')
    return render_template('change_password.html', form=form)


@mod.route('/admin')
def admin():
    form = AdminForm()
    if form.validate_on_submit():
        print('Gotcha!')
    return render_template('admin.html', form=form)