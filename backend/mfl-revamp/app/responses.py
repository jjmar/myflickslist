from flask import jsonify


def success_response(**kwargs):
    response = {'success': 1}
    for key, value in kwargs.iteritems():
        response[key] = value
    rv = jsonify(response)
    rv.status_code = 200
    return rv


def error_response(status_code, message):
    response = {'success': 0}
    response['message'] = message
    rv = jsonify(response)
    rv.status_code = status_code
    return rv
