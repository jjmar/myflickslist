from app import db

from sqlalchemy_utils import TSVectorType
from flask_sqlalchemy import BaseQuery
from sqlalchemy_searchable import SearchQueryMixin

movie_genre_lnk = db.Table('movie_genre_lnk', db.Model.metadata,
                           db.Column('movie_id', db.Integer, db.ForeignKey('movie.id')),
                           db.Column('genre_id', db.Integer, db.ForeignKey('genre.id')))

movie_country_lnk = db.Table('movie_country_lnk', db.Model.metadata,
                             db.Column('movie_id', db.Integer, db.ForeignKey('movie.id')),
                             db.Column('country_id', db.Integer, db.ForeignKey('country.id')))


class MovieQuery(BaseQuery, SearchQueryMixin):
    pass


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    query_class = MovieQuery
    search_vector = db.Column(TSVectorType('title'))

    # Movie Metadata
    title = db.Column(db.Text())
    status = db.Column(db.Text())
    budget = db.Column(db.BigInteger())
    imdb_id = db.Column(db.Text())
    revenue = db.Column(db.BigInteger())
    backdrop_path = db.Column(db.Text())
    poster_path = db.Column(db.Text())
    adult = db.Column(db.Boolean, default=False)
    original_language = db.Column(db.Text())
    overview = db.Column(db.Text())
    release_date = db.Column(db.Date())
    runtime = db.Column(db.Integer())
    tagline = db.Column(db.Text())
    homepage = db.Column(db.Text())

    # Relationships
    genres = db.relationship('Genre', backref='movies', secondary=movie_genre_lnk)
    characters = db.relationship('Character', backref='found_in')  # Should this be many to many?
    videos = db.relationship('Video')
    countries = db.relationship('Country', backref='movies', secondary=movie_country_lnk)
    recommendations = db.relationship('Recommendation', foreign_keys='Recommendation.recommendation_from',
                                      backref='from_movie')

    # Statistics
    rating_sum = db.Column(db.Integer(), default=0)  # Sum of all ratings
    num_ratings = db.Column(db.Integer(), default=0)  # Number of non-NULL ratings
    num_favourites = db.Column(db.Integer(), default=0)
    num_completed = db.Column(db.Integer(), default=0)
    num_ptw = db.Column(db.Integer(), default=0)
    num_custom = db.Column(db.Integer(), default=0)

    def add_completed_member(self, rating):
        self.num_completed += 1

        if rating:
            self.rating_sum += rating
            self.num_ratings += 1

    def add_ptw_member(self):
        self.num_ptw += 1

    def get_movie_metadata(self):
        ret = dict()
        ret['title'] = self.title
        ret['status'] = self.status
        ret['budget'] = self.budget
        ret['imdb_id'] = self.imdb_id
        ret['revenue'] = self.revenue
        ret['backdrop_path'] = self.backdrop_path
        ret['poster_path'] = self.poster_path
        ret['adult'] = self.adult
        ret['orginal_language'] = self.original_language
        ret['overview'] = self.overview
        ret['release_date'] = self.release_date
        ret['runtime'] = self.runtime
        ret['tagline'] = self.tagline
        ret['homepage'] = self.homepage

        ret['genres'] = [g.genre for g in self.genres]
        ret['characters'] = [{'character_name': c.character_name, 'actor_name': c.actor_name,
                              'profile_path': c.profile_path, 'actor_id': c.actor_id, 'order': c.order}
                             for c in self.characters]
        ret['videos'] = [{'site': v.site, 'key': v.key, 'type': v.type, 'name': v.name} for v in self.videos]
        ret['countries'] = [c.name for c in self.countries]
        return ret

    def get_movie_statistics(self):
        ret = dict()
        ret['rating_sum'] = self.rating_sum
        ret['num_ratings'] = self.num_ratings
        ret['num_favourites'] = self.num_favourites
        ret['num_completed'] = self.num_completed
        ret['num_ptw'] = self.num_ptw
        ret['num_custom'] = self.num_custom
        return ret


class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(db.Text(), unique=True)


class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    character_name = db.Column(db.Text())
    actor_name = db.Column(db.Text())
    # M : 1
    actor_id = db.Column(db.Integer(), db.ForeignKey('actor.id'))
    actor = db.relationship('Actor', backref='roles')
    profile_path = db.Column(db.Text())
    order = db.Column(db.Integer())
    movie_id = db.Column(db.Integer(), db.ForeignKey('movie.id'))
    cast_id = db.Column(db.Integer())
    credit_id = db.Column(db.Text())


class ActorQuery(BaseQuery, SearchQueryMixin):
    pass


class Actor(db.Model):
    id = db.Column(db.Integer(), primary_key=True)  # 1-1 w/ api
    query_class = ActorQuery
    search_vector = db.Column(TSVectorType('name'))

    biography = db.Column(db.Text())
    birthday = db.Column(db.Date())
    deathday = db.Column(db.Date())
    homepage = db.Column(db.Text())
    name = db.Column(db.Text())
    place_of_birth = db.Column(db.Text())
    profile_path = db.Column(db.Text())
    imdb_id = db.Column(db.Text())

    def get_actor_metadata(self):
        ret = dict()
        ret['biography'] = self.biography
        ret['birthday'] = self.birthday
        ret['deathday'] = self.deathday
        ret['homepage'] = self.homepage
        ret['name'] = self.name
        ret['place_of_birth'] = self.place_of_birth
        ret['profile_path'] = self.profile_path
        ret['imdb_id'] = self.imdb_id
        return ret


class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    site = db.Column(db.Text())
    key = db.Column(db.Text())
    type = db.Column(db.Text())
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    name = db.Column(db.Text())
    iso_639_1 = db.Column(db.String(2))


class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text())
    iso_3166_1 = db.Column(db.String(2), unique=True, index=True)

