from flask import Blueprint, request, Response, jsonify, current_app
from flaskapp import db
from flaskapp.models import DatabaseManager, User, Day, Profilechange, db_errors
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError


dm = DatabaseManager(db, User, Day, Profilechange)

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


@mod.route('/get_api_token', methods=['POST', 'GET'])
def get_token():
    email = request.headers['email']
    password = request.headers['password']
    if email and password:
        try:
            user = dm.user_sign_in(email, password)
            if user and user.is_admin:
                return response_format(
                    data={
                        'token': jwt.encode(
                            {
                                'email': email,
                                'is_admin': True,
                                'exp': datetime.utcnow() + current_app.config['JWT_EXPIRATION']
                                },
                                current_app.config['SECRET_KEY'],
                                'HS256'
                            )
                    }
                )
            return response_format(
                message='Incorrect e-mail or password',
                status=401
            )
        except:
            return response_format(
                message='Incorrect e-mail or password',
                status=401
            )
    return response_format(
        message='E-mail or password are missing',
        status=401
        )

@mod.route('/check_token')
def check_token():
    token = request.headers['Authorization']
    if token:
        try:
            jwt.decode(token, current_app.config['SECRET_KEY'])
            return response_format(
                message='Your token is verified successfully!',
                status=200
            )
        except ExpiredSignatureError:
            return response_format(
                message='Expired token',
                status=401
            )
        except InvalidTokenError:
            return response_format(
                message='Invalid token',
                status=401
            )
    return response_format(
        message='Token is missing',
        status=401
    )

@mod.route('/get_unregistered_users', methods=['GET'])
def get_users():
    return response_format(data={
        'users': list(map(
            lambda user: {
                'name': user.name,
                'surname': user.surname,
                'room': user.room,
                'email': user.email
            }, dm.get_unregistered_users()
        ))
    })

@mod.route('/get_admins', methods=['GET'])
def get_admins():
    return response_format(
        message="all admins' e-mails are listed",
        data={
            'admins': [
                admin.email for admin in dm.get_admins()
            ]
        }
    )

@mod.route('/accept_user_registration/<email>', methods=['PUT'])
def accept_registration(email):
    searched_user = dm.get_user(email)
    searched_user.is_registered = True
    db.session.commit()
    return response_format(
        message='The user has been accepted',
        data={
            'user': {
                'name': searched_user.name,
                'surname': searched_user.surname,
                'room': searched_user.room,
                'email': searched_user.email
            }
        }
    )

@mod.route('/get_profilechanges', methods=['GET'])
def get_profilechanges():
    return response_format(
        data={
            list(map(lambda change: 
                {'change': {
                    'user': {
                        'name': change.requested_by[0].name,
                        'surname': change.requested_by[0].surname,
                        'room': change.requested_by[0].room,
                        'email': change.requested_by[0].email
                    },
                    'to_commit': {
                        'name': change.name,
                        'surname': change.surname,
                        'room': change.room,
                    }
                }}, dm.get_profilechanges()
            ))
            
        }
    )

@mod.route('/accept_profilechange/<email>')
def accept_profilechange(email):
    searched_user = dm.get_user(email)
    user_copy = searched_user.copy()
    change = searched_user.requested_changes.first()
    change_copy = change.copy()

    searched_user.name = change.name
    searched_user.surname = change.surname
    searched_user.room = change.room

    db.session.remove(change)
    db.session.commit()
    return response_format(
        message='Changes have been commited',
        data={
            'user_before': {
                'name': user_copy.name,
                'surname': user_copy.surname,
                'room': user_copy.room,
                'email': user_copy.email
            },
            'changes': {
                'name': change_copy.name,
                'surname': change_copy.surname,
                'room': change_copy.room,
                'email': searched_user.email
            }
        }
    )
