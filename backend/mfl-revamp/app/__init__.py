from flask import Flask
from config import DefaultConfig
from flask_sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()


def init_app():
    app = Flask(__name__)
    app.config.from_object(DefaultConfig)

    db.init_app(app)
    bcrypt.init_app(app)

    from main import main as main_blueprint
    from account import account as account_blueprint
    from list import list as list_blueprint
    from movie import movie as movie_blueprint
    from profile import profile as profile_blueprint
    from search import search as search_blueprint
    from auth import auth as auth_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(account_blueprint)
    app.register_blueprint(profile_blueprint)
    app.register_blueprint(list_blueprint)
    app.register_blueprint(movie_blueprint)
    app.register_blueprint(search_blueprint)
    app.register_blueprint(auth_blueprint)

    return app
