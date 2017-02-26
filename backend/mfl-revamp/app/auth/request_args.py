from webargs import fields, validate

login_args = {
    'email': fields.Str(required=True, validate=validate.Email()),
    'password': fields.Str(required=True)
}

register_args = {
    'email': fields.Str(required=True, validate=validate.Email()),
    'username': fields.Str(required=True, validate=validate.Regexp(regex='^[a-zA-Z0-9_]{6,64}$',
                                                                   error='Username must be an alphanumeric string '
                                                                         'between 6-64 characters in length')),
    'password': fields.Str(required=True, validate=validate.Length(min=8, error='Password must be atleast 8 characters '
                                                                                'long'))
}

request_new_password_args = {
    'email': fields.Str(required=True, validate=validate.Email())
}

verify_account_args = {
    'verify_token': fields.Str(required=True)
}

set_new_password_args = {
    'reset_token': fields.Str(required=True),
    'password': fields.Str(required=True, validate=validate.Length(min=8, error='Password must be atleast 8 characters '
                                                                                'long'))
}
