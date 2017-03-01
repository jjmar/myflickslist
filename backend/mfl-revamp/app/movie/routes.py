from app.movie import movie
from app.models.movie import Movie
from app.responses import success_response, error_response
import request_args

from webargs.flaskparser import use_args


@movie.route('/getmoviedetails', methods=['POST'])
@use_args(request_args.get_movie_details_args, locations=('json',))
def get_movie_details(args):
    movie = Movie.query.get(args['movie_id'])

    if not movie:
        return error_response(400, "Movie does not exist")

    response = {}
    for k, v in movie.get_movie_metadata().iteritems():
        response[k] = v
    response['metadata'] = movie.get_movie_statistics()

    return success_response(results=response)
