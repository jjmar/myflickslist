from api import db
from api.models.movie import Genre, Movie, Country, Character, Actor, Video
from api.tmdb.api_request import perform_request

from datetime import datetime


# Fetches and store all genres
def fetch_genres():
    genres = perform_request("genre")

    for g in genres['genres']:
        genre = Genre(id=g['id'], genre=g['name'])
        db.session.add(genre)

    db.session.commit()


# Fetches and stores all data for a specific movie
def fetch_movie_data(movie_id):
    data = perform_request("movie_info", movie_id)

    if data:
        cast = data['credits']['cast']
        videos = data['videos']['results']

        movie = Movie(id=data['id'], imdb_id=data['imdb_id'], backdrop_path=data['backdrop_path'],
                      poster_path=data['poster_path'], adult=True if (data['adult'] == "true") else False,
                      title=data['title'], original_language=data['original_language'], overview=data['overview'],
                      release_date=_validate_date(data['release_date']), runtime=data['runtime'], status=data['status'],
                      tagline=data['tagline'], homepage=data['homepage'], revenue=data['revenue'],
                      budget=data['budget'])

        for g in data['genres']:
            genre = Genre.query.get(g['id'])
            if not genre:
                continue
            movie.genres.append(genre)

        for c in cast:
            actor = Actor.query.get(c['id'])
            if not actor:
                r = perform_request('person', c['id'])
                actor_null_check( r )
                actor = Actor(id=r['id'], biography=r['biography'], birthday=_validate_date(r['birthday']),
                              deathday=_validate_date(r['deathday']), homepage=r['homepage'],
                              name=r['name'], place_of_birth=r['place_of_birth'],
                              profile_path=r['profile_path'], imdb_id=r['imdb_id'])

            character = Character(character_name=c['character'], actor_name=c['name'], profile_path=c['profile_path'],
                                  cast_id=c['cast_id'], order=c['order'], credit_id=c['credit_id'], actor=actor)

            movie.characters.append(character)

        for v in videos:
            video = Video(iso_639_1=v['iso_639_1'], site=v['site'], key=v['key'], type=v['type'], name=v['name'])
            movie.videos.append(video)

        for c in data['production_countries']:
            country = Country.query.filter_by(iso_3166_1=c['iso_3166_1']).first()
            if country:
                movie.countries.append(country)
            else:
                movie.countries.append(Country(name=c['name'], iso_3166_1=c['iso_3166_1']))

        db.session.add(movie)
        db.session.commit()

# Why is TMDB returning missing keys - bleh
def actor_null_check( actor ):
    if not 'birthdate' in actor:
        actor['birthdate'] = None
    if not 'place_of_birth' in actor:
        actor['place_of_birth'] = None
    if not 'homepage' in actor:
        actor['homepage'] = None
    if not 'deathday' in actor:
        actor['deathday'] = None
    if not 'birthday' in actor:
        actor['birthday'] = None


def fetch_all_movies(limit=None):
    if not limit:
        limit = perform_request("latest_movie")['id']

    i = 0
    while i < limit:
        fetch_movie_data(i)
        i += 1


def _validate_date(date_str):
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
    except:
        return None
    return date
