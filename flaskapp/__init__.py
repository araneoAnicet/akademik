from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
db = SQLAlchemy()

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'APP_SECRET_KEY'

db.init_app(app)

from flaskapp.site.routes import mod as site_mod
from flaskapp.api.routes import mod as api_mod

app.register_blueprint(site_mod)
app.register_blueprint(api_mod)
