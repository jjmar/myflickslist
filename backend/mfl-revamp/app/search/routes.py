from app.search import search
from app.models.movie import Movie, Actor
from app.models.user import User
from app.models.list import CustomList
from app.responses import success_response

from flask import request


@search.route('/searchmovies', methods=['GET'])
def movie_search():
    q = request.args.get('q', '')
    page = request.args.get('page', 1)

    response = Movie.query.search(q).paginate(page=page, per_page=10, error_out=False)
    return success_response(results=response)


@search.route('/searchactors', methods=['GET'])
def actor_search():
    q = request.args.get('q', '')
    page = request.args.get('page', 1)


@search.route('/searchlists', methods=['GET'])
def list_search():
    q = request.args.get('q', '')
    page = request.args.get('page', 1)


@search.route('/searchusers', methods=['GET'])
def user_search():
    q = request.args.get('q', '')
    page = request.args.get('page', 1)


