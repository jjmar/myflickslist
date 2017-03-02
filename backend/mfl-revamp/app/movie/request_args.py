from webargs import fields, validate

get_movie_details_args = {
    'movie_id': fields.Integer(required=True)
}

get_actor_details_args = {
    'actor_id': fields.Integer(required=True)
}

post_movie_review_args = {
    'movie_id': fields.Integer(required=True),
    'body': fields.Str(required=True, validate=validate.Length(min=0, max=10000))
}

remove_movie_review_args = {
    'review_id': fields.Integer(required=True)
}