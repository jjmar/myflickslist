from app.frontend import frontend

from flask import make_response


@frontend.route('/')
def index():
    return make_response(open('app/angular_app/index.html').read())