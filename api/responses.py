from flask import jsonify


def success_response(**kwargs):
    response = {'success': True}

    if len(kwargs):
        response['data'] = {}
    
    for key, value in kwargs.items():
        response['data'][key] = value
    rv = jsonify(response)
    rv.status_code = 200
    return rv


def error_response(status_code, message):
    response = {'success': False,
                'message': message
    }
    rv = jsonify(response)
    rv.status_code = status_code
    return rv


def jwt_error(message):
    return error_response(401, message)
