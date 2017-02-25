from webargs import fields, validate, missing

friend_args = {
    'user_id': fields.Integer(required=True)
}

set_profile_info_args = {
    'fav_genre': fields.Str(missing=None, validate=validate.Length(max=64)),
    'gender': fields.Str(missing=None, validate=lambda x: x in ('Male', 'Female')),
    'location': fields.Str(missing=None, validate=validate.Length(max=64)),
    'website': fields.Str(missing=None, validate=validate.Length(max=64)),
    'about': fields.Str(missing=None, validate=validate.Length(max=256))
}

get_profile_info_args = {
    'user_id': fields.Integer(required=True)
}