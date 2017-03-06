from webargs import fields, validate

create_custom_list_args = {
    'name': fields.Str(required=True, validate=validate.Length(min=1, max=64)),
    'private': fields.Boolean(required=True),
    'description': fields.Str(missing=None, validate=validate.Length(max=256))
}