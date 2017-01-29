from app import init_app, database
from app.models.list import List, ListItem
from app.models.movie import Movie, Character, Actor, Video, Country, Genre, Review, Recommendation
from app.models.user import User
from flask_script import Manager

app = init_app()

manager = Manager(app)

@manager.command
def create_tables():
    database.create_tables(models=[List, ListItem, Movie, Character, Actor, Video, Country, Genre, Recommendation,
                                   Review, User])


@manager.command
def drop_tables():
    database.drop_tables(models=[List, ListItem, Movie, Character, Actor, Video, Country, Genre, Recommendation, Review,
                                 User])


if __name__ == "__main__":
    manager.run()
