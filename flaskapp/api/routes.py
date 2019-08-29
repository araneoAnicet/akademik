from flask import Blueprint, request, Response, jsonify
from flaskapp import db
from flaskapp.models import DatabaseManager, User, Day, Profilechange

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