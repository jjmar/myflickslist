from app.frontend import frontend

from flask import make_response


@frontend.route('/')
def index():
    return make_response(open('app/frontend/app/index.html').read())