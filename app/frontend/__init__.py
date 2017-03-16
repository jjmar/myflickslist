from flask import Blueprint
from flask import make_response

frontend = Blueprint('frontend', __name__)

import routes
