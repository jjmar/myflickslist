from app import db


movie_genre_lnk = db.Table('movie_genre_lnk', db.Model.metadata,
                           db.Column('movie_id', db.Integer, db.ForeignKey('movie.id')),
                           db.Column('genre_id', db.Integer, db.ForeignKey('genre.id')))

movie_country_lnk = db.Table('movie_country_lnk', db.Model.metadata,
                             db.Column('movie_id', db.Integer, db.ForeignKey('movie.id')),
                             db.Column('country_id', db.Integer, db.ForeignKey('country.id')))


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # Movie Specific Data
    genres = db.relationship('Genre', backref='movies', secondary=movie_genre_lnk)
    characters = db.relationship('Character', backref='found_in') # Should this be many to many?
    videos = db.relationship('Video')
    countries = db.relationship('Country', backref='movies', secondary=movie_country_lnk)

    # 1 : M
    recommendations = db.relationship('Recommendation', foreign_keys='Recommendation.recommendation_from',
                                      backref='from_movie')

    # Statistics
    avg_rating = db.Column(db.Integer(), default=0)  # rating_sum / num_ratings
    rating_sum = db.Column(db.Integer(), default=0)  # Sum of all ratings
    num_ratings = db.Column(db.Integer(), default=0)  # Number of non-NULL ratings
    num_members = db.Column(db.Integer(), default=0)  # Number of times present in user MFL's (num_completed + num_ptw)
    num_favourites = db.Column(db.Integer(), default=0)
    num_completed = db.Column(db.Integer(), default=0)  # Number of users who have watched this movie
    num_ptw = db.Column(db.Integer(), default=0)  # Number of users who are planning to watch this movie
    num_custom = db.Column(db.Integer(), default=0)  # Number of times this movie appears in custom lists


class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(db.Text(), unique=True)


class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    character = db.Column(db.Text())
    # M : 1
    actor_id = db.Column(db.Integer(), db.ForeignKey('actor.id'))
    actor = db.relationship('Actor', backref='roles')
    profile_path = db.Column(db.Text())
    order = db.Column(db.Integer())
    movie_id = db.Column(db.Integer(), db.ForeignKey('movie.id'))
    cast_id = db.Column(db.Integer())
    credit_id = db.Column(db.Text())


class Actor(db.Model):
    id = db.Column(db.Integer(), primary_key=True) # 1-1 w/ api
    biography = db.Column(db.Text())
    birthday = db.Column(db.Date())
    deathday = db.Column(db.Date())
    homepage = db.Column(db.Text())
    name = db.Column(db.Text())
    place_of_birth = db.Column(db.Text())
    profile_path = db.Column(db.Text())
    imdb_id = db.Column(db.Text())


class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    site = db.Column(db.Text())
    key = db.Column(db.Text())
    type = db.Column(db.Text())
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    iso_639_1 = db.Column(db.String(2))


class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text())
    iso_3166_1 = db.Column(db.String(2), unique=True, index=True)

