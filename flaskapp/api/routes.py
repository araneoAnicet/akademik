from flask import Blueprint, request, Response, jsonify
from flaskapp.models import db, User, Day, Profilechange

mod = Blueprint('api', __name__, url_prefix='/api')

def response_format(
    message='OK',
    status=200,
    data=None,
    ):
    return jsonify({
        'message': message,
        'status': status,
        'data': data,
        'request_payload': {
            'url': str(request.url),
            'method': str(request.method),
            'headers': dict(request.headers)
        }
    }), status


@mod.route('/get_users', methods=['GET'])
def get_users():
    return response_format(data={
        'users': [
            {
                'name': user.name,
                'surname': user.surname,
                'room': user.room
            }
        ] for user in User.query.all()
    })