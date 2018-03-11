from webargs import fields, validate

friend_args = {
    'user_id': fields.Integer(required=True)
}

update_profile_info_args = {
    'fav_genre': fields.String(missing=None, validate=validate.Length(max=64)),
    'gender': fields.String(missing=None, validate=lambda x: x in ('Male', 'Female')),
    'location': fields.String(missing=None, validate=validate.Length(max=64)),
    'website': fields.String(missing=None, validate=validate.Length(max=64)),
    'about': fields.String(missing=None, validate=validate.Length(max=256))
}

get_profile_info_args = {
    'user_id': fields.Integer(required=True)
}

post_comment_args = {
    'host_id': fields.Integer(required=True),
    'body': fields.String(required=True, validate=validate.Length(min=1, max=512))
}

remove_comment_args = {
    'comment_id': fields.Integer(required=True)
}

get_user_reviews = {
    'user_id': fields.Integer(required=True),
    'page': fields.Integer(missing=1, validate=validate.Range(min=1))
}

get_user_recommendations = {
    'user_id': fields.Integer(required=True),
    'page': fields.Integer(missing=1, validate=validate.Range(min=1))
}

get_user_comments = {
    'user_id': fields.Integer(required=True),
    'page': fields.Integer(missing=1, validate=validate.Range(min=1))
}
