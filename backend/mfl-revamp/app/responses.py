from flask import jsonify

RESPONSES = {
            0: {"message": "Authentication Required", "status": 400},
            1: {"message": "Item already present in list", "status": 400},
            2: {"message": "Generic form validation error", "status": 400},
            3: {"message": "Maximum number of items favourited reached (max: 5)", "status": 400},
            4: {"message": "Invalid movie_id", "status": 400},
            5: {"message": "Item already favourited", "status": 400},
            6: {"message": "Invalid list_id", "status": 400},
            7: {"message": "Invalid item_id", "status": 400},
            8: {"message": "Cannot befriend self", "status": 400},
            9: {"message": "Already friends", "status": 400},
            10: {"message": "Invalid user_id", "status": 400},
            11: {"message": "Invalid comment_id", "status": 400},
            12: {"message": "Cannot submit more than one review for a movie", "status": 400},
            13: {"message": "Review must be placed for movie on users completed list", "status": 400}
            }


def success_response(payload=None):
    response = {"success": 1}
    if payload:
        response["payload"] = payload
    rv = jsonify(response)
    rv.status_code = 200
    return rv


def error_response(error_code):
    error = RESPONSES[error_code]
    payload = {"success": 0,
               "message": error["message"],
               "status": error["status"],
               "code": error_code}
    rv = jsonify(payload)
    rv.status_code = error["status"]
    return rv