from app import db

from sqlalchemy.orm import relationship
from flask_sqlalchemy import BaseQuery
from sqlalchemy_utils import TSVectorType
from sqlalchemy_searchable import SearchQueryMixin

from datetime import datetime


class Favourite(db.Model):
    user_id = db.Column(db.ForeignKey('user.id'), primary_key=True)
    movie_id = db.Column(db.ForeignKey('movie.id'), primary_key=True)
    movie = db.relationship('Movie')
    ordering = db.Column(db.Integer())


class FlicksList(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(64))
    owner_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    items = relationship('FlicksListItem', backref='list')

    def get_list_details(self):
        ret = {
            'completed': [],
            'ptw': []
        }

        for item in self.items:
            if item.completed:
                ret['completed'].append({'title': item.movie.title, 'list_item_id': item.id, 'notes': item.notes,
                                         'completed': item.completed, 'rating': item.rating,
                                         'completion_date': item.completion_date, 'ordering': item.ordering})
            else:
                ret['ptw'].append({'title': item.movie.title, 'list_item_id': item.id, 'notes': item.notes,
                                   'completed': item.completed, 'ordering': item.ordering})

        return ret


class FlicksListItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie = db.relationship('Movie')
    movie_id = db.Column(db.Integer(), db.ForeignKey('movie.id'))
    list_id = db.Column(db.Integer(), db.ForeignKey('flicks_list.id'))
    notes = db.Column(db.String(64))
    completed = db.Column(db.Boolean(), default=False)
    rating = db.Column(db.Integer())
    completion_date = db.Column(db.Date())
    ordering = db.Column(db.Integer())


class CustomListQUery(BaseQuery, SearchQueryMixin):
    pass


class CustomList(db.Model):
    query_class = CustomListQUery
    search_vector = db.Column(TSVectorType('name'))

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(64))
    owner_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    items = relationship('CustomListItem', cascade='all, delete-orphan', backref='list')
    creation_ts = db.Column(db.DateTime(), default=datetime.utcnow)
    description = db.Column(db.String(256))
    private = db.Column(db.Boolean(), default=False)


class CustomListItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie = db.relationship('Movie')
    movie_id = db.Column(db.Integer(), db.ForeignKey('movie.id'))
    list_id = db.Column(db.Integer(), db.ForeignKey('custom_list.id'))
    notes = db.Column(db.String(64))
    ordering = db.Column(db.Integer())
