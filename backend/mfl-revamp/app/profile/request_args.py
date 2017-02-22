from webargs import fields, validate

friend_args = {
    'user_id': fields.Number(required=True)
}