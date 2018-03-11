from api import db
from api.services.auth import auth
from api.email import send_welcome_email
from api.models.user import User
from api.responses import success_response, error_response
from api.services.auth import request_args

from flask_jwt_extended import create_access_token
from webargs.flaskparser import use_args


@auth.route('/login', methods=['POST'])
@use_args(request_args.login_args, locations=('json',))
def login(args):
    user = User.query.filter_by(email=args['email']).first()
    if user and user.verify_password(args['password']):
        token = create_access_token(identity=user.id)

        response = {
            'token': token,
            'verified': user.verified
        }

        return success_response(**response)

    return error_response(403, 'Invalid credentials')


@auth.route('/register', methods=['POST'])
@use_args(request_args.register_args, locations=('json',))
def register(args):

    if User.query.filter_by(email=args['email']).first():
        return error_response(400, 'User with that email already exists')
    elif User.query.filter_by(username=args['username']).first():
        return error_response(400, 'User with that username already exists')

    user = User(email=args['email'], username=args['username'])
    user.set_password(password=args['password'])
    db.session.add(user)
    db.session.commit()

    send_welcome_email(recipient=args['email'], username=user.username, token=user.generate_confirm_token())
    return success_response()
