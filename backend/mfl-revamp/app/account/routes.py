from . import account
import request_args
from ..responses import success_response, error_response
from .. import db
from ..models.user import User

from flask_jwt_extended import jwt_required, get_jwt_identity
from webargs.flaskparser import use_args
from webargs import missing


@account.route('/updateemail', methods=['POST'])
@jwt_required
@use_args(request_args.account_email_args, locations=('json',))
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
@use_args(request_args.account_password_args, locations=('json',))
def update_account_password(args):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return error_response(400, 'User does not exist')

    user.set_password(args['password'])
    db.session.add(user)
    db.session.commit()
    return success_response()

