from flask import render_template
from db_management import app
from forms_management import LoginBoxForm, ChangePasswordForm, ForgotPasswordForm 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/oups')
def not_signed_in():
    return render_template('not_signed_in.html')

@app.route('/registration')
def registration():
    form = LoginBoxForm()

    if form.validate_on_submit():
        print('Gocha!')
    return render_template('registration.html', form=form)

@app.route('/sign_in')
def sign_in():
    form = LoginBoxForm()

    if form.validate_on_submit():
        print('Gocha!')
    return render_template('sign_in.html', form=form)

@app.route('/admin')
def admin():
    return render_template('admin.html')