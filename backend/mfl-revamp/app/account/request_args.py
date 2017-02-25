from webargs import fields, validate, missing

account_email_args = {
    'email': fields.Str(required=True, validate=validate.Email())

}

account_password_args = {
    'password': fields.Str(required=True, validate=validate.Length(min=8, error='Password must be atleast 8 characters long'))
}