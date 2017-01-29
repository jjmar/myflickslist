from flask import Flask, g
from config import DefaultConfig
from peewee import SqliteDatabase

database = SqliteDatabase(DefaultConfig.DATABASE)


def _db_connect():
    g.db = database
    g.db.connect()


def _db_disconnect(request):
    if not g.db.is_closed():
        g.db.close()
    return request


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

    app.before_request(_db_connect)
    app.after_request(_db_disconnect)

    return app
