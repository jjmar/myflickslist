from flask import Flask
from config import DefaultConfig


def init_app():
    app = Flask(__name__)
    app.config.from_object(DefaultConfig)

    from main import main as main_blueprint
    from account import account as account_blueprint
    from list import list as list_blueprint
    from movie import movie as movie_blueprint
    from profile import profile as profile_blueprint
    from search import search as search_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(account_blueprint)
    app.register_blueprint(profile_blueprint)
    app.register_blueprint(list_blueprint)
    app.register_blueprint(movie_blueprint)
    app.register_blueprint(search_blueprint)

    return app
