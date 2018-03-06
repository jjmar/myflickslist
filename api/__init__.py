from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_searchable import make_searchable

from api.config import DefaultConfig
from api.error_handlers import handle_unprocessable_entity
from api.responses import jwt_error

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

    # Register backend (api) blueprint
    from api.services.account import account as account_blueprint
    from api.services.list import list as list_blueprint
    from api.services.movie import movie as movie_blueprint
    from api.services.profile import profile as profile_blueprint
    from api.services.search import search as search_blueprint
    from api.services.auth import auth as auth_blueprint

    app.register_blueprint(account_blueprint, url_prefix=API_PREFIX + '/account')
    app.register_blueprint(profile_blueprint, url_prefix=API_PREFIX + '/profile')
    app.register_blueprint(list_blueprint, url_prefix=API_PREFIX + '/list')
    app.register_blueprint(movie_blueprint, url_prefix=API_PREFIX + '/movie')
    app.register_blueprint(search_blueprint, url_prefix=API_PREFIX + '/search')
    app.register_blueprint(auth_blueprint, url_prefix=API_PREFIX + '/auth')

    # Register error handlers
    app.register_error_handler(422, handle_unprocessable_entity)

    # Edit JWT error responses to conform to API response format
    jwt.expired_token_loader(callback=jwt_error)
    jwt.unauthorized_loader(callback=jwt_error)
    jwt.invalid_token_loader(callback=jwt_error)

    make_searchable()
    return app
