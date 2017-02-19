from . import auth
from .. import db
from ..models.user import User
from ..responses import success_response

from request_args import register_args
from webargs.flaskparser import use_args


@auth.route('/login', methods=['POST'])
def login():
    return 'login'


@auth.route('/register', methods=['POST'])
@use_args(register_args, locations=('json',))
def register(args):
    user = User(email=args['email'], username=args['username'])
    user.set_password(password=args['password'])
    db.session.add(user)
    db.session.commit()
    return success_response()


@auth.route('/protected', methods=['POST'])
def protected():
    return 'protected'
