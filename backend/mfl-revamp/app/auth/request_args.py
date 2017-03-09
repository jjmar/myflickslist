from webargs import fields, validate

login_args = {
    'email': fields.String(required=True, validate=validate.Email()),
    'password': fields.String(required=True)
}

register_args = {
    'email': fields.String(required=True, validate=validate.Email()),
    'username': fields.String(required=True, validate=validate.Regexp(regex='^[a-zA-Z0-9_]{6,64}$',
                                                                      error='Username must be an alphanumeric string '
                                                                            'between 6-64 characters in length')),
    'password': fields.String(required=True, validate=validate.Length(min=8,
                                                                      error='Password must be atleast 8 characters long'))
}
