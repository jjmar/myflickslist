from webargs import fields

get_movie_details_args = {
    'movie_id': fields.Integer(required=True)
}

get_actor_details_args = {
    'actor_id': fields.Integer(required=True)
}