from . import auth
from .. import db
from ..models.user import User
from ..responses import success_response, error_response
from ..email import send_welcome_email

import request_args

from webargs.flaskparser import use_args
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity


@auth.route('/login', methods=['POST'])
@use_args(request_args.login_args, locations=('json',))
def login(args):
    user = User.query.filter_by(email=args['email']).first()
    if user and user.verify_password(args['password']):
        token = create_access_token(identity=user.id)
        return success_response(token=token)
    return error_response(403, "Invalid credentials")


@auth.route('/register', methods=['POST'])
@use_args(request_args.register_args, locations=('json',))
def register(args):

    if User.query.filter_by(email=args['email']).first():
        return error_response('User with that email already exists')
    elif User.query.filter_by(username=args['username']).first():
        return error_response('User with that username already exists')

    user = User(email=args['email'], username=args['username'])
    user.set_password(password=args['password'])
    db.session.add(user)
    db.session.commit()

    send_welcome_email(recipient=args['email'], username=user.username, token=user.generate_confirm_token())
    return success_response()


@auth.route('/verify/<token>', methods=['GET'])
def verify_account(token):
    user = User.verify_confirmation_token(token)
    if user:
        user.verified = True
        db.session.add(user)
        db.session.commit()
        return success_response()
    else:
        return error_response(400, 'Invalid verification token')


@auth.route('/protected', methods=['POST'])
@jwt_required
def protected():
    current_user = get_jwt_identity()
    return str(current_user)
