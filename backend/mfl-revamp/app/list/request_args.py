from webargs import fields, validate

create_custom_list_args = {
    'name': fields.Str(required=True, validate=validate.Length(min=1, max=64)),
    'private': fields.Boolean(required=True),
    'description': fields.Str(missing=None, validate=validate.Length(max=256))
}

edit_custom_list_args = {
    'list_id': fields.Integer(required=True),
    'private': fields.Boolean(required=True),
    'description': fields.Str(required=True, validate=validate.Length(max=256))
}

add_custom_list_item_args = {
    'list_id': fields.Integer(required=True),
    'movie_id': fields.Integer(required=True),
    'notes': fields.Str(missing=None, validate=validate.Length(max=64))
}

delete_custom_list_item_args = {
    'list_item_id': fields.Integer(required=True)
}

get_user_lists_args = {
    'user_id': fields.Integer(required=True)
}

get_list_details_args = {
    'list_id': fields.Integer(required=True)
}

get_favourites_args = {
    'user_id': fields.Integer(required=True)
}