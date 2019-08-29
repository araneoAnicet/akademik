from flask import render_template, redirect, flash, url_for, request, Blueprint
from flaskapp import db
from flaskapp.models import DatabaseManager, User, Day, Profilechange
from flaskapp.site.forms import LoginBoxForm, ChangePasswordForm, ForgotPasswordForm, RegistrationBoxForm


mod = Blueprint('site', __name__)


dm = DatabaseManager(db, User, Day, Profilechange)

@mod.route('/debug', methods=['GET'])
# testing route!
def debug():
    new_user = User(name='Adolf', surname='Hitler', room=666, email='nazi@demo.com', password='fucktheworld')
    db.session.add(new_user)
    db.session.commit()
    return render_template('debug.html', users=User)

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
        print('\n\nEntered submit button\n\n')
        try:
            dm.user_registration(
                form.data['name'],
                form.data['surname'],
                form.data['email'],
                form.data['password'],
                form.data['room']
                )
            return redirect(url_for('site.index'))
        except:
            flash('Sorry, user with such an e-mail already exists.')
            flash('Please, try again')
            return redirect(url_for('site.registration'))
    return render_template('registration.html', form=form)


@mod.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    form = LoginBoxForm()

    if form.validate_on_submit():
        try:
            if dm.user_sign_in(form.data['email'], form.data['password']):
                return redirect(url_for('site.index'))
            flash('Incorrect e-mail or password')
            return redirect(url_for('site.sign_in'))
        except:
            flash('Incorrect e-mail or password')
            return redirect(url_for('site.sign_in'))
    return render_template('sign_in.html', form=form)


@mod.route('/change_password')
def change_password():
    form = LoginBoxForm()

    if form.validate_on_submit():
        print('Gocha!')
    return render_template('change_password.html', form=form)


@mod.route('/admin')
def admin():
    return render_template('admin.html')