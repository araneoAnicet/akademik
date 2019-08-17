from flask import render_template, redirect, flash, url_for, request
from db_management import app, DatabaseManager, db, User, Day
from forms_management import LoginBoxForm, ChangePasswordForm, ForgotPasswordForm, RegistrationBoxForm
from calendar import current_month_days, get_today

dm = DatabaseManager(app, db, User, Day)

@app.route('/<requested_month>', methods=['GET'])
def index(requested_month=None):
    if requested_month:
        pass

    return render_template('index.html')


@app.route('/oups')
def not_signed_in():
    return render_template('not_signed_in.html')


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationBoxForm()

    if form.validate_on_submit():
        print('\n\nEntered submit button\n\n')
        try:
            dm.user_registration(
                form.data['name'],
                form.data['surname'],
                form.data['email'],
                form.data['password']
                )
            return redirect(url_for('index'))
        except:
            flash('Sorry, user with such an e-mail already exists.')
            flash('Please, try again')
            return redirect(url_for('registration'))
    return render_template('registration.html', form=form)


@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    form = LoginBoxForm()

    if form.validate_on_submit():
        try:
            if dm.user_sign_in(form.data['email'], form.data['password']):
                return redirect(url_for('index'))
            flash('Incorrect e-mail or password')
            return redirect(url_for('sign_in'))
        except:
            flash('Incorrect e-mail or password')
            return redirect(url_for('sign_in'))
    return render_template('sign_in.html', form=form)


@app.route('/change_password')
def change_password():
    form = LoginBoxForm()

    if form.validate_on_submit():
        print('Gocha!')
    return render_template('change_password.html', form=form)


@app.route('/admin')
def admin():
    return render_template('admin.html')