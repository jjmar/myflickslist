from . import profile
from ..models.user import User
from request_args import add_remove_friend_args
from ..responses import success_response, error_response

from webargs.flaskparser import use_args
from flask_jwt_extended import get_jwt_identity, jwt_required


@profile.route('/addfriend', methods=['POST'])
@use_args(add_remove_friend_args, locations=('json',))
@jwt_required
def add_friend(args):
    user_id = get_jwt_identity()
    friendee_id = args['user_id']

    user = User.query.get(user_id)
    friendee = User.query.get(friendee_id)

    if not user:
        return error_response(400, "User does not exist")
    elif not friendee:
        return error_response(400, "Friend does not exist")

    if user is friendee:
        return error_response(400, "Cannot add self as friend")
    elif friendee in user.friends:
        return error_response(400, "Friendship already exists")

    user.add_friend(friendee)
    return success_response()


@profile.route('/removefriend', methods=['POST'])
@use_args(add_remove_friend_args, locations=('json',))
@jwt_required
def remove_friend(args):
    user_id = get_jwt_identity()
    friendee_id = args['user_id']

    user = User.query.get(user_id)
    friendee = User.query.get(friendee_id)

    if not user:
        return error_response(400, "User does not exist")
    elif not friendee:
        return error_response(400, "Friend does not exist")

    if friendee not in user.friends:
        return error_response(400, "Friendship doesn't exist")

    user.remove_friend(friendee)
    return success_response()
