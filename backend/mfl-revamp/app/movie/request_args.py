from webargs import fields, validate

get_movie_details_args = {
    'movie_id': fields.Integer(required=True)
}

get_actor_details_args = {
    'actor_id': fields.Integer(required=True)
}

post_movie_review_args = {
    'movie_id': fields.Integer(required=True),
    'body': fields.String(required=True, validate=validate.Length(min=1, max=10000))
}

remove_movie_review_args = {
    'review_id': fields.Integer(required=True)
}

post_recommendation_args = {
    'recommendation_from': fields.Integer(required=True),
    'recommendation_to': fields.Integer(required=True),
    'body': fields.String(required=True, validate=validate.Length(min=1, max=500))
}

remove_recommendation_args = {
    'recommendation_id': fields.Integer(required=True)
}