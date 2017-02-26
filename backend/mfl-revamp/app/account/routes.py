from app.account import request_args, account
from app import db
from app.models.user import User
from app.responses import success_response, error_response
from app.email import send_reset_password_email

from flask_jwt_extended import jwt_required, get_jwt_identity
from webargs.flaskparser import use_args


@account.route('/updateemail', methods=['POST'])
@jwt_required
@use_args(request_args.update_account_email_args, locations=('json',))
def update_account_email(args):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return error_response('User does not exist')

    if not User.query.filter(User.email == args['email']).first():
        user.email = args['email']
        db.session.add(user)
        db.session.commit()
    else:
        return error_response(400, 'User already exists with that email')

    return success_response()


@account.route('/updatepassword', methods=['POST'])
@jwt_required
@use_args(request_args.update_account_password_args, locations=('json',))
def update_account_password(args):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return error_response(400, 'User does not exist')

    user.set_password(args['password'])
    db.session.add(user)
    db.session.commit()
    return success_response()


@account.route('/verifyaccount', methods=['POST'])
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


@account.route('/setnewpassword', methods=['POST'])
@use_args(request_args.set_new_password_args, locations=('json',))
def set_new_password(args):
    user = User.verify_reset_password_token(args['reset_token'])
    if user:
        user.set_password(args['password'])
        db.session.add(user)
        db.session.commit()
        return success_response()
    return error_response(400, 'Invalid token')


@account.route('/requestnewpassword', methods=['POST'])
@use_args(request_args.request_new_password_args, locations=('json',))
def request_new_password(args):
    user = User.query.filter_by(email=args['email']).first()
    if user:
        send_reset_password_email(recipient=args['email'], username=user.username,
                                  token=user.generate_reset_password_token())
    return success_response()
