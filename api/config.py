import os
import datetime


class DefaultConfig(object):

    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = 'postgresql://' + \
                              os.environ.get('MFL_DB_USER') + ':' + \
                              os.environ.get('MFL_DB_PASSWORD') + '@' + \
                              os.environ.get('MFL_DB_NAME')
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True

    # Flask Mail
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MFL_MAIL_USER')
    MAIL_PASSWORD = os.environ.get('MFL_MAIL_PASS')
    MAIL_DEFAULT_SENDER = "myflickslist"

    # Flask Config
    DEBUG = True

    # API Access token expiration
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=7)

    # Account Verification token expiration (in seconds)
    JWT_CONFIRM_TOKEN_EXPIRES = 3600

    # Reset Password token expiration (in seconds)
    JWT_RESET_PASS_TOKEN_EXPIRES = 3600

    # Keys
    SECRET_KEY = os.environ.get('MFL_APP_KEY')
    TMDB_API_KEY = os.environ.get('MFL_API_KEY')

    # TMDB API
    TMDB_API_URL = 'http://api.themoviedb.org/3/'
