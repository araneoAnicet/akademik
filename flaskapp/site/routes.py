from flask import render_template, redirect, flash, url_for, request, Blueprint
from flaskapp import db
from flaskapp.config import flash_categories
from flaskapp.models import DatabaseManager, User, Day, Profilechange, db_errors
from flaskapp.site.forms import LoginBoxForm, ChangePasswordForm, ForgotPasswordForm, RegistrationBoxForm


mod = Blueprint('site', __name__)


dm = DatabaseManager(db, User, Day, Profilechange)

@mod.route('/debug', methods=['GET'])
# testing route!
def debug():
    # drops the data
    db.drop_all()
    db.create_all()
    return render_template('debug.html', message='The database has been cleaned successfully!')

@mod.route('/', methods=['GET'])
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
    return render_template('admin.html')