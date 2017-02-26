from webargs import fields, validate

update_account_email_args = {
    'email': fields.Str(required=True, validate=validate.Email())

}

update_account_password_args = {
    'password': fields.Str(required=True, validate=validate.Length(min=8, error='Password must be atleast 8 characters long'))
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