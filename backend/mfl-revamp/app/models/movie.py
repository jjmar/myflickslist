from . import BaseModel
from peewee import IntegerField, CharField, TextField, DateField, PrimaryKeyField
from datetime import date


class Movie(BaseModel):

    # Movie Specific Data

    # genres M:M
    # characters 1:M or M:M
    # videos 1:M
    # countries M:M
    # reviews 1:M
    # reccomendations 1:M

    # Statistics
    avg_rating = IntegerField(default=0)  # rating_sum / num_ratings
    rating_sum = IntegerField(default=0)  # sum of all ratings
    num_ratings = IntegerField(default=0)  # number of non-null ratings
    num_members = IntegerField(default=0)  # number of times present in users MFL's (num_completed + num_ptw)
    num_favs = IntegerField(default=0)
    num_completed = IntegerField(default=0)
    num_ptw = IntegerField(default=0)
    num_custom = IntegerField(default=0)


class Genre(BaseModel):
    genre = CharField()


class Character(BaseModel):
    character = CharField()
    actor_name = CharField()
    # actor_id = IntegerField() Foreign Key to Actors
    profile_path = CharField()
    order = IntegerField()
    #movie_id = M:M
    cast_id = IntegerField()
    credit_id = CharField()


class Actor(BaseModel):
    id = PrimaryKeyField() # 1-1 with API
    biography = TextField()
    birthday = DateField()
    deathday = DateField()
    homepage = CharField()
    name = CharField()
    place_of_birth = CharField()
    profile_path = CharField()
    imdb_id = IntegerField()


class Video(BaseModel):
    site = CharField()
    key = CharField()
    type = CharField()
    #movie_id = m:1
    iso_639_1 = CharField(max_length=2)


class Country(BaseModel):
    name = CharField()
    iso_3166_1 = CharField(max_length=2, unique=True, index=True)


class Review(BaseModel):
    body = CharField(max_length=10000)
    #author_id
    #movie_id
    timestamp = DateField(default=date.today)


class Recommendation(BaseModel):
    body = CharField(max_length=500)
    #parent_id
    #recommendation_id
    #author_id
    #recommendation