from app import db
from app.movie import movie
from app.models.movie import Movie, Actor
from app.models.user import User
from app.models.social import Review, Recommendation
from app.responses import success_response, error_response
import request_args

from webargs.flaskparser import use_args
from flask_jwt_extended import jwt_required, get_jwt_identity


@movie.route('/getmoviedetails', methods=['POST'])
@use_args(request_args.get_movie_details_args, locations=('json',))
def get_movie_details(args):
    movie = Movie.query.get(args['movie_id'])

    if not movie:
        return error_response(400, "Movie does not exist")

    response = {}
    for k, v in movie.get_movie_metadata().iteritems():
        response[k] = v
    response['metadata'] = movie.get_movie_statistics()

    return success_response(results=response)


@movie.route('/getactordetails', methods=['POST'])
@use_args(request_args.get_actor_details_args, locations=('json',))
def get_actor_details(args):
    actor = Actor.query.get(args['actor_id'])

    if not actor:
        return error_response(400, 'Actor does not exist')

    response = {}
    for k, v in actor.get_actor_metadata().iteritems():
        response[k] = v
    return success_response(results=response)


@movie.route('/postreview', methods=['POST'])
@use_args(request_args.post_movie_review_args, locations=('json',))
@jwt_required
def post_movie_review(args):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return error_response(400, 'User does not exist')

    movie = Movie.query.get(args['movie_id'])
    if not movie:
        return error_response(400, 'Movie does not exist')

    # Check user hasn't already submitted a review for that movie
    existing_review = Review.query.filter_by(author_id=user_id).filter_by(movie_id=args['movie_id']).first()

    if existing_review:
        return error_response(400, 'User has already submitted a review for this movie')

    review = Review(author_id=user_id, movie_id=args['movie_id'], body=args['body'])
    db.session.add(review)
    db.session.commit()

    return success_response(review_id=review.id)


@movie.route('/removereview', methods=['POST'])
@use_args(request_args.remove_movie_review_args, locations=('json',))
@jwt_required
def remove_movie_review(args):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return error_response(400, 'User does not exist')

    review = Review.query.get(args['review_id'])

    if not review:
        return error_response(400, 'Review does not exist')
    elif review.author_id != user_id:
        return error_response(400, 'Review does not belong to user')

    db.session.delete(review)
    db.session.commit()
    return success_response()


@movie.route('/postrecommendation', methods=['POST'])
@use_args(request_args.post_recommendation_args, locations=('json',))
@jwt_required
def post_recommendation(args):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return error_response(400, 'User does not exist')

    recommendation_from = Movie.query.get(args['recommendation_from'])
    if not recommendation_from:
        return error_response(400, '1st movie does not exist')

    recommendation_to = Movie.query.get(args['recommendation_to'])
    if not recommendation_to:
        return error_response(400, '2nd movie does not exist')

    existing_rec = Recommendation.query.filter_by(recommendation_from=args['recommendation_from'])\
                                       .filter_by(recommendation_to=args['recommendation_to'])\
                                       .filter_by(author_id=user_id).first()

    if existing_rec:
        return error_response(400, 'Recommendation pairing already exists')

    recommendation = Recommendation(author_id=user_id, body=args['body'],
                                    recommendation_from=args['recommendation_from'],
                                    recommendation_to=args['recommendation_to'])

    db.session.add(recommendation)
    db.session.commit()
    return success_response(recommendation_id=recommendation.id)


@movie.route('/removerecommendation', methods=['POST'])
@use_args(request_args.remove_recommendation_args, locations=('json',))
@jwt_required
def remove_recommendation(args):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return error_response(400, 'User does not exist')

    recommendation = Recommendation.query.get(args['recommendation_id'])

    if not recommendation:
        return error_response(400, 'Recommendation does not exist')
    elif recommendation.author_id != user_id:
        return error_response(400, 'Recommendation does not belong to user')

    db.session.delete(recommendation)
    db.session.commit()
    return success_response()
