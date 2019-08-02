from flask import render_template
from db_management import app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/oups')
def not_signed_in():
    return render_template('not_signed_in.html')

@app.route('/registration')
def registration():
    return render_template('registration.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')