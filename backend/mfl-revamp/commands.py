from app import db, init_app
from app.models.user import User, Comment, Friendship
from app.models.list import DefaultList, DefaultListItem, FavList, FavListItem, CustomList, CustomListItem
from app.models.movie import Movie, Character, Country, Actor, Video, Genre
from app.models.social import Review, Recommendation
from flask_script import Command


class CreateTables(Command):
    def run(self):
        db.create_all()


class DropTables(Command):
    def run(self):
        db.drop_all()
