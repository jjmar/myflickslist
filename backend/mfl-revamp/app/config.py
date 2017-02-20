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

    # Flask Config
    DEBUG = True

    # JWT
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=7)

    # Keys
    SECRET_KEY = os.environ.get('MFL_REVAMP_APP_KEY')
    TMDB_API_KEY = os.environ.get('MFL_REVAMP_API_KEY')