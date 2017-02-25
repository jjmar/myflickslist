from . import profile
from ..models.user import User, Friendship
from .. import db
import request_args
from ..responses import success_response, error_response

from webargs.flaskparser import use_args
from flask_jwt_extended import get_jwt_identity, jwt_required


# Profile info routes

@profile.route('/updateinfo', methods=['POST'])
@use_args(request_args.set_profile_info_args, locations=('json',))
@jwt_required
def update_profile_info(args):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    user.fav_genre = args['fav_genre']
    user.gender = args['gender']
    user.location = args['location']
    user.website = args['website']
    user.about = args['about']

    db.session.add(user)
    db.session.commit()
    return success_response()


@profile.route('/getinfo', methods=['POST'])
@use_args(request_args.get_profile_info_args)
def get_profile_info(args):
    user = User.query.get(args['user_id'])

    if not user:
        return error_response('User does not exist')

    response = dict()
    response['fav_genre'] = user.fav_genre
    response['gender'] = user.gender
    response['location'] = user.location
    response['website'] = user.website
    response['about'] = user.about
    response['username'] = user.username
    return success_response(results=response)

# Friendship routes


@profile.route('/sendfriendrequest', methods=['POST'])
@use_args(request_args.friend_args, locations=('json',))
@jwt_required
def send_friend_request(args):
    user_id = get_jwt_identity()
    friendee_id = args['user_id']

    user = User.query.get(user_id)
    friendee = User.query.get(friendee_id)

    if not user:
        return error_response(400, "User does not exist")
    elif not friendee:
        return error_response(400, "Friend does not exist")
    elif user_id == friendee_id:
        return error_response(400, "Cannot befriend self")

    to_friendship = db.session.query(Friendship).filter(Friendship.user_id==user_id).filter(Friendship.friend_id==friendee_id).first()

    if to_friendship and not to_friendship.active:
        return error_response(400, "Request already sent")
    elif to_friendship and to_friendship.active:
        return error_response(400, "Friendship already exists")

    from_friendship = db.session.query(Friendship).filter(Friendship.user_id==friendee_id).filter(Friendship.friend_id==user_id).filter(Friendship.active==0).first()

    # They've already sent us an invite, create friendship
    if from_friendship:
        from_friendship.active = 1
        to_friendship = Friendship(user_id=user_id, friend_id=friendee_id, active=1)
        db.session.add(from_friendship)
        db.session.add(to_friendship)
    # Otherwise, send invite
    else:
        invite = Friendship(user_id=user_id, friend_id=friendee_id, active=0)
        db.session.add(invite)
    db.session.commit()
    return success_response()


@profile.route('/acceptfriendrequest', methods=['POST'])
@use_args(request_args.friend_args, locations=('json',))
@jwt_required
def accept_friend_request(args):
    user_id = get_jwt_identity()
    friendee_id = args['user_id']

    user = User.query.get(user_id)
    friendee = User.query.get(friendee_id)

    if not user:
        return error_response(400, "User does not exist")
    elif not friendee:
        return error_response(400, "Friend does not exist")

    from_friendship = db.session.query(Friendship).filter(Friendship.user_id==friendee_id).filter(Friendship.friend_id==user_id).filter(Friendship.active==0).first()

    if not from_friendship:
        return error_response(400, "Friendship request doesn't exist")

    to_friendship = Friendship(user_id=user_id, friend_id=friendee_id, active=1)
    from_friendship.active = 1
    db.session.add(to_friendship)
    db.session.add(from_friendship)
    db.session.commit()
    return success_response()


@profile.route('/rejectfriendrequest', methods=['POST'])
@use_args(request_args.friend_args, locations=('json',))
@jwt_required
def reject_friend_request(args):
    user_id = get_jwt_identity()
    friendee_id = args['user_id']

    user = User.query.get(user_id)
    friendee = User.query.get(friendee_id)

    if not user:
        return error_response(400, "User does not exist")
    elif not friendee:
        return error_response(400, "Friend does not exist")

    from_friendship = db.session.query(Friendship).filter(Friendship.user_id==friendee_id).filter(Friendship.friend_id==user_id).filter(Friendship.active==0).first()

    if not from_friendship:
        return error_response(400, "Friendship request doesn't exist")

    db.session.delete(from_friendship)
    db.session.commit()
    return success_response()


@profile.route('/removefriend', methods=['POST'])
@use_args(request_args.friend_args, locations=('json',))
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

    to_friendship = db.session.query(Friendship).filter(Friendship.user_id==user_id).filter(Friendship.friend_id==friendee_id).filter(Friendship.active==1).first()
    from_friendship = db.session.query(Friendship).filter(Friendship.user_id==friendee_id).filter(Friendship.friend_id==user_id).filter(Friendship.active==1).first()

    if not to_friendship or not from_friendship:
        return error_response(400, "Friendship doesn't exist")

    db.session.delete(to_friendship)
    db.session.delete(from_friendship)
    db.session.commit()
    return success_response()
