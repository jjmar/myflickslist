from api import db
from api.tmdb.fetchers import fetch_genres, fetch_all_movies
from api.models.list import *
from api.models.user import *
from api.models.movie import *
from api.models.social import *

from flask_script import Command


class CreateTables(Command):
    def run(self):
        db.create_all()


class DropTables(Command):
    def run(self):
        db.drop_all()


class Initailize(Command):
    def run(self):
        db.drop_all()
        db.session.execute( "DROP FUNCTION IF EXISTS actor_search_vector_update()")
        db.session.execute( "DROP FUNCTION IF EXISTS custom_list_search_vector_update()")
        db.session.execute( "DROP FUNCTION IF EXISTS movie_search_vector_update()")
        db.session.execute( "DROP FUNCTION IF EXISTS user_search_vector_update()")
        db.session.commit()
        db.configure_mappers()
        db.create_all()
        fetch_genres()
        fetch_all_movies(10)
