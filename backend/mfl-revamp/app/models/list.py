from . import BaseModel
from peewee import CharField, DateField, TextField, BooleanField, IntegerField


class List(BaseModel):
    # All Lists
    name = CharField(max_length=64)
    #user_id
    #items
    type = CharField(max_length=20)

    # Custom Lists
    date_created = DateField()
    description = CharField(max_length=256)


class ListItem(BaseModel):
    # All List Items
    # movie
    # list_id
    ordering = IntegerField()
    notes = CharField(max_length=64)

    # Default List
    completed = BooleanField()
    rating = IntegerField()
    date_completed = DateField()