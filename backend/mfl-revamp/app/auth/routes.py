from . import auth
from .. import db
from ..models.user import User
from ..responses import success_response, error_response
from ..email import send_welcome_email, _send_reset_password_email

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
        return error_response(400, 'User with that email already exists')
    elif User.query.filter_by(username=args['username']).first():
        return error_response(400, 'User with that username already exists')

    user = User(email=args['email'], username=args['username'])
    user.set_password(password=args['password'])
    db.session.add(user)
    db.session.commit()

    send_welcome_email(recipient=args['email'], username=user.username, token=user.generate_confirm_token())
    return success_response()


@auth.route('/verifyaccount', methods=['POST'])
@use_args(request_args.verify_account_args, locations=('json',))
def verify_account(args):
    user = User.verify_confirmation_token(args['verify_token'])
    if user:
        user.verified = True
        db.session.add(user)
        db.session.commit()
        return success_response()
    else:
        return error_response(400, 'Invalid token')


@auth.route('/setnewpassword', methods=['POST'])
@use_args(request_args.new_password_args, locations=('json',))
def set_new_password(args):
    user = User.verify_reset_password_token(args['reset_token'])
    if user:
        user.set_password(args['password'])
        db.session.add(user)
        db.session.commit()
        return success_response()
    return error_response(400, 'Invalid token')


# Always returns successful
@auth.route('/requestnewpassword', methods=['POST'])
@use_args(request_args.request_password_args, locations=('json',))
def request_new_password(args):
    user = User.query.filter_by(email=args['email']).first()
    if user:
        _send_reset_password_email(recipient=args['email'], username=user.username, token=user.generate_reset_password_token())
    return success_response()


@auth.route('/protected', methods=['POST'])
@jwt_required
def protected():
    current_user = get_jwt_identity()
    return str(current_user)
