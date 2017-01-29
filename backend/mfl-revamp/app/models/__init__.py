from app import database
from peewee import Model


class BaseModel(Model):
    class Meta:
        database = database