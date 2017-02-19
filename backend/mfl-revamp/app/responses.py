from flask import jsonify


def success_response():
    response = {'success': 1}
    rv = jsonify(response)
    rv.status_code = 200
    return rv


def error_response(status_code, payload=None):
    response = {'success': 0}
    if payload:
        response['message'] = payload
    rv = jsonify(response)
    rv.status_code = status_code
    return rv
