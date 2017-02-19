from webargs import fields

register_args = {
    'email': fields.Str(required=True),
    'username': fields.Str(required=True),
    'password': fields.Str(required=True)
}
