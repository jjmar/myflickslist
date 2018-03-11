from api.responses import error_response


def handle_unprocessable_entity(err):
    data = getattr(err, 'data')
    messages = data['messages']
    return error_response(422, message=messages)
