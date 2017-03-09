from webargs import fields, validate

create_custom_list_args = {
    'name': fields.Str(required=True, validate=validate.Length(min=1, max=64)),
    'private': fields.Boolean(required=True),
    'description': fields.String(missing=None, validate=validate.Length(max=256))
}

edit_custom_list_args = {
    'list_id': fields.Integer(required=True),
    'private': fields.Boolean(required=True),
    'description': fields.String(required=True, validate=validate.Length(max=256))
}

add_custom_list_item_args = {
    'list_id': fields.Integer(required=True),
    'movie_id': fields.Integer(required=True),
    'notes': fields.String(missing=None, validate=validate.Length(max=64))
}

delete_custom_list_item_args = {
    'list_item_id': fields.Integer(required=True)
}

delete_custom_list_args = {
    'list_id': fields.Integer(required=True)
}

get_custom_lists_args = {
    'user_id': fields.Integer(required=True)
}

add_favourite_item_args = {
    'movie_id': fields.Integer(required=True)
}

get_favourites_args = {
    'user_id': fields.Integer(required=True)
}

remove_favourite_item_args = {
    'movie_id': fields.Integer(required=True)
}

add_flicks_list_item_args = {
    'movie_id': fields.Integer(required=True),
    'notes': fields.String(missing=None, validate=validate.Length(max=64)),
    'rating': fields.Integer(missing=None, validate=validate.Range(min=1, max=10)),
    'completion_date': fields.Date(missing=None),
    'completed': fields.Boolean(required=True)
}