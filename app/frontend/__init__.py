from flask import Blueprint
from flask import make_response

frontend = Blueprint('frontend', __name__)


@frontend.route('/')
def index():
    return make_response(open('app/frontend/index.html').read())
