from app import db
from app.profile import profile, request_args
from app.models.user import User, Friendship, Comment
from app.models.social import Recommendation, Review
from app.models.movie import Movie
from app.responses import success_response, error_response
from app.util import paginate

from webargs.flaskparser import use_args
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy.orm import aliased


# Profile info routes

@profile.route('/updateinfo', methods=['POST'])
@use_args(request_args.update_profile_info_args, locations=('json',))
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


@profile.route('/info', methods=['POST'])
@use_args(request_args.get_profile_info_args)
def get_profile_info(args):
    user = User.query.get(args['user_id'])

    if not user:
        return error_response(400, 'User does not exist')

    comments = db.session.query(Comment, User)\
                         .join(User, Comment.host_id == User.id)\
                         .filter(Comment.host_id == user.id)\
                         .order_by(Comment.timestamp).limit(5)

    response = {
        'fav_genre': user.fav_genre,
        'gender': user.gender,
        'location': user.location,
        'website': user.website,
        'about': user.about,
        'username': user.username,
        'comments': [{'author': user.username, 'body': comment.body, 'timestamp': comment.timestamp,
                      'author_id': user.id} for comment, user in comments]
    }

    return success_response(**response)

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

    to_friendship = db.session.query(Friendship)\
                              .filter(Friendship.user_id == user_id)\
                              .filter(Friendship.friend_id == friendee_id)\
                              .first()

    if to_friendship and not to_friendship.active:
        return error_response(400, "Request already sent")
    elif to_friendship and to_friendship.active:
        return error_response(400, "Friendship already exists")

    from_friendship = db.session.query(Friendship)\
                                .filter(Friendship.user_id == friendee_id)\
                                .filter(Friendship.friend_id == user_id)\
                                .filter(Friendship.active == 0)\
                                .first()

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

    from_friendship = db.session.query(Friendship)\
                                .filter(Friendship.user_id == friendee_id)\
                                .filter(Friendship.friend_id == user_id)\
                                .filter(Friendship.active == 0).first()

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

    from_friendship = db.session.query(Friendship)\
                                .filter(Friendship.user_id == friendee_id)\
                                .filter(Friendship.friend_id == user_id)\
                                .filter(Friendship.active == 0).first()

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

    to_friendship = db.session.query(Friendship)\
                              .filter(Friendship.user_id == user_id)\
                              .filter(Friendship.friend_id == friendee_id)\
                              .filter(Friendship.active == 1)\
                              .first()

    from_friendship = db.session.query(Friendship)\
                                .filter(Friendship.user_id == friendee_id)\
                                .filter(Friendship.friend_id == user_id)\
                                .filter(Friendship.active == 1)\
                                .first()

    if not to_friendship or not from_friendship:
        return error_response(400, "Friendship doesn't exist")

    db.session.delete(to_friendship)
    db.session.delete(from_friendship)
    db.session.commit()
    return success_response()

# Comments


@profile.route('/postcomment', methods=['POST'])
@use_args(request_args.post_comment_args, locations=('json',))
@jwt_required
def post_comment(args):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return error_response(400, 'User does not exist')

    host = User.query.get(args['host_id'])

    if not host:
        return error_response(400, 'User does not exist')

    comment = Comment(author_id=user_id, host_id=args['host_id'], body=args['body'])
    db.session.add(comment)
    db.session.commit()

    return success_response(comment_id=comment.id)


@profile.route('/removecomment', methods=['POST'])
@use_args(request_args.remove_comment_args, locations=('json',))
@jwt_required
def remove_comment(args):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return error_response(400, 'User does not exist')

    comment_id = args['comment_id']
    comment = Comment.query.filter_by(id=comment_id).filter_by(host_id=user_id).first()

    if not comment:
        return error_response(400, 'Comment does not exist')

    db.session.delete(comment)
    db.session.commit()
    return success_response()


@profile.route('/reviews', methods=['POST'])
@use_args(request_args.get_user_reviews, locations=('json',))
def get_user_reviews(args):
    user = User.query.get(args['user_id'])

    if not user:
        return error_response(400, 'User does not exist')

    query = db.session.query(Review, Movie)\
                      .join(Movie)\
                      .filter(Review.author_id == user.id)\
                      .order_by(Review.timestamp)

    pagination = paginate(query, page=args['page'], per_page=10)

    response = {
        'items': [{'body': review.body, 'timestamp': review.timestamp, 'movie_title': movie.title, 'movie_id': movie.id}
                  for review, movie in pagination.items],
        'page_size': 10,
        'current_page': pagination.page,
        'total_pages': pagination.pages,
        'total_results': pagination.total
    }

    return success_response(**response)


@profile.route('/recommendations', methods=['POST'])
@use_args(request_args.get_user_recommendations, locations=('json',))
def get_user_recommendations(args):
    user = User.query.get(args['user_id'])

    if not user:
        return error_response(400, 'User does not exist')

    movie_from = aliased(Movie)
    movie_to = aliased(Movie)

    query = db.session.query(Recommendation, movie_from, movie_to) \
                      .join(movie_from, Recommendation.recommendation_from == movie_from.id) \
                      .join(movie_to, Recommendation.recommendation_to == movie_to.id) \
                      .filter(Recommendation.author_id == user.id)

    pagination = paginate(query, page=args['page'], per_page=10)

    response = {
        'items': [{'body': recommendation.body, 'movie_from_title': movie_from.title,
                   'movie_from_poster_path': movie_from.poster_path, 'movie_from_id': movie_from.id,
                   'movie_to_title': movie_to.title, 'movie_to_poster_path': movie_to.poster_path,
                   'movie_to_id': movie_to.id} for recommendation, movie_from, movie_to in pagination.items],
        'page_size': 10,
        'current_page': pagination.page,
        'total_pages': pagination.pages,
        'total_results': pagination.total
    }

    return success_response(**response)


@profile.route('/comments', methods=['POST'])
@use_args(request_args.get_user_comments, locations=('json',))
def get_user_comments(args):
    user = User.query.get(args['user_id'])

    if not user:
        return error_response(400, 'User does not exist')

    query = db.session.query(Comment, User) \
                      .join(User, Comment.host_id == User.id) \
                      .filter(Comment.host_id == user.id) \
                      .order_by(Comment.timestamp)

    pagination = paginate(query, page=args['page'], per_page=10)

    response = {
        'items': [{'author': user.username, 'body': comment.body, 'timestamp': comment.timestamp,
                   'author_id': user.id} for comment, user in pagination.items],
        'page_size': 10,
        'current_page': pagination.page,
        'total_pages': pagination.pages,
        'total_results': pagination.total
    }

    return success_response(**response)