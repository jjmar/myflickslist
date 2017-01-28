import os


class DefaultConfig():

    # Flask Config
    DEBUG = True

    # Keys
    SECRET_KEY = os.environ.get("MFL_REVAMP_APP_KEY")
    TMDB_API_KEY = os.environ.get("MFL_REVAMP_API_KEY")