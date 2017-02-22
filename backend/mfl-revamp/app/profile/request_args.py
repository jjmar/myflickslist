from webargs import fields, validate

add_remove_friend_args = {
    'user_id': fields.Number(required=True)
}