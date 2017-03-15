from app import db

from datetime import date


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    body = db.Column(db.String(10000))

    # M:1
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    movie = db.relationship('Movie', backref='reviews')

    timestamp = db.Column(db.Date(), default=date.today)


class Recommendation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    body = db.Column(db.String(500))
    timestamp = db.Column(db.Date(), default=date.today)

    recommendation_from = db.Column(db.Integer(), db.ForeignKey('movie.id'))

    # M : 1
    recommendation_to = db.Column(db.Integer(), db.ForeignKey('movie.id'))
    recommendation = db.relationship('Movie', foreign_keys='Recommendation.recommendation_to')
