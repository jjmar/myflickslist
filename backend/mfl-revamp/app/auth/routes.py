from . import auth
from .. import db
from ..models.user import User
from ..responses import success_response, error_response
import request_args

from sqlalchemy.exc import IntegrityError
from webargs.flaskparser import use_args
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity


@auth.route('/login', methods=['POST'])
@use_args(request_args.login_args, locations=('json',))
def login(args):
    user = User.query.filter_by(email=args['email']).first()
    if user and user.verify_password(args['password']):
        token = create_access_token(identity=args['email'])
        return success_response(token=token)
    return error_response(403, "Invalid credentials")


@auth.route('/register', methods=['POST'])
@use_args(request_args.register_args, locations=('json',))
def register(args):
    user = User(email=args['email'], username=args['username'])
    user.set_password(password=args['password'])
    db.session.add(user)

    try:
        db.session.commit()
    except IntegrityError, e:
        return error_response(409, e.orig.diag.message_detail)
    return success_response()


@auth.route('/protected', methods=['POST'])
@jwt_required
def protected():
    current_user = get_jwt_identity()
    return current_user
