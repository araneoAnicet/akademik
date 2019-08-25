from flask import Blueprint
from flaskapp.models import User, Day

mod = Blueprint('api', __name__, url_prefix='/api')