from app import db
from app.models.user import User, Comment, Friendship
from app.models.list import FlicksList, FlicksListItem, Favourite, CustomList, CustomListItem
from app.models.movie import Movie, Character, Country, Actor, Video, Genre
from app.models.social import Review, Recommendation
from app.tmdb.fetchers import fetch_genres, fetch_all_movies
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
        db.configure_mappers()
        db.create_all()
        fetch_genres()
        fetch_all_movies(10)
