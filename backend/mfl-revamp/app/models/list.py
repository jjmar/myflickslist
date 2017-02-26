from app import db

from sqlalchemy.orm import relationship

from datetime import datetime


class DefaultList(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(64))
    owner_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    items = relationship('DefaultListItem', backref='list')


class FavList(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(64))
    owner_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    items = relationship('FavListItem', backref='list')


class CustomList(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(64))
    owner_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    items = relationship('CustomListItem', backref='list')
    creation_ts = db.Column(db.DateTime(), default=datetime.utcnow)
    description = db.Column(db.String(256))
    private = db.Column(db.Boolean(), default=False)

class DefaultListItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie = db.relationship('Movie')
    movie_id = db.Column(db.Integer(), db.ForeignKey('movie.id'))
    list_id = db.Column(db.Integer(), db.ForeignKey('default_list.id'))
    notes = db.Column(db.String(64))
    completed = db.Column(db.Boolean(), default=False)
    rating = db.Column(db.Integer())
    completion_date = db.Column(db.Date())


class CustomListItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie = db.relationship('Movie')
    movie_id = db.Column(db.Integer(), db.ForeignKey('movie.id'))
    list_id = db.Column(db.Integer(), db.ForeignKey('custom_list.id'))
    notes = db.Column(db.String(64))
    ordering = db.Column(db.Integer())


class FavListItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie = db.relationship('Movie')
    movie_id = db.Column(db.Integer(), db.ForeignKey('movie.id'))
    list_id = db.Column(db.Integer(), db.ForeignKey('fav_list.id'))
    notes = db.Column(db.String(64))
    ordering = db.Column(db.Integer())
