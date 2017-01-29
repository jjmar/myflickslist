from . import BaseModel
from peewee import CharField, DateField, DateTimeField, TextField, IntegerField
from flask import current_app


class User(BaseModel):

    # Account Specific
    email = CharField(unique=True)
    username = CharField(unique=True)
    password = CharField()

    # Profile Specific
    fav_genre = CharField()
    join_date = DateField()
    last_online = DateTimeField
    gender = CharField()
    location = CharField()
    website = CharField()
    about = CharField(max_length=500)
    profile_views = IntegerField(default=0)

    #friends M:M
    #profile_comments 1:M
    #posted_comments 1:M

    #default_list 1:1
    #favourites_list 1:1
    #custom_lists 1:M