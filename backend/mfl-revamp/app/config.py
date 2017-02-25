import os
import datetime


class DefaultConfig():

    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = "postgresql://" + \
                              os.environ.get("MFL_DB_USER") + ":" + \
                              os.environ.get("MFL_DB_PASSWORD") + "@" + \
                              os.environ.get("MFL_DB_NAME")
    
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

    # JWT
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=7)

    # Confirmation Token
    CONFIRM_TOKEN_EXPIRES = 3600

    # Keys
    SECRET_KEY = os.environ.get('MFL_REVAMP_APP_KEY')
    TMDB_API_KEY = os.environ.get('MFL_REVAMP_API_KEY')