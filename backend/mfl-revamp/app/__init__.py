from config import DefaultConfig
from error_handlers import handle_unprocessable_entity

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_migrate import Migrate
from sqlalchemy_searchable import make_searchable

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()
mail = Mail()
migrate = Migrate()

API_PREFIX = '/api'


def init_app():
    app = Flask(__name__)
    app.config.from_object(DefaultConfig)

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)

    from main import main as main_blueprint
    from account import account as account_blueprint
    from list import list as list_blueprint
    from movie import movie as movie_blueprint
    from profile import profile as profile_blueprint
    from search import search as search_blueprint
    from auth import auth as auth_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(account_blueprint, url_prefix=API_PREFIX + '/account')
    app.register_blueprint(profile_blueprint, url_prefix=API_PREFIX + '/profile')
    app.register_blueprint(list_blueprint, url_prefix=API_PREFIX + '/list')
    app.register_blueprint(movie_blueprint, url_prefix=API_PREFIX + '/movie')
    app.register_blueprint(search_blueprint, url_prefix=API_PREFIX + '/search')
    app.register_blueprint(auth_blueprint, url_prefix=API_PREFIX + '/auth')

    # Register error handlers
    app.register_error_handler(422, handle_unprocessable_entity)
    make_searchable()
    return app
